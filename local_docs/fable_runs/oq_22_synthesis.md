# OQ-22 synthesis: does GMS-100's Σ_init price a scarce catalyst?

Context file (`local_docs/`, never cited by the spec). Orchestrator synthesis of `oq_22_answer.md` (`sonnet`, from `oq_22_brief.md`) and `oq_22_review.md` (`opus`), written 2026-11-15. Every result is at level `derived`. The CED values are LOOKUP; the B_infra inputs, duty scenarios and cell-level overpotentials are MEMORY or search snippets.

## Verdict

- **"Nearly free" holds for the central set the brief fixed** (j = 1 A/cm², 8e4 h, continuous duty). Ir at 0.2 to 2 mg/cm² gives Δη_be = 0.1 to 1.6 mV, and Pt at 0.1 to 0.5 mg/cm² gives 0.07 to 0.76 mV. Every row is below 10 mV. The review reproduced every number and matched the central set to 0.0001 mV with its own molar-form code.
- **The finding is a framework property, but its size depends on the data and the duty.** The review separates two claims:
  - **Framework:** GMS-100 0.1 has no term that measures depletion. Dispersal is charged b_ch, which per kg is smaller for Pt than for Fe (0.72 against 6.75 MJ/kg). λ_ℰ prices avoidable loop infrastructure, not scarcity. Scarcity can enter only through the CExC data: ore grade, and the source's allocation rule.
  - **Data and duty:** "about 1 mV" holds with CED at 2006–10 revenue allocation and continuous duty. Ir at 1 to 2 mg/cm² leaves "nearly free" in four plausible cases:
    - revenue allocation redone at 2024–26 Ir prices: 9 to 24 mV;
    - renewable-coupled duty below about 1e4 A·h/cm²: 14 to 29 mV;
    - an ERC-type depletion term, using the PGM average as the Ir proxy: 20 mV;
    - GMS-100's own shared-loop rule: "conditional" up to 11 to 35 mV at a 1 % share of loop throughput.
- **E18's own case does not rest on Σ_init in either direction.**
  - In alkaline, NiFe is at least as active as IrO₂ (Δη = −34 to −48 mV in half-cells, from snippets). The candidate wins on Σ̇ alone, so the question is moot.
  - At cell level, PEM (IrO₂) against AEM (NiFe) differs by +50 to +1160 mV. That is 31 to 716 times the largest Δη_be. Σ̇ decides.
  - The material term matters only within about ±2 mV of parity at continuous duty.
- **Part B (Prompt 8 D4) does not settle which configuration the spec is in.**
  - "Mix of B and C" overstates the evidence. The CED source is silent on capital goods in both its SI and its main text. The C share counts production ventilation as "maintaining".
  - Defensible reading: undetermined between C and B+C. A is excluded only by inference.
  - α depends on the definition of "fixed part": 0.84 to 0.95 with all fixed flows, 0.20 to 0.70 with loop capital only. Prompt 8's flip value of 0.804 lies between the two readings.
  - The source fails items 1, 2, 4, 5 and 6 of REQ-LIFECYCLE-CEXC-SOURCE as published and meets item 3 (revenue allocation, 2006–10 prices).

Reviewer counts: 0 BLOCKER, 7 MAJOR, 8 MINOR. The answer's two scripts and the review script reproduce byte for byte (orchestrator re-run, 2026-11-15). The reviewer stopped at the usage limit after its review file was complete; it was not resumed.

## Where the review disagrees with the answer

| Answer | Review | Orchestrator view |
|---|---|---|
| E18's scarcity sentence is reversed under GMS-100's terms | It holds only for the central duty and the 2006–10 allocation (findings 3, 4). E18's own case rests on Σ̇ either way (finding 5) | Agree with the review; replace E18's sentence (D2) |
| λ_ℰ estimate adds 0.8 to 29 % | For a shared Pt or Ir loop, the verdict quantity is f₀ and f_max (REQ-LIFECYCLE-SHARED-INFRASTRUCTURE-VERDICT), not λ_ℰ; between about 1 mV and the f_max edge GMS-100 says "conditional" (finding 2) | Agree. This is partly the brief's convention 10. The spec is right; the answer applied it too narrowly (D3 (b)) |
| Mass allocation gives Δη_be < 0, "so the candidate wins" | Inverted: Δη_be < 0 means the incumbent wins at zero penalty (finding 1) | Agree; errata (D7) |
| Part B: mix of B and C, not A; α = 0.84 to 0.95 | Undetermined between C and B+C; α depends on the definition and straddles 0.804 (findings 6, 7) | Agree; record in OQ-14 (D6) |
| Lever factors, transport share | j·τ factor for Pt 0.1 is 453, not 340; transport minimum 3.35 J/K (findings 8, 9) | Errata (D7) |

## What it means for the spec

