"""Rows C09-C13: OH- diffusion-limited current, bubble coverage, ohmic losses, activation entropy rate,
break-even overpotential for platinum removal.

C09 j_lim = F D c/delta_N; C10 Theta = 0.023 J^0.3, d_eta = b ln(1/(1-Theta)); C11 eta_ohm = J ASR (no check);
C12 J eta/T0 and J eta/T_cell; C13 d_eta_be = e m''/(J tau).  UNSURE constants used as written.
Level: derived (unverified).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gms_core import *

print("Rows C09-C13  (level: derived, unverified)")
head("C09 diffusion-limited current")
D = 5.27e-9
print_inputs(D=D, c=[1000, 6900], delta_N_um=[10, 50, 100], t_OH=0.73)
vals = {}
for c in (1000, 6900):
    for dn in (10e-6, 50e-6, 100e-6):
        j = F_CONST * D * c / dn
        vals[(c, dn)] = j
        print("  c=%5g mol/m3 delta_N=%3.0f um: j_lim=%.4g A/m2 = %.3f A/cm2 ; with migration (1/(1-0.73)): %.3f A/cm2" % (c, dn * 1e6, j, j / 1e4, j / 1e4 / 0.27))
j = vals[(1000, 50e-6)]
rng("1 M, 50 um [A/cm2] (statement: about 1)", j / 1e4, 0.9, 1.1)
rng("1 M range [A/cm2]", min(vals[(1000, d)] for d in (10e-6, 50e-6, 100e-6)) / 1e4, 0.5, 5.0)
rng("1 M range max [A/cm2]", max(vals[(1000, d)] for d in (10e-6, 50e-6, 100e-6)) / 1e4, 0.5, 5.0)
rng("6.9 M range min [A/cm2]", min(vals[(6900, d)] for d in (10e-6, 50e-6, 100e-6)) / 1e4, 3.5, 35)
rng("6.9 M range max [A/cm2]", max(vals[(6900, d)] for d in (10e-6, 50e-6, 100e-6)) / 1e4, 3.5, 35)
info("C09", "hand range 0.5-5 for 1 M spans delta_N = 100..10 um: j(100 um)=%.2f, j(10 um)=%.2f A/cm2 (exact end points of the range)" % (vals[(1000, 100e-6)] / 1e4, vals[(1000, 10e-6)] / 1e4))

head("C10 bubble coverage")
B05 = R_GAS * 298.15 / (0.5 * F_CONST)
for Jv in (1e3, 1e4, 2e4):
    th = 0.023 * Jv ** 0.3
    ok = 0 < th < 1
    print("  J=%g A/m2: Theta=%.4f (%s)  d_eta: %.2f mV (b=0.05139), %.2f mV (b=0.01737)" % (Jv, th, "in (0,1)" if ok else "OUT OF (0,1)", B05 * math.log(1 / (1 - th)) * 1e3, 0.01737 * math.log(1 / (1 - th)) * 1e3))
    check("C10 Theta in (0,1) at J=%g" % Jv, ok, "Theta=%.4f" % th)
th = 0.023 * 1e4 ** 0.3
rng("Theta at 1e4 A/m2", th, 0.34, 0.38)
rng("d_eta (b=0.05139) mV", B05 * math.log(1 / (1 - th)) * 1e3, 21, 25)
rng("d_eta (b=0.01737) mV", 0.01737 * math.log(1 / (1 - th)) * 1e3, 7, 9)
rng("Theta at 1e4 vs outside range 0.2-0.6", th, 0.2, 0.6)
th2 = 0.023 * 2e4 ** 0.3
info("C10 note", "Theta(2e4 A/m2)=%.3f; formula is for flat electrodes in stagnant electrolyte, applied to foam as an extrapolation" % th2)

head("C11 ohmic losses (no check)")
for lab, asrs in (("acid membrane", (0.10, 0.15, 0.20)), ("alkaline diaphragm + gap", (0.15, 0.25, 0.30))):
    print("  %s: " % lab + ", ".join("ASR=%.2f ohm cm2 -> %.3f V" % (a, 1.0 * a) for a in asrs))
info("C11", "one multiplication; no check available (spec says so)")

head("C12 activation entropy rate per m2")
Tc = 353.15
Jm = 1e4
print("  T0=%.2f K, T_cell=%.2f K, T0/T_cell=%.5f" % (T0, Tc, T0 / Tc))
for eta in (0.001, 0.05, 0.10, 0.145, 0.30):
    s0, sc = Jm * eta / T0, Jm * eta / Tc
    print("  eta=%.3f V: J eta = %.1f W/m2; J eta/T0 = %.4f W/K/m2; J eta/T_cell = %.4f W/K/m2; ratio %.5f; fraction of reversible power J*1.229 V = %.4f" % (eta, Jm * eta, s0, sc, sc / s0, eta / 1.229))
rng("eta=0.1 V: J eta [W/m2]", Jm * 0.1, 999.9, 1000.1)
rng("eta=0.1 V: J eta/T0 [W/K/m2]", Jm * 0.1 / T0, 3.34, 3.36)
check("C12 ratio = T0/T_cell = 0.844 (identity; not counted)", False, "printed only") if False else info("C12 ratio identity", "ratio equals T0/T_cell = %.5f by construction; not counted" % (T0 / Tc))
issue("C12 check (ratio = T0/T_cell) is an identity: the ratio of two expressions with the same numerator; flagged per instructions, not counted")

head("C13 break-even overpotential difference for removing Pt")
tau = 1.44e8
Jm = 1e4
print_inputs(J=Jm, tau_op=tau, e_Pt_MJ_per_kg=[1.0e5, 2.4e5, 3.0e5], m_g_per_m2=[0.5, 3.0, 5.0], d_eta=[0.01, 0.05, 0.1])
for e in (1.0e5, 2.4e5, 3.0e5):
    for m in (0.5, 3.0, 5.0):
        Eper = e * 1e6 * m * 1e-3     # J/m2
        deb = Eper / (Jm * tau)
        pb = ", ".join("%.3g V -> %.2f d" % (de, Eper / (Jm * de) / 86400) for de in (0.01, 0.05, 0.1))
        print("  e_Pt=%.1e MJ/kg, m=%.1f g/m2: e*m=%.4g MJ/m2; d_eta_be=%.4g mV; payback %s" % (e, m, Eper / 1e6, deb * 1e3, pb))
Eper = 2.4e5 * 1e6 * 3.0e-3
deb = Eper / (Jm * tau)
rng("middle d_eta_be [mV]", deb * 1e3, 0.4, 0.6)
allb = [e * 1e6 * m * 1e-3 / (Jm * tau) * 1e3 for e in (1e5, 2.4e5, 3e5) for m in (0.5, 3.0, 5.0)]
rng("min d_eta_be [mV]", min(allb), 0.03, 1.0)
info("C13 range note", "max d_eta_be over the grid = %.3f mV (hand range 0.03-1.0 mV)" % max(allb))
rng("max d_eta_be [mV]", max(allb), 0.03, 1.0)
rng("payback at 0.1 V, middle [days]", Eper / (Jm * 0.1) / 86400, 7.5, 8.5)
H2 = Jm * tau / (2 * F_CONST) * 241.8e3 / 1e6
frac = Eper / 1e6 / H2
print("  hydrogen energy per m2 over tau_op = %.4g MJ/m2; e*m/that = %.3e" % (H2, frac))
check("C13 magnitude cross-check: e*m ~ 4e-4 of H2 energy (units/magnitude only; shares J, tau)", 3.5e-4 <= frac <= 4.5e-4, "ratio %.3e, H2 energy %.3g MJ/m2" % (frac, H2))
issue("C13 magnitude cross-check shares inputs J and tau_op with the main formula (spec says it checks units and magnitude only); flagged, not independent")
