"""RP1 plan format: GPX reading, simplification, binary encode/decode (stdlib only).

Binary layout (all varints are LEB128, 'zz' = zigzag-signed). See spec/plan-format.md.
"""
import base64
import math
import struct
import xml.etree.ElementTree as ET

EARTH_R = 6371000.0
FMT_VERSION = 1
NO_STEP = 0  # step byte: 0 = none, n = workout step index n-1


# ---------------------------------------------------------------- projection
def make_projection(lat0_e6, lon0_e6):
    """Equirectangular projection to metres around the route origin (same maths as the watch)."""
    lat0 = lat0_e6 / 1e6
    lon0 = lon0_e6 / 1e6
    k = math.pi / 180.0 * EARTH_R
    kx = k * math.cos(math.radians(lat0))

    def fwd(lat, lon):
        return ((lon - lon0) * kx, (lat - lat0) * k)

    def inv(x, y):
        return (lat0 + y / k, lon0 + x / kx)

    return fwd, inv


# ---------------------------------------------------------------- GPX
def read_gpx(path):
    """Return list of (lat, lon, ele_or_None). Uses the first track (all segments) or the first route."""
    root = ET.parse(path).getroot()

    def local(tag):
        return tag.rsplit("}", 1)[-1]

    pts = []
    trks = [e for e in root if local(e.tag) == "trk"]
    rtes = [e for e in root if local(e.tag) == "rte"]
    src = []
    if trks:
        for seg in trks[0]:
            if local(seg.tag) == "trkseg":
                src += [p for p in seg if local(p.tag) == "trkpt"]
    elif rtes:
        src = [p for p in rtes[0] if local(p.tag) == "rtept"]
    for p in src:
        ele = None
        for c in p:
            if local(c.tag) == "ele" and c.text:
                try:
                    ele = float(c.text)
                except ValueError:
                    pass
        pts.append((float(p.get("lat")), float(p.get("lon")), ele))
    if len(pts) < 2:
        raise ValueError("GPX has fewer than 2 track/route points")
    return pts


# ---------------------------------------------------------------- geometry
def douglas_peucker(xy, tol):
    """Iterative Douglas-Peucker; returns sorted kept indices (always includes first and last)."""
    n = len(xy)
    keep = [False] * n
    keep[0] = keep[n - 1] = True
    stack = [(0, n - 1)]
    while stack:
        a, b = stack.pop()
        if b <= a + 1:
            continue
        ax, ay = xy[a]
        bx, by = xy[b]
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy
        best, bi = -1.0, -1
        for i in range(a + 1, b):
            px, py = xy[i]
            if L2 == 0:
                d = math.hypot(px - ax, py - ay)
            else:
                t = ((px - ax) * dx + (py - ay) * dy) / L2
                t = 0.0 if t < 0 else 1.0 if t > 1 else t
                d = math.hypot(px - (ax + t * dx), py - (ay + t * dy))
            if d > best:
                best, bi = d, i
        if best > tol:
            keep[bi] = True
            stack.append((a, bi))
            stack.append((bi, b))
    return [i for i in range(n) if keep[i]]


def smooth(vals, window):
    """Centered moving average (window in samples, odd)."""
    if window <= 1:
        return list(vals)
    h = window // 2
    out = []
    n = len(vals)
    pre = [0.0]
    for v in vals:
        pre.append(pre[-1] + v)
    for i in range(n):
        a, b = max(0, i - h), min(n, i + h + 1)
        out.append((pre[b] - pre[a]) / (b - a))
    return out


# ---------------------------------------------------------------- varints
def put_uv(buf, v):
    if v < 0:
        raise ValueError("negative uvarint")
    while v >= 0x80:
        buf.append((v & 0x7F) | 0x80)
        v >>= 7
    buf.append(v)


def zz(v):
    return (v << 1) if v >= 0 else ((-v << 1) - 1)


def unzz(u):
    return (u >> 1) if not (u & 1) else -((u + 1) >> 1)


def put_sv(buf, v):
    put_uv(buf, zz(v))


def put_str(buf, s, maxlen=40):
    b = s.encode("utf-8")[:maxlen]
    while True:
        try:
            b.decode("utf-8")
            break
        except UnicodeDecodeError:
            b = b[:-1]
    buf.append(len(b))
    buf += b


class Reader:
    def __init__(self, data):
        self.d, self.i = data, 0

    def u8(self):
        v = self.d[self.i]
        self.i += 1
        return v

    def uv(self):
        v = s = 0
        while True:
            b = self.d[self.i]
            self.i += 1
            v |= (b & 0x7F) << s
            if not b & 0x80:
                return v
            s += 7

    def sv(self):
        return unzz(self.uv())

    def s(self):
        n = self.u8()
        v = bytes(self.d[self.i:self.i + n]).decode("utf-8")
        self.i += n
        return v

    def i32(self):
        v = struct.unpack(">i", bytes(self.d[self.i:self.i + 4]))[0]
        self.i += 4
        return v


