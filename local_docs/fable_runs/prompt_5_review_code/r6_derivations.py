#!/usr/bin/env python3
"""S5 review, task (3): independent checks of the derivations the answer relies on.
 1. A4 crossover D_c = (1 - x)/(kappa - 1) and the D > 1 condition (sympy).
 2. D1 Tafel-validity threshold (closed form, and a direct Butler-Volmer root check with alpha_a = alpha_c = 0.5).
 3. Shape-anisotropy ceiling mu0 Ms^2/12 at p = 2/3 (sympy) and the p <= 1/2 branch.
 4. Exchange-spring formulas: numbers of G3.13; hard fraction implied by the 2.4 nm / 9 nm multilayer of the 1993 abstract.
 5. G1.4: same-geometry penalty against thickness for fin, porous electrode, slab absorber (isotropic) and strip (skin
    effect), with kappa = 2. Checks the claim 'thick limit kappa^(1/2), thin limit kappa' per problem.
 6. B3 strip by direct quadrature of the cosh field (third route) and the optimum-to-optimum ratio.
 7. Kelvin optimum (sympy) and J* for Cu; optimum rectangular fin constants.
 8. H1 atom counts (per-atom energy of LiCoO2 + 3C).
Usage: python3 r6_derivations.py   Level: derived.
"""
import math
import numpy as np, sympy as S
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import quad
from scipy.special import expn

print("== 1. A4 duty crossover ==")
x, k, D = S.symbols("x kappa D", positive=True)
# Sigma_g - Sigma_s in units of Sigma_init,s at equal volume: (x - 1) + D (kappa - 1)
Dc = S.solve(S.Eq((x - 1) + D*(k - 1), 0), D)[0]
print("  D_c =", S.simplify(Dc), "; D_c > 1 <=>", S.solve(S.Gt(Dc.subs(k, 1.63842), 1), x))
kap = 5.80e7/3.54e7
for nm, xv in (("Nuss primary", 194*2700/(59.3*8960)), ("ICE rec/rec", 29.0*2700/(16.5*8960)), ("Nuss mix", 131*2700/(53.7*8960))):
    print("  %-12s x = %.4f, D_c = %.4f" % (nm, xv, (1 - xv)/(kap - 1)))
J2t = (59.3e6*8960 - 194e6*2700)/(1/3.54e7 - 1/5.80e7)
print("  Nuss primary (J^2 tau)* = %.3e A^2 s/m^4 -> %.3e s at 1 A/mm^2" % (J2t, J2t/1e12))

print("\n== 2. D1 Tafel validity ==")
F, R = 96485.332, 8.314462
for T in (298.15, 353.15):
    f = F/(R*T)
    for aa, ac in ((0.5, 0.5),):
        # error of Tafel eta for BV with both alphas: eta - eta_T = -ln(1 - exp(-(aa+ac) f eta))/(aa f)
        err = lambda eta: -math.log(1 - math.exp(-(aa + ac)*f*eta))/(aa*f)
        th = brentq(lambda e: err(e) - 0.002, 1e-3, 1.0)
        # direct check: choose j/j0 so that BV eta = th, compare to Tafel
        jr = math.exp(aa*f*th) - math.exp(-ac*f*th); etaT = math.log(jr)/(aa*f)
        print("  T = %.2f K, alpha_a = alpha_c = %.1f: 2 mV threshold eta = %.2f mV; direct BV check eta - eta_T = %.3f mV" % (T, aa, 1e3*th, 1e3*(th - etaT)))
    # Delta-eta error with eta_g >= eta_s is bounded by err(eta_s); with area compensation eta_g < eta_s the bound is err(eta_g)
print("  Delta-eta error = err(eta_g) - err(eta_s); both errors positive and decreasing, so |error| <= err(min(eta_s, eta_g)):")
print("  the condition 'both above threshold' is sufficient; without area compensation (eta_g >= eta_s) the planner's 'eta_s above threshold' already suffices.")

print("\n== 3. Shape-anisotropy ceiling ==")
p, Hp, Ms = S.symbols("p H Ms", positive=True)
BH = (p*Ms - Hp)*Hp            # in units of mu0
Hc = (1 - p)*Ms/2
inner = S.solve(S.diff(BH, Hp), Hp)[0]
print("  unconstrained optimum H' =", inner, "; reachable iff p*Ms/2 <= Hc <=> p <=", S.solve(S.Eq(inner, Hc), p))
edge = S.simplify(BH.subs(Hp, Hc))
popt = S.solve(S.diff(edge, p), p)
print("  edge branch BH(Hc) =", S.factor(edge), "; stationary p =", popt, "; value =", S.simplify(edge.subs(p, popt[0])/Ms**2), "* mu0 Ms^2")
print("  p <= 1/2 branch maximum:", S.simplify((BH.subs(Hp, inner)).subs(p, S.Rational(1, 2))/Ms**2), "* mu0 Ms^2")
mu0 = 1.25663706e-6
for nm, B in (("Fe65Co35 2.45 T", 2.45), ("Fe65Co35 2.43 T", 2.43), ("Fe 2.15 T", 2.15)):
    print("  %s: mu0 Ms^2/12 = %.1f kJ/m^3; mu0 Ms^2/4 = %.1f kJ/m^3" % (nm, B**2/mu0/12/1e3, B**2/mu0/4/1e3))
