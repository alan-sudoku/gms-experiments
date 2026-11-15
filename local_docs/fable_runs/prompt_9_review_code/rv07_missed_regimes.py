"""rv07: missed regimes - cases where every alternative is wrong.

Purpose: compare three rules against a reference ("truth" within the stated model) in four regimes:
 (i)   tau_w,s = inf (current 0.1 evaluation, m_s = 0),
 (ii)  "no outcome" for any finite tau_w,s (current decision table),
 (iii) the answer's three-output rule (claim 8: m_s from a given life on both sides, R_s by claim 3,
       constant Sigma_dot profile; 'g loses' reported as one-sided with omega* = f/(m_s+1)).
 Regimes: A gradually degrading incumbent (age-increasing loss) with a performance limit t_perf;
 B R_s by the incumbent's asymmetric boundary while Sigma_g carries manufacturing (block example);
 C GMS-230 combined-case (paralinear) upper bound on side s, now applied to every unit of side s;
 D GMS-230 consumed-metal convention on side s with retired units (OQ-19), bounds only.
Task: S5 review task 7.
Assumptions: all numbers made up; time in years, costs in J/K; Sigma_dot terms common to both sides cancel;
the paralinear scale obeys d(y^2)/dt = 1 - c y in reduced units (y = x / sqrt(2 k_p)), so the GMS-230 bound
is K sqrt(t) and the truth K y(t); 'truth' means the stated model evaluated without the convention under test.
Level: derived.
"""
import math

from scipy.integrate import solve_ivp

M = 1e6


def verdict(f):
    return "g wins" if f < 0 else ("tie (g does not win)" if f == 0 else "g loses")


print("Regime A: incumbent loss rate sigma0 + beta a, beta = 0.1e6 J/K/yr^2, R_s = 1.0e6 J/K, tau = 20 yr,"
      " t_perf = 10 yr (performance limit, a given life); everything else in f lumped as A = 9.5e6 J/K")
beta, Rs, tau, tperf, A = 0.1 * M, 1.0 * M, 20.0, 10.0, 9.5 * M
Lage = lambda t: beta * t * t / 2
# truth: optimal schedule subject to t_i <= t_perf; convex L -> equal split; search n
best = min(((n - 1) * Rs + n * Lage(tau / n), n) for n in range(math.ceil(tau / tperf), 30))
Ts = math.sqrt(2 * Rs / beta)
ageing_inf = Lage(tau)                         # (i): never replaced, mean rate over the horizon
ms_iii = math.ceil(tau / tperf) - 1           # (iii): given life t_perf
ageing_iii = ms_iii * Rs + (beta * tperf / 2) * tau   # constant Sigma_dot = mean rate over one unit life
mm = math.ceil(tau / Ts) - 1
ageing_claim45_formula = mm * Rs + mm * Lage(Ts) + Lage(tau - mm * Ts)
f_true = A - best[0]
for name, val in [("truth (optimal, n = %d)" % best[1], best[0]), ("(i) tau_w,s = inf", ageing_inf),
                  ("(iii) given life t_perf, m_s = %d" % ms_iii, ageing_iii),
                  ("claims 4-5 with T* = %.3f yr but spec schedule" % Ts, ageing_claim45_formula)]:
    f = A - val
    print(f"  {name:48s}: ageing+replacement = {val / M:7.3f}e6 J/K, f = {f / M:+7.3f}e6 J/K -> {verdict(f)};"
          f" error vs truth {(f - f_true) / M:+7.3f}e6 J/K")
print("  (ii): t_perf < tau gives tau_w,s < inf -> no outcome, although the truth is determinate (g loses)")

