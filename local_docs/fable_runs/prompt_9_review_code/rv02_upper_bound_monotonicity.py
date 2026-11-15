"""rv02: claims 1 and 7 - f_inf is an upper bound on f, and a shorter tau_w,s never raises f.

Purpose: (a) prove symbolically, for the spec profile (constant Sigma_dot, K >= 0, R >= 0), that
Sigma_s(tau; tau_w,s) is non-increasing in tau_w,s and equals the tau_w,s = inf value for
tau_w,s >= tau, so f(tau_w,s) <= f_inf; check continuity of the oxidation term where m_s changes
and the boundary convention at tau = j*tau_w,s; (b) supplement with an exact-rational scan;
(c) show where it fails: age-increasing Sigma_dot_s, R_s < 0; (d) bound the effect of the GMS-230
consumed-metal convention once side s has retired units.
Task: S5 review task 2.
Assumptions: EQ-LIFECYCLE-REPLACEMENT-COUNT and the k = g case of EQ-LIFECYCLE-SIDE-IRREVERSIBILITY
applied to side s; numbers in (b)-(d) are made up for illustration.
Level: derived.
"""
import math
import random
from fractions import Fraction as Fr

import sympy as sp

print("(a) symbolic proof")
K, tw, tau, m = sp.symbols("K tau_w tau m", positive=True)
r = tau - m * tw  # age of the unit in service, 0 < r <= tw inside a fixed-m interval
O = K * (m * sp.sqrt(tw) + sp.sqrt(r))
dO = sp.simplify(sp.diff(O, tw))
print("  dO/dtau_w at fixed m =", dO)
print("  = (K m / 2) (1/sqrt(tau_w) - 1/sqrt(r)) <= 0 because 0 < r <= tau_w")
# continuity at tau_w = tau/j: from above m = j-1, r = tau_w; from below m = j, r -> 0
j = sp.symbols("j", positive=True, integer=True)
tw_j = tau / j
above = K * ((j - 1) * sp.sqrt(tw_j) + sp.sqrt(tau - (j - 1) * tw_j))
below = sp.limit(K * (j * sp.sqrt(tw) + sp.sqrt(sp.Max(tau - j * tw, 0))), tw, tw_j, "-")
print("  O just above tau/j - O just below tau/j =", sp.simplify(above - K * j * sp.sqrt(tw_j)))
# subadditivity: m sqrt(tw) + sqrt(r) >= sqrt(m tw + r)
a_, b_ = sp.symbols("a b", nonnegative=True)
print("  (sqrt a + sqrt b)^2 - (a+b) =", sp.expand((sp.sqrt(a_) + sp.sqrt(b_)) ** 2 - (a_ + b_)), ">= 0")
print("  so Delta_s = m R_s + K (m sqrt(tw) + sqrt(r) - sqrt(tau)) >= 0 when R_s >= 0, K >= 0")


def m_count(T, w):
    return max(0, math.ceil(Fr(T) / Fr(w)) - 1)


def sigma_s_osc(T, w, Kx, R):
    mm = m_count(T, w)
    rr = Fr(T) - mm * Fr(w)
    return mm * R + Kx * (mm * math.sqrt(w) + math.sqrt(rr)), mm


print("\n(b) exact-rational scan (supplement, not a proof)")
random.seed(9)
viol = 0
checks = 0
for _ in range(300):
    T = Fr(random.randint(10, 400), 10)
    Kx = random.uniform(0, 5)
    R = random.uniform(0, 5)
    ws = sorted({Fr(random.randint(1, 2 * int(T * 10)), 10) for _ in range(60)} | {T / jj for jj in range(1, 8)})
    vals = [sigma_s_osc(T, w, Kx, R)[0] for w in ws]
    inf_val = Kx * math.sqrt(T)
    for i in range(1, len(vals)):
        checks += 1
        if vals[i] > vals[i - 1] + 1e-9:
            viol += 1
    for w, v in zip(ws, vals):
        if v < inf_val - 1e-9:
            viol += 1
print(f"  pairs checked: {checks}; violations of monotonicity or of Sigma_s >= Sigma_s(inf): {viol}")
# boundary: tau = j tau_w gives m = j-1 (not replaced at the horizon)
print("  m_s at tau = 3*tau_w (exact) =", m_count(Fr(24), Fr(8)), "(left-continuous convention, unit not replaced)")

print("\n(c1) age-increasing loss rate sigma_s(a) = sigma0 + beta a (outside the spec profile)")
# per-unit loss L(t) = sigma0 t + beta t^2/2; tau = 20, R_s = 1, beta = 0.1 (made-up units)
T, R, beta = 20.0, 1.0, 0.1


def Ss_age(w):
    if w >= T:
        return beta * T ** 2 / 2
    mm = math.ceil(T / w) - 1
    rr = T - mm * w
    return mm * R + mm * beta * w ** 2 / 2 + beta * rr ** 2 / 2


for w in [1, 2, 4, 5, 6.67, 10, 20, 40]:
    print(f"  tau_w,s = {w:6.2f}: ageing part of Sigma_s = {Ss_age(w):7.3f}")
print("  Sigma_s is U-shaped in tau_w,s: a shorter tau_w,s (10 -> 5) LOWERS Sigma_s, so it RAISES f;"
      " f_inf is no longer an upper bound; f_inf < 0 => 'g wins' is UNSAFE")

print("\n(c2) R_s < 0 (needs a credit term that the spec's R_s terms do not contain)")
for Rn in [-0.5]:
    print(f"  R_s = {Rn}, K = 0, tau = 20, tau_w,s = 8 (m_s = 2): Delta_s = m_s R_s = {2 * Rn} < 0 => f = f_inf + {-2 * Rn}"
          " > f_inf; 'f_inf < 0 => g wins' UNSAFE")
print("  Spec terms for R_s: M_s b_transport/T0 >= 0; Sigma_EOL^ret = n/T0 [R_rec w_remelt + (1-R_rec) CExC] >= 0"
      " given w_lost,remelt >= 0 (exergy destroyed) and CExC >= b_ch >= 0 (REQ-LIFECYCLE-EXTRACTION-WORK-NONNEGATIVE;"
      " b_ch >= 0 is not stated as a REQ: UNSURE)")

print("\n(d) GMS-230 consumed-metal convention with retired units on side s")
# Over_s <= (1-Rrec) * D_s, D_s = total degradation irreversibility of side s (all units);
# Under_s <= m_s * Rrec * CExC * n_cons / T0, which RAISES the true Sigma_s.
# Lower bound on true Sigma_s: finite case minus inf case
Kx, Rrec, Rs = sp.symbols("K R_rec R_s", nonnegative=True)
S = sp.symbols("S", positive=True)  # m sqrt(tw) + sqrt(r) >= sqrt(tau)
sq = sp.symbols("sqrt_tau", positive=True)
lb_fin = m * Rs + Kx * (S - sq) - (1 - Rrec) * Kx * S   # relative to Sigma_s,model(inf)
lb_inf = -(1 - Rrec) * Kx * sq
print("  lower bound(true Sigma_s, finite) - lower bound(true Sigma_s, inf) =",
      sp.factor(sp.simplify(lb_fin - lb_inf)))
print("  = m R_s + R_rec K (S - sqrt(tau)) >= 0: the finite case is never worse for 'g wins' than the 0.1 inf case;"
      " the make-up undercharge on side s lowers the modelled Sigma_s (favours s, safe for 'g wins')")
