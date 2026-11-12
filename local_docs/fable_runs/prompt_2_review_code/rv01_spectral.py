"""Independent check of rows R32-R35 (spectral exergy of radiation). Reviewer script.

All results are claims at level `derived` (unverified). Standalone: numpy only.

Method differs from r32_r35_spectral_exergy.py on purpose:
- composite Gauss-Legendre quadrature on piecewise intervals in u (not trapezoid on logspace);
- integrands written as mode exergy per unit u, ambient occupation n0 computed with expm1;
- dilution modelled two ways: the original max(eps*n_s, n0) and the physically additive
  mixture n = eps*n_s + (1 - eps)*n0 (sun fills a fraction eps of the hemisphere's etendue,
  ambient sky the rest; occupations of incoherent fields sharing a mode after scattering
  add by etendue weight).
- adds a test of the per-mode Carnot bound when the brightness temperature exceeds Ts.
Run: python3 rv01_spectral.py > outputs/rv01_spectral.txt
"""
import math
import numpy as np

TS = 5772.0
T0 = 298.15
x = T0 / TS
EPS = 2.1627e-5

# composite Gauss-Legendre grid on [1e-6, 200] in u, dense near 0 and around u ~ x scale
edges = np.unique(np.concatenate([np.geomspace(1e-6, 1.0, 400), np.linspace(1.0, 200.0, 800)[1:], [2.266]]))  # edge at u_c so the step is not inside a cell
gx, gw = np.polynomial.legendre.leggauss(16)
a, b = edges[:-1, None], edges[1:, None]
U = (0.5 * (b - a) * gx + 0.5 * (b + a)).ravel()
W = (0.5 * (b - a) * gw).ravel()


def occ(u, T_over_Ts):
    """Bose-Einstein occupation at temperature T (u in units of k*Ts)."""
    z = u / T_over_Ts
    out = np.zeros_like(u)
    ok = z < 700
    out[ok] = 1.0 / np.expm1(z[ok])
    return out


def sg(n):
    n = np.asarray(n, float)
    out = np.zeros_like(n)
    p = n > 0
    out[p] = (1 + n[p]) * np.log1p(n[p]) - n[p] * np.log(n[p])
    return out


ns = occ(U, 1.0)
n0 = occ(U, x)


def work(n):
    return np.sum(W * U**2 * (U * (n - n0) - x * (sg(n) - sg(n0))))


E = np.sum(W * U**3 * ns)
print(f"E = {E:.10f}  (pi^4/15 = {math.pi**4/15:.10f})")
land = 1 - 4 / 3 * x + x**4 / 3
psi_full = work(ns) / E
print(f"R32 check: psi(full blackbody) = {psi_full:.8f}; Landsberg formula = {land:.8f}; diff = {psi_full-land:.2e}")

uc = 2.266
n_hp = np.where(U >= uc, ns, n0)
E_hp = np.sum(W * U**3 * ns * (U >= uc))
print(f"R33 check: psi(high-pass u>=2.266) = {work(n_hp)/E_hp:.6f}; energy fraction = {E_hp/E:.6f}")
kk = np.arange(1, 200)
frac_exact = np.sum(np.exp(-kk*uc)*(uc**3/kk + 3*uc**2/kk**2 + 6*uc/kk**3 + 6/kk**4)) / (math.pi**4/15)
print(f"           energy fraction above u_c, series (exact) = {frac_exact:.6f}")

n_max = np.maximum(EPS * ns, n0)
n_add = EPS * ns + (1 - EPS) * n0
print(f"R34a check: psi(diluted, max model) = {work(n_max)/(EPS*E):.6f}")
print(f"R34a alt  : psi(diluted, additive etendue mixture) = {work(n_add)/(EPS*E):.6f}")
n_nob = EPS * ns
print(f"R34b check: psi(diluted, no sky background) = {work(n_nob)/(EPS*E):.6f}")
print(f"           share (1/3)x^4/eps = {x**4/3/EPS:.6f}; psi34b - psi34a(max) = {work(n_nob)/(EPS*E) - work(n_max)/(EPS*E):.6f}")

# sensitivity of the diluted value to the dilution factor (Earth-Sun distance range)
for eps in (2.0e-5, 2.1627e-5, 2.3e-5):
    print(f"   eps = {eps:.4e}: psi(additive) = {work(eps*ns + (1-eps)*n0)/(eps*E):.6f}")

# Per-mode Carnot bound with brightness temperature ABOVE Ts (not tested in R35, which used f <= 1)
rng = np.random.default_rng(1)
u = rng.uniform(0.05, 20, 20000)
Tb = TS * rng.uniform(1.0, 1.10, 20000)          # brightness temperature 0-10 % above Ts
n = occ(u, Tb / TS)
nn0 = occ(u, x)
w_mode = u * (n - nn0) - x * (sg(n) - sg(nn0))
carnot_Ts = u * n * (1 - x)
carnot_Tb = u * n * (1 - T0 / Tb)
v_Ts = int(np.sum(w_mode > carnot_Ts * (1 + 1e-12)))
v_Tb = int(np.sum(w_mode > carnot_Tb * (1 + 1e-12)))
print(f"Per-mode bound with Tb in [Ts, 1.1 Ts]: violations of hv*n*(1 - T0/Ts): {v_Ts} of 20000; "
      f"of hv*n*(1 - T0/Tb): {v_Tb}")
print(f"   max relative excess over (1 - T0/Ts) bound: {np.max((w_mode - carnot_Ts)/carnot_Ts):.3e}")

# Brightness temperature of the real Sun near 480 nm. INPUT IS UNSURE: the AM0 spectral
# irradiance value 2.05 W/m2/nm near 480 nm is the reviewer's recollection of standard
# extraterrestrial spectra, not read from a dataset here.
h, c, k = 6.62607015e-34, 2.99792458e8, 1.380649e-23
lam = 480e-9
omega = math.pi * EPS                               # solid angle of the solar disk [sr]


def irr(T):
    return 2 * h * c**2 / lam**5 / math.expm1(h * c / (lam * k * T)) * omega * 1e-9   # W/m2/nm


lo, hi = 3000.0, 9000.0
target = 2.05                                        # UNSURE input
for _ in range(100):
    mid = 0.5 * (lo + hi)
    lo, hi = (mid, hi) if irr(mid) < target else (lo, mid)
print(f"5772 K blackbody at 480 nm, solar disk: {irr(TS):.4f} W/m2/nm; brightness T for 2.05 W/m2/nm (UNSURE input): {lo:.0f} K")
