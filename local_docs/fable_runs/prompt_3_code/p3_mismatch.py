"""p3_mismatch.py -- Prompt 3, S2 implementer.

Purpose : thermal-mismatch fatigue of a lattice layer bonded to a stiff partner:
          local amplitude, stiffness ratio S, life and critical temperature swing,
          dissipation under strain control, interlayer shear and thermal-lag magnitudes.
          Level: derived (unverified; FROM MEMORY inputs used as given).
Spec rows: R28 (mismatch strain, local amplitude), R29 (stiffness ratio S), R30 (life and
          Delta T at N=10958), R31 (dissipation under strain control), R32 (shear, lag).
Source  : local_docs/fable_runs/prompt_3_plan.md section 3.2, derivations D4, D10.
Assumptions: equibiaxial layer strain; M_L: octet rho E_s/6, BCC biaxial modulus from the
          R7 strut model (Euler-Bernoulli, axial force kept), A E_s rho^2/(1-0.3);
          c_BCC = sigma_peak/(E_s eps_m) from R7; S enters via 1/(1+S) (and is also shown
          at S = 0, because the spec's quoted expected values appear to omit it);
          R30 Goodman mean stress sigma_m = min(sigma_y, E_s*dalpha*dT_ref) applied to
          the local amplitude (no K_n, no c on the mean) -- UNSURE reading of the spec.
          Pure Python (system python3, no numpy).
Run     : python3 p3_mismatch.py
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

NCYC = 10958   # 30 years of daily cycles (spec value)
CNU = 1 / (1 - NUS)


def M_L(lat, rho):
    if lat == 'octet':
        return rho * ES / 6
    if lat == 'A':
        return ES * rho ** 2 / (1 - 0.3)
    if lat == 'BCC':
        return bcc_biaxial(bcc_props(rho))['M'] * ES
    raise ValueError(lat)


def c_bcc(rho):
    return bcc_biaxial(bcc_props(rho))['peak']


def M2(pn):
    a, E, nu = PARTNERS[pn]
    return E / (1 - nu)


def Sratio(lat, rho, pn, hr=1.0):
    return M_L(lat, rho) * hr / M2(pn)


def eps_m(pn, dT):
    return abs(ALPHA_S - PARTNERS[pn][0]) * dT


def sig_loc(pn, dT, kn, c, S):
    return 0.5 * kn * c * ES * eps_m(pn, dT) / (1 + S)


LATS = ['octet', 'BCC', 'A']

# ---------------------------------------------------------------- R29
print("=== R29 stiffness ratio S = M_L H_L/(M_2 H_2) ===")
print("  M_2 [GPa]: " + ", ".join(f"{p}={M2(p) / 1e9:.1f}" for p in PARTNERS))
allS = []
for hr in (0.1, 1.0, 10.0):
    print(f"  H_L/H_2 = {hr}")
    print("    lattice rho    " + "  ".join(f"{p:>10s}" for p in PARTNERS))
    for lat in LATS:
        for rho in (0.1, 0.2, 0.4):
            row = [Sratio(lat, rho, p, hr) for p in PARTNERS]
            if hr == 1.0:
                allS += [(s, lat, rho, p) for s, p in zip(row, PARTNERS)]
            print(f"    {lat:6s} {rho:.1f}   " + "  ".join(f"{s:10.5f}" for s in row))
smin = min(allS)
smax = max(allS)
info('R29', f'H_L=H_2: min S = {smin[0]:.5f} ({smin[1]}, rho={smin[2]}, {smin[3]}); max S = {smax[0]:.5f} ({smax[1]}, rho={smax[2]}, {smax[3]})')
check_true('R29', 'min S is BCC, rho=0.1, steel; max S is A, rho=0.4, Ti', (smin[1], smin[2], smin[3]) == ('BCC', 0.1, 'steel') and (smax[1], smax[2], smax[3]) == ('A', 0.4, 'Ti-6Al-4V'))
check('R29', 'min S about 0.0005 (spec tolerance 2 %)', smin[0], 0.0005, 0.02)
check('R29', 'max S about 0.09 (spec tolerance 2 %)', smax[0], 0.09, 0.02)
check('R29', 'octet rho=0.2 Ti S ~ 0.0135', Sratio('octet', 0.2, 'Ti-6Al-4V'), 0.0135, 0.02)
check_true('R29', '1/(1+S) >= 0.91 at H_L=H_2', 1 / (1 + smax[0]) >= 0.91, f'min 1/(1+S) = {1 / (1 + smax[0]):.4f}')

# ---------------------------------------------------------------- R28
print("\n=== R28 mismatch strain and local amplitude ===")
Sct = Sratio('octet', 0.2, 'Ti-6Al-4V')
print(f"  c values: 1; 1/(1-nu_s)={CNU:.4f}; c_BCC(rho)=sigma_peak/(Es eps_m) from R7: " +
      ", ".join(f"rho={r}: {c_bcc(r):.4f}" for r in (0.1, 0.2, 0.4)))
print("  Ti-6Al-4V, rho=0.2, octet S (H_L=H_2) =", f"{Sct:.5f}")
print("  sigma_a,loc [MPa] (with S) by dT and K_n, c=1; '*' = not elastic (K_n c Es eps_m > sigma_y)")
DTS = (10, 20, 30, 50, 100, 200, 300, 500)
for pn in PARTNERS:
    print(f"   partner {pn} (dalpha={abs(ALPHA_S - PARTNERS[pn][0]) * 1e6:.2f}e-6, eps_m(50K)={eps_m(pn, 50):.3e})")
    print("     dT [K]   " + "  ".join(f"Kn={kn}:c=1".rjust(13) for kn in (1, 2, 3)))
    for dT in DTS:
        cells = []
        S = Sratio('octet', 0.2, pn)
        for kn in (1, 2, 3):
            ne = kn * 1 * ES * eps_m(pn, dT) > SY
            cells.append(f"{sig_loc(pn, dT, kn, 1, S) / MP:11.2f}{'*' if ne else ' '} ")
            if ne:
                pass
        print(f"     {dT:5d}    " + "  ".join(cells))
print("  Ti-6Al-4V, 50 K: sigma_a,loc for c options and lattices (K_n=1,2,3), with own S:")
for lat in LATS:
    for rho in (0.1, 0.2, 0.4):
        S = Sratio(lat, rho, 'Ti-6Al-4V')
        cs = [('1', 1.0), ('1/(1-nu)', CNU), ('c_BCC', c_bcc(rho))]
        print(f"    {lat:6s} rho={rho}: S={S:.5f}  " + "; ".join(
            f"c={n}: " + "/".join(f"{sig_loc('Ti-6Al-4V', 50, kn, c, S) / MP:.2f}" for kn in (1, 2, 3)) for n, c in cs))
nel = []
for pn in PARTNERS:
    for dT in DTS:
        for kn in (1, 2, 3):
            for cn, c in (('1', 1.0), ('1/(1-nu)', CNU), ('c_BCC(0.2)', c_bcc(0.2))):
                if kn * c * ES * eps_m(pn, dT) > SY:
                    nel.append((pn, dT, kn, cn))
info('R28', f'{len(nel)} of {len(PARTNERS) * len(DTS) * 3 * 3} cells flagged not elastic (K_n c Es eps_m > sigma_y = 250 MPa)')
RES.append(('R28', 'FLAG', f'{len(nel)} cells not elastic (listed with * in the table for c=1; all-c count here)'))
check('R28', 'Ti 50 K eps_m', eps_m('Ti-6Al-4V', 50), 6.2e-4, 0.01)
check('R28', 'Ti 50 K Es*eps_m [MPa]', ES * eps_m('Ti-6Al-4V', 50) / MP, 43.4, 0.01)
check('R28', 'Ti 50 K sigma_a,loc K_n=c=1 [MPa], S=0 (spec value)', sig_loc('Ti-6Al-4V', 50, 1, 1, 0.0) / MP, 21.7, 0.01)
check('R28', 'Ti 50 K sigma_a,loc K_n=3,c=1 [MPa], S=0 (spec value)', sig_loc('Ti-6Al-4V', 50, 3, 1, 0.0) / MP, 65.0, 0.01)
check('R28', 'Ti 50 K sigma_a,loc K_n=c=1 [MPa] with octet S (rho=0.2)', sig_loc('Ti-6Al-4V', 50, 1, 1, Sct) / MP, 21.7, 0.01)
check('R28', 'Ti 50 K sigma_a,loc K_n=3,c=1 [MPa] with octet S (rho=0.2)', sig_loc('Ti-6Al-4V', 50, 3, 1, Sct) / MP, 65.0, 0.01)

# ---------------------------------------------------------------- R30
print("\n=== R30 mismatch life and Delta T at which N = 10958 ===")


def Nlife(sar, b):
    return 1e7 * (sar / SW7) ** (1 / b)


def sar_of(pn, dT, kn, c, S, dTref, b):
    sa = sig_loc(pn, dT, kn, c, S)
    if dTref > 0:
        sm = min(SY, ES * abs(ALPHA_S - PARTNERS[pn][0]) * dTref)
        return sa / (1 - sm / SU)
    return sa


def dT_x(pn, kn, c, S, dTref, b, lo=1.0, hi=500.0):
    f = lambda dT: Nlife(sar_of(pn, dT, kn, c, S, dTref, b), b) - NCYC
    flo, fhi = f(lo), f(hi)
    if flo < 0:
        return '<1', None
    if fhi > 0:
        return '>500', None
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi), True


pn = 'Ti-6Al-4V'
print(f"  Ti-6Al-4V, N(50 K) and dT_x [K]; columns S=0 | octet S (rho=0.2)")
for b in (B_MACH, B_AS):
    for kn in (1, 2, 3):
        for cn, c in (('1', 1.0), ('1.49', 1.49)):
            for dTref in (0, 100, 200, 300):
                out = []
                for S in (0.0, Sct):
                    N50 = Nlife(sar_of(pn, 50, kn, c, S, dTref, b), b)
                    x, ok = dT_x(pn, kn, c, S, dTref, b)
                    xs = f"{x:.1f}" if ok else x
                    elastic = ''
                    if ok and kn * c * ES * abs(ALPHA_S - PARTNERS[pn][0]) * x > SY:
                        elastic = ' NOT-ELASTIC'
                    out.append(f"N(50)={N50:.3e} dT_x={xs}{elastic}")
                print(f"    b={b} Kn={kn} c={cn:4s} dTref={dTref:3d} | " + " | ".join(out))
N50 = Nlife(sar_of(pn, 50, 3, 1, 0.0, 0, B_AS), B_AS)
check('R30', 'Ti, c=1, K_n=3, no mean, b=-0.1434, S=0: N(50 K) ~ 5.7e6', N50, 5.7e6, 0.03)
x3, _ = dT_x(pn, 3, 1, 0.0, 0, B_AS)
check('R30', 'same: dT_x ~ 122 K', x3, 122, 0.03)
x1, _ = dT_x(pn, 1, 1, 0.0, 0, B_AS)
check('R30', 'K_n=1: dT_x ~ 367 K', x1, 367, 0.03)
check_true('R30', 'K_n=1 dT_x is outside the elastic range (flag)', 1 * ES * abs(ALPHA_S - 8.6e-6) * x1 > SY,
           f'K_n c Es eps_m at dT_x = {ES * abs(ALPHA_S - 8.6e-6) * x1 / MP:.1f} MPa > 250')
flag('R30', f'K_n=1, Ti, no mean, b=-0.1434: dT_x={x1:.0f} K gives K_n c Es eps_m = {ES * abs(ALPHA_S - 8.6e-6) * x1 / MP:.0f} MPa > sigma_y (not elastic)')
N50s = Nlife(sar_of(pn, 50, 3, 1, Sct, 0, B_AS), B_AS)
x3s, _ = dT_x(pn, 3, 1, Sct, 0, B_AS)
info('R30', f'with octet S: N(50 K) = {N50s:.3e} ({100 * (N50s / 5.7e6 - 1):+.1f} % vs spec 5.7e6); dT_x = {x3s:.1f} K ({100 * (x3s / 122 - 1):+.1f} % vs spec 122)')
check('R30', 'with octet S: N(50 K) vs spec 5.7e6 (3 %)', N50s, 5.7e6, 0.03)
check('R30', 'with octet S: dT_x vs spec 122 (3 %)', x3s, 122, 0.03)
xm, _ = dT_x(pn, 3, 1, 0.0, 300, B_AS)
info('R30', f'Ti K_n=3, c=1, b=-0.1434, sigma_m=min(sigma_y, Es dalpha dT_ref=300 K)=250 MPa (Goodman): dT_x = {xm:.2f} K ({"< 50 K" if xm < 50 else ">= 50 K"})')
x_nomean = dT_x(pn, 3, 1, 0.0, 0, B_AS)[0]
check_true('R30', 'dT_x > 50 K without mean stress; < 50 K with sigma_m = sigma_y (spec expectation "possibly")', x_nomean > 50 and xm < 50,
           f'no mean {x_nomean:.1f} K; with sigma_y mean {xm:.2f} K')
print("  dT_x [K] for all partners, K_n=3, c=1, no mean, S=0 / octet S (b=-0.095 | -0.1434); also K_n=1")
for pn2 in PARTNERS:
    S2 = Sratio('octet', 0.2, pn2)
    cells = []
    for kn in (3, 1):
        for b in (B_MACH, B_AS):
            for S in (0.0, S2):
                x, ok = dT_x(pn2, kn, 1, S, 0, b)
                cells.append(f"{x:.1f}" if ok else x)
            cells.append('|')
    print(f"    {pn2:10s} K_n=3,b=-0.095: {cells[0]}/{cells[1]}  b=-0.1434: {cells[3]}/{cells[4]}   K_n=1,b=-0.095: {cells[6]}/{cells[7]}  b=-0.1434: {cells[9]}/{cells[10]}")
    for kn in (3, 1):
        for b in (B_MACH, B_AS):
            x, ok = dT_x(pn2, kn, 1, 0.0, 0, b)
            if not ok:
                RES.append(('R30', 'FLAG', f'{pn2} K_n={kn} b={b}: dT_x {x} (outside 1-500 K sweep)'))

# ---------------------------------------------------------------- R31
print("\n=== R31 mismatch dissipation under strain control (Ti-6Al-4V, rho=0.2) ===")
pn = 'Ti-6Al-4V'
res31 = {}
for dT in (10, 50):
    for lat in LATS:
        for S in (0.0, Sratio(lat, 0.2, pn)):
            ea = eps_m(pn, dT) / (2 * (1 + S))
            dS = PSI * VENV * M_L(lat, 0.2) * ea ** 2 / T0
            res31[(dT, lat, S == 0.0)] = dS
            print(f"  dT={dT:3d} K {lat:6s} S={S:8.5f}: eps_a={ea:.4e} dS/cycle={dS:.4e} J/K; total over {NCYC} cycles = {dS * NCYC:.4e} J/K; M_L={M_L(lat, 0.2) / 1e9:.4f} GPa")
check('R31', 'octet 50 K dS per cycle, S=0 (spec value) ~3.7e-6', res31[(50, 'octet', True)], 3.7e-6, 0.02)
check('R31', 'octet 50 K total over 10958 cycles, S=0 ~0.041', res31[(50, 'octet', True)] * NCYC, 0.041, 0.02)
check('R31', 'octet 50 K dS per cycle, with S ~3.7e-6', res31[(50, 'octet', False)], 3.7e-6, 0.02)
check('R31', 'octet 50 K total over 10958 cycles, with S ~0.041', res31[(50, 'octet', False)] * NCYC, 0.041, 0.02)
rA0 = res31[(50, 'A', True)] / res31[(50, 'octet', True)]
rA1 = res31[(50, 'A', False)] / res31[(50, 'octet', False)]
check('R31', 'ratio A/octet, S=0: 6 rho/0.7 = 1.714', rA0, 6 * 0.2 / 0.7, 0.02)
check('R31', 'ratio A/octet, with S: 6 rho/0.7 = 1.714', rA1, 6 * 0.2 / 0.7, 0.02)
info('R31', f'A/octet ratio {rA0:.4f} (S=0) / {rA1:.4f} (with S): A dissipates more under strain control; R16 at fixed stress gives octet/A = 1.8 (octet dissipates more): opposite directions')
check_true('R31', 'direction opposite to R16 (A/octet > 1 here, octet/A = 9 rho = 1.8 > 1 in R16)', rA0 > 1 and 9 * 0.2 > 1)

# ---------------------------------------------------------------- R32
print("\n=== R32 interlayer shear and thermal-lag magnitudes ===")
print("  L/H_L:  gamma/eps_m = L/(2 H_L)")
for r in (1, 2, 4, 8, 16):
    g = r / 2
    print(f"    L/H_L={r:2d}: {g:.2f}  ({'> 2' if g > 2 else ('= 2' if g == 2 else '< 2')})")
identity('R32', 'gamma/eps_m = L/(2 H_L) > 2 for L/H_L > 4', 'magnitude table only; equals 2 exactly at L/H_L = 4')
print("  thermal lag: E_s alpha_s dT_lag vs E_s dalpha dT (dT = 50 K)")
for pn2 in ('Ti-6Al-4V', '316L'):
    mism = ES * abs(ALPHA_S - PARTNERS[pn2][0]) * 50
    for lag in (1, 5, 10):
        ls = ES * ALPHA_S * lag
        print(f"    {pn2:10s} dT_lag={lag:2d} K: lag stress {ls / MP:6.2f} MPa; mismatch {mism / MP:6.2f} MPa; ratio {ls / mism:.3f}")
check('R32', 'lag stress 10 K [MPa]', ES * ALPHA_S * 10 / MP, 14.7, 0.01)
check('R32', 'Ti mismatch stress 50 K [MPa]', ES * abs(ALPHA_S - 8.6e-6) * 50 / MP, 43.4, 0.01)
check('R32', '316L mismatch stress 50 K [MPa]', ES * abs(ALPHA_S - 16e-6) * 50 / MP, 17.5, 0.01)
check('R32', '316L dalpha = 5.0e-6', abs(ALPHA_S - 16e-6), 5.0e-6, 0.01)
info('R32', 'break-even dT_lag/dT = dalpha/alpha_s: Ti ' f"{abs(ALPHA_S - 8.6e-6) / ALPHA_S:.3f}, 316L {abs(ALPHA_S - 16e-6) / ALPHA_S:.3f} (D10: 0.59, 0.24)")

summary()
