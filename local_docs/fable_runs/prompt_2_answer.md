# Prompt 2 answer (S4): `GMS-100` exergy accounting coherence

Status: every statement is a claim at level `derived` (unverified). Inputs to all examples are made up. Derivations are in `prompt_2_plan.md` and are referenced as "plan D1" to "plan D7"; they are repeated only where they changed.

## Verdict

1. The accounting is repairable but not yet coherent: 1 BLOCKER (only when the dead state differs from the standard environment), 7 MAJOR, 2 conditional MAJOR, 6 MINOR.
2. Subtracting `b_ch` from `CExC` is sound, but the credit is never reversed when material is dispersed, so the extraction ledger does not close; material terms are cumulative while operational terms are local.
3. "The asymmetry always favours the incumbent" is false, and `λ_ℰ` is an average share, not a marginal one.
4. The recovery test is not a valid necessary condition until omitted channels, the cold-source sign and the fixed `η_L` are fixed.
5. All 40 spec rows and 4 added checks pass. They confirm algebra and arithmetic on made-up inputs, not the framework's data.

Notation: `b` = `b_ch`; `w_ext = CExC − b`; `w_rm` = `w_lost,remelt`; `R` = `R_rec`; `Tref` = 298.15 K; `x = T0/Ts`.

Where the numbers come from (all in `local_docs/fable_runs/prompt_2_code/`, output in `outputs/` under the same base name with `.txt`):

| Rows | Script |
|---|---|
| R1–R7 | `r01_r07_toy_chain.py` |
| R8–R13 | `r08_r13_extraction_closure.py` |
| R14–R21 | `r14_r21_closed_form_conventions.py` |
| R22–R31 | `r22_r31_dead_state_and_sinks.py` |
| R32–R35 | `r32_r35_spectral_exergy.py` |
| R36–R39 | `r36_r39_landsberg_infrastructure.py` |
| S4-A to S4-D | `s4_literal_r14_and_reconcile.py` (added in this stage) |

---

## 1. Logic/consistency findings (checkable by algebra)

**L1 (Q5) — BLOCKER when `T0 ≠ Tref`; no effect at the standard environment.**
- Term: every material term divided by `T0` (`Σ_s,init`, `Σ_g,init`, `R_g`, the EOL terms, `λ_ℰ`).
- Problem: the tabulated losses were dissipated on Earth against `Tref`. Dividing them by another `T0` rescales upstream terms by `Tref/T0` relative to operational terms.
- Correction: `Σ_upstream = (CExC − b)/Tref`; in general `Σ = Σ_k W_lost,k/T0,k`, with `T0,k` the environment where loss `k` was dissipated (plan D5(1)).
- Example: a 600 kJ Earth-side loss is 2012.41 J/K at `Tref` and 3000.00 J/K at `T0` = 200 K, ratio 1.49075 (R24). With losses 900 and 600 kJ and orbital operation 1500 and 2700 J/K, the corrected margin `Σ_g − Σ_s` is −193.80 J/K (candidate wins) and the framework's is +300 J/K (candidate loses) (R25).
- Sources: K9, K11.

**L2 (Q5) — MAJOR.** `CExC` cannot be transformed to another dead state; `b_ch` can.
- Term: `CExC(x)`, `b_ch(x)` wherever a non-standard dead state is used.
- `CExC = Σ_k r_k·b_k` is a tally over one Earth supply chain (a path quantity), so no shift formula exists (plan D5(5)).
- Equations for `b_ch` (plan D5(3), D5(4)): temperature at fixed reference composition, `b(T0) = (T0/Tref)·b° + (1 − T0/Tref)·d°`, `d° = −ΔH_r°`; reference-species potentials, `Δb_i = −Σ_j ν_ij·Δμ_j,env`, `Δμ_j,env = R·T0·ln(p_j'/p_j)`.
- Answer to Q5: the comparison is meaningful at a non-standard dead state only if upstream terms are frozen as entropy at `Tref` (L1) and local terms use the local environment. In low Earth orbit the reference species are absent, so a locally referenced `b_ch` is not a resource measure.
- Example: `b°` = 400, `d°` = 420 kJ/mol, `T0` = 250 K gives 403.230 kJ/mol (R22), reproduced through `ΔS_r°` = −67.08 J/(mol·K) (R23). Lowering ambient O2 from 20.39 kPa to 1.0e-5 Pa at 298.15 K changes `b` of a metal `M + ½O2 → MO` by −26 569 J/mol (R26).
- Sources: K4, K5, K6 (reference environment). The temperature formula stands on the Gibbs–Helmholtz derivation; K8 is no longer relied on.

