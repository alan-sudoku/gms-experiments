"""Rows B01, B02: plate-fin efficiency against k at fixed h, and Al thickness that matches Cu.

B01: eta = tanh(mH)/(mH), m = sqrt(2h/(k t)); second method: finite-difference solution
of theta'' = m^2 theta (400 nodes, adiabatic tip via ghost node), root flux by a
second-order one-sided difference.  B02: t_Al = t_Cu*k_Cu/k_Al, open-area ratios.
Assumptions: as in plan 3.2 rows B01, B02.  Level: derived (unverified).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gms_core import *


def eta_an(k, h, t, Hh=H):
    m = math.sqrt(2 * h / (k * t))
    return math.tanh(m * Hh) / (m * Hh)


def eta_fd(k, h, t, Hh=H, n=400):
    m2 = 2 * h / (k * t)
    dx = Hh / (n - 1)
    # unknowns theta_1..theta_{n-1}; theta_0 = 1; tip node n-1 with ghost theta_n = theta_{n-2}
    N = n - 1
    A = np.zeros((N, N)); b = np.zeros(N)
    for i in range(N):
        A[i, i] = -2 - m2 * dx * dx
        if i > 0:
            A[i, i - 1] = 1
        else:
            b[i] -= 1.0
        if i < N - 1:
            A[i, i + 1] = 1
        else:
            A[i, i - 1] = 2
    th = np.concatenate(([1.0], np.linalg.solve(A, b)))
    dth0 = (-3 * th[0] + 4 * th[1] - th[2]) / (2 * dx)
    return -k * t * dth0 / (2 * h * Hh)


print("Rows B01, B02  (level: derived, unverified)")
t = 0.4e-3
ks = [390, 200, 180, 150, 120, 100]
hs = [40, 75, 150]
print_inputs(H=H, t=t, h=hs, k=ks)
head("B01 table: eta_analytic / eta_FD")
print("k\\h " + "".join("%22g" % h for h in hs))
maxd = 0
for k in ks:
    row = "%4g" % k
    for h in hs:
        a, f = eta_an(k, h, t), eta_fd(k, h, t)
        maxd = max(maxd, abs(a - f))
        row += "   %.5f / %.5f  " % (a, f)
    print(row)
check("B01 max |eta - eta_FD| <= 0.005", maxd <= 0.005, "max diff %.3e" % maxd)
hand = {390: .79, 200: .66, 180: .64, 150: .60, 120: .56, 100: .52}
for k in ks:
    e = eta_an(k, 75, t)
    ok = abs(e - hand[k]) <= 0.03
    print(("RANGE-OK    " if ok else "RANGE-MISS  ") + "eta(h=75,k=%g)=%.4f hand %.2f +-0.03" % (k, e, hand[k]))
    if not ok:
        issue("hand-range miss B01 eta(h=75,k=%g)=%.4f vs %.2f+-0.03" % (k, e, hand[k]))
e = eta_an(1e6, 75, t)
check("B01 limit k=1e6: eta within 1e-3 of 1", abs(e - 1) < 1e-3, "eta=%.6f" % e)
m = math.sqrt(2 * 75 / (1 * t)); e = eta_an(1, 75, t)
check("B01 limit k=1: eta within 1% of 1/(mH)", abs(e * m * H - 1) < 0.01, "eta=%.6f, 1/(mH)=%.6f" % (e, 1 / (m * H)))
e2 = eta_fd(1, 75, t); info("FD at k=1 (not part of check)", "eta_FD=%.6f" % e2)

head("B02 Al thickness matching the Cu fin")
tcu, Nf = 0.4e-3, 32
scu = 1 - Nf * tcu / W
print_inputs(t_Cu=tcu, N_f=Nf, W=W, sigma_Cu="%.4f" % scu)
smin_viol = []
for k in K_AL_SET:
    ta = tcu * K_CU / k
    sa = 1 - Nf * ta / W
    s_ch = (W - Nf * ta) / (Nf - 1)
    e_cu = eta_an(K_CU, 75, tcu); e_al = eta_an(k, 75, ta)
    print("k_Al=%4g  t_Al=%.4f mm  sigma_Al=%.4f  channel gap s=%.4f mm  eta_Al(h=75)=%.12f eta_Cu=%.12f diff=%.2e" % (
        k, ta * 1e3, sa, s_ch * 1e3, e_al, e_cu, abs(e_al - e_cu)))
    if s_ch < S_MIN:
        smin_viol.append((k, ta, s_ch))
    if ta > AL_T[-1]:
        issue("B02 t_Al=%.3f mm for k=%g exceeds the Al sweep maximum 2.0 mm" % (ta * 1e3, k))
info("B02 equal-eta check is an identity (eta depends on k*t only); printed, not counted")
rng("t_Al min", K_CU * tcu / 200 * 1e3, 0.78, 1.56); rng("t_Al max", K_CU * tcu / 100 * 1e3, 0.78, 1.56)
rng("sigma_Al (k=100)", 1 - Nf * tcu * K_CU / 100 / W, 0.17, 0.58)
rng("sigma_Al (k=200)", 1 - Nf * tcu * K_CU / 200 / W, 0.17, 0.58)
rng("sigma_Cu", scu, 0.78, 0.80)
for k, ta, sg in smin_viol:
    issue("B02 inconsistency with 3.1 manufacturing limits: N_f=32 with t_Al=%.3f mm (k=%g) gives channel gap %.3f mm < 0.8 mm limit" % (ta * 1e3, k, sg * 1e3))
issue("B02 / B01 check 'substitute t_Al into the B01 function and get equal eta' is true by construction (m depends on k*t only); flagged per instructions") 
