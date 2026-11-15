Context file (`local_docs/`, never cited by the spec).
S5 review of `prompt_7_web_answer.md`, written 2026-11-15.

Reviewer: `opus` S5, adversarial. Every statement here is a claim at level `derived`; agreement with the answer is not validation. Scripts are in `local_docs/fable_runs/prompt_7_review_code/`, with their stdout in `outputs/<script>.txt`. Run them from any directory with `.venv/bin/python`.

## Summary verdict

1. The answer recommends currency (A) for edition 0.1. That agrees with E15 and with `EQ-LIFECYCLE-LOST-WORK-CURRENCY` as written. Every number reproduces, and claim 5's flip condition holds exactly ("if and only if") on all 5,057 flipped cases of rv02 (5.06 %).
2. The two protective parts of the verdict do not hold up. First, T₀,eval is a pure scale factor only if T₀,eval is decoupled from the dead state. In GMS-100 it is the same T₀ that prices the operational losses, so for heat-transfer losses it changes rankings. Second, the "undecided" band (1, r) uses (B)'s arbitrary weight r, not the real carrier factor c_op. It misses c* = 2.5 with c_op = 3, and it misses every case with c_op < 1.
3. Claim 4's failure of (A) is the mixed-basis item already open in GMS-100 (OQ-15), not a property of the currency. Claim 6's upstream term CExC − b_ch is already GMS-100's w_lost,ext.
4. Claim 1 mixes bases. Its c = T_h/(T_h − T₀) is an energy ratio. On an exergy basis valued at T_ref, c < 1 whenever T₀ < T_ref, so "c_k ≥ 1" fails across environments.
5. The answer misses one regime: for a radiating spacecraft the "effective T₀" is a convention (the sink is about 2.7 K). That convention moves S_gen by about ×100 under (B) and moves heat-transfer lost work by about ×100 under (A). Findings: 0 BLOCKER, 5 MAJOR, 9 MINOR.

## Findings

