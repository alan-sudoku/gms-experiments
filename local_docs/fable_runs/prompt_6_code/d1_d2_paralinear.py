"""D1, D2: Tedmon paralinear solution, its bounds, and an independent ODE integration.

Spec rows: D1 (closed form / root solution and bounds), D2 (RK4 of the ODE and a
dimensional example).  Claim level: derived (unverified).

Method summary
  D1  For each theta solve theta = -y - ln(1-y) for y in [0,1) by bisection
      (log1p; for theta > 30 use y = 1 - exp(-theta - 1)).  m = y + theta,
      U = sqrt(2 theta) + theta, L = max(sqrt(2 theta), theta).
      Maxima of U/m (golden section on ln theta) and of m/L (kink at theta = 2).
  D2  RK4 on dy/dtheta = (1-y)/y from y0 = sqrt(2 th0) - (2/3) th0, th0 = 1e-6,
      with geometric step growth h = min(eps*theta, eps), eps halved until y at
      theta in {0.1, 1, 2, 3.5, 10, 100} changes by < 0.1 %.  Compared with D1.
      Dimensional example: delta_lim = kp'/kl, t(theta=2) = 2 kp'/kl^2.

Independence of D2 from D1
  D1 uses the *integrated* relation theta(y) and a root solve (no ODE).
  D2 uses only the *differential* equation dy/dtheta = (1-y)/y, a series start
  and RK4; it never evaluates -y - ln(1-y).  So D2 checks the integration and the
  root solve numerically.  It does NOT check the derivation of the dimensionless
  ODE from d(delta)/dt = kp'/delta - kl (that is shared; done by hand in the
  planner's section 2.4: dy/dtheta = 1/y - 1).

Assumptions
  * kp' follows the plan's convention delta*d(delta)/dt = kp' (no loss).
  * L05 constants are converted from Opila and Hann 1997 (see data/SOURCES.md);
    the conversion is the implementer's, marked UNSURE.
  * numpy and plain Python only.
"""
import math
import numpy as np


# ---------------------------------------------------------------- helpers
def bisect(f, lo, hi, rel=1e-12, maxit=400):
    """Bisection; returns (root, flo, fhi, bracketed)."""
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return None, flo, fhi, False
    for _ in range(maxit):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if fm == 0.0:
            return mid, flo, fhi, True
        if flo * fm < 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
        if (hi - lo) <= rel * max(abs(hi), abs(lo), 1e-300):
            break
    return 0.5 * (lo + hi), flo, fhi, True


def golden_max(f, a, b, tol=1e-10):
    gr = (math.sqrt(5) - 1) / 2
    c, d = b - gr * (b - a), a + gr * (b - a)
    fc, fd = f(c), f(d)
    while abs(b - a) > tol:
        if fc > fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a)
            fd = f(d)
    x = 0.5 * (a + b)
    return x, f(x)


def solve_y(theta):
    """y(theta) from theta = -y - ln(1-y).  Returns (y, method)."""
    if theta > 30.0:
        return 1.0 - math.exp(-theta - 1.0), "asym"
    g = lambda y: -y - math.log1p(-y) - theta
    r, _, _, ok = bisect(g, 0.0, 1.0 - 1e-16)
    assert ok
    return r, "bisect"


def mt(theta):
    y, _ = solve_y(theta)
    return y + theta


def U(theta):
    return math.sqrt(2 * theta) + theta


def L(theta):
    return max(math.sqrt(2 * theta), theta)


# ---------------------------------------------------------------- D1
print("=" * 70)
print("D1: Tedmon paralinear solution and bounds  (level: derived)")
print("=" * 70)
lt = np.arange(-4 * 20, 4 * 20 + 1) / 20.0          # log10 theta, 20 per decade
th = 10.0 ** lt
n_asym = int(np.sum(th > 30))
ys, ms = [], []
maxres = 0.0
th_maxres = None
for t in th:
    y, meth = solve_y(t)
    ys.append(y)
    ms.append(y + t)
    if meth == "bisect":
        r = abs(-y - math.log1p(-y) - t) / t
        if r > maxres:
            maxres, th_maxres = r, t
ys, ms = np.array(ys), np.array(ms)
Uu = np.array([U(t) for t in th])
Ll = np.array([L(t) for t in th])
print(f"grid: {len(th)} points, theta {th[0]:g} .. {th[-1]:g}, {n_asym} points use the "
      "asymptotic form y = 1 - exp(-theta-1) (theta > 30)")
print(f"max relative residual |theta(y)-theta|/theta (bisection points) = {maxres:.3e} at theta = {th_maxres:.3g}\n"
      "  (y is converged to 1e-12 in y, but 1-y ~ exp(-theta) is below that for theta > ~20, so the "
      "theta-residual is large there; m = y + theta is unaffected at 1e-12)")