**L3 (Q2) — MAJOR.** The extraction ledger does not close.
- Terms: `Σ_s,EOL`, `Σ_g,EOL`, `Σ^ret_EOL`.
- Problem: `Σ_init` credits the retained `b`; when the fraction `1 − R` is dispersed that exergy is neither charged nor held as stock.
- Answer to Q2: charging `b` on dispersion plus `CExC − b` on make-up exactly completes the account (total charge = resource exergy in − metal exergy still held). A double count arises only if make-up is charged at full `CExC` and `b` is charged at every dispersal.
- Correction (convention V1 and V2 adopted):
  `Σ_s,EOL = (n(x)/T0)·[R·w_rm + (1 − R)·b(x)]`
  `Σ_g,EOL = (1/T0)·Σ_i n_i·[R_i·w_rm,i + (1 − R_i)·b_i]`
  `Σ^ret_EOL = (1/T0)·Σ_i n_i·[R_i·w_rm,i + (1 − R_i)·CExC_i]`
- Example (`n` = 2 mol, `CExC` = 1500, `b` = 400 kJ/mol, `R` = 0.8, `m` = 3): framework charge 3520 kJ (R9); resource in 4800 kJ; with the last unit in service the gap is 480 kJ (R10); with it retired the corrected charge is 4160 kJ = 4800 − 640 (R11); the double-count variant gives 4640 kJ, 480 kJ too many (R12). An event-by-event ledger over 1000 random cases closes to 1.7e-15 (S4-B).
- Effect on the comparison, one example: the omitted term is 251.55 J/K for the incumbent and 10 196.21 J/K for the candidate, a shift of 9944.66 J/K against the candidate (R15).
- Limits: the closure is a property of the ledger model. It assumes dispersal destroys the full `b`, `CExC` includes the ore's own exergy, and the `K·sqrt(τ)` terms hold no chemical exergy of lost material (not visible in the prompt, UNSURE).

**L4 (Q1) — MAJOR.** Mixed basis.
- Terms: `Σ̇_g τ`, `Σ̇_s τ`, `Σ_g,mfg,eff`, `Σ_comp/N_units`, `b_transport`.
- Problem: material terms include upstream conversion losses of energy carriers; operational, manufacturing and computation terms do not. Not a double count: an omission that reweights material against operation.
- Correction (cumulative basis everywhere): `Σ̇ → Σ̇_local + (r_el − 1)·P_el/T0`; `Σ_comp → r_el·W_comp/T0`; the same factor on each delivered carrier in `Σ_g,mfg,eff`; `b_transport` as cumulative exergy of the fuel. `r_el = CExC_el/W_el`.
- Example: in the toy chain `CExC − b` = 1030 kJ/mol while a delivered-energy view sees 730 kJ/mol (R1, R3). With 10 W against 12 W for 10 years and a material handicap of 4.0e6 J/K, the candidate loses by 1 883 105.8 J/K on the local basis (R6) and wins by 2 350 682.5 J/K at `r_el` = 3.0 (R7). At the toy chain's own `r_el` = 2.5 it wins by 1 292 235.5 J/K; the flip occurs for any `r_el` above 1.8896 (S4-C).
- Realistic `r_el` is data (UNSURE).

**L5 (Q4) — MAJOR.** "Charging the incumbent only extraction + transport always favours the incumbent" is false.
- Term: `Σ_s,init`, and the net of `Σ_s + λ_ℰ`.
- True part: omitted incumbent stages are non-negative, so omissions alone never turn a true loss into a reported win (0 of 10 000 trials; 2122 reported losses were true wins, R21). The test is therefore valid for "geometry wins" only.
- Counterexample: if `x` is used as an oxide but charged with the metal's `CExC`, the incumbent is overcharged: 2012.41 J/K against 1157.14 J/K for the real chain, overcharge 855.27 J/K (R19). A candidate at 1500 J/K is reported as winning and truly loses (R20). Assumes the framework uses elemental `CExC(x)` whatever the form of `x` (UNSURE).
- Other asymmetries in the candidate's favour: L3 (R15) and L9 (R38).
- Correction (minimal symmetric boundary): `Σ_s,init = [Σ_j n_j,s·w_lost,prec,j + M_s·b_transport]/T0 + Σ_s,mfg,eff + Σ_s,tooling/N_s,units`, over all elements of the incumbent in the form used; computation on both sides or neither (plan D4).