| # | Severity | Location | Finding | Evidence |
|---|---|---|---|---|
| 1 | MAJOR | Claim 8; verdict ("T₀,eval stated as a scale only") | Σ_A = (1/T₀,eval) Σ T₀,k S_gen,k is scale-invariant only if each lost work is fixed independently of T₀,eval. In GMS-100, DEF-DEAD-STATE allows one dead state per evaluation, and Ṡ_gen,phys = Ḃ_lost,phys / T₀ prices operational losses at that same T₀. For a loss whose S_gen is fixed by the process (heat transfer between design temperatures; also chemical lost work evaluated at T₀), B_lost = T₀ S_gen, so the GMS-100 margin is ΔU/T₀ + ΔS_op and its sign depends on T₀. Dissipated work (B_lost = W) is the only case where claim 8 holds in GMS-100. Claim 8's falsifier ("any rank change means the code re-references losses") would misdiagnose this physical T₀ dependence as a code bug. | `rv7_03_gms100_ledger.py` (b): the heat-transfer pair prefers D2 at 150 K and D1 at 200 and 290 K; the dissipated-work pair prefers D1 at every T₀ |
| 2 | MAJOR | Verdict ("undecided" band); claim 5 | The band flags a verdict iff the break-even carrier factor c* = −ΔU/ΔO lies in (1, r), with r = T_ref/T₀. Because r is (B)'s weight and not a physical cost ratio, the band protects against claim 4's failure only when c* happens to lie in (1, r). It misses the case c* = 2.5 with c_op = 3 at 150 K, where (A) and (B) agree and both are wrong. It never catches c_op < 1. A rule built on a declared, sourced c_op range [lo, hi] (undecided iff c* ∈ (lo, hi), otherwise decide by the sign of ΔU + cΔO over the range) is never decided-but-wrong when c_op lies in the range. Reporting c* is the input-free form of the same rule. | `rv7_04_carrier_and_band.py` (b): with c_op ~ U(2, 3), the verdict rule is decided-but-wrong in 2.52 % of cases and the range rule in 0.00 %; with c_op ~ U(0, 1) the figures are 11.13 % and 0.00 %; the c* = 2.5 and c* = 0.8 cases are not flagged and both currencies are wrong |
| 3 | MAJOR | Claim 1 | c_k is defined as primary exergy per J of work, but the example c = T_h/(T_h − T₀) is J of heat per J of work, an energy basis. Valued as exergy at T₀, c = 1 for a reversible engine. Valued as exergy at T_ref, where the resource stock is held, c = (1 − T_ref/T_h)/(1 − T₀/T_h), which is below 1 for T₀ < T_ref (0.41 to 0.99 in the grid). So "c_k ≥ 1, c_k = 1 is a physical limit" fails across environments. A free flux (sunlight) gives c ≈ 0 per marginal J. The direction "c rises with T₀, opposite to (B)" survives. The conclusion "(A) is the closer one" is then unsupported in general: both currencies over-weight operation whenever c_op < 1. | `rv7_04_carrier_and_band.py` (a): at T_h = 600 K, T₀ = 150 K, c_E = 1.333, c_Xref = 0.671, (B) r = 1.988 |
| 4 | MAJOR | Claim 4 | Claim 4's failure of (A) is the mixed-basis problem that GMS-100 already records (`EQ-LIFECYCLE-EXERGY-FUNCTIONAL` assumptions; Open items; OQ-15): material terms are cumulative, operational terms are delivered energy. c_op is exactly the carrier factor r_el of the candidate fix. With the carrier factor applied to carrier-fed terms, (A) ranks claim 4 correctly, so claim 4 is not evidence against the currency. GMS-100's operational terms (fatigue dissipation, chemical attack, passivation) are environment-driven, and OQ-15 says the carrier factor does not apply to them; for these, c_op may be near 0 (no stock drawn), not 3. The synthesis should route claim 4 to OQ-15, not OQ-13. | Reading of GMS-100 §1.2 and Open items; `rv7_02_numbers.py` (claim 4 arithmetic) |
| 5 | MAJOR | Verdict validity range ("each T₀,k the real heat-rejection reservoir"); claim 7 | For a radiating spacecraft the heat-rejection reservoir is the deep-space sink (about 2.725 K, the cosmic background), not a 150 to 290 K "effective T₀". (a) At T₀ = 2.725 K, r = 109.4, and (A)/(B) disagree in 24.8 % of equal-scale cases (10.4 % at 150 K). (b) For 1 J dissipated through a 290 K radiator, S_gen is 3.45e-3 J/K at the radiator surface, 4.60e-3 J/K if the entropy of the emitted blackbody radiation (4/3 Q/T) is included, and 0.367 J/K at the sink, a span of ×106. (c) The lost work of a heat-transfer loss under (A) moves ×106 between 290 K and 2.725 K dead states. The validity condition is therefore undefined for the answer's own headline case, and claim 7's "convention" defect affects (A) as well, not only (B). | `rv7_05_missed_regimes.py` (a), (b), (c); the 4/3 factor is a recalled textbook result, UNSURE for grey surfaces |
| 6 | MINOR | Claim 5; verdict band | Claim 5 and the band treat a single operational environment. When operation spans several environments, (A) and (B) disagree even with ΔU = 0; claim 3 itself is such a case, and its ratio |ΔU|/|ΔO| = 0 lies outside (1, r). With upstream plus phases at 290 K and 150 K, the claim-5 band (aggregated ΔO, r = max r_k) catches 46.0 % of the disagreements. The general form is a box test: the sign of ΔU + Σ c_k ΔO_k over c_k ∈ [lo_k, hi_k], evaluated at the endpoints because the form is linear. In GMS-100 this case is not representable (one dead state); see finding 11. | `rv7_04_carrier_and_band.py` (c) |
| 7 | MINOR | Claim 6; verdict ("upstream term taken as CExC − Ex_product") | CExC − Ex_product is already GMS-100's w_lost,ext = CExC − b_ch in Σ_s,init and R_g. GMS-100 never divides CExC alone into an upstream term. Over the life, the "overstatement" b_ch is charged at dispersal (Σ_s,EOL, Σ_g,EOL): with R_rec = 0, Σ_init + Σ_EOL = CExC/T₀ exactly. Σ_EOL^ret charges CExC on purpose (dispersal plus virgin make-up). The claim is right for the extraction stage alone and wrong if read as a correction to the lifecycle ledger. Applying the verdict's wording to Σ_EOL^ret would drop the dispersal charge. CExC − b_ch also carries the source's by-product allocation and its waste-exergy convention (REQ-LIFECYCLE-CEXC-SOURCE item 3), so it is "cumulative destruction" only under that allocation. The recalled Szargut balance form is UNSURE (not checked against a source). | `rv7_03_gms100_ledger.py` (d) (placeholder CExC, b_ch) |
| 8 | MINOR | Claim 6 (Al figure) | 33 MJ/kg matches the older Szargut table value of 888.4 kJ/mol (32.93 MJ/kg). Search snippets give a revised value of about 795.7 to 796.1 kJ/mol (Szargut et al. 2005; Rivero and Garfias 2006), which is 29.5 MJ/kg, −10.6 % from 33 MJ/kg and just outside the stated ±10 %. The figure is only illustrative in the answer, but in the project the value must match the CExC source (REQ-LIFECYCLE-CEXC-SOURCE item 2). UNSURE: snippets only, papers not read. | `rv7_02_numbers.py` (claim 6); web search, titles and technical terms only |
| 9 | MINOR | Falsifiers of claims 2, 3, 5, 7, 8 | Several falsifiers cannot fail. Claim 5's is an algebraic identity: in every flipped case, ΔU + ΔO = ΔO(1 − c*) with c* ∈ (1, r), and 0 of 5,057 rv02 flips violate it. Claim 2's needs a violation of energy conservation (a 2:1 battery draw for 1 J each), and claim 3's needs an energy balance in which 100 J costs less than 60 J. Claim 7's (S_gen insensitive to T₀ for dissipated work) contradicts S = W/T₀, which is a definition. Claim 8's can fail but misattributes the cause (finding 1). Only claims 1, 4 and 6 have falsifiers that need external data. | `rv7_01_flip_condition.py` §2 |
| 10 | MINOR | Question background; OQ-13 text ("about 5 %") | The 5 % is a property of rv02's sampling, not a frequency in real designs. It is 0.95 % in the 270 to 290 K bin and 10.29 % in the 150 to 170 K bin. It is 10.1 % among trade-off cases. rv02's scale ratio k (upstream/operational) runs from 0.69 to 1.33, close to the worst case (10.99 % at k = 1.31, T₀ = 150 K). The fraction falls to 0.16 % at k = 0.01 and to 3.6 % for magnitudes log-uniform over 4 decades. Among close calls (trade-off, |A margin| < 10 % of |ΔU|) it is 49 %. The exact statement is claim 5's: a flip occurs iff c* ∈ (1, r). | `rv7_01_flip_condition.py` §4 |
| 11 | MINOR | Claim 3; OQ-13 | Claim 3's per-phase T₀ needs two dead states in one evaluation, which DEF-DEAD-STATE forbids. GMS-100 evaluates both phases at one T₀ and, for dissipated work, ranks 100 J against 60 J correctly at any T₀. Claim 3 is valid against (B) but describes no GMS-100 failure. Adopting (B), which divides upstream terms by T_ref and operational terms by T₀, would also require revising GMS-000 DEF-DEAD-STATE, not only GMS-100. | `rv7_03_gms100_ledger.py` (c) |
| 12 | MINOR | Claim 2 | "S_gen does not depend on any dead-state choice" is true but incomplete: S_gen depends on the control-volume boundary (where T_boundary is taken), which plays the same role. The answer covers this in part with "T₀,k must be the reservoir that actually receives the heat". | `rv7_05_missed_regimes.py` (b) |
| 13 | MINOR | Claim 4 ("only by accident") | (B) is not right by accident. It is right iff c* does not lie between r and c_op, a determinate condition. "Its implicit rate 1.99 is unrelated to 3" is the accurate part. | `rv7_04_carrier_and_band.py` (b) |
| 14 | MINOR | Not in the answer (supports (A)) | (B) as defined needs the temperature of each site where an upstream loss occurred. CExC tables give lost work at T_ref only, and W/T_site differs from W/T_ref by +9.2 % at 273 K and −4.8 % at 313 K. (B) is therefore not computable from tabulated data; using T_ref is itself a convention, which is the answer's claim 6 last bullet. | `rv7_05_missed_regimes.py` (d) |

