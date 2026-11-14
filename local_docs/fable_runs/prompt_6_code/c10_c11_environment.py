"""C10 life factor from an environment S-N curve; C11 environment curve together with section loss.

Spec rows: C10 (needs C1), C11 (needs C3, C10).  LOOKUP inputs L01 (k5, k8): NOT read from a source
(ASM Handbook Vol. 19 is a paywalled book); the planner's UNSURE grid is used; see data/SOURCES.md.
C10: sigma_air(N) = sf (2N)^b; sigma_env(1e5) = k5 sigma_air(1e5); sigma_env(1e8) = k8 sigma_air(1e8);
b_env = log10[sigma_env(1e8)/sigma_env(1e5)]/3; N_env(s) = 1e5 (sigma_env(1e5)/s)^(-1/b_env);
F_env = N_air(s)/N_env(s) at s = sigma_a0; sweep s in [100,400] (61 log points); crossover F_env = 1 by
bisection on ln s (bracket [100,400], extended once x10 per side if no sign change).
Independent check of the crossover: closed form from equating the two power laws (log-linear solve);
the bisection never uses it.
C11: tau0_env = N_env/nu; q_env = p(-1/b_env); tau_c from the C4 formula; F_sec,env = tau0_env/tau_c;
frequency at which F_sec,env = 1.05 by bisection on ln nu in [ln 0.01, ln 10].
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_common import *

S0 = sigma_a0()

def sig_air(N):
    return SIGMA_F * (2.0 * N) ** B_EXP

def N_air(s):
    return 0.5 * (s / SIGMA_F) ** (1.0 / B_EXP)

def env_curve(k5, k8):
    s5 = k5 * sig_air(1e5)
    s8 = k8 * sig_air(1e8)
    b_env = math.log10(s8 / s5) / 3.0
    return s5, s8, b_env

def N_env(s, k5, k8):
    s5, s8, be = env_curve(k5, k8)
    return 1e5 * (s5 / s) ** (-1.0 / be)

def F_env(s, k5, k8):
    return N_air(s) / N_env(s, k5, k8)

def crossover(k5, k8):
    """bisection on ln s of ln F_env; returns (sigma or None, note)."""
    if k5 == 1.0 and k8 == 1.0:
        return None, "null case: F_env = 1 identically, no crossover defined"
    f = lambda ls: math.log(F_env(math.exp(ls), k5, k8))
    for lo, hi, tag in ((100.0, 400.0, "[100,400]"), (10.0, 4000.0, "extended [10,4000]")):
        r, flo, fhi, it = bisect(f, math.log(lo), math.log(hi))
        if r is not None:
            return math.exp(r), "bracketed on %s (ends ln F = %.3f, %.3f)" % (tag, flo, fhi)
        last = (flo, fhi, tag)
    return None, "NO SIGN CHANGE on [100,400] nor on extended [10,4000] (ends ln F = %.3g, %.3g)" % last[:2]

def crossover_closed(k5, k8):
    s5, s8, be = env_curve(k5, k8)
    b = B_EXP
    # (1/b) ln(s/sf) + ln 0.5 = ln 1e5 + (1/be)(ln s - ln s5)
    den = 1.0 / b - 1.0 / be
    if abs(den) < 1e-12:
        return None
    rhs = math.log(1e5) - math.log(0.5) - math.log(s5) / be + math.log(SIGMA_F) / b
    return math.exp(rhs / den)

print("C10  sigma_a0 = %.4f MPa" % S0)
s5, s8, be = env_curve(0.9, 0.4)
Ne = N_env(S0, 0.9, 0.4); F = F_env(S0, 0.9, 0.4)
print("Baseline (k5,k8)=(0.9,0.4): sigma_env(1e5)=%.3f, sigma_env(1e8)=%.3f, b_env=%.5f (exp -0.219), N_env=%.4e (exp 3.2e6), F_env=%.2f (accept 130..180) -> %s" %
      (s5, s8, be, Ne, F, "PASS" if 130 <= F <= 180 else "FAIL"))
cx, note = crossover(0.9, 0.4)
print("   crossover (bisection) sigma=%.3f MPa, N=%.4e (exp near 284 MPa, N ~4.1e4); %s; closed-form-power-law check %.3f" % (cx, N_air(cx), note, crossover_closed(0.9, 0.4)))
print("   hand-value check of 284: %+.2f %%" % ((cx / 284 - 1) * 100))
print()
print("F_env at sigma_a0 for k5=0.9:")
exp = {0.25: 351, 0.3: 269, 0.5: 84, 0.6: 43, 0.8: 8.2}
for k8, e in exp.items():
    v = F_env(S0, 0.9, k8)
    print("   k8=%.2f F_env=%.2f expected %g diff %+.2f%% %s" % (k8, v, e, (v / e - 1) * 100, "PASS" if abs(v / e - 1) <= 0.05 else "FAIL"))
print()
print("Full grid: F_env(sigma_a0), crossover sigma [MPa] (bisection), closed-form power-law crossover, N at crossover; sweep = 61 log points in [100,400]")
sw = np.logspace(math.log10(100), math.log10(400), 61)
for k5 in (0.8, 0.9, 1.0):
    for k8 in (0.25, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0):
        v = F_env(S0, k5, k8)
        cx, note = crossover(k5, k8)
        sign_in_sweep = (np.array([F_env(s, k5, k8) for s in sw]) - 1.0)
        brk = bool(sign_in_sweep.min() < -1e-9 and sign_in_sweep.max() > 1e-9)
        cc = crossover_closed(k5, k8)
        extra = ""
        if k5 == 1.0:
            extra = "  [k5=1: crossover at N=1e5 by construction, not a check]"
        if k5 == k8 == 1.0:
            extra = "  [null case F=1 identically; no crossover]"
        print("   k5=%.1f k8=%.2f F_env=%9.3f  sweep-bracketed=%-5s crossover=%s  closed=%s  %s%s" %
              (k5, k8, v, brk, ("%.2f (N=%.3e)" % (cx, N_air(cx))) if cx else "none", ("%.2f" % cc) if cc else "n/a", note, extra))
print("   null case k5=k8=1: F_env(sigma_a0) = %.12f -> %s" % (F_env(S0, 1, 1), "PASS" if abs(F_env(S0, 1, 1) - 1) < 1e-9 else "FAIL"))
print("   (null case is an IDENTITY: with k5=k8=1 the env curve is the air curve by construction.)")

print("\nC11")
def f_sec(nu, kind, size, r, ns, k5=0.9, k8=0.4):
    s5, s8, be = env_curve(k5, k8)
    Ne = N_env(S0, k5, k8)
    tau0 = Ne / nu / YR
    p = 1 if kind == "wall" else 2
    q = p * (-1.0 / be)
    tc = t_c_years(kind, size, r, ns)
    rho = tau0 / tc
    x = float(tau_c_over_tc(rho, q))
    return tau0 / (x * tc), tau0, q, tc, rho

def nu_threshold(kind, size, r, ns, target=1.05):
    f = lambda ln: f_sec(math.exp(ln), kind, size, r, ns)[0] - target
    return bisect(f, math.log(0.01), math.log(10.0))

expC11 = {0.01: 2.34, 0.1: 1.15, 1: 1.016, 10: 1.002}
print("Wall 0.3 mm, n_s=2, r=10 um/yr (tc=15 yr), baseline (0.9,0.4):")
for nu, e in expC11.items():
    F, tau0, q, tc, rho = f_sec(nu, "wall", 0.3e-3, 10, 2)
    print("   nu=%-5g tau0_env=%.5g yr q_env=%.4f rho=%.5f F_sec,env=%.4f expected %.3f diff %+.2f%% %s" % (nu, tau0, q, rho, F, e, (F / e - 1) * 100, "PASS" if abs(F / e - 1) <= 0.15 else "FAIL"))
r, a, b, it = nu_threshold("wall", 0.3e-3, 10, 2)
print("   nu at F=1.05: %s (end values F-1.05 at 0.01 Hz: %+.4f, at 10 Hz: %+.4f) -> %s" %
      (("%.4f Hz" % math.exp(r)) if r else "not bracketed", a, b, "between 0.1 and 1 Hz: PASS" if r and 0.1 < math.exp(r) < 1 else "FAIL/CHECK"))
print("Strut 0.3 mm, r=10 um/yr (tc=15 yr, p=2):")
for nu in (0.01, 0.1, 1, 10):
    F, tau0, q, tc, rho = f_sec(nu, "strut", 0.3e-3, 10, 1)
    print("   nu=%-5g tau0_env=%.5g yr q_env=%.4f rho=%.5f F_sec,env=%.4f" % (nu, tau0, q, rho, F))
r, a, b, it = nu_threshold("strut", 0.3e-3, 10, 1)
print("   nu at F=1.05: %s (end values %+.4f, %+.4f)" % (("%.4f Hz" % math.exp(r)) if r else "not bracketed in [0.01,10] Hz", a, b))
print("\nFull C3 grid (r, h0/d0, n_s): F_sec,env at nu = 0.01, 0.1, 1, 10 Hz; nu at F=1.05")
for kind, nss in (("wall", (1, 2)), ("strut", (1,))):
    for ns in nss:
        for h in (0.3e-3, 1e-3, 3e-3):
            for r in (1, 3, 10):
                Fs = [f_sec(nu, kind, h, r, ns)[0] for nu in (0.01, 0.1, 1, 10)]
                rt, a, b, it = nu_threshold(kind, h, r, ns)
                if rt is None:
                    thr = "no sign change (F at 0.01 Hz %.3f, 10 Hz %.3f): %s" % (a + 1.05, b + 1.05, "all >1.05 in range" if a > 0 and b > 0 else "all <1.05 in range")
                else:
                    thr = "%.4g Hz" % math.exp(rt)
                print("   %-5s n_s=%d size=%.1f mm r=%-2g  F = %s  nu(1.05)=%s" % (kind, ns, h * 1e3, r, ", ".join("%.4f" % F for F in Fs), thr))
