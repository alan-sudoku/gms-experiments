"""Prompt 6 S4, script 2 of 2: D5/D6 restated for the corrected expansion mismatch (M18).

Level `derived` (unverified). S3 found: Al alloy 22.8e-6 /K minus alumina 8.1e-6 /K = 14.7e-6 /K;
the planner's 7e-6 /K fits a Ni-base or Fe-Cr substrate. Both are kept, each for its own substrate.
Formulas restated from prompt_6_plan.md 2.4 and rows D5, D6. Values at 7e-6 /K are compared with
the saved S2 output (outputs/d5_d7_scale_thresholds.txt, outputs/d6_scale_cracking.txt).

Run: python3 s4_d5_d6_mismatch.py > outputs/s4_d5_d6_mismatch.txt
"""
import math

E_OX = 380e9      # Pa, M17
NU_OX = 0.25      # M17
F_EDGE = 1.12     # M15
E_AL = 73e9       # Pa, M05
SIGF, N0 = 900.0, 5e8
DA = {"7e-6 (planner; Ni-base or Fe-Cr substrate)": 7e-6, "14.7e-6 (Al alloy substrate, S3)": 14.7e-6}
GC = (1.0, 5.0, 20.0, 100.0)            # J/m2, M20
DT = (50.0, 100.0, 200.0, 500.0, 1000.0)  # K (50 and 100 added in S4 for the Al case)


def delta_c(gc, eps):
    return gc * (1.0 - NU_OX) / (E_OX * eps ** 2)


def eps_c(kic_mpa, c):
    return kic_mpa * 1e6 / (F_EDGE * E_OX * math.sqrt(math.pi * c))


def c_cross(kic_mpa, eps):
    return (1.0 / math.pi) * (kic_mpa * 1e6 / (F_EDGE * E_OX * eps)) ** 2


def check(label, val, ref, tol=2e-3):
    ok = abs(val - ref) <= tol * abs(ref)
    print("    S2 check %-44s s4 = %-10.5g S2 = %-10.5g %s" % (label, val, ref, "reproduced" if ok else "DIFFERS"))


print("Prompt 6 S4 script 2: D5/D6 with the corrected expansion mismatch (level derived)")
print()
print("=" * 96)
print("D5: mismatch strain, biaxial scale stress, critical scale thickness delta_c = G_c (1-nu)/(E_ox eps^2)")
print("=" * 96)
tab = {}
for name, da in DA.items():
    print()
    print("Delta alpha = %s /K" % name)
    print("  dT [K]   eps = da*dT   sigma = E_ox eps/(1-nu) [GPa]   delta_c [um] for G_c = 1 / 5 / 20 / 100 J/m2 (eps_mech = 0)   |  with eps_mech = 1.5e-3")
    for dt in DT:
        eps = da * dt
        d0 = [delta_c(g, eps) * 1e6 for g in GC]
        d1 = [delta_c(g, eps + 1.5e-3) * 1e6 for g in GC]
        tab[(da, dt)] = d0
        tab[(da, dt, "mech")] = d1
        print("  %6.0f   %.4e   %8.3f                      %9.4f %9.4f %9.4f %9.4f   |  %8.4f %8.4f %8.4f %8.4f" % (
            dt, eps, E_OX * eps / (1 - NU_OX) / 1e9, d0[0], d0[1], d0[2], d0[3], d1[0], d1[1], d1[2], d1[3]))
print()
check("delta_c (7e-6, Gc 5, dT 1000)", tab[(7e-6, 1000.0)][1], 0.2014)
check("delta_c (7e-6, Gc 5, dT 500)", tab[(7e-6, 500.0)][1], 0.8056)
check("delta_c (7e-6, Gc 100, dT 500)", tab[(7e-6, 500.0)][3], 16.1117)
check("delta_c (7e-6, Gc 1, dT 200)", tab[(7e-6, 200.0)][0], 1.0070)
check("delta_c (7e-6, Gc 5, dT 200, eps_mech)", tab[(7e-6, 200.0, "mech")][1], 1.1734)
r = 14.7e-6 / 7e-6
print()
print("Ratios Al substrate / planner value at the same dT, eps_mech = 0:")
print("  mismatch strain and stress: x %.3f ; delta_c: x %.4f (= 1/%.3f) ; time to spall t_sp = delta_c^2/(2 kp'): x %.5f (= 1/%.2f)" % (
    r, r ** -2, r ** 2, r ** -4, r ** 4))
