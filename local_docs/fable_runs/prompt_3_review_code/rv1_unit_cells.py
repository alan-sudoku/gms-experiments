"""rv1_unit_cells.py -- Prompt 3, S5 independent review.

Level: derived (unverified). Pure Python, no numpy.

Independent route to the octet and BCC unit-cell constants. S2 solved strut forces
(force route, p3_unit_cells.py); this script builds the 6x6 stiffness from the strut
strain-energy density of an affinely deformed Bravais lattice (energy route):

  W(eps) = (rho*E_s/nf) * sum_f 0.5*[ (n.eps.n)^2/lam + (3/4)(d/l)^2/(lam^3 (1+Phi)) |eps.n - (n.eps.n) n|^2 ]

  n      unit strut direction of family f (nf families, equal volume share)
  d/l    strut diameter over node-to-node length
  lam    l_f/l, flexible length over node-to-node length (rigid node zone a_r = (1-lam) l/2)
  Phi    Timoshenko shear term (3/4)(d/l)^2/lam^2 * 2(1+nu_s)/kappa_s, 0 for Euler-Bernoulli
  bending term switched off = pin-jointed model

Affine deformation with zero node rotation is exact for both cells because the nodes of
BCC and of the octet (FCC) each form a Bravais lattice with inversion symmetry.
Strut stresses: axial E_s (n.eps.n)/lam; bending peak (fixed-guided) 3 E_s |g| (d/l)/(lam^2 (1+Phi)).

Run: python3 rv1_unit_cells.py > outputs/rv1_unit_cells.txt
"""
import math

S3 = math.sqrt(3.0)
NUS = 0.33
KAPPA_S = 0.9
VP = [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)]


def unit(v):
    m = math.sqrt(sum(x * x for x in v))
    return [x / m for x in v]


OCT = [unit(v) for v in [(1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1), (0, 1, 1), (0, 1, -1)]]
BCC = [unit(v) for v in [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]]


def d_over_l(cell, rho):
    if cell == 'oct':
        return 2 * math.sqrt(rho / (6 * math.sqrt(2) * math.pi))
    dL = math.sqrt(rho / (S3 * math.pi))
    return dL / (S3 / 2)


def tens(e):
    """Voigt (engineering shear) -> 3x3 tensor."""
    t = [[0.0] * 3 for _ in range(3)]
    for k, (i, j) in enumerate(VP):
        if i == j:
            t[i][i] = e[k]
        else:
            t[i][j] = t[j][i] = e[k] / 2
    return t


def strut_terms(eps, n):
    en = [sum(eps[i][j] * n[j] for j in range(3)) for i in range(3)]
    a = sum(n[i] * en[i] for i in range(3))
    g = [en[i] - a * n[i] for i in range(3)]
    return a, math.sqrt(sum(x * x for x in g))


class Cell:
    def __init__(self, cell, rho, bend=True, timo=False, lam=1.0):
        self.fam = OCT if cell == 'oct' else BCC
        self.rho = rho
        self.dl = d_over_l(cell, rho)
        self.lam = lam
        self.phi = (0.75 * (self.dl / lam) ** 2 * 2 * (1 + NUS) / KAPPA_S) if timo else 0.0
        self.kt = (0.75 * self.dl ** 2 / (lam ** 3 * (1 + self.phi))) if bend else 0.0

    def W(self, e):          # energy density, E_s = 1
        eps = tens(e)
        s = 0.0
        for n in self.fam:
            a, g = strut_terms(eps, n)
            s += 0.5 * (a * a / self.lam + self.kt * g * g)
        return self.rho * s / len(self.fam)

    def C(self):
        I = [[1.0 if i == j else 0.0 for j in range(6)] for i in range(6)]
        C = [[0.0] * 6 for _ in range(6)]
        for i in range(6):
            C[i][i] = 2 * self.W(I[i])
        for i in range(6):
            for j in range(6):
                if i != j:
                    C[i][j] = self.W([I[i][k] + I[j][k] for k in range(6)]) - self.W(I[i]) - self.W(I[j])
        return C

    def stresses(self, e):
        eps = tens(e)
        out = []
        for n in self.fam:
            a, g = strut_terms(eps, n)
            ax = a / self.lam
            bd = (3 * g * self.dl / (self.lam ** 2 * (1 + self.phi))) if self.kt > 0 else 0.0
            out.append((ax, bd))
        return out