**L6 (Q6) — MAJOR.** The recovery budget omits channels.
- Term: `Ḃ_intercepted(t)` and the verdict wording.
- Each included channel is an upper bound, but the sum bounds only "solar plus thermal through area `A`". The prompt's phrase "lower bound" is not right; its consequence is: a route using an omitted channel can be declared infeasible wrongly.
- Correction: restrict the verdict to "infeasible on intercepted solar and thermal exergy alone", or add an upper bound for every admitted channel: radiative cold sink `A_sky·σ·[(1/3)T0⁴ − (4/3)T0·T_c³ + T_c⁴]`, cold reservoir `Q̇_c·(T0/T_c − 1)`, wind `(1/2)ρv³·A_w`, stored or imported exergy as a budget line (plan D6).
- Example (1 m², 24 h, 200 W/m² mean, demand 20 MJ): framework budget 16.122 MJ, INFEASIBLE; with a deep-space sink (153.100 W/m², R29) 29.350 MJ, not excluded; with a 270 K sky (8.007 W/m²) 16.814 MJ, still infeasible (R30). The verdict flips for a sky colder than 219.47 K (S4-D).
- Sources: K66, K67 (153.1 W/m² as the ultimate limit).

**L7 (Q6) — MAJOR.** Cold source has the wrong sign.
- Term: `q_thermal·(1 − T0/T_source)` for `T_source < T0`.
- Correction: `q_c·(T0/T_source − 1)` for `T_source < T0`; clamping at zero is not enough.
- Example: 100 W/m² at 250 K with `T0` = 300 K gives −20 W/m² in the framework and +20 W/m² corrected (R31).

**L8 (Q7) — MAJOR.** `λ_ℰ` is an average share.
- Term: `λ_ℰ = B_infra/(T0·N_alloc)`.
- It is correct only for the all-or-nothing case (every unit stops using `x`, the infrastructure is dedicated, avoidable and scales linearly). For partial displacement the credit is `∂B_infra/∂N`. A per-unit share is arbitrary when units carry different `n(x)`.
- Correction: system test `Σ_k N_k·(Σ_g,k − Σ_s,k) < B_infra,avoidable/Tref`, or per-mole share `λ_k = n_k(x)·B_infra,avoidable/(Tref·Σ_k N_k·n_k(x))` (plan D7).
- Example: average 201.241 J/K against marginal 67.080 J/K (R37); per unit 201.241 J/K each against 34.109 and 1705.432 J/K per mole (R39).
- Sources: K41, K42.

**L9 (Q7) — MAJOR if the `CExC` source includes capital goods.** Double count and one-sidedness.
- Term: `Σ_s + λ_ℰ`.
- If `CExC(x)` already includes infrastructure, `λ_ℰ` counts it twice, in the candidate's favour. Separately, the candidate's elements also have infrastructure that is neither charged nor credited.
- Correction: `CExC` without capital goods plus an explicit infrastructure term for every element on both sides, or `CExC` with capital goods and no `λ_ℰ`.
- Example: 150 J/K of omitted incumbent stages against a double-counted 201.241 J/K leaves 51.241 J/K in the candidate's favour (R38).
- Sources: K12, K49 (database-based indicators inherit capital goods; not read in the text).

**L10 (Q1) — MAJOR if manufacturing yield is low, else MINOR.** Scrap is not pinned down.
- Terms: `Σ_i n_i·w_lost,prec,i` and `Σ_g,mfg,eff` (in `Σ_g,init` and `R_g`).
- Correction: `n_i` = net amount in the part, and `Σ_g,mfg,eff = Σ_process + (1/T0)·Σ_i n_i·(1/y_i − 1)·[(1 − R_scrap,i)·w_ext,i + R_scrap,i·w_rm,i + w_conv,i]`.
- Example (20 mol net, yield 0.6): 13.333 mol scrap; correct burden 3180.0 kJ (10 665.8 J/K); charged as fresh precursor 25 600.0 kJ (85 862.8 J/K); omitted 0 (R8).

