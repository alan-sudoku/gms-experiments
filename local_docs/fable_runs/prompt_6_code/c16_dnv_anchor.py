"""C16 welded-steel code anchor: air versus free corrosion, DNV-RP-C203 curve D.

Spec row: C16.  L03 constants READ from DNV-RP-C203 (April 2010 edition, rules.dnv.com) Table 2-1
(air, curve D: m1=3.0, log a1=12.164, m2=5.0, log a2=15.606, fatigue limit at 1e7 cycles 52.63 MPa)
and Table 2-3 (free corrosion, curve D: log a = 11.687, m = 3, all cycles).  The edition differs from the
planner's 'edition UNSURE'; the 2016 DNVGL edition was not opened.  Raw file saved (gitignored) in data/raw/dnv2010.pdf.
N_air = 10^log a1/Ds^3 above the knee stress, 10^log a2/Ds^5 below; N_fc = 10^log a_fc/Ds^3; factor N_air/N_fc.
"Real check on the looked-up constants": both air branches give 1e7 cycles at the knee within 1 %.
"""
la1, la2, lfc, knee = 12.164, 15.606, 11.687, 52.63
def N_air(ds): return 10 ** la1 / ds ** 3 if ds >= knee else 10 ** la2 / ds ** 5
def N_fc(ds): return 10 ** lfc / ds ** 3
exp = {100: 3.0, 80: 3.0, 52.63: 3.0, 40: 5.2, 30: 9.2, 20: 20.7}
print("Branch consistency at knee %.2f MPa: 10^log a1/knee^3 = %.5e, 10^log a2/knee^5 = %.5e (target 1e7)" % (knee, 10 ** la1 / knee ** 3, 10 ** la2 / knee ** 5))
for nm, v in (("m=3 branch", 10 ** la1 / knee ** 3), ("m=5 branch", 10 ** la2 / knee ** 5)):
    print("   %s: %.4e, diff from 1e7 %+.3f %% -> %s" % (nm, v, (v / 1e7 - 1) * 100, "PASS" if abs(v / 1e7 - 1) <= 0.01 else "FAIL"))
print("Factor N_air/N_fc (= 10^(12.164-11.687) = %.4f above knee):" % 10 ** (la1 - lfc))
for ds, e in exp.items():
    f = N_air(ds) / N_fc(ds)
    print("   Ds=%-6g N_air=%.4e N_fc=%.4e factor=%.3f expected %.1f diff %+.2f%% %s" % (ds, N_air(ds), N_fc(ds), f, e, (f / e - 1) * 100, "PASS" if abs(f / e - 1) <= 0.02 else "FAIL"))
print("Note: 'factor 3.0 at and above the knee' is the constant 10^(delta log a); it is the same two tabulated numbers, an arithmetic identity of the lookup, not an independent check. Branch consistency at the knee is the real check.")
print("Note: the knee in the table is 'fatigue limit at 1e7 cycles' = 52.63 MPa in a branch-consistent sense only; free-corrosion curve has no knee.")