def solve(A, b):
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def uniaxial(cell, dvec):
    d = unit(dvec)
    sig = [d[i] * d[j] for (i, j) in VP]
    e = solve(cell.C(), sig)
    eps = tens(e)
    edd = sum(d[i] * eps[i][j] * d[j] for i in range(3) for j in range(3))
    Ed = 1.0 / edd
    st = cell.stresses(e)
    peak = max(ax + bd for ax, bd in [(abs(a), b) for a, b in st])
    W = cell.W(e)                       # = 0.5 * sigma.eps for unit stress
    srms = math.sqrt(2 * W / cell.rho)  # E_s = 1
    return dict(E=Ed, k=peak, r2=(peak / srms) ** 2, W=W, half_e=0.5 * edd, st=st)


def equibiaxial(cell):
    C = cell.C()
    ez = -(C[2][0] + C[2][1]) / C[2][2]
    e = [1.0, 1.0, ez, 0.0, 0.0, 0.0]
    st = cell.stresses(e)
    c = max(abs(a) + b for a, b in st)
    M = C[0][0] + C[0][1] + C[0][2] * ez
    return dict(ez=ez, c=c, M=M, st=st)


def hydro(cell):
    st = cell.stresses([1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
    return max(abs(a) for a, b in st), max(b for a, b in st)


print("=== 1 octet, pin-jointed (rho = 1 normalisation; S2 values: E 1/9, 1/6, 1/5; r^2 1, 6, 1.8) ===")
o = Cell('oct', 1.0, bend=False)
for lab, dv in (('[100]', (1, 0, 0)), ('[110]', (1, 1, 0)), ('[111]', (1, 1, 1))):
    u = uniaxial(o, dv)
    print(f"  {lab}: E/(rho E_s) = {u['E']:.9f}; k_peak*rho = {u['k']:.9f}; r^2 = {u['r2']:.9f}; energy check W vs 0.5 sigma.eps: {u['W']:.9e} {u['half_e']:.9e}")
C = o.C()
print(f"  C11 = {C[0][0]:.9f} (1/6), C12 = {C[0][1]:.9f} (1/12), C44 = {C[3][3]:.9f} (1/12)")
eb = equibiaxial(o)
print(f"  equibiaxial, free normal: eps_zz/eps_m = {eb['ez']:.9f} (S2: -1); c = {eb['c']:.9f} (S2: 1); biaxial modulus/(rho E_s) = {eb['M']:.9f} (S2: 1/6)")
print(f"  hydrostatic: max axial = {hydro(o)[0]:.9f} (S2: 1)")

print("\n=== 2 BCC, beam model, checks against S2 (R6, R7, R9) ===")
for timo in (False, True):
    lab = 'Timoshenko' if timo else 'Euler-Bernoulli'
    print(f"  {lab}")
    for rho in (0.02, 0.1, 0.2, 0.3, 0.4):
        b = Cell('bcc', rho, timo=timo)
        u = uniaxial(b, (0, 0, 1))
        eb = equibiaxial(b)
        print(f"    rho={rho:4.2f}: C1=E/(E_s rho^2)={u['E']/rho**2:.5f}  k_peak={u['k']:.3f}  k_peak*rho^1.5={u['k']*rho**1.5:.4f}  "
              f"r^2={u['r2']:.4f}  c_equibiaxial={eb['c']:.5f}  eps_z/eps_m={eb['ez']:.4f}  hydro (axial, bend)={hydro(b)}")


def crossover(timo, lam_eta=0.0):
    lo, hi = 0.02, 0.6

    def f(r):
        dl = d_over_l('bcc', r)
        lam = 1 - 2 * lam_eta * dl
        return equibiaxial(Cell('bcc', r, timo=timo, lam=lam))['c'] - 1.0
    if f(lo) * f(hi) > 0:
        return None
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if f(lo) * f(m) <= 0:
            hi = m
        else:
            lo = m
    return 0.5 * (lo + hi)


print(f"  crossover c = 1: EB {crossover(False):.4f} (S2 0.2267); Timoshenko {crossover(True):.4f} (S2 0.3093)")

print("\n=== 3 BCC, rigid node zones (sensitivity, UNSURE): a_r = eta*d at each strut end, lam = 1 - 2 eta d/l ===")
print("  eta = 0.87 is the distance (d/2)/sin(35.26 deg) at which two struts at 70.5 deg stop overlapping; 0.25 and 0.5 are milder.")
print("  rho  eta   lam    | EB: C1    k_peak   r^2    c_eq   | Timo: C1  k_peak   r^2    c_eq  | E_s rho^2/E_eff (EB..Timo)")
for rho in (0.1, 0.2, 0.3, 0.4):
    for eta in (0.0, 0.25, 0.5, 0.87):
        dl = d_over_l('bcc', rho)
        lam = 1 - 2 * eta * dl
        vals = []
        for timo in (False, True):
            b = Cell('bcc', rho, timo=timo, lam=lam)
            u = uniaxial(b, (0, 0, 1))
            vals.append((u['E'] / rho ** 2, u['k'], u['r2'], equibiaxial(b)['c']))
        print(f"  {rho:.1f}  {eta:4.2f}  {lam:.3f}  | {vals[0][0]:.4f}  {vals[0][1]:7.2f}  {vals[0][2]:6.2f}  {vals[0][3]:.3f}  | "
              f"{vals[1][0]:.4f}  {vals[1][1]:7.2f}  {vals[1][2]:6.2f}  {vals[1][3]:.3f} | {1/vals[0][0]:.2f}..{1/vals[1][0]:.2f}")
for eta in (0.25, 0.5, 0.87):
    x = crossover(False, eta)
    y = crossover(True, eta)
    print(f"  crossover c = 1 with eta={eta}: EB {x if x is None else round(x, 4)}; Timoshenko {y if y is None else round(y, 4)}")

print("\n=== 4 octet with rigid joints (monolithic AM), affine, Euler-Bernoulli and Timoshenko ===")
print("  S2/S4 use the pin-jointed octet: k_peak*rho = 3 [100], 6 [110]; r^2 = 1 [100], 6 [110].")
for rho in (0.1, 0.2, 0.3, 0.4):
    for timo in (False, True):
        for eta in (0.0, 0.5):
            dl = d_over_l('oct', rho)
            lam = 1 - 2 * eta * dl
            c = Cell('oct', rho, bend=True, timo=timo, lam=lam)
            out = []
            for lab, dv in (('[100]', (1, 0, 0)), ('[110]', (1, 1, 0)), ('[111]', (1, 1, 1))):
                u = uniaxial(c, dv)
                ax = max(abs(a) for a, b in u['st']) * rho
                out.append(f"{lab} E/(rho Es)={u['E']:.4f} k*rho={u['k']*rho:.3f} (max axial*rho {ax:.3f}) r^2={u['r2']:.3f}")
            eb = equibiaxial(c)
            print(f"  rho={rho:.1f} d/l={dl:.4f} {'Timo' if timo else 'EB  '} eta={eta}: " + "; ".join(out)
                  + f"; equibiaxial c={eb['c']:.3f} (axial {max(abs(a) for a, b in eb['st']):.3f}, max bending {max(b for a, b in eb['st']):.3f})")

print("\n=== 5 consequence for the Q4 life-entropy bound (S proportional to 1/(K_n^2 r^2), same sigma_w) ===")
rho = 0.2
pin = 1.0
for timo in (False, True):
    for eta in (0.0, 0.5):
        dl = d_over_l('oct', rho)
        c = Cell('oct', rho, bend=True, timo=timo, lam=1 - 2 * eta * dl)
        u = uniaxial(c, (1, 0, 0))
        print(f"  octet [100], rho 0.2, {'Timo' if timo else 'EB'}, eta={eta}: r^2 = {u['r2']:.3f}; S_max(rigid)/S_max(pin) = {pin/u['r2']:.3f}; "
              f"S4's 3.418e4 J/K (1 Hz, 30 y, sigma_w7 60, b -0.095, K_n 1) becomes {3.4182e4*pin/u['r2']:.3e} J/K; "
              f"fatigue-limited sigma_a at 1e7 = 60/k_peak = {60/u['k']:.3f} MPa (S2: 4.000)")
