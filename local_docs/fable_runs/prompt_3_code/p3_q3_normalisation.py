"""p3_q3_normalisation.py -- Prompt 3, S2 implementer.

Purpose : Q3 normalisation: how many decades a solid-constant macroscopic Basquin law
          over-predicts lattice life, and the predicted normalised endurance ratio.
          Level: derived (unverified; FROM MEMORY inputs used as given).
Spec rows: R26 (life over-prediction), R27 (predicted normalised endurance ratio).
Source  : local_docs/fable_runs/prompt_3_plan.md section 3.2.
Assumptions: k_peak per topology from the R13 definitions (A f=1.5, B BCC Euler-Bernoulli,
          C octet [100], [110]); sigma_y=250 MPa (AlSi10Mg), 950 MPa (Ti-6Al-4V);
          Goodman only for AlSi10Mg (sigma_u=400 MPa; no Ti-6Al-4V sigma_u in the inputs table);
          the Goodman option in R27 reduces the allowable local amplitude as in R25.
          Pure Python (system python3, no numpy).
Run     : python3 p3_q3_normalisation.py
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

# ---------------------------------------------------------------- R26
print("=== R26 life over-prediction log10[(K_n k_peak)^(-1/b)] [decades] ===")
for b in (B_MACH, B_AS):
    for kn in (1.0, 2.0):
        print(f"  b={b}, K_n={kn}")
        print("    rho     " + "  ".join(f"{t:>7s}" for t in TOPS))
        for rho in RHO_SWEEP:
            T = topologies(rho)
            print(f"    {rho:.4f}  " + "  ".join(f"{math.log10((kn * T[t]['k']) ** (-1 / b)):7.2f}" for t in TOPS))
T = topologies(0.2)
exp26 = {('C100', B_MACH): 12.4, ('C100', B_AS): 8.2, ('A', B_MACH): 18.4, ('A', B_AS): 12.2,
         ('B', B_MACH): 22.3, ('B', B_AS): 14.8}
for (t, b), e in exp26.items():
    v = math.log10((1.0 * T[t]['k']) ** (-1 / b))
    check('R26', f'rho=0.2 K_n=1 {t} b={b} [decades]', v, e, 0.05, rel=False)

# ---------------------------------------------------------------- R27
print("\n=== R27 predicted normalised endurance ratio ===")
FB = FSHAPE
mat = {'AlSi10Mg': dict(sy=250e6, sw=(40e6, 60e6, 100e6), su=SU),
       'Ti-6Al-4V': dict(sy=950e6, sw=(150e6, 200e6, 300e6), su=None)}
Rn = 0.1
m = (1 + Rn) / (1 - Rn)
print(f"  amplitude basis: sigma_w/(f K_n sigma_y) bending (f=1.5; f=1.698 in brackets), sigma_w/(K_n sigma_y) stretch")
print(f"  R=0.1 basis: sigma_max/sigma_y = (2/(1-R)) x amplitude ratio, 2/(1-R)={2 / (1 - Rn):.4f}; Goodman replaces sigma_w by sigma_w/(1+{m:.4f} sigma_w/sigma_u)")
for name, d in mat.items():
    print(f"  {name} (sigma_y = {d['sy'] / MP:.0f} MPa)")
    print("    sigma_w  K_n | bend amp [f=1.698] | stretch amp | R=0.1 bend, stretch (no Goodman) | R=0.1 bend, stretch (Goodman)")
    for sw in d['sw']:
        for kn in (1.0, 1.5, 2.0, 3.0):
            bend = sw / (FB * kn * d['sy'])
            bend2 = sw / (F_CIRC * kn * d['sy'])
            st = sw / (kn * d['sy'])
            f01 = 2 / (1 - Rn)
            if d['su']:
                swg = sw / (1 + m * sw / d['su'])
                g = f"{f01 * swg / (FB * kn * d['sy']):.4f}, {f01 * swg / (kn * d['sy']):.4f}"
            else:
                g = 'n/a (no sigma_u input for Ti-6Al-4V)'
            print(f"    {sw / MP:6.0f}  {kn:3.1f} | {bend:.4f} [{bend2:.4f}]   | {st:.4f}      | {f01 * bend:.4f}, {f01 * st:.4f}"
                  f"             | {g}")
check('R27', 'AlSi10Mg bending, sw=60, K_n=1', 60e6 / (FB * 250e6), 0.16, 0.01)
check('R27', 'AlSi10Mg stretch, sw=60, K_n=1', 60e6 / 250e6, 0.24, 0.01)
check('R27', 'Ti-6Al-4V bending, sw=200, K_n=1', 200e6 / (FB * 950e6), 0.14, 0.01)
check('R27', 'Ti-6Al-4V stretch, sw=200, K_n=1', 200e6 / 950e6, 0.21, 0.01)
# rho-independence: normalised ratio uses k_peak/ (collapse-or-yield) ratios; verify numerically for A and C
for t in ('A', 'C100'):
    vals = [(SW7 / topologies(r)[t]['k']) / topologies(r)[t]['fy'] for r in RHO_SWEEP]
    spread = max(vals) / min(vals) - 1
    identity('R27', f'rho-independence of fatigue/first-yield ratio {t}', f'= sigma_w7/sigma_y = {vals[0]:.5f}, spread {spread:.1e}')
flag('R27', 'Goodman option not computed for Ti-6Al-4V: no sigma_u in the inputs table (UNSURE value would be needed)')
info('R27', 'comparison with literature endurance ratios deliberately not made (spec: only after S3 confirms values and stress basis)')

summary()
