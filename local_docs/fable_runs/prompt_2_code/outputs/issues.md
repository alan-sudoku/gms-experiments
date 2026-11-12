# Issues (no row failed a sanity check or tolerance; the items below are ambiguities)

All results are claims at level `derived` (unverified).

1. R14: the row says to build the left side "literally from the prompt's formulas". Those formulas are in a file I was not told to read. I read claim C5 (plan lines 51-54) and C6, and built the left side stage by stage from the structure they describe: unit 0 virgin, m replacement units each extracting (1-R_i) virgin, m+1 units each paying conversion, remelt R_i*w_rm, transport and manufacturing, tooling+components once over N_units. This is a reconstruction, not the literal prompt text, so the R14 PASS (max rel diff 5.9e-16; multiplier check 8.5e-16) tests C5 against my reconstruction. UNSURE whether it matches the prompt. Unit handling (kJ to J, MJ/kg to J/kg) was my choice.
2. R13: "choice C equals choice B" uses choice labels the row does not define. I read claim C4 (plan lines 40-50). I implemented choice C as make-up charged CExC-b plus dispersion charged b, and choice B as F + (m+1)(1-R)nb. Both are algebraically the same expression as the row's two sides, so the check is close to tautological. The labels may differ from the spec author's.
3. R7 uses r_el = 3.0 (row text) while R3 uses r_el = 1/eta_el = 2.5. Used as written, not reconciled.
4. R3: "cumulative loss" is not defined in the row. I took it as loss_gen + loss_smelt = 1030 kJ/mol.
5. Tolerances not given in the spec, assumed by me and printed as "assumed" in the outputs: R32 E vs pi^4/15 (1e-5); R33 energy fraction (0.001); R34b eps*sig*Ts^4 (0.1 W/m2) and sig*T0^4/3 (0.01 W/m2); R26 bO2_std uses the row's +/-5 J/mol.
6. R30: "deep-space sink" taken as Tc = 0 K from R29; unrounded R29 values were used.
7. R20 and R21 booleans/counts: R21 second count was 2122 (> 0), first count 0.
