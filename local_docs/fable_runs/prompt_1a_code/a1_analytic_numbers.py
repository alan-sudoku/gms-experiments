"""A1/A2 closed-form numbers: skin depths, Claim A's formula, and what it implies.

What it computes
    1. Skin depths of Cu, Al and the homogenised lattice at 5, 10 and 100 kHz.
    2. Claim A's factor F(xi) = xi (sinh 2xi + sin 2xi)/(cosh 2xi - cos 2xi): the small-xi
       expansion 1 + 4 xi^4/45, and the minimum of F(xi)/xi (optimum plate or wall
       thickness: 1.57 delta per one-sided field, value 0.917).
    3. What Claim A's model predicts for the A3 case (lattice struts 0.228 mm, each
       strut treated as an isolated foil; solid Cu bar treated as a 1-D plate) next to
       the 2-D field solution, i.e. the size of the claim's error.
    4. Thick-limit scaling ratios sqrt(sigma_Cu/sigma_Al), sqrt(1/rho_bar), ...
    5. Strut-level proximity loss as a fraction of the bar-scale loss:
       fill (t/delta)^2 / 6 for square struts, fill (d/delta)^2 / 8 for round struts.
    6. Ideal Litz estimate in the same envelope: R_dc/fill * (1 + fill^2 h^2 d^2/(48 delta^4)).

Which answer items it supports
    A1.1-A1.4, A2.1, A2.7, A3 (the 'claim-implied' column).

Assumptions
    1-D (plane) field for every closed form; low-frequency (d << delta) dipole loss for
    items 5 and 6; ideal transposition for item 6; 20 C conductivities; mu = mu0.
    Items 5 and 6 are this answer's own derivations (level `derived`).

Run time: a few seconds.
"""
import math

from eddy2d import S_AL, S_CU, delta, dowell_skin, solid_bar, solve

a, b = 50e-3, 5e-3
A = 4 * a * b
P = 4 * (a + b)
FILL = 0.3

print("== 1. skin depths [mm]")
for f in (5e3, 1e4, 1e5):
    print(f"   f={f:7.0f} Hz  Cu {delta(S_CU,f)*1e3:.4f}  Al {delta(S_AL,f)*1e3:.4f}  "
          f"lattice 0.300*sAl {delta(0.3*S_AL,f)*1e3:.4f}  0.222*sAl {delta(0.6/2.7*S_AL,f)*1e3:.4f}  "
          f"0.100*sAl {delta(0.1*S_AL,f)*1e3:.4f}")

print("\n== 2. Claim A's factor F(xi)")
for xi in (0.1, 0.28, 0.5, 0.88, 1.0, 1.5, 2.0, 3.0, 5.0):
    print(f"   xi={xi:5.2f}  F={dowell_skin(xi):8.4f}   1+4xi^4/45={1+4*xi**4/45:8.4f}   F/xi={dowell_skin(xi)/xi:7.4f}")
best = min(((dowell_skin(x / 1000) / (x / 1000), x / 1000) for x in range(500, 4000)))
print(f"   minimum of F/xi: {best[0]:.4f} at xi = {best[1]:.3f}  (thick limit F/xi -> 1)")

print("\n== 3. Claim A's model applied to the A3 case vs the 2-D field solution")
t_w = math.sqrt(FILL) * (5e-3 / 12)          # strand side of the 0.417 mm-pitch bundle
for f in (1e4, 1e5):
    xi = t_w / delta(S_AL, f)
    r_lat_claim = dowell_skin(xi) / (FILL * S_AL * A)
    xi_cu = 2 * b / delta(S_CU, f)
    r_cu_one = dowell_skin(xi_cu) / (S_CU * A)           # field on one face (as the formula is written)
    r_cu_two = dowell_skin(xi_cu / 2) / (S_CU * A)       # field on both faces (isolated plate)
    r_cu_2d = solve(solid_bar(a, b, S_CU, f, 1), f)["R"]
    r_lat_2d = solve(solid_bar(a, b, FILL * S_AL, f, 1), f)["R"]
    print(f"   f={f:.0f}: strut t_w={t_w*1e3:.3f} mm xi={xi:.3f} F={dowell_skin(xi):.4f}")
    print(f"      lattice: claim {r_lat_claim*1e6:8.2f} uOhm/m   2-D homogenised {r_lat_2d*1e6:8.2f}   "
          f"claim underestimates by x{r_lat_2d/r_lat_claim:.1f}")
    print(f"      solid Cu: claim formula, xi=t/delta={xi_cu:.2f}: {r_cu_one*1e6:8.2f};  xi=t/(2delta): {r_cu_two*1e6:8.2f};  "
          f"2-D: {r_cu_2d*1e6:8.2f} uOhm/m")
    print(f"      R_lattice/R_Cu: claim {r_lat_claim/r_cu_one:.3f} (one-sided) or {r_lat_claim/r_cu_two:.3f} (two-sided);"
          f"  2-D {r_lat_2d/r_cu_2d:.3f}")

print("\n== 4. thick-limit scaling ratios (R ~ 1/sqrt(sigma) at fixed shape)")
print(f"   sqrt(sCu/sAl) = {math.sqrt(S_CU/S_AL):.4f}")
for name, k in (("0.300", 0.3), ("0.222", 0.6 / 2.7), ("0.100", 0.1)):
    print(f"   sigma_eff={name}*sAl: R/R_solidAl = {math.sqrt(1/k):.3f}   R/R_solidCu = {math.sqrt(S_CU/(k*S_AL)):.3f}"
          f"   DC: R/R_solidCu = {S_CU/(k*S_AL):.2f}")

print("\n== 5. strut-level proximity loss / bar-scale loss (thin struts, pitch << delta_eff)")
for f in (1e4, 1e5):
    d = delta(S_AL, f)
    for t in (0.1e-3, 0.2e-3, 0.228e-3, 0.259e-3):
        print(f"   f={f:.0f} t={t*1e3:.3f} mm t/delta={t/d:.2f}: square fill*(t/d)^2/6 = {FILL*(t/d)**2/6:.4f}"
              f"   round fill*(d/delta)^2/8 = {FILL*(t/d)**2/8:.4f}")

print("\n== 6. ideal Al Litz, fill 0.3, bundle 10 x 100 mm (h = 10 mm)")
h = 2 * b
rdc = 1 / (FILL * S_AL * A)
for f, ds in ((1e4, (0.3e-3, 0.2e-3, 0.1e-3)), (1e5, (0.1e-3, 0.071e-3, 0.05e-3))):
    d = delta(S_AL, f)
    for dia in ds:
        ratio = FILL ** 2 * h ** 2 * dia ** 2 / (48 * d ** 4)
        n = FILL * A / (math.pi * dia ** 2 / 4)
        print(f"   f={f:.0f} strand d={dia*1e3:.3f} mm (d/delta={dia/d:.2f}) strands={n:8.0f}  R_dc={rdc*1e6:.2f}  "
              f"prox ratio={ratio:.3f}  R'={rdc*(1+ratio)*1e6:7.2f} uOhm/m")
