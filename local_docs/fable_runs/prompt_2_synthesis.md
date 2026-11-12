# Prompt 2 synthesis (orchestrator)

Date: 2026-11-12. Inputs: `prompt_2_answer.md` (S4, `fable` high) and `prompt_2_review.md` (S5, `opus` high), checked against the current text of GMS-100 (fixed after review r1, not accepted). Everything here is level `derived`: two models agreeing is not validation (S16). All numeric examples use made-up inputs. They show mechanisms, not how large the effects are.

## Result

The GMS-100 accounting is **internally repairable**. The answer and the review agree on the algebra. The review downgrades the answer's only BLOCKER to a convention choice: 0 BLOCKER, 3 MAJOR (1 conditional), 9 MINOR. Reproducibility is good: all 7 scripts re-run byte-identical. Every number in the answer that the reviewer checked matches the saved outputs. The reviewer's independent quadrature reproduces the spectral rows to 3e-4 or better.

**Agreed by both (algebra checked independently):**

- **Q2, dispersal.** The current EOL terms never charge `b_ch` for the dispersed fraction 1 − R_rec. So extraction is *not* charged exactly once in exergy terms: the prompt's ledger is short by (m + 1)(1 − R)·n·b. Charging `b` at dispersal plus `CExC − b` at make-up closes the ledger exactly, with no double count. The reviewer confirmed this from mass flows (agreement 1.4e-15). Corrected terms:
  - `Σ_s,EOL = (n/T₀)[R·w_remelt + (1 − R)·b]`
  - `Σ_g,EOL = (1/T₀)Σ_i n_i[R_i·w_remelt,i + (1 − R_i)·b_i]`
  - `Σ^ret_EOL = (1/T₀)Σ_i n_i[R_i·w_remelt,i + (1 − R_i)·CExC_i]`

  This answers the GMS-100 open item "whether the EOL terms charge b_ch". It refines U1 rather than overturning it: the count 1 + m(1 − R) of virgin extractions still holds when w_conv is held fixed.
- **Q5, CExC.** CExC cannot be transformed to another dead state: it is a path tally over one Earth supply chain. `b_ch` can be transformed: there is a Gibbs–Helmholtz formula in T₀ and a reference-species formula. In low-Earth orbit the reference species are absent, so a locally referenced `b_ch` is not a resource measure.
- **Q3, allocation.** The framework is closest to closed-loop recycling inside the horizon with no-credit (cut-off-like) ends. In circular-footprint terms that is A = 0 with the outgoing quality ratio set to 0, which is not a standard parameter set. It is defensible as an entropy ledger, which has no negative entries. For a single life (the incumbent), it is harsher than every named method. Per kJ/mol in the example:

  | Method | Charge (kJ/mol) |
  |---|---|
  | Framework | 1140 |
  | Cut-off | 1100 |
  | 50:50 | 680 |
  | Circular footprint (A = 0.2) | 428 |
  | Avoided burden | 260 |

  No widely adopted exergy-specific rule for end-of-life allocation was found.
- **Q4, asymmetry.** "Charging the incumbent only extraction + transport always favours the incumbent" is **not true in general**. The true part: omitted incumbent stages are non-negative, so they never turn a real loss into a reported win. A "geometry wins" verdict is therefore robust to them, and a "geometry loses" verdict is not. The answer's counterexample charges an oxide incumbent with the metal's CExC. The reviewer notes the sign depends on the production route: an oxide made from refined metal reverses it. Either way, GMS-100's sentence "favours the incumbent material" (§3, `EQ-LIFECYCLE-INCUMBENT-INITIAL-CAPITAL` assumptions) is too strong.
- **Q6, recovery test.** The budget omits channels (cold sky, cold reservoirs, wind, stored or imported exergy), so it is not an upper bound on available exergy. "Fails → infeasible" is therefore not justified. The example verdict flips for a sky colder than 219.47 K. This confirms the earlier triage note for round 2 in `orchestrator_state.md` §4. On diluted or diffuse sunlight, the undiluted Landsberg factor overestimates, which is the safe direction for a necessary condition. "Lower bound" is the wrong word for the budget; the consequence is agreed.
- **Q1, basis.** The material terms are cumulative (they include the upstream losses of energy carriers). Operation, manufacturing and computation are charged delivered energy only (GMS-100 §4, computation assumptions: "the electrical energy delivered to the computing hardware"). This is an omission that reweights material against operation, not a double count. In the made-up example the verdict flips at r_el ≈ 1.89. The reviewer adds that the correction applies only where dissipation is fed by a purchased carrier.

