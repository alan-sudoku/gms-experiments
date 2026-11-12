"""Step 2 of the runbook: sanity checks of the two installed solvers.

All results are level `derived` (simulation, not measurement).

G1  GetDP, isolated round Cu wire, R_ac/R_dc against the exact Bessel solution,
    a/delta = 0.5 ... 8, two mesh levels. Tolerance 0.5 % on the finer level.
G2  GetDP, 10 x 10 mm Cu bar, R' against prompt_1a_code/eddy2d.py (fine mesh), 1/10/100 kHz.
    Tolerance 1 %. (Two unrelated methods: finite elements vs volume integral equation.)
F1  FastHenry, DC resistance of a single bar against L/(sigma A). Tolerance 1e-4.
F2  FastHenry, partial self-inductance of a long thin square bar (1 mm x 1 mm x 1 m)
    against the GMD formula mu0 l/(2 pi) [ln(2l/g) - 1 + g/l], g = 0.44705 s.
    Tolerance 0.5 %.
F3  FastHenry, 10 x 10 mm Cu bar, R' by length differencing (1 m and 2 m) against
    eddy2d and G2, 1/10/100 kHz, two filament levels. Tolerance 1 %.
F1-F3 use FastHenry's dense direct solver (-s ludecomp -m direct -a off): with the default
multipole method FastHenry splits a single bar into 8 pieces and a 41 x 41 bar took > 10 min.

Run:  ~/opt/sim/venv/bin/python s2_sanity.py | tee outputs/s2_sanity.txt
"""
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "common"))
sys.path.insert(0, str(HERE.parents[1] / "prompt_1a_code"))
import simtools as st          # noqa: E402
import eddy2d                  # noqa: E402

W = st.WORK / "s2_sanity"
DIRECT = ("-s", "ludecomp", "-m", "direct", "-a", "off")   # exact dense solve for single bars
results = []                   # (check, case, value, reference, rel err, tol, pass)


def record(check, case, val, ref, tol):
    err = (val - ref) / ref
    ok = abs(err) <= tol
    results.append((check, case, val, ref, err, tol, ok))
    print(f"{check:3s} {case:44s} {val:14.6g} {ref:14.6g} {err*100:+8.3f} %  "
          f"(tol {tol*100:.2f} %)  {'PASS' if ok else 'FAIL'}", flush=True)


print("Tools: getdp", st.GETDP.resolve(), "| fasthenry", st.FASTHENRY.resolve())
print(f"{'chk':3s} {'case':44s} {'value':>14s} {'reference':>14s} {'error':>10s}")
t_all = time.time()

# ------------------------------------------------------------------ G1 round wire
a = 5e-3
for x in (0.5, 1, 2, 4, 8):
    f = 1 / (math.pi * st.MU0 * st.S_CU * (a / x) ** 2)
    d = st.delta(st.S_CU, f)
    ref = st.bessel_round_wire_ratio(a, st.S_CU, f)
    for lvl, div in ((1, 4), (2, 8)):
        h = min(d, a) / div
        wd = W / f"G1_x{x}_l{lvl}"
        wd.mkdir(parents=True, exist_ok=True)
        ntri = st.mesh_2d(lambda occ: [(occ.addDisk(0, 0, 0, a, a), 1)], wd / "m.msh",
                          h, 2 * a, 20 * a, 3 * min(d, a))
        r = st.getdp_solve(wd, wd / "m.msh", f, {1: st.S_CU}, {1: 1.0})
        rdc_mesh = 1 / (st.S_CU * r["area"])      # DC of the meshed (polygonal) section
        tol = 0.005 if lvl == 2 else 0.02
        record("G1", f"a/delta={x:<4} h=delta/{div} ({ntri} tri)", r["Z"][1].real / rdc_mesh,
               ref, tol)

# ------------------------------------------------------------------ G2 square bar vs eddy2d
s = 5e-3                              # half side
eddy_ref = {}
for f in (1e3, 1e4, 1e5):
    e = eddy2d.solve(eddy2d.solid_bar(s, s, st.S_CU, f, lvl=2), f)["R"]
    eddy_ref[f] = e
    d = st.delta(st.S_CU, f)
    wd = W / f"G2_{int(f)}"
    wd.mkdir(parents=True, exist_ok=True)
    ntri = st.mesh_2d(lambda occ: [(occ.addRectangle(-s, -s, 0, 2 * s, 2 * s), 1)],
                      wd / "m.msh", min(d, s) / 8, 4 * s, 40 * s, 3 * min(d, s))
    r = st.getdp_solve(wd, wd / "m.msh", f, {1: st.S_CU}, {1: 1.0})
    eddy_ref[("getdp", f)] = r["Z"][1].real
    record("G2", f"10x10 Cu {f/1e3:g} kHz, uOhm/m ({ntri} tri)", r["Z"][1].real * 1e6,
           e * 1e6, 0.01)

# ------------------------------------------------------------------ F1 DC
d1 = st.fh_solid_bar("F1", 10e-3, 10e-3, 1.0, st.S_CU, [1e-3], 1, 1)
z, wall, _ = st.fh_run(W / "F1", d1, DIRECT)
record("F1", "10x10 Cu x 1 m, DC, Ohm", z[0][1].real, 1.0 / (st.S_CU * 1e-4), 1e-4)

# ------------------------------------------------------------------ F2 inductance
sd, ln = 1e-3, 1.0
d2 = st.fh_solid_bar("F2", sd, sd, ln, st.S_CU, [1e-3], 1, 1)
z, wall, _ = st.fh_run(W / "F2", d2, DIRECT)
f0 = z[0][0]
g = 0.44705 * sd
lref = st.MU0 * ln / (2 * math.pi) * (math.log(2 * ln / g) - 1 + g / ln)
record("F2", "1x1 mm x 1 m partial L, H", z[0][1].imag / (2 * math.pi * f0), lref, 0.005)

# ------------------------------------------------------------------ F3 square bar AC
for f in (1e3, 1e4, 1e5):
    for lvl, (n, r_) in enumerate(((21, 1.25), (41, 1.12))):
        R = {}
        for L in (1.0, 2.0):
            dk = st.fh_solid_bar("F3", 2 * s, 2 * s, L, st.S_CU, [f], n, n, r_, r_)
            z, wall, rss = st.fh_run(W / f"F3_{int(f)}_{lvl}_{L}", dk, DIRECT)
            R[L] = z[0][1].real
        rp = (R[2.0] - R[1.0]) / 1.0
        record("F3", f"10x10 Cu {f/1e3:g} kHz, {n}x{n} fil r={r_}, uOhm/m", rp * 1e6,
               eddy_ref[f] * 1e6, 0.01)

print(f"\nSummary: {sum(r[-1] for r in results)}/{len(results)} pass; "
      f"total wall {time.time()-t_all:.0f} s")
for r in results:
    if not r[-1]:
        print("  FAIL:", r[0], r[1])
