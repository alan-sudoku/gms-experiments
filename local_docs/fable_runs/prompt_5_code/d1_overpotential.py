#!/usr/bin/env python3
"""D1: overpotential price of a lower exchange current (Butler-Volmer vs Tafel).
Spec row D1. Claims G1.7, G2.1, G2.5. Level: derived (unverified).
j = R_f j0 [exp(alpha F eta/RT) - exp(-(1-alpha) F eta/RT)] (formula as written in the spec; for alpha>1 the "cathodic" exponent has the
opposite sign, see issues_a.md). Solve eta by brentq for incumbent s and candidate g (j0_g = j0_s/kappa, R_f ratio r = R_f,g/R_f,s);
Delta eta = eta_g - eta_s vs Tafel b log10(kappa/r), b = 2.303 R T/(alpha F).
Sweep: kappa in [1,1e6] (25 log points), alpha in {0.5,1,1.5,2}, j in {2e3,5e3,1e4,2e4} A/m2, T in {298.15, 353.15} K,
j0_s in {1e-3, 1e1} A/m2, r in {1,10,100,1000}. Output: power penalty j*Delta eta/T0 (W/K per m2).
No LOOKUP values. Published value b(0.5, 298.15)=118.3 mV/dec: 2.303RT/F = 59.16 mV is a textbook constant (not confirmed from a source in this run).
"""
import numpy as np
from scipy.optimize import brentq
F, R, T0 = 96485.332, 8.314462, 298.15
def eta_solve(j, jref, alpha, T):
    f = lambda e: jref*(np.exp(alpha*F*e/(R*T)) - np.exp(-(1-alpha)*F*e/(R*T))) - j
    tafel = (R*T/(alpha*F))*np.log(max(j/jref, 1.0)) + 1e-9
    hi = 2*tafel + 0.2
    while f(hi) < 0: hi *= 2
    lo = 1e-12
    return brentq(f, lo, hi, xtol=1e-14, rtol=1e-13)
kap = np.logspace(0, 6, 25); alphas = (0.5, 1.0, 1.5, 2.0); js = (2e3, 5e3, 1e4, 2e4); Ts = (298.15, 353.15); j0s = (1e-3, 1e1); rs = (1, 10, 100, 1000)
print("INPUTS: F=96485.332, R=8.314462, T0=298.15; sweep as in docstring. No lookup.")
b05 = 2.303*R*298.15/(0.5*F)*1e3; b1 = 2.303*R*298.15/F*1e3
print(f"b(alpha=0.5, 298.15 K) = {b05:.2f} mV/dec (spec 118.3); 2.303RT/F = {b1:.2f} mV (published 59.16)")
for a in alphas: print(f"  b(alpha={a}, 298.15 K) = {2.303*R*298.15/(a*F)*1e3:.1f} mV/dec")
fails = 0
ok = abs(b05-118.3) < 0.2 and abs(b1-59.16) < 0.05; fails += (not ok); print(f"CHECK b values -> {'PASS' if ok else 'FAIL'}")
rows = []
for T in Ts:
  for a in alphas:
    for j in js:
      for j0 in j0s:
        for r in rs:
          for k in kap:
            es = eta_solve(j, 1.0*j0, a, T); eg = eta_solve(j, r*j0/k, a, T)   # R_f,s = 1, R_f,g = r  -> j0,eff,g = r*j0_s/k
            b = 2.303*R*T/(a*F)
            rows.append((T, a, j, j0, r, k, es, eg-es, b*np.log10(k/r), eg))