**Where the reviewer disagrees with the answer:**

1. **L1: dividing upstream losses by a non-standard T₀.** The answer rates this a BLOCKER; the reviewer rates it a MAJOR *convention*. The framework's `W/T₀` ledger is a lost-work ledger divided by one constant, which is the literal reading of "lost work / T₀". The answer's entropy ledger (each loss divided by the T₀ of the environment where it occurred) is also valid. The two disagree in about 5 % of random cases. The answer's claim that they give the same decisions is circular. No tool settles this: it is a choice of currency.
2. **L8: λ_ℰ.** The answer says λ_ℰ is an average share, not a marginal one, and proposes the marginal value. The reviewer points out that the average share is the right figure for the all-or-nothing case, which is exactly what "credited only if x leaves the whole system" describes. The real defect is different: one product's credit depends on the infrastructure disappearing, an event that another product's choice can veto. In that scenario the answer's marginal default under-credits by 134 J/K per unit.
3. **L16: by-product elements.** The answer rates this MINOR; the reviewer rates it MAJOR for by-product elements (UNSURE). Szargut-type tables may use substitution credits for by-products, and scarce elements are often by-products, so CExC(x) may be set by an allocation rule.
4. **Smaller points:**
   - **L7:** the cold-source sign error exists only if q_thermal is recorded as a non-negative magnitude.
   - **V9:** Carnot at T_sun is not provable for real sunlight, whose brightness temperature exceeds 5772 K in parts of the spectrum (UNSURE).
   - **S4-B:** the answer's event-ledger check is a tautology.
   - **L10:** the scrap correction omits the dispersal term `b`.
   - **L11, L4:** severities are overstated.

**Already handled by the current GMS-100 text** (the prompt was written from the source draft, before the r1 fixes):

- **L7:** `EQ-LIFECYCLE-INTERCEPTED-EXERGY-FLUX` already restricts q_thermal to sources above T₀. The cold sink is listed in Open items, so L7 merges into the Q6 channel finding.
- **L11:** `EQ-LIFECYCLE-LANDSBERG-EFFICIENCY` already gives the formula. 0.933 is only an example value, and T_sun is listed in Open items.

**Single most decisive external check (reviewer):** the documentation of the CExC(x) data source the framework will use. We need to know whether it includes the ore's own exergy, which by-product rule it applies, and whether it includes capital goods. That one fact conditions the Q2 closure, the λ_ℰ double count (L9), the by-product issue (L16) and the oxide counterexample (L5). GMS-100 does not name a source yet.

## Implications for the project

- **GMS-100 round 2** (the next loop step) should take these as fixes. Round 2 is the last round, so anything not fixed becomes an OQ and an `## Open items` entry. Four current Open items get an answer:
  - dispersal of b_ch (D1);
  - the dead state for CExC and b_ch (D2);
  - asymmetry (narrowed by D5);
  - w_conv ≥ 0 (D7).
