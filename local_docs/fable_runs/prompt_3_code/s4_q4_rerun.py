"""s4_q4_rerun.py -- Prompt 3, S4 finaliser.

Purpose : targeted re-runs of the Q4 numbers with the inputs S3 put in doubt, and the
          closed-form quantities S2 could not bracket on a grid.  Nothing here redoes
          the S2 unit-cell models; their constants are taken from the S2 output where
          marked "S2".  Level: derived (unverified).
Sections: 1 Basquin anchors (sigma_w7 30..100 MPa, sigma_u 400/460 MPa)
          2 limits on sigma_a at N = 1e7, rho = 0.2
          3 crossover N_x (closed form, no grid)
          4 Delta S per cycle, Sdot, total over life (self-consistent and fixed amplitude)
          5 maximum life-integrated entropy with a service cap (closed form)
          6 comparators and ratios (LPBF up to 600 MJ/kg, c_p alternatives)
          7 damping conventions psi = 2 pi eta = 4 pi zeta
          8 amplitude-dependent psi, n_d = 4 added
          9 thermoelastic damping with alpha_s = 23e-6 and 27e-6 /K
          10 local entropy density against the fatigue fracture entropy
          11 normalised endurance ratio against the values S3 found
Inputs  : local_docs/fable_runs/prompt_3_plan.md section 3.1; changes from
          local_docs/fable_runs/prompt_3_citations.md (a).
Run     : python3 s4_q4_rerun.py > outputs/s4_q4_rerun.txt
Pure Python (system python3, no numpy).
"""
import math

ES = 70e9
SY = 250e6
RHO = 0.2
VENV = 1e-3
PSI = 5e-3
T0 = 300.0
YEAR = 3.15576e7
DAY = 86400.0
RHOS = 2670.0
MP = 1e6
S3 = math.sqrt(3.0)

# S2 constants (p3_unit_cells.txt, R6, rho = 0.2): BCC C1 = E*/(E_s rho^2)
C1_BCC_EB = 0.0902299
C1_BCC_TIMO = 0.08153
# S2 constants (p3_unit_cells.txt, R5): kappa for a circular section, linear moment
KAPPA_CIRC = {2.0: 1.0, 2.3: 1.16207, 2.5: 1.29797, 3.0: 1.76425, 4.0: 3.6}

FAILS = []


def reg(name, val, exp, tol):
    """Regression against a value printed by S2 (shows this script reproduces S2)."""
    err = abs(val - exp) / abs(exp)
    ok = err <= tol
    print(f"  REGRESSION vs S2 {name}: here={val:.6g} S2={exp:.6g} err={err:.2e} -> {'OK' if ok else 'MISMATCH'}")
    if not ok:
        FAILS.append(name)


def topo(rho=RHO, sy=SY, es=ES):
    """name -> (k_peak, E_eff [Pa], collapse [Pa], first yield [Pa])."""
    dl = math.sqrt(rho / (S3 * math.pi))          # BCC d/L
    kA = (1.5 / 0.3) * rho ** -1.5
    kB = (2 * math.sqrt(2) / math.pi) * dl ** -3 + 1 / rho
    kC1 = 3 / rho
    kC2 = 6 / rho
    plB = (4 * math.sqrt(2) / 3) * sy * dl ** 3
    return {
        'A': (kA, es * rho ** 2, 0.3 * rho ** 1.5 * sy, sy / kA),
        'B(EB)': (kB, C1_BCC_EB * es * rho ** 2, plB, sy / kB),
        'B(Timo)': (kB, C1_BCC_TIMO * es * rho ** 2, plB, sy / kB),
        'C100': (kC1, rho * es / 9, rho * sy / 3, sy / kC1),
        'C110': (kC2, rho * es / 6, rho * sy / 6, sy / kC2),
    }


def r2(name, rho=RHO, es=ES):
    """(sigma_peak/sigma_rms)^2 = k_peak^2 rho E_eff/E_s (energy identity)."""
    k, e, _, _ = topo(rho)[name]
    return k * k * rho * e / es


def b_anchor(sw7, su):
    return math.log(sw7 / (1.67 * su)) / math.log(2e7)


def sw(N, sw7, b):
    return sw7 * (N / 1e7) ** b


