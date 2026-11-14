"""p3_q4_limits.py -- Prompt 3, S2 implementer.

Purpose : Q4 amplitude limits of four lattice topologies (A Gibson-Ashby, B BCC, C octet
          [100] and [110]): volume/mass, collapse, buckling, stress concentration,
          fatigue vs first-yield vs collapse, regression of the superseded 20 MPa case.
          Level: derived (unverified; FROM MEMORY inputs used as given).
Spec rows: R10 (strut volume, mass), R11 (collapse vs rho), R12 (elastic buckling),
          R13 (k_peak vs rho), R14 (limits vs N), R15 (20 MPa regression).
Source  : local_docs/fable_runs/prompt_3_plan.md section 3.2, derivations D1-D3, D6, D7.
Assumptions: rho=0.2, V_env=1e-3 m^3, sigma_y=250 MPa, sigma_w7=60 MPa (as-built, R=-1),
          K_n=1 unless swept; BCC model = Euler-Bernoulli with axial force kept (R6);
          octet = pin-jointed affine (R1/R2).  Pure Python (system python3, no numpy).
Run     : python3 p3_q4_limits.py
"""
# ======================================================================
# Shared block (copied verbatim into every script so each is standalone).
# Pure Python (system python3 has no numpy).  SI units inside, MPa on print.
# ======================================================================
import math, sys

RES = []   # (row, kind, text)


def check(row, name, val, exp, tol, rel=True):
    err = abs(val - exp) / abs(exp) if (rel and exp != 0) else abs(val - exp)
    ok = err <= tol
    print(f"  [{row}] CHECK {name}: computed={val:.6g} expected={exp:.6g} "
          f"err={err:.3g} tol={tol:g} -> {'PASS' if ok else 'FAIL'}")
    RES.append((row, 'PASS' if ok else 'FAIL', name))
    return ok


def check_true(row, name, cond, detail=''):
    print(f"  [{row}] CHECK {name}: {detail} -> {'PASS' if cond else 'FAIL'}")
    RES.append((row, 'PASS' if cond else 'FAIL', name))
    return cond


def identity(row, name, detail=''):
    print(f"  [{row}] IDENTITY (true by construction, not a check) {name}: {detail}")
    RES.append((row, 'IDENTITY', name))


def info(row, msg):
    print(f"  [{row}] INFO {msg}")


def flag(row, msg):
    print(f"  [{row}] FLAG {msg}")
    RES.append((row, 'FLAG', msg))


def summary():
    print("\n==== SUMMARY (this script) ====")
    rows = sorted({r for r, _, _ in RES}, key=lambda s: int(s[1:]))
    for r in rows:
        p = sum(1 for a, k, _ in RES if a == r and k == 'PASS')
        f = sum(1 for a, k, _ in RES if a == r and k == 'FAIL')
        i = sum(1 for a, k, _ in RES if a == r and k == 'IDENTITY')
        g = sum(1 for a, k, _ in RES if a == r and k == 'FLAG')
        print(f"  {r}: PASS={p} FAIL={f} IDENTITY={i} FLAG={g}")
        for a, k, t in RES:
            if a == r and k in ('FAIL', 'FLAG', 'IDENTITY'):
                print(f"      {k}: {t}")


# ---- small linear algebra ----
def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def matinv(M):
    n = len(M)
    A = [list(map(float, M[i])) + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c]))
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c:
                fct = A[r][c]
                A[r] = [x - fct * y for x, y in zip(A[r], A[c])]
    return [row[n:] for row in A]


def matvec(M, v):
    return [dot(r, v) for r in M]


def logspace(lo, hi, n):
    a, b = math.log10(lo), math.log10(hi)
    return [10 ** (a + (b - a) * i / (n - 1)) for i in range(n)]


# ---- inputs (spec 3.1); SI ----
RHO_BAR = 0.2
VENV = 1e-3
PSI = 5e-3
T0 = 300.0
YEAR = 3.15576e7
DAY = 86400.0
ES = 70e9
NUS = 0.33
RHOS = 2670.0
SY = 250e6
SU = 400e6
SW7 = 60e6
SIGF = 668e6
B_AS = -0.1434
B_MACH = -0.095
KN = 1.0
FSHAPE = 1.5
F_CIRC = 16 / (3 * math.pi)
ALPHA_S = 21e-6
KTH = 130.0
CP = 900.0
HF = 397e3
TLIQ = 873.0
PARTNERS = {  # alpha [1/K], E [Pa], nu
    'Ti-6Al-4V': (8.6e-6, 114e9, 0.34),
    'steel': (12e-6, 200e9, 0.30),
    '316L': (16e-6, 193e9, 0.30),
    'Cu': (16.5e-6, 120e9, 0.34),
    'Invar': (1.3e-6, 141e9, 0.29),
}
RHO_SWEEP = [0.05, 0.10, 1 / 9, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]
S3 = math.sqrt(3.0)
MP = 1e6