print("  with eps_mech = 1.5e-3, dT = 200 K: delta_c ratio = %.4f ; dT = 100 K (Al) vs 200 K (planner): %.4f" % (
    tab[(14.7e-6, 200.0, "mech")][1] / tab[(7e-6, 200.0, "mech")][1], tab[(14.7e-6, 100.0, "mech")][1] / tab[(7e-6, 200.0, "mech")][1]))
print("  dT that gives the same mismatch strain as the planner's (7e-6, 200 K): %.1f K for the Al substrate" % (200.0 * 7e-6 / 14.7e-6))
print("NOTE (UNSURE, memory, no source read): dT = 500 and 1000 K are above what an aluminium alloy can see in service")
print("  (2024 solidus about 775 K); those two columns are meaningful for the 7e-6 substrates only.")

print()
print("=" * 96)
print("D6: scale cracking strain eps_c = K_Ic/(f E_ox sqrt(pi c)) against the strain the scale sees")
print("=" * 96)
for b in (-0.102, -0.124):
    sig = SIGF * (2 * N0) ** b
    eps_a = sig * 1e6 / E_AL
    print()
    print("b = %.3f: sigma_a0 = %.3f MPa, cyclic strain amplitude eps_a = %.4e" % (b, sig, eps_a))
    print("  crossover flaw size c_x [um] where eps_c = eps_a, K_Ic = 0.5 / 1 / 2 / 4 MPa sqrt(m): " +
          " / ".join("%.4f" % (c_cross(k, eps_a) * 1e6) for k in (0.5, 1.0, 2.0, 4.0)))
    if abs(b + 0.102) < 1e-9:
        check("c_x K_Ic = 1 (eps_a from sigma_a0 = 108.7)", c_cross(1.0, 108.7e6 / E_AL) * 1e6, 0.7926)
        check("c_x K_Ic = 4", c_cross(4.0, 108.7e6 / E_AL) * 1e6, 12.6810)
        check("eps_c (c = 1 um, K_Ic = 1) [1e-3]", eps_c(1.0, 1e-6) * 1e3, 1.3256)
    dt_eq = eps_a / 14.7e-6
    print("  temperature change at which the Al-alumina mismatch strain equals eps_a: %.1f K (%.1f K with 7e-6)" % (dt_eq, eps_a / 7e-6))
    for dt in (50.0, 100.0, 200.0):
        eps_tot = eps_a + 14.7e-6 * dt
        print("  Al substrate, dT = %3.0f K: eps_th = %.3e, bound eps_a + eps_th = %.3e -> c_x (K_Ic = 0.5 / 1 / 2 / 4) = " % (dt, 14.7e-6 * dt, eps_tot) +
              " / ".join("%.4f" % (c_cross(k, eps_tot) * 1e6) for k in (0.5, 1.0, 2.0, 4.0)) + " um")
print()
print("Native film check: eps_c at c = 0.01 um (10 nm), K_Ic = 0.5 / 1 / 2 / 4: " +
      " / ".join("%.3e" % eps_c(k, 1e-8) for k in (0.5, 1.0, 2.0, 4.0)))
print("  largest strain in the Al table above (b = -0.102, dT = 200 K): %.3e -> below every one of these: %s" % (
    SIGF * (2 * N0) ** -0.102 * 1e6 / E_AL + 14.7e-6 * 200.0,
    SIGF * (2 * N0) ** -0.102 * 1e6 / E_AL + 14.7e-6 * 200.0 < eps_c(0.5, 1e-8)))
print("All values level `derived`; G_c, K_Ic grids and E_ox, nu_ox are unsourced planner values (M17, M19, M20: UNSURE).")