T = topo()
print("=== 0 regression of the S2 central values ===")
reg('k_peak B (R13)', T['B(EB)'][0], 132.766, 1e-4)
reg('fatigue limit A at 1e7 [MPa] (R14)', 60e6 / T['A'][0] / MP, 1.07331, 1e-4)
reg('fatigue limit B at 1e7 [MPa] (R14)', 60e6 / T['B(EB)'][0] / MP, 0.451922, 1e-4)
reg('r^2 B (R9)', r2('B(EB)'), 12.724, 1e-3)
reg('r^2 A (R17)', r2('A'), 25.0, 1e-9)
reg('r^2 C110 (R2)', r2('C110'), 6.0, 1e-9)
print(f"  r^2: A={r2('A'):.4f} B(EB)={r2('B(EB)'):.4f} B(Timo)={r2('B(Timo)'):.4f} C100={r2('C100'):.4f} C110={r2('C110'):.4f}")
print(f"  E_eff [GPa]: A={T['A'][1]/1e9:.4f} B(EB)={T['B(EB)'][1]/1e9:.4f} B(Timo)={T['B(Timo)'][1]/1e9:.4f} C100={T['C100'][1]/1e9:.4f} C110={T['C110'][1]/1e9:.4f}")
print(f"  E_s rho^2 / E_BCC: EB {1/C1_BCC_EB:.2f}, Timoshenko {1/C1_BCC_TIMO:.2f}")

print("\n=== 1 Basquin anchors: sigma_f' = 1.67 sigma_u; b = ln(sigma_w7/sigma_f')/ln(2e7) ===")
print("  sigma_u [MPa]  sigma_f' [MPa]  machined sigma_w7 (b=-0.095) [MPa] | as-built b for sigma_w7 = 30, 40, 60, 100 MPa")
for su in (400e6, 430e6, 460e6):
    sf = 1.67 * su
    row = "  ".join(f"{b_anchor(s * MP, su):.4f}" for s in (30, 40, 60, 100))
    print(f"  {su/MP:6.0f}        {sf/MP:6.1f}          {sf*(2e7)**-0.095/MP:6.1f}                         | {row}")
print("  as-built / machined ratio implied by sigma_w7 = 30, 60 against 110, 125, 130 MPa (S3 machined values):")
for s in (30, 60):
    print(f"    sigma_w7={s}: " + ", ".join(f"{s/m:.2f}" for m in (110, 125, 130)))
print("  Aboulkhair 2016 lower bound read as a stress range at R = 0.1 (basis UNSURE): range 63 MPa -> amplitude "
      f"{63/2:.1f} MPa, sigma_max {63/0.9:.1f} MPa, mean {63/0.9*0.55:.1f} MPa")

print("\n=== 2 limits on sigma_a at N = 1e7, rho = 0.2, R = -1 [MPa] ===")
print("  first yield / collapse: " + "; ".join(f"{n} {v[3]/MP:.3f} / {v[2]/MP:.3f}" for n, v in T.items() if n != 'B(Timo)'))
print("  sigma_w7  K_n |   A      B      C100   C110   (fatigue-limited sigma_a; binding limit)")
for s in (30, 40, 60, 100):
    for kn in (1, 2):
        vals = []
        for n in ('A', 'B(EB)', 'C100', 'C110'):
            fat = s * MP / (kn * T[n][0])
            bind = 'fat' if fat < T[n][3] else 'yield'
            vals.append(f"{fat/MP:6.3f}({bind})")
        print(f"   {s:4d}    {kn}   | " + " ".join(vals))

print("\n=== 3 crossover N_x = 1e7 (K_n sigma_y/sigma_w7)^(1/b): fatigue binds for N > N_x (closed form) ===")
bs = (-0.07, -0.095, -0.1434, -0.20)
sws = (30, 40, 60, 100)
kns = (1, 1.5, 2, 3, 4)
allx = []
for b in bs:
    for s in sws:
        for kn in kns:
            allx.append((1e7 * (kn * SY / (s * MP)) ** (1 / b), b, s, kn))
print("  rows b; columns sigma_w7 = 30, 40, 60, 100 MPa at K_n = 1")
for b in bs:
    print(f"   b={b:7.4f}: " + "  ".join(f"{1e7*(SY/(s*MP))**(1/b):.3g}" for s in sws))