# bound test (real test: bounds come from the inequalities of 2.4, m from the root)
viol_U = np.sum(ms > Uu * (1 + 1e-12))
viol_L = np.sum(ms < Ll * (1 - 1e-12))
print(f"bound test L <= m <= U at every grid point: violations of U = {viol_U}, of L = {viol_L}"
      f" -> {'PASS' if viol_U == 0 and viol_L == 0 else 'FAIL'}  (real test: independent bounds)")
print(f"min m/L = {np.min(ms/Ll):.6f}, max U/m = {np.max(Uu/ms):.6f}")

# max of U/m
rat = Uu / ms
i = int(np.argmax(rat))
print(f"U/m coarse grid maximum at index {i} (theta = {th[i]:.4g}), value {rat[i]:.6f}; "
      f"interior = {0 < i < len(th) - 1}")
if 0 < i < len(th) - 1:
    f1 = lambda s: U(math.exp(s)) / mt(math.exp(s))
    s, v = golden_max(f1, math.log(th[i - 1]), math.log(th[i + 1]))
    print(f"  golden-section on ln theta: theta* = {math.exp(s):.6f}, max U/m = {v:.6f}")
    print(f"  spec check: max in [1.35, 1.39] -> {'PASS' if 1.35 <= v <= 1.39 else 'FAIL'}; "
          f"theta in [2.5, 4.5] -> {'PASS' if 2.5 <= math.exp(s) <= 4.5 else 'FAIL'}; "
          f"hand value 1.369 within 1 %: {'PASS' if abs(v/1.369-1) <= 0.01 else 'FAIL'}")
    print("  (golden-section position is only good to ~1e-8 in ln theta: flat maximum, "
          "function error eps ~ 1e-16)")
else:
    print("  maximum at a grid end -> would need to extend (not the case here)")

# max of m/L, kink at 2
rat2 = ms / Ll
j = int(np.argmax(rat2))
print(f"m/L coarse grid maximum at index {j} (theta = {th[j]:.4g}), value {rat2[j]:.6f}; "
      f"interior = {0 < j < len(th) - 1}")
f2 = lambda s: mt(math.exp(s)) / L(math.exp(s))
sl, vl = golden_max(f2, math.log(th[j - 1]), math.log(2.0))
sr, vr = golden_max(f2, math.log(2.0), math.log(th[j + 1]))
print(f"  golden left of kink: theta = {math.exp(sl):.6f}, {vl:.6f}; right of kink: "
      f"theta = {math.exp(sr):.6f}, {vr:.6f}")
y2, _ = solve_y(2.0)
print(f"  at theta = 2: y = {y2:.6f}, m = {y2 + 2:.6f}, L = 2, m/L = {(y2 + 2)/2:.6f}")
print(f"  spec check: m/L(2) hand 1.474 within 1 %: {'PASS' if abs((y2+2)/2/1.474-1) <= 0.01 else 'FAIL'}; "
      f"y(2) hand 0.9475 within 1 %: {'PASS' if abs(y2/0.9475-1) <= 0.01 else 'FAIL'}")
print("  note: U/L <= 2 with equality at theta = 2 (kink): U(2)/L(2) = "
      f"{U(2.0)/L(2.0):.6f}")

# limits
t = 1e-4
y, _ = solve_y(t)
print(f"limit theta -> 0:  (m - sqrt(2 theta))/(theta/3) at theta = 1e-4: "
      f"{(y + t - math.sqrt(2*t))/(t/3):.6f}  (expect 1)")
t = 1e4
y, _ = solve_y(t)
print(f"limit theta -> inf: m - theta at theta = 1e4: {y + t - t:.12f}  (expect 1; "
      "this value is y itself and uses the asymptotic form, so it is by construction"
      " IDENTITY-like for theta > 30)")
print("D1 hand values: y(1) =", f"{solve_y(1.0)[0]:.4f}", "(0.8414), y(3.5) =",
      f"{solve_y(3.5)[0]:.4f}", "(0.9888)")

# ---------------------------------------------------------------- D2
print()
print("=" * 70)
print("D2: RK4 of dy/dtheta = (1-y)/y, independent of D1  (level: derived)")
print("=" * 70)
targets = [0.1, 1.0, 2.0, 3.5, 10.0, 100.0]
th0 = 1e-6


