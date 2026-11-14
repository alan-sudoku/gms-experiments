"""rv2_entropy_mismatch.py -- Prompt 3, S5 independent review.

Level: derived (unverified). Pure Python, no numpy. Inputs as in prompt_3_plan.md 3.1 and the
S4 changes (sigma_w7 30..60 MPa, sigma_u 400..460 MPa, alpha_s 21..27e-6 /K).

Sections
 1 life-integrated entropy: brute-force sigma_a grid against S4's closed form (independent code)
 2 frequency above 1 Hz (not asked by the prompt; tests the scope of claim 1)
 3 thermoelastic damping: round-strut Zener constant; inter-strut (cell-scale) relaxation in the
   octet, which the answer and the Q1 web answer call "about zero for stretch-dominated cells"
 4 bilayer plate: Timoshenko (1925) closed-form curvature, independent of S4's 2x2 solve
 5 diurnal mismatch life: recount of S4's 0/4/10 of 60, with c = 1.49 (bonded roots) and with a
   cool-down mean stress (Goodman), the end of the bound pair claim 19 does not use
 6 Q3 over-prediction decades and Q4 headline ratios
Run: python3 rv2_entropy_mismatch.py > outputs/rv2_entropy_mismatch.txt
"""
import math

ES, SY, RHO, VENV, PSI, T0 = 70e9, 250e6, 0.2, 1e-3, 5e-3, 300.0
YEAR, DAY, MP = 3.15576e7, 86400.0, 1e6
RHOS, CP, KTH = 2670.0, 900.0, 130.0
M_PART = RHOS * RHO * VENV
COMP = {'melt floor': M_PART * (900 * 573 + 397e3) / T0, 'LPBF 50': M_PART * 50e6 / T0,
        'LPBF 600': M_PART * 600e6 / T0, 'primary Al 200': M_PART * 200e6 / T0}

# ---------------------------------------------------------------- 1
print("=== 1 S(sigma_a) = nu*dS*min(N_f/nu, tau_s), brute-force log grid (20001 points, 0.01..30 MPa) ===")
TOPO = {  # k_peak, E_eff [Pa] at rho 0.2 (S2 constants; pin-jointed octet; BCC Timoshenko)
    'A': (5.0 * RHO ** -1.5, ES * RHO ** 2),
    'B(Timo)': (132.766, 0.08153 * ES * RHO ** 2),
    'C100': (15.0, RHO * ES / 9),
}


def S_of(sa, name, nu, tau, sw7, b, kn=1.0):
    k, E = TOPO[name]
    if kn * k * sa > SY:
        return None                       # above first yield, excluded as in S2
    Nf = 1e7 * (kn * k * sa / sw7) ** (1 / b)
    dS = PSI * VENV * sa * sa / (2 * E * T0)
    return dS * min(Nf, nu * tau * YEAR)


for name, nu, tau, sw7, b, ref in (('C100', 1.0, 30, 60e6, -0.095, 3.418e4), ('B(Timo)', 1.0, 30, 60e6, -0.095, 2.973e3),
                                    ('C100', 1 / DAY, 30, 60e6, -0.1517, 7.429), ('A', 1.0, 20, 60e6, -0.1434, 659.126)):
    best = (0.0, 0.0)
    n = 20001
    for i in range(n):
        sa = 10 ** (-2 + (math.log10(30) + 2) * i / (n - 1)) * MP
        s = S_of(sa, name, nu, tau, sw7, b)
        if s is not None and s > best[0]:
            best = (s, sa)
    print(f"  {name:8s} nu={nu:.3g} Hz tau={tau} y sw7={sw7/MP:.0f} b={b}: grid max {best[0]:.4e} J/K at sigma_a {best[1]/MP:.4f} MPa; "
          f"S4 closed form {ref:.4e}; rel diff {best[0]/ref-1:+.2e}")

# ---------------------------------------------------------------- 2
print("\n=== 2 frequency above 1 Hz: S_max = S(1e7)*(nu tau_s/1e7)^(1+2b), K_n = 1, sigma_w7 = 60 MPa, 30 y (extrapolated Basquin, UNSURE) ===")
S7 = 1e7 * PSI * RHO * VENV * (60e6) ** 2 / (2 * ES * T0)     # r^2 = 1
print(f"  S(1e7, r^2 = 1) = {S7:.2f} J/K; comparators: " + ", ".join(f"{k} {v:.3e}" for k, v in COMP.items()))
for b in (-0.095, -0.1517):
    for nu in (1.0, 10.0, 100.0):
        N = nu * 30 * YEAR
        sw = 60 * (N / 1e7) ** b
        row = []
        for lab, r2 in (('C100 pin r2=1', 1.0), ('C100 rigid r2=3.95', 3.953), ('B r2=11.5', 11.497), ('A r2=25', 25.0)):
            S = S7 * (N / 1e7) ** (1 + 2 * b) / r2
            row.append(f"{lab}: {S:.2e} ({S/COMP['LPBF 50']*100:.1f} % LPBF50)")
        print(f"  b={b} nu={nu:5.0f} Hz N={N:.2e} strut amplitude {sw:.1f} MPa | " + "; ".join(row))