**L11 (Q6) — MINOR near 300 K, MAJOR for a colder dead state.** `η_L` is hard-coded.
- Term: `η_L ≈ 0.933`. Correction: `η_L = 1 − (4/3)x + (1/3)x⁴` per run (or V9).
- Example: 0.933335 at (300 K, 6000 K), 0.953800 at (200 K, 5772 K) (R27); at 1361 W/m² the fixed value gives 1269.81 W/m² where the bound is 1298.12 W/m² (R36). Too low is the unsafe direction.
- Sources: K51, K53, K54.

**L12 (Q6) — MINOR.** Landsberg factor on diffuse or filtered sunlight.
- Term: `η_L·q_solar`.
- Answer to Q6: for diluted or diffuse sunlight the undiluted factor overestimates, which is safe; a dilution-dependent bound is needed only for sharpness. Overestimating the budget or underestimating the requirement is the safe direction for a necessary condition.
- Caveat: `η_L` is exact only for the full blackbody spectrum. The provable bound for any light whose brightness temperature nowhere exceeds `Ts` is the Carnot factor `1 − x` (plan D6).
- Example at (298.15 K, 5772 K): spectral integral 0.931130 = Landsberg (R32); high-pass filtered, undiluted 0.93554 (R33); hemispherically diluted 0.7321 with an ambient sky, 0.8378 without sky background (R34a, R34b); Carnot 0.948345, gap 0.017216 (R28); per-mode bound, 0 violations in 9797 cases (R35).
- Sources: K52, K53, K55, K57, K61; K63 for real spectra (abstract only).

**L13 (Q2) — MINOR.** Extraction multiplier.
- The stated "virgin extraction is charged `1 + m(1 − R)` times" follows from the prompt's formulas, per element. Closed form in plan C5. Built literally from `Σ_g,init`, `R_g`, `Σ^ret_EOL` and `Σ_g,EOL`, it agrees to 5.9e-16 (S4-A).
- New condition: the count holds with `w_conv` held fixed. If `w_lost,prec` is the fixed input instead, the multiplier of `w_ext` is `−m·R` (S4-A). Require `w_conv = w_lost,prec − w_lost,ext ≥ 0`, both from one data source.

**L14 (Q3) — MINOR.** Mapping identity.
- Per element, with `E_V = w_ext`, `E_rec = w_rm`: `total = (m + 1)·[(1 − R)·E_V + R·E_rec] + R·E_V` (R18).
- It exceeds a cut-off chain by `R·E_rec` and an avoided-burden chain by `R·E_V`: 1920 against 1880 and 1040 kJ/mol, differences 40 and 880 (R17).
- Answer to Q3: closest to closed-loop recycling inside the horizon with no-credit (cut-off-like) ends. Differences: the first unit is fully virgin, the scrap generator pays the terminal remelt, and the recovered terminal stock gets no credit. In circular-footprint terms this is `A` = 0 with the outgoing quality ratio set to zero, not a standard parameter set (plan D3). Defensible as a physical entropy ledger, which has no negative entries; but for a single life (the incumbent) it is harsher than every named method (V2), which favours the candidate.
- Sources for the named approaches: cut-off or recycled content K32; end-of-life recycling or avoided burden K33, K40; 50:50 K38; circular footprint formula K36, K37; side-by-side comparisons K34, K35, K45; closed loop K29 (UNSURE clause).
- Exergy-specific allocation: I found no widely adopted exergy rule for end-of-life allocation. Related work: K15, K16 (life-cycle irreversibility), K19, K20 (entropy production as the measure), K21–K24 (exergy losses of recycling loops), K25, K26 (replacement cost). Whether Szargut gives a rule for scrap inputs is UNSURE.

**L15 (Q6) — MINOR.** Remaining validity conditions: `A` is the largest area the site allows; `ΔG_recovery = ΔG° + R·T·ln Q` at actual activities; both sides in joules per recovered functional unit (plan C14). No number; units of `ΔG_recovery` and `n_rec` are not given in the prompt (UNSURE).

**L16 (Q1) — MINOR (conditions to record).** `w_lost,ext = CExC − b_ch` is consistent with how cumulative exergy consumption is defined.
- It equals `Tref·S_gen` of the chain only if `CExC` counts all resource inputs including the ore, uses the same reference environment as `b_ch`, carries no substitution credit, and `b_ch` is that of the form delivered (plan D1). Otherwise `w_lost,ext = Σ_k r_k·b_k − b_product − Σ b_byproducts`.
- Example: toy chain 1030 kJ/mol, 3454.64 J/(K·mol) (R1, R2); a substitution credit leaves 150 kJ/mol unaccounted (R4).
- Double-count audit between `CExC`, `b_ch`, `w_lost,prec`, `Σ_g,mfg,eff`: table in plan D1; the only overlaps are L3, L4 and L10.
- Sources: K1, K2, K3, K7.