print("\nRegime B: block example; truth = symmetric inventory, incumbent manufacturing 1.5e6 J/K per unit")
f_inf = 4.4 * M
f_iii = f_inf - 2 * 1.0 * M
f_truth = f_iii - 3 * 1.5 * M
print(f"  truth: f = {f_truth / M:+.3f}e6 J/K -> {verdict(f_truth)}")
print(f"  (i) f_inf = {f_inf / M:+.3f}e6 J/K -> {verdict(f_inf)}; error {(f_inf - f_truth) / M:+.3f}e6 J/K")
print(f"  (ii) no outcome")
print(f"  (iii) f = {f_iii / M:+.3f}e6 J/K -> {verdict(f_iii)} (one-sided, omega* = {f_iii / 3 / M:.3f}e6 J/K < 1.5e6);"
      f" error {(f_iii - f_truth) / M:+.3f}e6 J/K")

print("\nRegime C: GMS-230 combined case on side s; reduced paralinear scale d(y^2)/dt = 1 - c y, c = 1 yr^-1/2"
      " (steady y = 1 yr^1/2); K_s = 1.0e6 J/(K yr^1/2); R_s = 0.5e6 J/K; tau = 20 yr; tau_w,s = 8 yr;"
      " everything else in f lumped as B = 4.2e6 J/K")
c = 1.0


def y_of(t):
    # z = y^2, dz/dt = 1 - c sqrt(z), z(0) = 0
    if t == 0:
        return 0.0
    sol = solve_ivp(lambda s, z: [1 - c * math.sqrt(max(z[0], 0.0))], (0, t), [0.0], rtol=1e-10, atol=1e-12)
    return math.sqrt(sol.y[0][-1])


Ks, Rs_c, tau, tws, B = 1.0 * M, 0.5 * M, 20.0, 8.0, 4.2 * M
ms = math.ceil(tau / tws) - 1
rem = tau - ms * tws
true_s = ms * Rs_c + Ks * (ms * y_of(tws) + y_of(rem))
bound_iii = ms * Rs_c + Ks * (ms * math.sqrt(tws) + math.sqrt(rem))
bound_i = Ks * math.sqrt(tau)
true_inf = Ks * y_of(tau)
f_true = B - true_s
print(f"  y(8) = {y_of(8):.4f}, y(4) = {y_of(4):.4f}, y(20) = {y_of(20):.4f} (bound sqrt: {math.sqrt(8):.4f}, {math.sqrt(4):.4f}, {math.sqrt(20):.4f})")
print(f"  truth (finite life, paralinear): s-part = {true_s / M:.4f}e6, f = {f_true / M:+.4f}e6 J/K -> {verdict(f_true)}")
for name, val in [("(i) tau_w,s = inf, bound", bound_i), ("(iii) m_s = %d, bound on every unit" % ms, bound_iii)]:
    f = B - val
    print(f"  {name:38s}: s-part = {val / M:.4f}e6, f = {f / M:+.4f}e6 J/K -> {verdict(f)}; error {(f - f_true) / M:+.4f}e6 J/K")
print(f"  bound excess over truth: m_s = 0: {(bound_i - true_inf) / M:.4f}e6 J/K; m_s = {ms}: {(bound_iii - true_s + 0) / M - 0:.4f}e6 J/K"
      " (excess grows with m_s because sum sqrt(t_i) > sqrt(tau))")
print("  (ii): no outcome")

print("\nRegime D: GMS-230 consumed metal on side s with retired units (placeholder values)")
n_cons, Rrec, CExC, T0, ms_d = 50.0, 0.6, 4.0e5, 298.15, 2
under = ms_d * Rrec * CExC * n_cons / T0
print(f"  make-up undercharge bound = m_s R_rec CExC n_cons / T0 = {under:.4e} J/K (n_cons = 50 mol/unit,"
      f" R_rec = 0.6, CExC = 4.0e5 J/mol, m_s = 2): model Sigma_s too low, f too high, favours s (safe for 'g wins')")
print("  a case with 0 < f_model < under is 'g loses' under (i) and (iii) and 'g wins' in truth: wrong but in the"
      " direction the boundary already labels one-sided")
