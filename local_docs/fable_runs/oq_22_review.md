# OQ-22 check: adversarial review (`opus`)

Context file (`local_docs/`, never cited by the spec). Written 2026-11-15 by the reviewer. Level: every statement here is a claim at level `derived` (unverified). Agreement with the answer is not validation.

Review code: `oq_22_review_code/rv01_independent_check.py`, output `oq_22_review_code/rv01_independent_check.txt` (cited below as "rv01 line N"). The script does not import the answer's scripts or read its CSVs. It builds GMS-100's terms in molar form, evaluates f(τ) directly and finds Δη_be as the root of f by bisection. Downloads are in `oq_22_review_code/raw/` (Nuss and Eckelman main article only).

## Summary verdict

1. Every number in the answer reproduces from its scripts (byte-identical re-run), and an independent molar-form root of f(τ) matches the central set to 0.0001 mV. **"Nearly free" holds for the central set as the brief defines it** (maximum 1.62 mV).
2. It holds only for that set. It fails for Ir at 1 to 2 mg/cm² in four plausible cases: (a) the revenue allocation is redone at 2024 to 2026 Ir prices (9.0 to 24 mV, above 10 mV in 5 of 6 cases); (b) low-throughput renewable duty, 3e3 to 6e3 A·h/cm² (14 to 29 mV); (c) an ERC-type term (20 mV); (d) GMS-100's own shared-loop rule (f_max), which gives "conditional", not "incumbent wins", over a band that can reach 10 to 35 mV.
3. The answer misreads one case. With mass allocation and g_high, Δη_be < 0 means **the incumbent wins** at zero penalty. It does not mean "the candidate wins".
4. Minimal safe statement: GMS-100 has no depletion term. Its unconditional material terms are worth at most about 2 mV at continuous duty. In E18's own case the verdict is set by Σ̇ in both directions (NiFe ahead in alkaline: moot; PEM vs AEM at cell level: +50 to +1160 mV). E18's sentence should say "rests on Σ̇", not "on scarcity".
5. Part B: "mix of B and C" is inference, not evidence; B is unsupported. α = 0.84 to 0.95 follows from the definition used: with "fixed part" read as loop capital only, α = 0.20 to 0.70. The Prompt 8 flip value 0.804 lies between the two readings.

Counts: BLOCKER 0, MAJOR 7, MINOR 8.

## Findings

