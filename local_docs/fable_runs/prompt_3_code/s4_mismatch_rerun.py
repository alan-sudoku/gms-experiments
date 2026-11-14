"""s4_mismatch_rerun.py -- Prompt 3, S4 finaliser.

Purpose : targeted re-runs of the thermal-mismatch numbers (plan rows R28-R32) with the
          inputs S3 put in doubt, and two checks S2 was not asked for.
          Level: derived (unverified).
Sections: 1 bilayer plate, exact two-unknown solution: what 1/(1+S) leaves out
            (bending relief), and the equal-modulus bimetal check 1/8 + 3/8
          2 local amplitude and life at diurnal Delta T, sigma_w7 30/60 MPa,
            alpha_s 21/23/27e-6 /K, all five partners
          3 Delta T_x at N = 10958 cycles (30 years at 1 per day), closed form, with
            three flags; mean stress as a bound pair (none / Goodman)
          4 BCC constant c: Euler-Bernoulli against Timoshenko (S2 values)
          5 dissipation under strain control with alpha_s 27e-6 /K
          6 thermal-lag magnitudes with alpha_s 27e-6 /K
Model   : sigma_a,loc = (1/2) K_n c E_s abs(alpha_s - alpha_2) Delta T/(1+S)
          N = 1e7 (g sigma_a,loc/sigma_w7)^(1/b);  g = 1 or 1/(1 - sigma_m/sigma_u)
          S = M_L H_L/(M_2 H_2), M_L = rho E_s/6 (octet, rho = 0.2), M_2 = E_2/(1-nu_2)
Run     : python3 s4_mismatch_rerun.py > outputs/s4_mismatch_rerun.txt
Pure Python (system python3, no numpy).
"""
import math

ES = 70e9
SY = 250e6
RHO = 0.2
VENV = 1e-3
PSI = 5e-3
T0 = 300.0
MP = 1e6
NCYC = 10958.0          # 30 years at 1 per day
DAYS_PER_YEAR = 365.25
PARTNERS = {            # alpha [1/K], E [Pa], nu  (plan section 3.1)
    'Ti-6Al-4V': (8.6e-6, 114e9, 0.34),
    'steel': (12e-6, 200e9, 0.30),
    '316L': (16e-6, 193e9, 0.30),
    'Cu': (16.5e-6, 120e9, 0.34),
    'Invar': (1.3e-6, 141e9, 0.29),
}
ML_OCT = RHO * ES / 6
# S2 constants (p3_unit_cells.txt, R7): BCC sigma_peak/(E_s eps_m), equibiaxial
C_BCC = {0.1: (0.67603, 0.64238), 0.2: (0.94338, 0.85669), 0.3: (1.13537, 0.99007),
         0.4: (1.28618, 1.08135), 0.5: (1.40973, 1.14667)}
# S2 constants (p3_mismatch.txt, R31): equibiaxial moduli at rho = 0.2 [Pa]
ML_ALL = {'octet': 2.3333e9, 'BCC': 0.4793e9, 'A': 4.0e9}
FAILS = []


def reg(name, val, exp, tol):
    err = abs(val - exp) / abs(exp)
    ok = err <= tol
    print(f"  REGRESSION vs S2 {name}: here={val:.6g} S2={exp:.6g} err={err:.2e} -> {'OK' if ok else 'MISMATCH'}")
    if not ok:
        FAILS.append(name)


def M2(pn):
    return PARTNERS[pn][1] / (1 - PARTNERS[pn][2])


def S_of(pn, h=1.0, ML=ML_OCT):
    return ML * h / M2(pn)


def b_anchor(sw7, su):
    return math.log(sw7 / (1.67 * su)) / math.log(2e7)


def sig_loc(dalpha, dT, kn, c, S):
    return 0.5 * kn * c * ES * dalpha * dT / (1 + S)


def nlife(sar, sw7, b):
    return 1e7 * (sar / sw7) ** (1 / b)


def dTx(dalpha, kn, c, S, sw7, b, g=1.0):
    """Closed form: Delta T at which N = NCYC."""
    return 2 * sw7 * (NCYC / 1e7) ** b * (1 + S) / (g * kn * c * ES * dalpha)


# ----------------------------------------------------------------------
print("=== 1 bilayer plate: exact solution with bending against 1/(1+S) ===")
print("  layer L (lattice): modulus M_L, thickness H_L, free strain eps_m; layer 2 (partner): M_2, H_2, free strain 0")
print("  unknowns: interface strain e0 and curvature kappa; equations: zero net force and zero net moment")
print("  phi(z) = -(elastic strain in L)/eps_m = strut-stress factor that replaces 1/(1+S)")