# ---------------------------------------------------------------- 3
print("\n=== 3 thermoelastic damping ===")
D = KTH / (RHOS * CP)
for a in (21e-6, 27e-6):
    dE = ES * a * a * T0 / (RHOS * CP)
    print(f"  alpha_s={a*1e6:.0f}e-6: Delta_E = {dE:.4e}; D = {D:.4e} m^2/s")
    # (a) round strut, first radial mode of a cylinder in bending: f = (j'_11)^2 D/(2 pi R^2), j'_11 = 1.8412
    print("   (a) intra-strut, reed (S2/S4) vs round section (f_Z,round = 1.8412^2*D/(2 pi R^2) = 2.158 D/d^2, weight 0.97):")
    for t in (0.5e-3, 1e-3, 2e-3, 5e-3):
        fr = math.pi * D / (2 * t * t)
        fc = 1.8412 ** 2 * D / (2 * math.pi * (t / 2) ** 2)
        wc = 8 / (1.8412 ** 2 * (1.8412 ** 2 - 1))
        pr = 2 * math.pi * dE * (1 / fr) / (1 + (1 / fr) ** 2)
        pc = 2 * math.pi * dE * wc * (1 / fc) / (1 + (1 / fc) ** 2)
        print(f"       t=d={t*1e3:.1f} mm: f_Z reed {fr:7.1f} Hz, round {fc:7.1f} Hz; psi_TE(1 Hz) reed {pr:.3e} ({pr/PSI:.3f} x psi), round {pc:.3e} ({pc/PSI:.3f} x psi)")
    # (b) inter-strut, octet under [100]: strut stresses +-3 sigma/rho (8 tension, 4 compression struts per node);
    # each strut uniform, ends at the node (mean) temperature: 1D Dirichlet modes, f_n = n^2 pi D/(2 l^2), weight 8/(pi^2 n^2), odd n.
    # relaxation strength = Delta_E * (variance fraction of strut stress), only the bending-free axial part.
    for lab, s in (('[100] pin', [3, 3, 3, 3, -3, -3]), ('[110] pin', [6, 0, 0, 0, 0, 0]), ('[111] pin', [3, 3, 3, -1, -1, -1])):
        m = sum(s) / len(s)
        vf = sum((x - m) ** 2 for x in s) / sum(x * x for x in s)
        print(f"   (b) inter-strut, octet {lab}: variance fraction of strut stress = {vf:.3f} (relaxes at cell scale; mean part relaxes only at envelope scale)")
        if lab != '[100] pin':
            continue
        for cell in (3e-3, 5e-3, 7e-3, 10e-3):
            l = cell / math.sqrt(2)
            f1 = math.pi * D / (2 * l * l)
            for f in (1.0, 1 / DAY):
                tot = 0.0
                for nmode in range(1, 200, 2):
                    fn = nmode * nmode * f1
                    x = f / fn
                    tot += 8 / (math.pi ** 2 * nmode * nmode) * x / (1 + x * x)
                p = 2 * math.pi * dE * vf * tot
                if f == 1.0:
                    p1 = p
                else:
                    pd = p
            print(f"       cell {cell*1e3:4.1f} mm, strut length {l*1e3:.2f} mm: f_1 = {f1:6.2f} Hz; psi_inter(1 Hz) = {p1:.3e} ({p1/PSI:.2f} x psi); psi_inter(1/day) = {pd:.1e}")
print("  (b) is a 1D estimate: node heat capacity, convection and the bending of rigid joints are ignored (UNSURE); FE or a frequency sweep is needed.")

# ---------------------------------------------------------------- 4
print("\n=== 4 bilayer plate, Timoshenko (1925) closed-form curvature with biaxial moduli ===")


def timoshenko(M1, h1, M2, h2):
    """layer 1 has free misfit 1 relative to layer 2; returns phi at interface, mid, top of layer 1."""
    m, n, h = h1 / h2, M1 / M2, h1 + h2
    kap = 6 * (1 + m) ** 2 / (h * (3 * (1 + m) ** 2 + (1 + m * n) * (m * m + 1 / (m * n))))
    P = 2 * kap * (M1 * h1 ** 3 / 12 + M2 * h2 ** 3 / 12) / h     # force per width, from moment balance
    mid = P / (M1 * h1)
    return mid + kap * h1 / 2, mid, mid - kap * h1 / 2


