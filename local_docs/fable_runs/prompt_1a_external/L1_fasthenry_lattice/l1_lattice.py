"""L1 of the runbook: 3-D node-connected aluminium lattice bar in FastHenry2.

Test run. All results are level `derived` (simulation, not measurement).

Geometry
    Simple-cubic lattice, pitch p, square struts of side t, aluminium (37.7 MS/m).
    Nodes at (i p, j p, k p), i = 0..NX (width), j = 0..NY (thickness), k = 0..NZ (length).
    Every lattice edge is one FastHenry segment (axial along z, transverse along x and y).
    Each end face (k = 0 and k = NZ) is one equipotential node (.equiv); the transverse
    struts lying in the end faces are omitted (they would be shorted by the ideal end plate).
    FastHenry segments overlap at the nodes, so the solver's metal volume is slightly above
    the geometric lattice; the comparison uses the lattice's own computed DC resistance,
    so this does not enter any ratio.
    Envelope used for the solid references: W = NX p + t, T = NY p + t (outer strut faces).

Per-length resistance
    R' = (R(NZ2) - R(NZ1)) / ((NZ2 - NZ1) p): the end regions cancel.

References, same tool, same envelope and lengths (single segment, dense direct solve):
    hom : solid bar with sigma chosen to give the lattice's own DC R' (equal DC resistance)
          (also compared with prompt_1a_code/eddy2d.py in 2-D: column hom/2D, should be ~1)
    Al  : solid aluminium
    Cu  : solid copper

Frequencies: chosen so that T/delta_eff runs from 0.5 to 10 (delta_eff from sigma_hom).

Criteria (review, "single most decisive check"), recorded but not a verdict in this test run:
    C1: lattice (R/R_dc) more than 20 % below hom (R/R_dc) at T >= 6 delta_eff with
        struts thinner than delta_Al  -> would falsify the 1a verdict
    C2: lattice R' below solid Cu R' at any frequency -> would falsify the 1a verdict

Run (pilot):  ~/opt/sim/venv/bin/python l1_lattice.py --nx 8 --ny 4 --nz 16 32 \
                  | tee outputs/l1_pilot.txt
"""
import argparse
import math
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "common"))
sys.path.insert(0, str(HERE.parents[1] / "prompt_1a_code"))
import simtools as st          # noqa: E402
import eddy2d                  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--nx", type=int, default=8)
ap.add_argument("--ny", type=int, default=4)
ap.add_argument("--nz", type=int, nargs=2, default=[16, 32])
ap.add_argument("--pitch", type=float, default=0.5e-3)
ap.add_argument("--fill", type=float, default=0.3)
ap.add_argument("--nf", type=int, default=12, help="number of frequencies")
ap.add_argument("--jobs", type=int, default=12)
ap.add_argument("--tol", type=float, default=1e-5, help="FastHenry GMRES tolerance")
ap.add_argument("--precond", default="off",
                help="FastHenry -p option for the lattice. 'off' is the default here: the "
                     "default sparse preconditioner took ~900 s to build for a 3 800-filament "
                     "lattice that solves in 2 s without it (same R to 6 digits)")
ap.add_argument("--fil", type=int, default=0,
                help="filaments per strut side; 0 = automatic from t/delta_Al")
ap.add_argument("--direct-check", action="store_true",
                help="also solve the lattice with the dense direct solver at one frequency")
ap.add_argument("--tag", default="pilot")
ap.add_argument("--mem-gb", type=float, default=14.0,
                help="memory budget shared by parallel FastHenry jobs")
ap.add_argument("--kb-per-fil", type=float, default=55.0,
                help="memory estimate per lattice filament (measured ~51 kB, -p off)")
args = ap.parse_args()

P = args.pitch
# strut side for a simple-cubic lattice of fill rho: 3 x^2 - 2 x^3 = rho, x = t/p
x = 0.3
for _ in range(60):
    x -= (3 * x * x - 2 * x ** 3 - args.fill) / (6 * x - 6 * x * x)