## Reproducibility

| Answer location | Stated | Recomputed | Script | Match |
|---|---|---|---|---|
| Question / OQ-13 | about 5 % | 5.06 % (5,057 / 100,000) | `rv7_01_flip_condition.py` | yes |
| Claim 5 | r = 1.028 at 290 K | 1.0281 | `rv7_02_numbers.py` | yes |
| Claim 5; verdict | r = 1.988 at 150 K; "at most 1.99" | 1.9877 | `rv7_02_numbers.py` | yes |
| Claim 5 | iff ΔU·ΔO < 0 and 1 < \|ΔU\|/\|ΔO\| < r | 0 counterexamples either way on 100,000 cases | `rv7_01_flip_condition.py` | yes |
| Claim 5 | \|ΔU+ΔO\| < (r−1)\|ΔO\| on flips | 5,057 of 5,057 | `rv7_01_flip_condition.py` | yes |
| Claim 2 | 6.67e-3, 3.33e-3 J/K | 6.667e-3, 3.333e-3 | `rv7_02_numbers.py` | yes |
| Claim 3 | 0.345, 0.400 J/K; 67 % more | 0.3448, 0.4000; ratio 1.6667 | `rv7_02_numbers.py` | yes |
| Claim 4 | (A) 1010 vs 1000 MJ | 1010, 1000 | `rv7_02_numbers.py` | yes |
| Claim 4 | c_op = 3: 1030 vs 1100 MJ | 1030, 1100 | `rv7_02_numbers.py` | yes |
| Claim 4 | break-even 1.25 | 1.2500 | `rv7_02_numbers.py` | yes |
| Claim 4 | (B) 3.421 vs 3.520 MJ/K | 3.4207, 3.5196 | `rv7_02_numbers.py` | yes |
| Claim 4 | implicit rate 1.99 | 1.9877 | `rv7_02_numbers.py` | yes |
| Claim 6 | Al 33 MJ/kg (±10 %) | 32.93 (888.4 kJ/mol); 29.49 (795.7 kJ/mol, −10.6 %) | `rv7_02_numbers.py` | arithmetic yes; source value UNSURE |
| Claim 6 | 0.11 MJ/(kg·K) | 0.1107 | `rv7_02_numbers.py` | yes |
| Claim 7 | factor 1.93 | 1.9333 | `rv7_02_numbers.py` | yes |