---

## 2. Convention choices (practice differs)

| # | Choice | Options | Recommended default | Why |
|---|---|---|---|---|
| V1 (Q2) | When dispersed `b_ch` is destroyed | at dispersal; never; at replacement cost (K25, K26) | At dispersal | Closes the ledger (R11, S4-B) and matches "dispersed, not replaced". Replacement cost is a different, larger quantity. |
| V2 (Q3) | End-of-life allocation | cut-off; avoided burden; 50:50; circular footprint; no-credit ledger | No-credit ledger with both sides retired at `τ` (remelt and dispersal charged); avoided burden as a declared sensitivity case | An entropy ledger has no negative entries. The choice moves the incumbent most: single life 1140 (framework), 1100 (cut-off), 680 (50:50), 428 (circular footprint, `A` = 0.2), 260 kJ/mol (avoided burden) (R16). |
| V3 (Q3) | Horizon | integer replacements; pro-rated last unit | Integer, no residual credit; report the verdict on both sides of each `τ = m·τ_w` | Pro-rating is a credit. `Σ_g` steps by `R_g` at each replacement (algebra, not run), so a single `τ` can mislead. |
| V4 (Q4) | Boundary and cut-off rule | as is; symmetric | Same stages, data basis and exclusion threshold on both sides; missing incumbent data entered as a stated lower bound and the verdict labelled one-sided | L5. The threshold value is a free choice. K29 (UNSURE clause). |
| V5 (Q5) | Dead state for mixed sites | entropy basis with `T0,k`; exergy against one `T0*` | Entropy basis, `T0,k` per site | Same decisions; keeps the J/K ledger; L1. |
| V6 (Q1) | Cumulative indicator and by-product rule | all-resource `CExC`; non-renewable-only (K7); substitution, exergy, mass or economic partition | All-resource `CExC`, no substitution credit, partition by exergy content; economic partition as sensitivity for by-product elements | L16 needs it for closure (R4). Size of the effect for by-product `x` is UNSURE. |
| V7 (Q7) | Infrastructure | attributional charge; consequential credit | Base case `λ_ℰ` at the marginal value (zero if infrastructure is fixed); the all-or-nothing case as a separate system-level scenario | The test is a decision, so only the change it causes counts (K41, K42); R37. |
| V8 (Q6) | Channels and sink temperature | deep space; site effective sky | Declare the channel list; deep-space sink for an INFEASIBLE verdict | Only the colder sink is a provable upper bound. 0 K and 3 K differ by 6.1e-4 W/m² (S4-D). |
| V9 (Q6) | Solar factor | Landsberg/Petela; Carnot/Jeter (K52, K56, K57) | `(1 − T0/Ts)·q_solar` | Provable for any spectrum (R35); costs 0.017216 of `q_solar` in tightness (R28). |

Basis (L4) is also a choice between cumulative and local; either is admissible, a mixture is not. Cumulative is recommended because the material terms cannot be made local without process data.

---

## 3. Weak spots in the evidence

- **R14.** The implementer regrouped the terms (remelt attached to each of `m + 1` units) instead of using the prompt's `R_g`, `Σ^ret_EOL` and `Σ_g,EOL`. The two are the same sum; S4-A now builds it literally and agrees with plan C5.
- **R13.** The first check confirms an algebraic rearrangement on random inputs. The second compared one expression with itself, because choice C was coded as choice B. S4-B replaces it with an event ledger using the plan's definitions of choices A to D. Neither supports the physical premises listed under L3.
- **R3 against R7.** 2.5 follows from the toy chain's `η_el` = 0.4; 3.0 was a separate illustrative value. L4 holds for both (S4-C).
- **Assumed tolerances** (issues.md item 5) apply to cross-check quantities only; the differences are 5.5e-9, 1.7e-5, 0.027 W/m² and 0.0016 W/m² (R32–R34b). No claim rests on them.
- **R30.** The sink was taken at 0 K; see V8.
- **R3 "cumulative loss"** was read as 1030 kJ/mol (generation plus smelter), which is the plan's meaning.
- **Framework facts not visible in the prompt** (each conditions a severity): form of `x` in the incumbent (L5); `n_i` gross or net (L10); content of `K·sqrt(τ)` (L3); `CExC` source (L9, L16); units in the recovery test (L15); whether the thermal term is clamped (L7).