def bilayer(ML, HL, M2_, H2):
    a11 = ML * HL + M2_ * H2
    a12 = ML * HL ** 2 / 2 - M2_ * H2 ** 2 / 2
    a22 = ML * HL ** 3 / 3 + M2_ * H2 ** 3 / 3
    b1 = ML * HL
    b2 = ML * HL ** 2 / 2
    det = a11 * a22 - a12 * a12
    e0 = (b1 * a22 - b2 * a12) / det
    kap = (a11 * b2 - a12 * b1) / det
    phi = lambda z: 1 - e0 - kap * z
    return e0, kap, phi(0.0), phi(HL / 2), phi(HL)


e0, kap, p0, pm, pt = bilayer(1.0, 1.0, 1.0, 1.0)
print(f"  bimetal check (equal modulus, equal thickness, uniaxial): interface stress/(E eps) = {p0:.6f} (expect 0.5); "
      f"mean (force) part = {pm:.6f} (expect 1/8); bending part = {p0-pm:.6f} (expect 3/8); far surface = {pt:.6f} (expect -0.25)")
if abs(p0 - 0.5) > 1e-12 or abs(pm - 0.125) > 1e-12:
    FAILS.append('bimetal 1/8 + 3/8')
print("  case                                   h=H_L/H_2   S        1/(1+S)   free to bend: phi(interface)  phi(mid)   phi(top)   first order 1-(4+3h)S")
for lab, ML, pn in (('octet rho 0.2 on Ti-6Al-4V', ML_OCT, 'Ti-6Al-4V'),
                    ('octet rho 0.2 on steel', ML_OCT, 'steel'),
                    ('A rho 0.4 on Ti-6Al-4V', 0.16 * ES / 0.7, 'Ti-6Al-4V'),
                    ('BCC rho 0.2 on Ti-6Al-4V', ML_ALL['BCC'], 'Ti-6Al-4V')):
    for h in (0.1, 0.5, 1.0, 2.0, 10.0):
        S = ML * h / M2(pn)
        _, _, p0, pm, pt = bilayer(ML, h, M2(pn), 1.0)
        print(f"  {lab:38s} {h:5.1f}     {S:.5f}  {1/(1+S):.4f}    {p0:.4f}                       {pm:.4f}     {pt:.4f}     {1-(4+3*h)*S:.4f}")
reg('S octet rho 0.2, Ti, h = 1 (R29)', S_of('Ti-6Al-4V'), 0.0135088, 1e-4)
reg('S A rho 0.4, Ti, h = 1 (R29)', 0.16 * ES / 0.7 / M2('Ti-6Al-4V'), 0.0926316, 1e-4)

# ----------------------------------------------------------------------
print("\n=== 2 local amplitude and life at diurnal Delta T (octet S at H_L = H_2, c = 1, no mean stress) ===")
St = S_of('Ti-6Al-4V')
reg('sigma_a,loc Ti 50 K K_n=3 with S [MPa] (R28)', sig_loc(12.4e-6, 50, 3, 1, St) / MP, 64.2323, 1e-4)
reg('N(50 K) Ti K_n=3 b=-0.1434 S=0 (R30)', nlife(sig_loc(12.4e-6, 50, 3, 1, 0.0), 60e6, -0.1434), 5.66149e6, 1e-4)
reg('N(50 K) Ti K_n=3 b=-0.1434 with S (R30)', nlife(sig_loc(12.4e-6, 50, 3, 1, St), 60e6, -0.1434), 6.21683e6, 1e-4)
reg('dT_x Ti K_n=3 b=-0.1434 S=0 [K] (R30)', dTx(12.4e-6, 3, 1, 0.0, 60e6, -0.1434), 122.474, 1e-4)
reg('dT_x Ti K_n=3 b=-0.1434 with S [K] (R30)', dTx(12.4e-6, 3, 1, St, 60e6, -0.1434), 124.128, 1e-4)
reg('dT_x Ti K_n=3 Goodman sigma_m=250, sigma_u=400, S=0 [K] (R30)', dTx(12.4e-6, 3, 1, 0.0, 60e6, -0.1434, 1 / (1 - 250 / 400)), 45.93, 1e-3)
reg('dT_x Invar K_n=3 b=-0.095 S=0 [K] (R30)', dTx(19.7e-6, 3, 1, 0.0, 60e6, -0.095), 55.4, 2e-3)
print("  effect of S on the Ti, 50 K, K_n = 3 case: stress x %.4f; life x %.4f (b = -0.1434), x %.4f (b = -0.095)"
      % (1 / (1 + St), (1 + St) ** (1 / 0.1434), (1 + St) ** (1 / 0.095)))
print("  effect of sigma_w7 60 -> 30 MPa at fixed b on life: x %.3g (b = -0.1434), x %.3g (b = -0.095)" % (0.5 ** (1 / 0.1434), 0.5 ** (1 / 0.095)))