## Derivation checks

**Claim 5 flip condition.** In rv02's variables, ΔU = W_g − W_s and ΔO = T₀(S_g − S_s); rv02's `lw` equals ΔU + ΔO and T_ref · `ent` equals ΔU + rΔO, with r = T_ref/T₀ > 1. Let f(t) = ΔU + tΔO, which is linear in t. f(1) and f(r) have strictly opposite signs iff the root t* = c* = −ΔU/ΔO lies strictly in (1, r), that is, iff ΔU·ΔO < 0 and 1 < |ΔU|/|ΔO| < r. In a flip, |f(1)| = |ΔO|(c* − 1) < (r − 1)|ΔO|. Boundary cases: at c* = 1, (A) ties and (B) is non-zero; at c* = r, (B) ties. rv02's `np.sign` comparison counts both as disagreements, while the answer's strict inequality excludes them. If ΔO = 0 or ΔU = 0, there is no flip. None of these ties occurs in rv02's continuous sample (0 zeros). The condition holds only for one operational environment (finding 6).

**Claim 1 decomposition.** Σ_B · T_ref = Σ_k (T_ref/T₀,k) W_lost,k, so (B) is the case c_k = T_ref/T₀,k; correct. The heat-resource example has a basis error (finding 3).

**Claim 3.** S_gen = W/T₀,k for dissipated work rejected to T₀,k, and W_lost = T₀,k S_gen = W; correct.

