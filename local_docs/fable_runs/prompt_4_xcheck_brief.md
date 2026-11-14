# Prompt 4 cross-check brief: independent solver (`sonnet`)

Context file (`local_docs/`, never cited by the spec). Written 2026-11-14 by the orchestrator. User decision D6 (2026-11-14, `prompt_4_synthesis.md`): the project's own pure-Python checks must be cross-checked by another solver (SciPy, numpy). This run re-computes the decisive Prompt 4 results with SciPy/numpy as an independent numerical oracle. SciPy 1.18.1, numpy, sympy, mpmath, hypothesis are in the project `.venv`.

## Inputs (read only these)

- The fenced block in `local_docs/fable_questions.md`, section "Prompt 4 (optional): solver lemma red-team" (the claims C1–C5 and f).
- `local_docs/fable_runs/prompt_4_brief.md`, section "Definitions the block leaves implicit" (conventions: segment [t_m, t_{m+1}), tie τ = j·τ_w belongs to segment j, λ_ℰ inside d₀ with ∂f/∂λ_ℰ = −1, win means f < 0).
- `local_docs/fable_runs/prompt_4_synthesis.md`, the "Result" table only (the claims as restated, which you are cross-checking).
- The saved outputs `local_docs/fable_runs/prompt_4_code/outputs/c1_root_count.txt` and `prompt_4_review_code/outputs/r1_c1_exact_roots.txt`, only to take the reference numbers you compare against (3-root example and its roots).

Do **not** read or import the scripts in `prompt_4_code/` or `prompt_4_review_code/`. Independence is the point: write your own evaluator of f from the block.

## Checks

- **X1, C1 roots per segment (SciPy).** Find all roots of f(Δt) on (0, τ_w) by a method independent of the earlier grid and quartic counts: locate the critical points of f with `scipy.optimize.brentq` on f′ (bracket using the sign of f″ and the known limits), then bracket and solve f on each monotone piece with `brentq`. Also, as a second route, square out the radicals into a polynomial and use `numpy.polynomial.polynomial.polyroots`, keeping only roots that satisfy the original (unsquared) equation. Cases: (i) the 3-root reference example from the outputs, compare the three roots (relative tolerance 1e-10 on Δt/τ_w); (ii) at least 2,000 random cases with at least 300 inside the 3-root window (K_g > 0, 1 ≤ m < ρ − 1, a and d′ chosen to put both critical points inside the segment), m from 1 up to 1e6; (iii) m = 0 and K_s ≤ K_g. Report: maximum root count found, count agreement between the two SciPy/numpy routes, and every case where they disagree, re-evaluated at 50 digits in mpmath to say which route is right.
- **X2, C3 T (SciPy).** For random (a, K_g, K_s, R_g, d₀, τ_w) with ā ≠ 0 and ā = 0, compute the time after which the bound in the Result table fixes the verdict by `brentq` on the bound function, compare with the closed form stated there, and check on a τ grid beyond T that f has the claimed sign.
- **X3, C4 and C5 worst case (SciPy global optimiser).** For random boxes over (a, K_g, K_s, d₀, R_g, τ_w, λ_ℰ), every coordinate non-degenerate, and fixed τ (including τ near j·τ_w and τ < τ_w), maximise and minimise f over the box with `scipy.optimize.differential_evolution` (fixed seed) and check that the maximum is not larger than f at the pessimistic corner, and the minimum not smaller than f at the optimistic corner, within a stated tolerance. At least 200 boxes. Any violation: re-evaluate both points exactly (`fractions.Fraction` for m and Δt, mpmath for the square roots) before calling it a violation.
- **X4, C4 h(s) (SciPy).** For random τ and K_g > 0, sample h(s) = K_g·[m√s + √(τ − m·s)] densely on (0, τ] including s = τ/k ± ulp, and check monotonicity with numpy; at the points s = τ/k compare left and right limits.

## Files you write (only these)

Under `local_docs/fable_runs/prompt_4_xcheck_code/`: one standalone script per check (`x1_*.py` … `x4_*.py`; a small shared evaluator module is allowed, written by you), each with a docstring (purpose, claim, method, how to run) and fixed seeds, runnable with `<gms-local>/.venv/bin/python <path>` from any directory; saved stdout in `outputs/<script>.txt`; `outputs/issues.md` (empty if none). Then `local_docs/fable_runs/prompt_4_xcheck.md`: a table (check, claim, method, cases, agreement with the earlier results, disagreements), and a short "Not settled" section. Leave no `.hypothesis/` or `__pycache__/` directory (set `sys.dont_write_bytecode = True` before importing a local module).

## Common rules

Read only the files named here. Do not edit files you were not told to write. Do not commit. Do not install anything. Do not search the web. Every number you state must be reproducible from a saved script. Mark anything you could not verify as UNSURE. A check that compares an expression with itself, or that is true by construction, must be flagged, not passed. Everything you produce is a claim at level `derived`; agreement between solvers is evidence of self-consistency, not physical correctness.

Final message: scripts, result per check (agree / disagree with numbers), disagreements and issues.