ALPHAS = (21e-6, 23e-6, 27e-6)
print("  years to failure at 1 cycle per day; '>cap' means N > 1e7 cycles (27 379 y, outside the fitted range); '*' = below 30 y")
print("  columns: Delta T = 20 K and 50 K, each for K_n = 1, 2, 3")


def yrs(N):
    if N > 1e7:
        return '   >cap'
    y = N / DAYS_PER_YEAR
    return f"{y:7.3g}" + ('*' if y < 30 else ' ')


worst = []
for a in ALPHAS:
    for sw7 in (60e6, 30e6):
        for b in (-0.095, round(b_anchor(sw7, 400e6), 4)):
            print(f"  alpha_s={a*1e6:.0f}e-6  sigma_w7={sw7/MP:.0f} MPa  b={b}")
            for pn, (a2, _, _) in PARTNERS.items():
                da = abs(a - a2)
                S = S_of(pn)
                cells = []
                for dT in (20, 50):
                    for kn in (1, 2, 3):
                        N = nlife(sig_loc(da, dT, kn, 1.0, S), sw7, b)
                        cells.append(yrs(N))
                        if dT == 50:
                            worst.append((N / DAYS_PER_YEAR, pn, a, sw7, b, kn))
                s50 = sig_loc(da, 50, 1, 1.0, S) / MP
                print(f"    {pn:10s} dalpha={da*1e6:5.1f}e-6  sigma_a,loc(50 K, K_n=1)={s50:6.2f} MPa | 20 K: " + " ".join(cells[:3]) + " | 50 K: " + " ".join(cells[3:]))
print("  count of (partner, alpha_s, sigma_w7, b) cases at 50 K with life below 30 years, by K_n:")
for kn in (1, 2, 3):
    sel = [w for w in worst if w[5] == kn]
    bad = [w for w in sel if w[0] < 30]
    print(f"    K_n={kn}: {len(bad)} of {len(sel)}"
          + ("; shortest %.3g y (%s, alpha_s=%.0fe-6, sigma_w7=%.0f, b=%s)" % (min(bad)[0], min(bad)[1], min(bad)[2] * 1e6, min(bad)[3] / MP, min(bad)[4]) if bad else ""))
print("  same count restricted to the plan inputs (alpha_s = 21e-6, sigma_w7 = 60 MPa):")
for kn in (1, 2, 3):
    sel = [w for w in worst if w[5] == kn and w[2] == 21e-6 and w[3] == 60e6]
    bad = [w for w in sel if w[0] < 30]
    print(f"    K_n={kn}: {len(bad)} of {len(sel)}; shortest life {min(sel)[0]:.3g} y ({min(sel)[1]}, b={min(sel)[4]})")
print("  same count for sigma_w7 = 30 MPa with alpha_s = 21e-6 (only the fatigue input changed):")
for kn in (1, 2, 3):
    sel = [w for w in worst if w[5] == kn and w[2] == 21e-6 and w[3] == 30e6]
    bad = [w for w in sel if w[0] < 30]
    print(f"    K_n={kn}: {len(bad)} of {len(sel)}; shortest life {min(sel)[0]:.3g} y ({min(sel)[1]}, b={min(sel)[4]})")

# ----------------------------------------------------------------------
print("\n=== 3 Delta T_x [K] at N = 10958 cycles, closed form (no bracket needed) ===")
print("  flags at Delta T_x: n = notch-root range K_n c E_s eps_m/(1+S) above sigma_y (S2's criterion, here with S);")
print("                      Y = nominal strut range c E_s eps_m/(1+S) above sigma_y; T = Delta T_x above 500 K (outside any service range)")
print("  local amplitude allowed at N = 10958 [MPa]: " + "; ".join(
    f"sw7={sw7/MP:.0f}, b={b}: {sw7*(NCYC/1e7)**b/MP:.1f}" for sw7 in (60e6, 30e6) for b in (-0.095, round(b_anchor(sw7, 400e6), 4))))


def flags(da, dT, kn, c, S):
    rng = c * ES * da * dT / (1 + S)
    f = ''
    if kn * rng > SY:
        f += 'n'
    if rng > SY:
        f += 'Y'
    if dT > 500:
        f += 'T'
    return f


for a in ALPHAS:
    for sw7 in (60e6, 30e6):
        for b in (-0.095, round(b_anchor(sw7, 400e6), 4)):
            print(f"  alpha_s={a*1e6:.0f}e-6  sigma_w7={sw7/MP:.0f} MPa  b={b}:  K_n = 1, 2, 3 (c = 1) | K_n = 3, c = 1.49")
            for pn, (a2, _, _) in PARTNERS.items():
                da = abs(a - a2)
                S = S_of(pn)
                cells = []
                for kn, c in ((1, 1.0), (2, 1.0), (3, 1.0), (3, 1.49)):
                    x = dTx(da, kn, c, S, sw7, b)
                    cells.append(f"{x:7.1f}{flags(da, x, kn, c, S):3s}")
                print(f"    {pn:10s} " + " ".join(cells[:3]) + " | " + cells[3])