def crc16(data):
    crc = 0xFFFF
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


# ---------------------------------------------------------------- encode
def zone_for(kind, value, thr):
    """Intensity zone 1..7 from target vs threshold (power: Coggan %FTP; HR: %LTHR)."""
    if not thr:
        return 0
    r = value / float(thr)
    cuts = (0.55, 0.75, 0.90, 1.05, 1.20, 1.50) if kind == "P" else (0.68, 0.83, 0.94, 1.05, 1.21, 1.50)
    z = 1
    for c in cuts:
        if r >= c:
            z += 1
    return z


TARGET_KEYS = ("P", "H", "C")   # power W, heart rate bpm, cadence rpm


def seg_targets(s):
    """Normalise a segment dict to {"P": (lo, hi), "H": ..., "C": ...}. Accepts the short form
    {"kind": "P", "low": 280, "high": 300} or {"targets": {"P": [280, 300], "C": 90}}."""
    out = {}
    if "targets" in s:
        for k, v in s["targets"].items():
            if k not in TARGET_KEYS:
                raise ValueError("unknown target key %r (use P, H, C)" % k)
            lo, hi = (v, v) if isinstance(v, (int, float)) else (v[0], v[1])
            out[k] = (int(lo), int(hi))
    else:
        out[s.get("kind", "P")] = (int(s["low"]), int(s["high"]))
    return out


def seg_zone(s, plan):
    if s.get("zone") is not None:
        return s["zone"]
    t = seg_targets(s)
    if "P" in t:
        return zone_for("P", sum(t["P"]) / 2.0, plan.get("ftp"))
    if "H" in t:
        return zone_for("H", sum(t["H"]) / 2.0, plan.get("lthr"))
    return 0