# ---- octet (pin-jointed affine model), R1/R2 ----
_OCT = [[a / math.sqrt(2) for a in v] for v in
        [(1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1), (0, 1, 1), (0, 1, -1)]]
_VP = [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)]


def octet_C(rho=1.0, Es_=1.0):
    """C_ijkl = rho*Es/6 * sum n_i n_j n_k n_l; returns 6x6 Voigt (engineering shear)."""
    def c(i, j, k, l):
        return rho * Es_ / 6.0 * sum(n[i] * n[j] * n[k] * n[l] for n in _OCT)
    return [[c(i, j, k, l) for (k, l) in _VP] for (i, j) in _VP]


def octet_strain_for_stress(rho, d, Es_=1.0):
    """Strain tensor (3x3) for unit uniaxial stress d(x)d."""
    Sv = matinv(octet_C(rho, Es_))
    nd = math.sqrt(dot(d, d))
    d = [x / nd for x in d]
    sv = [d[i] * d[j] for (i, j) in _VP]
    ev = matvec(Sv, sv)
    eps = [[0.0] * 3 for _ in range(3)]
    for idx, (i, j) in enumerate(_VP):
        if i == j:
            eps[i][i] = ev[idx]
        else:
            eps[i][j] = eps[j][i] = ev[idx] / 2.0
    return eps, Sv, d


def quad(n, eps):
    return sum(n[i] * eps[i][j] * n[j] for i in range(3) for j in range(3))


def octet_struts(rho, d, Es_=1.0):
    """Strut stresses for unit sigma_a along d (Es_ cancels)."""
    eps, Sv, dd = octet_strain_for_stress(rho, d, Es_)
    return [Es_ * quad(n, eps) for n in _OCT]


# ---- BCC strut model (D3/D4), L = 1, Es = 1 normalised unless given ----
NB = [1 / S3, 1 / S3, 1 / S3]


def bcc_props(rho, Es_=1.0, nus=0.33, timo=False, kafac=1.0, L=1.0):
    d = L * math.sqrt(rho / (S3 * math.pi))
    l = S3 * L / 2
    A = math.pi * d * d / 4
    I = math.pi * d ** 4 / 64
    ka = kafac * Es_ * A / l
    kt = 12 * Es_ * I / l ** 3
    if timo:
        G = Es_ / (2 * (1 + nus))
        Phi = 12 * Es_ * I / (0.9 * G * A * l * l)
        kt = kt / (1 + Phi)
    return dict(rho=rho, d=d, l=l, A=A, I=I, ka=ka, kt=kt, L=L, Es=Es_)


def bcc_force(P, eps):
    D = [0.5 * P['L'] * e for e in eps]
    a = dot(D, NB)
    F = [P['ka'] * a * NB[i] + P['kt'] * (D[i] - a * NB[i]) for i in range(3)]
    return F, a


def bcc_parts(P, F):
    """axial stress, bending peak stress (fixed-guided ends), axial force."""
    Nax = dot(F, NB)
    Ft = math.sqrt(max(dot(F, F) - Nax * Nax, 0.0))
    return abs(Nax) / P['A'], Ft * P['l'] * P['d'] / (4 * P['I']), Nax, Ft


def bcc_uniaxial(P, ez=1.0):
    """Uniaxial stress along z, lateral faces free: solve ex=ey from F_x = 0."""
    f0 = bcc_force(P, (0.0, 0.0, ez))[0][0]
    f1 = bcc_force(P, (1.0, 1.0, ez))[0][0]
    ex = -f0 / (f1 - f0)
    F, a = bcc_force(P, (ex, ex, ez))
    sbar = 4 * F[2] / P['L'] ** 2
    ax, bend, Nax, Ft = bcc_parts(P, F)
    return dict(ex=ex, ez=ez, F=F, a=a, sbar=sbar, Estar=sbar / ez, nu=-ex / ez,
                ax=ax, bend=bend, Nax=Nax, Ft=Ft)


