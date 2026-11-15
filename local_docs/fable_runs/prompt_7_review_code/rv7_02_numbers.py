"""S5 review of prompt_7_web_answer.md, task 2: recompute every number in claims 2-8 and the verdict.

Purpose
  Reproduce the stated figures: r at 150 and 290 K (claim 5, verdict), claim 2's resistor
  entropies, claim 3's 0.345/0.400 J/K, claim 4's 1010/1000 MJ, 1030/1100 MJ, break-even 1.25,
  3.421/3.520 MJ/K and implicit rate 1.99, claim 6's 33 MJ/kg -> 0.11 MJ/(kg K) for Al,
  claim 7's factor 1.93.

Assumptions
  T_ref = 298.15 K. The Al chemical exergy is the answer's recalled 33 MJ/kg; this script only
  checks the arithmetic. The cross-check 888.4 kJ/mol / 26.98 g/mol uses a value recalled by the
  reviewer (UNSURE, not verified against a source here). Everything is a claim at level `derived`.

Run: <repo>/.venv/bin/python rv7_02_numbers.py  (from any directory)
"""
TREF = 298.15

print("== claim 5 / verdict: r = T_ref/T0 ==")
for T in (150.0, 290.0):
    print(f"  r({T:.0f} K) = {TREF/T:.4f}")

print("== claim 2: resistors dissipating 1 J ==")
for T in (150.0, 300.0):
    print(f"  S_gen at {T:.0f} K = {1/T:.3e} J/K")

print("== claim 3: dissipated work, one battery ==")
s1, s2 = 100 / 290, 60 / 150
print(f"  design 1: 100 J at 290 K -> {s1:.4f} J/K; design 2: 60 J at 150 K -> {s2:.4f} J/K")
print(f"  (B) prefers design {'1' if s1 < s2 else '2'}; battery draw ratio 100/60 = {100/60:.4f} "
      f"(answer: 67 % more)")

print("== claim 4: T0,op = 150 K ==")
U1, O1, U2, O2 = 1000.0, 10.0, 950.0, 50.0  # MJ
print(f"  (A) totals: D1 {U1+O1:.0f} MJ, D2 {U2+O2:.0f} MJ -> prefers D{'1' if U1+O1 < U2+O2 else '2'}")
c = 3.0
print(f"  c_op = 3: D1 {U1+c*O1:.0f} MJ, D2 {U2+c*O2:.0f} MJ -> true best D{'1' if U1+c*O1 < U2+c*O2 else '2'}")
cstar = -(U2 - U1) / (O2 - O1)
print(f"  break-even c* = -dU/dO = {cstar:.4f}")
B1, B2 = U1 / TREF + O1 / 150, U2 / TREF + O2 / 150
print(f"  (B): D1 {B1:.4f} MJ/K, D2 {B2:.4f} MJ/K -> prefers D{'1' if B1 < B2 else '2'}")
print(f"  (B) implicit rate on operation relative to upstream = T_ref/150 = {TREF/150:.4f}")

print("== claim 6: Al chemical exergy ==")
print(f"  33 MJ/kg / T_ref = {33/TREF:.4f} MJ/(kg K)  (+-10 %: {29.7/TREF:.4f} .. {36.3/TREF:.4f})")
print(f"  reviewer recall (UNSURE): 888.4 kJ/mol / 26.98 g/mol = {888.4/26.98:.2f} MJ/kg")
# Web search snippets (2026-11-15, not checked against the full papers): older Szargut table
# 888.4 kJ/mol; Szargut et al. 2005 / Rivero & Garfias 2006 revised value ~795.7-796.1 kJ/mol.
for v in (795.7, 796.1):
    print(f"  revised value (search snippet, UNSURE): {v} kJ/mol / 26.98 g/mol = {v/26.98:.2f} MJ/kg "
          f"-> {v/26.98/TREF:.4f} MJ/(kg K); offset from 33 MJ/kg: {(v/26.98-33)/33*100:+.1f} %")

print("== claim 7: dissipated work, T0 convention 150 vs 290 K ==")
print(f"  S_gen ratio = 290/150 = {290/150:.4f}")