- **GMS-100:** no formula change. The framework's lack of a depletion term is a scope fact. Finding 3 shows that a revenue-allocated CExC source carries a price year, which moves Ir's value by up to about 20 times. REQ-LIFECYCLE-CEXC-SOURCE item 3 asks for the allocation rule but not the price year.
- **GMS-310 Part C:** E18's last sentence ("the substitution case rests on scarcity (Σ_init), not on Σ̇") is not supported. The brief must say what decides the case (Σ̇ and its drift) and when the material term can matter (low throughput, current-price allocation, a shared loop).
- **OQ-22:** the question as asked ("does Σ_init price scarcity?") is answered: not as a depletion measure, and only about 1 mV at continuous duty with the data read. What stays open is whether GMS-100 should have a depletion term, and a sourced CExC for Ir and Pt.
- **OQ-14:** the decisive check (the CExC and B_infra decomposition) was attempted and did not settle the configuration. It still needs a source that declares its capital goods and loop flows.

## Decisions proposed

| # | Decision | Proposal | Orchestrator recommendation |
|---|---|---|---|
| D1 | Fable reserve (a) | The trigger is met for the central set. Two options: (i) run the Fable follow-up now ("does GMS-100 price scarcity, and should it have a depletion term?"), with review findings 2, 3 and 4 in the block; (ii) hold the reserve. The review shows that the GMS-310 Part C verdict does not depend on the answer (Σ̇ decides). The "should" question also needs data that no run could read (an Ir ERC, a sourced CExC with its price year). | (ii) Hold. Record the "should" question as the rest of OQ-22. Revisit only if a scenario's verdict falls inside the band where the material term matters (low throughput, Ir ≥ 1 mg/cm²) |
| D2 | E18's scarcity sentence | New correction E30 (GMS-310 Part C) replaces E18's last sentence with the review's safe form: "In GMS-100's terms the material of a mg/cm² PGM loading is worth of order 1 mV of overpotential at continuous duty, scaling as 1/(j·τ); the substitution case is decided by Σ̇ (cell voltage and its drift). GMS-100 does not price depletion; whether it should is open (OQ-22)." Drafting notes only; GMS-310 is not drafted | Adopt |
| D3 | GMS-310 Part C brief notes | (a) Report the material term as Δη_be with its 1/(j·τ) scaling and the throughput at which it reaches 10 mV (Ir 2 mg/cm² about 9.6e3, Ir 1 about 4.7e3, Pt 0.5 about 3.3e3 A·h/cm²; `derived`); no numbers from this run go into the spec (R1). (b) A PGM loop is shared, so the Part C verdict follows REQ-LIFECYCLE-SHARED-INFRASTRUCTURE-VERDICT (f₀, f_max, conditional with ψ_infra), not λ_ℰ. (c) A PEM-to-AEM swap removes Ir, Pt, Ti and fluoropolymer together; GMS-100's parity test removes one x at a time, so state this as a limitation (Open item). (d) A Pt cathode substitute is an HER catalyst (Ni or NiMo in alkaline), not NiFe (finding 10). (e) The Prompt 9 note stands: if the incumbent's loss rises with age, the profile cannot represent it; the drift difference that the material term can offset is about 0.03 µV/h over 8e4 h, far below reported drifts (0.7 to 84 µV/h, snippets) | Adopt |
| D4 | OQ-22 | Narrow it to: (a) whether GMS-100 should carry a depletion term (ERC-type), and its owner, data and licence; (b) a sourced CExC for Ir and Pt (ore exergy included, allocation rule and price year declared, chemical form). Answered: GMS-100 0.1 has no depletion term, and the material term is about 1 mV at continuous duty with CED data (`fable_runs/oq_22_review.md`, minimal safe statement). Phase 6 decisive check: a time-resolved cell-voltage record of IrO₂ against NiFe anodes in the same AEM cell over at least 1000 h at a stated j | Adopt |
| D5 | REQ-LIFECYCLE-CEXC-SOURCE item 3 | Add "and, for an allocation by economic value, the price year" (finding 3). GMS-100 is accepted, so this would be E31, a one-clause wording change. Two options: apply now, or with the W5 batch | Adopt; apply with the W5 batch, since no evaluation uses a source before Phase 2 |
| D6 | OQ-14 | Add: the decomposition attempted on Pt (CED source) leaves the configuration undetermined between C and B+C. α depends on whether the "fixed part" is loop capital only (0.20 to 0.70) or all fixed flows (0.84 to 0.95), and the flip value 0.804 lies between them. The decisive check stays open and needs a source that declares capital goods and loop flows | Adopt |
| D7 | Records | Errata section in `oq_22_answer.md` (findings 1, 6, 7, 8, 9, pointing to the review); plan V20; `orchestrator_state.md` §3 (OQ-14, OQ-22) and §4 (GMS-310 notes); a row in `fable_delegation_plan.md` §7 for the reserve (a) trigger | Adopt |

## Cost

| Stage | Model | Time | Tokens | Tool calls |
|---|---|---|---|---|
| Check (plan, scripts, answer) | `sonnet` | 14 min | about 242k | 70 |
| Review | `opus` high | stopped by the 5-hour limit after writing the review | not reported | not reported |
