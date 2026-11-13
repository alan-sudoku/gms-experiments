"""Rows C06, C07, C08: Ni foam roughness and electronic drop; utilisation of a porous electrode;
thickness-independent minimum overpotential.

M-PE: delta = J L/(kappa_eff b); theta from 2 theta tan(theta) = delta (bisection, tol 1e-12);
E = sin(2 theta)/(2 theta); dEta_ion = b ln(1/E); kappa_eff = kappa (eps (1-eps_g))^1.5;
eta_min = b acosh(1 + J^2/(4 kappa_eff a_v j0 b)).  Second method for C07: RK4 shooting on u'' = exp(u).
Units: J, j0 in A/m2, a_v in m2/m3, kappa in S/m, b in V.  Level: derived (unverified).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gms_core import *

T_EC = 298.15
B05 = R_GAS * T_EC / (0.5 * F_CONST)
B40 = 0.04 / math.log(10)
print("Rows C06, C07, C08  (level: derived, unverified)")
print("b(alpha=0.5, 298.15 K) = %.5f V ; b(40 mV/decade) = %.5f V (spec quotes 0.01737)" % (B05, B40))


def theta_of(delta):
    lo, hi = 1e-12, math.pi / 2 - 1e-12
    f = lambda t: 2 * t * math.tan(t) - delta
    while hi - lo > 1e-12:
        mid = 0.5 * (lo + hi)
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def util(delta):
    th = theta_of(delta)
    return th, math.sin(2 * th) / (2 * th)


def keff(kappa, eps, eg):
    return kappa * (eps * (1 - eg)) ** 1.5


def etamin(J, kef, av, j0, b):
    return b * math.acosh(1 + J * J / (4 * kef * av * j0 * b))


def rk4_delta(u1, n=2000):
    """u''=exp(u) from zeta=0 (u=u1, u'=0) to zeta=1; returns (u'(1), u(1))."""
    h = 1.0 / n
    u, w = u1, 0.0
    for _ in range(n):
        def f(uu, ww): return ww, math.exp(uu) if uu < 700 else float("inf")
        k1 = f(u, w)
        k2 = f(u + 0.5 * h * k1[0], w + 0.5 * h * k1[1])
        k3 = f(u + 0.5 * h * k2[0], w + 0.5 * h * k2[1])
        k4 = f(u + h * k3[0], w + h * k3[1])
        u += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        w += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        if u > 700 or not math.isfinite(w):
            return float("inf"), float("inf")
    return w, u


def E_numeric(delta):
    lo, hi = -30.0, 1.596
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        w, _u = rk4_delta(mid)
        if w < delta:
            lo = mid
        else:
            hi = mid
    u1 = 0.5 * (lo + hi)
    w, u0 = rk4_delta(u1)
    return delta / math.exp(u0), w


# ---------------------------------------------------------------- C06
head("C06 Ni foam: geometric roughness and electronic drop")
Lf, sig, Jm, wrib = 1.6e-3, 1.43e7, 1.0e4, 0.010
print_inputs(L=Lf, sigma_Ni=sig, J=Jm, rib_pitch=wrib, a_v=[5e3, 1e4, 1.5e4], rho_bar=[0.03, 0.05, 0.10])
lb = Jm * Lf / (2 * sig)
print("lower bound J L/(2 sigma_Ni) = %.4e V" % lb)
allok = True
dvs = []
for av in (5e3, 1e4, 1.5e4):
    print("  a_v=%g: R_f,geom = %.2f" % (av, av * Lf))
for rb in (0.03, 0.05, 0.10):
    s1, s2 = sig * rb / 3, sig * rb ** 1.7
    d1, d2 = Jm * Lf / (2 * s1), Jm * Lf / (2 * s2)
    i1, i2 = Jm * wrib ** 2 / (8 * s1 * Lf), Jm * wrib ** 2 / (8 * s2 * Lf)
    dvs += [d1, d2]
    print("  rho_bar=%.2f: Lemlich sigma_eff=%.4e dV=%.4e V (in-plane %.4e V); power law sigma_eff=%.4e dV=%.4e V (in-plane %.4e V)" % (rb, s1, d1, i1, s2, d2, i2))
    allok = allok and d1 < 1e-3 and d2 < 1e-3 and d1 > lb and d2 > lb
check("C06 both models give dV < 1 mV and exceed the solid-Ni bound", allok, "max dV %.3e V, min dV %.3e V" % (max(dvs), min(dvs)))
rng("R_f,geom min", 5e3 * Lf, 8, 24); rng("R_f,geom max", 1.5e4 * Lf, 8, 24)
rng("dV min", min(dvs), 1e-5, 3e-4); rng("dV max", max(dvs), 1e-5, 3e-4)
for rb in (0.03, 0.05, 0.10):
    ip = Jm * wrib ** 2 / (8 * sig * rb / 3 * Lf)
    rng("dV_ip Lemlich rho=%.2f [mV]" % rb, ip * 1e3, 0.2, 2.0)
info("C06 consistency", "rho_bar = 0.10 corresponds to eps = 0.90 used in C07/C08 foam cases; rho_bar 0.03/0.05 (eps 0.97/0.95) are not used elsewhere; dV_ip uses an assumed rib pitch")

# ---------------------------------------------------------------- C07
head("C07 utilisation of a finite porous electrode")
print_inputs(L=[0.3e-3, 1.6e-3], J=Jm, kappa=[20, 62, 140], eps=0.9, eps_g=[0, 0.3], b=[B05, 0.01737])
print("%8s %6s %5s %8s | %7s %6s %7s %7s %9s %9s" % ("L[mm]", "kappa", "eg", "b[V]", "delta", "theta", "E", "Leff[um]", "dEta[V]", "E_num"))
maxrel_grid = 0
for Lc in (0.3e-3, 1.6e-3):
    for kap in (20, 62, 140):
        for eg in (0.0, 0.3):
            for b in (B05, 0.01737):
                kef = keff(kap, 0.9, eg)
                dl = Jm * Lc / (kef * b)
                th, E = util(dl)
                En, _w = E_numeric(dl)
                maxrel_grid = max(maxrel_grid, abs(E - En) / E)
                print("%8.2f %6g %5.1f %8.5f | %7.3f %6.3f %7.4f %7.1f %9.5f %9.5f" % (Lc * 1e3, kap, eg, b, dl, th, E, E * Lc * 1e6, b * math.log(1 / E), En))
print("max |E - E_num|/E over the 24 grid cases: %.3e" % maxrel_grid)
check("C07 grid cases (extra): |E-E_num|/E <= 0.005", maxrel_grid <= 0.005, "max %.3e" % maxrel_grid)
for dl in (0.5, 5.0, 50.0):
    th, E = util(dl)
    En, w = E_numeric(dl)
    check("C07 delta=%g: E=%.6f vs E_num=%.6f (|rel| <= 0.005)" % (dl, E, En), abs(E - En) / E <= 0.005, "rel diff %.3e (shooting residual of delta %.2e)" % ((E - En) / E, w - dl))
th, E = util(0.01)
check("C07 delta=0.01: E within 1 % of 1 - delta/3", abs(E / (1 - 0.01 / 3) - 1) < 0.01, "E=%.6f, 1-delta/3=%.6f" % (E, 1 - 0.01 / 3))
th, E = util(100.0)
check("C07 delta=100: E within 1 % of 2/delta", abs(E / 0.02 - 1) < 0.01, "E=%.6f, 2/delta=0.02" % E)
kef = keff(62, 0.9, 0.0)
dl = Jm * 1.6e-3 / (kef * B05)
th, E = util(dl)
rng("hand case delta", dl, 5.5, 6.3); rng("hand case E", E, 0.27, 0.31); rng("hand case dEta_ion", B05 * math.log(1 / E), 0.058, 0.068)
dl2 = Jm * 1.6e-3 / (kef * 0.01737)
rng("hand case b=17.4 mV: E", util(dl2)[1], 0.10, 0.12)
info("C07 note", "E_num uses the RK4 solution of u''=exp(u) with u'(1)=0; for a given delta it is independent of the theta bisection")

# ---------------------------------------------------------------- C08
head("C08 thickness-independent minimum overpotential")
refs = {("P1", 1): 0.084643, ("P1", 100): 0.0012845, ("P1", 200): 0.000642, ("P2", 1): 0.381205, ("P2", 100): 0.144752, ("P2", 200): 0.109675}
print("Pt references (from C02 recomputed): " + ", ".join("%s Rf=%d: %.6f V" % (k[0], k[1], v) for k, v in refs.items()))
cases = [("bare foam", 1e4, 0.90), ("foam Rf,tot=1000", 6.25e5, 0.90), ("1 um pores", 2e6, 0.50), ("0.1 um pores", 2e7, 0.50)]
print("%-18s %8s %6s %4s %5s | %9s %10s | reaches (P1:1/100/200, P2:1/100/200)" % ("case", "j0[A/m2]", "kappa", "eg", "a_v", "eta_min", "R_eff"))
Jc = 1.0e4
tafel_bad = 0
hand = {}
for nm, av, eps in cases:
    for j0 in (0.01, 0.1, 1.0):
        for kap in (62, 140):
            for eg in (0.0, 0.3):
                kef = keff(kap, eps, eg)
                em = etamin(Jc, kef, av, j0, B05)
                Reff = Jc / (2 * j0 * math.sinh(em / B05))
                v = "".join("Y" if em <= refs[k] else "n" for k in [("P1", 1), ("P1", 100), ("P1", 200), ("P2", 1), ("P2", 100), ("P2", 200)])
                print("%-18s %8.2g %6g %4.1f %.3g | %9.5f %10.4g | %s" % (nm, j0, kap, eg, av, em, Reff, v))
                arg = Jc ** 2 / (2 * kef * av * j0 * B05)
                if arg > 100:
                    tf = B05 * math.log(arg)
                    if abs(tf / em - 1) > 0.01:
                        tafel_bad += 1
                        issue("C08 Tafel limit miss >1%% for %s j0=%g kappa=%g eg=%g: eta_min=%.5f Tafel=%.5f" % (nm, j0, kap, eg, em, tf))
                if (av, j0, kap, eg) == (2e6, 0.1, 62, 0.0): hand["a2e6"] = em
                if (av, j0, kap, eg) == (2e7, 0.1, 62, 0.0): hand["a2e7"] = em
check("C08 Tafel form within 1 % when argument > 100", tafel_bad == 0, "%d misses" % tafel_bad)
rng("hand eta_min a_v=2e6, j0=0.1, kappa=62, eg=0", hand["a2e6"], 0.27, 0.29)
rng("hand eta_min a_v=2e7, j0=0.1, kappa=62, eg=0", hand["a2e7"], 0.15, 0.17)
print("Second route (foam, L = 0.016 m): eta_thick = b ln(J/(a_v j0 L E)) vs eta_min")
bad2 = 0
n2 = 0
for nm, av, eps in cases[:2]:
    for j0 in (0.01, 0.1, 1.0):
        for kap in (62, 140):
            for eg in (0.0, 0.3):
                kef = keff(kap, eps, eg)
                Lt = 0.016
                dl = Jc * Lt / (kef * B05)
                th, E = util(dl)
                et = B05 * math.log(Jc / (av * j0 * Lt * E))
                em = etamin(Jc, kef, av, j0, B05)
                applies = em > 3 * B05
                rel = et / em - 1
                print("  %-18s j0=%-5g kappa=%-4g eg=%.1f delta=%8.2f E=%.4f eta_thick=%.5f eta_min=%.5f rel=%+.3e %s" % (nm, j0, kap, eg, dl, E, et, em, rel, "(applies)" if applies else "(eta_min <= 3b: not applicable)"))
                if applies:
                    n2 += 1
                    if abs(rel) > 0.02:
                        bad2 += 1
                        issue("C08 second route misses 2%% for %s j0=%g kappa=%g eg=%g: rel %.3e" % (nm, j0, kap, eg, rel))
check("C08 second route within 2 %% when eta_min > 3 b (%d applicable cases)" % n2, bad2 == 0, "%d misses" % bad2)
issue("C08 uses sinh-kinetics in eta_min but Tafel-form kinetics in D8's utilisation E; the 2 % comparison therefore also absorbs the sinh-vs-exp difference, which is small only for eta_min > 3b")