def bcc_biaxial(P, em=1.0):
    """Equibiaxial strain em (x,y), sigma_zz = 0: solve ez from F_z = 0."""
    f0 = bcc_force(P, (em, em, 0.0))[0][2]
    f1 = bcc_force(P, (em, em, 1.0))[0][2]
    ez = -f0 / (f1 - f0)
    F, a = bcc_force(P, (em, em, ez))
    sbar = 4 * F[0] / P['L'] ** 2
    ax, bend, Nax, Ft = bcc_parts(P, F)
    return dict(ez=ez, F=F, a=a, sbar=sbar, M=sbar / em, ax=ax, bend=bend,
                peak=ax + bend, Nax=Nax, Ft=Ft)


def bcc_hydro(P, em=1.0):
    F, a = bcc_force(P, (em, em, em))
    ax, bend, Nax, Ft = bcc_parts(P, F)
    return dict(ax=ax, bend=bend, sbar=4 * F[0] / P['L'] ** 2)


def bcc_energy(P, F, nq=20000):
    """(8/L^3)[int M^2/(2 Es I) dx + N^2 l/(2 Es A)], M = F_t (l/2 - x), midpoint rule."""
    Nax = dot(F, NB)
    Ft = math.sqrt(max(dot(F, F) - Nax * Nax, 0.0))
    l = P['l']
    h = l / nq
    s = 0.0
    for i in range(nq):
        x = (i + 0.5) * h
        M = Ft * (l / 2 - x)
        s += M * M
    Ub = s * h / (2 * P['Es'] * P['I'])
    Ua = Nax ** 2 * l / (2 * P['Es'] * P['A'])
    return 8 / P['L'] ** 3 * (Ub + Ua)


def bcc_summary(rho):
    """k_peak, E*/(Es), r^2, collapse/sigma_y for Euler-Bernoulli BCC at rho."""
    P = bcc_props(rho)
    u = bcc_uniaxial(P)
    k = (u['ax'] + u['bend']) / u['sbar']
    kb = u['bend'] / u['sbar']
    U = bcc_energy(P, u['F'])
    srms = math.sqrt(2 * 1.0 * U / rho)          # Es = 1
    r = (u['ax'] + u['bend']) / srms
    rb = u['bend'] / srms
    dL = P['d'] / P['L']
    return dict(P=P, k=k, kb=kb, Estar=u['Estar'], C1=u['Estar'] / rho ** 2, nu=u['nu'],
                r=r, r2=r * r, rb=rb, coll=4 * math.sqrt(2) / 3 * dL ** 3, u=u, U=U)


# ---- topologies (A Gibson-Ashby, B BCC, C octet) at rho, per unit sigma_a ----
def topologies(rho, sy=SY, Es_=ES, fA=FSHAPE):
    out = {}
    out['A'] = dict(k=(fA / 0.3) * rho ** -1.5, Eeff=Es_ * rho ** 2, r2=(fA / 0.3) ** 2,
                    coll=0.3 * rho ** 1.5 * sy)
    b = bcc_summary(rho)
    out['B'] = dict(k=b['k'], Eeff=b['Estar'] * Es_, r2=b['r2'], coll=b['coll'] * sy)
    for name, d in (('C100', (1, 0, 0)), ('C110', (1, 1, 0))):
        st = octet_struts(rho, d)
        eps, Sv, dd = octet_strain_for_stress(rho, d)
        Ed = 1.0 / quad(dd, eps)                     # normalised, Es = 1
        peak = max(abs(s) for s in st)
        r2 = peak ** 2 / (sum(s * s for s in st) / 6)
        k = peak                                   # sigma_a = 1, strut stress = k*sigma_a
        out[name] = dict(k=k, Eeff=Ed * Es_, r2=r2, coll=sy / k)
    for t in out.values():
        t['fy'] = sy / t['k']
    return out


def basquin(N, sw7, b):
    return sw7 * (N / 1e7) ** b
# ======================================================================

TOPS = ['A', 'B', 'C100', 'C110']

# ---------------------------------------------------------------- R10
print("=== R10 strut volume and mass ===")
Vs = RHO_BAR * VENV
m = RHOS * Vs
check('R10', 'V_s [m^3]', Vs, 2e-4, 1e-12)
check('R10', 'm [kg]', m, 0.534, 1e-9)

