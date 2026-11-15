"""S5 review of prompt_7_web_answer.md, task 1: claim 5 (flip condition) and the 5 % figure.

Purpose
  1. Re-run rv02's random sweep (same seed, same sampling order) and reproduce 5.06 %.
  2. Map rv02 onto the answer's variables: dU = Wg - Ws (upstream lost work, J),
     dO = T0 * (Sg - Ss) (operational lost work at the operational dead state, J),
     r = T_ref / T0. Currency (A) ranks by sign(dU + dO); currency (B), multiplied by
     T_ref, ranks by sign(dU + r*dO).
  3. Test claim 5's "if and only if": flip <=> dU*dO < 0 and 1 < |dU|/|dO| < r,
     and the margin bound |dU + dO| < (r - 1)|dO| on every flipped case.
  4. Measure how much the 5 % depends on rv02's sampling: flip fraction per T0 bin,
     as a function of the scale ratio k = (upstream scale)/(operational scale), for
     other magnitude distributions, and conditional on a trade-off (dU*dO < 0).

Assumptions
  rv02's sampling is reproduced exactly (numpy default_rng(0), draw order T0, Wg, Ws, Sg, Ss).
  The alternative distributions in part 4 are illustrative, not claims about real designs.
  Everything printed is a claim at level `derived`.

Run: <repo>/.venv/bin/python rv7_01_flip_condition.py  (from any directory)
"""
import numpy as np

TREF = 298.15

# ---- 1. rv02 sweep, reproduced verbatim -------------------------------------------------
rng = np.random.default_rng(0)
N = 100000
T0r = rng.uniform(150, 290, N)
Wg_, Ws_ = rng.uniform(0, 2e6, N), rng.uniform(0, 2e6, N)
Sg_, Ss_ = rng.uniform(0, 1e4, N), rng.uniform(0, 1e4, N)
ent = (Wg_ - Ws_) / TREF + (Sg_ - Ss_)
lw = (Wg_ - Ws_) + T0r * (Sg_ - Ss_)
flip_rv02 = np.sign(ent) != np.sign(lw)
print("== 1. rv02 reproduction ==")
print(f"rv02 disagreement fraction: {flip_rv02.mean()*100:.2f} %  ({flip_rv02.sum()} of {N})")

# ---- 2./3. claim 5 on the same cases -----------------------------------------------------
dU = Wg_ - Ws_
dO = T0r * (Sg_ - Ss_)
r = TREF / T0r
A = dU + dO
B = dU + r * dO
flipAB = np.sign(A) != np.sign(B)
print(f"zero signs: A==0 {np.sum(A==0)}, B==0 {np.sum(B==0)}, dO==0 {np.sum(dO==0)}, dU==0 {np.sum(dU==0)}")
print(f"flip via (A,B) form == rv02 flip on every case: {np.array_equal(flipAB, flip_rv02)}")
with np.errstate(divide="ignore", invalid="ignore"):
    ratio = np.abs(dU) / np.abs(dO)
cond = (dU * dO < 0) & (ratio > 1) & (ratio < r)
print("== 2. claim 5 'if and only if' on rv02 cases ==")
print(f"flipped cases: {flipAB.sum()}, cases meeting the inequality: {cond.sum()}")
print(f"flipped but inequality false (counterexamples to 'only if'): {np.sum(flipAB & ~cond)}")
print(f"inequality true but not flipped (counterexamples to 'if'):    {np.sum(cond & ~flipAB)}")
margin_ok = np.abs(A[flipAB]) < (r[flipAB] - 1) * np.abs(dO[flipAB])
print(f"margin bound |dU+dO| < (r-1)|dO| holds on {margin_ok.sum()} of {flipAB.sum()} flipped cases")
cstar = -dU[flipAB] / dO[flipAB]
print(f"break-even c* = -dU/dO on flipped cases: min {cstar.min():.4f}, max {cstar.max():.4f} "
      f"(must lie in (1, r<=1.988))")
# relative margin under (A) on flipped cases, as a fraction of total |dU|
rel = np.abs(A[flipAB]) / np.abs(dU[flipAB])
print(f"|A margin| / |dU| on flipped cases: median {np.median(rel):.3f}, max {rel.max():.3f}")