def rk4_run(eps):
    f = lambda y: (1.0 - y) / y
    t, y = th0, math.sqrt(2 * th0) - (2.0 / 3.0) * th0
    out = []
    nsteps = 0
    for tg in targets:
        while t < tg * (1 - 1e-15):
            h = min(eps * t, eps)
            if t + h > tg:
                h = tg - t
            k1 = f(y)
            k2 = f(y + 0.5 * h * k1)
            k3 = f(y + 0.5 * h * k2)
            k4 = f(y + h * k3)
            y += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
            t += h
            nsteps += 1
        out.append(y)
    return np.array(out), nsteps


eps = 0.1
prev, n = rk4_run(eps)
print(f"{'eps':>10} {'steps':>8}  y at theta = " + "  ".join(f"{t:g}" for t in targets) + "   max rel change")
print(f"{eps:10.5g} {n:8d}  " + "  ".join(f"{v:.6f}" for v in prev))
conv_eps = None
for k in range(1, 9):
    eps /= 2
    cur, n = rk4_run(eps)
    ch = np.max(np.abs(cur / prev - 1))
    print(f"{eps:10.5g} {n:8d}  " + "  ".join(f"{v:.6f}" for v in cur) + f"   {ch:.3e}")
    if ch < 1e-3 and conv_eps is None:
        conv_eps = eps
    prev = cur
y_rk = prev
print(f"step-halving criterion (< 0.1 % change): first met at eps = {conv_eps}; "
      f"final value used is the finest run (eps = {eps:g})")
y_d1 = np.array([solve_y(t)[0] for t in targets])
rel = np.abs(y_rk / y_d1 - 1)
print("comparison with D1 (bisection root):")
for t, a, b, r in zip(targets, y_rk, y_d1, rel):
    print(f"  theta = {t:7.3f}: RK4 y = {a:.8f}, D1 y = {b:.8f}, rel diff = {r:.2e}")
print(f"max rel diff {rel.max():.2e} -> {'PASS' if rel.max() < 1e-3 else 'FAIL'} (tolerance 0.1 %)")
for t, h in [(1.0, 0.8414), (2.0, 0.9475), (3.5, 0.9888)]:
    v = y_rk[targets.index(t)]
    print(f"  hand value y({t}) = {h}: RK4 {v:.4f}, rel dev {abs(v/h-1):.2e}")

# dimensional example
print()
print("Dimensional example (delta_lim = kp'/kl, t(theta=2) = 2 kp'/kl^2)")
# L05 conversion from Opila and Hann 1997, J. Am. Ceram. Soc. 80(1):197-205
# SiC, 50 % H2O / 50 % O2, 1200 C, 4.4 cm/s; values read from Fig. 4 / Tables III, IV
kp_w = 2.7e-3            # mg^2/(cm^4 h)   (Fig. 4; Table III: 2.72e-3)
kl_w = 5.3e-3            # mg SiO2/(cm^2 h) (Fig. 4; Table IV: 5.27e-3)
conv = 13.6              # um per (mg/cm^2), amorphous silica (paper Eq. 16)
rho_sio2 = 2.2           # g/cm^3 (paper, amorphous silica)
kp_thick = conv ** 2 * kp_w                  # um^2/h, paper kp' (x^2 = kp' t)
kl_thick = kl_w * 1e-3 / rho_sio2 * 1e4      # um/h  (mass loss / density)
print(f"  paper-convention kp' = {kp_thick:.4f} um^2/h (paper Fig. 1 typical: 0.50), "
      f"kl = {kl_thick:.4f} um/h (paper Fig. 1 typical: 0.02)")
print(f"  limiting thickness kp'/(2 kl) = {kp_thick/(2*kl_thick):.2f} um (paper text: 6.9 um from "
      "all 1200 C data; not reproduced: UNSURE, see issues)")
kp_p = 0.5 * kp_thick * 1e-12 / 3600.0       # m^2/s, plan convention delta*d(delta)/dt = kp'
kl_s = kl_thick * 1e-6 / 3600.0              # m/s
for name, kp_, kl_ in [("L05 (Opila-Hann conversion, UNSURE)", kp_p, kl_s),
                       ("fallback (parametric)", 1e-17, 1e-12)]:
    print(f"  {name}: kp' = {kp_:.4e} m^2/s, kl = {kl_:.4e} m/s -> delta_lim = {kp_/kl_*1e6:.3f} um, "
          f"t(theta=2) = {2*kp_/kl_**2:.4e} s = {2*kp_/kl_**2/86400:.1f} d")
print("  fallback expected: delta_lim = 10 um, t(theta=2) = 2e7 s -> "
      f"{'PASS' if abs(1e-17/1e-12*1e6-10) < 1e-9 and abs(2e-17/1e-24-2e7) < 1e-3 else 'FAIL'}"
      "  (these two are arithmetic identities of the formulas, flagged IDENTITY)")
