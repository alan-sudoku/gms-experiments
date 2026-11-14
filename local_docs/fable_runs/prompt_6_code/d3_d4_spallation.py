"""D3, D4: periodic complete spallation and fractional spallation ensemble.

Spec rows: D3, D4 (D4 reuses the D3 routine).  Claim level: derived (unverified).

D3  m(t) = [floor(t/dt) + sqrt(frac(t/dt))] * sqrt(2 kp dt).  Compared with the
    parabolic law sqrt(2 kp t) and with U = sqrt(2 kp t) + t sqrt(2 kp/dt) on a grid
    of 100 points per interval up to N = 1000 intervals.  Report at
    N in {1, 2, 5, 10, 100, 1000}.  The grid is built from integer indices
    (interval i, sub-step j/100) so floor/frac are exact.
D4  n0 = 1/F_A equal patches; patch j (1..n0) spalls completely at intervals
    j, j + n0, ...; each segment of scale growth since the last spall (or t = 0)
    contributes sqrt(2 kp L_seg).  m_ens = mean over patches.  Long-run slope by
    least squares over [10 n0, 20 n0] intervals versus sqrt(2 kp F_A/dt).

Assumptions: kp = 1e-17 m^2/s, dt = 3600 s (cancel in ratios); each patch's
metal loss is the scale thickness removed at a spall plus the current scale
thickness (same bookkeeping as D3).  numpy only.
"""
import math
import numpy as np

KP = 1e-17
DT = 3600.0
C = math.sqrt(2 * KP * DT)           # sqrt(2 kp dt)

# ------------------------------------------------------------------ D3
print("=" * 70)
print("D3: periodic complete spallation  (level: derived)")
print("=" * 70)


def m_periodic(i, f):
    """metal loss at t = (i + f) dt; i integer intervals, f in [0,1)."""
    return (i + np.sqrt(f)) * C


NMAX = 1000
i_idx = np.repeat(np.arange(NMAX), 100)
f_idx = np.tile(np.arange(100) / 100.0, NMAX)
i_idx = np.append(i_idx, NMAX)
f_idx = np.append(f_idx, 0.0)
tau = i_idx + f_idx                                    # t / dt
m = m_periodic(i_idx, f_idx)
par = np.sqrt(2 * KP * DT * tau)
Ub = par + tau * math.sqrt(2 * KP * DT) * 1.0          # t*sqrt(2 kp/dt) = tau*sqrt(2 kp dt)
ok_par = np.all(m >= par * (1 - 1e-12))
ok_U = np.all(m <= Ub * (1 + 1e-12))
print(f"grid points: {len(tau)} (100 per interval, up to N = {NMAX})")
print(f"parabolic <= m at every grid point: {'PASS' if ok_par else 'FAIL'}   "
      f"m <= U at every grid point: {'PASS' if ok_U else 'FAIL'}   (real test, tolerance 1e-9)")
print(f"  min (m - parabolic)/parabolic = {np.min((m - par)[1:]/par[1:]):.3e}, "
      f"min (U - m)/U = {np.min((Ub - m)[1:]/Ub[1:]):.3e}")
print(f"{'N':>6} {'m/parabolic':>14} {'sqrt(N)':>10} {'U/m':>12} {'1+1/sqrt(N)':>12}")
worst = 0.0
for N in (1, 2, 5, 10, 100, 1000):
    k = N * 100
    assert tau[k] == N
    r1 = m[k] / par[k]
    r2 = Ub[k] / m[k]
    worst = max(worst, abs(r1 / math.sqrt(N) - 1), abs(r2 / (1 + 1 / math.sqrt(N)) - 1))
    print(f"{N:6d} {r1:14.9f} {math.sqrt(N):10.6f} {r2:12.9f} {1+1/math.sqrt(N):12.9f}")
print(f"max relative deviation from sqrt(N), 1+1/sqrt(N): {worst:.2e} -> "
      f"{'PASS' if worst < 1e-9 else 'FAIL'} (tolerance 1e-9)")
print("IDENTITY CHECK: the values sqrt(N) and 1 + 1/sqrt(N) at t = N dt follow from the "
      "formula for m by algebra (m = N C, parabolic = sqrt(N) C, U = (sqrt(N)+N) C); "
      "the numbers above test arithmetic, not physics.  The inequality over all grid "
      "points is the real test of the two bounds.")

# ------------------------------------------------------------------ D4
print()
print("=" * 70)
print("D4: fractional spallation ensemble  (level: derived)")
print("=" * 70)


def m_patch(t_int, j, n0):
    """Metal loss of patch j (1..n0) at time t_int (in intervals, array).  Spalls at j, j+n0, ..."""
    t_int = np.asarray(t_int, dtype=float)
    before = t_int < j
    # time since patch's last spall (or since 0 if none yet)
    k = np.floor((t_int - j) / n0)                    # completed later cycles (valid if not before)
    k = np.where(before, -1.0, k)
    last = np.where(before, 0.0, j + k * n0)
    # completed segments: first of length j, then k of length n0 (if not before)
    done = np.where(before, 0.0, math.sqrt(j) + k * math.sqrt(n0))
    cur = np.sqrt(t_int - last)
    return C * (done + cur)


def m_ens(t_int, n0):
    tot = np.zeros_like(np.asarray(t_int, dtype=float))
    for j in range(1, n0 + 1):
        tot += m_patch(t_int, j, n0)
    return tot / n0


for FA in (0.001, 0.01, 0.1):
    n0 = int(round(1 / FA))
    print(f"\nF_A = {FA}: n0 = {n0} patches")
    # long-run slope by least squares over [10 n0, 20 n0] intervals
    ts = np.linspace(10 * n0, 20 * n0, 400)
    me = m_ens(ts, n0)
    slope_per_int, _ = np.polyfit(ts, me, 1)
    slope_expected = math.sqrt(2 * KP * FA / DT) * DT   # per interval
    r = slope_per_int / slope_expected
    print(f"  slope ratio (LSQ) / sqrt(2 kp F_A/dt) = {r:.5f} -> "
          f"{'PASS' if abs(r - 1) <= 0.02 else 'FAIL'} (tolerance 2 %)")
    for mult in (1, 10, 100):
        t = mult * n0
        e = m_ens(np.array([float(t)]), n0)[0]
        p = math.sqrt(2 * KP * DT * t)
        print(f"  t = {mult:3d} n0 dt: m_ens/parabolic = {e/p:8.4f}   sqrt(t/(n0 dt)) = {math.sqrt(mult):7.4f}")
print("\nIDENTITY/CONSISTENCY NOTE: for t >> n0 dt each patch advances by sqrt(2 kp n0 dt) per n0 "
      "intervals by construction, so the slope ratio follows from the patch formula; this is "
      "an asymptote consistency check, as the spec says, not an independent proof.")
