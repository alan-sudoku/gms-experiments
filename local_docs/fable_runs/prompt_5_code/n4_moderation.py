#!/usr/bin/env python3
"""Row N4 (claim G3.8): moderation lever.

(1) 1/v gain factor sqrt(E/0.0253 eV) for sigma(E)/sigma0 = sqrt(0.0253/E) at E = 1 eV, 1 keV, 100 keV, 1 MeV (inverse = cross section ratio).
(2) mean lethargy gain per collision xi(A) = 1 + ((A-1)^2/(2A)) ln((A-1)/(A+1)) (xi = 1 for A = 1) and collisions from 2 MeV to 0.0253 eV
    = ln(E1/E2)/xi for A = 1, 2, 12, 56.
No LOOKUP. The comparison values 18 (H), 25 (D), 115 (C) are the plan's 'published textbook values (Lamarsh and Baratta 2001)'
quoted in the spec; the book itself was NOT consulted (UNSURE; they are taken from the spec as given). Level `derived`.
"""
import math
from scipy.optimize import brentq
E0 = 0.0253
FAILS = []
def check(name, ok, detail):
    print("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok: FAILS.append(name)
def xi(A):
    if A == 1: return 1.0
    return 1 + (A-1)**2/(2*A)*math.log((A-1)/(A+1))
print("N4 inputs: E0 = 0.0253 eV; E in {1 eV, 1 keV, 100 keV, 1 MeV}; A in {1, 2, 12, 56}; E1 = 2 MeV")
print("\n(1) 1/v gain (sigma(E0)/sigma(E) = sqrt(E/E0)); plan expects 6.3, 199, 1990, 6290")
for E, exp in ((1.0, 6.3), (1e3, 199), (1e5, 1990), (1e6, 6290)):
    g = math.sqrt(E/E0); r = math.sqrt(E0/E)
    print("  E=%-8g eV: sigma/sigma0 = %.4e, gain = %.5g  (plan %.4g, dev %+.2f%%)" % (E, r, g, exp, 100*(g/exp-1)))
    check("gain at %g eV matches plan to 1%%" % E, abs(g/exp-1) < 0.01, "%.5g vs %g" % (g, exp))
print("\n(2) xi and collisions from 2 MeV to 0.0253 eV: ln(E1/E2) = %.4f" % math.log(2e6/E0))
PUB = {1: 18, 2: 25, 12: 115}
for A in (1, 2, 12, 56):
    x = xi(A); n = math.log(2e6/E0)/x
    s = "  A=%-3d xi = %.5f  collisions = %.2f" % (A, x, n)
    if A in PUB: s += "   published %d, diff %+.2f" % (PUB[A], n-PUB[A])
    print(s)
    if A in PUB: check("collisions A=%d within +-1 of %d" % (A, PUB[A]), abs(n-PUB[A]) <= 1, "%.2f" % n)
print("  limit check xi(A -> 1+): A = 1+1e-6 gives %.6f (should tend to 1)" % xi(1+1e-6))
print("  large-A check: xi(56) vs 2/(A+2/3) = %.5f vs %.5f" % (xi(56), 2/(56+2/3)))
check("xi(56) within 1% of the large-A approximation 2/(A+2/3)", abs(xi(56)/(2/(56+2/3))-1) < 0.01, "")
print("  Energy at which sigma/sigma0 = 1e-3.. (extra): sqrt(E0/E) = 1e-3 at E = %.4g eV" % (E0/1e-6))
print("  note: the 1/v gain is a property of the cross-section law for a 1/v absorber only; resonance absorbers (Cd, Gd) are not 1/v above their resonances, see N2.")
print("FAILED CHECKS:", FAILS if FAILS else "none")