T_STRUT = x * P
NX, NY = args.nx, args.ny
W_ENV, T_ENV = NX * P + T_STRUT, NY * P + T_STRUT
WORK = st.WORK / f"L1_{args.tag}"
DIRECT = ("-s", "ludecomp", "-m", "direct", "-a", "off")
ITER = ("-t", repr(args.tol), "-p", args.precond)


def nid(i, j, k):
    return 1 + i + (NX + 1) * (j + (NY + 1) * k)


def lattice_deck(nz, f, nfil):
    d = st.FHDeck(f"SC Al lattice {NX}x{NY}x{nz}, p={P*1e3} mm, t={T_STRUT*1e3:.4f} mm")
    for k in range(nz + 1):
        for j in range(NY + 1):
            for i in range(NX + 1):
                d.node(nid(i, j, k), i * P, j * P, k * P)
    e = 0
    for k in range(nz + 1):
        for j in range(NY + 1):
            for i in range(NX + 1):
                if k < nz:                                   # axial
                    e += 1
                    d.seg(e, nid(i, j, k), nid(i, j, k + 1), T_STRUT, T_STRUT, st.S_AL,
                          nfil, nfil, wdir=(1, 0, 0))
                if 0 < k < nz:                               # transverse, not in end faces
                    if i < NX:
                        e += 1
                        d.seg(e, nid(i, j, k), nid(i + 1, j, k), T_STRUT, T_STRUT, st.S_AL,
                              nfil, nfil, wdir=(0, 1, 0))
                    if j < NY:
                        e += 1
                        d.seg(e, nid(i, j, k), nid(i, j + 1, k), T_STRUT, T_STRUT, st.S_AL,
                              nfil, nfil, wdir=(1, 0, 0))
    for k in (0, nz):
        d.equiv([nid(i, j, k) for j in range(NY + 1) for i in range(NX + 1)])
    d.port(nid(0, 0, 0), nid(0, 0, nz))
    d.freqs([f])
    return d


def graded_counts(size, dlt):
    """(n, ratio) for FastHenry filaments across `size` so the edge filament is about
    delta/4, at most 41 filaments, odd count."""
    h0 = dlt / 4
    if size / h0 <= 41:
        n = max(3, int(math.ceil(size / h0)) | 1)
        return n, 1.0
    m = 20                                         # filaments per half, n = 41
    lo, hi = 1.0, 3.0
    for _ in range(80):                            # solve h0 (r^m - 1)/(r - 1) = size/2
        r = 0.5 * (lo + hi)
        if h0 * (r ** m - 1) / (r - 1) > size / 2:
            hi = r
        else:
            lo = r
    return 2 * m + 1, round(0.5 * (lo + hi), 4)


def solid_deck(nz, f, sigma):
    dlt = st.delta(sigma, f)
    nw, rw = graded_counts(W_ENV, dlt)
    nh, rh = graded_counts(T_ENV, dlt)
    return st.fh_solid_bar("solid ref", W_ENV, T_ENV, nz * P, sigma, [f], nw, nh, rw, rh), (nw, nh)


def run_case(name, deck, opts):
    z, wall, rss = st.fh_run(WORK / name, deck, opts)
    return z[0][1], wall, rss


def per_length(r1, r2):
    return (r2 - r1) / ((args.nz[1] - args.nz[0]) * P)


t0 = time.time()
print(f"L1 {args.tag}: lattice {NX} x {NY} cells, lengths {args.nz} cells, pitch {P*1e3} mm, "
      f"strut {T_STRUT*1e3:.4f} mm (t/p = {x:.4f}, fill {args.fill})")
print(f"envelope W x T = {W_ENV*1e3:.4f} x {T_ENV*1e3:.4f} mm; axial lines {(NX+1)*(NY+1)}")

# ---------------------------------------------------------------- DC of the lattice
f_dc = 1e-3
r_dc = {}
for nz in args.nz:
    deck = lattice_deck(nz, f_dc, 1)
    z, wall, rss = run_case(f"dc_{nz}", deck, DIRECT)
    r_dc[nz] = z.real
    print(f"DC lattice nz={nz}: {deck.n_nodes} nodes, {deck.n_segs} segments, "
          f"R = {z.real:.6e} Ohm  [{wall:.1f} s, {rss/1e3:.0f} MB]")
