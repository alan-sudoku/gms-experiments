# Issues, ambiguities, artefacts (prompt 4)

All items are claims at level `derived`.

## Ambiguities in the claims
1. C1 formula is undefined for K_g = 0 (rho = infinity, division by zero) and for K_s = K_g (rho = 1, t_m/(rho-1) divides by zero). Outcome is still consistent (no zero in (0,tw)), but the text should say so. (c1_root_count.py part 1, part 5)
2. C1 literal statement fails in one degenerate class: m = 0 and K_s = K_g gives f'' identically 0 (zero set is the whole interval) and, if also a = 0 and d' = 0, f identically 0 (infinitely many roots). Same for K_g = K_s = 0 with a = 0 and d' = 0 (any m). Needs "f not identically zero" and "m >= 1 or K_s != K_g". (c1 part 5)
3. C1 "zero only when K_s > K_g" is necessary, not sufficient: zero lies in (0,tw) only if m < rho - 1 and m >= 1 (x* = 0 for m = 0). (c1 part 3a coverage: 162 of 564 K_s>K_g>0 cases had the zero inside.)
4. C2 has no content for m = 0 (no boundary). The jump identity is true by construction of d_m' (flagged).
5. C3 "eventually" has no bound in the claim; explicit T given in c3 (from f >= abar tau - Ks sqrt(tau) + d0 - R and f <= abar tau - Ks sqrt(tau) + d0 + Kg sqrt(tw)/4). T can be astronomically large when |abar| or K_s is tiny.
6. C4 says "strictly decreasing" for tau >= tw; true only for K_g > 0 and s in (0, tau]. For K_g = 0, h == 0. For s > tau h is flat (m = 0). The "shorter tw never favourable" conclusion holds weakly on all s > 0.
7. C4/C5 tie convention matters: m = floor(tau/tw) makes m R left-continuous in tw (value at the tie is the higher one). The alternative convention (m = ceil(tau/tw) - 1) is also monotone but gives different f at ties by R_g.
8. C5 requires the box to be a product of independent intervals (no coefficient depends on tw) and lambda to enter as -lambda only. Not tested: coefficients coupled to tw. UNSURE.

## Float64 artefacts and solver tolerances
1. Tie hazard: for tau = fl(j*tw), floor(tau/tw) != j in 10825 of 200000 random (tw, j) (c4 part 3). m R then changes by one R_g, so a float solver flips the verdict side by R_g at an intended tie. Ties must be handled with a tolerance or with exact/integer arithmetic for j.
2. Cancellation in dt = tau - m*tw: tau one ulp above j*tw = 1e10 with tw = 1e9 gives dt = 1.907e-6, so K_g*sqrt(dt) = K_g*1.38e-3 is pure rounding noise (c4 part 3); error in f of order K_g*sqrt(ulp(tau)). Similar at tw = 0.1, m = 3: f differs by 1.6e-8 from the exact value (c2 part 3 line 'tw=0.1').
3. m = 0, K_s = K_g: f = a*dt + d' exactly, but the float expression K_g*sqrt(dt) - K_s*sqrt(dt) with tiny a (7e-146 case) absorbs a*dt: f evaluates to exactly 0 at all 40000 grid points (8 hypothesis cases reached this). Compute (K_g - K_s)*sqrt(dt) or branch on K_s == K_g. (c1 part 3b "FLOAT ARTEFACT" counter)
4. Quadratic-formula T for abar < 0 with tiny |abar|: the textbook root (-K + sqrt(K^2 + 4|abar|c))/(2|abar|) returned 0 at 60 digits when |abar| ~ 1e-263. Use y = 2c/(K + sqrt(K^2 + 4|abar|c)). (found while writing c3; fixed in script)
5. c5 part 4: no float64 ordering violation f_pess >= f_any >= f_opt in the 3000 sampled cases. This is weak evidence (ties computed from exact Fractions then rounded); the hazard in item 1 is the realistic route to a violation.

## Failed or vacuous checks
1. c5 coverage "degenerate coord" is 2994/3000 (any of 7 coordinates degenerate almost always); fully non-degenerate boxes appear in about 1/128 of draws. "tw distinct" 923 and "pess wins" 952 and "opt wins, pess loses" 1616 are adequate, but a fully non-degenerate box is under-sampled. Not a failure, a thin spot.
2. c1 3-root examples are rare under random sampling: 6 of 60000 in the first search; the tuned hypothesis mode (forcing x* < 1 and f'(x*) < 0 < f'(1)) reaches 37 examples. Count 4 never occurred.
3. Identity checks flagged as true by construction: c2 SymPy jump; c3 decomposition f = abar tau + ...; c4 dh/ds algebra and continuity at s = tau/k are algebra (proof), not numeric tests.
4. c3 part 5 uses tw := (sqrt tw)^2 in float and a = float(-(R+Kg sqrt tw)/tw), so abar is only 0 up to 1e-16 relative; a margin |a|*2^-52*tau is allowed. The exact abar = 0 case is established by the SymPy and Fraction checks in part 4 (K_s = 0) and by the bound proof (K_s > 0).