- **Two r1 user decisions are refined, not reversed:** U1 (extraction once: still holds; dispersal is added) and U3 (necessary condition: kept; the decision rule needs narrowing or more channels).
- **Tier 2 (manufacturing yield):** the scrap formula (L10, plus the reviewer's dispersal term) belongs to the yield document, which GMS-100 already defers to.
- **Scenarios:** any LEO or cold-dead-state scenario needs D2 decided first.
- **Citations usable as candidate anchors** (record-level only, no full text read): Szargut et al. 1988 and Szargut 2005 (CExC); Morris & Szargut 1986 and Rivero & Garfias 2006 (`b_ch`); PEF Guide 2013/179/EU Annex II §5.4.7 (50:50); EU 2021/2279 (circular footprint formula); Petela 1964; Landsberg & Tonge 1979, 1980; Buddhiraju, Santhanam & Fan 2018 (153.1 W/m² sky-sink limit at 300 K / 3 K); Ekvall & Weidema 2004 (marginal against average). ISO 14044 clause numbers stay UNSURE.

## Decisions for the user

**Decided 2026-11-12: the user accepted the recommendation for D1–D7.** Recorded as E14 (D1), E15 (D2) and E16 (D4) in drafting notes §A; OQ-13, OQ-14 and OQ-15 and the GMS-100 round 2 fix items (D3, D5, D6, D7) in `orchestrator_state.md`; the scrap formula as a GMS-210 brief note.

| # | Decision | Options | Recommendation |
|---|---|---|---|
| D1 | Dispersal of `b_ch` (Q2) | (a) charge `b` at dispersal: the corrected Σ_s,EOL, Σ_g,EOL and Σ^ret_EOL above, with "both sides retired at τ" written into the Σ_g,EOL definition (reviewer F12: it charges the in-service unit's dispersal at τ); (b) do not charge it, and state that extraction is charged once in CExC − b terms only | (a): both reviewers agree; it closes the ledger and answers an existing open item |
| D2 | Currency across dead states (Q5, L1) | (a) lost-work currency: keep Σ = Σ_k W_k / T₀ and state it explicitly; upstream terms are Earth-side lost work from tables at the reference environment; (b) entropy currency: Σ = Σ_k W_k / T₀,k with T₀,k the environment where the loss occurred; (c) restrict 0.1 to T₀ = T_ref and leave non-standard dead states as an OQ | (a) for 0.1, with (b) recorded as the alternative in an OQ. (a) is the current equations' literal reading and needs no new symbol. Either way, add as a REQ: CExC is never transformed; `b_ch` may be transformed with the stated formulas |
| D3 | Recovery test channels (Q6) | (a) narrow the decision rule to "infeasible on intercepted solar and thermal exergy alone" and keep the omitted channels as an Open item; (b) add a bounded sky-sink term (σT₀⁴/3 per m² for a deep-space sink) and list the other channels as budget lines; (c) both | (a). (b) is the sharper fix, but adding the deep-space bound makes the test nearly vacuous on Earth (153 W/m² against about 187 W/m² mean solar in the example). With (a), the triage note's "η_ex rejected" decision still stands |
| D4 | λ_ℰ (Q7) | (a) keep U2 (average share) and add: λ_ℰ applies only when x leaves every product that shares B_infra(x) (the all-or-nothing case), plus a REQ that CExC(x) must exclude capital goods whenever λ_ℰ > 0; (b) switch to the marginal value ∂B_infra/∂N (the answer's V7) | (a): the reviewer shows (b) under-credits in exactly the scenario the framework defines. The multi-product veto becomes an OQ |
| D5 | Boundary asymmetry wording (Q4) | (a) replace "favours the incumbent material" with the true part: omitted incumbent stages are non-negative, so "geometry wins" verdicts are robust to them and "geometry loses" verdicts are one-sided. Add that CExC must be for the chemical form of x actually used. Symmetrisation stays OQ-9; (b) symmetrise now (the answer's L5 boundary) | (a): it fixes a false statement without new data. (b) needs incumbent manufacturing data the 0.1 scenarios do not have |
| D6 | Mixed basis (Q1, L4) | (a) state in GMS-100 that material terms are cumulative while operational, manufacturing and computation terms are delivered energy; record this as a known bias and an OQ; (b) add a carrier factor r_el to the carrier-fed terms (Σ_comp, and tier 2 for Σ_mfg_eff) | (a) for 0.1: there is no source for r_el yet, and the reviewer notes it does not apply to environment-driven dissipation |
| D7 | Data-source requirements and minor fixes | One REQ on the CExC source: (i) it includes the ore's exergy, (ii) it uses the same reference environment as `b_ch`, (iii) its by-product rule is declared, (iv) inclusion of capital goods is declared (see D4), (v) it is for the form of x used. Make w_conv ≥ 0 an input check. Pass the scrap formula (L10 plus the reviewer's `b` term) to the yield document as a brief note | Adopt. (i)–(v) turn the reviewer's decisive check into a requirement on whoever picks the data |

If you accept, I would record them as follows:
- D1, D2 and D4 as new corrections E14–E16 in drafting notes §A;
- D3, D5, D6 and D7 as round 2 fix items in `orchestrator_state.md` §4;
- the alternatives and the multi-product veto as new OQs.

Nothing in the spec changes until round 2 runs.

## Cost

| Stage | Model | Time | Tokens | Tool calls |
|---|---|---|---|---|
| S1 planner | `fable` high | 20 min | 188k | 6 |
| S2 implementer | `sonnet` | 3 min | 99k | 11 |
| S3 citations | `sonnet` | 4.5 min | 196k | 86 |
| S4 finaliser | `fable` high | 7 min | 174k | 11 |
| S5 reviewer | `opus` high | 9.5 min | 227k | 31 |

Fable used 362k tokens, against 286k for the single-pass Prompt 1a. The split did not save Fable tokens here, because Prompt 2 is almost all judgement, as §4 predicted. It did keep Fable's tool calls to 17 (against 70) and moved all computation and the citation searches to Sonnet. S4 was not skipped: 8 citations were not verified, and S2 raised 6 issues. S4 used them: it rebuilt R14 from the prompt's formulas, reconciled r_el, and dropped 6 citations it could not support.