# ---------------------------------------------------------------- R11
print("\n=== R11 collapse strength vs rho (MPa) ===")
def coll4(rho, sy):
    B = bcc_summary(rho)
    return (0.3 * rho ** 1.5 * sy, 4 * math.sqrt(2) / 3 * sy * B['P']['d'] ** 3, rho * sy / 3, rho * sy / 6)
for sy in (200e6, 250e6, 280e6):
    print(f"  sigma_y = {sy / MP:.0f} MPa      rho      A        B        C[100]   C[110]")
    for rho in RHO_SWEEP:
        c = coll4(rho, sy)
        print(f"                       {rho:.4f}  " + "  ".join(f"{x / MP:8.3f}" for x in c))
c = coll4(0.2, SY)
for nm, v, e in zip(('A', 'B', 'C[100]', 'C[110]'), c, (6.71, 3.32, 16.67, 8.33)):
    check('R11', f'rho=0.2 collapse {nm} [MPa]', v / MP, e, 0.005)
check('R11', 'A reproduces orchestrator 6.7 MPa', c[0] / MP, 6.7, 0.005)
check('R11', 'C[100] reproduces orchestrator 17 MPa (spec tolerance 0.5 %)', c[2] / MP, 17.0, 0.005)

# ---------------------------------------------------------------- R12
print("\n=== R12 elastic buckling limits (MPa) ===")
def sigE(rho):
    return math.pi ** 2 * ES * (rho / (6 * math.sqrt(2) * math.pi)) / 4
print("  rho      A: 0.05 Es rho^2   C: rho*sigE/3   sigE(strut)   C yield collapse   yield governs (A,C)")
sweep12 = [0.01, 0.02, 0.03, 0.04] + RHO_SWEEP
for rho in sweep12:
    bA = 0.05 * ES * rho ** 2
    bC = rho * sigE(rho) / 3
    cA = 0.3 * rho ** 1.5 * SY
    cC = rho * SY / 3
    print(f"  {rho:.4f}  {bA / MP:12.3f}      {bC / MP:12.3f}  {sigE(rho) / MP:10.1f}    {cC / MP:10.3f}        "
          f"{'A:yield' if cA < bA else 'A:BUCKLE'}, {'C:yield' if cC < bC else 'C:BUCKLE'}")
check('R12', 'A at rho=0.2 [MPa]', 0.05 * ES * 0.04 / MP, 140.0, 0.02)
check('R12', 'sigma_E at rho=0.05 [MPa]', sigE(0.05) / MP, 324.0, 0.02)
rx = SY * 4 * 6 * math.sqrt(2) * math.pi / (math.pi ** 2 * ES)
# numeric bisection (independent of the closed form)
lo, hi = 1e-4, 0.5
for _ in range(100):
    mid = 0.5 * (lo + hi)
    if sigE(mid) < SY:
        lo = mid
    else:
        hi = mid
rxn = 0.5 * (lo + hi)
check('R12', 'C: rho where buckling = yield collapse (bisection) ~0.039', rxn, 0.039, 0.02)
info('R12', f'closed form 24 sqrt2 sigma_y/(pi E) = {rx:.5f}; bisection {rxn:.5f}')
rxA = (6 * SY / ES) ** 2
info('R12', f'A: rho where 0.05 Es rho^2 = 0.3 rho^1.5 sigma_y: (6 sigma_y/Es)^2 = {rxA:.3e}')
ok_main = all(rho * SY / 3 < rho * sigE(rho) / 3 and 0.3 * rho ** 1.5 * SY < 0.05 * ES * rho ** 2 for rho in RHO_SWEEP)
check_true('R12', 'yield governs over the main sweep (rho >= 0.05)', ok_main)
ok_ext = all(rho * SY / 3 < rho * sigE(rho) / 3 for rho in [0.01, 0.02, 0.03, 0.04])
if not ok_ext:
    flag('R12', 'spec says "yield governs over the whole sweep" but with the 0.01-0.05 extension C buckles for rho < 0.0386 (D2 says yield governs only for rho >= 0.05)')

