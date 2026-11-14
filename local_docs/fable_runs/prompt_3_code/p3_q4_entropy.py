"""p3_q4_entropy.py -- Prompt 3, S2 implementer.

Purpose : dissipated entropy of the four topologies at the fatigue-limited amplitude:
          per-cycle entropy and rate, strut-form rate, life entropy bound, service-capped
          entropy maximum, comparator entropies, local entropy density.
          Level: derived (unverified; FROM MEMORY inputs used as given).
Spec rows: R16 (Delta S, Sdot matrix), R17 (strut-form Sdot), R18 (life bound, tau_wearout),
          R19 (S vs sigma_a with service cap), R20 (comparators), R21 (local entropy density).
Source  : local_docs/fable_runs/prompt_3_plan.md section 3.2, derivations D1, D6-D9.
Assumptions: rho=0.2, V=1e-3 m^3, psi=5e-3 (amplitude independent), T0=300 K, sigma_y=250,
          sigma_w7=60 MPa, K_n=1 (R16-R20 unless stated), self-consistent E_eff per topology:
          A E_s rho^2, B E* from R6 (Euler-Bernoulli), C [100] rho E_s/9 (R1).
          Pure Python (system python3, no numpy).
Run     : python3 p3_q4_entropy.py
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

RHO = 0.2
T = topologies(RHO)
NAMES3 = ['A', 'B', 'C100']
CENT = {t: SW7 / (KN * T[t]['k']) for t in T}   # fatigue-limited sigma_a at N=1e7, b irrelevant


def dS_cycle(sa, Eeff):
    return PSI * VENV * sa ** 2 / (2 * Eeff * T0)


# ---------------------------------------------------------------- R16
print("=== R16 Delta S per cycle [J/K] and Sdot [W/K] ===")
sa_cols = [('A central', CENT['A']), ('B central', CENT['B']), ('C100 central', CENT['C100']),
           ('1 MPa', 1e6), ('2 MPa', 2e6)]
Ecols = [('E_s rho^2 (A)', T['A']['Eeff']), ('E* (B, R6)', T['B']['Eeff']), ('rho Es/9 (C100)', T['C100']['Eeff'])]
print(f"  E_eff [GPa]: " + ", ".join(f"{n}={e / 1e9:.4f}" for n, e in Ecols))
print("  sigma_a column vs E_eff column: per cycle dS [J/K]; Sdot at 1 Hz; Sdot at 1/86400 Hz")
selfcons = {}
for i, (sn, sa) in enumerate(sa_cols):
    for j, (en, E) in enumerate(Ecols):
        ds = dS_cycle(sa, E)
        if i < 3 and i == j:
            tag = 'self-consistent'
            selfcons[NAMES3[i]] = ds
        elif i < 3:
            tag = 'inconsistent pair'
        else:
            tag = 'fixed amplitude (not a topology pair)'
        print(f"    {sn:13s} sa={sa / MP:7.4f} MPa | {en:16s} | dS={ds:.4e}  Sdot(1Hz)={ds * 1.0:.4e}  Sdot(1/day)={ds / DAY:.4e}  [{tag}]")
        if tag == 'inconsistent pair':
            RES.append(('R16', 'FLAG', f'inconsistent pair {sn} x {en}'))
check('R16', 'A self-consistent dS per cycle', selfcons['A'], 3.43e-6, 0.01)
check('R16', 'B self-consistent dS per cycle', selfcons['B'], 6.7e-6, 0.05)
check('R16', 'C100 self-consistent dS per cycle', selfcons['C100'], 8.57e-5, 0.01)
check('R16', '1 MPa with E_s rho^2', dS_cycle(1e6, Ecols[0][1]), 2.98e-6, 0.01)
check('R16', '1 MPa with rho Es/9', dS_cycle(1e6, Ecols[2][1]), 5.36e-6, 0.01)
check('R16', 'ratio 1 MPa (rho Es/9)/(E_s rho^2) = 9 rho = 1.8', dS_cycle(1e6, Ecols[2][1]) / dS_cycle(1e6, Ecols[0][1]), 1.8, 0.01)
info('R16', 'off-diagonal cells are printed with the tag "inconsistent pair" and counted as FLAG lines in the summary (labels, not problems)')
# the 1.8 ratio is 9*rho by construction of the two moduli; keep as a check of E_eff values only
info('R16', 'D7 Sdot at 1/day: A 3.97e-11, B 7.8e-11, C 9.92e-10 W/K: ' +
     ", ".join(f"{t}={selfcons[t] / DAY:.3e}" for t in NAMES3))

# ---------------------------------------------------------------- R17
print("\n=== R17 strut-form Sdot = nu psi rho V sigma_rms^2/(2 Es T0) ===")
for nu, nus in ((1.0, '1 Hz'), (1 / DAY, '1/day')):
    # C100: sigma_rms from R2 strut stresses
    st = octet_struts(RHO, (1, 0, 0))
    srms = CENT['C100'] * math.sqrt(sum(s * s for s in st) / 6)
    sd = nu * PSI * RHO * VENV * srms ** 2 / (2 * ES * T0)
    check('R17', f'C100 {nus}: strut-form vs R16 (1e-6)', sd, nu * selfcons['C100'], 1e-6)
    # B: sigma_rms from R9 quadrature energy
    bs = bcc_summary(RHO)
    srmsB = CENT['B'] * bs['k'] / bs['r']
    sdB = nu * PSI * RHO * VENV * srmsB ** 2 / (2 * ES * T0)
    check('R17', f'B {nus}: strut-form (R9) vs R16 (1e-4)', sdB, nu * selfcons['B'], 1e-4)
    # A: sigma_rms defined by identity
    srmsA = CENT['A'] * T['A']['k'] / math.sqrt(T['A']['r2'])
    sdA = nu * PSI * RHO * VENV * srmsA ** 2 / (2 * ES * T0)
    identity('R17', f'A {nus}: sigma_rms from r^2=25 (r defined by the identity); strut-form={sdA:.4e} vs R16={nu * selfcons["A"]:.4e}')
info('R17', f"A: k_peak*sqrt(rho*E_eff/E_s) = {T['A']['k'] * math.sqrt(RHO * T['A']['Eeff'] / ES):.6f} (= f/0.3 = 5, r^2=25)")

# ---------------------------------------------------------------- R18
print("\n=== R18 life entropy bound S(N) = N psi rho V sigma_w(N)^2/(2 Es T0 Kn^2 r^2) ===")
bs = bcc_summary(RHO)
st111 = octet_struts(RHO, (1, 1, 1))
r2_111 = max(abs(s) for s in st111) ** 2 / (sum(s * s for s in st111) / 6)
R2S = [('C100', T['C100']['r2']), ('C111', r2_111), ('C110', T['C110']['r2']), ('B', bs['r2']), ('A', 25.0)]
print("  r^2: " + ", ".join(f"{n}={v:.4f}" for n, v in R2S))


def Slife(N, b, r2, kn=1.0):
    return N * PSI * RHO * VENV * basquin(N, SW7, b) ** 2 / (2 * ES * T0 * kn ** 2 * r2)


for b in (B_MACH, B_AS):
    print(f"  b={b}: S(N) [J/K]   N        " + "  ".join(f"{n:>10s}" for n, _ in R2S))
    for N in (1e2, 1e4, 1e6, 1e7, 1e8, 1e10):
        print(f"                       {N:.0e}  " + "  ".join(f"{Slife(N, b, r2):10.4g}" for _, r2 in R2S))
for (n, r2), e, tol in zip(R2S, (857, 476, 143, 67, 34), (0.01, 0.01, 0.01, 0.05, 0.01)):
    check('R18', f'S(1e7) {n} [J/K]', Slife(1e7, B_AS, r2), e, tol)
for nu, nus, e in ((1.0, '1 Hz', 0.317), (1 / DAY, '1/day', 27379)):
    check('R18', f'tau_wearout at 1e7 cycles, {nus} [years]', 1e7 / nu / YEAR, e, 0.01)
print("  tau_wearout N/nu [years]: N=1e2..1e10")
for N in (1e2, 1e4, 1e6, 1e7, 1e8, 1e10):
    print(f"    N={N:.0e}: 1 Hz {N / YEAR:.4g} y; 1/day {N * DAY / YEAR:.4g} y")
# equality with R16 for the self-consistent pairs, over N and b
selfmap = {'A': 'A', 'B': 'B', 'C100': 'C100', 'C110': 'C110'}
r2map = dict(R2S)
for b in (B_MACH, B_AS):
    for N in (1e3, 1e7, 1e9):
        for t in ('A', 'B', 'C100', 'C110'):
            sa = basquin(N, SW7, b) / (KN * T[t]['k'])
            s16 = N * dS_cycle(sa, T[t]['Eeff'])
            tol = 0.05 if t == 'B' else 0.01
            check('R18', f'b={b} N={N:.0e} {t}: R18 vs R16 dS x N', Slife(N, b, T[t]['r2']), s16, tol)
identity('R18', 'S(N)/S(1e7) = (N/1e7)^(1+2b)', 'algebraic consequence of the formula, not a check')

# ---------------------------------------------------------------- R19
print("\n=== R19 S(sigma_a) with service cap tau_s; maximum location and value ===")
GRID = logspace(0.05e6, 30e6, 3000)
exp19 = {('C100', 1.0, B_AS, 20): (2.21, 1.65e4), ('C100', 1.0, B_MACH, 20): (None, 2.46e4),
         ('C100', 1 / DAY, B_AS, 20): (11.3, 5.0), ('C100', 1 / DAY, B_MACH, 20): (None, 2.5)}
SMAX = {}
print("  topology nu    b       tau[y]  sigma_a*(grid)  sigma_a*(analytic)  Smax(grid)   Smax(analytic)  interior?")
for t in NAMES3:
    Tt = T[t]
    fy = Tt['fy']
    for nu in (1.0, 1 / DAY):
        for b in (B_MACH, B_AS):
            for tau in (10, 20, 30):
                Ncap = nu * tau * YEAR
                best = (-1, None, None)
                nel = 0
                imax = -1
                for i, sa in enumerate(GRID):
                    if sa > fy:
                        nel += 1
                        continue
                    Nf = 1e7 * (KN * Tt['k'] * sa / SW7) ** (1 / b)
                    S = dS_cycle(sa, Tt['Eeff']) * min(Nf, Ncap)
                    if S > best[0]:
                        best = (S, sa, i)
                nvalid = len(GRID) - nel
                sstar = SW7 * (Ncap / 1e7) ** b / (KN * Tt['k'])
                suse = min(sstar, fy)
                Nf_use = 1e7 * (KN * Tt['k'] * suse / SW7) ** (1 / b)
                Sana = dS_cycle(suse, Tt['Eeff']) * min(Nf_use, Ncap)
                interior = 0 < best[2] < nvalid - 1
                SMAX[(t, nu, b, tau)] = (best[0], best[1], Sana, sstar)
                print(f"  {t:5s}    {nu:.2e} {b:7.4f} {tau:3d}    {best[1] / MP:9.4f}       {sstar / MP:9.4f}         "
                      f"{best[0]:.4e}   {Sana:.4e}   {'interior' if interior else 'EDGE'}")
                if not interior:
                    flag('R19', f'maximum on a grid edge for {t} nu={nu:.2e} b={b} tau={tau}: sigma_a*={best[1] / MP:.3f} MPa (first yield {fy / MP:.3f})')
                elif sstar > fy:
                    flag('R19', f'analytic sigma_a*={sstar / MP:.3f} MPa exceeds first yield for {t} nu={nu:.2e} b={b} tau={tau}; maximum is capped by first yield')
                check('R19', f'{t} nu={nu:.2e} b={b} tau={tau}: grid max vs analytic', best[0], Sana, 0.03)
                if sstar < GRID[0] or sstar > GRID[-1]:
                    flag('R19', f'analytic sigma_a* outside the grid for {t} nu={nu:.2e} b={b} tau={tau}')
for key, (sae, Se) in exp19.items():
    t, nu, b, tau = key
    S, sa, Sana, sstar = SMAX[key]
    if sae is not None:
        check('R19', f'{t} nu={nu:.2e} b={b} tau={tau}: sigma_a* [MPa]', sa / MP, sae, 0.03)
    check('R19', f'{t} nu={nu:.2e} b={b} tau={tau}: S max [J/K]', S, Se, 0.03)
for nu in (1.0, 1 / DAY):
    for b in (B_MACH, B_AS):
        for tau in (10, 20, 30):
            c = SMAX[('C100', nu, b, tau)][0]
            a = SMAX[('A', nu, b, tau)][0]
            check('R19', f'A = C100/25 nu={nu:.2e} b={b} tau={tau}', a, c / 25, 0.03)
for nu in (1.0, 1 / DAY):
    bb = SMAX[('B', nu, B_AS, 20)][0]
    cc = SMAX[('C100', nu, B_AS, 20)][0]
    info('R19', f'C100/B at nu={nu:.2e}, b=-0.1434, 20 y: {cc / bb:.3f} (r^2_B = {bs["r2"]:.3f})')

# ---------------------------------------------------------------- R20
print("\n=== R20 comparators (m = 0.534 kg) ===")
mass = RHOS * RHO * VENV
melt = mass * (CP * (TLIQ - T0) + HF) / T0
lp_lo, lp_hi = mass * 50e6 / T0, mass * 500e6 / T0
prim = mass * 200e6 / T0
print(f"  melt floor = {melt:.4e} J/K; LPBF 50 MJ/kg = {lp_lo:.4e}, 500 MJ/kg = {lp_hi:.4e}; primary 200 MJ/kg = {prim:.4e}")
check('R20', 'melt floor ~1.6e3 J/K (spec tolerance 1 %)', melt, 1.6e3, 0.01)
check('R20', 'LPBF low ~0.9e5 J/K (spec tolerance 1 %)', lp_lo, 0.9e5, 0.01)
check('R20', 'LPBF high ~9e5 J/K (spec tolerance 1 %)', lp_hi, 9e5, 0.01)
check('R20', 'primary ~3.6e5 J/K (spec tolerance 1 %)', prim, 3.6e5, 0.01)
print("  ratio of each R19 maximum to comparators: melt, LPBF50, LPBF500, primary, 1e3, 1e5")
for key in sorted(SMAX, key=lambda k: (k[0], k[1], -k[2], k[3])):
    S = SMAX[key][0]
    print(f"    {key[0]:5s} nu={key[1]:.2e} b={key[2]:7.4f} tau={key[3]:2d}  S={S:.3e}  " +
          "  ".join(f"{S / c:.3e}" for c in (melt, lp_lo, lp_hi, prim, 1e3, 1e5)))
Smax_all = max(v[0] for v in SMAX.values())
info('R20', f'largest R19 maximum over all cases = {Smax_all:.3e} J/K; below melt floor? {Smax_all < melt}; below 1e5? {Smax_all < 1e5}')

# ---------------------------------------------------------------- R21
print("\n=== R21 local entropy density s(N) = N psi sigma_w(N)^2/(2 Es T0 Kn^2) [MJ/(m^3 K)] ===")
print("  N        b=-0.095   b=-0.1434   ratio to 4 MJ/(m3 K) (b=-0.095, -0.1434)")
for N in (1e2, 1e4, 1e6, 1e7, 1e8, 1e10):
    ss = [N * PSI * basquin(N, SW7, b) ** 2 / (2 * ES * T0) / 1e6 for b in (B_MACH, B_AS)]
    print(f"  {N:.0e}  {ss[0]:9.4g}  {ss[1]:9.4g}    {ss[0] / 4:.4g}, {ss[1] / 4:.4g}")
s7 = 1e7 * PSI * SW7 ** 2 / (2 * ES * T0) / 1e6
check('R21', 's(1e7) [MJ/(m^3 K)]', s7, 4.29, 0.01)
info('R21', f'ratio to 4 MJ/(m^3 K) at 1e7 = {s7 / 4:.3f} (interpretive, no pass/fail)')

summary()
