#!/usr/bin/env python3
"""encode_plan.py - GPX + segment JSON -> [[RP1:...]] block (stdlib only, Python 3.8+).

Usage:
  encode_plan.py route.gpx plan.json [--png preview.png] [--tol 15] [--grid 4] [--elev-step 50] [--out block.txt] [--workout-line]
  (--workout-line: stdout/--out = blank line + the one block line, to append to the END of a workout description)

plan.json:
{
  "plan_name": "Tue threshold climbs", "date": "2026-11-17", "route_name": "Kesselberg loop",
  "ftp": 290, "lthr": 168,                      # optional: only used to colour segments (zone 1-7)
  "segments": [ {"start_m": 0, "end_m": 12400, "kind": "P", "low": 150, "high": 170,
                 "label": "Warm-up", "step": 0},      # step = workout step index (0-based), optional
                 ... ],
  "workout_steps": [ {"index": 0, "kind": "P", "low": 150, "high": 170}, ... ]   # optional, for the check
}
Prints the block on stdout (last line), everything else on stderr, so `... > block.txt` works.
Exit code 0 = ok (warnings allowed), 2 = invalid input (overlap, out of range, ...).
"""
import argparse
import json
import os
import struct
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rp1  # noqa: E402

ZONE_RGB = {0: (150, 150, 150), 1: (176, 190, 197), 2: (66, 133, 244), 3: (52, 168, 83), 4: (251, 188, 5),
            5: (234, 120, 40), 6: (200, 40, 40), 7: (120, 30, 120)}


def eprint(*a):
    print(*a, file=sys.stderr)


def validate(plan, total_m):
    """Return (errors, warnings)."""
    errs, warns = [], []
    segs = plan.get("segments", [])
    prev = 0
    for i, s in enumerate(segs):
        tag = "segment %d (%s)" % (i, s.get("label", ""))
        if "start_m" not in s or "end_m" not in s:
            errs.append("%s: missing start_m/end_m" % tag)
            continue
        try:
            tg = rp1.seg_targets(s)
        except (KeyError, ValueError, TypeError, IndexError) as ex:
            errs.append("%s: bad targets (%s)" % (tag, ex))
            continue
        for k, (lo, hi) in tg.items():
            if lo > hi:
                errs.append("%s: %s low > high" % (tag, k))
        if s["end_m"] <= s["start_m"]:
            errs.append("%s: end_m must be greater than start_m" % tag)
        if s["start_m"] < prev:
            errs.append("%s: overlaps or is out of order (starts at %d m, previous ended at %d m)" % (tag, s["start_m"], prev))
        if s["end_m"] > total_m + 25:
            errs.append("%s: ends at %d m but the route is only %d m long" % (tag, s["end_m"], total_m))
        if len(s.get("label", "").encode("utf-8")) > 24:
            warns.append("%s: label longer than 24 bytes, will be cut" % tag)
        prev = s["end_m"]
    if segs and segs[0]["start_m"] > 0:
        warns.append("route starts with %d m not covered by any segment" % segs[0]["start_m"])
    for a, b in zip(segs, segs[1:]):
        if b["start_m"] > a["end_m"]:
            warns.append("gap of %d m between '%s' and '%s' (shown as no target)" % (b["start_m"] - a["end_m"], a.get("label"), b.get("label")))
    steps = {s["index"]: s for s in plan.get("workout_steps", [])}
    for i, s in enumerate(segs):
        st = s.get("step")
        if st is None:
            continue
        w = steps.get(st)
        if w is None:
            if steps:
                warns.append("segment %d links to workout step %d which is not in workout_steps" % (i, st))
            continue
        ts, tw = rp1.seg_targets(s), rp1.seg_targets(w)
        for k in tw:   # every target the workout step has must be identical in the segment
            if ts.get(k) != tw[k]:
                warns.append("TARGET MISMATCH segment %d '%s' %s %s vs workout step %d %s %s" % (i, s.get("label", ""), k, ts.get(k), st, k, tw[k]))
        for k in ts:   # extra targets (e.g. cadence) only on the segment are fine, but say so
            if k not in tw:
                warns.append("note: segment %d has %s target %s that workout step %d does not have (display only)" % (i, k, ts[k], st))
    return errs, warns