print("  model assumptions: rectangular M(H) loop of each needle, Neel mean-field H_c(p) = H_c(0)(1 - p), coherent rotation;")
print("  incoherent reversal (curling) lowers H_c well below Ms/2 for real needle radii, so 1/12 is an upper bound of this model only.")

print("\n== 4. Exchange-spring numbers ==")
def es(Bs, Bh, Kh):
    Mss, Mh = Bs/mu0, Bh/mu0
    fh = mu0*Mss**2/(4*Kh); bh = mu0*Mss**2/4*(1 - mu0*(Mss - Mh)*Mss/(2*Kh))
    return fh, bh/1e3
print("  Sm2Fe17N3 (1.55 T, 12 MJ/m3) + Fe65Co35 2.43 T: f_h = %.4f, (BH)max = %.0f kJ/m3" % es(2.43, 1.55, 12e6))
print("  Nd2Fe14B (1.61 T, 4.9 MJ/m3) + Fe65Co35 2.43 T: f_h = %.4f, (BH)max = %.0f kJ/m3" % es(2.43, 1.61, 4.9e6))
print("  wall width pi sqrt(A/K), A = 8 pJ/m, K = 4.9 MJ/m3: %.2f nm" % (math.pi*math.sqrt(8e-12/4.9e6)*1e9))
fh_ml = 2.4/(2.4 + 9.0)
# rare-earth mass fraction of such a multilayer: Sm2Fe17N3 (Sm 23 wt%) volume fraction fh_ml; densities 7.7 and 8.1 g/cm3 (REVIEWER MEMORY, UNSURE)
mSm = 2*150.36/(2*150.36 + 17*55.845 + 3*14.007)
wRE = fh_ml*7.7*mSm/(fh_ml*7.7 + (1 - fh_ml)*8.1)
print("  1993 abstract multilayer 2.4 nm hard / 9 nm soft (search result, not read): hard volume fraction %.3f; Sm mass fraction of Sm2Fe17N3 %.3f;" % (fh_ml, mSm))
print("  RE wt%% of the multilayer with densities 7.7 / 8.1 g/cm3 (UNSURE) = %.1f%% (abstract: 5 wt%%). The formula's f_h = 0.098 is a lower limit;" % (100*wRE))
print("  the abstract's design sits at about 0.21, so 'f_h 0.10 to 0.24' understates the hard fraction of the quoted realisation by about 2x.")

print("\n== 5. G1.4: same-geometry penalty P = F(c_s)/F(c_g), kappa = 2, against the incumbent's thickness parameter ==")
kap2 = 2.0
xi = np.logspace(-3, 2, 2001)
# fin: penalty = q_s/q_g = sqrt(k_s/k_g) tanh(m_s L)/tanh(m_g L), m_g = sqrt(kappa) m_s
Pfin = math.sqrt(kap2)*np.tanh(xi)/np.tanh(math.sqrt(kap2)*xi)
# porous electrode: j0eff = j0 a lam tanh(L/lam), lam ~ j0^-1/2 -> ratio s/g = kappa * (lam_s/lam_g) tanh(L/lam_s)/tanh(L/lam_g) = sqrt(kappa) tanh(X)/tanh(X/sqrt(kappa))
Ppor = math.sqrt(kap2)*np.tanh(xi)/np.tanh(xi/math.sqrt(kap2))
# slab absorber, isotropic flux: P = 1 - 2 E3(tau), tau_g = tau_s/kappa
Pabs = (1 - 2*expn(3, xi))/(1 - 2*expn(3, xi/kap2))
# strip skin effect: R_g/R_s = kappa F(xi/sqrt(kappa))/F(xi)
Fd = lambda z: z*(np.sinh(2*z) + np.sin(2*z))/(np.cosh(2*z) - np.cos(2*z))
xs = xi[xi < 30]
Pstr = kap2*Fd(xs/math.sqrt(kap2))/Fd(xs)
for nm, P in (("fin (X = m_s L)", Pfin), ("porous electrode (X = L/lam_s)", Ppor), ("slab absorber (X = tau_s)", Pabs), ("strip, skin effect (X = t/(2 delta_s))", Pstr)):
    print("  %-38s thin end %.4f, thick end %.4f, min %.4f, max %.4f   (kappa^1/2 = %.4f, kappa = %.1f)" % (nm, P[0], P[-1], P.min(), P.max(), math.sqrt(kap2), kap2))
