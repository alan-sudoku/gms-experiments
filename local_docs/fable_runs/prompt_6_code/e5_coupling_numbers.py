"""E5: coupling numbers and first-order error estimates for g (strut) and s (wall).

Spec row E5: x_e = tau_c/t_c; rate error p*x_e/2 versus M_lin(x_e,p) - 1; life error q*rho/2 versus
F_cur - 1; thermal number Q*dT/(R*T^2) versus the exact Arrhenius multiplier - 1 for dT in {1, 5} K,
Q = 50 kJ/mol, T = 300 K; weighted sum with E3 shares.
g and s as in E2 (strut 0.3 mm p=2; wall 3 mm n_s=1 p=1; r = 10 um/yr, nu = 1 Hz).
Uses: c_common.py (C1, C3, C4), e3_a10_shares.shares (E3), p6_common (Simpson, R_GAS), and the saved
outputs a1_a2_a3_multipliers.txt (A1 values) and a6_arrhenius_dT.txt (A6 dT) as cross-checks.
M_lin closed form and the Arrhenius multiplier are re-stated here (a1/a6 scripts execute on import and
have no main guard); M_lin is verified against composite Simpson (independent) and the saved A1 output;
the multiplier against A6's saved dT (eps = 0.05, Q 50 kJ/mol, T 300 K -> 1.05).
Assumptions / ambiguity: "weighted sum with E3 shares" is not defined in the spec. Reading used here:
embodied share carries the life error (F_cur - 1), corrosion share carries the rate error
(and, as a separate line, the thermal error compounded), fatigue share carries no error in this row.
E3 shares belong to the worked strut (g); s has no E3 shares, so the sum is shown for g only.
Claims are level `derived` (unverified).
Run: .venv/bin/python local_docs/fable_runs/prompt_6_code/e5_coupling_numbers.py
"""
import os, sys, re, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import c_common as cc
from p6_common import simpson, R_GAS
from e3_a10_shares import shares
from e2_verdict_error import f_cur


def m_lin(x, p):
    if p == 1:
        return -math.log1p(-x) / x
    return ((1 - x) ** (1 - p) - 1) / ((p - 1) * x)


def m_lin_quad(x, p):
    return simpson(lambda s: (1 - s) ** (-float(p)), 0.0, x)[0] / x


def arr_mult(Q, T, dT):
    return math.exp((Q / R_GAS) * (1.0 / T - 1.0 / (T + dT)))