rdc_lat = per_length(r_dc[args.nz[0]], r_dc[args.nz[1]])
rdc_analytic = 1 / (st.S_AL * T_STRUT ** 2 * (NX + 1) * (NY + 1))
print(f"lattice R'_dc = {rdc_lat*1e6:.4f} uOhm/m; analytic 1/(sigma t^2 N_lines) = "
      f"{rdc_analytic*1e6:.4f} uOhm/m ({(rdc_lat/rdc_analytic-1)*100:+.4f} %)")
sig_hom = 1 / (rdc_lat * W_ENV * T_ENV)
print(f"sigma_hom (equal DC) = {sig_hom:.5e} S/m = {sig_hom/st.S_AL:.4f} sigma_Al")

# ---------------------------------------------------------------- frequency sweep
ratios = np.geomspace(0.5, 10, args.nf)                 # T / delta_eff
freqs = [1 / (math.pi * st.MU0 * sig_hom * (T_ENV / q) ** 2) for q in ratios]


def nfil_for(f):
    if args.fil:
        return args.fil
    tq = T_STRUT / st.delta(st.S_AL, f)
    return 1 if tq <= 0.5 else (3 if tq <= 1.5 else 5)


jobs = []
for q, f in zip(ratios, freqs):
    for nz in args.nz:
        jobs.append(("lat", q, f, nz))
        for ref, sg in (("hom", sig_hom), ("Al", st.S_AL), ("Cu", st.S_CU)):
            jobs.append((ref, q, f, nz, sg))


def n_lattice_segs(nz):
    return (NX + 1) * (NY + 1) * nz + (nz - 1) * (NX * (NY + 1) + (NX + 1) * NY)


def est_mem_kb(job):
    if job[0] == "lat":
        return n_lattice_segs(job[3]) * nfil_for(job[2]) ** 2 * args.kb_per_fil
    return 100e3                                   # dense solid bar, <= 41 x 41 filaments


BUDGET_KB = args.mem_gb * 1e6
_used = [0.0]
_cv = threading.Condition()


def do(job):
    need = min(est_mem_kb(job), BUDGET_KB)         # a job bigger than the budget runs alone
    with _cv:
        _cv.wait_for(lambda: _used[0] + need <= BUDGET_KB)
        _used[0] += need
    try:
        kind, q, f, nz = job[:4]
        name = f"{kind}_q{q:.3f}_nz{nz}"
        if kind == "lat":
            nf = nfil_for(f)
            deck = lattice_deck(nz, f, nf)
            z, wall, rss = run_case(name, deck, ITER)
            print(f"  done {name}: {wall:.0f} s, {rss/1e6:.2f} GB "
                  f"(est {est_mem_kb(job)/1e6:.2f} GB)", flush=True)
            return job, z, wall, rss, f"{nf}x{nf} fil/strut, {deck.n_segs} seg"
        deck, (nw, nh) = solid_deck(nz, f, job[4])
        z, wall, rss = run_case(name, deck, DIRECT)
        return job, z, wall, rss, f"{nw}x{nh} fil"
    finally:
        with _cv:
            _used[0] -= need
            _cv.notify_all()


jobs.sort(key=lambda j: -est_mem_kb(j))
res = {}
info = {}
with ThreadPoolExecutor(args.jobs) as ex:
    for job, z, wall, rss, note in ex.map(do, jobs):
        res[(job[0], job[1], job[3])] = z
        info[(job[0], job[1], job[3])] = (wall, rss, note)

# DC references per length for the solid bars
rdc_ref = {"hom": rdc_lat, "Al": 1 / (st.S_AL * W_ENV * T_ENV), "Cu": 1 / (st.S_CU * W_ENV * T_ENV),
           "lat": rdc_lat}