---

## 4. Citations

"Record" means S3 confirmed existence and that the title, abstract or catalogue record plausibly supports the use. No equation or section was read unless stated. Sections not listed were not checked.

| Id | Reference | Section | Used for | Status |
|---|---|---|---|---|
| K1 | Szargut, Morris, Steward (1988), Exergy Analysis of Thermal, Chemical, and Metallurgical Processes, Hemisphere | not checked | `CExC`, cumulative degree of perfection | record; by-product rule UNSURE |
| K2 | Szargut (2005), Exergy Method: Technical and Ecological Applications, WIT Press | not checked | same | record |
| K3 | Szargut, Morris (1987), Cumulative exergy consumption and cumulative degree of perfection of chemical processes, Int. J. Energy Res. 11(2), 245–261 | not checked | same | record |
| K4 | Szargut (1989), Chemical exergies of the elements, Applied Energy 32(4), 269–286 | not checked | reference species | record |
| K5 | Morris, Szargut (1986), Standard chemical exergy of some elements and compounds on the planet Earth, Energy 11(8), 733–755 | not checked | standard environment | record |
| K6 | Rivero, Garfias (2006), Standard chemical exergy of elements updated, Energy 31(15), 3310–3326 | not checked | dependence on reference choices | record |
| K7 | Szargut, Ziębik, Stanek (2002), Depletion of the unrestorable natural exergy resources as a measure of the ecological cost, Energy Convers. Manage. 43(9–12), 1149–1163 | not checked | non-renewable-only indicator | record; title corrected; volume UNSURE |
| K9 | Bejan (2016), Advanced Engineering Thermodynamics, 4th ed., Wiley | Ch. 5 "Exergy Analysis" (Gouy–Stodola, location not checked); Ch. 9 "Solar Power" (radiation conversion) | lost-work theorem; Petela, Spanner, Jeter comparison | record; chapters corrected |
| K11 | Gouy (1889), Sur l'énergie utilisable, J. Physique 8, 501–518 | not checked | origin of the theorem | record |
| K12 | Bösch, Hellweg, Huijbregts, Frischknecht (2007), Applying cumulative exergy demand (CExD) indicators to the ecoinvent database, Int. J. LCA 12(3), 181–190 | not checked | database-based indicator | record |
| K15 | Cornelissen, Hirs (2002), The value of the exergetic life cycle assessment besides the LCA, Energy Convers. Manage. 43(9–12), 1417–1424 | not checked | life-cycle irreversibility | record |
| K16 | Cornelissen (1997), Thermodynamics and sustainable development: the use of exergy analysis and the reduction of irreversibility, PhD thesis, Univ. of Twente | not checked | same | record |
| K19 | Gößling-Reisemann (2008), What is resource consumption and how can it be measured? Theoretical considerations, J. Ind. Ecol. 12(1), 10–25 | not checked | entropy production as the measure | record |
| K20 | Gößling-Reisemann (2008), What is resource consumption and how can it be measured? Application of entropy analysis to copper production, J. Ind. Ecol. 12(4), 570–582 | not checked | same, metal chain | record (via a reference list) |
| K21 | Amini, Remmerswaal, Castro, Reuter (2007), Quantifying the quality loss and resource efficiency of recycling by means of exergy analysis, J. Cleaner Prod. 15(10), 907–913 | not checked | exergy of recycling loops | record |
| K22 | Castro, Remmerswaal, Brezet, Reuter (2007), Exergy losses during recycling and the resource efficiency of product systems, Resour. Conserv. Recycl. 52(2), 219–233 | not checked | same | record; author order UNSURE |
| K23 | Ignatenko, van Schaik, Reuter (2007), Exergy as a tool for evaluation of the resource efficiency of recycling systems, Minerals Eng. 20(9), 862–874 | not checked | same | record |
| K24 | Dewulf et al. (2010), Recycling rechargeable lithium ion batteries: critical analysis of natural resource savings, Resour. Conserv. Recycl. 54(4), 229–234 | not checked | cumulative exergy, recycled against virgin | record |
| K25 | Valero, Valero (2014), Thanatia: The Destiny of the Earth's Mineral Resources: A Thermodynamic Cradle-to-Cradle Assessment, World Scientific | not checked | replacement cost | record; title completed |
| K26 | Valero, Valero, Domínguez (2013), Exergy replacement cost of mineral resources, J. Environ. Account. Manage. 1(2), 147–158 | not checked | same | record |
| K29 | ISO 14044:2006, Environmental management — Life cycle assessment — Requirements and guidelines | 4.3.4.3 (reuse and recycling), 4.2.3.3 (cut-off), 4.2.3.7 (comparisons) | closed loop; equal boundaries | UNSURE (clause numbers not confirmed) |
| K32 | Frischknecht (2010), LCI modelling approaches applied on recycling of materials in view of environmental sustainability, risk perception and eco-efficiency, Int. J. LCA 15(7), 666–671 | not checked | recycled content against end-of-life recycling | record |
| K33 | Atherton (2007), Declaration by the metals industry on recycling principles, Int. J. LCA 12(1), 59–60 | not checked | end-of-life recycling approach | record; volume and pages UNSURE |
| K34 | Allacker et al. (2014), Allocation solutions for secondary material production and end of life recovery: proposals for product policy initiatives, Resour. Conserv. Recycl. 88, 1–12 | not checked | side-by-side comparison of approaches | record |
| K35 | Allacker, Mathieux, Pennington, Pant (2017), The search for an appropriate end-of-life formula for the purpose of the European Commission Environmental Footprint initiative, Int. J. LCA 22(9), 1441–1458 | not checked | end-of-life formulas | record |
| K36 | European Commission (2021), Recommendation (EU) 2021/2279 on the use of the Environmental Footprint methods | Annex I (PEF method); section not checked | circular footprint formula | record |
| K37 | Zampori, Pant (2019), Suggestions for updating the Product Environmental Footprint (PEF) method, EUR 29682 EN | not checked | same | record |
| K38 | European Commission (2013), Recommendation 2013/179/EU | Annex II (PEF Guide), section 5.4.7 "End-of-Life" | 50:50 formula | record; annex corrected; exact form not read |
| K40 | Weidema (2000), Avoiding co-product allocation in life-cycle assessment, J. Ind. Ecol. 4(3), 11–33 | not checked | system expansion, avoided burden | record; year corrected |
| K41 | Ekvall, Weidema (2004), System boundaries and input data in consequential life cycle inventory analysis, Int. J. LCA 9(3), 161–171 | not checked | marginal against average data | record |
| K42 | Finnveden et al. (2009), Recent developments in Life Cycle Assessment, J. Environ. Manage. 91(1), 1–21 | not checked | attributional against consequential | record |
| K45 | Ekvall, Björklund, Sandin, Jelse, Lagergren, Rydberg (2020), Modeling recycling in life cycle assessment, IVL report C551 | not checked | survey of recycling allocation | record; publisher corrected |
| K49 | Frischknecht et al. (2007), The environmental relevance of capital goods in life cycle assessments of products and services, Int. J. LCA 12 (Special Issue 1), 7–17 | not checked | capital goods in databases | record |
| K51 | Petela (1964), Exergy of heat radiation, J. Heat Transfer 86(2), 187–192 | not checked | `1 − (4/3)x + (1/3)x⁴` | record |
| K52 | Petela (2003), Exergy of undiluted thermal radiation, Solar Energy 74(6), 469–488 | not checked | scope: undiluted radiation | record |
| K53 | Landsberg, Tonge (1979), Thermodynamics of the conversion of diluted radiation, J. Phys. A 12(4), 551–562 | not checked | dilution factor | record |
| K54 | Landsberg, Tonge (1980), Thermodynamic energy conversion efficiencies, J. Appl. Phys. 51(7), R1–R20 | not checked | Landsberg efficiency | record |
| K55 | Press (1976), Theoretical maximum for energy from direct and diffuse sunlight, Nature 264, 734–735 | not checked | direct against diffuse | record |
| K56 | Bejan (1987), Unification of three different theories concerning the ideal conversion of enclosed radiation, J. Solar Energy Eng. 109(1), 46–51 | not checked | Petela, Spanner, Jeter | record |
| K57 | Jeter (1981), Maximum conversion efficiency for the utilization of direct solar radiation, Solar Energy 26(3), 231–236 | not checked | Carnot-form bound | record |
| K61 | Candau (2003), On the exergy of radiation, Solar Energy 75(3), 241–247 | not checked | arbitrary spectra | record |
| K63 | Chu, Liu (2009), Analysis of terrestrial solar radiation exergy, Solar Energy 83(8), 1390–1404 | abstract | real spectra: quality factor about 0.929 extraterrestrial, 0.917 terrestrial | record (abstract) |
| K66 | Byrnes, Blanchard, Capasso (2014), Harvesting renewable energy from Earth's mid-infrared emissions, PNAS 111(11), 3927–3932 | not checked | work from a cold sky | record |
| K67 | Buddhiraju, Santhanam, Fan (2018), Thermodynamic limits of energy harvesting from outgoing thermal radiation, PNAS 115(16), E3609–E3615 | not checked | 153.1 W/m² ultimate limit (300 K, 3 K) | record (search summary); page range UNSURE |
| K70 | Planck (1914), The Theory of Heat Radiation, transl. Masius | not located | entropy of a radiation mode | record; section UNSURE |

