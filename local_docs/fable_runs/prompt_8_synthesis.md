# Prompt 8 synthesis: infrastructure credit shared by several products (OQ-14)

Context file (`local_docs/`, never cited by the spec). Orchestrator synthesis of `prompt_8_web_answer.md` (Fable, no tools) and `prompt_8_review.md` (`opus` S5), written 2026-11-15. Every result is at level `derived`; all inputs are the made-up rv03 numbers.

## Verdict

- **The answer's core analysis holds in the linear model.** The S5 review reproduces every number. With B_infra = F + v·N, the best set of switching products is either "those with d_k < v/T₀" or "all". All switch iff F/T₀ > Σ N_k·max(0, d_k − v/T₀). In rv03's case both should switch, a gain of 2.62e10 J/K. The answer's three-way rule (pass / fail / conditional) is the most decisive sound rule possible from one product's data.
- **Claim 2 holds, with a narrower scope.** No rule that must return pass or fail (or a single λ) from one product's data can match the system optimum. A sound three-way rule exists; its "conditional" band is exactly where one product's data cannot decide.
- **The answer's first-edition rule does not stand as a spec rule.** "λ = v/T unconditional" is not a lower bound when outside users absorb the freed supply (rebound), or when B_infra is convex and v is read as B′(N). There it gives wrong verdicts labelled unconditional, losing 6.6e9 to 2.2e10 J/K. F, v and F_av are not spec symbols. No document owns a verdict over several products.
- **The current spec (E16) is wrong in rv03's own case**, losing the whole joint gain (2.62e10 J/K). It has two defects the no-tools answer could not see:
  - **Bypass (finding 1).** REQ-LIFECYCLE-CEXC-SOURCE item 4 removes capital goods from CExC only when λ_ℰ > 0. Under E16 a partial exit has λ_ℰ = 0, so the average share returns through Σ_s,init. Product 1 then switches alone, losing 1.01e11 J/K.
  - **Double count (finding 2).** B_infra includes monitoring, assaying and maintaining, which a CExC source may also contain. When the gate opens, v/T₀ is counted twice (loss 2.88e10 J/K at d = (230, 230)).
- **E16 also credits sunk exergy.** B_infra includes "establishing" the loop, which is already spent for an existing chain. With half of F sunk (α = 0.5, d = (150, 190)), E16 switches both and loses 1.98e10 J/K.
- **Some cases make every alternative wrong** (E16, the average share without the gate, marginal only, the answer): capacity steps, partial rebound and convex B_infra. They occur in 2–12 % of random profiles in those regimes and in none of the linear ones.
- **A sound replacement exists with one new input.** The reviewer's rule R5 needs only B_infra, T₀ and N_k, the positions of this product that share B_infra(x). It gave no wrong unconditional verdict in any of the five regimes tested:
  - pass unconditionally if f(τ) < 0 with λ_ℰ = 0;
  - fail unconditionally if f(τ) ≥ 0 with the largest possible credit B_infra/(T₀·N_k);
  - otherwise "conditional on the other products", reported with ψ_k = N_k·T₀·(Σ_g − Σ_s)/B_infra.

  The price is a wider conditional band: in rv03's case, (0, 223.6) J/K for product 1, against the answer's (67.08, 216.15). R5 is sound only if the bypass is closed: with capital goods inside CExC, its "pass with λ_ℰ = 0" is no longer conservative.

Reviewer counts: 0 BLOCKER, 7 MAJOR, 7 MINOR. All 6 review scripts reproduce byte for byte (orchestrator re-run, 2026-11-15), and rv03 §D matches its saved output.

## Where the review disagrees with the answer

| Answer | Review | Orchestrator view |
|---|---|---|
| Claim 2: no per-product rule can agree with the system test | True only for rules that must return pass or fail; the three-way rule is sound | Agree with the review; the answer's own rule already shows it |
| Claim 5: a lone switcher is under-credited by v | Depends on what the CExC source contains: under-credit (A), over-credit by the average share (B), or v is already counted (C). The spec cannot tell A from C | Agree; this is why the CExC source conditions must change (D1) |
| Claims 6–7: λ = v/T₀ is "unconditional", "exact" with outside users | Fails under rebound and convex B_infra; holds under capacity steps | Agree; drop "unconditional" for any credit above 0 |
| Claim 6: staggered switching shrinks F_av | Right, but makes λ depend on switching dates and the remaining horizon, against U6 | Agree; keep staggered switching open (OQ-14) |
| Claim 7: F enters only a system verdict (Σφ_k < 1) | No GMS-100 symbol carries other products' data; no owner for that verdict | Agree; an owner above GMS-100 is a later decision |
| Uses T_ref | The spec uses T₀; mixing them moves Σφ from 0.804 to 0.885 at T₀ = 250 K | Use T₀ throughout |

## What it means for the spec