mx = max(allx)
below = sum(1 for x in allx if x[0] < 1e2)
inside = sum(1 for x in allx if 1e2 <= x[0] <= 1e10)
above = sum(1 for x in allx if x[0] > 1e10)
print(f"  {len(allx)} combinations (4 b x 4 sigma_w7 x 5 K_n): N_x < 1e2 for {below}; inside 1e2..1e10 for {inside}; > 1e10 for {above}")
print(f"  largest N_x = {mx[0]:.3g} (b={mx[1]}, sigma_w7={mx[2]}, K_n={mx[3]})")
s2grid = [x for x in allx if x[2] != 30]
print(f"  S2 grid only (sigma_w7 40, 60, 100): N_x < 1e2 for {sum(1 for x in s2grid if x[0] < 1e2)} of {len(s2grid)} (S2 reported 45 of 60 outside the grid)")
print("  implied sigma_f' = sigma_w7 (2e7)^(-b) below sigma_y = 250 MPa (curve never reaches yield at N >= 1):")
for b in bs:
    print(f"   b={b:7.4f}: " + "  ".join(f"sw7={s}: {s*(2e7)**(-b):.0f} MPa" for s in sws))

print("\n=== 4 Delta S per cycle, Sdot and total over life at the fatigue-limited sigma_a (N = 1e7, K_n = 1) ===")
print("  Delta S = psi V sigma_a^2/(2 E_eff T0); Sdot = nu Delta S; total = 1e7 Delta S; tau = 1e7/nu = "
      f"{1e7/YEAR:.4f} y at 1 Hz, {1e7*DAY/YEAR:.0f} y at 1 per day")
for s in (60, 30):
    print(f"  sigma_w7 = {s} MPa")
    print("    topology   sigma_a [MPa]  dS/cycle [J/K]  Sdot 1 Hz [W/K]  Sdot 1/day [W/K]  total over 1e7 cycles [J/K]  total 30 y at 1/day (10958 cycles) [J/K]")
    for n in ('A', 'B(EB)', 'B(Timo)', 'C100', 'C110'):
        k, e, _, _ = T[n]
        sa = s * MP / k
        dS = PSI * VENV * sa ** 2 / (2 * e * T0)
        print(f"    {n:8s}   {sa/MP:8.4f}      {dS:.4e}     {dS:.4e}      {dS/DAY:.4e}       {dS*1e7:9.2f}                    {dS*10958:.4e}")
print("  prompt's literal cross: fixed sigma_a with both moduli (E_s rho^2 = 2.8 GPa; rho E_s/9 = 1.5556 GPa)")
print("    sigma_a [MPa]  modulus      dS/cycle [J/K]  Sdot 1 Hz [W/K]  Sdot 1/day [W/K] | N_f and total over life [J/K] for sigma_w7 = 60 (b=-0.1434) and 30 (b=-0.1846)")
for sa in (1e6, 2e6):
    for n, lab in (('A', 'E_s rho^2  '), ('C100', 'rho E_s/9  ')):
        k, e, _, fy = T[n]
        dS = PSI * VENV * sa ** 2 / (2 * e * T0)
        out = []
        for s, b in ((60, -0.1434), (30, b_anchor(30e6, 400e6))):
            Nf = 1e7 * (k * sa / (s * MP)) ** (1 / b)
            out.append(f"N_f={Nf:.3e}, S={Nf*dS:.3e}")
        el = '' if sa <= fy else ' (above first yield)'
        print(f"    {sa/MP:4.1f}           {lab}  {dS:.4e}     {dS:.4e}      {dS/DAY:.4e}  | " + " ; ".join(out) + el)
        print(f"                                 strut peak {k*sa/MP:.1f} MPa; total with a 30 y cap instead of N_f: 1 Hz {dS*30*YEAR:.3e} J/K "
              f"(N = {30*YEAR:.3e}); 1/day {dS*30*YEAR/DAY:.3e} J/K (N = {30*YEAR/DAY:.0f}); N_f/nu at 1 Hz for sw7 = 60: "
              f"{1e7*(k*sa/60e6)**(1/-0.1434)/YEAR:.3g} y")
print(f"  ratio of the two moduli at fixed sigma_a = 9 rho = {9*RHO:.2f}")
print("  self-consistent pairs, ratio of Delta S: C100/A = "
      f"{(60e6/T['C100'][0])**2/T['C100'][1] / ((60e6/T['A'][0])**2/T['A'][1]):.2f}; "
      f"C100/B(EB) = {(60e6/T['C100'][0])**2/T['C100'][1] / ((60e6/T['B(EB)'][0])**2/T['B(EB)'][1]):.2f}; "
      f"B(Timo)/B(EB) = {C1_BCC_EB/C1_BCC_TIMO:.4f}")