def build_plan(gpx_pts, plan, tol=15.0, grid=4, elev_step=50, smooth_m=100):
    """gpx_pts: [(lat,lon,ele)], plan: dict (see tools/encode_plan.py). Returns (bytes, info dict)."""
    lat0_e6 = int(round(gpx_pts[0][0] * 1e6))
    lon0_e6 = int(round(gpx_pts[0][1] * 1e6))
    fwd, _ = make_projection(lat0_e6, lon0_e6)
    xy = [fwd(p[0], p[1]) for p in gpx_pts]
    cum = [0.0]
    for i in range(1, len(xy)):
        cum.append(cum[-1] + math.hypot(xy[i][0] - xy[i - 1][0], xy[i][1] - xy[i - 1][1]))
    total_m = cum[-1]

    # --- elevation: resample by distance, smooth, delta-encode
    ele_raw = [p[2] for p in gpx_pts]
    missing = sum(1 for e in ele_raw if e is None)
    last = next((e for e in ele_raw if e is not None), 0.0)
    for i, e in enumerate(ele_raw):
        if e is None:
            ele_raw[i] = last
        last = ele_raw[i]
    n_el = int(total_m // elev_step) + 2
    res, j = [], 0
    for k in range(n_el):
        d = min(k * elev_step, total_m)
        while j < len(cum) - 2 and cum[j + 1] < d:
            j += 1
        seg = cum[j + 1] - cum[j]
        t = 0.0 if seg <= 0 else min(1.0, max(0.0, (d - cum[j]) / seg))
        res.append(ele_raw[j] + t * (ele_raw[j + 1] - ele_raw[j]))
    res = smooth(res, max(1, int(round(smooth_m / elev_step)) | 1))
    ele_q = [int(round(v * 2)) for v in res]  # 0.5 m units

    # --- polyline: DP, quantise to grid, true-distance correction
    keep = douglas_peucker(xy, tol)
    q = []
    for i in keep:
        q.append((int(round(xy[i][0] / grid)), int(round(xy[i][1] / grid))))
    # drop consecutive duplicates after quantisation (keep last point)
    kk, qq = [keep[0]], [q[0]]
    for i in range(1, len(keep)):
        if q[i] != qq[-1]:
            kk.append(keep[i])
            qq.append(q[i])
    keep, q = kk, qq
    if len(q) < 2:
        raise ValueError("route collapses to fewer than 2 points after simplification")
    maxext = max(max(abs(a), abs(b)) for a, b in q)
    if maxext > 32767:
        raise ValueError("route extent %d grid units exceeds int16; use --grid %d" % (maxext, grid * 2))

    buf = bytearray()
    buf.append(FMT_VERSION)
    buf.append(grid)
    buf.append(elev_step // 10)  # elevation spacing in 10 m units (50 m -> 5)
    d = plan["date"].split("-")
    put_uv(buf, int(d[0]) * 10000 + int(d[1]) * 100 + int(d[2]))
    buf += struct.pack(">ii", lat0_e6, lon0_e6)
    put_uv(buf, int(round(total_m)))
    put_str(buf, plan.get("plan_name", ""))
    put_str(buf, plan.get("route_name", ""))

    put_uv(buf, len(q))
    px, py = 0, 0
    drift = 0.0
    prev_true, prev_cum_q = 0.0, 0.0
    pts_info = []
    for n, (gx, gy) in enumerate(q):
        put_sv(buf, gx - px)
        put_sv(buf, gy - py)
        if n > 0:
            chord = math.hypot((gx - px) * grid, (gy - py) * grid)
            true_d = cum[keep[n]] - cum[keep[n - 1]]
            want = true_d - chord + drift
            extra = int(round(want))
            drift = want - extra  # error diffusion keeps cumulative distance within 0.5 m
            put_sv(buf, extra)
        px, py = gx, gy

    put_uv(buf, len(ele_q))
    put_sv(buf, ele_q[0])
    for i in range(1, len(ele_q)):
        put_sv(buf, ele_q[i] - ele_q[i - 1])

    segs = plan.get("segments", [])
    put_uv(buf, len(segs))
    prev_end = 0
    for s in segs:
        a, b = int(s["start_m"]), int(s["end_m"])
        put_uv(buf, a - prev_end)
        put_uv(buf, b - a)
        tg = seg_targets(s)
        mask = sum(1 << i for i, k in enumerate(TARGET_KEYS) if k in tg)
        buf.append(mask | (seg_zone(s, plan) << 3))
        step = s.get("step")
        buf.append(NO_STEP if step is None else step + 1)
        for k in TARGET_KEYS:
            if k in tg:
                put_uv(buf, tg[k][0])
                put_uv(buf, tg[k][1])
        put_str(buf, s.get("label", ""), 24)
        prev_end = b
    buf += struct.pack(">H", crc16(buf))
    info = dict(points_raw=len(gpx_pts), points_kept=len(q), total_m=total_m, elev_samples=len(ele_q),
                missing_ele=missing, segments=len(segs), bytes=len(buf), grid=grid, tol=tol)
    return bytes(buf), info


def to_block(data):
    return "[[RP1:" + base64.urlsafe_b64encode(data).decode().rstrip("=") + "]]"


def from_block(text):
    i = text.index("[[RP1:") + 6
    j = text.index("]]", i)
    s = text[i:j].strip()
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def extract_plan(text):
    """Plan bytes from free text (workout description or note), as the watch does: the first [[RP1:...]] block
    whose checksum is valid. Tolerates prose before/after, CRLF, spaces or line breaks inside the block, a block
    that is the last line without newline. Returns None if there is no valid block (damaged block = None)."""
    pos = 0
    while True:
        i = text.find("[[RP1:", pos)
        if i < 0:
            return None
        j = text.find("]]", i + 6)
        if j < 0:
            return None
        s = "".join(text[i + 6:j].split())
        try:
            data = base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
            if len(data) > 20 and crc16(data[:-2]) == struct.unpack(">H", data[-2:])[0]:
                return data
        except Exception:
            pass
        pos = i + 6


# ---------------------------------------------------------------- decode
def decode_plan(data):
    if crc16(data[:-2]) != struct.unpack(">H", data[-2:])[0]:
        raise ValueError("RP1 checksum mismatch (plan damaged or edited)")
    r = Reader(data)
    ver = r.u8()
    if ver != FMT_VERSION:
        raise ValueError("unsupported RP1 version %d" % ver)
    grid = r.u8()
    elev_step = r.u8() * 10
    ymd = r.uv()
    lat0, lon0 = r.i32(), r.i32()
    total = r.uv()
    plan_name, route_name = r.s(), r.s()
    n = r.uv()
    pts = []
    x = y = 0
    cum = 0.0
    for k in range(n):
        x += r.sv()
        y += r.sv()
        if k > 0:
            px, py = pts[-1][0], pts[-1][1]
            chord = math.hypot((x - px) * grid, (y - py) * grid)
            cum += chord + r.sv()
        pts.append((x, y, cum))
    ne = r.uv()
    e = r.sv()
    elev = [e]
    for _ in range(ne - 1):
        e += r.sv()
        elev.append(e)
    ns = r.uv()
    segs = []
    prev_end = 0
    for _ in range(ns):
        a = prev_end + r.uv()
        b = a + r.uv()
        kz = r.u8()
        step = r.u8()
        tg = {}
        for i, k in enumerate(TARGET_KEYS):
            if kz & (1 << i):
                tg[k] = (r.uv(), r.uv())
        label = r.s()
        prim = next(k for k in TARGET_KEYS if k in tg)
        segs.append(dict(start_m=a, end_m=b, kind=prim, zone=kz >> 3, step=None if step == NO_STEP else step - 1,
                         low=tg[prim][0], high=tg[prim][1], targets=tg, label=label))
        prev_end = b
    return dict(version=ver, grid=grid, elev_step=elev_step, date="%04d-%02d-%02d" % (ymd // 10000, ymd // 100 % 100, ymd % 100),
                lat0_e6=lat0, lon0_e6=lon0, total_m=total, plan_name=plan_name, route_name=route_name,
                pts=pts, elev_m=[v / 2.0 for v in elev], segments=segs)
