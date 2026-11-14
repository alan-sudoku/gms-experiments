"""C17 frequency below which uniform dissolution outruns a threshold crack.

Spec row: C17.  nu_crit = r / (da/dN)_th, r in m/s (1 um/yr = 3.16881e-14 m/s), (da/dN)_th = 1e-10 m/cycle (M16).
Plausibility only.  Not independent: a single division.
"""
UM = 3.16881e-14
for r in (1, 10):
    v = r * UM / 1e-10
    e = {1: 3.2e-4, 10: 3.2e-3}[r]
    print("r=%d um/yr: nu_crit = %.4e Hz (planner %.1e, diff %+.2f%%) %s" % (r, v, e, (v / e - 1) * 100, "PASS" if abs(v / e - 1) <= 0.01 else "FAIL"))
print("Single division of two inputs: plausibility only, no independent check available.")