print("\n=== 5 maximum life-integrated entropy with a service cap tau_s (closed form) ===")
print("  S_max = N* psi rho V s_loc^2/(2 E_s T0 r^2), N* = nu tau_s, s_loc = min(sigma_w(N*)/K_n, sigma_y); sigma_a* = s_loc/k_peak")
S7 = lambda s: 1e7 * PSI * RHO * VENV * (s * MP) ** 2 / (2 * ES * T0)
print(f"  S(1e7) for C100, K_n = 1: sigma_w7 = 60 -> {S7(60):.2f} J/K; 30 -> {S7(30):.2f} J/K")


def smax(name, nu, tau_y, s, b, kn):
    N = nu * tau_y * YEAR
    sloc = sw(N, s * MP, b) / kn
    capped = sloc > SY
    sloc = min(sloc, SY)
    S = N * PSI * RHO * VENV * sloc ** 2 / (2 * ES * T0 * r2(name))
    return S, sloc / T[name][0], N, capped


reg('S_max C100 1 Hz 20 y b=-0.1434 (R19 analytic)', smax('C100', 1.0, 20, 60, -0.1434, 1)[0], 1.6478e4, 1e-3)
reg('S_max C100 1 Hz 30 y b=-0.095 (R19 analytic)', smax('C100', 1.0, 30, 60, -0.095, 1)[0], 3.4182e4, 1e-3)
reg('S_max C100 1/day 30 y b=-0.1434 (R19 analytic)', smax('C100', 1 / DAY, 30, 60, -0.1434, 1)[0], 6.634, 1e-3)
reg('S_max A 1 Hz 20 y b=-0.1434 (R19 analytic)', smax('A', 1.0, 20, 60, -0.1434, 1)[0], 659.126, 1e-3)
reg('S_max B 1 Hz 30 y b=-0.095 (R19 analytic)', smax('B(EB)', 1.0, 30, 60, -0.095, 1)[0], 2686.46, 2e-3)
cases = []
for nu, nulab in ((1.0, '1 Hz'), (1 / DAY, '1/day')):
    print(f"  nu = {nulab}")
    print("    sigma_w7  b        K_n  tau_s[y]   N*         |  S_max [J/K] (sigma_a* [MPa]):  A            B(Timo)        C110           C100")
    for s in (60, 30):
        for b in (-0.095, -0.1434, round(b_anchor(s * MP, 460e6), 4)):
            for kn in (1, 2):
                for tau in (10, 30):
                    cells = []
                    for n in ('A', 'B(Timo)', 'C110', 'C100'):
                        S, sa, N, cap = smax(n, nu, tau, s, b, kn)
                        cells.append(f"{S:9.3e} ({sa/MP:6.3f}{'Y' if cap else ''})")
                        cases.append((S, nulab, n, s, b, kn, tau))
                    print(f"    {s:4d}     {b:8.4f}  {kn}    {tau:2d}      {N:.3e}  |  " + "  ".join(cells))
print("    'Y' after sigma_a* = first yield, not fatigue, sets the amplitude at that N*")
for nulab in ('1 Hz', '1/day'):
    for grp, names in (('bending (A, B)', ('A', 'B(Timo)')), ('stretch (C100, C110)', ('C100', 'C110'))):
        sel = [c for c in cases if c[1] == nulab and c[2] in names]
        lo, hi = min(sel), max(sel)
        print(f"  {nulab}, {grp}: min {lo[0]:.3e} J/K ({lo[2]}, sw7={lo[3]}, b={lo[4]}, K_n={lo[5]}, {lo[6]} y); "
              f"max {hi[0]:.3e} J/K ({hi[2]}, sw7={hi[3]}, b={hi[4]}, K_n={hi[5]}, {hi[6]} y)")
print("  design factor on the allowable stress: 0.8 -> S x %.2f; 0.6 -> S x %.2f (S scales as stress squared)" % (0.8 ** 2, 0.6 ** 2))
print("  psi range of the prompt (1e-3 to 1e-2) scales every S by 0.2 to 2")

print("\n=== 6 comparators (m = rho_s rho V) and ratios ===")
m = RHOS * RHO * VENV
print(f"  m = {m:.3f} kg")
comp = {}
for cp in (739.0, 900.0, 922.0):
    comp[f'melt floor c_p={cp:.0f}'] = m * (cp * (873.0 - T0) + 397e3) / T0
for e in (50, 148, 200, 300, 500, 600):
    comp[f'LPBF {e} MJ/kg'] = m * e * 1e6 / T0