# ---------------------------------------------------------------- R13
print("\n=== R13 k_peak vs rho ===")
print("  rho     A(f=1.5)  A(f=1.698)  B(BCC EB)  C[100]   C[110]  | orch rho^-1.5  orch 1/rho")
for rho in RHO_SWEEP:
    T = topologies(rho)
    print(f"  {rho:.4f}  {T['A']['k']:8.2f}  {(F_CIRC / 0.3) * rho ** -1.5:9.2f}  {T['B']['k']:9.2f}  "
          f"{T['C100']['k']:7.2f}  {T['C110']['k']:7.2f}  | {rho ** -1.5:9.2f}   {1 / rho:7.2f}")
T = topologies(0.2)
for nm, v, e, tol in (('A f=1.5', T['A']['k'], 55.9, 0.005), ('A f=1.698', (F_CIRC / 0.3) * 0.2 ** -1.5, 63.3, 0.005),
                      ('B', T['B']['k'], 132.8, 0.01), ('C[100]', T['C100']['k'], 15.0, 0.005),
                      ('C[110]', T['C110']['k'], 30.0, 0.005), ('orch rho^-1.5', 0.2 ** -1.5, 11.18, 0.005),
                      ('orch 1/rho', 1 / 0.2, 5.0, 0.005)):
    check('R13', f'rho=0.2 k_peak {nm}', v, e, tol)

# ---------------------------------------------------------------- R14
print("\n=== R14 limits on sigma_a vs N ===")
Ns = [10 ** (2 + i / 10) for i in range(0, 81)]   # 1e2..1e10, 10 points/decade


def limits(rho, N, sw7, b, kn, sy=SY):
    T = topologies(rho, sy=sy)
    out = {}
    for t in TOPS:
        fat = basquin(N, sw7, b) / (kn * T[t]['k'])
        fy = sy / T[t]['k']
        co = T[t]['coll']
        lim = min((fat, 'fatigue'), (fy, 'first yield'), (co, 'collapse'))
        out[t] = (fat, fy, co, lim[1], lim[0])
    return out


L = limits(0.2, 1e7, SW7, B_AS, 1.0)
print("  central (rho=0.2, sigma_w7=60, K_n=1, N=1e7, b=-0.1434) [MPa]: fatigue / first yield / collapse / binding")
for t, e in zip(TOPS, (1.07, 0.452, 4.00, 2.00)):
    print(f"    {t:5s} {L[t][0] / MP:8.4f} {L[t][1] / MP:8.4f} {L[t][2] / MP:8.4f}  {L[t][3]}")
    check('R14', f'central fatigue limit {t} [MPa]', L[t][0] / MP, e, 0.01)
    check_true('R14', f'central binding {t} = fatigue', L[t][3] == 'fatigue')
print("  N sweep, central parameters, topology C100 (every 5th point):")
print("    N        fatigue  firstYield collapse binding")
for i in range(0, len(Ns), 5):
    l = limits(0.2, Ns[i], SW7, B_AS, 1.0)['C100']
    print(f"    {Ns[i]:.2e} {l[0] / MP:8.3f} {l[1] / MP:8.3f} {l[2] / MP:8.3f} {l[3]}")

print("  N_x = 1e7 (K_n sigma_y/sigma_w7)^(1/b) over the parameter grid (topology independent):")
outside = []
tot = 0
for b in (-0.07, -0.095, -0.1434, -0.20):
    for sw7 in (40e6, 60e6, 100e6):
        for kn in (1, 1.5, 2, 3, 4):
            Nx = 1e7 * (kn * SY / sw7) ** (1 / b)
            tot += 1
            if not (1e2 <= Nx <= 1e10):
                outside.append((b, sw7 / MP, kn, Nx))
for b in (-0.07, -0.095, -0.1434, -0.20):
    print(f"    b={b}: " + "  ".join(f"sw7={sw7 / MP:.0f}/Kn={kn}:{1e7 * (kn * SY / sw7) ** (1 / b):.3g}"
                                     for sw7 in (60e6,) for kn in (1, 2, 4)))
check('R14', 'N_x (b=-0.1434, sw7=60, Kn=1) ~ 475', 1e7 * (SY / SW7) ** (1 / B_AS), 475, 0.01)
check('R14', "N_x (b=-0.10) ~ 'about 6' (spec tolerance 1 %)", 1e7 * (SY / SW7) ** (1 / -0.10), 6, 0.01)
if outside:
    flag('R14', f'crossover N_x outside the N grid 1e2..1e10 (sweep does not bracket it) for {len(outside)} of {tot} (b, sigma_w7, K_n) combinations; examples: '
         + "; ".join(f"b={b},sw7={s:.0f},Kn={k}->{n:.2g}" for b, s, k, n in outside[:6]))
