# Prompt 7 synthesis: entropy currency across environments (OQ-13)

Context file (`local_docs/`, never cited by the spec). Orchestrator synthesis of `prompt_7_web_answer.md` (Fable, no tools) and `prompt_7_review.md` (`opus` S5), written 2026-11-15. Every result is at level `derived`.

## Verdict

- **Currency:** both the answer and the review support E15's lost-work currency (A) for edition 0.1. Currency (B), the entropy currency, is not adopted for three reasons:
  - it misranks pure dissipated work: 100 J lost at 290 K counts as better than 60 J lost at 150 K (answer claim 3);
  - it cannot be computed from tables, which give upstream lost work at T_ref only, not at each site's temperature (review finding 14);
  - it needs two dead states in one evaluation, which GMS-000 DEF-DEAD-STATE forbids (review finding 11).
- **The 5 % figure:** it is an artefact of rv02's sampling. It ranges from 0.95 % to 10.3 % across T₀ bins and falls to 3.6 % when magnitudes spread over 4 decades. The exact statement is answer claim 5, now checked on all 5,057 flipped cases: (A) and (B) disagree if and only if the break-even factor c* = −ΔU/ΔO lies in (1, T_ref/T₀). Here ΔU is the difference in upstream lost work and ΔO the difference in operational lost work.
- **What lies behind the disagreement:** the real question is how much primary exergy one joule of operational work costs (c_op). GMS-100 already has this as OQ-15, the mixed-basis item and its carrier factor. It is not a currency question. Answer claim 4, the example where (A) misranks, is OQ-15's problem.
- **Parts of the answer's verdict that do not stand:**
  - **"T₀,eval is only a scale factor" (claim 8) is false in GMS-100.** There, T₀ is also the dead state of operational losses. For a heat-transfer loss, Σ = S_gen does not depend on T₀, while tabulated upstream terms scale as 1/T₀, so the choice of T₀ changes rankings. In `rv7_03` (b), D2 wins at 150 K and D1 wins at 200 K and 290 K.
  - **The proposed "undecided" band (1, r) gives no protection.** It uses (B)'s weight r, which has no physical basis. With c* = 2.5 and c_op = 3, both currencies are wrong and nothing is flagged. It is decided but wrong in 2.5 % of cases for c_op in (2, 3), and in 11.1 % for c_op in (0, 1).
- **A regime nobody had considered:** a radiating spacecraft rejects heat to deep space at about 2.7 K. Its "effective T₀" is therefore a convention, and that convention moves the heat-transfer lost work by about ×100 under (A) as well as under (B).
- **Answer claim 6:** the upstream term CExC − Ex_product is already GMS-100's w_lost,ext = CExC − b_ch. Over the life of the unit, b_ch is charged at dispersal, so GMS-100's ledger needs no change.

Reviewer counts: 0 BLOCKER, 5 MAJOR, 9 MINOR. All 5 review scripts reproduce (orchestrator re-run, 2026-11-15). I checked the claim 8 counterexample by hand: Σ_op = T₀·S_gen/T₀ = S_gen.

## Where the review disagrees with the answer

| Answer | Review | Orchestrator view |
|---|---|---|
| Claim 1: c_k ≥ 1; (A) is "closer" | Energy/exergy basis error: on an exergy basis at T_ref, c < 1 when T₀ < T_ref; a free flux gives c ≈ 0 | Review is right. (A) is the 0.1 choice because of claims 2 and 3 and finding 14, not claim 1 |
| Claim 4: (A) misranks when c_op ≠ 1 | That is the mixed basis (OQ-15), not the currency | Agree with the review |
| Claim 8 and verdict: T₀,eval only scales | False in GMS-100 for heat-transfer losses | Agree; GMS-100 should say so (D2) |
| Verdict: "undecided" when c* ∈ (1, r) | Not protective; use a declared c_op range (box test) or report c* | Agree; route to OQ-15 (D4) |
| Validity: "T₀,k the real heat-rejection reservoir" | Undefined for a radiating spacecraft (about 2.7 K sink) | Agree; this is a convention to decide (D3) |
| Claim 6: CExC/T_ref overstates upstream S_gen | True for the extraction stage alone; GMS-100 already uses CExC − b_ch and charges b_ch at dispersal | No spec change; data note only (D5) |