# boundary / tie cases, exact rational arithmetic
from fractions import Fraction as F
print("== 2b. boundary cases (exact) ==")
rr = F(29815, 15000)  # r at T0 = 150 K
for name, u, o in [("c*=1 (A tie)", F(-1), F(1)), ("c*=r (B tie)", -rr, F(1)),
                   ("dO=0", F(1), F(0)), ("dU=0", F(0), F(1))]:
    a, b = u + o, u + rr * o
    sa, sb = (a > 0) - (a < 0), (b > 0) - (b < 0)
    print(f"  {name:14s}: sign A {sa:+d}, sign B {sb:+d}, np.sign-style 'disagree' = {sa != sb}, "
          f"strict-opposite = {sa*sb < 0}")

# ---- 4. sensitivity of the fraction to sampling -----------------------------------------
print("== 4a. rv02 flip fraction per T0 bin (same cases) ==")
edges = np.arange(150, 291, 20)
for lo, hi in zip(edges[:-1], edges[1:]):
    m = (T0r >= lo) & (T0r < hi)
    print(f"  T0 in [{lo},{hi}) K: r in [{TREF/hi:.3f},{TREF/lo:.3f}], flip {flipAB[m].mean()*100:5.2f} %")
tr = dU * dO < 0
print(f"rv02 flip fraction conditional on a trade-off (dU*dO<0): {flipAB[tr].mean()*100:.2f} % "
      f"(trade-off share {tr.mean()*100:.1f} %)")
k_rv02 = 2e6 / (T0r * 1e4)
print(f"rv02 implicit scale ratio k = 2e6/(T0*1e4): {k_rv02.min():.3f} .. {k_rv02.max():.3f}")


def flip_frac(T0, k, n=400000, dist="rv02", seed=1):
    """Fraction of (A)/(B) disagreements at fixed T0, with upstream scale = k * operational scale."""
    g = np.random.default_rng(seed)
    if dist == "rv02":       # difference of two uniforms (triangular), as rv02
        u = g.uniform(0, 1, n) - g.uniform(0, 1, n)
        o = g.uniform(0, 1, n) - g.uniform(0, 1, n)
    elif dist == "normal":
        u, o = g.normal(size=n), g.normal(size=n)
    elif dist == "logmag4":  # magnitudes log-uniform over 4 decades, random signs
        u = 10 ** g.uniform(0, 4, n) * g.choice([-1, 1], n)
        o = 10 ** g.uniform(0, 4, n) * g.choice([-1, 1], n)
    u = k * u
    rr_ = TREF / T0
    return np.mean(np.sign(u + o) != np.sign(u + rr_ * o))


print("== 4b. flip fraction vs scale ratio k (upstream/operational), rv02 shapes ==")
ks = [0.01, 0.1, 0.3, 0.5, 0.7, 1.0, 1.4, 2.0, 3.0, 10.0, 100.0]
print("  k     " + "  ".join(f"T0={T:>3d}" for T in (150, 200, 250, 290)))
for k in ks:
    print(f"  {k:<6g}" + "  ".join(f"{flip_frac(T, k)*100:6.2f}%" for T in (150, 200, 250, 290)))
kgrid = np.exp(np.linspace(np.log(0.2), np.log(5), 61))
fr = [flip_frac(150, k, n=200000) for k in kgrid]
i = int(np.argmax(fr))
print(f"  max over k at T0=150 K: {fr[i]*100:.2f} % at k = {kgrid[i]:.2f}")

print("== 4c. other magnitude distributions, k = 1 ==")
for dist in ("rv02", "normal", "logmag4"):
    print(f"  {dist:8s}: " + "  ".join(f"T0={T}: {flip_frac(T, 1.0, dist=dist)*100:5.2f}%" for T in (150, 200, 290)))

print("== 4d. illustration (not a bound): trade-off cases whose |dU|/|dO| is log-uniform over one "
      "decade centred on 1 ==")
for T in (150, 200, 290):
    rr_ = TREF / T
    # log-uniform ratio over [10^-0.5, 10^0.5]: P(1<ratio<r) = log10(r)/1
    print(f"  T0={T}: P(1<ratio<r) = {np.log10(rr_):.3f}  -> flip share of trade-offs {np.log10(rr_)*100:.1f} %")

print("== 4e. close calls in rv02: flip share among cases whose (A) margin is small ==")
for frac in (0.05, 0.1, 0.25, 0.5):
    m = tr & (np.abs(A) < frac * np.abs(dU))
    print(f"  trade-off and |dU+dO| < {frac:.2f}|dU|: {m.sum():5d} cases, flipped {flipAB[m].mean()*100:5.1f} %")