print("  equal layers (bimetal check): interface, mid, top = %.6f %.6f %.6f (S4: 0.5, 0.125, -0.25)" % timoshenko(1, 1, 1, 1))
M2TI = 114e9 / (1 - 0.34)
for lab, ML in (('octet rho 0.2 on Ti-6Al-4V', RHO * ES / 6), ('A rho 0.4 on Ti-6Al-4V', 0.16 * ES / 0.7)):
    for h in (1.0, 10.0):
        p = timoshenko(ML, h, M2TI, 1.0)
        print(f"  {lab}, H_L/H_2={h}: interface {p[0]:.4f}, mid {p[1]:.4f}, top {p[2]:.4f}")
print("  S4 [4M] section 1: octet Ti h=1: 0.9203, 0.8522, 0.7840; A rho 0.4 Ti h=1: 0.7150, 0.4739, 0.2329")

# ---------------------------------------------------------------- 5
print("\n=== 5 diurnal mismatch life (1 per day, 50 K, octet S at H_L = H_2) ===")
PART = {'Ti-6Al-4V': (8.6e-6, 114e9, 0.34), 'steel': (12e-6, 200e9, 0.30), '316L': (16e-6, 193e9, 0.30),
        'Cu': (16.5e-6, 120e9, 0.34), 'Invar': (1.3e-6, 141e9, 0.29)}


def banch(sw7, su=400e6):
    return round(math.log(sw7 / (1.67 * su)) / math.log(2e7), 4)


def life_years(da, kn, c, S, sw7, b, g=1.0, dT=50.0):
    sa = g * 0.5 * kn * c * ES * da * dT / (1 + S)
    return 1e7 * (sa / sw7) ** (1 / b) / 365.25


for c, g_lab in ((1.0, 'c = 1, no mean (S4)'), (1.49, 'c = 1/(1-nu_s) = 1.49, no mean'), (1.0, 'c = 1, Goodman sigma_m = min(sigma_y, E_s dalpha 300 K), sigma_u 460')):
    counts = {1: 0, 2: 0, 3: 0}
    tot = {1: 0, 2: 0, 3: 0}
    for a in (21e-6, 23e-6, 27e-6):
        for sw7 in (60e6, 30e6):
            for b in (-0.095, banch(sw7)):
                for pn, (a2, E2, n2) in PART.items():
                    da = abs(a - a2)
                    S = (RHO * ES / 6) / (E2 / (1 - n2))
                    g = 1.0
                    if 'Goodman' in g_lab:
                        g = 1 / (1 - min(SY, ES * da * 300) / 460e6)
                    for kn in (1, 2, 3):
                        y = life_years(da, kn, c, S, sw7, b, g)
                        tot[kn] += 1
                        if y < 30:
                            counts[kn] += 1
    print(f"  {g_lab}: lives below 30 y: " + ", ".join(f"K_n={k}: {counts[k]} of {tot[k]}" for k in (1, 2, 3)))
S_ti = (RHO * ES / 6) / (114e9 / 0.66)
for su in (400e6, 460e6):
    g = 1 / (1 - SY / su)
    for b in (-0.1434, -0.095):
        print(f"  Ti-6Al-4V, plan inputs (alpha 21e-6, sigma_w7 60), K_n=3, c=1, 50 K, b={b}: life {life_years(12.4e-6, 3, 1, S_ti, 60e6, b):.3g} y without mean; "
              f"{life_years(12.4e-6, 3, 1, S_ti, 60e6, b, g):.3g} y with Goodman sigma_m = sigma_y, sigma_u = {su/MP:.0f} (g = {g:.2f})")
print("  validity check of the Q5 mismatch default (nominal range + mean < sigma_y) at dT_ref = 300 K, 50 K swing, c = 1, alpha_s 21e-6:")
for pn in ('Ti-6Al-4V', 'Invar', 'steel'):
    da = abs(21e-6 - PART[pn][0])
    print(f"    {pn}: mean E_s dalpha dT_ref = {ES*da*300/MP:.0f} MPa; range c E_s dalpha 50 K = {ES*da*50/MP:.1f} MPa; mean + range = {ES*da*350/MP:.0f} MPa vs sigma_y 250")

# ---------------------------------------------------------------- 6
print("\n=== 6 Q3 over-prediction decades log10((K_n k_peak)^(-1/b)), K_n = 1, rho = 0.2 ===")
for name, k in (('C100 pin', 15.0), ('C100 rigid (rv1)', 5.794 / 0.2), ('A', 5.0 * 0.2 ** -1.5), ('B', 132.766)):
    print(f"  {name:18s} k_peak={k:7.2f}: b=-0.095 {math.log10(k)/0.095:5.1f} decades; b=-0.1434 {math.log10(k)/0.1434:5.1f}")
print("  headline ratios (claim 1): " + "; ".join(f"{S:.3e}/{k} = {S/COMP[k]:.3g}" for S, k in
      ((3.418e4, 'LPBF 50'), (3.418e4, 'LPBF 600'), (3.418e4, 'melt floor'), (2.973e3, 'LPBF 50'), (7.429, 'melt floor'))))
print(f"  part mass {M_PART:.4f} kg; melt floor c_p 900: {COMP['melt floor']:.4e} J/K")
