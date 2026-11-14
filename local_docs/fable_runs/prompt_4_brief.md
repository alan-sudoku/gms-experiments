# Prompt 4 brief: solver lemma red-team (`sonnet`)

Context file (`local_docs/`, never cited by the spec). Written 2026-11-14 by the orchestrator (`local_docs/orchestration/fable_delegation_plan.md`). Prompt 4 has no Fable stages (§4 matrix): one `sonnet` agent does planning, computation and the answer; an `opus` S5 reviewer follows. User decisions 2026-11-14: start now; SymPy, hypothesis and numpy installed in the project `.venv`; scope C1–C5 only; `opus` S5 review.

## Task

Read `local_docs/fable_questions.md`, section "Prompt 4 (optional): solver lemma red-team", the fenced text block only. For each claim C1–C5, find a concrete counterexample or give a proof sketch backed by executable checks. Prefer concrete numeric counterexamples to prose. Cover every edge case the block names (K_g = 0, a = 0, τ < τ_w, ties at τ = j·τ_w), and also K_s = K_g, K_s = 0, R_g = 0 and m = 0.

## Definitions the block leaves implicit (use these)

- τ_w > 0. Segments are [t_m, t_{m+1}) with t_m = m·τ_w, so at a tie τ = j·τ_w the point belongs to segment m = j (f has already jumped). m = floor(τ/τ_w).
- a is any real (sign free); K_g, K_s, R_g ≥ 0; d₀ is any real.
- λ in C5 is λ_ℰ ≥ 0, a one-off credit independent of τ that sits inside d₀: d₀ = D − λ_ℰ, so ∂f/∂λ_ℰ = −1. Treat D as the coefficient called d₀ in the box and λ_ℰ as a separate coefficient.
- "Pessimistic corner" means each coefficient at the bound of its interval that makes f larger (worse for geometry); "optimistic" the bound that makes f smaller. The direction per coefficient is part of what C5 asks; derive it, do not assume it.
- Winning set = {τ ≥ 0 : f(τ) < 0}. f = 0 is a tie, not a win.

## Method

1. **Symbolic (SymPy)** where a claim is an identity or a sign argument: f'' and its zero (C1), the boundary jump (C2), the per-period drift behind ā (C3), dh/ds on each interval of constant m and the behaviour of h across the points s = τ/k where m changes (C4), the partial derivatives of f in each coefficient (C5).
2. **Property tests (hypothesis)** for each claim, with `@settings(database=None, derandomize=True, deadline=None)` and enough examples to be meaningful (at least 2,000 per property). Strategies must reach the edge cases above (use `st.sampled_from` mixed with ranges, or `hypothesis.target`, or a coverage assertion) so the tests are not vacuous; report the coverage counts. Ranges must span realistic scales (τ_w from 1e3 to 1e9 s, horizons up to about 1e10 s) and small ones.
3. **Root counting for C1**: compare the claimed count with a dense grid (refined near sign changes) on each segment; report the maximum number of roots found per segment and an example that reaches it, if any.
4. **C3**: give an explicit T after which the verdict is permanent where you can, and check it numerically; for ā = 0 with K_s = 0 check periodicity exactly; for ā = 0 with K_s > 0 check whether "eventually wins" holds for every d₀, R_g, K_g.
5. **C5**: test the inclusion winning set(pessimistic) ⊆ winning set(any input in the box) ⊆ winning set(optimistic) on random boxes and random interior points, pointwise in τ, including τ near and exactly at j·τ_w for the corner and the interior τ_w values. Also say whether C5 for τ_w follows from C4, and check that logic.
6. **Confirm every counterexample** found in float64 at 50 or more digits (mpmath, installed with SymPy) or exactly in SymPy before you call it a counterexample. If it does not survive, report it as a float64 artefact, with the magnitudes involved (this matters for the solver's tolerance).
7. A check that compares an expression with itself, or that is true by construction, must be flagged as such in the output, not reported as a pass.

## Files you write (only these)

All under `local_docs/fable_runs/`:

- `prompt_4_code/*.py`: one standalone script per claim (or a shared helper module plus one per claim). Docstring: purpose, claim ids, assumptions, how to run. Each runs with `<gms-local>/.venv/bin/python <path>` from any directory, with fixed seeds, and needs no files outside `prompt_4_code/`. It must not leave a `.hypothesis/` directory anywhere; delete one if it appears.
- `prompt_4_code/outputs/<script>.txt`: saved stdout of each script.
- `prompt_4_code/outputs/issues.md`: ambiguities in the claims, failed or vacuous checks, float64 artefacts. Empty file if none.
- `prompt_4_answer.md`: the answer. Format:
  - Summary table: claim, verdict (holds / holds with conditions / false), the decisive script.
  - Per claim: proof sketch or concrete counterexample (exact numbers, reproducible from a named script and output line); edge cases and where it fails; a suggested restatement if the claim is false or needs conditions.
  - "Identity checks": the checks that are true by construction.
  - "Not settled": what the scripts could not decide.

## Common rules

Read only the files named here. Do not edit files you were not told to write. Do not commit. Do not install anything. Every number you state must be reproducible from a saved script. Do not search the web. Mark anything you could not verify as UNSURE. Everything you produce is a claim at level `derived` (unverified); passing property tests are evidence, not proof.

Final message: list of scripts, verdict per claim, counterexamples (if any), and issues.