**Claim 4.** C(c) = ΔU + cΔO with ΔU = −50 MJ and ΔO = +40 MJ gives c* = 1.25; correct.

**Claim 7.** ∂ ln S/∂ ln T₀ = −1 for S = W/T₀, and 290/150 = 1.933; correct. The same convention also changes (A) for heat-transfer losses (findings 1 and 5).

**Claim 8.** The algebra is correct when T₀,eval is independent of the W_lost,k. "Re-referring each loss as T₀,eval S_gen,k collapses (A) to (B)" is correct: Σ T₀,eval S_gen,k / T₀,eval = Σ S_gen,k.

## Check against E15 and GMS-100

- **(A) against `EQ-LIFECYCLE-LOST-WORK-CURRENCY`.** They match: Σ = (1/T₀) Σ_c B_lost,c, with one T₀ per evaluation and tabulated upstream terms taken as lost work at the source's reference environment without conversion (E15; REQ-LIFECYCLE-REFERENCE-ENVIRONMENT item 1). In GMS-100 the evaluation T₀ is the DEF-DEAD-STATE scenario input and is also the T₀ in Ṡ_gen,phys = Ḃ_lost,phys / T₀. The two forms are numerically identical when the evaluation dead state is the operational environment (`rv7_03` (a)). The answer's decoupled "T₀,eval as a scale only" is not GMS-100's construction (finding 1).
- **Verdict "report in J".** GMS-100 already minimises 𝓛_lifecycle in J (`EQ-LIFECYCLE-OBJECTIVE`). J/K is the same quantity divided by one T₀, so the ranking is the same at a fixed T₀.
- **Claim 3 under DEF-DEAD-STATE.** Not representable (finding 11).
- **Claim 6 against w_lost,ext.** It is the same quantity, already in GMS-100 (finding 7).
- **Claim 7, third defect** (Ex_product destroyed in another environment). Already recorded: REQ-LIFECYCLE-REFERENCE-ENVIRONMENT items 2 to 4, and the Open item for §3.2. GMS-100 deliberately charges b_ch at its source-reference value.
- **Claim 4 against the mixed-basis Open item.** This is OQ-15's problem (finding 4).
- **Open point 2** (chemical exergy off Earth). Partly covered by `EQ-LIFECYCLE-CHEMICAL-EXERGY-TEMPERATURE-SHIFT`, `EQ-LIFECYCLE-CHEMICAL-EXERGY-REFERENCE-SHIFT` and REQ item 4 (no locally referenced b_ch as a resource measure). For an environment with no reference species, it remains outside the range of validity.
- **Open point 1** (free flux). This matches finding 3 and the GMS-100 Open item that the carrier factor does not apply to environment-driven dissipation.

## Missed regimes

1. **The deep-space sink as the environment** (finding 5). r is about 109, and S_gen and heat-transfer lost work both depend on a boundary convention by about ×100. The "effective T₀" must be a declared convention, and it affects (A) through heat-transfer losses as well as (B).
2. **Heat-transfer losses against dissipated work.** Only dissipated work makes (A) independent of T₀. For heat-transfer losses (A) inherits T₀ (finding 1). The answer's examples are all dissipated work.
3. **Staging and boundary.** Heat degraded from 400 K to a 290 K radiator and then radiated to space loses nearly all of its exergy relative to a 2.7 K dead state, but at the radiation step, not in the heat exchanger. How lost work is split between stages depends on the boundary (`rv7_05` (b), (c)).
4. **Upstream site ambient different from T_ref** (finding 14). (B) cannot be computed from tables.
5. **Operation over several environments** (finding 6). The band does not generalise; a box test does.
6. **c_op < 1** (cold-environment heat engines valued at T_ref, free fluxes). The verdict's band lies entirely above 1 (findings 2 and 3).

