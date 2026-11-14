"""E2: error of the verdict ratio for a thin g (strut) and a thick s (wall).

Spec row E2: verdict error = [w_emb*F_g + (1-w_emb)] / [w_emb*F_s + (1-w_emb)].
g: round strut d0 = 0.3 mm, p = 2 (q = 2 m); s: wall h0 = 3 mm, n_s = 1, p = 1 (q = m);
both r = 10 um/yr, nu = 1 Hz. F = F_cur from C4 (c_common.c4, t_c from c_common.t_c_years).
w_emb in {0.1, 0.5, 0.687, 1.0}; 0.687 is replaced by the E3 embodied share (main b_ch, UNSURE) and
the planner's literal 0.687 is also run.
Uses: c_common.py (C1, C3, C4), e1_cost_sensitivity.cost_ratio (E1), e3_a10_shares.shares (E3).
Checks: hand F_g = 7.0, F_s = 1.24, errors 5.7 / 3.6 / 1.56 (tolerance 3 %). Cross-check of the verdict
error against E1's formula with w_ox = 0, M = 1 is an IDENTITY check (same formula). Claims: `derived`.
Run: .venv/bin/python local_docs/fable_runs/prompt_6_code/e2_verdict_error.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_common as cc
from e1_cost_sensitivity import cost_ratio
from e3_a10_shares import shares


def f_cur(kind, size_m, p, n_s=1, r=10.0, nu=1.0):
    tc = cc.t_c_years(kind, size_m, r, n_s)
    rho = cc.tau0_years(nu) / tc
    q = p * cc.M_EXP
    x, F, Fmin = cc.c4(rho, q)
    return dict(tc=tc, rho=rho, q=q, x_e=float(x), tau_c=float(x) * tc, F=float(F), Fmin=float(Fmin))


def verdict_error(w, Fg, Fs):
    return (w * Fg + (1 - w)) / (w * Fs + (1 - w))


def main():
    g = f_cur("strut", 0.3e-3, 2)
    s = f_cur("wall", 3e-3, 1, n_s=1)
    print("E2: verdict error for thin g (strut 0.3 mm, p=2) and thick s (wall 3 mm, n_s=1, p=1), r=10 um/yr, nu=1 Hz")
    for nm, d in (("g", g), ("s", s)):
        print("  %s: t_c = %.3f yr, rho = %.5f, q = %.4f, tau_c = %.4f yr, x_e = %.5f, F_cur = %.4f, F_min = %.4f" %
              (nm, d['tc'], d['rho'], d['q'], d['tau_c'], d['x_e'], d['F'], d['Fmin']))
    print("  hand: F_g = 7.0 (tau_c 2.25 yr, F_min 6.7), F_s = 1.24")
    for nm, v, h in (("F_g", g['F'], 7.0), ("F_s", s['F'], 1.24), ("tau_c_g", g['tau_c'], 2.25), ("F_min_g", g['Fmin'], 6.7)):
        d = (v - h) / h
        print("  %-8s calc %.4f hand %.3g dev %+.2f %% -> %s" % (nm, v, h, 100 * d, "PASS" if abs(d) <= 0.03 else "FAIL (outside 3 %)"))
    e3 = shares()
    w_e3 = e3['w_emb']
    print("\nE3 embodied share (main b_ch 795.7 kJ/mol, UNSURE) = %.4f ; alt b_ch: %.4f" % (w_e3, shares(888.2e3)['w_emb']))
    hand = {1.0: 5.7, 0.5: 3.6, 0.1: 1.56}
    print("\nverdict error  [w F_g + (1-w)] / [w F_s + (1-w)]")
    allpass = True
    out = {}
    for label, w in (("0.1", 0.1), ("0.5", 0.5), ("0.687 (planner literal)", 0.687), ("E3 share %.4f" % w_e3, w_e3), ("1.0", 1.0)):
        v = verdict_error(w, g['F'], s['F'])
        out[label] = v
        line = "  w_emb = %-24s error = %.4f" % (label, v)
        if w in hand:
            h = hand[w]
            d = (v - h) / h
            ok = abs(d) <= 0.03
            allpass &= ok
            line += "  hand %.3g dev %+.2f %% -> %s" % (h, 100 * d, "PASS" if ok else "FAIL")
        # cross-check through E1 (identity: same formula)
        e1 = cost_ratio(g['F'], 1.0, w, 0.0) / cost_ratio(s['F'], 1.0, w, 0.0)
        line += "  [E1 route %.4f, diff %.1e: IDENTITY]" % (e1, abs(e1 - v))
        print(line)
    print("\nverdict error at w_emb = 1: F_g/F_s = %.4f (hand 5.7; computed %.2f %% off)" % (g['F'] / s['F'], 100 * (g['F'] / s['F'] - 5.7) / 5.7))
    print("verdict error is monotone increasing in w_emb on the grid: %s" % ("yes" if out["0.1"] < out["0.5"] < out["1.0"] else "no"))
    print("\nStatus E2: %s (hand values within 3 %%; identity cross-check with E1 flagged)" % ("PASS" if allpass else "FAIL"))


if __name__ == "__main__":
    main()
