"""Record the finished cases of the stopped L1 pilot (test run, level `derived`).

The pilot (8 x 4 cells, lengths 32 and 64 cells, pitch 0.5 mm) was stopped on 2026-11-13
after the end-point test (T/delta_eff = 0.5 and 10). This script reads the FastHenry
outputs left in ~/opt/sim/work/L1_pilot_ends and prints what can be derived from them.
It runs no solver.

Run:  ~/opt/sim/venv/bin/python l1_partial_record.py | tee outputs/l1_pilot_partial.txt
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "common"))
import simtools as st          # noqa: E402

W = st.WORK / "L1_pilot_ends"
NX, NY, NZ = 8, 4, (32, 64)
P = 0.5e-3
x = 0.3
for _ in range(60):
    x -= (3 * x * x - 2 * x ** 3 - 0.3) / (6 * x - 6 * x * x)
T_STRUT = x * P
W_ENV, T_ENV = NX * P + T_STRUT, NY * P + T_STRUT
DL = (NZ[1] - NZ[0]) * P


def z_of(name):
    p = W / name / "Zc.mat"
    if not p.exists():
        return None
    r = st.fh_parse_zc(p)
    return r[0] if r else None


def rss_wall(name):
    log = (W / name / "fasthenry.log").read_text(errors="replace")
    rss = next((int(l.split()[1]) for l in log.splitlines() if l.startswith("MAXRSS_KB")), None)
    tot = next((float(l.split()[1]) for l in log.splitlines() if l.strip().startswith("Total:")),
               None)
    return rss, tot


print(f"Lattice {NX} x {NY} cells, pitch {P*1e3} mm, strut {T_STRUT*1e3:.4f} mm, "
      f"envelope {W_ENV*1e3:.4f} x {T_ENV*1e3:.4f} mm, lengths {NZ} cells "
      f"(differencing length {DL*1e3:.0f} mm)")

dc = [z_of(f"dc_{n}") for n in NZ]
rdc = (dc[1][1].real - dc[0][1].real) / DL
rdc_an = 1 / (st.S_AL * T_STRUT ** 2 * (NX + 1) * (NY + 1))
sig_hom = 1 / (rdc * W_ENV * T_ENV)
print(f"DC: lattice R' = {rdc*1e6:.2f} uOhm/m; analytic 1/(sigma t^2 N_lines) = {rdc_an*1e6:.2f} "
      f"({(rdc/rdc_an-1)*100:+.4f} %); sigma_hom = {sig_hom:.4e} S/m = {sig_hom/st.S_AL:.4f} sigma_Al")
rdc_ref = {"lat": rdc, "hom": rdc, "Al": 1 / (st.S_AL * W_ENV * T_ENV),
           "Cu": 1 / (st.S_CU * W_ENV * T_ENV)}

for q in (0.5, 10.0):
    print(f"\n== T/delta_eff = {q}")
    z = {(k, n): z_of(f"{k}_q{q:.3f}_nz{n}") for k in ("lat", "hom", "Al", "Cu") for n in NZ}
    f = next(v[0] for v in z.values() if v)
    print(f"f = {f:.6g} Hz; delta_Al = {st.delta(st.S_AL, f)*1e3:.4f} mm; "
          f"t/delta_Al = {T_STRUT/st.delta(st.S_AL, f):.3f}; pitch/delta_eff = {P/(T_ENV/q):.3f}")
    for k in ("lat", "hom", "Al", "Cu"):
        for n in NZ:
            v = z[(k, n)]
            rw = rss_wall(f"{k}_q{q:.3f}_nz{n}")
            print(f"  {k:3s} nz={n:2d}: " + (f"R = {v[1].real:.6e} Ohm, X = {v[1].imag:.6e} Ohm"
                                              if v else "NOT FINISHED (stopped)")
                  + (f"   [{rw[1]:.1f} s, {rw[0]/1e6:.2f} GB]" if v and rw[0] else ""))
    R = {}
    for k in ("lat", "hom", "Al", "Cu"):
        if z[(k, NZ[0])] and z[(k, NZ[1])]:
            R[k] = (z[(k, NZ[1])][1].real - z[(k, NZ[0])][1].real) / DL
    for k, v in R.items():
        print(f"  per-length {k:3s}: R' = {v*1e6:10.2f} uOhm/m, R/R_dc = {v/rdc_ref[k]:.4f}")
    if "lat" in R:
        print(f"  k_lat/k_hom = {(R['lat']/rdc)/(R['hom']/rdc):.4f}; lat/Cu = {R['lat']/R['Cu']:.3f}; "
              f"lat/Al = {R['lat']/R['Al']:.3f}")
    else:
        a, b = z[("lat", NZ[0])], z[("hom", NZ[0])]
        c = z[("Cu", NZ[0])]
        print(f"  no per-length lattice value (nz={NZ[1]} not finished). Single length nz={NZ[0]} "
              f"only, end effects included, NOT a per-length result: R_lat/R_hom = "
              f"{a[1].real/b[1].real:.4f}, R_lat/R_Cu = {a[1].real/c[1].real:.3f}")
