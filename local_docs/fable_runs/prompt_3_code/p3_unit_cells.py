"""p3_unit_cells.py -- Prompt 3, S2 implementer.

Purpose : unit-cell mechanics of the octet (pin-jointed affine model) and the BCC
          slender-strut model.  Level: derived (unverified; inputs FROM MEMORY used as given).
Spec rows: R1 (octet constants), R2 (octet strut stresses), R3 (octet energy), R4 (octet
          mismatch), R5 (beam integrals), R6 (BCC single strut), R7 (BCC biaxial),
          R8 (BCC collapse / first yield), R9 (BCC energy identity and r).
Source  : local_docs/fable_runs/prompt_3_plan.md section 3.2, derivations D2-D5.
Assumptions: round struts, rho_bar = sqrt(3)*pi*(d/L)^2, L = 1, E_s = 1 (normalised) for
          R1-R7; node overlap ignored; BCC axial force kept (k_a*(Delta.n)*n) even though
          the axial strain tends to zero.  Pure Python (system python3 has no numpy).
Run     : python3 p3_unit_cells.py
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

# ---------------------------------------------------------------- R1
print("=== R1 octet elastic constants (normalised, rho=1, Es=1) ===")
for rho in (1.0,):
    Cv = octet_C(rho, 1.0)
    Sv = matinv(Cv)
    E = {}
    for lab, d in (('100', (1, 0, 0)), ('110', (1, 1, 0)), ('111', (1, 1, 1))):
        eps, _, dd = octet_strain_for_stress(rho, d)
        E[lab] = 1.0 / quad(dd, eps)
        # transverse direction orthogonal to d
        t = {'100': (0, 1, 0), 'ach': None}.get(lab)
        if lab == '100':
            nu = -quad((0, 1, 0), eps) / quad(dd, eps)
        elif lab == '110':
            nu_t = -quad((0, 0, 1), eps) / quad(dd, eps)
            info('R1', f"nu for load [110], transverse [001] = {nu_t:.9f}")
        else:
            tt = [1 / math.sqrt(2), -1 / math.sqrt(2), 0]
            info('R1', f"nu for load [111], transverse [1-10] = {-quad(tt, eps) / quad(dd, eps):.9f}")
    G = 1.0 / Sv[3][3]
    K = 1.0 / (3 * (Sv[0][0] + Sv[0][1] + Sv[0][2]))
    check('R1', 'E_100/(rho Es)', E['100'], 1 / 9, 1e-9)
    check('R1', 'E_110/(rho Es)', E['110'], 1 / 6, 1e-9)
    check('R1', 'E_111/(rho Es)', E['111'], 1 / 5, 1e-9)
    check('R1', 'nu ([100], transverse [010])', nu, 1 / 3, 1e-9)
    check('R1', 'G/(rho Es)', G, 1 / 12, 1e-9)
    check('R1', 'bulk/(rho Es)', K, 1 / 9, 1e-9)
    info('R1', f"S11={Sv[0][0]:.9f} S12={Sv[0][1]:.9f} S44={Sv[3][3]:.9f}  (D2: 9, -3, 12)")

# ---------------------------------------------------------------- R2
print("\n=== R2 octet strut stress / sigma_a (report x rho_bar; rho=1 and 0.2) ===")
exp_sorted = {'100': [-3, -3, -3, 3, 3, 3], '111': [-1, -1, -1, 3, 3, 3], '110': [0, 0, 0, 0, 0, 6]}
exp_r2 = {'100': 1.0, '111': 1.8, '110': 6.0}
for rho in (1.0, 0.2):
    for lab, d in (('100', (1, 0, 0)), ('110', (1, 1, 0)), ('111', (1, 1, 1))):
        st = [s * rho for s in octet_struts(rho, d)]
        peak = max(abs(s) for s in st)
        rms = math.sqrt(sum(s * s for s in st) / 6)
        print(f"  rho={rho} [{lab}] strut stress x rho/sigma_a = {[round(s, 9) for s in st]} "
              f"peak={peak:.9f} rms={rms:.9f} r2={peak**2 / rms**2:.9f}")
        if lab == '100':
            ok = all(abs(abs(s) - 3) < 1e-9 for s in st)
            check_true('R2', f'[100] rho={rho} all |s|=3', ok)
        else:
            srt = sorted(st)
            ok = max(abs(a - b) for a, b in zip(srt, sorted(exp_sorted[lab]))) < 1e-9
            check_true('R2', f'[{lab}] rho={rho} sorted values', ok, str([round(s, 6) for s in srt]))
        check('R2', f'[{lab}] rho={rho} r2', peak ** 2 / rms ** 2, exp_r2[lab], 1e-9)

# ---------------------------------------------------------------- R3
print("\n=== R3 octet energy: sigma_a^2/(2 E_d) vs rho*mean(s_k^2)/(2 Es) ===")
for rho in (1.0, 0.2):
    for lab, d in (('100', (1, 0, 0)), ('110', (1, 1, 0)), ('111', (1, 1, 1))):
        eps, _, dd = octet_strain_for_stress(rho, d)
        Ed = 1.0 / quad(dd, eps)
        Um = 1.0 / (2 * Ed)
        st = octet_struts(rho, d)
        Us = rho * (sum(s * s for s in st) / 6) / 2
        check('R3', f'rho={rho} [{lab}] U_macro vs U_strut', Um, Us, 1e-9)
info('R3', 'two routes (C inversion vs strut stresses) test Clapeyron + implementation, not the pin-jointed assumption')

# ---------------------------------------------------------------- R4
print("\n=== R4 octet under mismatch strain (eps_m = 1, rho = 1, Es = 1) ===")
C = octet_C(1.0, 1.0)
# (a) equibiaxial eps_x=eps_y=1, sigma_zz = 0 : C31*ex + C32*ey + C33*ez = 0
ez = -(C[2][0] + C[2][1]) / C[2][2]
epsa = [[1, 0, 0], [0, 1, 0], [0, 0, ez]]
sa = [quad(n, epsa) for n in _OCT]
sxx = C[0][0] * 1 + C[0][1] * 1 + C[0][2] * ez
check('R4', 'eps_zz/eps_m', ez, -1.0, 1e-9)
check_true('R4', 'in-plane struts at Es*eps_m, others 0',
           all(abs(sa[i] - 1) < 1e-9 for i in (0, 1)) and all(abs(sa[i]) < 1e-9 for i in (2, 3, 4, 5)),
           str([round(s, 9) for s in sa]))
check('R4', 'sigma_xx/(rho Es eps_m)', sxx, 1 / 6, 1e-9)
check_true('R4', 'max strut strain <= eps_m', max(abs(s) for s in sa) <= 1 + 1e-12)
epsb = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
sb = [quad(n, epsb) for n in _OCT]
sh = C[0][0] + C[0][1] + C[0][2]
check_true('R4', 'all struts at Es*eps_m', all(abs(s - 1) < 1e-9 for s in sb), str(sb))
check('R4', 'hydrostatic sigma/(rho Es eps_m)', sh, 1 / 3, 1e-9)
check_true('R4', 'max strut strain <= eps_m', max(abs(s) for s in sb) <= 1 + 1e-12)

# ---------------------------------------------------------------- R5
print("\n=== R5 beam integrals (midpoint quadrature) ===")
NQ = 4000


def beam_moments(n, section, nq=NQ):
    """<|M y|^n>/(Mmax ymax)^n over length (x in [0,1], M=|1-2x|) and section."""
    s_len = sum(abs(1 - 2 * (i + 0.5) / nq) ** n for i in range(nq)) / nq
    if section == 'rect':
        s_sec = sum(abs(-1 + 2 * (j + 0.5) / nq) ** n for j in range(nq)) / nq
    else:  # circle, radius 1, area weight = chord width
        num = den = 0.0
        for j in range(nq):
            y = -1 + 2 * (j + 0.5) / nq
            w = 2 * math.sqrt(max(1 - y * y, 0.0))
            num += abs(y) ** n * w
            den += w
        s_sec = num / den
    return s_len * s_sec


def kappa(n, section):
    return beam_moments(n, section) / beam_moments(2, section) ** (n / 2)


for sec, e in (('rect', 1 / 9), ('circ', 1 / 12)):
    check('R5', f'<sigma^2>/sigma_peak^2 {sec}', beam_moments(2, sec), e, 1e-3)
for sec, tbl in (('rect', {2: 1.0, 3: 1.69, 4: 3.24}), ('circ', {2: 1.0, 3: 1.76, 4: 3.60})):
    for n in (2, 2.3, 2.5, 3, 4):
        kv = kappa(n, sec)
        if n == 2:
            identity('R5', f'kappa(2)=1 {sec}', f'value {kv:.6f}')
        elif n in tbl:
            check('R5', f'kappa({n}) {sec} vs spec value (quoted to 3 s.f.)', kv, tbl[n], 1e-3)
        else:
            info('R5', f'kappa({n}) {sec} = {kv:.5f}')

# ---------------------------------------------------------------- R6
RHOS6 = [0.02, 0.05, 0.10, 1 / 9, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]
print("\n=== R6 BCC single strut, uniaxial (L=1, Es=1, nu_s=0.33) ===")
print("  rho    | EB: C1      nu     Csig_b  Csig_ax  Cb_b   k_peak | Timo: C1      nu     k_peak  dC1%")
for rho in RHOS6:
    ux = {}
    for timo in (False, True):
        P = bcc_props(rho, timo=timo)
        u = bcc_uniaxial(P)
        ux[timo] = (P, u)
    P, u = ux[False]
    C1 = u['Estar'] / rho ** 2
    Cs_b = u['bend'] * rho ** 1.5 / u['sbar']
    Cs_a = (u['bend'] + u['ax']) * rho ** 1.5 / u['sbar']
    Cb_b = u['bend'] / (1.0 * u['ez'] * rho ** 0.5)
    kpk = (u['bend'] + u['ax']) / u['sbar']
    Pt, ut = ux[True]
    C1t = ut['Estar'] / rho ** 2
    kt_ = (ut['bend'] + ut['ax']) / ut['sbar']
    print(f"  {rho:.4f} |    {C1:.5f}  {u['nu']:.4f}  {Cs_b:.3f}  {Cs_a:.3f}  {Cb_b:.4f}  {kpk:.2f} |"
          f"    {C1t:.5f}  {ut['nu']:.4f}  {kt_:.2f}  {100 * (C1t / C1 - 1):+.1f}")
    if abs(rho - 0.02) < 1e-12:
        check('R6', 'rho=0.02 C1 vs closed form sqrt3/(6 pi)', C1, S3 / (6 * math.pi), 0.01)
        check('R6', 'rho=0.02 C1 vs 0.0919', C1, 0.0919, 0.01)
        check_true('R6', 'rho=0.02 C1 low by <0.5% vs closed form', 0 <= 1 - C1 / (S3 / (6 * math.pi)) <= 0.005,
                   f'low by {100 * (1 - C1 / (S3 / (6 * math.pi))):.3f} %')
        check('R6', 'rho=0.02 C_sigma bending', Cs_b, 11.43, 0.01)
        check('R6', 'rho=0.02 C_b bending', Cb_b, 1.050, 0.01)
        check('R6', 'rho=0.02 Poisson ratio -> 0.5', u['nu'], 0.5, 0.01)
    if abs(rho - 0.20) < 1e-12:
        check('R6', 'rho=0.2 C1 ~ 0.0902', C1, 0.0902, 0.01)
        check('R6', 'rho=0.2 k_peak ~ 132.8', kpk, 132.8, 0.01)
# bending-only (inextensible) limit via large k_a: demonstrates the 1.5 trap
print("  -- axial-force trap check at rho=0.02: inextensible limit (k_a x 1e8) and 'axial force dropped'")
P = bcc_props(0.02, kafac=1e8)
u = bcc_uniaxial(P)
info('R6', f"k_a x1e8: C1={u['Estar'] / 0.02 ** 2:.5f} (closed form 0.091888); axial strain a={u['a']:.3e}; "
           f"axial stress N/A over sbar={u['ax'] / u['sbar'] * 0.02:.5f} (expect 1.0 = sigma/rho)")
# trap variant: impose a = Delta.n = 0 exactly (eps_z = -2 eps_x) and use only the transverse force k_t*Delta_t
P0 = bcc_props(0.02)
Dz = 0.5 * 1.0 * 1.0                 # Delta_z for eps_z = 1
Dx = 0.5 * (-0.5)                    # Delta_x = Delta_y for eps_x = -0.5
Dvec = [Dx, Dx, Dz]
Fdrop_z = P0['kt'] * Dvec[2]         # transverse force only, no axial force k_a*a
Edrop = 4 * Fdrop_z
info('R6', f"axial force dropped (F=k_t*Delta only): C1={Edrop / 0.02 ** 2:.5f}; correct/dropped = {u['Estar'] / Edrop:.4f} "
           f"(planner: dropping gives modulus low by 1.5)")
check('R6', 'trap ratio correct/dropped = 1.5', u['Estar'] / Edrop, 1.5, 0.01)

# ---------------------------------------------------------------- R7
print("\n=== R7 BCC equibiaxial (eps_x=eps_y=eps_m=1, sigma_zz=0) ===")
print("  rho    | ez/em   peak/(Es em) [EB]  formula   M/(Es rho^2)  E*/(1-nu)/(Es rho^2) | Timo: peak  M/(Es rho^2)")
f_closed = lambda r: 2.100 * r ** 0.5 + 0.368 * r
for rho in RHOS6:
    P = bcc_props(rho)
    bb = bcc_biaxial(P)
    u = bcc_uniaxial(P)
    E1nu = u['Estar'] / (1 - u['nu'])
    Pt = bcc_props(rho, timo=True)
    bt = bcc_biaxial(Pt)
    print(f"  {rho:.4f} | {bb['ez']:.4f}  {bb['peak']:.5f}           {f_closed(rho):.5f}  {bb['M'] / rho ** 2:.5f}      "
          f"{E1nu / rho ** 2:.5f}               | {bt['peak']:.5f}  {bt['M'] / rho ** 2:.5f}")
    check('R7', f'rho={rho:.4f} biaxial modulus = E*/(1-nu) (two routes)', bb['M'], E1nu, 1e-6)
    if abs(rho - 0.02) < 1e-12:
        check('R7', 'rho=0.02 ez/em -> -2', bb['ez'], -2.0, 0.02)
        check('R7', 'rho=0.02 peak vs 2.100 r^.5+0.368 r', bb['peak'], f_closed(rho), 0.02)
        check('R7', 'rho=0.02 biaxial modulus vs 0.1838 rho^2', bb['M'] / rho ** 2, 0.1838, 0.02)


def cross(r):
    return bcc_biaxial(bcc_props(r))['peak'] - 1.0


lo, hi = 0.02, 0.6
flo, fhi = cross(lo), cross(hi)
print(f"  bisection bracket: f(0.02)={flo:.4f}  f(0.6)={fhi:.4f}")
if flo * fhi < 0:
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if cross(mid) * flo > 0:
            lo = mid
        else:
            hi = mid
    rx = 0.5 * (lo + hi)
    info('R7', f"crossover rho (sigma_peak = Es eps_m), EB model: {rx:.4f} (reported, not pass/fail; spec expects 0.19-0.23)")
    if not (0.19 <= rx <= 0.23):
        flag('R7', f'crossover rho {rx:.4f} outside spec range 0.19-0.23')
    else:
        info('R7', 'crossover inside the spec range 0.19-0.23')
    # Timoshenko
    lo, hi = 0.02, 0.6
    ct = lambda r: bcc_biaxial(bcc_props(r, timo=True))['peak'] - 1.0
    flo = ct(lo)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if ct(mid) * flo > 0:
            lo = mid
        else:
            hi = mid
    info('R7', f"crossover rho, Timoshenko: {0.5 * (lo + hi):.4f}")
else:
    flag('R7', 'bisection bracket 0.02-0.6 does not bracket the crossover')
print("  hydrostatic strain:")
for rho in (0.02, 0.2, 0.4):
    h = bcc_hydro(bcc_props(rho))
    check('R7', f'hydrostatic rho={rho} strut stress = Es eps_m', h['ax'], 1.0, 1e-9)
    check_true('R7', f'hydrostatic rho={rho} zero bending', h['bend'] < 1e-9, f"bend={h['bend']:.2e}")

# ---------------------------------------------------------------- R8
print("\n=== R8 BCC collapse and first yield (sigma_y = 250 MPa) ===")
print("  rho    d/L     collapse[MPa]  first yield[MPa] (EB, with axial)  collapse/bend-only-yield")
for rho in RHOS6:
    P = bcc_props(rho)
    u = bcc_uniaxial(P)
    dL = P['d']
    coll = 4 * math.sqrt(2) / 3 * SY * dL ** 3
    fy = SY / ((u['bend'] + u['ax']) / u['sbar'])
    fyb = SY / (u['bend'] / u['sbar'])
    print(f"  {rho:.4f} {dL:.4f}  {coll / MP:9.4f}      {fy / MP:9.4f}                    {coll / fyb:.5f}")
    if abs(rho - 0.2) < 1e-12:
        check('R8', 'rho=0.2 collapse 3.32 MPa', coll / MP, 3.32, 0.01)
        check('R8', 'rho=0.2 first yield 1.88 MPa', fy / MP, 1.88, 0.01)
    if abs(rho - 0.02) < 1e-12:
        check('R8', 'rho=0.02 numeric ratio collapse/bending-only yield vs 16/(3 pi) (stiffness route vs closed form)',
              coll / fyb, 16 / (3 * math.pi), 0.01)
identity('R8', 'collapse / bending-only first yield = 16/(3 pi)',
         f"closed-form algebra (4 sqrt2/3)*(2 sqrt2/pi) = {4 * math.sqrt(2) / 3 * 2 * math.sqrt(2) / math.pi:.6f} vs 16/(3pi) = {16 / (3 * math.pi):.6f} (algebra, not physics)")

# ---------------------------------------------------------------- R9
print("\n=== R9 BCC energy identity and r (EB) ===")
print("  rho    U_macro=sbar^2/(2E*)  U_strut(quadrature)   rel diff     r(bend only)  r(with axial)")
for rho in RHOS6:
    P = bcc_props(rho)
    u = bcc_uniaxial(P)
    Um = u['sbar'] ** 2 / (2 * u['Estar'])
    Us = bcc_energy(P, u['F'])
    srms = math.sqrt(2 * Us / rho)
    rb = u['bend'] / srms
    ra = (u['bend'] + u['ax']) / srms
    print(f"  {rho:.4f} {Um:.6e}        {Us:.6e}       {abs(Um - Us) / Um:.2e}     {rb:.5f}       {ra:.5f}")
    check('R9', f'rho={rho:.4f} energy two routes', Us, Um, 1e-6)
    if abs(rho - 0.02) < 1e-12:
        check('R9', 'rho=0.02 r (bending only) -> 2 sqrt3', rb, 2 * S3, 0.01)
    if abs(rho - 0.2) < 1e-12:
        check('R9', 'rho=0.2 r with axial ~ 3.57', ra, 3.57, 0.01)
        info('R9', f'rho=0.2 r^2 with axial = {ra ** 2:.3f} (D3: about 12.7)')

summary()