A = np.array(rows)
# note: r multiplies the effective exchange current of g: kappa_eff = kappa/r ; kappa/r < 1 means g beats s (negative price)
d = A[:, 7]-A[:, 8]
hi100 = A[:, 6] > 0.1
print(f"{len(A)} (T, alpha, j, j0_s, r, kappa) cases; eta_s > 100 mV in {hi100.sum()} of them")
print(f"max |full - Tafel| for eta_s > 100 mV: {np.abs(d[hi100]).max()*1e3:.3f} mV")
sel = hi100 & (A[:, 8] > 0)
print(f"   restricted to those with Tafel price > 0 (kappa_eff > 1): {np.abs(d[sel]).max()*1e3:.3f} mV ({sel.sum()} cases)")
ok = np.abs(d[hi100]).max() < 2e-3; fails += (not ok)
print(f"CHECK (spec literal) |Delta eta_full - b log10 kappa_eff| < 2 mV for eta_s > 100 mV -> {'PASS' if ok else 'FAIL'}")
both = (A[:, 6] > 0.1) & (A[:, 9] > 0.1)
okb = np.abs(d[both]).max() < 2e-3
print(f"also requiring eta_g > 100 mV as well (both overpotentials in the Tafel regime): {both.sum()} cases, max |full - Tafel| = {np.abs(d[both]).max()*1e3:.3f} mV -> {'PASS' if okb else 'FAIL'} (diagnostic: the spec condition eta_s>100 mV alone lets in cases where the candidate's overpotential is below 100 mV because R_f ratio > kappa)")
iw = np.where(both)[0][np.argmax(np.abs(d[both]))]; w = A[iw]
print(f'worst case with both > 100 mV: T={w[0]}, alpha={w[1]}, j={w[2]:g}, j0_s={w[3]:g}, r={w[4]:g}, kappa={w[5]:.3g}, eta_s={w[6]*1e3:.1f} mV, eta_g={w[9]*1e3:.1f} mV, deviation {d[iw]*1e3:.2f} mV')
lo = ~hi100
print(f"for eta_s <= 100 mV: {lo.sum()} cases; max deviation {np.abs(d[lo]).max()*1e3:.2f} mV; fraction above 2 mV: {(np.abs(d[lo]) > 2e-3).mean()*100:.1f}%")
# where does it fail: bin by eta_s
for a_ in alphas:
    m = (A[:, 1] == a_)
    for lo_, hi_ in ((0, 0.02), (0.02, 0.05), (0.05, 0.1), (0.1, 1e9)):
        mm = m & (A[:, 6] > lo_) & (A[:, 6] <= hi_)
        if mm.any(): print(f"   alpha={a_}: eta_s in ({lo_*1e3:.0f},{min(hi_,9.9)*1e3:.0f}] mV: n={mm.sum():5d}, max dev {np.abs(d[mm]).max()*1e3:7.2f} mV")
print("\nexample rows, T=353.15 K, alpha=0.5, j=1e4 A/m2, j0_s=1e-3 A/m2, R_f ratio 1  (kappa, eta_s [V], Delta eta full [mV], Tafel [mV], power penalty j*Deta/T0 [W/K/m2]):")
for r_ in A:
    if r_[0] == 353.15 and r_[1] == 0.5 and r_[2] == 1e4 and r_[3] == 1e-3 and r_[4] == 1 and r_[5] in kap[::4]:
        print(f"   {r_[5]:10.3g} {r_[6]:8.4f} {r_[7]*1e3:10.2f} {r_[8]*1e3:10.2f} {r_[2]*r_[7]/T0:12.2f}")
print("\nrange of the Delta-eta needed to compensate kappa in [1,1e6] at alpha=0.5, 298.15 K: 0 .. %.0f mV (Tafel)" % (b05*6))
print("with R_f,g/R_f,s = r, the price b log10(kappa/r) is negative when r > kappa: area compensates (kappa_eff<1). That is the R_f route of G1.7.")
print("sweep bracketing: kappa 1..1e6 covers 0 to 6 decades; the |dev|>2 mV region (small eta_s) is covered by the j0_s=1e1 / j=2e3 low-overpotential cases: yes, eta_s reaches below 100 mV in %d cases" % lo.sum())
print("IDENTITY CHECKS: none (full Butler-Volmer root vs Tafel asymptote).")
print("OVERALL", "PASS" if fails == 0 else f"FAIL ({fails})")
