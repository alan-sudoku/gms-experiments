#!/usr/bin/env python3
"""S5 review, task (2): independent slab Monte Carlo for broad-beam transmitted-energy buildup (row F6, claim G3.4).
Written without reusing f6_buildup_mc.py code. Same physics definition as F6 (so the check tests the implementation,
not the physics choices): pencil beam, normal incidence, infinite slab; free-electron Klein-Nishina Compton; XCOM
photoelectric (log-log interpolation, separate on each side of an edge); no coherent, no fluorescence, no pair
(E0 <= 1 MeV); 20 keV cut-off with local deposit. Differences from F6: Compton energy sampled by Kahn's method,
full 3-D direction vectors, own interpolation, own target solve (weighted linear fit of ln T_E against mu*x on
points around each target). Usage: python3 r3_f6_mc_independent.py [N]   Level: derived.
Inputs: prompt_5_code/data/xcom_z006.csv, xcom_z074.csv (photoelectric column), nist_tab1_za.csv (Z/A).
"""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.normpath(os.path.join(HERE, "..", "prompt_5_code", "data"))
N = int(float(sys.argv[1])) if len(sys.argv) > 1 else 400_000
NA = 6.02214076e23; RE = 2.8179403262e-13; MEC2 = 0.51099895; ECUT = 0.020

def read_pe(z):
    segs = [[]]; prevE = None
    for ln in open(os.path.join(D, "xcom_z%03d.csv" % z)):
        if ln.startswith("#") or ln.startswith("edge"): continue
        p = ln.rstrip("\n").split(",")
        E, pe = float(p[1]), float(p[4])
        if prevE is not None and E == prevE:       # edge: start a new segment at the post-edge value
            segs.append([])
        segs[-1].append((E, pe)); prevE = E
    return [np.array(s) for s in segs]
def za(z):
    for ln in open(os.path.join(D, "nist_tab1_za.csv")):
        p = ln.split(",")
        if p[0].strip() == str(z): return float(p[2])
SEG = {6: read_pe(6), 74: read_pe(74)}; ZA = {6: za(6), 74: za(74)}
def pe(z, E):
    out = np.empty_like(E)
    segs = SEG[z]
    for k, s in enumerate(segs):
        lo = s[0, 0]; hi = segs[k+1][0, 0] if k+1 < len(segs) else np.inf
        m = (E >= lo) & (E < hi) if k > 0 else (E < hi)
        if m.any():
            out[m] = np.exp(np.interp(np.log(E[m]), np.log(s[:, 0]), np.log(s[:, 1])))
    return out
def kn(E):  # cm2 per electron
    a = E/MEC2
    t1 = (1+a)/a**2*(2*(1+a)/(1+2*a) - np.log(1+2*a)/a)
    return 2*math.pi*RE**2*(t1 + np.log(1+2*a)/(2*a) - (1+3*a)/(1+2*a)**2)
def mu(z, E): return pe(z, E) + NA*ZA[z]*kn(E)

def kahn(a, rng):
    """Kahn's rejection method for x = E/E' (Lux & Koblinger form). Returns eps = E'/E."""
    eps = np.empty_like(a); todo = np.arange(len(a))
    while len(todo):
        aa = a[todo]; n = len(todo)
        r1, r2, r3 = rng.random(n), rng.random(n), rng.random(n)
        b1 = r1 <= (1+2*aa)/(9+2*aa)
        x = np.where(b1, 1+2*aa*r2, (1+2*aa)/(1+2*aa*r2))
        cth = 1 + (1 - x)/aa
        acc = np.where(b1, r3 <= 4*(1/x - 1/x**2), r3 <= 0.5*(cth**2 + 1/x))
        eps[todo[acc]] = 1/x[acc]; todo = todo[~acc]
    return eps