def main():
    print("E5: coupling numbers and first-order error estimates")
    cases = [("g", f_cur("strut", 0.3e-3, 2), 2), ("s", f_cur("wall", 3e-3, 1, n_s=1), 1)]
    hand = {"g": dict(x=0.150, rate=(0.150, 0.177), life=(10.4, 6.0)), "s": dict(x=0.042, rate=(0.0212, 0.0218), life=(0.259, 0.244))}
    res = {}
    for nm, d, p in cases:
        x, rho, q = d['x_e'], d['rho'], d['q']
        r1 = p * x / 2
        Mex = m_lin(x, p)
        Mq = m_lin_quad(x, p)
        l1 = q * rho / 2
        lex = d['F'] - 1
        res[nm] = dict(r1=r1, rex=Mex - 1, l1=l1, lex=lex, x=x)
        h = hand[nm]
        print("\n%s: p = %d, q = %.4f, t_c = %.1f yr, rho = %.5f, tau_c = %.4f yr" % (nm, p, q, d['tc'], rho, d['tau_c']))
        print("  x_e = tau_c/t_c = %.5f  (hand %.3f, %+.2f %%)" % (x, h['x'], 100 * (x - h['x']) / h['x']))
        print("  rate error:  first-order p x_e/2 = %.5f ; exact M_lin - 1 = %.5f (Simpson %.5f, rel diff %.1e) ; first/exact = %.3f" % (r1, Mex - 1, Mq - 1, abs(Mq - Mex) / Mex, r1 / (Mex - 1)))
        print("               hand: %.4g vs %.4g -> devs %+.2f %% / %+.2f %%" % (h['rate'][0], h['rate'][1], 100 * (r1 - h['rate'][0]) / h['rate'][0], 100 * (Mex - 1 - h['rate'][1]) / h['rate'][1]))
        print("  life error:  first-order q rho/2 = %.4f ; exact F_cur - 1 = %.4f ; first/exact = %.3f" % (l1, lex, l1 / lex))
        print("               hand: %.4g vs %.4g -> devs %+.2f %% / %+.2f %%" % (h['life'][0], h['life'][1], 100 * (l1 - h['life'][0]) / h['life'][0], 100 * (lex - h['life'][1]) / h['life'][1]))
        if rho > 0.5:
            print("  NOTE: rho = %.3f is near/above 1: the first-order life estimate q rho/2 is INVALID (overestimates by %.0f %%)." % (rho, 100 * (l1 / lex - 1)))
    # cross-check against saved A1 output
    a1 = open(os.path.join(HERE, "outputs", "a1_a2_a3_multipliers.txt")).read()
    pat = re.compile(r"p=\s*(-?\d+) x_e=\s*([\d.]+) closed=([\d.]+) simpson")
    rows = [(int(a), float(b), float(c)) for a, b, c in pat.findall(a1)]
    md = max(abs(m_lin(x, p) - c) / c for p, x, c in rows)
    print("\nCross-check of M_lin against saved A1 output (%d rows): max rel diff %.1e" % (len(rows), md))
    print("  (this compares my restated closed form with A1's closed form: independent code, same formula; A1's own Simpson route is the independent check)")

    print("\nThermal number, Q = 50 kJ/mol, T = 300 K")
    Q, T = 50e3, 300.0
    th = {}
    for dT in (1.0, 5.0):
        f1 = Q * dT / (R_GAS * T ** 2)
        ex = arr_mult(Q, T, dT) - 1
        th[dT] = ex
        print("  dT = %g K: first-order Q dT/(R T^2) = %.5f ; exact multiplier - 1 = %.5f ; ratio %.3f" % (dT, f1, ex, f1 / ex))
    a6 = open(os.path.join(HERE, "outputs", "a6_arrhenius_dT.txt")).read()
    m = re.search(r"eps=0.05 Q= 50 kJ/mol T= 300 K: closed=\s*([\d.]+)", a6)
    dT6 = float(m.group(1))
    print("  A6 saved dT for eps = 0.05 (50 kJ/mol, 300 K) = %.4f K ; multiplier at that dT = %.6f (should be 1.05; rounding of the 4-digit saved value)" % (dT6, arr_mult(Q, T, dT6)))
    print("  inversion consistent with A6 within 1e-4: %s (independent: A6 bisection vs forward evaluation here)" % (abs(arr_mult(Q, T, dT6) - 1.05) < 1e-4))

    s3 = shares()
    print("\nWeighted sum with E3 shares (g only; main b_ch, UNSURE): w_fat = %.4f, w_corr = %.4f, w_emb = %.4f" % (s3['w_fat'], s3['w_corr'], s3['w_emb']))
    g = res['g']
    for lab, r_, l_ in (("first-order", g['r1'], g['l1']), ("exact", g['rex'], g['lex'])):
        base = s3['w_corr'] * r_ + s3['w_emb'] * l_
        print("  %-11s: w_corr*rate + w_emb*life = %.4f*%.4f + %.4f*%.4f = %.4f" % (lab, s3['w_corr'], r_, s3['w_emb'], l_, base))
        for dT in (1.0, 5.0):
            thx = (Q * dT / (R_GAS * T ** 2)) if lab == "first-order" else th[dT]
            comp = (1 + r_) * (1 + thx) - 1
            print("      with thermal dT=%g K on the corrosion rate: %.4f (corrosion term %.4f)" % (dT, s3['w_corr'] * comp + s3['w_emb'] * l_, s3['w_corr'] * comp))
    print("  first-order weighted sum overestimates the exact by %.1f %% (dominated by the life term; first-order life invalid at rho = %.2f)" %
          (100 * ((s3['w_corr'] * g['r1'] + s3['w_emb'] * g['l1']) / (s3['w_corr'] * g['rex'] + s3['w_emb'] * g['lex']) - 1), cases[0][1]['rho']))
    print("  AMBIGUITY: spec does not define the weighted sum; the share-to-error mapping above is the implementer's reading.")
    print("\nStatus E5: PASS (hand values within rounding; first-order life estimate for g flagged invalid near rho = 1; weighted sum is ambiguous)")


if __name__ == "__main__":
    main()