for e in (150, 200, 220, 260):
    comp[f'primary Al {e} MJ/kg'] = m * e * 1e6 / T0
comp['prompt low 1e3'] = 1e3
comp['prompt high 1e5'] = 1e5
for k, v in comp.items():
    print(f"    {k:26s} {v:.4e} J/K")
head = [
    ('diurnal, any cell, largest (C100, sw7 60, b -0.1434, K_n 1, 30 y)', smax('C100', 1 / DAY, 30, 60, -0.1434, 1)[0]),
    ('1 Hz, bending, largest (B(Timo), sw7 60, b -0.095, K_n 1, 30 y)', smax('B(Timo)', 1.0, 30, 60, -0.095, 1)[0]),
    ('1 Hz, C100, sw7 60, b -0.095, K_n 1, 30 y (largest of all)', smax('C100', 1.0, 30, 60, -0.095, 1)[0]),
    ('1 Hz, C100, sw7 60, b -0.1434, K_n 1, 30 y', smax('C100', 1.0, 30, 60, -0.1434, 1)[0]),
    ('1 Hz, C100, sw7 30, b -0.095, K_n 1, 30 y', smax('C100', 1.0, 30, 30, -0.095, 1)[0]),
    ('1 Hz, C100, sw7 30, b -0.1929, K_n 1, 30 y', smax('C100', 1.0, 30, 30, -0.1929, 1)[0]),
    ('1 Hz, C100, sw7 30, b -0.1929, K_n 2, 30 y', smax('C100', 1.0, 30, 30, -0.1929, 2)[0]),
    ('1 Hz, C100 at the 1e7 fatigue limit, sw7 60 (0.317 y life)', S7(60)),
    ('1 Hz, A at the 1e7 fatigue limit, sw7 60 (0.317 y life)', S7(60) / 25),
]
keys = ('melt floor c_p=900', 'LPBF 50 MJ/kg', 'LPBF 600 MJ/kg', 'primary Al 200 MJ/kg', 'prompt low 1e3', 'prompt high 1e5')
print("  ratios S/comparator: " + " | ".join(keys) + " | (LPBF 50 + primary 200)")
for lab, S in head:
    print(f"    {lab:62s} S={S:.3e}: " + " ".join(f"{S/comp[k]:.2e}" for k in keys)
          + f" {S/(comp['LPBF 50 MJ/kg']+comp['primary Al 200 MJ/kg']):.2e}")

print("\n=== 7 damping conventions: psi = Delta U/U = 2 pi eta = 4 pi zeta (small damping) ===")
for lab, eta in (('dural loss factor low', 4e-4), ('dural loss factor high', 1e-3), ('pure Al low', 2e-5), ('pure Al high', 2e-3)):
    print(f"    eta = {eta:.1e} ({lab}): psi = {2*math.pi*eta:.3e}; psi/5e-3 = {2*math.pi*eta/5e-3:.2f}")
for lab, z in (('LPBF AlSi10Mg modal, low', 0.013e-2), ('LPBF AlSi10Mg modal, high', 0.311e-2), ('LPBF AlSi10Mg modal, max of another study', 1.0348e-2)):
    print(f"    zeta = {z:.4e} ({lab}): psi = {4*math.pi*z:.3e}; psi/5e-3 = {4*math.pi*z/5e-3:.2f}")
print(f"    if the prompt's 5e-3 were a loss factor eta: psi = {2*math.pi*5e-3:.3e} (x {2*math.pi:.2f}); if a damping ratio zeta: psi = {4*math.pi*5e-3:.3e} (x {4*math.pi:.2f})")

print("\n=== 8 factor on Sdot from amplitude-dependent psi, kappa(n_d) (sigma_rms/sigma_ref)^(n_d-2), n_d = 4 added ===")
srms = {'A': 60.0 / math.sqrt(r2('A')), 'B(EB)': 60.0 / math.sqrt(r2('B(EB)')), 'C100': 60.0}
print("  sigma_rms at the sigma_w7 = 60 MPa limit [MPa]: " + ", ".join(f"{k}={v:.3f}" for k, v in srms.items()))
lo, hi = 1e9, 0.0
for n in ('A', 'B(EB)', 'C100'):
    print(f"  {n}: rows n_d; columns sigma_ref = 5, 20, 60 MPa")
    for nd in (2.3, 2.5, 3.0, 4.0):
        kap = 1.0 if n == 'C100' else KAPPA_CIRC[nd]
        vals = [kap * (srms[n] / sr) ** (nd - 2) for sr in (5, 20, 60)]
        if nd <= 3.0:
            lo, hi = min(lo, *vals), max(hi, *vals)
        print(f"    n_d={nd}: " + "  ".join(f"{v:9.4f}" for v in vals))