| # | Severity | Location | Finding | Evidence |
|---|---|---|---|---|
| 1 | MAJOR | `outputs/issues.md` item 11; `oq22_part_a.txt` A5 footnote ("so the candidate wins for any Delta_eta >= 0") | **Sign of the verdict inverted.** Δη_be < 0 means the candidate must be *more* active to win; at Δη = 0, f > 0 and the incumbent wins. The answer body says only "Δη_be < 0", but the outputs state the wrong verdict, and the brief asked about this claim. With g_low the same rows have Δη_be > 0, so the sign depends on the side-g bound, not on Ir. | rv01 lines 40, 42, 44: "f at d_eta = 0: +1.437e+05 ... INCUMBENT wins (f > 0)"; lines 41, 43, 45 (g_low: candidate wins) |
| 2 | MAJOR | Answer Part A "λ_ℰ estimate" column; Summary "λ_ℰ ... adds 0.8 to 29 percent" | **The λ_ℰ column is not GMS-100's verdict quantity for Pt or Ir.** Their loops are shared (N_share < N_alloc), so REQ-LIFECYCLE-SHARED-INFRASTRUCTURE-VERDICT applies: the candidate wins unconditionally below Δη_be(f₀), the incumbent wins unconditionally only above Δη_be(f_max), and the band between is "conditional". f_max credits b_infra·m″/(T₀·s), where s is the product's share of loop throughput. At s = 0.01, Ir 2 mg/cm² gives Δη_be(f_max) = 11 (mid) to 35 mV (hi). Below about 1.2 mV GMS-100 says the candidate wins; between about 1.2 and 35 mV it says "no verdict for the product alone". It never says "incumbent wins, scarcity unpriced". The brief's convention 10 asked for λ_ℰ, so this is partly inherited, but the answer's E18 conclusion rests on it. | rv01 lines 141, 143, 145-146; GMS-100 lines 313-324 |
| 3 | MAJOR | Answer "Not settled", last bullet ("allocation rules by 1.7× for Ir"; "no input read is that uncertain") | **A plausible change to the allocation moves Ir 2 mg/cm² to "between" at the central case.** Table S38 allocates by revenue at 2006-10 prices: Ir 15,919.87 $/kg (495 $/oz), on the same S38 row. At 2024 to 2026 Ir prices (snippet, UNSURE) and a basket revenue factor r of 0.8 to 1.3 (MEMORY), Ir's CED scales by 7.4 to 19.8. Ir 2 mg/cm² then gives 9.0 to 24.3 mV (5 of 6 cases "between"), and Ir 1 mg/cm² up to 12.1 mV. The 10 mV line needs κ ≈ 8.3. This is also the clearest case of the data, not the framework, bringing in price scarcity (condition 3). | rv01 lines 118, 127-133; S38 price column (answer raw `nuss/s1.txt` line 7512 block) |
| 4 | MAJOR | Summary bullet 5 ("So E18's ... is reversed for this case under GMS-100's own terms") | **The conclusion goes beyond the duty set.** Δη_be ∝ 1/(j·τ) exactly. 10 mV is reached at throughputs of 9.6e3 (Ir 2), 4.7e3 (Ir 1) and 3.3e3 (Pt 0.5) A·h/cm². Renewable-coupled scenarios (MEMORY) at 6.1e3 and 3.3e3 A·h/cm² give Ir 2 at 15.7 and 29.3 mV, Ir 1 at 14.4 mV and Pt 0.5 at 10.2 mV. These are the duties AEM and PEM electrolysis is built for. The answer's grid shows the corner (24 mV), but the verdict omits it. | rv01 lines 60-70 |
| 5 | MAJOR | Answer as a whole (no test of the case E18 names) | **E18's own case was not tested.** E18 names Ir/Ru oxide to NiFe at the alkaline/AEM electrode, compared at cell level. In alkaline half-cells NiFe LDH beats IrOx/IrO₂ (Δη = −34 to −48 mV, snippet), so the question is moot: the candidate wins on Σ̇ alone. A PEM (IrO₂) vs AEM (NiFe) cell-level comparison gives Δη = +50 to +1160 mV, which is 31 to 716 times the largest central Δη_be: Σ̇ decides. Either way the case rests on Σ̇, and Σ_init decides only in a band of at most ±2 mV. | rv01 lines 92-97 |
| 6 | MAJOR | Part B, B5 "Configuration: MIX of B (probable) and C (certain in kind). Not A." | **Unsupported as evidence.** B: the SI is silent, and the main article (reviewer download) has no "infrastructure" or "capital good" string. "ecoinvent usually includes infrastructure" is MEMORY. One search result suggests some older ecoinvent metal datasets lacked infrastructure (UNSURE). C: the 17 to 27 percent share counts ventilation, cooling and holding furnaces as "monitoring, assaying and maintaining flows". The spec's B_infra is the loop's monitoring, assaying and maintaining, not production ventilation. Only C "in kind" (site-total energy contains site monitoring and maintenance) is a fair inference. The answer itself says A cannot be told from C. Defensible statement: undetermined between C and B+C; A is excluded only by inference. | `oq22_part_b.txt` lines 88-93; reviewer grep of the main article (no match); search note in "What still needs external checking" |
| 7 | MAJOR | Part B, B4 "α = 0.95 / 0.91 / 0.84" | **α follows from a definition.** The answer puts all fixed operating energy into the fixed part F and counts all of it as avoidable, so α is close to 1 by construction. With F = loop capital (the "establishing" part, as in Prompt 8 (b)), α = a_cap = 0.20 / 0.45 / 0.70. Prompt 8's rv03 joint verdict flips at 0.804, which lies between the two readings. The bracket does not settle which side of 0.804 a real loop is on, and every input is MEMORY. | rv01 lines 151-154 |
| 8 | MINOR | Summary bullet 2 ("or j·τ 25 to 340 times smaller") | Mismatch with the output. For Pt 0.1 mg/cm² j·τ must fall by 453, not 340; the CExC and j·τ levers differ because side g does not scale with CExC. | `oq22_part_a.txt` A6: "j*tau: divided by 453.3"; rv01 line 35 |
| 9 | MINOR | Part A, under the term table ("Transport term ... 7 to 67 J/K per m² (≤ 5e-6 of Σ_s,init)") | Mismatch: the minimum is 3.35 J/K (Pt 0.1), and the Ir share is 5.92e-6, above 5e-6. No effect on any class. | `oq22_part_a.txt` A2 row "Pt 0.1 ... 3.35"; rv01 lines 29-33 |
| 10 | MINOR | Pt rows (convention 2 applied to the PEM cathode) | NiFe LDH is an OER catalyst and is not stable in acid. A NiFe candidate is not a functional HER replacement for Pt (Ni or NiMo in alkaline would be). Numbers are insensitive, since side g is ≤ 26 percent of Σ_s,init. | answer Part A inputs table; A2 g-side shares |
| 11 | MINOR | `oq22_common.py` `side_g(erc=True)` | The ERC of Ni and Fe is multiplied by the precursor factor ψ = 3. A depletion cost is not a processing cost. Effect: 8.19 vs 8.22 mV for Pt 0.5. | `oq22_part_a.txt` A7(b) "8.1863"; rv01 line 123 "8.22" |
| 12 | MINOR | `oq22_common.py` λ for Ir | Ir gets Pt's b_infra/CExC fraction. Ir is 0.43 percent of ZA revenue (S30), so the share of loop exergy that leaves with Ir is likely far below Pt's. This overstates Ir's λ, a conservative direction for "nearly free". | `data/nuss_pgm_allocation.csv` rev_share Ir 0.0043 |
| 13 | MINOR | `alloc_factor` "mass_all" | Mixes S28 masses (1970-92) with S30 revenue shares (2006-10 prices). The factor is a ratio of two different bases. | `oq22_common.py` docstring of `alloc_factor` |
| 14 | MINOR | Remelt proxy | Uses secondary/mix (0.049), not secondary/primary (0.039), and scales with the allocated CExC in A5. The remelt cost should not depend on the primary allocation. Effect < 1 percent. | `oq22_common.py` `w_remelt_kg` |
| 15 | MINOR | A3 footnote vs `issues.md` item 3 | A3 calls the Thanatia M&M value "exergy"; issues item 3 says its definition is not stated. The labels are inconsistent. | `oq22_part_a.txt` A3 footnote |