## Claim by claim

| Claim | Position | Reason |
|---|---|---|
| 1 | Partly agree | The decomposition and "(B) ≡ c_k = T_ref/T₀,k" are correct. c = T_h/(T_h−T₀) is an energy basis, and c_k ≥ 1 fails on an exergy basis at T_ref and for free fluxes. "(A) is closer" is unsupported in general. |
| 2 | Agree, with caveat | S_gen is dead-state-free but depends on the boundary. The falsifier cannot fail. |
| 3 | Agree (as an argument against (B)) | The arithmetic is correct. It is not a GMS-100 case (one dead state), and the falsifier cannot fail. |
| 4 | Agree on arithmetic; disagree on the inference | The failure belongs to the mixed basis (OQ-15), not to the currency. "By accident" is wrong. |
| 5 | Agree | Verified exactly on rv02, but it applies to one operational environment only, and the falsifier is an identity. |
| 6 | Agree on the quantity, disagree on the framing | It is already GMS-100's w_lost,ext. "Overstates" holds stage-wise but not over the life. The Szargut form is UNSURE, and the Al value is at the edge of ±10 %. |
| 7 | Agree, incomplete | 1.93 is correct, and the third defect is already recorded in GMS-100. The T₀ convention also affects (A) through heat-transfer losses. |
| 8 | Disagree for GMS-100 | It holds only for decoupled T₀,eval or T₀-independent lost work, and the falsifier misdiagnoses. |
| Verdict | Partly follows | "(A) for edition 0.1" follows from claims 1 to 3 and agrees with E15. "T₀,eval as a scale only" conflicts with DEF-DEAD-STATE coupling. The band is not protective. The validity range ("real heat-rejection reservoir") is undefined for a radiating spacecraft. |

## What still needs external checking

- c_op, the primary exergy at T_ref per J delivered on board, for real power chains (solar array plus battery, radioisotope, chemical), including launch. No tool in this review can supply it. This is also OQ-15's r_el.
- Szargut's cumulative exergy balance form (CExC = product exergy + cumulative losses, by-product allocation, waste exergy): source needed.
- The aluminium standard chemical exergy (888.4 against about 795.7 kJ/mol) and which value the chosen CExC source uses: source needed (only search snippets were seen here).
- The entropy of radiation emitted by grey radiators (the 4/3 factor is for a blackbody): source needed.
- The dead-state convention for a radiating spacecraft. This is a decision for the user, not a computation; it should be an ADR or scenario-preset note for `configs/dead_states/`.

**Single most decisive check:** obtain a sourced c_op for one real spacecraft power chain, on a stated basis (primary exergy at T_ref per J delivered), and place it against 1 and r = T_ref/T₀. If c_op lies near 1, (A) without correction is adequate. If c_op lies well above r or below 1, both currencies misrank, and the fix is the carrier factor of OQ-15, not a change of currency (OQ-13). Either way, the result moves the decision from OQ-13 to OQ-15.

Sources for finding 8 (search results only; papers not read):
- [Standard chemical exergy of elements updated (Rivero and Garfias, Energy 2006)](https://www.sciencedirect.com/science/article/abs/pii/S0360544206000569)
- [Standard Chemical Exergy, ScienceDirect topic page (table credited to Szargut et al.)](https://www.sciencedirect.com/topics/engineering/standard-chemical-exergy)
- [Towards an International Reference Environment of Chemical Exergy (Szargut et al. 2005)](https://www.exergoecology.com/exergoecology/szargut2005)
- [Appendix 1, Standard chemical exergy (MIT course reading)](https://web.mit.edu/2.813/www/readings/APPENDIX.pdf)