def run(z, E0, X, rng):
    E = np.full(N, E0); d = np.tile([0.0, 0.0, 1.0], (N, 1)); zz = np.zeros(N)
    T = 0.0; T2 = np.zeros(N); alive = np.arange(N)
    while len(alive):
        m = mu(z, E)
        zz = zz + d[:, 2]*(-np.log(rng.random(len(E)))/m)
        out = zz >= X; back = zz <= 0
        T2[alive[out]] = E[out]
        k = ~(out | back)
        alive, E, d, zz, m = alive[k], E[k], d[k], zz[k], m[k]
        if not len(E): break
        absorb = rng.random(len(E)) < pe(z, E)/m
        k = ~absorb
        alive, E, d, zz = alive[k], E[k], d[k], zz[k]
        if not len(E): break
        a = E/MEC2; eps = kahn(a, rng)
        cth = 1 - (1/eps - 1)/a; cth = np.clip(cth, -1, 1); sth = np.sqrt(1 - cth**2)
        phi = 2*math.pi*rng.random(len(E)); cp, sp = np.cos(phi), np.sin(phi)
        u, v, w = d[:, 0], d[:, 1], d[:, 2]
        den = np.sqrt(np.maximum(1 - w*w, 0))
        small = den < 1e-10
        un = np.where(small, sth*cp, u*cth + sth*(u*w*cp - v*sp)/np.where(small, 1, den))
        vn = np.where(small, sth*sp, v*cth + sth*(v*w*cp + u*sp)/np.where(small, 1, den))
        wn = np.where(small, np.sign(w)*cth, w*cth - sth*cp*den)
        nrm = np.sqrt(un*un + vn*vn + wn*wn)
        d = np.stack([un/nrm, vn/nrm, wn/nrm], axis=1)
        E = E*eps
        k = E >= ECUT
        alive, E, d, zz = alive[k], E[k], d[k], zz[k]
    t = T2/E0
    return t.mean(), t.std(ddof=1)/math.sqrt(N)

# sampler self-test: mean eps against numerical KN integral
rng = np.random.default_rng(777)
for E0 in (0.5, 1.0):
    a = E0/MEC2; c = np.linspace(-1, 1, 200001)
    e = 1/(1 + a*(1-c)); w = e**2*(e + 1/e - (1 - c*c))
    ref = np.trapezoid(w*e, c)/np.trapezoid(w, c)
    s = kahn(np.full(2_000_000, a), rng)
    print("Kahn sampler self-test E0 = %.1f MeV: <eps> MC %.5f +- %.5f, quadrature %.5f" % (E0, s.mean(), s.std()/math.sqrt(len(s)), ref))
print("N = %d histories per point" % N)
res = {}
for name, z in (("C", 6), ("W", 74)):
    for E0 in (0.5, 1.0):
        m0 = float(mu(z, np.array([E0]))[0])
        pts = []
        for mx in (4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0):
            rng = np.random.default_rng([2026, z, int(E0*10), int(mx*10)])
            T, s = run(z, E0, mx/m0, rng)
            pts.append((mx, T, s))
        pts = np.array(pts)
        for tgt in (1e-2, 1e-3):
            lt = np.log(pts[:, 1]); i = np.argsort(abs(lt - math.log(tgt)))[:4]
            ww = (pts[i, 1]/pts[i, 2])**2
            A = np.vstack([np.ones(4), pts[i, 0]]).T * np.sqrt(ww)[:, None]
            coef, *_ = np.linalg.lstsq(A, lt[i]*np.sqrt(ww), rcond=None)
            mx_t = (math.log(tgt) - coef[0])/coef[1]
            res[(name, E0, tgt)] = mx_t/m0
            print("  %s %.1f MeV mu=%.5f cm2/g: T_E=%g at mu*x = %.3f, x = %.3f g/cm2 (own points used in the fit: %s)" % (
                name, E0, m0, tgt, mx_t, mx_t/m0, ", ".join("%.1f:%.3e" % (p[0], p[1]) for p in pts[sorted(i)])))
F6r = {(0.5, 1e-2): 1.9555, (0.5, 1e-3): 1.8849, (1.0, 1e-2): 1.1629, (1.0, 1e-3): 1.1436}
print("\nx_C/x_W, this script against F6 (outputs/f6_buildup_mc.txt):")
for E0 in (0.5, 1.0):
    for tgt in (1e-2, 1e-3):
        r = res[("C", E0, tgt)]/res[("W", E0, tgt)]
        print("  E0 = %.1f MeV, T_E = %g: %.4f   F6 %.4f   diff %+.1f%%" % (E0, tgt, r, F6r[(E0, tgt)], 100*(r/F6r[(E0, tgt)] - 1)))
