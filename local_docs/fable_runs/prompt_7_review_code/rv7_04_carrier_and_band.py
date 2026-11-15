"""S5 review of prompt_7_web_answer.md, tasks 5 and 6: claim 1's c_k and the verdict's "undecided" band.

Purpose
  (a) Claim 1 says, for a heat resource at T_h, c = T_h/(T_h - T0) and c_k >= 1, with c_k defined
      as primary EXERGY per J of work delivered in environment k. Compare three bases:
        energy basis       c_E   = T_h/(T_h - T0)                     (J of heat per J of work)
        exergy at T0       c_X0  = 1                                  (reversible engine)
        exergy at T_ref    c_Xref = (1 - T_ref/T_h)/(1 - T0/T_h)      (heat valued where the
                                                                       resource stock is held)
      and a free flux (sunlight), which draws no stock: c = 0 per J at the margin.
  (b) Band protection. True cost C(c) = dU + c*dO; (A) = C(1), (B)*T_ref = C(r). Break-even
      c* = -dU/dO. The band of the verdict flags "undecided" iff c* in (1, r). Cases:
      claim 4 (c* = 1.25, inside), c* = 2.5 with true c_op = 3 at T0 = 150 K (outside, both wrong),
      c* = 0.8 with c_op = 0.5 (outside below 1, both wrong). Monte Carlo of misses and false
      alarms against a declared c_op range, vs a declared-range test.
  (c) Several operational environments: (A) and (B) can disagree with dU = 0 (claim 3 is one),
      and claim 5's single-ratio inequality is then undefined. Generalised test: sign of
      dU + sum_k c_k dO_k over a declared box of c_k (linear, so extremes at endpoints).

Assumptions
  rv02-like sampling (difference of uniforms, equal scales) for the Monte Carlo; the c_op ranges
  are illustrative. Everything is a claim at level `derived`.

Run: <repo>/.venv/bin/python rv7_04_carrier_and_band.py  (from any directory)
"""
import numpy as np

TREF = 298.15

print("== (a) c for a heat resource at T_h used in an environment at T0 ==")
print("  T_h[K]  T0[K]   c_E(energy)  c_X0(exergy@T0)  c_Xref(exergy@T_ref)  (B) T_ref/T0")
for Th in (400.0, 600.0, 1000.0):
    for T0 in (150.0, 200.0, 290.0):
        cE = Th / (Th - T0)
        cXref = (1 - TREF / Th) / (1 - T0 / Th)
        print(f"  {Th:6.0f}  {T0:5.0f}   {cE:10.4f}   {1.0:14.4f}   {cXref:19.4f}   {TREF/T0:10.4f}")
print("  -> c_E >= 1 always, but it is an energy ratio; on an exergy basis valued at T_ref, c < 1")
print("     whenever T0 < T_ref (a cold environment lets the same stock deliver more work), so the")
print("     claim 'c_k >= 1, c_k = 1 is a physical limit' does not hold across environments.")
for eta2 in (0.5,):
    T0, Th = 150.0, 600.0
    print(f"  with a second-law efficiency {eta2}: c_Xref(600 K, 150 K) = {(1-TREF/Th)/(1-T0/Th)/eta2:.4f}")
print("  free flux (sunlight) at the margin: c = 0 per J (no stock drawn; hardware already in CExC)")

print("== (b) does the band (1, r) protect against claim 4's failure mode? ==")
def case(name, U1, O1, U2, O2, T0, cop):
    r = TREF / T0
    dU, dO = U2 - U1, O2 - O1
    cs = -dU / dO
    pick = lambda c: "D1" if U1 + c * O1 < U2 + c * O2 else "D2"
    flagged = 1 < cs < r
    print(f"  {name}: c* = {cs:.3f}, r = {r:.3f}, band flags undecided: {flagged}; "
          f"(A) {pick(1)}, (B) {pick(r)}, true at c_op={cop}: {pick(cop)}")
case("claim 4       ", 1000, 10, 950, 50, 150.0, 3.0)
case("c*=2.5, c_op=3", 1000, 10, 900, 50, 150.0, 3.0)
case("c*=0.8, c_op=.5", 1000, 50, 1008, 40, 150.0, 0.5)