Not relied on any more: K8 (Kotas 1985), K39 (Lindfors et al. 1995), K46 (PAS 2050:2011), K60 (Green 2003), K68 (Rosen, Dincer 2004), K71 (Rosen 1954): all UNSURE. K44 (Nordelöf et al. 2019, Batteries 5(3), 51) exists but its abstract covers only cut-off and end-of-life recycling archetypes; K34 replaces it.

---

## 5. Changed since plan

1. **C5 (L13).** Now tested against the prompt's literal formulas (S4-A); the claim stands. Added: the `1 + m(1 − R)` count needs `w_conv` held fixed; with `w_lost,prec` fixed the multiplier is `−m·R`.
2. **C4 (L3).** Half of R13 was a self-comparison; replaced by S4-B. Claim stands, restated as a property of the ledger model. "Normally favours the candidate" dropped: R15 is one made-up case.
3. **C2 (L4).** `r_el` reconciled: the flip holds at 2.5 and 3.0, threshold 1.8896 (S4-C). R7 value is −2 350 682.5 J/K, not the plan's −2 350 682.6.
4. **C18 (V2).** Plan offered "(c) or (a)" and its (c) charged only events within `τ`, which contradicted the plan's own corrected `Σ_g,EOL`. Now one default: both sides retired at `τ`, no credit. This also settles the timing remark in plan C5.
5. **C13 (L12, V9).** Hand estimates replaced by computed values: 0.9355 → 0.93554, 0.734 → 0.7321, 0.838 → 0.8378. The with/without-sky difference is 0.1057, not equal to the cold-sky share 0.1097 as the plan said. Carnot is promoted from "if a proof is wanted" to the default. The open question on real spectra is narrowed by K63's abstract (terrestrial value below `η_L`), not closed.
6. **K67 (L6).** 48.4 W/m² is a result for one device configuration, not a limit. No claim used it as a limit: plan C10 and R30 use the ultimate form. Used as the bound it would be unsafe: at a demand of 25 MJ it gives 20.308 MJ (infeasible) against 29.350 MJ (not excluded) (S4-D). The paper's emitter temperature (225.1 K per S3) against 225 K in R29 is not reconciled (UNSURE).
7. **C24 (V8).** Default set to the deep-space sink; flip temperature 219.47 K added.
8. **C21, C22, C23 (V6, V3, V7).** The plan gave no default; defaults added. V6 has low confidence.
9. **C1 (L16).** Labelled MINOR instead of "no severity".
10. **Citations.** Records corrected: K7 (title), K9 (chapters), K25 (title), K36 (annex), K38 (Annex II, section 5.4.7), K40 (year 2000), K45 (IVL report C551). K8, K39, K46, K60, K68, K71 dropped as evidence; the claims they supported now rest on plan D5(3) (for K8, K68), K38 (for K39), K54 with R27 (for K60) and K70 with R32 (for K71); K46 was not needed. K44 restricted and replaced by K34. K29 kept as UNSURE; V4 rests on plan D4, not on the clause. K29, K60, K68 were "sure" in the plan and are now UNSURE.
11. **Left out:** plan citations not needed by a finding (K10, K13, K14, K17, K18, K27, K28, K30, K31, K43, K47, K48, K50, K58, K59, K62, K64, K65, K69) are not repeated here; their S3 status is in `prompt_2_citations.md`.
12. **Unchanged:** C3, C6, C7, C8, C9, C10, C11, C12, C14, C15, C16, C17, C19, C20.
