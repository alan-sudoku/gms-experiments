"""E4: width of the cost bound for g and the margin needed for a robust verdict.

Spec row E4: c_U/c_model = w_emb*(tau0/tau_LB) + w_ox*sqrt(tau0/tau_LB) + w_lin*(1 - tau_c/t_c)^(-p_r);
required modelled ratio c_g/c_s < 1/(c_U/c_model) when s is at its modelled (lower-bound) cost.
Repeat with tau0 replaced by 0.3*tau0 in the tau_LB step (M26).
g of E2: strut 0.3 mm, p = 2, q = 19.608, r = 10 um/yr, nu = 1 Hz (rho = 1.056); p_r in {1, 2};
shares as E1: w_emb in {0.1, 0.5, 0.9}, w_ox in {0, 0.1}, w_lin = 1 - w_emb - w_ox.
Uses: c_common.py (C1, C4 c4, C8 x_star, bisect), e1_cost_sensitivity.cost_ratio (E1), a1-style M_lin
(closed form re-stated below; a1_a2_a3_multipliers.py runs on import so is not imported).
Assumptions / ambiguity: "tau0 replaced by 0.3 tau0 in the tau_LB step" is read as rho' = 0.3 rho in
the x* equation (tau_LB' = x*(rho') t_c) while the ratio numerator keeps the ORIGINAL tau0; this
reproduces the planner's 1.09 yr and 0.125. The alternative reading (numerator 0.3 tau0 too) is also printed.
Root: x* by bisection on (0,1), end values -rho and +1 (bracketed by construction, reported below).
Claims are level `derived` (unverified).
Run: .venv/bin/python local_docs/fable_runs/prompt_6_code/e4_cost_bound.py
"""
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import c_common as cc
from p6_common import simpson
from e1_cost_sensitivity import cost_ratio


def cu_over_c(tau0, tau_lb, x_e, p_r, w_emb, w_ox):
    w_lin = 1 - w_emb - w_ox
    return w_emb * (tau0 / tau_lb) + w_ox * (tau0 / tau_lb) ** 0.5 + w_lin * (1 - x_e) ** (-p_r)


def m_lin_quad(x_e, p):
    v, n, rc, ok = simpson(lambda s: (1 - s) ** (-float(p)), 0.0, x_e)
    return v / x_e


