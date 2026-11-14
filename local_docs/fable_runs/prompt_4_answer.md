# Prompt 4 answer: solver lemma red-team (C1-C5)

Level: everything here is `derived` (unverified); passing property tests are evidence, not proof. Scripts are in `local_docs/fable_runs/prompt_4_code/` (run with `<gms-local>/.venv/bin/python <script>`), saved stdout in `prompt_4_code/outputs/`. Conventions as in the brief (m = floor(tau/tw), ties belong to segment j, win = f < 0, lambda enters as -lambda).

## Summary

| Claim | Verdict | Decisive script |
|---|---|---|
| C1 f'' has <= 1 zero, at most 3 roots per segment | holds with conditions (degenerate f'' == 0 / f == 0 cases; formula undefined at K_g = 0 and K_s = K_g) | c1_root_count.py |
| C2 jump of -R_g at each boundary | holds (m >= 1; true by construction of d_m') | c2_boundary_jump.py |
| C3 long-run verdict from abar | holds (explicit T given; ties and tiny-|abar| float caveats) | c3_long_run.py |
| C4 h strictly decreasing, m R non-increasing | holds with conditions (K_g > 0, s <= tau for strictness; weak otherwise) | c4_tw_monotone.py |
| C5 interval screening | holds with conditions (independent product box; derived corner directions) | c5_interval_screening.py |

No counterexample to the intended content of any claim. Literal-statement failures are listed under C1 only. Shared issues: `prompt_4_code/outputs/issues.md`.

## C1

Proof sketch (c1 part 1, SymPy): f'' = -K_g/(4 dt^{3/2}) + K_s/(4 (t_m+dt)^{3/2}) = phi/(4 dt^{3/2} (t_m+dt)^{3/2}) with phi = K_s dt^{3/2} - K_g (t_m+dt)^{3/2}. Zero iff (dt/(t_m+dt))^{3/2} = K_g/K_s; psi(dt) = dt/(t_m+dt) is strictly increasing for t_m > 0, so at most one zero, at dt = t_m/(rho-1) (SymPy check: residual 0). f'' < 0 before it (K_g term dominates), > 0 after; f'(0+) = +infinity for K_g > 0. So f' decreases then increases: at most 2 zeros of f', at most 3 monotone pieces of f, at most 3 roots.

Maximum reached: 3. Concrete 3-root example, tw = 1 (scale-invariant, dt = tw x), m = 1, a = 0.27462901204136775, K_g = 0.06913552752653546, K_s = 0.8205556354592521, d' = 0.5436108308140535. mp-60 signs of f at x = 0, x_max = 0.0836947300, x_min = 0.6798047735, 1-1e-12: -, +, -, + (values -0.00231579, 0.00702195, -0.00156347, 0.00156347); roots 0.00129908433342134, 0.45843123476155969, 0.904736521823163779 (output "(4)" lines of c1_root_count.txt). Here x* = m/(rho-1) = 0.2379 lies between the two critical points, as expected. A variant with f(0) = 0 exactly (root at dt = 0, one in (x_max,x_min), one in (x_min,1)) is also confirmed at 60 digits (m = 2, a = 0.3343930682806595, K_g = 0.011893402175123942, K_s = 1.0611111269210844). Count 4 never occurred: 60000 tuned plus 60000 generic searches (max 3 and 2), 3000 hypothesis examples for the root bound (37 with 3 roots, 126 with 2), 3000 for the f'' zero property (162 with the zero inside (0,tw)).

Edge cases:
- K_g = 0: rho = infinity, x* = 0 not in (0,tw); K_s > 0 gives f convex, at most 2 roots. Formula undefined (division by zero).
- K_s = 0, K_g > 0: f concave, at most 2 roots.
- K_s = K_g, m >= 1: rho = 1, formula undefined, f'' < 0 on (0,tw), no zero. Consistent with the claim.
- K_s = K_g, m = 0: f'' is identically 0 (zero set is the whole interval), f = a dt + d' linear. Literal claim "at most one zero" false. If also a = 0 and d' = 0, f is identically 0.
- K_g = K_s = 0: f linear in dt; f identically 0 if a = 0 and d0 + m R_g = 0.
- m = 0, K_s > K_g: x* = 0, outside the open interval: f convex, at most 2 roots.
- a = 0: no effect on the root bound (a enters f' only as a constant).
- tau < tau_w: only m = 0, covered by the m = 0 rows.
- The zero lies in (0,tw) only if m >= 1 and m < rho - 1; "only when K_s > K_g" is necessary, not sufficient.

Restatement: "If f is not identically zero, then f has at most 3 roots in [0,tw) (counting the endpoint dt = 0). For K_s > K_g > 0 and m >= 1, f'' has exactly one zero on (0,inf), at t_m/(rho-1); it lies in (0,tw) iff m < rho - 1. In all other cases with (K_g, K_s) not equal, f'' has no zero in (0,tw). If m = 0 and K_s = K_g, or K_g = K_s = 0, f is linear in dt."

Float note: for m = 0, K_s = K_g with tiny a, the float expression cancels to exactly 0 (issues.md, artefact 3).

## C2

True: segment m-1 at dt = tw minus segment m at dt = 0 equals -R_g (SymPy, symbolic m). This is an identity by construction of d_m' (flagged); the non-trivial check is the hypothesis test (2500 examples, exact Fractions, mp-60) of the global evaluator at t_m - 1e-40 tw versus t_m, which agrees (coverage: K_g = 0: 1166, R = 0: 1149, m >= 1e6: 512, tw >= 1e3: 897). Holds for m >= 1 only (no boundary at m = 0). Continuous parts (a, K_g, K_s) do not jump; f at t_m is the upper value, consistent with the tie convention. Float64: error at t_m of order K_g sqrt(ulp) (e.g. 5.7e-6 at tw = 1e9, m = 1e7; 1.6e-8 at tw = 0.1, m = 3), see c2 part 3.

## C3

Proof (c3 part 1, SymPy, closed form): with tau = m tw + dt, f = abar tau + r(dt) - K_s sqrt(tau) + d0, r(dt) = (a-abar) dt + K_g sqrt(dt) = -(R/tw) dt + K_g (sqrt(dt) - dt/sqrt(tw)). Since 0 <= sqrt(dt) - dt/sqrt(tw) <= sqrt(tw)/4, we get -R < r <= K_g sqrt(tw)/4, hence

abar tau - K_s sqrt(tau) + d0 - R <= f <= abar tau - K_s sqrt(tau) + d0 + K_g sqrt(tw)/4.

(Bounds verified at 3000 random points, exact ties included; coverage K_g = 0: 1402, tie: 1370.) Explicit T, with y = sqrt(tau):
- abar > 0, loses for all tau > T = y+^2, y+ = (K_s + sqrt(K_s^2 - 4 abar (d0 - R)))/(2 abar), or T = 0 if the discriminant is negative.
- abar < 0, wins for all tau > T = y^2, y = 2c/(K_s + sqrt(K_s^2 + 4|abar|c)), c = d0 + K_g sqrt(tw)/4 (T = 0 if c <= 0). Use this stable form; the textbook root returns 0 at 60 digits for |abar| ~ 1e-263.
- abar = 0, K_s > 0: wins for all tau > (max(c,0)/K_s)^2. Holds for every d0, R_g, K_g (including K_g = 0, R_g = 0). T is huge when K_s is small (d0 = 1e6, K_s = 1e-6 gives T about 1e24 s).
Hypothesis checks of the T verdicts at tau >= T and at exact ties above T: 3000 examples each (loses 1992, wins 961 cases; K_g = 0: 1373, R = 0: 1559, ties 1296).

abar = 0, K_s = 0: f is exactly periodic with period tw: SymPy f_{m+1}(dt) - f_m(dt) = 0 with a = -(R+K_g sqrt(tw))/tw, and 4000 exact Fraction instances (tw = q^2, dt = r^2, m in {0,1,2,17,1e6}) with 0 non-periodic. Periodic does not mean always winning or never: example tw = 1, K_g = 1, R = 0, a = -1, d0 = -1/8 has f = 0.0625 > 0 at sqrt(dt) = 1/4 and f = -0.125 < 0 at dt = 0 in every segment.

Edge cases: strict inequality at the permanent verdict; ties f = 0 not wins. a = 0, K_g = 0, R_g = 0 all covered (abar = 0 needs R = 0 then, K_g = 0). Claim holds as stated.

## C4

Proof (c4 part 1, SymPy): on an interval of constant m, dh/ds = K_g m/2 (1/sqrt(s) - 1/sqrt(r)), r = tau - m s with 0 <= r < s; so dh/ds < 0 for m >= 1, K_g > 0 (on r = 0 the one-sided derivative is -infinity). At s = tau/k, h using m = k and using m = k-1 both equal K_g sqrt(k tau): h is continuous across every change of m (SymPy: difference 0). Hence h is strictly decreasing on (0,tau] for K_g > 0; m = floor(tau/s) is non-increasing in s, so m R_g is non-increasing, with a downward jump of R_g at each s = tau/k as s increases (left-continuous). Numeric (exact Fractions, mp-60, 3000 examples each): h(s1) >= h(s2) for s1 < s2 <= tau (strict gap > 1e-30 relative in 1051 cases; ties s = tau/k in 1880; m >= 1000 in 2099); continuity at tau/k at 1e-30 relative offsets (3000); f(tau; s1) >= f(tau; s2) for all tau including s2 > tau (696 cases).

Edge cases: K_g = 0 gives h == 0, so "strictly" fails, weak monotonicity holds. For s >= tau, h = K_g sqrt(tau) flat (m = 0, or m = 1 with r = 0): strict only on (0,tau]. Conclusion "shorter tw never favourable" holds weakly for all tw > 0. Tie: at s = tau/k exactly, m = k (higher). Float hazard (c4 part 3): with tau = fl(j*tw), floor(tau/tw) != j in 10825 of 200000 draws, e.g. tw = 0.0367344509464381, j = 960439, tau = 35281.199332546064 (the exact floor of the double values is 960438; float gives j). One wrong m changes m R_g by R_g, so float solvers flip the verdict at intended ties. dt = tau - m tw cancels: at tau one ulp above 1e10 with tw = 1e9, dt = 1.907e-6 (K_g sqrt(dt) noise 1.4e-3 K_g).

Restatement: "For K_g > 0 and tau >= tw, h is strictly decreasing in s on (0,tau] and constant for s >= tau; for K_g = 0, h == 0. m R_g is non-increasing in s on (0,inf). Hence f(tau) is non-increasing in tw for every tau >= 0."

## C5

Derivatives (c5 part 1, SymPy, within a segment): df/da = tau >= 0, df/dK_g = sqrt(dt) + m sqrt(tw) >= 0, df/dK_s = -sqrt(tau) <= 0, df/dd0 = 1, df/dR_g = m >= 0, df/dlambda = -1, df/dtw = m K_g (1/(2 sqrt(tw)) - 1/(2 sqrt(dt))) <= 0 within a segment, and across a change of m the K_g part is continuous while m R_g jumps down (C4). So pointwise in tau, f is coordinatewise monotone.

Pessimistic corner (largest f): a max, K_g max, K_s MIN, d0 max, R_g max, tw MIN, lambda MIN. Optimistic corner: a min, K_g min, K_s MAX, d0 min, R_g min, tw MAX, lambda MAX. (K_s, lambda, tw run opposite to a naive reading.) Since f_pess >= f_any >= f_opt pointwise, f_pess < 0 implies f_any < 0 implies f_opt < 0: the inclusions hold for the strict win set; f = 0 is not a win in any of them.

Tests (exact, mp-60): single-coordinate monotonicity (3000 examples, per coordinate 311-769; ties for either tw: 589/468/564, ulp neighbours 447, tw changes crossing a segment boundary 260); box ordering and inclusion (3000 examples; random tau 857, tau = j tw_pess 511, tau = j tw_opt 329, tau = j tw_any 310, ulp neighbours 287, tau = 0: 310, tau < tw_pess: 396, vertices 1196; pess wins 952, opt wins while pess loses 1616). No violation. Thin spot: nearly every box had a degenerate coordinate (see issues.md).

Does C5 for tw follow from C4? Yes, given two additions. f depends on tw only through K_g [m sqrt(tw) + sqrt(tau - m tw)] + m R_g, and C4 gives both parts non-increasing in tw. (i) C4 is stated for tau >= tw; for tw > tau, m = 0 and the term equals its value at tw = tau, so f is flat there, and monotonicity holds on all tw > 0 (c4 prop 2c). (ii) C5 additionally needs the six other coordinatewise monotonicities (derivatives above) and a product box with independent coefficients; if any coefficient is tied to tw (e.g. K_g or a re-fitted per tw), C5 can fail. UNSURE: not tested.

Float64 (c5 part 4): no ordering violation among the sampled cases (weak evidence). Realistic route to violation: the tie hazard above.

Restatement: "f is coordinatewise non-decreasing in a, K_g, d0, R_g and non-increasing in K_s, lambda, tw (pointwise in tau >= 0, all tw > 0, K_g, R_g >= 0, ties as m = floor(tau/tw)). For a product box of independent intervals, the corner (a max, K_g max, K_s min, d0 max, R_g max, tw min, lambda min) gives f_pess >= f >= f_opt, so win set(pess) is a subset of win set(any) is a subset of win set(opt)."

## Identity checks (true by construction, not evidence)

- c2 part 1: f(t_m^-) - f(t_m) = -R_g follows from the definition of d_m'.
- c3 part 1: f = abar tau + (a-abar) dt + K_g sqrt(dt) - K_s sqrt(tau) + d0 is algebra.
- c1 part 1 and c4 part 1: SymPy confirms f'', its zero, dh/ds and the equality of h at s = tau/k with m = k and m = k-1 as algebra. These are proofs of the algebra, not tests of the claims.
- c3 part 4 (K_s = 0, abar = 0 periodicity): a symbolic identity; the Fraction run is an independent confirmation.

## Not settled

- C1: no proof that the 3-root window is nonempty over all parameter classes; existence shown by example, count 4 excluded by proof not by test. Behaviour when a, K_g, K_s depend on tw or on each other: untested.
- C3: T bounds are valid but not tight; no minimal T.
- C5: coefficients coupled to tw (UNSURE), and the solver's actual interval-screening code are untested; float64 ordering evidence is weak.
- Alternative tie convention (m = ceil(tau/tw) - 1) was not tested, only argued monotone.
- Any statement about solver tolerances is limited to the magnitudes listed in issues.md.
