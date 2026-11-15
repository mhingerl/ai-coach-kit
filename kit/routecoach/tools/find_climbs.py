#!/usr/bin/env python3
"""List climbs of a GPX (stdlib): start/end km, length, gain, average gradient. Helps the coach place segments.
usage: find_climbs.py route.gpx [min_gain_m=40]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rp1, math

def climbs(pts, min_gain=40.0, step=50.0):
    fwd, _ = rp1.make_projection(int(pts[0][0] * 1e6), int(pts[0][1] * 1e6))
    xy = [fwd(p[0], p[1]) for p in pts]
    cum = [0.0]
    for i in range(1, len(xy)):
        cum.append(cum[-1] + math.hypot(xy[i][0] - xy[i - 1][0], xy[i][1] - xy[i - 1][1]))
    n = int(cum[-1] // step) + 1
    el, j = [], 0
    for k in range(n):
        d = k * step
        while j < len(cum) - 2 and cum[j + 1] < d: j += 1
        t = (d - cum[j]) / max(cum[j + 1] - cum[j], 1e-9)
        el.append(pts[j][2] + min(1, max(0, t)) * (pts[j + 1][2] - pts[j][2]))
    el = rp1.smooth(el, 5)
    out, i = [], 0
    while i < n - 1:
        if el[i + 1] > el[i]:
            a = i; lo = el[i]; peak = el[i]; pk = i; k = i
            while k < n - 1 and (el[k + 1] >= peak - 10):
                k += 1
                if el[k] > peak: peak, pk = el[k], k
            gain = peak - lo
            if gain >= min_gain:
                L = (pk - a) * step
                out.append((a * step, pk * step, L, gain, 100.0 * gain / L if L else 0))
            i = max(k, i + 1)
        else:
            i += 1
    return out, cum[-1]

if __name__ == "__main__":
    pts = rp1.read_gpx(sys.argv[1])
    cl, total = climbs(pts, float(sys.argv[2]) if len(sys.argv) > 2 else 40.0)
    print("route %.1f km" % (total / 1000))
    for a, b, L, g, gr in cl:
        print("km %5.1f - %5.1f  length %4.1f km  gain %3.0f m  avg %.1f %%" % (a / 1000, b / 1000, L / 1000, g, gr))
