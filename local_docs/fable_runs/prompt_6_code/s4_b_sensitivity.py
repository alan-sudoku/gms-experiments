"""Prompt 6 S4, script 1 of 2: headline numbers for both candidate Basquin exponents.

Level `derived` (unverified). Neither b value is confirmed (M03 differs: -0.102 planner,
-0.124 secondary table; same sigma_f' = 900 MPa). Headline numbers only; the full row set
is NOT re-run. Self-contained: formulas are restated from prompt_6_plan.md sections 2.6,
2.7 and 3.3, and every b = -0.102 value is compared with the saved S2 output.

Run: python3 s4_b_sensitivity.py > outputs/s4_b_sensitivity.txt
"""
import math

YR = 3.15576e7            # s
UM_YR = 1e-6 / YR         # m/s per (um/yr)
KSI = 6.894757            # MPa
SIGF = 900.0              # MPa, M02
N0 = 5e8                  # cycles, M04
E_AL = 73e9               # Pa, M05
RHO_M = 2780.0            # kg/m3, M06
M_AL = 26.98e-3           # kg/mol, M07
T0 = 298.15               # K, M23
PSI = 2e-3                # M21
E_EMB = 200e6             # J/kg, M27
B_CH = 795.7e3            # J/mol, L04 (revised value)
NU = 1.0                  # Hz
R_CORR = 10.0             # um/yr


def bisect(f, lo, hi, tol=1e-13):
    flo, fhi = f(lo), f(hi)
    if not (flo < 0.0 < fhi or fhi < 0.0 < flo):
        raise ValueError("no sign change: f(lo)=%g f(hi)=%g" % (flo, fhi))
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if (fm < 0.0) == (flo < 0.0):
            lo, flo = mid, fm
        else:
            hi = mid
        if (hi - lo) <= tol * max(abs(hi), 1e-300):
            break
    return 0.5 * (lo + hi)


def tau_c_over_tc(rho, q):
    """C4 closed form: coupled life / t_c, linear recession, Miner."""
    return 1.0 - (1.0 + (q - 1.0) * rho) ** (-1.0 / (q - 1.0))


def fmin_max(q):
    """C6: worst case of F_min over rho (at rho = 1)."""
    return 1.0 / (1.0 - q ** (-1.0 / (q - 1.0)))


def xstar(rho, q):
    """C8: root of x - rho (1-x)^q on (0, 1)."""
    return bisect(lambda x: x - rho * (1.0 - x) ** q, 0.0, 1.0)


def m_lin(xe, p):
    """A1: life-averaged multiplier, linear recession."""
    if abs(p - 1.0) < 1e-12:
        return -math.log(1.0 - xe) / xe
    return ((1.0 - xe) ** (1.0 - p) - 1.0) / ((p - 1.0) * xe)


def env_curve(b, k5, k8):
    s5 = k5 * SIGF * (2e5) ** b
    s8 = k8 * SIGF * (2e8) ** b
    b_env = math.log10(s8 / s5) / 3.0
    return s5, b_env


def f_env(b, k5, k8, sigma):
    s5, b_env = env_curve(b, k5, k8)
    n_air = 0.5 * (sigma / SIGF) ** (1.0 / b)
    n_env = 1e5 * (s5 / sigma) ** (-1.0 / b_env)
    return n_air / n_env, n_env, b_env


def check(label, val, ref, tol=2e-3):
    ok = abs(val - ref) <= tol * abs(ref)
    print("    S2 check %-34s s4 = %-12.6g S2 = %-12.6g %s" % (label, val, ref, "reproduced" if ok else "DIFFERS"))