print("  mean stress from cool-down (Ti-6Al-4V and Invar, K_n = 3, c = 1, octet S): bound pair")
print("    lower bound on Delta T_x: Goodman, sigma_m = min(sigma_y, E_s dalpha dT_ref), dT_ref = 300 K; upper bound: no mean-stress effect")
for su in (400e6, 460e6):
    for a in (21e-6, 27e-6):
        for sw7 in (60e6, 30e6):
            b = round(b_anchor(sw7, 400e6), 4)
            row = []
            for pn in ('Ti-6Al-4V', 'Invar'):
                da = abs(a - PARTNERS[pn][0])
                S = S_of(pn)
                sm = min(SY, ES * da * 300.0)
                g = 1 / (1 - sm / su)
                row.append(f"{pn}: sigma_m={sm/MP:.0f} MPa, g={g:.3f}, dT_x {dTx(da, 3, 1.0, S, sw7, b, g):.1f} to {dTx(da, 3, 1.0, S, sw7, b):.1f} K")
            print(f"    sigma_u={su/MP:.0f} alpha_s={a*1e6:.0f}e-6 sigma_w7={sw7/MP:.0f} b={b}: " + "; ".join(row))
print(f"  dT_ref at which E_s dalpha dT_ref = sigma_y: Ti {SY/(ES*12.4e-6):.0f} K (alpha_s 21e-6), {SY/(ES*18.4e-6):.0f} K (alpha_s 27e-6); "
      f"Invar {SY/(ES*19.7e-6):.0f} K, {SY/(ES*25.7e-6):.0f} K")

# ----------------------------------------------------------------------
print("\n=== 4 BCC constant c = sigma_peak/(E_s eps_m), equibiaxial strain (S2 R7 values) ===")
print("  rho    c (Euler-Bernoulli)  c (Timoshenko)  1/c EB   1/c Timo   (1/c is the margin of the c = 1 screen; below 1 = non-conservative)")
for r, (ceb, cti) in C_BCC.items():
    print(f"  {r:.1f}    {ceb:.4f}               {cti:.4f}          {1/ceb:.3f}    {1/cti:.3f}")
print("  crossover c = 1 (S2 R7): rho = 0.2267 (Euler-Bernoulli), 0.3093 (Timoshenko)")
print(f"  original formula E_s rho^2 eps_m as a local stress, rho = 0.2: low by c/rho^2 = {C_BCC[0.2][0]/0.04:.1f} (BCC, EB), {C_BCC[0.2][1]/0.04:.1f} (BCC, Timoshenko), {1/0.04:.1f} (octet)")

# ----------------------------------------------------------------------
print("\n=== 5 dissipation under strain control, Delta S = psi V M_L eps_a^2/T0, 10958 cycles, Delta T = 50 K, Ti-6Al-4V ===")
reg('octet total, alpha_s 21e-6, with S (R31)', NCYC * PSI * VENV * ML_ALL['octet'] * (0.5 * 12.4e-6 * 50 / (1 + 0.01351)) ** 2 / T0, 3.9868e-2, 1e-3)
for a in ALPHAS:
    da = abs(a - 8.6e-6)
    row = []
    for lat, ML in ML_ALL.items():
        S = ML / M2('Ti-6Al-4V')
        ea = 0.5 * da * 50 / (1 + S)
        row.append(f"{lat}: {NCYC*PSI*VENV*ML*ea*ea/T0:.4e}")
    print(f"  alpha_s={a*1e6:.0f}e-6: total over 30 y [J/K] " + "; ".join(row))
da = abs(27e-6 - 1.3e-6)
print("  largest listed case (Invar, alpha_s 27e-6, lattice A): %.4e J/K" % (
    NCYC * PSI * VENV * ML_ALL['A'] * (0.5 * da * 50 / (1 + ML_ALL['A'] / M2('Invar'))) ** 2 / T0))

# ----------------------------------------------------------------------
print("\n=== 6 thermal lag E_s alpha_s dT_lag against the mismatch term E_s dalpha dT (dT = 50 K) ===")
for a in (21e-6, 27e-6):
    for pn in ('Ti-6Al-4V', '316L'):
        da = abs(a - PARTNERS[pn][0])
        print(f"  alpha_s={a*1e6:.0f}e-6 {pn:10s}: lag 10 K = {ES*a*10/MP:.1f} MPa; mismatch = {ES*da*50/MP:.1f} MPa; break-even dT_lag/dT = dalpha/alpha_s = {da/a:.3f}")

print("\n==== SUMMARY ====")
print("  regression mismatches against S2: " + (", ".join(FAILS) if FAILS else "none"))