print("  => fin: penalty between 1 (thin) and kappa^1/2 (thick); absorber: between kappa (thin) and 1 (black);")
print("     only the porous electrode spans [kappa^1/2, kappa]; the strip dips below kappa^1/2.")
print("     G1.4 ('thick limit c^(1/2), penalty kappa^(1/2) thick and kappa thin') holds for the porous electrode only.")
print("     Compensation price (not penalty) for the fin is t_g/t_s = kappa at every mL (equal k t); G1.4 mixes the two.")

print("\n== 6. B3 strip by quadrature of the cosh field ==")
def ratio_q(xi_):
    g = (1 + 1j)            # x in units of delta; E = cosh(g x)/cosh(g xi), x in [-xi, xi]
    Ef = lambda xx: np.cosh(g*xx)/np.cosh(g*xi_)
    I2 = quad(lambda xx: abs(Ef(xx))**2, -xi_, xi_, limit=400)[0]
    Ir = quad(lambda xx: Ef(xx).real, -xi_, xi_, limit=400)[0]; Ii = quad(lambda xx: Ef(xx).imag, -xi_, xi_, limit=400)[0]
    return 2*xi_*I2/(Ir**2 + Ii**2)
mu0 = 1.25663706e-6; sCu, sAl = 5.80e7, 3.54e7
dCu = math.sqrt(2/(2*math.pi*50*mu0*sCu)); dAl = math.sqrt(2/(2*math.pi*50*mu0*sAl))
worst = 0
for tr in np.geomspace(0.05, 30, 40):
    for z in (tr/2, tr*dCu/dAl/2):
        worst = max(worst, abs(ratio_q(z)/Fd(z) - 1))
print("  max |F_quad/F_closed - 1| over 80 points: %.1e" % worst)
res = minimize_scalar(lambda tr: (sCu/sAl)*ratio_q(tr*dCu/dAl/2)/ratio_q(tr/2), bounds=(2, 10), method="bounded")
print("  minimum same-geometry R_ac ratio Al/Cu = %.4f at t/delta_Cu = %.3f (answer: 1.216 at 4.72)" % (res.fun, res.x))
mn = minimize_scalar(lambda z: Fd(z)/z, bounds=(0.5, 5), method="bounded")
print("  each metal at its own optimum thickness (xi = %.4f, F/xi = %.4f): R_min,Al/R_min,Cu = sqrt(kappa) = %.4f" % (mn.x, mn.fun, math.sqrt(sCu/sAl)))
print("  => the dip to 1.216 appears only when both use the same thickness; with each at its optimum the ratio is 1.280 (fairness rule).")

print("\n== 7. Kelvin optimum and fin constants ==")
A, e, rho, sig, I, Lc, tau, T0 = S.symbols("A e rho sigma I L tau T0", positive=True)
Sig = e*rho*A*Lc/T0 + I**2*Lc*tau/(sig*A*T0)
As = S.solve(S.diff(Sig, A), A)[0]
print("  A* =", S.simplify(As), "; Sigma* =", S.simplify(Sig.subs(A, As)))
print("  J* Cu (e 55 MJ/kg, tau 6.31e8 s) = %.4f A/mm^2" % (math.sqrt(5.8e7*8960*55e6/6.31e8)/1e6))
beta = brentq(lambda b: math.tanh(b) - 3*b/math.cosh(b)**2, 0.5, 3)
# q' = theta sqrt(2hkt) tanh(beta), beta = L sqrt(2h/(k t)), A_p = t L ; express A_p in terms of q': t = (q'/theta)^2/(2hk tanh^2 beta), L = beta sqrt(k t/(2h))
h_, k_, q_ = 50.0, 200.0, 3.0
t_ = q_**2/(2*h_*k_*math.tanh(beta)**2); L_ = beta*math.sqrt(k_*t_/(2*h_)); Ap = t_*L_
print("  optimum beta = %.5f; A_p h^2 k/(q'/theta)^3 = %.5f (answer: 1.4192 and 0.504)" % (beta, Ap*h_**2*k_/q_**3))

print("\n== 8. H1 per-atom energy, LiCoO2 + 3C at 0.5 Li ==")
atoms = {"Li": 1, "Co": 1, "O": 2, "C": 3}
print("  atoms in LiCoO2 + 3C = %d (h1 script uses N_at = 6)" % sum(atoms.values()))
print("  n V / N_at = 0.5 * 3.7 / 7 = %.4f eV/atom (answer table: 0.308 = 0.5 * 3.7 / 6)" % (0.5*3.7/7))