print(f"  range for n_d 2.3..3 (S2 R22): {lo:.3f} to {hi:.3f}; n_d = 2.3 only: "
      + ", ".join(f"{n}: {min((1.0 if n=='C100' else KAPPA_CIRC[2.3])*(srms[n]/sr)**0.3 for sr in (5,20,60)):.2f}-{max((1.0 if n=='C100' else KAPPA_CIRC[2.3])*(srms[n]/sr)**0.3 for sr in (5,20,60)):.2f}" for n in srms))

print("\n=== 9 thermoelastic damping with alpha_s = 21, 23, 27e-6 /K (k = 130 W/(m K), c_p = 900) ===")
D = 130.0 / (RHOS * 900.0)
for a in (21e-6, 23e-6, 27e-6):
    dE = ES * a * a * T0 / (RHOS * 900.0)
    row = []
    for t in (0.5e-3, 1e-3, 2e-3, 5e-3):
        fz = math.pi * D / (2 * t * t)
        x = 1.0 / fz
        row.append(f"t={t*1e3:.1f} mm: {2*math.pi*dE*x/(1+x*x):.3e} ({2*math.pi*dE*x/(1+x*x)/5e-3:.3f})")
    print(f"  alpha_s={a*1e6:.0f}e-6: Delta_E={dE:.4e}; psi_TE,max = pi Delta_E = {math.pi*dE:.4e} ({math.pi*dE/5e-3:.2f} x 5e-3); psi_TE(1 Hz) (ratio to 5e-3): " + "; ".join(row))
print("  f_Z [Hz] for t = 0.5, 1, 2, 5 mm: " + ", ".join(f"{math.pi*D/(2*t*t):.1f}" for t in (0.5e-3, 1e-3, 2e-3, 5e-3)))

print("\n=== 10 local entropy density s(N) = N psi sigma_w(N)^2/(2 E_s T0) against 4 MJ/(m^3 K) ===")
print("  sigma_w7  b        | s(N)/4e6 at N = 1e6, 1e7, 1e8, 1e9")
for s, b in ((60, -0.095), (60, -0.1434), (30, -0.095), (30, b_anchor(30e6, 400e6))):
    print(f"   {s:3d}     {b:8.4f} | " + "  ".join(f"{N*PSI*sw(N, s*MP, b)**2/(2*ES*T0)/4e6:.4g}" for N in (1e6, 1e7, 1e8, 1e9)))
print("  a constant accumulated entropy at failure needs dissipation per cycle ~ sigma^(-1/b): exponent "
      + ", ".join(f"{-1/b:.2f} (b={b})" for b in (-0.07, -0.095, -0.1434, -0.20)))

print("\n=== 11 normalised endurance ratio: model against the values S3 found ===")
print("  model amplitude/lattice yield = sigma_w/(f K_n sigma_y) bending (f = 1.5), sigma_w/(K_n sigma_y) stretch, K_n = 1;")
print(f"  as sigma_max at R = 0.1: x 2/(1-R) = {2/0.9:.4f}; reported values taken as sigma_max over lattice yield at R = 0.1 (basis UNSURE)")
rep = (0.15, 0.2, 0.25, 0.6)
for lab, swv, sy in (('Ti-6Al-4V', (150, 200, 300), 950.0), ('AlSi10Mg', (30, 60), 250.0)):
    for s in swv:
        bend = s / (1.5 * sy)
        stre = s / sy
        print(f"  {lab} sigma_w={s}: amplitude ratio bend {bend:.3f}, stretch {stre:.3f}; sigma_max basis bend {bend*2/0.9:.3f}, stretch {stre*2/0.9:.3f}; "
              f"model(bend)/reported {rep}: " + ", ".join(f"{bend*2/0.9/r:.2f}" for r in rep)
              + "; model(stretch)/reported: " + ", ".join(f"{stre*2/0.9/r:.2f}" for r in rep))
print("  the ratio model/reported is also the K_n that would make the model match; quoting it as K_n would be a fit, not a result")

print("\n==== SUMMARY ====")
print("  regression mismatches against S2: " + (", ".join(FAILS) if FAILS else "none"))