# ------------------------------------------------------------------ previews
def ascii_preview(dec, width=100, height=14):
    el = dec["elev_m"]
    total = dec["total_m"]
    lo, hi = min(el), max(el)
    span = max(hi - lo, 1.0)
    cols = []
    for c in range(width):
        i = min(len(el) - 1, int(c * len(el) / width))
        cols.append((el[i] - lo) / span)
    rows = []
    for r in range(height, 0, -1):
        rows.append("".join("#" if cols[c] * height >= r - 0.5 else " " for c in range(width)))
    bar = [" "] * width
    for s in dec["segments"]:
        a = int(s["start_m"] / total * width)
        b = max(a + 1, int(s["end_m"] / total * width))
        ch = str(s["zone"]) if s["zone"] else "?"
        for c in range(a, min(b, width)):
            bar[c] = ch
    lab = [" "] * width
    for s in dec["segments"]:
        a = int(s["start_m"] / total * width)
        t = "%d%s%s" % ((s["low"] + s["high"]) // 2, {"P": "W", "H": "bpm", "C": "rpm"}[s["kind"]], "+" if len(s["targets"]) > 1 else "")
        for k, chh in enumerate(t):
            if a + k < width:
                lab[a + k] = chh
    out = ["elevation %.0f-%.0f m, route %.1f km" % (lo, hi, total / 1000.0), "".join(lab), "".join(bar)] + rows
    out.append("".join("|" if (c * total / width) % 10000 < total / width else "-" for c in range(width)) + "  (| = every 10 km)")
    return "\n".join(out)


def write_png(path, w, h, px):
    raw = b"".join(b"\x00" + bytes(px[y * w * 3:(y + 1) * w * 3]) for y in range(h))

    def chunk(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) +
                chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def png_preview(path, dec, w=900, h=420):
    px = bytearray([255] * (w * h * 3))

    def rect(x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(h, y1)):
            for x in range(max(0, x0), min(w, x1)):
                i = (y * w + x) * 3
                px[i:i + 3] = bytes(c)

    el, total = dec["elev_m"], dec["total_m"]
    lo, hi = min(el), max(el)
    span = max(hi - lo, 1.0)
    L, R, T, B = 20, w - 20, 70, h - 120
    zone_at = lambda m: next((s["zone"] for s in dec["segments"] if s["start_m"] <= m < s["end_m"]), -1)
    for x in range(L, R):
        m = (x - L) / float(R - L) * total
        i = min(len(el) - 1, int(m / dec["elev_step"]))
        y = int(B - (el[i] - lo) / span * (B - T))
        z = zone_at(m)
        rect(x, y, x + 1, B, ZONE_RGB.get(z, (225, 225, 225)) if z >= 0 else (225, 225, 225))
        if z >= 0:
            rect(x, 40, x + 1, 58, ZONE_RGB[z])
    for km in range(0, int(total // 1000) + 1, 5):
        x = L + int(km * 1000.0 / total * (R - L))
        rect(x, B, x + 1, B + (10 if km % 10 == 0 else 5), (0, 0, 0))
    # inset: route shape
    pts = dec["pts"]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    sx, sy = max(max(xs) - min(xs), 1), max(max(ys) - min(ys), 1)
    sc = min((w - 2 * L) / float(sx), (h - B - 30) / float(sy))
    ox, oy = L, h - 10
    prev = None
    for p in pts:
        cx = int(ox + (p[0] - min(xs)) * sc)
        cy = int(oy - (p[1] - min(ys)) * sc)
        if prev:
            n = max(abs(cx - prev[0]), abs(cy - prev[1]), 1)
            for k in range(n + 1):
                rect(prev[0] + (cx - prev[0]) * k // n, prev[1] + (cy - prev[1]) * k // n,
                     prev[0] + (cx - prev[0]) * k // n + 2, prev[1] + (cy - prev[1]) * k // n + 2, (30, 30, 30))
        prev = (cx, cy)
    write_png(path, w, h, px)


# ------------------------------------------------------------------ main
def run(gpx, plan, tol=15.0, grid=4, elev_step=50):
    pts = rp1.read_gpx(gpx)
    data, info = rp1.build_plan(pts, plan, tol=tol, grid=grid, elev_step=elev_step)
    errs, warns = validate(plan, info["total_m"])
    return data, info, errs, warns


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("gpx")
    ap.add_argument("plan")
    ap.add_argument("--workout-line", action="store_true",
                    help="print a blank line + the single block line, ready to append to the END of a workout description "
                         "(stdout and --out); the checks and previews on stderr are unchanged")
    ap.add_argument("--png")
    ap.add_argument("--out")
    ap.add_argument("--tol", type=float, default=15.0)
    ap.add_argument("--grid", type=int, default=4)
    ap.add_argument("--elev-step", type=int, default=50)
    a = ap.parse_args(argv)
    plan = json.load(open(a.plan))
    data, info, errs, warns = run(a.gpx, plan, a.tol, a.grid, a.elev_step)
    for e in errs:
        eprint("ERROR:", e)
    for w in warns:
        eprint("WARNING:", w)
    if errs:
        return 2
    block = rp1.to_block(data)
    dec = rp1.decode_plan(rp1.from_block(block))  # round trip every time
    assert dec["segments"] and dec["total_m"] == int(round(info["total_m"])) or not plan.get("segments")
    km = info["total_m"] / 1000.0
    eprint("route %.1f km, %d GPX points -> %d polyline points (tol %.0f m, grid %d m), %d elevation samples (%d m)" % (
        km, info["points_raw"], info["points_kept"], a.tol, a.grid, info["elev_samples"], a.elev_step))
    eprint("binary %d B, text block %d chars -> %.0f B/km binary, %.0f chars/km" % (info["bytes"], len(block), info["bytes"] / km, len(block) / km))
    eprint("limits: Storage value ~8 KB (docs) | note text must stay intact | see docs/spikes.md for measured limits")
    if len(block) > 5000:
        eprint("WARNING: block is %d characters. Background fetch on the Edge 530 is only safe up to ~5000 characters; "
               "the settings-paste path has no such limit. Options: --tol 25 --elev-step 100, or split the ride into section plans." % len(block))
    if info["missing_ele"]:
        eprint("WARNING: %d GPX points without elevation (filled from neighbours)" % info["missing_ele"])
    eprint(ascii_preview(dec))
    if a.png:
        png_preview(a.png, dec)
        eprint("preview written:", a.png)
    text = ("\n" + block + "\n") if a.workout_line else (block + "\n")
    if a.out:
        open(a.out, "w").write(text)
    sys.stdout.write(text if a.workout_line else block + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