S2 = {  # saved S2 values at b = -0.102 (file in outputs/ named per entry)
    "sigma_a0": 108.7032,      # c1_c2_baseline.txt
    "fmin_wall": 4.378267,     # c6_c7_worst_case.txt
    "fmin_strut": 6.766141,    # c6_c7_worst_case.txt
    "F_g": 7.0336, "F_s": 1.2443, "tau_c_g": 2.2526,   # e2_verdict_error.txt
    "verr_1": 5.6526, "verr_05": 3.5795, "verr_01": 1.5651,
    "xstar": 0.109263, "margin": 0.1810, "margin_red": 0.1253, "margin_alt": 0.3474,  # e4_cost_bound.txt
    "F_env": 154.106,          # c10_c11_environment.txt
    "w_fat": 0.0999, "w_corr": 0.2138, "w_emb": 0.6863,  # e3_a10_shares.txt
    "a0": 119.22, "lf100": 19.802, "tau_pit": 1.30975,   # c12_c13_pits.txt
    "wsum_impl": 4.1787,       # e5_coupling_numbers.txt
    "N_L07": 4.3557e7,         # c1_c2_baseline.txt
    "Fsec_env_001": 2.3370, "Fsec_env_01": 1.1521, "Fsec_env_1": 1.0156,  # c10_c11_environment.txt
}

print("Prompt 6 S4 script 1: headline numbers for b = -0.102 and b = -0.124 (level derived; neither b confirmed)")
print("Fixed: sigma_f' = 900 MPa, N0 = 5e8 cycles, nu = 1 Hz, r = 10 um/yr; g = round strut d0 = 0.3 mm (p = 2);")
print("       s = wall h0 = 3 mm, one side attacked (p = 1). tau0 = N0/nu does not depend on b, so rho does not either.")
print()