else:
    info('R14', 'N_x inside the grid for all combinations')

print("  implied sigma_f' = sigma_w7 (2e7)^(-b) [MPa]:")
for b in (-0.07, -0.095, -0.10, -0.1434, -0.20):
    print(f"    b={b}: sigma_w7=40/60/100 -> " + ", ".join(f"{s * (2e7) ** (-b) / MP:.0f}" for s in (40e6, 60e6, 100e6)))
check('R14', "implied sigma_f' b=-0.10 [MPa]", SW7 * 2e7 ** 0.10 / MP, 322, 0.01)
identity('R14', "implied sigma_f' b=-0.1434 = 668 MPa", f"b was derived from sigma_f'=668 so this is circular: {SW7 * 2e7 ** 0.1434 / MP:.1f} MPa")
check('R14', 'sigma_w7(machined) = sigma_f (2e7)^b = 135 MPa (b=-0.095, sigma_f=668)', SIGF * (2e7) ** B_MACH / MP, 135.0, 0.01)
check('R14', 'b(as-built) = ln(60/668)/ln(2e7) = -0.1434', math.log(SW7 / SIGF) / math.log(2e7), -0.1434, 0.001)

print("  binding limit at N=1e7 over rho, sigma_w7, K_n (b=-0.1434):")
for sw7 in (40e6, 60e6, 100e6):
    for kn in (1, 2, 4):
        row = []
        for t in TOPS:
            kinds = {limits(r, 1e7, sw7, B_AS, kn)[t][3] for r in RHO_SWEEP}
            row.append(f"{t}:{'/'.join(sorted(kinds))}")
        print(f"    sw7={sw7 / MP:.0f} Kn={kn}: " + "  ".join(row))
print("  fatigue / collapse ratio vs rho (N=1e7, K_n=1, sigma_w7=60, b=-0.1434):")
print("    rho     A         B         C100      C110")
rat = {}
for rho in RHO_SWEEP:
    l = limits(rho, 1e7, SW7, B_AS, 1.0)
    rat[rho] = [l[t][0] / l[t][2] for t in TOPS]
    print(f"    {rho:.4f}  " + "  ".join(f"{x:.5f}" for x in rat[rho]))
spread = [max(rat[r][i] for r in RHO_SWEEP) / min(rat[r][i] for r in RHO_SWEEP) - 1 for i in range(4)]
for i, t in enumerate(TOPS):
    if t == 'B':
        flag('R14', f'fatigue/collapse ratio for B is NOT independent of rho (varies {100 * spread[i]:.1f} % over the sweep, axial term 1/rho in k_peak); spec says identity')
    else:
        identity('R14', f'fatigue/collapse ratio {t} independent of rho', f'spread {100 * spread[i]:.2e} %')

# ---------------------------------------------------------------- R15
print("\n=== R15 regression of the superseded 20 MPa case (rho=0.2, 1 Hz) ===")
T = topologies(0.2)
for t, e in zip(TOPS, (1118, 2655, 300, 600)):
    pk = T[t]['k'] * 20e6
    print(f"  {t:5s} sigma_peak = {pk / MP:8.1f} MPa; sigma_y=250: {'above' if pk > SY else 'below'}; "
          f"collapse limit {T[t]['coll'] / MP:.2f} MPa vs 20 MPa: {'above' if 20e6 > T[t]['coll'] else 'below'}")
    check('R15', f'peak {t} [MPa]', pk / MP, e, 0.01)
check_true('R15', 'all four peaks above sigma_y', all(T[t]['k'] * 20e6 > SY for t in TOPS))
check('R15', 'orchestrator 224 MPa = rho^-1.5 x 20', 0.2 ** -1.5 * 20, 224, 0.01)
check('R15', 'orchestrator 100 MPa = 1/rho x 20', 20 / 0.2, 100, 0.01)
dS = PSI * VENV * (20e6) ** 2 / (2 * ES * 0.2 ** 2 * T0)
check('R15', 'Sdot [W/K] at 1 Hz, E_s rho^2', dS * 1.0, 1.19e-3, 0.01)
check('R15', 'entropy per year [J/K]', dS * 1.0 * YEAR, 3.76e4, 0.01)
info('R15', f'per cycle dS = {dS:.4e} J/K')

summary()
