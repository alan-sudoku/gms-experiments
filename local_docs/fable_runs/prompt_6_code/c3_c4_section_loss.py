"""C3 recession-through time / rho / mass-loss class and C4 coupled life (closed form).

Spec rows: C3, C4 (needs C1). Inputs M02-M04, M06, M08.
Assumptions: p = 1 for wall (membrane load), p = 2 for round strut (axial load), q = p*m, m = 1/0.102.
Wall: t_c = h0/(n_s r); strut: t_c = d0/(2 r). nu grid {0.1, 1, 10} Hz.
C4 hand-value checks use the planner's tolerance 2 %; the hand values are the planner's own arithmetic.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_common import *

H = [0.3e-3, 1e-3, 3e-3]; R = [1, 3, 10]; NU = [0.1, 1, 10]
print("C3: recession-through times (yr)")
exp_tc = {(0.3,1):150,(0.3,3):50,(0.3,10):15,(1,1):500,(1,3):166.7,(1,10):50,(3,1):1500,(3,3):500,(3,10):150}
bad = 0
for ns in (1, 2):
    for h in H:
        row = []
        for r in R:
            tc = t_c_years("wall", h, r, ns)
            row.append(tc)
            if ns == 2:
                e = exp_tc[(round(h*1e3,1) if h<1e-3 else round(h*1e3), r)]
                if abs(tc/e-1) > 0.005: bad += 1
        print("  wall n_s=%d h0=%.1f mm: t_c(r=1,3,10) = %s" % (ns, h*1e3, ", ".join("%.4g" % v for v in row)))
for d in H:
    print("  strut d0=%.1f mm: t_c(r=1,3,10) = %s" % (d*1e3, ", ".join("%.4g" % t_c_years("strut", d, r) for r in R)))
print("  planner n_s=2 values reproduced within 0.5%%: %s" % ("PASS" if bad == 0 else "FAIL (%d)" % bad))

print("\nC3: rho = tau0/t_c at 1 Hz for wall n_s=2")
rhos = [tau0_years(1.0)/t_c_years("wall", h, r, 2) for h in H for r in R]
print("  min %.5f, max %.5f (expected 0.0106 .. 1.056) -> %s" % (min(rhos), max(rhos),
      "PASS" if abs(min(rhos)/0.0106-1) < 0.005 and abs(max(rhos)/1.056-1) < 0.005 else "FAIL"))
print("\nC3: mass-loss rate r*rho_m and ISO 9223 class (M08)")
for r in R:
    ml = mass_loss_g_m2_yr(r)
    print("  r=%g um/yr: %.3f g/(m2 yr) -> class %s" % (r, ml, iso_class(ml)))
print("  1..10 um/yr = %.2f .. %.2f g/(m2 yr) (expected 2.8 .. 27.8)" % (mass_loss_g_m2_yr(1), mass_loss_g_m2_yr(10)))
print("  class limits M08 are UNSURE (memory; ISO 9223 table not read)")

print("\nC4: coupled life, closed form; q = p*m, m = %.4f" % M_EXP)
print("  columns: geometry, nu, r, t_c[yr], rho, tau_c[yr], F_cur, F_min")
tab = {}
for kind, p, sizes, nss in (("wall", 1, H, (1, 2)), ("strut", 2, H, (1,))):
    q = p * M_EXP
    for ns in nss:
        for h in sizes:
            for nu in NU:
                for r in R:
                    tc = t_c_years(kind, h, r, ns)
                    rho = tau0_years(nu)/tc
                    x, fc, fm = c4(rho, q)
                    tab[(kind, ns, round(h*1e3,1), nu, r)] = (tc, rho, float(x)*tc, float(fc), float(fm))
                    print("  %-5s n_s=%d h0/d0=%.1f nu=%-4g r=%-2g tc=%9.4g rho=%9.5f tau_c=%9.5g F_cur=%8.4f F_min=%8.4f" %
                          (kind, ns, h*1e3, nu, r, tc, rho, float(x)*tc, float(fc), float(fm)))

print("\nC4 hand-value comparison (2 %% tolerance)")
checks = [
 (("wall",2,0.3,1,1),1.47),(("wall",2,0.3,1,3),2.26),(("wall",2,0.3,1,10),4.54),
 (("wall",2,1.0,1,1),1.15),(("wall",2,1.0,1,3),1.42),(("wall",2,1.0,1,10),2.26),
 (("wall",2,3.0,1,1),1.05),(("wall",2,3.0,1,3),1.15),(("wall",2,3.0,1,10),1.47),
 (("wall",1,3.0,1,1),1.026),(("wall",1,3.0,1,10),1.24),
]
for k, e in checks:
    v = tab[k][3]
    print("  %-26s F_cur=%.4f expected %.3f diff %+.2f%%  %s" % (k, v, e, (v/e-1)*100, "PASS" if abs(v/e-1) <= 0.02 else "FAIL"))
k = ("strut",1,0.3,1,10)
tc, rho, tcl, fc, fm = tab[k]
for name, v, e in (("tau_c [yr]", tcl, 2.25), ("F_cur", fc, 7.0), ("F_min", fm, 6.7)):
    print("  strut 0.3 mm r=10 1Hz %-10s %.4f expected %.2f diff %+.2f%%  %s" % (name, v, e, (v/e-1)*100, "PASS" if abs(v/e-1) <= 0.02 else "FAIL"))
print("  (t_c strut = %.3f yr, rho = %.4f)" % (tc, rho))
print("\nC4 sanity: tau_c < t_c and tau_c <= tau0 everywhere on grid:",
      all(v[2] < v[0] and v[2] <= tau0_years(nu)*(1+1e-12) for (kk, v), nu in [((a,b), a[3]) for a,b in tab.items()]))
print("C4 independent numerical verification of the closed form: see C5 (c5_rk4_verify.py).")