results = {}
for b in (-0.102, -0.124):
    is_ref = abs(b + 0.102) < 1e-12
    r = {}
    m = -1.0 / b
    sig = SIGF * (2.0 * N0) ** b
    tau0 = N0 / NU / YR
    print("=" * 100)
    print("b = %.3f   m = -1/b = %.4f" % (b, m))
    print("=" * 100)

    # ---- C1 / C2
    print("[C1] sigma_a0 = sigma_f' (2 N0)^b = %.4f MPa; tau0(1 Hz) = %.4f yr; eps_a = sigma_a0/E = %.4e" % (sig, tau0, sig * 1e6 / E_AL))
    s_max = sig / KSI
    s_eq = s_max * 2.0 ** 0.56
    if s_eq > 15.8:
        n_l07 = 10 ** (11.1 - 3.97 * math.log10(s_eq - 15.8))
        print("[C2] L07 curve (2024-T3 sheet) at R = -1, S_max = sigma_a0: S_eq = %.4f ksi, N = %.4e, N/N0 = %.4f" % (s_eq, n_l07, n_l07 / N0))
    else:
        n_l07 = float("inf")
        print("[C2] L07 curve (2024-T3 sheet) at R = -1, S_max = sigma_a0: S_eq = %.4f ksi < 15.8 ksi asymptote: L07 gives no finite life (N/N0 = inf)" % s_eq)
    s_eq_n0 = 15.8 + 10 ** ((11.1 - math.log10(N0)) / 3.97)
    sig_l07 = s_eq_n0 / 2.0 ** 0.56 * KSI
    print("[C2] stress amplitude at which L07 gives N0 = 5e8 (R = -1): %.2f MPa (does not depend on b); sigma_a0/that = %.3f" % (sig_l07, sig / sig_l07))
    if is_ref:
        check("sigma_a0", sig, S2["sigma_a0"])
        check("N (L07)", n_l07, S2["N_L07"])

    # ---- B rows that depend on m only
    print("[B6/M2.2] 10^(1/m) = %.4f  -> Miner-vs-min window s/s* in [%.4f, %.4f]" % (10 ** (1 / m), 10 ** (-1 / m), 10 ** (1 / m)))
    print("[B4/M2.3] (1+s)^m: s=0.1: %.3f  s=0.2: %.3f  s=0.5: %.2f  s=1: %.1f" % (1.1 ** m, 1.2 ** m, 1.5 ** m, 2.0 ** m))
    print("[C15/M2.10] displacement control threshold rho* = 1/(m+1) = %.5f" % (1.0 / (m + 1.0)))

    # ---- C6
    fw, fs = fmin_max(m), fmin_max(2.0 * m)
    print("[C6] worst F_min over rho (at rho = 1): wall q = m = %.4f: %.4f ; strut q = 2m = %.4f: %.4f" % (m, fw, 2 * m, fs))
    if is_ref:
        check("F_min,max wall", fw, S2["fmin_wall"])
        check("F_min,max strut", fs, S2["fmin_strut"])

    # ---- C3/C4/E2 for g and s
    tc_g = 0.3e-3 / (2.0 * R_CORR * 1e-6)          # yr, d0/(2r)
    tc_s = 3.0e-3 / (1.0 * R_CORR * 1e-6)          # yr, h0/(n_s r), n_s = 1
    rho_g, rho_s = tau0 / tc_g, tau0 / tc_s
    q_g, q_s = 2.0 * m, m
    xe_g, xe_s = tau_c_over_tc(rho_g, q_g), tau_c_over_tc(rho_s, q_s)
    tauc_g, tauc_s = xe_g * tc_g, xe_s * tc_s
    F_g, F_s = tau0 / tauc_g, tau0 / tauc_s
    Fmin_g = min(tau0, tc_g) / tauc_g
    print("[C4/E2] g: t_c = %.3f yr rho = %.5f q = %.4f tau_c = %.4f yr x_e = %.5f F_cur = %.4f F_min = %.4f" % (tc_g, rho_g, q_g, tauc_g, xe_g, F_g, Fmin_g))
    print("[C4/E2] s: t_c = %.3f yr rho = %.5f q = %.4f tau_c = %.4f yr x_e = %.5f F_cur = %.4f" % (tc_s, rho_s, q_s, tauc_s, xe_s, F_s))
    verr = {}
    for w in (0.1, 0.5, 1.0):
        verr[w] = (w * F_g + (1 - w)) / (w * F_s + (1 - w))
    print("[E2] verdict error [w F_g + (1-w)]/[w F_s + (1-w)]: w_emb = 0.1: %.4f ; 0.5: %.4f ; 1.0: %.4f" % (verr[0.1], verr[0.5], verr[1.0]))
    if is_ref:
        check("F_g", F_g, S2["F_g"]); check("F_s", F_s, S2["F_s"]); check("tau_c(g)", tauc_g, S2["tau_c_g"])
        check("verdict error w=1", verr[1.0], S2["verr_1"]); check("verdict error w=0.5", verr[0.5], S2["verr_05"])
        check("verdict error w=0.1", verr[0.1], S2["verr_01"])

    # ---- C8 / E4
    xs = xstar(rho_g, q_g)
    tlb = xs * tc_g
    xs_red = xstar(0.3 * rho_g, q_g)
    tlb_red = xs_red * tc_g
    end_rate = (1.0 - xe_g) ** (-2.0)

    def cu(w_emb, w_ox, life_ratio, p_r=2.0):
        w_lin = 1.0 - w_emb - w_ox
        return w_emb * life_ratio + w_ox * math.sqrt(life_ratio) + w_lin * (1.0 - xe_g) ** (-p_r)

    c_std = cu(0.5, 0.0, tau0 / tlb)
    c_red = cu(0.5, 0.0, tau0 / tlb_red)
    c_alt = cu(0.5, 0.0, 0.3 * tau0 / tlb_red)
    print("[C8/E4] x* = %.6f tau_LB = %.4f yr (tau_LB/tau_c = %.4f); reduced sum (rho' = 0.3 rho): x*' = %.6f tau_LB' = %.4f yr" % (xs, tlb, tlb / tauc_g, xs_red, tlb_red))
    print("[E4] w_emb = 0.5, w_lin = 0.5, p_r = 2: c_U/c_model = %.4f -> margin = %.4f" % (c_std, 1 / c_std))
    print("[E4]   reduced damage sum, reading A (rho' = 0.3 rho, numerator tau0):    c_U/c_model = %.4f -> margin = %.4f" % (c_red, 1 / c_red))
    print("[E4]   reduced damage sum, reading B (numerator 0.3 tau0 as well):       c_U/c_model = %.4f -> margin = %.4f" % (c_alt, 1 / c_alt))
    grid = [1.0 / cu(we, wo, tau0 / tlb, pr) for we in (0.1, 0.5, 0.9) for wo in (0.0, 0.1) for pr in (1.0, 2.0)]
    print("[E4]   standard margin over the share grid (w_emb 0.1/0.5/0.9, w_ox 0/0.1, p_r 1/2): %.4f to %.4f" % (min(grid), max(grid)))
    c_true = 0.5 * F_g + 0.5 * m_lin(xe_g, 2.0)
    print("[E4]   exact modelled c_true/c_model (w_emb = 0.5, p = 2) = %.4f ; bound/exact = %.3f" % (c_true, c_std / c_true))
    if is_ref:
        check("x*", xs, S2["xstar"]); check("margin", 1 / c_std, S2["margin"])
        check("margin reduced (A)", 1 / c_red, S2["margin_red"]); check("margin reduced (B)", 1 / c_alt, S2["margin_alt"])

    # ---- C10: environment factor, planner range only (L01 has no open source)
    fe, n_env, b_env = f_env(b, 0.9, 0.4, sig)
    print("[C10] baseline (k5, k8) = (0.9, 0.4): b_env = %.5f N_env = %.4e F_env = %.3f   (k5, k8 are the planner's UNSURE range, not data)" % (b_env, n_env, fe))
    row = "  ".join("k8=%.2f: %.1f" % (k8, f_env(b, 0.9, k8, sig)[0]) for k8 in (0.25, 0.30, 0.40, 0.50, 0.60, 0.80))
    print("[C10] k5 = 0.9: " + row)
    allf = [(f_env(b, k5, k8, sig)[0], k5, k8) for k5 in (0.8, 0.9, 1.0) for k8 in (0.25, 0.30, 0.40, 0.50, 0.60)]
    lo, hi = min(allf), max(allf)
    print("[C10] planner range k5 in {0.8, 0.9, 1.0}, k8 in {0.25 .. 0.6}: F_env from %.1f (k5=%.1f, k8=%.2f) to %.1f (k5=%.1f, k8=%.2f)" % (lo[0], lo[1], lo[2], hi[0], hi[1], hi[2]))
    for target, name in ((fs, "F_min,max strut"), (fw, "F_min,max wall")):
        k8x = bisect(lambda k: f_env(b, 0.9, k, sig)[0] - target, 0.4, 1.0)
        print("[C10] k8 at which F_env (k5 = 0.9) falls to %s = %.3f: k8 = %.4f (bracket [0.4, 1.0], sign change confirmed)" % (name, target, k8x))
    if is_ref:
        check("F_env baseline", fe, S2["F_env"])

    # ---- C11 headline: wall 0.3 mm, n_s = 2, environment curve + section loss
    q_env = -1.0 / b_env
    out = []
    for nu in (0.01, 0.1, 1.0):
        t0e = n_env / nu / YR
        rho_e = t0e / 15.0
        out.append(rho_e / tau_c_over_tc(rho_e, q_env))
    print("[C11] wall 0.3 mm, n_s = 2, r = 10: F_sec,env at 0.01 / 0.1 / 1 Hz = %.4f / %.4f / %.4f (q_env = %.4f)" % (out[0], out[1], out[2], q_env))
    if is_ref:
        check("F_sec,env 0.01 Hz", out[0], S2["Fsec_env_001"]); check("F_sec,env 0.1 Hz", out[1], S2["Fsec_env_01"])
        check("F_sec,env 1 Hz", out[2], S2["Fsec_env_1"])

    # ---- E4 with the environment curve applied to g (new in S4; not an S2 row)
    q_ge = 2.0 * q_env
    rho_ge = (n_env / NU / YR) / tc_g
    xs_e = xstar(rho_ge, q_ge)
    xe_ge = tau_c_over_tc(rho_ge, q_ge)
    c_env = 0.5 * tau0 / (xs_e * tc_g) + 0.5 * (1.0 - xe_ge) ** (-2.0)
    print("[E4-env, new] g upper bound with the environment curve (baseline k): tau_LB,env = %.4f yr, c_U/c_model = %.2f -> margin = %.5f" % (xs_e * tc_g, c_env, 1 / c_env))
    for k5, k8 in ((lo[1], lo[2]), (hi[1], hi[2])):
        fe2, n2, b2 = f_env(b, k5, k8, sig)
        rr = (n2 / NU / YR) / tc_g
        qq = 2.0 * (-1.0 / b2)
        c2 = 0.5 * tau0 / (xstar(rr, qq) * tc_g) + 0.5 * (1.0 - tau_c_over_tc(rr, qq)) ** (-2.0)
        print("[E4-env, new]   at (k5, k8) = (%.1f, %.2f), F_env = %.1f: c_U/c_model = %.2f -> margin = %.5f" % (k5, k8, fe2, c2, 1 / c2))

    # ---- C12 / C13 headline (pit as crack-like defect)
    Y = 2.0 * 1.12 / math.pi
    a0 = (1.0 / math.pi) * (3.0 / (Y * 2.0 * sig)) ** 2 * 1e6      # um, dK_th = 3 MPa sqrt(m)
    K100 = math.sqrt(a0 / (a0 + 100.0))
    lf100 = K100 ** (-m)
    t_a = a0 / (10.0 * R_CORR)                                      # yr, PF = 10
    e = m / 2.0 + 1.0
    tau_pit = t_a * ((1.0 + e * tau0 / t_a) ** (1.0 / e) - 1.0)
    t_perf = 300.0 / (2.0 * 10.0 * R_CORR)                          # yr, h0 = 0.3 mm, n_s = 2
    gov = "fatigue from the pit" if tau_pit < t_perf else "perforation"
    print("[C12] a0 (dK_th = 3) = %.2f um ; K(100 um) = %.4f ; life factor K^-m = %.3f" % (a0, K100, lf100))
    print("[C13a] PF = 10, r = 10: tau = %.4f yr (F = %.3f) ; t_perf = %.3f yr ; governing: %s ; life = %.4f yr" % (tau_pit, tau0 / tau_pit, t_perf, gov, min(tau_pit, t_perf)))
    if is_ref:
        check("a0", a0, S2["a0"]); check("life factor 100 um", lf100, S2["lf100"]); check("tau pit PF10 r10", tau_pit, S2["tau_pit"])

    # ---- E3 shares, A10 effect, E5 weighted sum
    d0, ell = 0.3e-3, 3e-3
    V = math.pi * d0 ** 2 * ell / 4.0
    A = math.pi * d0 * ell
    s_fat = NU * V * PSI * (sig * 1e6) ** 2 / (2.0 * E_AL * T0)
    s_corr = R_CORR * UM_YR * A * (RHO_M / M_AL) * B_CH / T0
    s_emb = E_EMB * RHO_M * V / (T0 * tau0 * YR)
    tot = s_fat + s_corr + s_emb
    w_fat, w_corr, w_emb = s_fat / tot, s_corr / tot, s_emb / tot
    print("[E3] rates fat / corr / emb = %.4e / %.4e / %.4e W/K ; shares = %.4f / %.4f / %.4f" % (s_fat, s_corr, s_emb, w_fat, w_corr, w_emb))
    print("[A10] total effect of damage-dependent hysteresis, beta = 5, gamma = 1: 1 + w_fat*2.5 = %.4f" % (1.0 + w_fat * 2.5))
    life_err = F_g - 1.0
    wsum_impl = w_corr * (m_lin(xe_g, 2.0) - 1.0) + w_emb * life_err
    wsum_s4 = w_emb * life_err + w_fat * (m_lin(xe_g, 2.0) - 1.0) + w_corr * (m_lin(xe_g, -1.0) - 1.0)
    print("[E5] weighted sum, S2 implementer's reading (w_corr x rate error p=2 + w_emb x life error): %.4f" % wsum_impl)
    print("[E5] weighted sum, S4 definition c_true/c_model - 1 = w_emb (F_cur-1) + w_fat (M_lin(x_e,2)-1) + w_corr (M_lin(x_e,-1)-1): %.4f" % wsum_s4)
    print("     (terms: embodied %.4f, hysteresis %+.4f, corrosion %+.4f; corrosion rate of a round strut goes as its area, p = -1)" % (w_emb * life_err, w_fat * (m_lin(xe_g, 2.0) - 1.0), w_corr * (m_lin(xe_g, -1.0) - 1.0)))
    verr_e3 = (w_emb * F_g + (1 - w_emb)) / (w_emb * F_s + (1 - w_emb))
    print("[E2] verdict error at the E3 embodied share %.4f: %.4f" % (w_emb, verr_e3))
    if is_ref:
        check("w_fat", w_fat, S2["w_fat"]); check("w_corr", w_corr, S2["w_corr"]); check("w_emb", w_emb, S2["w_emb"])
        check("weighted sum (S2 reading)", wsum_impl, S2["wsum_impl"])

    r.update(sig=sig, m=m, fw=fw, fs=fs, F_g=F_g, F_s=F_s, Fmin_g=Fmin_g, v1=verr[1.0], v05=verr[0.5], v01=verr[0.1],
             margin=1 / c_std, margin_red=1 / c_red, margin_alt=1 / c_alt, fe=fe, fe_lo=lo[0], fe_hi=hi[0],
             lf100=lf100, tau_pit=tau_pit, w_fat=w_fat, w_emb=w_emb, margin_env=1 / c_env, tlb=tlb, tauc_g=tauc_g)
    results[b] = r
    print()