## Reproducibility

| Item | Result | Evidence |
|---|---|---|
| `oq22_part_a.py` re-run with `.venv/bin/python -B` | byte-identical to `outputs/oq22_part_a.txt` | `diff` empty |
| `oq22_part_b.py` re-run | byte-identical to `outputs/oq22_part_b.txt` | `diff` empty |
| Answer numbers vs output lines | all match except findings 8 and 9. Derived ratios in the text (84 and 1200 "short of", needed/hi) are hand arithmetic on output values, correct, but not printed by a script | checked line by line against A1-A9, B1-B5 |
| Independent recomputation (own code, molar form, bisection root) | central set matches to ≤ 0.0001 mV | rv01 lines 15-22 |
| LOOKUP spot checks in the raw files | S38: Ir ZA 165000, RU 175000, TOTAL 169000; Pt ZA 308000, RU 327000, secondary 11900 MJ/kg: match. Szargut 2005 b_ch: Pt 140.97, Ir 256.56, Ni 232.71, Fe 376.99 kJ/mol: match. IntechOpen Table 1: Pt ERC 4,491,688, M&M 291,667 GJ/t: match. The same table has "PGM (average value for all PGM)" 2,695,013 / 175,000 and Pd 8,983,377, which the answer did not use for Ir | reviewer grep of `oq_22_code/data/raw/{nuss,exergoecology,intechopen}` |
| Web spot checks | Buchspies et al. 2017, *Minerals* 7(11):225, "PGE Production in Southern Africa, Part II: Environmental Aspects": confirmed (0.60 TJ CED fossil per kg 6E PGE). Nuss and Eckelman 2014, PLoS ONE e101298: confirmed; main text says LCIs linked to ecoinvent 2.2 in SimaPro 8 and is silent on infrastructure | web search; `raw/nuss_main/t.txt` |
| Identity checks | the answer flags its identity checks correctly. Mine: R1 root vs closed form, R2 (same scenario inputs), R12 (recomputes the answer's α) are by construction, not passes | rv01 line 159 |

## Derivation check

- **Rearrangement.** f(τ) = Σ_g(τ) − Σ_s(τ) − λ_ℰ (EQ-LIFECYCLE-PARITY-FUNCTION), with Σ_k(τ) = Σ_k,init + Σ̇_k·τ + Σ_k,EOL (τ_wearout = ∞, K_ox = 0) and Σ̇_g − Σ̇_s = j·Δη/T₀. Then f < 0 ⇔ Δη < T₀[Σ_s,init + Σ_s,EOL + λ − Σ_g,init − Σ_g,EOL]/(j·τ). This is the brief's convention 3. Checked numerically: f changes sign at the root, negative below it (rv01 lines 5-9).
- **Units.** n [mol/m²]·(CExC − b_ch) [J/mol]/T₀ and j [A/m²]·Δη [V]·τ [s]/T₀ are both J/(K·m²) (rv01 line 10).
- **Terms, sign and boundary.**
  - EQ-LIFECYCLE-INCUMBENT-INITIAL-CAPITAL: n(CExC − b_ch) + M_s·b_transport, with M_s the catalyst mass. This is right if supports are identical, but at cell level they are not (see Missed regimes).
  - EQ-LIFECYCLE-INCUMBENT-EOL: R·w_remelt + (1 − R)·b_ch with no virgin make-up. Right for the horizon unit.
  - EQ-LIFECYCLE-GEOMETRY-INITIAL-CAPITAL: Σ n_i·w_lost,prec,i + M_g·b_transport + Σ_mfg, tooling = computation = 0. w_lost,prec = ψ·w_lost,ext with ψ ≥ 1, so extraction is inside it, as the spec requires.
  - EQ-LIFECYCLE-GEOMETRY-EOL: R_rec = 0, b_ch only. Right.
  - EQ-LIFECYCLE-SUPPLY-CHAIN-COST: λ = b_infra·m″/T₀ under equal loading. Algebraically right, but see finding 2: for a shared loop the verdict uses f₀ and f_max, not λ.
  - Nothing is double counted inside Part A. The "λ on top of CED" double count of loop flows is named by the answer itself (Part B).
- **What GMS-100 charges for scarcity, term by term.**
  - At dispersal GMS-100 charges b_ch, which is not a scarcity measure. Per kg, dispersing Fe costs 9.3 times more than dispersing Pt (Fe 6.75 vs Pt 0.72 MJ/kg; rv01 lines 51-55).
  - No GMS-100 term is a depletion measure. Scarcity can enter only indirectly: through CExC (ore grade, and the data source's allocation rule, finding 3) and through B_infra (loop exergy, not depletion).
  - "GMS-100's terms do not price depletion" is therefore a property of the framework. "The magnitude is about 1 mV" is a property of the CED data at 2006-10 revenue allocation.

## Missed regimes (numbers from rv01)

| Regime | Result | "Nearly free" holds? |
|---|---|---|
| Low duty / renewable-coupled (Q = j·CF·8760·years; MEMORY scenarios) | Q for 10 mV: Ir 2 9.6e3, Ir 1 4.7e3, Pt 0.5 3.3e3 A·h/cm². PV 7 y part load (6.1e3): Ir 2 15.7 mV. Off-grid PV 5 y (3.3e3): Ir 1 14.4, Ir 2 29.3, Pt 0.5 10.2 mV (lines 60-70) | **No** for Ir ≥ 1 and Pt 0.5 below about 1e4 A·h/cm² |
| Standby | no current, no Σ̇ difference; it acts only through τ (life in operating hours), so it falls under the throughput row | as above |
| Incumbent replaced, PGM recycled at overhaul (Open-item R_s form; not evaluable in 0.1) | Ir 2: L = 1e4 h gives 2.4 mV (R_rec 0.9), 5.5 (0.5), 9.4 (0). Pt 0.5 ≤ 3.4 mV (lines 77-82). GMS-100 0.1 returns "no outcome" here whenever f ≥ 0 | yes in magnitude. The 0.1 verdict is "candidate wins" or "no outcome", never "incumbent wins" |
| Candidate (NiFe) short life, replaced | lowers Δη_be. Ir 0.2 and Pt 0.1 turn negative at L_g ≤ 1e4 h (lines 84-87) | yes (stronger) |
| Δη ≤ 0 (NiFe as good as or better than IrO₂, alkaline) | −34 to −48 mV half-cell (snippet) (lines 93-94) | moot: the candidate wins on Σ̇ alone |
| Cell level, PEM (IrO₂) vs AEM (NiFe), membrane and ohmic terms included | Δη = +50 to +1160 mV against Δη_be ≤ 1.62 mV (lines 95-97). Changing the PTL on side g (0.35 kg/m² Ni, MEMORY) moves Δη_be by only 0.013 mV (line 99). GMS-100's parity removes one x at a time, but a PEM-to-AEM swap removes Ir, Pt, Ti and fluoropolymer together; the pairwise test does not represent that | moot: Σ̇ decides |
| Loss rising with age (not representable in GMS-100's profile) | break-even drift difference 2·Δη_be/τ = 0.030 µV/h (Ir 2), 0.010 (Pt 0.5) (lines 105-109). Reported drifts: PEM 1.5 to 35, NiFe AEM 0.7 to 84 µV/h (snippet) | the material term is far below any measurable drift difference; drift decides |
| CExC well above CED (κ) | 10 mV needs κ ≈ 8.3 (Ir 2), 24 (Pt 0.5); κ = 2 to 3 (Buchspies vs Nuss gap, ore-grade decline) gives ≤ 3.6 mV (lines 116-120) | yes |
| ERC added (not a GMS-100 term) | Pt 0.5: 8.2 central, 16.4 at j = 0.5, 164 at the low corner. Ir with the PGM-average ERC as a proxy: Ir 2 19.9 (between) central, 39.8 (priced) at j = 0.5; Ir 1 9.95 (lines 122-126) | **no** for Ir 2. The answer did not compute Ir, though the table has a PGM-average row |
| Revenue allocation at current Ir prices | Ir 2: 9.0 to 24.3 mV; Ir 1 up to 12.1 (lines 128-133) | **no** for Ir 2 in 5 of 6 cases |
| Shared loop, f_max (GMS-100's own rule) | Ir 2: band up to 11 to 35 mV at s = 0.01, 100 to 342 at s = 0.001 (line 141) | the incumbent-win verdict needs Δη above that band. Between about 1 mV and the band edge the verdict is "conditional" |

**Cases where every alternative reading gives a wrong verdict.**

- **Shared loop.** Take Ir 2 mg/cm², s = 0.01, Δη = 5 mV. The CED stand-in, ERC-added Pt (Ir not computed), and λ_mid and λ_hi readings all classify this as "candidate loses". GMS-100's verdict is "conditional" (f₀ ≥ 0 and f_max < 0).
- **Short-life incumbent.** Take τ_wearout,s < τ with f ≥ 0. Every reading implies "incumbent wins"; GMS-100 says "no outcome".
- **Mass-allocation rows with g_high.** The answer's reading says "candidate wins"; GMS-100 says "incumbent wins" at Δη = 0.

## Part B

- **Decomposition.** The stage split (Buchspies shares applied to the CED row) is arithmetic on an assumption the answer states; its numbers match B2. No source splits capital, maintenance or fixed vs variable flows, and the answer says so correctly.
- **B_infra and α.** Every input is MEMORY. The corners are the true extremes of the stated ranges: b_infra rises with α_x, f_op and a_cap, and with c when a_cap > f_op, which holds at both corners. But α depends on the definition (finding 7), and α_x for Ir is not Pt's (finding 12).
- **Configuration.**
  - C in kind: plausible inference. Its size is unsupported, because it counts production ventilation as "maintaining".
  - B: unsupported; checked, both the SI and the main article are silent.
  - A: excluded only by the inference about C.
  - Verdict: "undetermined between C and B+C". "Mix of B and C" overstates the evidence.
- **REQ-LIFECYCLE-CEXC-SOURCE failures of the CED source, as published.**
  - 1: not met (no ore exergy).
  - 2: not met (no reference environment).
  - 3: met (revenue, 2006-10 prices; the price year should be recorded, finding 3).
  - 4: not met, because the declaration is missing. The second clause also bites: B_infra always enters through f_max for a shared loop, so capital goods must be shown excluded "whatever the value of λ_ℰ".
  - 5: not met for the forms actually used (IrO₂, Pt/C).
  - 6: not met (no declaration).
  - The answer's list (4, 6, and 1, 2, 5) is right.
- **What an evaluation would have to remove.** The answer's figures (loop capital 2.4e3 to 7.3e4 MJ/kg; avoidable fixed flows 2.0e3 to 4.0e4 MJ/kg) are bracket arithmetic on MEMORY inputs, not a decomposition.

## Minimal safe statement

The narrowest claim that survives every regime tested:

> GMS-100 0.1 has no term that measures depletion: dispersal is charged b_ch, which for Pt is smaller per kg than for Fe, and λ_ℰ prices avoidable loop infrastructure, not scarcity. With CExC from the CED data read (any published row, κ 0.8 to 3), the unconditional material terms of a Pt or Ir loading of ≤ 2 mg/cm² are worth ≤ about 2 mV of overpotential at throughput ≥ 8e4 A·h/cm², scaling as 1/(j·τ). The candidate therefore wins unconditionally only if its time-averaged penalty is below that. Above it, for a shared loop, GMS-100 returns "conditional" up to Δη_be(f_max), whose size is not established.

What this implies for E18:

- "The substitution case rests on scarcity (Σ_init), not on Σ̇" is not supported, in either direction:
  - In the alkaline/AEM case E18 names, NiFe is at least as active as IrO₂ (Δη ≤ 0), so the case rests on Σ̇ and durability.
  - At cell level against PEM, Δη is 31 to 716 times the largest Δη_be.
- A safe replacement: "In GMS-100's terms the material of a mg/cm² PGM loading is worth of order 1 mV of overpotential at continuous duty; the substitution case is decided by Σ̇ (cell voltage and its drift). GMS-100 does not price depletion; whether it should is open."
- Keep the two claims apart:
  - "GMS-100's terms do not price scarcity" is a property of the framework (R5, and the λ_ℰ definition).
  - "The magnitude is about 1 mV" is a property of the data: the CED stand-in at 2006-10 revenue allocation. An allocation at current prices, or an ERC-type term, moves Ir 2 mg/cm² into "between" (findings 3 and 5 rows above).

The Fable follow-up's trigger ("finding holds") is met for the central set. Its prompt should carry findings 2, 3 and 4, so it does not treat "nearly free" as duty- and data-independent.

## What still needs external checking

- A sourced CExC (exergy, ore included) for Ir and Pt, with a declared allocation rule and price year (conditions 1 to 3, 5). The reviewer did not find one; the Bösch CExD factors and Calvo et al. 2018 remain unread. UNSURE.
- The Ir ERC. Only the "PGM average" proxy exists in the table read. UNSURE.
- Ir and basket prices for a current-price reallocation: snippets only (2024 average 4762 $/oz; Aug to Oct 2026 7850 to 8200 $/oz); the basket factor r is MEMORY. UNSURE.
- Whether the ecoinvent 2.2 PGM datasets include infrastructure (condition 4). One search hint points the other way. UNSURE.
- The product's share s of Ir and Pt loop throughput (sets the f_max band). UNSURE.
- The alkaline and cell-level Δη and drift values: web snippets, mixed temperatures and electrolytes. UNSURE.
- b_infra, α, α_x, the fixed fractions: all MEMORY.

**Single most decisive check:** a measured, time-resolved cell-voltage record of IrO₂ against NiFe anodes in the same AEM cell (same membrane, cathode, electrolyte and temperature) over at least 1000 h at a stated j. It gives the time-averaged Δη and its drift with an uncertainty. If |Δη_avg| or the drift difference resolves above about 2 mV (or 0.03 µV/h over 8e4 h), Σ_init cannot decide the case for any CExC source within a factor 8 of CED. E18's sentence then has to read "rests on Σ̇" whatever the scarcity debate concludes.

Web sources consulted (titles and technical terms only): Buchspies et al. 2017 (doi.org/10.3390/min7110225); Nuss and Eckelman 2014 (journals.plos.org, main article); NiFe LDH vs IrOx alkaline OER (pubs.acs.org ACS Catal. 10:1886; pmc.ncbi.nlm.nih.gov PMC11434886); AEM cell voltage (Ferriday et al. 2024, onlinelibrary.wiley.com 10.1155/2024/7856850; Witte et al. 2025 ChemElectroChem; frontiersin.org 10.3389/fenrg.2026.1794912); drift (Galkina et al. 2024 Small; sciencedirect S0378775314008106; RSC EES D0EE04086J); Ir price (matthey.com PGM market reports 2025, 2026; USGS 2020 Minerals Yearbook PGM); ecoinvent metals (support.ecoinvent.org/metals; ecoinvent v3.11 change report on researchgate).