## What it means for the spec

- **GMS-100 (accepted).** The equations do not change. The changes are two pieces of wording:
  - the currency Open item records why (B) is not adopted;
  - one assumption sentence under EQ-LIFECYCLE-LOST-WORK-CURRENCY says that T₀ is not a free scale factor.

  Both are clarifications. No owned ID changes meaning.
- **GMS-000.** No change. DEF-DEAD-STATE (one dead state per evaluation) is what makes (B) impossible as written.
- **Scenarios.** Before any low-Earth-orbit or spacecraft dead-state preset is written (`configs/dead_states/`, which does not exist yet), the radiating-spacecraft convention must be decided.
- **GMS-410.** No "undecided" band from Prompt 7. Where a verdict trades upstream terms against carrier-fed operational terms, c* can be reported as a diagnostic (OQ-15).

## Decisions for the user

| # | Decision | Options | Recommendation |
|---|---|---|---|
| D1 | OQ-13 (currency) | (a) Close OQ-13: (A) stays (E15); (B) is not adopted for three reasons (it misranks dissipated work, it cannot be computed from tables, it needs two dead states). Rewrite GMS-100's currency Open item to give the reasons. Correct "about 5 %" to the exact condition c* ∈ (1, T_ref/T₀). (b) Keep OQ-13 open | (a). The remaining disagreement is OQ-15's c_op, not a currency choice |
| D2 | T₀ is not a free scale (claim 8, review finding 1) | (a) Add one assumption sentence to EQ-LIFECYCLE-LOST-WORK-CURRENCY: T₀ is also the dead state of operational losses; for a loss whose entropy generation the process fixes (heat transfer between given temperatures), Σ does not depend on T₀, while tabulated upstream terms scale as 1/T₀, so the choice of T₀ can change a ranking. (b) Leave as is | (a), recorded with D1 as new correction E27 (GMS-100, wording only). Apply both in one small GMS-100 edit with lint and tests. Timing: now, or with the W5 batch |
| D3 | Dead state of a radiating spacecraft (review finding 5) | (a) New OQ-23: the dead-state convention for a radiating spacecraft (deep-space sink at about 2.7 K, radiator temperature, or an effective T₀), to be decided before any spacecraft preset; ADR when settled. (b) Restrict 0.1 presets to terrestrial dead states and leave spacecraft to a later edition | (a), with no spacecraft preset in 0.1 until it is decided. (b) is the fallback if no one decides in time |
| D4 | The "undecided" band (verdict, review findings 2 and 6) | (a) Reject the r-based band. Extend OQ-15 with the box-test form: a verdict is undecided only if c* lies inside the declared, sourced range of c_op; with several environments, the sign is tested at the corners of the box of c_k ranges. Add a GMS-410 brief note: report c* as a diagnostic, with no verdict change in 0.1. Remove the "same path" sentence about Prompt 7 in `orchestrator_state.md` §4. (b) Adopt the answer's band | (a) |
| D5 | Data notes (claim 6, review finding 8) | (a) No spec change; add to the Prompt 3 data-pull and OQ-22 tasks that CExC and b_ch come from the same table (Al: 888.4 kJ/mol in the older Szargut table against about 795.7 kJ/mol revised, UNSURE). Add the decisive check (a sourced c_op for one spacecraft power chain, at T_ref, launch included) to OQ-15 as a Phase 6 item. (b) Nothing | (a) |
| D6 | Plan record | V17: Prompt 7 outcome (OQ-13 closed, E27, OQ-23, OQ-15 extended) | Adopt |

## Cost

| Stage | Model | Time | Tokens | Tool calls |
|---|---|---|---|---|
| Fable stage (no tools) | `fable` high | 6 min | about 44k | 0 |
| S5 reviewer | `opus` high | 8.4 min | about 123k | 28 |