- **GMS-100 (accepted).** Three changes, all before the `spec-0.1` tag, so they edit the existing IDs rather than minting `-R2`:
  - **REQ-LIFECYCLE-CEXC-SOURCE.**
    - Item 4 changes: capital goods are excluded whenever B_infra(x) is in the evaluation, not only when λ_ℰ > 0.
    - A new item 6: no upstream flow is counted in both CExC(x) and B_infra(x), and the source states which of the monitoring, assaying and maintaining flows it contains.
  - **EQ-LIFECYCLE-SUPPLY-CHAIN-COST and EQ-LIFECYCLE-PARITY-CONDITION.**
    - The all-or-nothing gate gives way to R5's three-way verdict for a partial exit.
    - The sole-user case (N_k = N_alloc) keeps the present average-share credit.
    - A new scenario input N_k, with no default.
  - **B_infra definition.** Either the avoidable part only, or a stated known bias for the sunk part (D3).
- **GMS-400 and GMS-410 briefs.** The parity decision gains a "conditional" outcome. GMS-400 carries ψ_k; GMS-410 reports it.
- **OQ-14 narrows.** Several items stay open:
  - any credit above 0 for a partial exit (the F/v split and its data, with the rebound and convexity conditions);
  - who owns a verdict over several products;
  - capacity steps and other non-linear B_infra;
  - staggered switching against U6;
  - margins on the "unconditional" labels;
  - the within-product case, which the parity assumption still excludes.
- **Data.** The review's decisive check overlaps the OQ-22 task: for one real scarce element, split the CExC source's supply-chain exergy into capital, operating and maintenance parts, and B_infra into sunk, avoidable-fixed and variable parts.

## Decisions for the user

**Decided 2026-11-15: the user accepted the recommendation for D1–D5.** Recorded as E28 in drafting notes §A (applied to GMS-100 the same day: REQ-LIFECYCLE-CEXC-SOURCE items 4 and 6, B_infra as the avoidable part over τ_infra, new EQ-LIFECYCLE-INFRASTRUCTURE-SHARE and REQ-LIFECYCLE-SHARED-INFRASTRUCTURE-VERDICT; lint 0 issues, 64 tests pass); OQ-14 narrowed, OQ-22 data task extended, GMS-400 and GMS-410 brief notes in `orchestrator_state.md` §3 and §4; plan V18.

| # | Decision | Options | Recommendation |
|---|---|---|---|
| D1 | CExC source conditions (findings 1, 2) | (a) Amend REQ-LIFECYCLE-CEXC-SOURCE. Item 4: "it excludes capital goods of the supply chain of x whenever B_infra(x) is part of the evaluation". New item 6: "no upstream flow is counted in both CExC(x) and B_infra(x); the source declares which monitoring, assaying and maintaining flows of the loop it contains". (b) Leave as is | (a). It closes a 1.01e11 J/K bypass and a double count with no new symbol. Under-crediting the candidate is the conservative direction the spec already uses |
| D2 | Partial exit (OQ-14 core; findings 5, 8, R5) | (a) Replace E16's all-or-nothing gate with R5. Sole user (N_k = N_alloc): λ_ℰ as now. Otherwise pass unconditionally if f(τ) < 0 with λ_ℰ = 0; fail unconditionally if f(τ) ≥ 0 with credit B_infra/(T₀·N_k); otherwise "conditional on the other products", with ψ_k reported. New scenario input N_k, no default. (b) The answer's rule (λ = v/T₀ unconditional, bracket to v/T₀ + F_av/(T₀·N_k)): needs F, v and F_av, which the spec does not define, and fails under rebound or convexity. (c) Keep E16 and record its known bias (loses the joint gain; wrong and unflagged) | (a), recorded as new correction E28 (GMS-100). It needs D1. Apply in one GMS-100 edit with lint and tests, with GMS-400 and GMS-410 brief notes for the "conditional" outcome |
| D3 | Sunk "establishing" part of B_infra (review Fit (b), finding 5) | (a) Redefine B_infra(x) as the avoidable part: the minimum exergy that removing x from every sharing product would avoid. That is monitoring, assaying and maintaining over a scenario-declared infrastructure horizon fixed independently of τ (keeps U6), plus any re-establishment within it, excluding exergy already spent. (b) Keep the definition; record in an assumption that for an existing chain λ_ℰ over-credits the candidate by the sunk part, the non-conservative direction | (a), with D2 under E28. Under R5 a sunk part only widens the conditional band, but in the sole-user case it gives wrong "candidate wins" verdicts. B_infra has no values yet, so redefining it costs nothing now |
| D4 | What stays open | Rewrite OQ-14 (`orchestrator_state.md` §3) and GMS-100's matching Open item: partial-exit credit above 0 (F/v split, rebound, convexity); the owner and inputs of a verdict over several products (a higher-tier scenario or portfolio document); capacity steps and non-linear B_infra; staggered switching against U6; uncertainty margins on the unconditional labels; the within-product case. Decisive check: the CExC and B_infra decomposition for one real scarce element, added to the OQ-22 data task | Adopt |
| D5 | Plan record | V18: Prompt 8 outcome (E28, OQ-14 narrowed, CExC-source items) | Adopt |

## Cost

| Stage | Model | Time | Tokens | Tool calls |
|---|---|---|---|---|
| Fable stage (no tools) | `fable` high | 2 min | about 42k | 0 |
| S5 reviewer | `opus` high | 12 min | about 142k | 23 |
