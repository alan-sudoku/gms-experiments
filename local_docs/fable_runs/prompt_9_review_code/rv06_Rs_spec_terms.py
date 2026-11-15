"""rv06: claims 2 and 3 - R_s written in the spec's own terms; is there a double count?

Purpose: itemise R_s under the answer's minimal rule ("recurring stages of Sigma_s,init applied to the
restored stock + retired-unit EOL") in GMS-100 symbols; count how often each flow (virgin extraction,
dispersal of b_ch, remelt, transport) is charged over the life of side s, and compare with the counting
GMS-100 section 5 states for side g; quantify the excess of two misreadings (extraction treated as a
recurring stage; the block's literal list "make-up + remelt + transport + retired-unit EOL"); state the
omitted stages per first unit and per replacement under the asymmetric boundary.
Task: S5 review task 3.
Assumptions: EQ-LIFECYCLE-INCUMBENT-INITIAL-CAPITAL, EQ-LIFECYCLE-INCUMBENT-EOL, EQ-LIFECYCLE-RETIRED-UNIT-EOL
(k = s, i = x), EQ-LIFECYCLE-GEOMETRY-REPLACEMENT-COST as written; the numeric values in (c) are made-up
placeholders, not data for any element.
Level: derived.
"""
import sympy as sp

n, CExC, bch, wrm, Rr, Ms, btr, T0, m = sp.symbols("n CExC b_ch w_rm R_rec M_s b_tr T_0 m", nonnegative=True)
wext = CExC - bch

S_init = (n * wext + Ms * btr) / T0
S_ret = n / T0 * (Rr * wrm + (1 - Rr) * CExC)
S_eol = n / T0 * (Rr * wrm + (1 - Rr) * bch)

print("(a) R_s under the answer's rule, read with the spec's terms")
R_rule = Ms * btr / T0 + S_ret
print("  recurring stages of Sigma_s,init applied to restored stock: transport only, M_s b_tr / T0"
      " (restored stock is already extracted; virgin make-up of the unrecovered fraction sits in Sigma_EOL^ret,"
      " as w_conv,i excludes w_lost,ext,i in R_g)")
print("  R_s =", sp.simplify(R_rule))

print("\n(b) life-cycle flow count on side s with m_s replacements (coefficients of n/T0 per flow)")
total = sp.expand((S_init + m * R_rule + S_eol) * T0)
wext_s, bch_s = sp.symbols("w_ext b_ch_", nonnegative=True)
tot2 = sp.expand(total.subs(CExC, wext_s + bch))
for name, sym in [("virgin extraction w_ext", wext_s), ("dispersal b_ch", bch), ("remelt w_rm", wrm), ("transport b_tr", btr)]:
    coef = sp.factor(sp.diff(tot2, sym))
    print(f"  {name:26s}: {coef}")
print("  -> extraction n (1 + m (1 - R_rec)) times, dispersal of the unrecovered fraction m + 1 times,"
      " remelt m + 1 times, transport m + 1 units: each physical flow once, same counting as GMS-100 section 5 for g")

print("\n(c) misreadings and their excess per replacement (placeholder numbers)")
R_misA = S_init + S_ret                 # extraction treated as recurring on the full stock
R_block = Ms * btr / T0 + n / T0 * ((1 - Rr) * CExC + Rr * wrm) + S_ret   # block list: make-up + remelt + transport + ret-EOL
exA = sp.simplify(R_misA - R_rule)
exB = sp.simplify(R_block - R_rule)
print("  misreading A (extraction recurring): excess =", exA, " = n w_ext / T0")
print("  block literal list: excess =", exB, " = Sigma_EOL^ret counted twice")
vals = {n: 1000, CExC: 4.0e5, bch: 1.3e5, wrm: 2.0e4, Rr: 0.6, Ms: 60, btr: 1.0e6, T0: 298.15, m: 2}
print(f"  placeholders: n = 1000 mol, CExC = 4.0e5 J/mol, b_ch = 1.3e5 J/mol, w_rm = 2.0e4 J/mol, R_rec = 0.6,"
      f" M_s = 60 kg, b_tr = 1.0e6 J/kg, T0 = 298.15 K, m_s = 2")
print(f"  R_s (rule) = {float(R_rule.subs(vals)):.4e} J/K; Sigma_s,init = {float(S_init.subs(vals)):.4e} J/K;"
      f" Sigma_s,EOL = {float(S_eol.subs(vals)):.4e} J/K")
print(f"  excess A per replacement = {float(exA.subs(vals)):.4e} J/K; over m_s = 2: {2 * float(exA.subs(vals)):.4e} J/K")
print(f"  excess block per replacement = {float(exB.subs(vals)):.4e} J/K; over m_s = 2: {2 * float(exB.subs(vals)):.4e} J/K")
print("  both raise Sigma_s, lower f, favour g: the unsafe direction for 'g wins'")

print("\n(d) omitted stages under the asymmetric boundary (against R_g's stage list)")
wconv, mfg, tool, comp = sp.symbols("w_conv_x Sigma_s_mfg Sigma_s_tool Sigma_s_comp", nonnegative=True)
om_init = n * wconv / T0 + mfg + tool + comp     # w_lost,prec = w_ext + w_conv; extraction is already charged
om_rep = n * wconv / T0 + mfg                    # R_g has conversion of restored stock + manufacturing; no tooling/compute
print("  omega_init =", om_init)
print("  omega_rep  =", om_rep)
print("  omega_init - omega_rep =", sp.simplify(om_init - om_rep), ">= 0: the stages differ, so omega* = f/(m_s+1)"
      " is a per-unit mean; the exact break-even is omega_init + m_s omega_rep = f")
