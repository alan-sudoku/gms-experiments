"""rv06: Task 6 and spec-fit points (a) and (c) of the Prompt 8 S5 review.

Physical truth (made up, linear): B_infra = F + v N, F avoided only when every product leaves; d0_k is
Sigma_g - Sigma_s with NO part of x's infrastructure inside Sigma_s (the answer's d_k).
What the CURRENT spec computes depends on where infrastructure sits inside CExC(x) (Sigma_s,init carries
n(x)[CExC(x) - b_ch(x)]/T0):
  config A: CExC source excludes capital goods and v is capital-like -> c_in = 0;
  config B: lambda = 0 (partial exit), so REQ-LIFECYCLE-CEXC-SOURCE item 4 does not force exclusion; the
            source includes capital goods allocated at the average share -> c_in = B/(T N) (assumption:
            the database's capital-goods share equals the spec's average share; UNSURE for real data);
            when lambda > 0, item 4 forces the source back to config A;
  config C: v is an operating flow (energy, reagents, maintenance) that every CExC source contains ->
            c_in = v/T in every evaluation, also when lambda > 0 (item 4 removes capital goods only).
Spec d_k = d0_k - c_in. E16 procedure: if every product passes d_k < lambda_avg (with the lambda>0 source) all
switch with credit; otherwise lambda = 0 and product k switches iff its d_k (lambda=0 source) < 0.
(a) T0 != T_ref: the rule's structure is invariant when every term is divided by the same T0; mixing
T_ref in lambda_lo with T0 in Sigma shifts the edge; with an operational part fixed in entropy and an
upstream part fixed in lost work, phi_k changes with T0 (made-up split).
Level `derived` (unverified). numpy only. Run: python rv06_spec_fit.py
"""
import itertools
import numpy as np

TREF = 298.15
F, v = 4e13, 2e4
N = np.array([9e8, 1e8])


def W_true(S, d0, T=TREF):
    w = sum(N[k] * (v / T - d0[k]) for k in S)
    return w + (F / T if len(S) == len(N) else 0.0)


def opt(d0):
    subs = [S for r in range(3) for S in itertools.combinations(range(2), r)]
    vals = {S: W_true(S, d0) for S in subs}
    b = max(vals.values())
    return b, [S for S, w in vals.items() if w >= b - 1e-6 * abs(b) - 1]


def spec_E16(d0, config):
    lam = (F + v * N.sum()) / (TREF * N.sum())
    c_pos = {"A": 0.0, "B": 0.0, "C": v / TREF}[config]          # source used when lambda > 0
    c_zero = {"A": 0.0, "B": lam, "C": v / TREF}[config]         # source used when lambda = 0
    if all(d0 - c_pos < lam):
        return (0, 1), "gate open, lambda = avg"
    return tuple(k for k in range(2) if d0[k] - c_zero < 0), "gate shut, lambda = 0"


def answer_rule(d0, config):
    # the answer with its 'never both' caveat applied correctly: if v is already in CExC, lambda_lo = 0
    lo = 0.0 if config == "C" else v / TREF
    dk = d0 - (v / TREF if config == "C" else 0.0)
    Sm = tuple(k for k in range(2) if dk[k] < lo)
    phi = np.maximum(0, N * (dk - lo)) * TREF / F
    return ((0, 1) if phi.sum() < 1 else Sm), phi.sum()


def answer_rule_naive(d0, config):
    # analyst who cannot tell where v sits (spec has no F/v split) and adds lambda_lo = v/T anyway
    dk = d0 - (v / TREF if config == "C" else 0.0)
    lo = v / TREF
    Sm = tuple(k for k in range(2) if dk[k] < lo)
    phi = np.maximum(0, N * (dk - lo)) * TREF / F
    return ((0, 1) if phi.sum() < 1 else Sm), phi.sum()


cases = {"rv03 d0=(150,400)": np.array([150.0, 400.0]),
         "claim 5 d0=(50,400)": np.array([50.0, 400.0]),
         "d0=(150,190)": np.array([150.0, 190.0]),
         "d0=(30,400)": np.array([30.0, 400.0]),
         "d0=(230,230)": np.array([230.0, 230.0])}
for name, d0 in cases.items():
    # in config C the physical truth is the same; only the bookkeeping differs, so the optimum is opt(d0)
    b, opts = opt(d0)
    print(f"== {name}: optimum W = {b:+.4e} J/K at {[[k+1 for k in S] for S in opts]}")
    for cfg in ("A", "B", "C"):
        S, why = spec_E16(d0, cfg)
        loss = b - W_true(S, d0)
        Sa, sp = answer_rule(d0, cfg)
        Sn, spn = answer_rule_naive(d0, cfg)
        print(f"  config {cfg}: E16 -> {[k+1 for k in S]} ({why}), loss {loss:.4e} J/K | answer (v located) -> "
              f"{[k+1 for k in Sa]}, loss {b - W_true(Sa, d0):.4e} | answer (v not located) -> {[k+1 for k in Sn]}, "
              f"loss {b - W_true(Sn, d0):.4e}")
# config C double count in E16 when the gate opens: credited vs saved per position
lam = (F + v * N.sum()) / (TREF * N.sum())
print(f"config C, gate open: credit per position = c_in + lambda = {v/TREF + lam:.4f} J/K vs true saving "
      f"{lam:.4f} J/K -> double count {v/TREF:.4f} J/K per position = {v/TREF*N.sum():.4e} J/K over N")

print("\n== (a) T0 != T_ref ==")
d0 = np.array([150.0, 400.0])
Bl = N * d0 * TREF            # lost-work form of d at T_ref (J), assumed T0-independent here
for T0 in (298.15, 250.0, 200.0):
    dT = Bl / (N * T0)
    phi_c = N * (dT - v / T0) * T0 / F
    phi_m = N * (dT - v / TREF) * T0 / F
    print(f"T0 = {T0}: all lost work T0-independent -> phi (consistent T0) = {np.round(phi_c,5)}, sum {phi_c.sum():.5f}; "
          f"lambda_lo with T_ref but d at T0 -> sum {phi_m.sum():.5f}; edge v/T0 = {v/T0:.3f} vs v/T_ref = {v/TREF:.3f} J/K")
# made-up split: d0_k = s_op_k (entropy fixed by process) + u_k / T0 (upstream lost work, J)
s_op = np.array([250.0, 300.0]); u = (d0 - s_op) * TREF
for T0 in (298.15, 250.0, 200.0):
    dT = s_op + u / T0
    phi = N * (dT - v / T0) * T0 / F
    b_all = (F + v * N.sum()) / T0 - (N * dT).sum()
    print(f"T0 = {T0}: split s_op = {s_op}, u = {u} J -> d = {np.round(dT,2)}, sum phi = {phi.sum():.4f}, W(all) = {b_all:+.4e} J/K")

print("\n== reviewer's spec-symbol bracket (R5 of rv04) on the rv03 case: [0, B_infra,av/(T0 N_k)] ==")
B = F + v * N.sum()
d0 = np.array([150.0, 400.0])
for k in range(2):
    print(f"product {k+1}: bracket (0, {B/(TREF*N[k]):.4f}) J/K; d = {d0[k]}; psi_k = N_k T0 d_k / B = {N[k]*TREF*d0[k]/B:.4f}")
print(f"all-exit system test sum psi_k = {(N*TREF*d0/B).sum():.4f} (< 1: all switch); answer's band for comparison: "
      f"({v/TREF:.4f}, {v/TREF + F/(TREF*N[0]):.4f}) and ({v/TREF:.4f}, {v/TREF + F/(TREF*N[1]):.4f})")