print("=" * 100)
print("Summary: headline number, b = -0.102, b = -0.124, ratio (second/first)")
print("=" * 100)
a, c = results[-0.102], results[-0.124]
rows = [
    ("sigma_a0 [MPa]", "sig"), ("m", "m"), ("F_min,max wall (C6)", "fw"), ("F_min,max strut (C6)", "fs"),
    ("F_cur g (C4)", "F_g"), ("F_min g (C4)", "Fmin_g"), ("F_cur s (C4)", "F_s"), ("tau_c g [yr]", "tauc_g"),
    ("tau_LB g [yr] (C8)", "tlb"),
    ("verdict error w_emb=1 (E2)", "v1"), ("verdict error w_emb=0.5", "v05"), ("verdict error w_emb=0.1", "v01"),
    ("E4 margin (standard)", "margin"), ("E4 margin reduced sum, reading A", "margin_red"),
    ("E4 margin reduced sum, reading B", "margin_alt"), ("E4 margin with env curve on g (new)", "margin_env"),
    ("F_env baseline (C10)", "fe"), ("F_env low end of planner range", "fe_lo"), ("F_env high end of planner range", "fe_hi"),
    ("pit life factor at 100 um (C12)", "lf100"), ("pit life PF=10 r=10 [yr] (C13a)", "tau_pit"),
    ("w_fat (E3)", "w_fat"), ("w_emb (E3)", "w_emb"),
]
for name, key in rows:
    print("  %-40s %12.5g %12.5g   x %.3f" % (name, a[key], c[key], c[key] / a[key]))
print()
print("Ordering test (does the ranking of defects change between the two b values?)")
for b in (-0.102, -0.124):
    r = results[b]
    print("  b = %.3f: F_env low end %.1f > F_min,max strut %.2f > F_min,max wall %.2f : %s" % (
        b, r["fe_lo"], r["fs"], r["fw"], r["fe_lo"] > r["fs"] > r["fw"]))
print("All values level `derived`. b is not confirmed either way; k5, k8 are the planner's range, not data.")