print("\nR' in uOhm/m (length-differenced). k = R/R_dc. t/dAl = strut side / delta_Al.")
print(f"{'T/d_eff':>7s} {'f [Hz]':>11s} {'t/dAl':>6s} {'p/d_eff':>7s} {'R_lat':>10s} {'R_hom':>10s} "
      f"{'R_Al':>10s} {'R_Cu':>10s} {'k_lat':>7s} {'k_hom':>7s} {'k_lat/k_hom':>11s} "
      f"{'lat/Cu':>7s} {'lat/Al':>7s} {'hom/2D':>7s}  fil")
rows = []
for q, f in zip(ratios, freqs):
    R = {kind: per_length(res[(kind, q, args.nz[0])].real, res[(kind, q, args.nz[1])].real)
         for kind in ("lat", "hom", "Al", "Cu")}
    k = {kind: R[kind] / rdc_ref[kind] for kind in R}
    d_eff = T_ENV / q
    tq = T_STRUT / st.delta(st.S_AL, f)
    r2d = eddy2d.solve(eddy2d.solid_bar(W_ENV / 2, T_ENV / 2, sig_hom, f, lvl=2), f)["R"]
    rows.append((q, f, tq, P / d_eff, R, k, R["hom"] / r2d))
    print(f"{q:7.3f} {f:11.4g} {tq:6.3f} {P/d_eff:7.3f} {R['lat']*1e6:10.2f} {R['hom']*1e6:10.2f} "
          f"{R['Al']*1e6:10.2f} {R['Cu']*1e6:10.2f} {k['lat']:7.4f} {k['hom']:7.4f} "
          f"{k['lat']/k['hom']:11.4f} {R['lat']/R['Cu']:7.3f} {R['lat']/R['Al']:7.3f} "
          f"{rows[-1][6]:7.4f}  "
          f"{info[('lat', q, args.nz[1])][2]}")

print("\nCriteria (recorded, not a verdict in this test run):")
c1 = [r for r in rows if r[0] >= 6 and r[2] < 1]
if c1:
    worst = min(r[5]["lat"] / r[5]["hom"] for r in c1)
    print(f"  C1 points (T >= 6 delta_eff and t < delta_Al): {len(c1)}; "
          f"min k_lat/k_hom = {worst:.4f}  -> {'TRIGGERED' if worst < 0.8 else 'not triggered'}")
else:
    print("  C1: no point satisfies T >= 6 delta_eff with t < delta_Al at this size "
          "(expected for the pilot; needs >= 12 cells across)")
mn = min(r[4]["lat"] / r[4]["Cu"] for r in rows)
print(f"  C2: min R_lat/R_Cu = {mn:.3f}  -> {'TRIGGERED' if mn < 1 else 'not triggered'}")

if args.direct_check:
    q, f = ratios[len(ratios) // 2], freqs[len(freqs) // 2]
    d = lattice_deck(args.nz[1], f, 1)
    zi, wi, ri = run_case("chk_iter", d, ITER)
    zd, wd, rd = run_case("chk_direct", d, DIRECT)
    print(f"\nSolver check, lattice nz={args.nz[1]}, 1 fil/strut, T/d_eff={q:.3f}: "
          f"multipole R={zi.real:.8e}, direct R={zd.real:.8e} ({(zi.real/zd.real-1)*100:+.4f} %); "
          f"L: {(zi.imag/zd.imag-1)*100:+.4f} %  [iter {wi:.1f} s {ri/1e3:.0f} MB, "
          f"direct {wd:.1f} s {rd/1e3:.0f} MB]")

print("\nRun cost per case (largest length):")
for (kind, q, nz), (wall, rss, note) in sorted(info.items()):
    if nz == args.nz[1] and kind == "lat":
        print(f"  lat T/d_eff={q:6.3f}: {wall:7.1f} s, {rss/1e3:7.0f} MB, {note}")
mx = max(v[1] for v in info.values())
print(f"peak RSS any case {mx/1e3:.0f} MB; total wall {time.time()-t0:.0f} s")
