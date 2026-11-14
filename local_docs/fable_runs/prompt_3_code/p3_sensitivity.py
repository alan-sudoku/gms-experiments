"""p3_sensitivity.py -- Prompt 3, S2 implementer.

Purpose : sensitivity of the Q4 limits and entropy maximum to inputs and to the damping
          model: amplitude-dependent psi, thermoelastic damping, one-at-a-time sensitivity,
          stress-ratio effects (Goodman/Morrow).  Level: derived (unverified; FROM MEMORY).
Spec rows: R22 (amplitude-dependent psi factor), R23 (thermoelastic damping),
          R24 (one-at-a-time sensitivity), R25 (stress-ratio effects).
Source  : local_docs/fable_runs/prompt_3_plan.md section 3.2, derivations D5, D6, D8, D11.
Assumptions: rho=0.2, topologies A (f=1.5), B (BCC, Euler-Bernoulli), C [100] as in
          p3_q4_limits.py; R24 central b = -0.1434 (as-built), N=1e7 for sigma_a,max;
          S maximum at nu = 1 Hz, tau_s = 20 y, K_n=1; kappa for A and B taken as the
          circular-section value (bending), C [100] kappa = 1 (uniform axial stress).
          Pure Python (system python3, no numpy).
Run     : python3 p3_sensitivity.py
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


def kappa_circ(n, nq=4000):
    """kappa(n) = <|sigma|^n>/<sigma^2>^(n/2) for a circular section with linear moment (R5 quadrature)."""
    def mom(nn):
        s_len = sum(abs(1 - 2 * (i + 0.5) / nq) ** nn for i in range(nq)) / nq
        num = den = 0.0
        for j in range(nq):
            y = -1 + 2 * (j + 0.5) / nq
            w = 2 * math.sqrt(max(1 - y * y, 0.0))
            num += abs(y) ** nn * w
            den += w
        return s_len * num / den
    return mom(n) / mom(2) ** (n / 2)


# ---------------------------------------------------------------- R22
print("=== R22 factor on Sdot from amplitude-dependent psi: kappa(n_d) (sigma_rms/sigma_ref)^(n_d-2) ===")
cent = {t: SW7 / (KN * T[t]['k']) for t in ('A', 'B', 'C100')}
srms = {'A': cent['A'] * T['A']['k'] / math.sqrt(T['A']['r2']),
        'B': cent['B'] * T['B']['k'] / math.sqrt(T['B']['r2']),
        'C100': cent['C100'] * T['C100']['k'] / math.sqrt(T['C100']['r2'])}
print("  sigma_rms at central amplitudes [MPa]: " + ", ".join(f"{t}={v / MP:.3f}" for t, v in srms.items()))
check('R22', 'sigma_rms A ~12.0 MPa', srms['A'] / MP, 12.0, 0.01)
check('R22', 'sigma_rms B ~16.8 MPa', srms['B'] / MP, 16.8, 0.01)
check('R22', 'sigma_rms C100 = 60 MPa', srms['C100'] / MP, 60.0, 0.01)
ND = (2.0, 2.3, 2.5, 3.0)
KAP = {n: kappa_circ(n) for n in ND}
print("  kappa (circular) = " + ", ".join(f"n_d={n}: {KAP[n]:.4f}" for n in ND) + "; C[100] kappa = 1")
facs = {}
for t in ('A', 'B', 'C100'):
    print(f"  {t}: rows n_d, columns sigma_ref = 5, 20, 60 MPa")
    for n in ND:
        kap = 1.0 if t == 'C100' else KAP[n]
        row = [kap * (srms[t] / (sr * 1e6)) ** (n - 2) for sr in (5, 20, 60)]
        for sr, v in zip((5, 20, 60), row):
            facs[(t, n, sr)] = v
        print(f"    n_d={n}: " + "  ".join(f"{v:9.4f}" for v in row))
for t in ('A', 'B', 'C100'):
    identity('R22', f'{t} n_d=2 factor = 1', f"{[facs[(t, 2.0, s)] for s in (5, 20, 60)]}")
vals = [v for (t, n, s), v in facs.items() if n != 2.0]
print(f"  over n_d in 2.3..3 (n_d=2 excluded): min={min(vals):.4f} max={max(vals):.4f}")
for t in ('A', 'B', 'C100'):
    vt = [v for (tt, n, s), v in facs.items() if tt == t and n != 2.0]
    print(f"    {t}: min={min(vt):.4f} max={max(vt):.4f}")
allv = list(facs.values())
info('R22', f'overall min={min(allv):.4f} (incl. n_d=2 -> 1), max={max(allv):.4f}; spec expects about 0.2-6')
if not (0.15 <= min(allv) <= 0.3 and 5 <= max(allv) <= 7):
    flag('R22', f'range {min(allv):.3f}-{max(allv):.3f} differs from the spec expectation "about 0.2-6"')
# (spec tolerance 1 % is not meaningful for a range; reported only)

# ---------------------------------------------------------------- R23
print("\n=== R23 thermoelastic damping (reed formula applied to round struts) ===")
def psi_te(f, t_m, k=KTH):
    D = k / (RHOS * CP)
    fz = math.pi * D / (2 * t_m ** 2)
    dE = ES * ALPHA_S ** 2 * T0 / (RHOS * CP)
    x = f / fz
    return 2 * math.pi * dE * x / (1 + x * x), fz, dE, D
_, _, dE, D = psi_te(1.0, 1e-3)
print(f"  D = {D:.4e} m^2/s, Delta_E = {dE:.4e}, pi*Delta_E = {math.pi * dE:.4e}")
check('R23', 'Delta_E ~ 3.85e-3', dE, 3.85e-3, 0.02)
xs = [10 ** (-4 + 8 * i / 20000) for i in range(20001)]
mx = max(2 * math.pi * dE * x / (1 + x * x) for x in xs)
check('R23', 'max psi_TE (x scan) ~ 1.21e-2', mx, 1.21e-2, 0.02)
for k in (100.0, 130.0, 170.0):
    print(f"  k = {k:.0f} W/(m K): psi_TE(f) for t = 0.2, 0.5, 1, 2, 5 mm   [f_Z in Hz]")
    print("    f [Hz]        " + "".join(f"t={t:<4}mm      " for t in (0.2, 0.5, 1, 2, 5)))
    for f in (1 / 86400, 1, 10, 100, 1000):
        print(f"    {f:<12.4g}  " + "  ".join(f"{psi_te(f, t * 1e-3, k)[0]:.3e}" for t in (0.2, 0.5, 1, 2, 5)))
    print("    f_Z [Hz]      " + "  ".join(f"{psi_te(1, t * 1e-3, k)[1]:.3e}" for t in (0.2, 0.5, 1, 2, 5)))
    print("    psi_TE/5e-3 at 1 Hz  " + "  ".join(f"{psi_te(1, t * 1e-3, k)[0] / 5e-3:.3e}" for t in (0.2, 0.5, 1, 2, 5)))
    print("    psi_TE/5e-3 max over f " + "  ".join(f"{max(2 * math.pi * dE * x / (1 + x * x) for x in xs) / 5e-3:.3f}" for t in (0.2,)))
p05, fz05, _, _ = psi_te(1.0, 0.5e-3)
p2, fz2, _, _ = psi_te(1.0, 2e-3)
check('R23', 't=0.5 mm f_Z ~ 340 Hz', fz05, 340, 0.02)
check('R23', 't=0.5 mm psi_TE(1 Hz) ~ 7.1e-5', p05, 7.1e-5, 0.02)
check('R23', 't=2 mm f_Z ~ 21 Hz', fz2, 21, 0.02)
check('R23', 't=2 mm psi_TE(1 Hz) ~ 1.1e-3', p2, 1.1e-3, 0.02)
info('R23', f'psi_TE/5e-3 at 1 Hz: t=0.5 mm {p05 / 5e-3:.4f}; t=2 mm {p2 / 5e-3:.4f}; max over f is {mx / 5e-3:.3f} x 5e-3')
info('R23', 'at 1/86400 Hz psi_TE < 1e-8 for all t (see table), i.e. negligible against 5e-3')

# ---------------------------------------------------------------- R24
print("\n=== R24 one-at-a-time sensitivity ===")
CENTRAL = dict(sw7=60e6, sy=250e6, Es=70e9, kn=1.0, psi=5e-3, b=B_AS, f=1.5)
RANGES = dict(sw7=(40e6, 100e6), sy=(200e6, 280e6), Es=(65e9, 75e9), kn=(1.0, 4.0),
              psi=(1e-3, 1e-2), b=(-0.07, -0.20), f=(1.5, 16 / (3 * math.pi)))


def sig_max(t, p):
    Tt = topologies(RHO, sy=p['sy'], Es_=p['Es'], fA=p['f'])[t]
    fat = basquin(1e7, p['sw7'], p['b']) / (p['kn'] * Tt['k'])
    return min(fat, Tt['fy'], Tt['coll'])


def S_max(t, p, nu=1.0, tau=20):
    Tt = topologies(RHO, sy=p['sy'], Es_=p['Es'], fA=p['f'])[t]
    Ncap = nu * tau * YEAR
    sstar = p['sw7'] * (Ncap / 1e7) ** p['b'] / (p['kn'] * Tt['k'])
    suse = min(sstar, Tt['fy'], Tt['coll'])
    Nf = 1e7 * (p['kn'] * Tt['k'] * suse / p['sw7']) ** (1 / p['b'])
    dS = p['psi'] * VENV * suse ** 2 / (2 * Tt['Eeff'] * T0)
    return dS * min(Nf, Ncap), sstar > min(Tt['fy'], Tt['coll'])


for t in ('A', 'B', 'C100'):
    c1, c2 = sig_max(t, CENTRAL), S_max(t, CENTRAL)[0]
    print(f"  topology {t}: central sigma_a,max(1e7) = {c1 / MP:.4f} MPa; S_max(1 Hz, 20 y) = {c2:.4e} J/K")
    rows = []
    for name, (lo, hi) in RANGES.items():
        if name == 'f' and t != 'A':
            continue
        plo, phi = dict(CENTRAL, **{name: lo}), dict(CENTRAL, **{name: hi})
        a_lo, a_hi = sig_max(t, plo), sig_max(t, phi)
        (s_lo, c_lo), (s_hi, c_hi) = S_max(t, plo), S_max(t, phi)
        eff_a = abs(math.log(a_hi / a_lo))
        eff_s = abs(math.log(s_hi / s_lo))
        rows.append((name, a_lo, a_hi, s_lo, s_hi, eff_a, eff_s, c_lo or c_hi))
    print("    ranked by effect on S_max (ln ratio):  input | sigma_a,max [MPa] lo, hi | S_max lo, hi | S ratio hi/lo | cap by yield/collapse?")
    for name, a_lo, a_hi, s_lo, s_hi, ea, es, cap in sorted(rows, key=lambda r: -r[6]):
        print(f"      {name:4s} | {a_lo / MP:8.4f} {a_hi / MP:8.4f} | {s_lo:.4e} {s_hi:.4e} | {s_hi / s_lo:8.4f} | {'YES' if cap else 'no'}")
    print("    ranked by effect on sigma_a,max:")
    for name, a_lo, a_hi, s_lo, s_hi, ea, es, cap in sorted(rows, key=lambda r: -r[5]):
        print(f"      {name:4s} | {a_lo / MP:8.4f} {a_hi / MP:8.4f} | ratio hi/lo {a_hi / a_lo:8.4f}")
    # identity scaling checks
    base = S_max(t, CENTRAL)[0]
    for name, expo in (('psi', 1), ('sw7', 2), ('kn', -2), ('Es', -1)):
        lo, hi = RANGES[name]
        sc = S_max(t, dict(CENTRAL, **{name: hi}))[0] / S_max(t, dict(CENTRAL, **{name: lo}))[0]
        pred = (hi / lo) ** expo
        if abs(sc / pred - 1) < 1e-9:
            identity('R24', f'{t}: S ~ {name}^{expo} (range ends ratio {sc:.5g} = predicted {pred:.5g})', 'analytic scaling')
        else:
            flag('R24', f'{t}: S scaling in {name} deviates from {name}^{expo}: {sc:.5g} vs {pred:.5g} (yield/collapse cap active?)')
    sb = S_max(t, dict(CENTRAL, b=-0.07))[0] / S_max(t, dict(CENTRAL, b=-0.20))[0]
    info('R24', f'{t}: b dependence (not an identity): S(b=-0.07)/S(b=-0.20) = {sb:.4g}')
    if t == 'A':
        sf = S_max('A', dict(CENTRAL, f=16 / (3 * math.pi)))[0] / S_max('A', CENTRAL)[0]
        info('R24', f'A: f 1.5 -> 1.698 changes S_max by factor {sf:.4f} (= (1.5/1.698)^2 = {(1.5 / (16 / (3 * math.pi))) ** 2:.4f})')

# ---------------------------------------------------------------- R25
print("\n=== R25 stress-ratio effects (sigma_u = 400 MPa, sigma_f' = 668 MPa) ===")
print("  mean/amplitude m=(1+R)/(1-R); sigma_max/sigma_a = 2/(1-R)")
for R in (-1.0, 0.0, 0.1):
    m = (1 + R) / (1 - R)
    print(f"  R={R}: m={m:.4f}, sigma_max/sigma_a = {2 / (1 - R):.4f}")
    wG = SW7 / (1 + m * SW7 / SU)
    wM = SW7 / (1 + m * SW7 / SIGF)
    print(f"     local amplitude allowed: no mean {SW7 / MP:.2f}; Goodman {wG / MP:.2f}; Morrow {wM / MP:.2f} MPa")
    print("     macroscopic sigma_a limits [MPa] (K_n=1, N=1e7): topology | fatigue(no mean) Goodman Morrow | first yield (on sigma_max) collapse (on sigma_max) | binding (Goodman)")
    for t in ('A', 'B', 'C100', 'C110'):
        k = T[t]['k']
        fat0, fatG, fatM = SW7 / k, wG / k, wM / k
        fyl = (1 - R) / 2 * T[t]['fy']
        col = (1 - R) / 2 * T[t]['coll']
        bind = min((fatG, 'fatigue(Goodman)'), (fyl, 'first yield'), (col, 'collapse'))[1]
        print(f"       {t:5s} | {fat0 / MP:7.3f} {fatG / MP:7.3f} {fatM / MP:7.3f} | {fyl / MP:7.3f} {col / MP:7.3f} | {bind}")
    if R == 0.1:
        check('R25', 'R=0.1 Goodman allowable local amplitude [MPa]', wG / MP, 50.7, 0.01)
        check('R25', 'R=0.1 mean/amplitude 1.222', m, 1.222, 0.01)
    if R == -1.0:
        identity('R25', 'R=-1 returns the R14 central limits (m=0, no mean-stress factor, sigma_max=2 sigma_a... collapse limit unchanged)',
                 f"Goodman allowable {wG / MP:.3f} MPa = sigma_w7 {SW7 / MP:.3f}")
# R = 10, compression-compression
R = 10.0
print(f"  R={R}: compression-compression; no mean-stress factor applied (fatigue amplitude limit = R14 value)")
for t in ('A', 'B', 'C100', 'C110'):
    k = T[t]['k']
    col = (R - 1) / (2 * R) * T[t]['coll']
    fyl = (R - 1) / (2 * R) * T[t]['fy']
    print(f"       {t:5s} fatigue(no mean factor) {SW7 / k / MP:7.3f} MPa; first yield on |sigma_min| {fyl / MP:7.3f}; collapse on |sigma_min| {col / MP:7.3f}")
flag('R25', 'R=10 compression-compression: reported without a mean-stress factor (compressive mean not credited); buckling/collapse in compression governs the peak')

# R=0.1 also check m numerically via allowable amplitude consistency
Rn = 0.1
mm = (1 + Rn) / (1 - Rn)
wG = SW7 / (1 + mm * SW7 / SU)
chk = wG / (1 - mm * wG / SU)   # equivalent fully reversed amplitude should return sigma_w7
check('R25', 'Goodman round trip: sigma_ar(allowable) = sigma_w7', chk, SW7, 1e-9)

summary()
