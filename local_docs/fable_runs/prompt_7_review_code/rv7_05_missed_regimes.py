"""S5 review of prompt_7_web_answer.md, task 7: regimes the answer does not treat.

Purpose
  (a) Deep space as "the environment": if the dead state is the cosmic background (~2.725 K)
      rather than an "effective" 150-290 K, r = T_ref/T0 is ~109 and currency (B) disagrees with
      (A) far more often (rv02-like sampling at equal scales).
  (b) Boundary dependence of S_gen for 1 J of dissipated work rejected by a radiator at T_rad to
      a 2.725 K sink: S_gen to the radiator surface, including the entropy of emitted blackbody
      radiation (4/3 Q/T_rad; recalled result, UNSURE as to applicability to grey radiators), and
      including absorption by the background. Lost work T0*S_gen for consistent and inconsistent
      pairings of T0 and boundary.
  (c) Heat-transfer loss (1 J from 400 K to a 290 K radiator): S_gen is fixed by the process, the
      lost work T0*S_gen depends on which T0 is "the environment" -> currency (A) inherits the
      dead-state convention for heat-transfer losses; (B) does not.
  (d) Upstream losses rejected at a site ambient other than T_ref: (B)'s "true" S_gen = W/T_site
      differs from W/T_ref; tables give only W at T_ref, so (B) is not computable from them.

Assumptions
  Illustrative temperatures only. Blackbody emission entropy flux (4/3)E/T is a recalled textbook
  result (UNSURE here for a grey surface). Everything is a claim at level `derived`.

Run: <repo>/.venv/bin/python rv7_05_missed_regimes.py  (from any directory)
"""
import numpy as np

TREF, TCMB = 298.15, 2.725

print("== (a) deep-space dead state ==")
rng = np.random.default_rng(0)
n = 400000
u = rng.uniform(0, 1, n) - rng.uniform(0, 1, n)
o = rng.uniform(0, 1, n) - rng.uniform(0, 1, n)
for T0 in (290.0, 150.0, 50.0, TCMB):
    r = TREF / T0
    frac = np.mean(np.sign(u + o) != np.sign(u + r * o))
    print(f"  T0 = {T0:7.3f} K: r = {r:8.3f}, (A)/(B) disagree {frac*100:5.2f} % (equal scales, rv02 shapes)")

print("== (b) 1 J of dissipated work rejected by a radiator to a 2.725 K sink ==")
Q = 1.0
for Trad in (290.0, 150.0):
    s_surf = Q / Trad
    s_rad = 4.0 / 3.0 * Q / Trad
    s_sink = Q / TCMB
    print(f"  T_rad = {Trad:.0f} K: S_gen to radiator {s_surf:.4e}, incl. emitted radiation {s_rad:.4e}, "
          f"incl. absorption at sink {s_sink:.4e} J/K (span x{s_sink/s_surf:.0f})")
    print(f"     consistent pairs: T_rad*S_surf = {Trad*s_surf:.3f} J, T_CMB*S_sink = {TCMB*s_sink:.3f} J; "
          f"inconsistent 150 K * S_surf = {150*s_surf:.3f} J, 290 K * S_sink = {290*s_sink:.1f} J")

print("== (c) heat-transfer loss: 1 J from 400 K to a 290 K radiator ==")
S = Q * (1 / 290.0 - 1 / 400.0)
print(f"  S_gen = {S:.4e} J/K (fixed by the process)")
for T0 in (290.0, 150.0, TCMB):
    print(f"  T0 = {T0:7.3f} K: lost work T0*S_gen = {T0*S:.4e} J")
print("  -> for heat-transfer losses the lost work in (A) moves by x"
      f"{290/TCMB:.0f} between a 290 K and a 2.725 K dead state; dissipated work does not move.")

print("== (d) upstream site ambient vs T_ref ==")
for Tsite in (273.15, 288.15, 313.15):
    print(f"  T_site = {Tsite:.2f} K: W/T_site over W/T_ref = {TREF/Tsite:.4f}")
