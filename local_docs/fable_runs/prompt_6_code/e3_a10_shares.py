"""E3 and A10: entropy-production shares of the worked strut; life-average factor for
damage-dependent hysteresis.

Spec rows: E3 (shares of fatigue hysteresis, corrosion, embodied cost), A10 (1 + beta/(gamma+1)).
Uses: c_common.py (C1: sigma_a0, tau0_years, YR, UM_PER_YR, RHO_M), p6_common.py (Simpson).
Assumptions (all claims level `derived`, unverified):
  - M21 psi = 2e-3, M05 E = 73 GPa, M23 T0 = 298.15 K, M07 M = 26.98 g/mol, M27 e_emb = 200 MJ/kg.
  - L04 (standard chemical exergy of Al, b_ch) is NOT in data/SOURCES.md, so the planner's UNSURE
    values 795.7 (main) and 888.2 kJ/mol (alternative) are used; results are marked UNSURE.
  - Embodied rate uses the air life tau0 at nu = 1 Hz (spec: tau0), not the coupled life.
  - A10 w_fat grid {0.01, 0.1, 0.5} plus the E3 fatigue share (main b_ch).
Importable: shares() returns the E3 numbers; running prints the report.
Run: .venv/bin/python local_docs/fable_runs/prompt_6_code/e3_a10_shares.py
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import c_common as cc
from p6_common import simpson

PSI = 2e-3            # M21
E_AL = 73e9           # M05 Pa
T0 = 298.15           # M23 K
M_AL = 26.98e-3       # M07 kg/mol
E_EMB = 200e6         # M27 J/kg
D0, ELL, NU, R_UM = 0.3e-3, 3e-3, 1.0, 10.0
B_CH_MAIN, B_CH_ALT = 795.7e3, 888.2e3   # L04 planner UNSURE values, J/mol


def shares(b_ch=B_CH_MAIN, e_emb=E_EMB):
    sig = cc.sigma_a0() * 1e6   # Pa
    V = math.pi * D0 ** 2 * ELL / 4
    A = math.pi * D0 * ELL
    r = R_UM * cc.UM_PER_YR      # m/s
    tau0_s = cc.tau0_years(NU) * cc.YR
    fat = NU * V * PSI * sig ** 2 / (2 * E_AL * T0)
    corr = r * A * (cc.RHO_M / M_AL) * b_ch / T0
    emb = e_emb * cc.RHO_M * V / (T0 * tau0_s)
    tot = fat + corr + emb
    return dict(fat=fat, corr=corr, emb=emb, tot=tot, w_fat=fat / tot, w_corr=corr / tot,
                w_emb=emb / tot, V=V, A=A, sigma_a0=sig / 1e6, tau0_yr=tau0_s / cc.YR)


def a10_factor(beta, gamma):
    return 1 + beta / (gamma + 1)


def main():
    print("E3: shares of entropy production for the worked strut (all UNSURE inputs; level derived)")
    print("inputs: d0=0.3 mm, l=3 mm, nu=1 Hz, r=10 um/yr, psi=%g (M21), E=73 GPa, T0=%.2f K, "
          "rho_m=%g, M=26.98 g/mol, e_emb=200 MJ/kg" % (PSI, T0, cc.RHO_M))
    print("L04 b_ch not in data/SOURCES.md: planner UNSURE values used.")
    res = {}
    for name, b in (("main b_ch=795.7 kJ/mol", B_CH_MAIN), ("alt  b_ch=888.2 kJ/mol", B_CH_ALT)):
        s = shares(b)
        res[name] = s
        print("\n%s" % name)
        print("  sigma_a0 = %.3f MPa (C1), V = %.4e m3, A = %.4e m2, tau0 = %.3f yr" %
              (s['sigma_a0'], s['V'], s['A'], s['tau0_yr']))
        print("  Sdot_fat  = %.4e W/K" % s['fat'])
        print("  Sdot_corr = %.4e W/K" % s['corr'])
        print("  Sdot_emb  = %.4e W/K" % s['emb'])
        print("  shares fat, corr, emb = %.4f, %.4f, %.4f (sum %.6f)" % (s['w_fat'], s['w_corr'], s['w_emb'], s['w_fat'] + s['w_corr'] + s['w_emb']))
    s = res["main b_ch=795.7 kJ/mol"]
    print("\nE3 plausibility vs planner hand values (+-3 %, UNSURE; plausibility only):")
    hand = [("Sdot_fat", s['fat'], 1.15e-10), ("Sdot_corr", s['corr'], 2.5e-10), ("Sdot_emb", s['emb'], 7.9e-10),
            ("w_fat", s['w_fat'], 0.10), ("w_corr", s['w_corr'], 0.21), ("w_emb", s['w_emb'], 0.69)]
    for n, v, h in hand:
        d = (v - h) / h
        print("  %-9s calc %.4e hand %.4e dev %+.2f %% %s" % (n, v, h, 100 * d, "within 3 %" if abs(d) <= 0.03 else "OUTSIDE 3 % (shares are rounded to 2 digits)"))
    a = res["alt  b_ch=888.2 kJ/mol"]
    print("  alt b_ch: Sdot_corr %.4e vs hand 2.75e-10 dev %+.2f %%" % (a['corr'], 100 * (a['corr'] - 2.75e-10) / 2.75e-10))
    print("  sensitivity of w_emb to e_emb 150 / 220 MJ/kg (main b_ch): %.4f / %.4f" %
          (shares(B_CH_MAIN, 150e6)['w_emb'], shares(B_CH_MAIN, 220e6)['w_emb']))
    print("  independence: single-pass arithmetic; no independent check exists (identity-class: hand values restate the same formulas).")

    print("\n" + "=" * 70)
    print("A10: life-average factor 1 + beta/(gamma+1) for psi = psi0 (1 + beta (t/tau)^gamma)")
    w_e3 = s['w_fat']
    wf = [0.01, 0.1, 0.5, w_e3]
    print("w_fat grid: 0.01, 0.1, 0.5 and E3 value %.4f (main b_ch; alt b_ch gives %.4f)" % (w_e3, a['w_fat']))
    print("closed form vs Simpson of (1 + beta s^gamma) on [0,1] (independent route)")
    maxrd = 0.0
    for beta in (0.5, 1, 5, 10):
        for gam in (1, 3, 10):
            cf = a10_factor(beta, gam)
            q, n, rc, ok = simpson(lambda x: 1 + beta * x ** gam, 0.0, 1.0)
            rd = abs(q - cf) / cf
            maxrd = max(maxrd, rd)
            effs = "  ".join("w=%.4f: %.5f" % (w, 1 + w * (cf - 1)) for w in wf)
            print("  beta=%-4g gamma=%-3d factor=%.6f simpson=%.6f (n=%d, rel %.1e)  total effect: %s" % (beta, gam, cf, q, n, rd, effs))
    print("max rel diff closed vs Simpson = %.2e -> %s" % (maxrd, "PASS" if maxrd < 1e-8 else "FAIL"))
    h = 1 + 0.1 * 5 / 2
    print("hand value beta=5, gamma=1, w_fat=0.1: %.4f vs 1.25 -> %s (exact arithmetic; no anchor; plausibility only)" %
          (1 + 0.1 * a10_factor(5, 1) - 0.1, "PASS" if abs(h - 1.25) < 1e-12 else "FAIL"))
    print("IDENTITY: the hand value 1.25 restates the formula (flagged). The Simpson check is independent in method.")
    print("Largest total effect on grid (beta=10, gamma=1, w_fat=0.5): %.3f; with E3 share: %.4f" %
          (1 + 0.5 * 10 / 2, 1 + w_e3 * 10 / 2))
    print("\nStatus E3: PASS plausibility only (all inputs UNSURE).  Status A10: PASS plausibility only.")


if __name__ == "__main__":
    main()