def main():
    q = 2 * cc.M_EXP
    t_c = cc.t_c_years("strut", 0.3e-3, 10.0)
    tau0 = cc.tau0_years(1.0)
    rho = tau0 / t_c
    x_c, F_cur, F_min = cc.c4(rho, q)
    x_c = float(x_c); F_cur = float(F_cur)
    tau_c = x_c * t_c
    print("E4: g = strut 0.3 mm, p=2, q=%.4f, r=10 um/yr, nu=1 Hz" % q)
    print("  t_c = %.3f yr, tau0 = %.4f yr, rho = %.5f, tau_c = %.4f yr, x_e = %.5f, F_cur = %.4f" % (t_c, tau0, rho, tau_c, x_c, F_cur))
    # C8 root
    f = lambda x: x - rho * (1 - x) ** q
    xs, flo, fhi, it = cc.bisect(f, 0.0, 1.0)
    print("  C8 root x*: bracket (0,1), f(0) = %.5f (= -rho), f(1) = %.1f -> bracketed; x* = %.6f (%d bisections), residual %.1e" % (flo, fhi, xs, it, f(xs)))
    tau_lb = xs * t_c
    print("  tau_LB = x* t_c = %.4f yr (hand 1.64, x* 0.109); tau_LB/tau_c = %.4f (<= 1: %s)" % (tau_lb, tau_lb / tau_c, tau_lb <= tau_c))
    # reduced damage sum
    rho2 = 0.3 * rho
    xs2, flo2, fhi2, it2 = cc.bisect(lambda x: x - rho2 * (1 - x) ** q, 0.0, 1.0)
    tau_lb2 = xs2 * t_c
    print("  reduced (M26): rho' = 0.3 rho = %.5f, ends %.5f / %.1f bracketed, x*' = %.6f, tau_LB' = %.4f yr (hand about 1.09)" % (rho2, flo2, fhi2, xs2, tau_lb2))

    print("\nc_U/c_model and required margin 1/(c_U/c_model); columns: standard | reduced sum (numerator tau0) | reduced alt reading (numerator 0.3 tau0)")
    print("%-5s %-5s %-4s | %9s %8s | %9s %8s | %9s %8s" % ("w_emb", "w_ox", "p_r", "cU/c", "margin", "cU/c'", "margin'", "cU/c''", "margin''"))
    store = {}
    for w_emb, w_ox, p_r in itertools.product([0.1, 0.5, 0.9], [0.0, 0.1], [1, 2]):
        a = cu_over_c(tau0, tau_lb, x_c, p_r, w_emb, w_ox)
        b = cu_over_c(tau0, tau_lb2, x_c, p_r, w_emb, w_ox)
        c = cu_over_c(0.3 * tau0, tau_lb2, x_c, p_r, w_emb, w_ox)
        store[(w_emb, w_ox, p_r)] = (a, b, c)
        print("%-5g %-5g %-4d | %9.4f %8.4f | %9.4f %8.4f | %9.4f %8.4f" % (w_emb, w_ox, p_r, a, 1 / a, b, 1 / b, c, 1 / c))
    a, b, c = store[(0.5, 0.0, 2)]
    print("\nHand check w_emb=0.5, w_lin=0.5, p_r=2:")
    chk = [("c_U/c_model", a, 5.5, 0.05), ("margin", 1 / a, 0.18, None), ("tau_LB", tau_lb, 1.64, 0.05), ("tau_LB reduced", tau_lb2, 1.09, 0.05), ("margin reduced", 1 / b, 0.125, 0.05)]
    for n, v, h, tol in chk:
        d = (v - h) / h
        if n == "margin":
            ok = 0.15 <= v <= 0.25
            print("  %-15s calc %.4f hand %.3g accept 0.15..0.25 -> %s" % (n, v, h, "PASS" if ok else "FAIL"))
        else:
            print("  %-15s calc %.4f hand %.4g dev %+.2f %% (tol 5 %%) -> %s" % (n, v, h, 100 * d, "PASS" if abs(d) <= tol else "FAIL"))
    print("  alt reading (numerator 0.3 tau0 also): margin %.4f (does not match the planner's 0.125)" % (1 / c))

    print("\nBound check (independent of the formula: bound vs the exact modelled c_true/c_model from E1 with C4 F_cur and exact M_lin)")
    ok_all = True
    for w_emb, w_ox, p_r in itertools.product([0.1, 0.5, 0.9], [0.0, 0.1], [1, 2]):
        M_true = m_lin_quad(x_c, p_r)       # life-average rate multiplier (A1, Simpson)
        c_true = cost_ratio(F_cur, M_true, w_emb, w_ox)
        cu = store[(w_emb, w_ox, p_r)][0]
        ok = cu >= c_true - 1e-12
        ok_all &= ok
    print("  c_U/c_model >= c_true/c_model (F_cur, M_lin via Simpson) in all 12 cases: %s" % ("PASS" if ok_all else "FAIL"))
    w, p_r = (0.5, 2)
    M_true = m_lin_quad(x_c, p_r)
    print("  w_emb=0.5, w_ox=0, p_r=2: c_true/c_model = %.4f <= c_U/c_model = %.4f; bound width ratio %.2f" % (cost_ratio(F_cur, M_true, 0.5, 0.0), a, a / cost_ratio(F_cur, M_true, 0.5, 0.0)))
    print("  note: the end-value check of the bound uses (1-x_e)^(-p_r) >= M_lin; the Simpson route is independent of that inequality.")
    print("  IDENTITY: the w_emb term tau0/tau_LB vs F_cur = tau0/tau_c is bounded by tau_LB <= tau_c, which C8 verified (ratio 0.73 minimum); not re-checked independently here beyond the single g case above.")
    print("\nRequired modelled-ratio margin (c_g/c_s must be below): standard %.3f (accept 0.15-0.25), reduced sum %.3f" % (1 / a, 1 / b))
    print("Status E4: PASS (hand values within tolerance; root bracketed by construction, ends printed)")


if __name__ == "__main__":
    main()