rng = np.random.default_rng(7)
n = 400000
dU = rng.uniform(0, 1, n) - rng.uniform(0, 1, n)
dO = rng.uniform(0, 1, n) - rng.uniform(0, 1, n)
T0 = 150.0
r = TREF / T0
cs = -dU / dO
band = (cs > 1) & (cs < r)
print("  Rules compared (true c_op drawn inside the declared range):")
print("   verdict rule : decide by sign(A) unless c* in (1, r), then 'undecided'")
print("   range rule   : decide by sign(dU + c dO) for c in [lo, hi] unless c* in (lo, hi), then 'undecided'")
for lo, hi in ((1.0, 4.0), (2.0, 3.0), (0.0, 1.0), (1.0, 1.5)):
    cop = rng.uniform(lo, hi, n)
    truth = np.sign(dU + cop * dO)
    A_wrong = np.sign(dU + dO) != truth
    v_dec_wrong = ~band & A_wrong
    v_undec = band
    r_band = (cs > lo) & (cs < hi)
    r_dec_wrong = ~r_band & (np.sign(dU + lo * dO) != truth)
    print(f"  c_op ~ U({lo},{hi}): (A) alone wrong {A_wrong.mean()*100:5.2f} % | verdict rule: decided-but-wrong "
          f"{v_dec_wrong.mean()*100:5.2f} %, undecided {v_undec.mean()*100:5.2f} % | range rule: decided-but-wrong "
          f"{r_dec_wrong.mean()*100:5.2f} %, undecided {r_band.mean()*100:5.2f} %")

print("== (c) several operational environments ==")
# claim 3 recast: no upstream difference, two operational phases at 290 K and 150 K
T = np.array([290.0, 150.0])
rk = TREF / T
dO_k = np.array([100.0 - 0.0, 0.0 - 60.0])     # D1 - D2 per phase [J]: D1 dissipates 100 J at 290 K, D2 60 J at 150 K
dU0 = 0.0
A = dU0 + dO_k.sum()
B = dU0 + (rk * dO_k).sum()
print(f"  claim 3 as a two-environment case: dU = 0, dO_k = {dO_k.tolist()} J; sign A {np.sign(A):+.0f}, "
      f"sign B {np.sign(B):+.0f} -> disagree with no upstream trade-off; claim 5's ratio |dU|/|dO| = "
      f"{abs(dU0)/abs(dO_k.sum()):.1f}, outside (1, r)")
# Monte Carlo: two operational environments + upstream
m = 400000
dU = rng.uniform(0, 1, m) - rng.uniform(0, 1, m)
d1 = rng.uniform(0, 1, m) - rng.uniform(0, 1, m)
d2 = rng.uniform(0, 1, m) - rng.uniform(0, 1, m)
A = dU + d1 + d2
B = dU + rk[0] * d1 + rk[1] * d2
dis = np.sign(A) != np.sign(B)
dO = d1 + d2
rmax = rk.max()
with np.errstate(divide="ignore", invalid="ignore"):
    ratio = np.abs(dU) / np.abs(dO)
band_agg = (dU * dO < 0) & (ratio > 1) & (ratio < rmax)
print(f"  MC, upstream + phases at 290 and 150 K: A/B disagree {dis.mean()*100:.2f} %; claim-5 band on "
      f"aggregated dO with r = max r_k catches {np.mean(band_agg[dis])*100:.1f} % of them; "
      f"flags {band_agg.mean()*100:.2f} % of all cases")
# box test with c_k in [1, r_k]: min/max of linear form over the box
lo = dU + np.minimum(d1, rk[0] * d1) + np.minimum(d2, rk[1] * d2)
hi = dU + np.maximum(d1, rk[0] * d1) + np.maximum(d2, rk[1] * d2)
box = (lo < 0) & (hi > 0)
print(f"  box test c_k in [1, r_k]: catches {np.mean(box[dis])*100:.1f} % of A/B disagreements "
      f"(100 % by construction), flags {box.mean()*100:.2f} % of all cases")
