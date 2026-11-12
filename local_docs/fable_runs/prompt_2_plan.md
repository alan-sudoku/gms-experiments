# Prompt 2 plan (S1): `GMS-100` exergy accounting coherence

Status: every statement here is a claim at level `derived` (unverified). No code was run and no web search was made in this stage. All numbers are hand arithmetic on made-up, illustrative inputs; each is tagged with the computation-spec row (`[Rn]`) that must reproduce it. Where a hand value and the implemented value disagree beyond the stated tolerance, the implemented value wins and the claim it supports must be re-examined. Items I could not verify are marked UNSURE.

Source read: `local_docs/fable_questions.md`, section "Prompt 2", fenced text block only. Nothing else in the repository was read, so every statement about "the framework" refers to the formulas as written in that block.

Notation used below (per element unless indexed):

- `T0` framework dead-state temperature [K]; `Tref` = 298.15 K, the temperature of the standard reference environment of the tables.
- `CExC` cumulative exergy consumption [J/mol]; `b` = `b_ch` standard chemical exergy [J/mol]; `w_ext = CExC − b`; `w_conv`, `w_rm` (= `w_lost,remelt`) [J/mol].
- `n` amount [mol]; `R` = `R_rec` recovered fraction [-]; `m` number of replacements [-].
- `E_V`, `E_rec`, `E_D`: virgin production, recycling and disposal burdens per mol in LCA allocation formulas [J/mol]; `R1` recycled content, `R2` end-of-life recycling rate.
- `x = T0/Ts` with `Ts` the solar brightness temperature [K].

---

## 1. Claims

### 1A. Logic and consistency findings (checkable by algebra or by a number)

**C1 (Q1) — verification, no severity.** Subtracting `b_ch` from `CExC` is consistent with how cumulative exergy consumption is defined: `CExC − b_ch` is the cumulative exergy loss of the chain (internal destruction plus exergy of wastes discharged), and `b_ch/CExC` is the cumulative degree of perfection (K1, K3). It equals `Tref·S_gen` of the chain only if all four conditions hold: (i) `CExC` counts the exergy of every resource input, including the ore itself and renewable inputs (a non-renewable-only indicator such as thermo-ecological cost, K7, does not qualify); (ii) `CExC` and `b_ch` use the same reference environment; (iii) the tabulated `CExC` carries no by-product credit by substitution; (iv) `b_ch` is that of the form actually delivered.
- Term affected: `w_lost,ext(x) = CExC(x) − b_ch(x)`.
- Corrected expression: none needed if (i)–(iv) hold; otherwise `w_lost,ext = Σ_k r_k·b_k − b_product − Σ b_byproducts`, with all resource inputs `k` and by-products counted explicitly.
- Confidence: high for the balance identity; medium for which published tables satisfy (i) and (iii) (UNSURE, see K1, K2, K12, K13).
- Falsifier: R1–R2 (toy two-stage chain closes exactly); R4 (a substitution credit breaks the equality).

**C2 (Q1) — MAJOR.** Basis mismatch. Material terms are cumulative (they include the upstream conversion losses of the energy carriers used in mining and smelting), while `Σ_g,mfg,eff`, `Σ_comp` ("delivered electricity only") and the operational terms `Σ̇·τ` are local or delivered. The same joule of delivered electricity is therefore weighted `r_el = CExC_el/W_el` times more heavily inside a material term than inside an operational, manufacturing or computation term. This is not a double count; it is an omission that changes the relative weight of material and operational terms and can reverse the decision.
- Terms affected: `Σ̇_g τ`, `Σ̇_s τ`, `Σ_g,mfg,eff`, `Σ_comp/N_units`, `b_transport`.
- Corrected expression (cumulative basis everywhere): `Σ̇ → Σ̇_local + (r_el − 1)·P_el/T0`; `Σ_comp → r_el·W_comp/T0`; the same factor on every delivered carrier in `Σ_g,mfg,eff`; `b_transport →` cumulative exergy of the transport fuel per kg moved.
- Confidence: high on the logic; `r_el` is data (I expect roughly 2.5–4 for thermal-dominated grids, UNSURE).
- Falsifier: R3 and R5–R7 (decision flips with `r_el = 3`). The claim fails if the framework already charges primary exergy for these terms, which the prompt text contradicts for computation.

**C3 (Q1) — MAJOR if manufacturing yield is low, otherwise MINOR.** The split between `Σ_i n_i·w_lost,prec,i` and `Σ_g,mfg,eff` ("including yield losses") is not defined tightly enough to exclude either a double count or an omission of the upstream burden of scrap. If `n_i` is the gross input and `Σ_g,mfg,eff` also contains scrap burden, extraction of the scrap is counted twice; if `n_i` is the net content and `Σ_g,mfg,eff` contains only process energy, it is omitted.
- Terms affected: `Σ_g,init`, `R_g` (both contain `Σ_g,mfg,eff`).
- Corrected expression: define `n_i` as the net amount in the finished part and require
  `Σ_g,mfg,eff = Σ_process + (1/T0)·Σ_i n_i·(1/y_i − 1)·[(1 − R_scrap,i)·w_ext,i + R_scrap,i·w_rm,i + w_conv,i]`.
- Confidence: medium (the prompt does not say which reading is implemented).
- Falsifier: R8; a mass balance on the implemented terms.

**C4 (Q2) — MAJOR.** The extraction ledger does not close. `Σ_init` credits the retained chemical exergy (`−b_ch`), but when the fraction `1 − R` is dispersed that exergy is neither charged as destroyed nor held as stock. Charging `b_ch` on dispersion together with `CExC − b_ch` on make-up does not double count; it exactly completes the account: total charge = resource exergy in − exergy of the metal stock still held. A double count arises only if make-up is charged at full `CExC` and dispersion is charged `b_ch` as well.
- Terms affected: `Σ_s,EOL`, `Σ_g,EOL`, `Σ^ret_EOL`.
- Corrected expressions:
  `Σ_s,EOL = (n(x)/T0)·[R·w_rm + (1 − R)·b_ch(x)]`
  `Σ_g,EOL = (1/T0)·Σ_i n_i·[R_i·w_rm,i + (1 − R_i)·b_ch,i]`
  `Σ^ret_EOL = (1/T0)·Σ_i n_i·[R_i·w_rm,i + (1 − R_i)·(w_ext,i + b_ch,i)]` (the bracket's last term is then `(1 − R_i)·CExC_i`).
- Closure identity: `n·[(CExC − b)(1 + m(1 − R)) + b(1 − R)(m + 1)] = n·[CExC·(1 + m(1 − R)) − R·b]`.
- Confidence: high for the algebra; conditional on the convention that dispersal takes the element to the dead state (C17).
- Falsifier: R9–R13. A check to make before adopting: if the `K·sqrt(τ)` terms already contain chemical exergy of material lost in service, the new term would overlap with them (UNSURE, not visible in the prompt).
- Direction: the omission favours the side that disperses more chemical exergy, which is normally the candidate with replacements, not the incumbent (R15).

**C5 (Q2) — verification, plus MINOR.** The stated convention "virgin extraction is charged `1 + m(1 − R_rec)` times" follows from the formulas, per element with its own `R_i`. Full closed form of the material part:
`Σ_g,init + m·R_g + Σ_g,EOL = (1/T0)·Σ_i n_i·{w_ext,i·[1 + m(1 − R_i)] + (m + 1)·w_conv,i + (m + 1)·R_i·w_rm,i} + (m + 1)·[M_G·b_transport/T0 + Σ_g,mfg,eff] + (Σ_tooling + Σ_comp)/N_units`.
MINOR: the unit in service at the horizon is charged a remelt that has not occurred by `τ`, while its dispersed fraction is not charged; both sides are treated alike, so this is a consistency of timing, not a bias.
- Confidence: high. Falsifier: R14.

**C6 (Q3) — MINOR as logic (the choice itself is C18).** The EOL and replacement convention is a finite-horizon closed loop with a fully virgin first unit and an uncredited terminal stock. Per element, with `E_V = w_ext` and `E_rec = w_rm`:
`total = (m + 1)·[(1 − R)·E_V + R·E_rec] + R·E_V`.
It exceeds a consistent cut-off (recycled-content) chain by exactly `R·E_rec` (the final remelt is charged to the scrap generator) and exceeds an avoided-burden chain by exactly `R·E_V` (no credit for the recovered terminal stock). For a single life (`m = 0`, which is the incumbent's case) the burden `E_V + R·E_rec` is higher than under either named method.
- Terms affected: `Σ_s,EOL`, `Σ_g,EOL`.
- Corrected expression: none required for internal consistency; see C18 for the options.
- Confidence: high for the identity; medium for the naming.
- Falsifier: R16–R18.

**C7 (Q4) — MAJOR.** "Charging the incumbent only extraction + transport always favours the incumbent" is false as stated. What is true: because the win test is additive and every omitted incumbent term is a non-negative entropy generation, the omissions alone can never turn a true loss into a reported win. The statement fails through what is charged, not what is omitted: (a) if the incumbent uses `x` in a less-processed form than the tabulated product (for example an oxide while `CExC(x)` is for the metal), the incumbent is overcharged and the candidate is favoured; (b) other asymmetries in the same inequality act in the candidate's favour and can outweigh the omitted terms: `λ_ℰ` double counting (C16) and the uncharged dispersion of `b_ch` (C4). Further, the one-sided conservatism protects only "geometry wins" verdicts; "geometry loses" verdicts, rankings against the incumbent and break-even horizons are biased by an unknown amount.
- Term affected: `Σ_s,init` (and the net of `Σ_s + λ_ℰ`).
- Corrected expression (minimal symmetric boundary): `Σ_s,init = [Σ_j n_j,s·w_lost,prec,j + M_s·b_transport]/T0 + Σ_s,mfg,eff + Σ_s,tooling/N_s,units`, over all elements `j` of the incumbent in the form used, with computation either included on both sides or excluded on both under one stated cut-off rule.
- Confidence: high for the proposition; medium for counterexample (a), which assumes `CExC(x)` is the elemental value regardless of the form of `x` in `s` (UNSURE).
- Falsifier: R19–R21.

**C8 (Q5) — BLOCKER when `T0 ≠ Tref`, no effect at the standard environment.** `[CExC − b_ch]/T0` is the entropy generated upstream only if `T0 = Tref`. The tabulated exergy losses were incurred on Earth against `Tref`; by Gouy–Stodola the entropy generated is `(CExC − b_ch)/Tref` whatever the dead state of the place of use. Dividing by a different `T0` rescales the upstream terms by `Tref/T0` relative to operational terms that are physical local entropy generation, and can reverse the decision.
- Terms affected: every material term divided by `T0` (`Σ_s,init`, `Σ_g,init`, `R_g`, EOL terms, `λ_ℰ`).
- Corrected expression: `Σ_upstream = (CExC − b_ch)/Tref`; in general `Σ = Σ_k W_lost,k/T0,k` with `T0,k` the environment in which loss `k` was dissipated.
- Confidence: high on the logic.
- Falsifier: R24–R25.

**C9 (Q5) — MAJOR.** `CExC` is a path quantity (a tally of resources drawn by a specific Earth supply chain), not a state function, so no dead-state transformation exists for it. `b_ch` can be transformed: for temperature at fixed reference composition `b(T0) = (T0/Tref)·b° + (1 − T0/Tref)·d°` (with `d° = −ΔH_r°`, constant `ΔH_r`), and for a change in reference-species chemical potentials `Δb_i = −Σ_j ν_ij·Δμ_j,env`. For low Earth orbit the Szargut reference species do not exist in the local environment, so a locally referenced `b_ch` is not meaningful as a resource measure. The comparison is meaningful at a non-standard dead state only if upstream terms are frozen as entropy at the standard environment (C8) and local terms use the local environment.
- Terms affected: `b_ch` wherever it appears; `η_L` and Carnot factors (C12).
- Confidence: high for the equations (standard thermodynamics); medium for the recommended convention (C20).
- Falsifier: R22–R23, R26.

**C10 (Q6) — MAJOR.** The verdict "fails → INFEASIBLE" is valid only if the right-hand side is an upper bound on all exergy available to the route and the left-hand side is a lower bound on what the route needs. As written, each included channel is individually an upper bound (Landsberg for sunlight, Carnot for heat), but the sum omits channels, so it is an upper bound only on "solar plus thermal through area A". The prompt's wording "a lower bound" is not correct (the sum can overestimate what is practically available by a large factor); the consequence the prompt suspects is correct: a route that uses an omitted channel can be declared infeasible wrongly.
- Term affected: `Ḃ_intercepted(t)` and the wording of the verdict.
- Corrected expression: either restrict the verdict to "infeasible on intercepted solar and thermal exergy alone", or add an upper bound for every admitted channel, for example a radiative cold sink `A_sky·σ·[(1/3)T0⁴ − (4/3)T0·T_c³ + T_c⁴]`, a cold reservoir `Q̇_c·(T0/T_c − 1)`, wind `(1/2)ρv³·A_w`, and stored or imported chemical exergy as an explicit budget line.
- Confidence: high on the logic; medium on the size of the omitted terms.
- Falsifier: R29–R30, R34b.

**C11 (Q6) — MAJOR.** For `T_source < T0` the term `q_thermal·(1 − T0/T_source)` is negative and reduces the budget, although a cold source is a positive exergy resource. This errs in the unsafe direction for a necessary condition.
- Term affected: thermal term of `Ḃ_intercepted`.
- Corrected expression: `q_thermal·(1 − T0/T_source)` for `T_source ≥ T0` and `q_c·(T0/T_source − 1)` for `T_source < T0`, with `q_c` the heat flux delivered to the cold body. Clamping at zero is not sufficient.
- Confidence: high. Falsifier: R31.

**C12 (Q6) — MINOR at `T0 ≈ 300 K`, MAJOR for a colder dead state.** `η_L ≈ 0.933` is the value for `T0/Ts = 0.05` (300 K, 6000 K). It is a function of the dead state, `η_L = 1 − (4/3)x + (1/3)x⁴`. For `T0 < 300 K` the hard-coded value understates the upper bound, which is the unsafe direction; for `T0 > 300 K` it overstates, which is safe.
- Corrected expression: compute `η_L(T0, Ts)` per run. Confidence: high. Falsifier: R27, R36.

**C13 (Q6) — MINOR.** For unconcentrated or diffuse terrestrial sunlight the undiluted Landsberg factor overestimates the exergy (hemispherically diluted sunlight has a markedly lower exergy-to-energy ratio), so it remains a valid and safe, but loose, bound. A dilution-dependent (Petela or Landsberg–Tonge type) bound is tighter and is needed only for sharpness, not for validity. One caveat against the framework: `η_L` is exact only for the full blackbody spectrum; spectrally filtered sunlight can exceed it slightly. The provable bound for any radiation whose brightness temperature nowhere exceeds `Ts` is the Carnot factor `1 − T0/Ts`, larger than `η_L` by at most `(x/3)(1 − x³)`.
- Term affected: `η_L·q_solar`.
- Corrected expression (if a provable bound is wanted): `(1 − T0/Ts)·q_solar`.
- Confidence: medium-high; whether real clear-sky direct-beam spectra sit above or below `η_L` is UNSURE.
- Falsifier: R32–R35.

**C14 (Q6) — MINOR.** Remaining validity conditions of the test: `A` must be the largest collecting area the site allows (not a design value); `ΔG_recovery` must be a true minimum, `ΔG° + R·T·ln Q` at the actual activities, because a standard-state value can exceed the true minimum when the real feed is more concentrated or the product less pure than the standard state; both sides must be in joules per recovered functional unit (`n(x)·ΔG_recovery` against `(1/n_rec)∫Ḃ dt`). Perfect storage and allocation of all intercepted exergy to recovery overestimate availability and are safe.
- Confidence: medium (the prompt gives no units for `ΔG_recovery` or `n_rec`). Falsifier: dimensional check of the implemented test.

**C15 (Q7) — MAJOR.** `λ_ℰ = B_infra/(T0·N_alloc)` is an average (fully allocated) share, not a marginal quantity. It is coherent only as the per-unit expression of an all-or-nothing counterfactual in which every one of the `N_alloc` units stops using `x` and the infrastructure is thereby avoided. That requires: infrastructure dedicated to `x` (not shared with a host metal), forward-looking avoidable exergy rather than sunk embodied exergy, `N_alloc` equal to the number of units actually displaced over the infrastructure life, and linear scaling. For partial displacement the credit is the marginal `∂B_infra/∂N`. Allocating per unit rather than per mole of `x` is arbitrary when units carry different `n(x)`.
- Corrected expression: system-level test `Σ_k N_k·(Σ_g,k − Σ_s,k) < B_infra,avoidable/Tref`, or a per-unit share by mole `λ_k = n_k(x)·B_infra,avoidable/(Tref·Σ_k N_k·n_k(x))`.
- Confidence: medium-high. Falsifier: R37, R39.

**C16 (Q7) — MAJOR, conditional.** `λ_ℰ` double counts with `CExC` whenever the `CExC` source already includes capital goods (process databases that include infrastructure by default do; classical process-chain tables largely do not; UNSURE which the framework uses, see K12, K13, K49). The double count is on the incumbent side and favours the candidate. Independently, `λ_ℰ` is asymmetric: the candidate's elements also have supply-chain infrastructure, which is neither charged nor credited.
- Corrected expression: use `CExC` exclusive of capital goods plus an explicit infrastructure term for every element on both sides, or `CExC` inclusive of capital goods and no `λ_ℰ`.
- Confidence: medium. Falsifier: R38; inspection of the `CExC` data source.

### 1B. Convention choices (practice differs; a choice must be recorded)

**C17 (Q2).** When to recognise destruction of `b_ch` of dispersed material: (a) at dispersal, as committed loss (recommended; matches "dispersed, not replaced" and closes the ledger, C4); (b) never, treating dispersed metal as a stock (the present behaviour; leaves the ledger open); (c) at an exergy replacement cost from a dispersed crust (K25, K26), which is a larger and different quantity. Confidence in recommending (a): medium. Test: R9–R12 show the consequence of each.

**C18 (Q3).** EOL allocation. Options: (a) cut-off: drop `R·w_rm` from the terminal unit and from `Σ_s,EOL`, give the first unit its real recycled content; (b) avoided burden: keep `R·w_rm`, credit `R·Q·w_ext` for the terminal stock; (c) keep the present no-credit physical ledger but then charge only events that occur within `τ`; (d) circular footprint formula with a declared `A`. Recommended: (c) or (a) as the base case because an entropy ledger has no physical negative entries, with (b) as a declared sensitivity case, since the choice changes the incumbent's burden most (R16). Confidence: medium.

**C19 (Q4).** Symmetric boundary and cut-off rule: same life-cycle stages, same data basis and same exclusion threshold on both sides (K29); where incumbent data are missing, enter a stated lower bound and report the verdict as one-sided. Confidence: high that symmetry is required for comparative claims; the threshold value is a choice.

**C20 (Q5).** Dead-state convention for mixed sites: entropy basis with site-specific `T0,k` (recommended) or exergy basis against one declared `T0*` (same decisions, different units). The retained and dispersed `b_ch` are referenced to the environment where the material ends up. Confidence: medium.

**C21 (Q1).** Which cumulative indicator and by-product rule: all-resource `CExC` versus non-renewable-only indicators; mass, exergy, economic or substitution allocation for `x` produced as a by-product of a host metal. This choice can change `CExC(x)` by a large factor for by-product elements (UNSURE on magnitudes). Also whether dissipation of freely intercepted environmental exergy (sunlight) in operation counts as attributable entropy generation.

**C22 (Q3).** Horizon treatment: integer replacements with no residual-value credit (present) versus pro-rating the last unit by the fraction of life used. The present rule makes the verdict non-monotonic in `τ` (a step of `R_g` at each `τ = m·τ_w`).

**C23 (Q7).** Attributional (every unit of `x` carries its infrastructure share, unconditionally, as a charge) versus consequential (credit only the change caused by the decision) treatment of infrastructure (K41, K42). `λ_ℰ` currently mixes the two.

**C24 (Q6).** Which channels count as "on-site environmental exergy" and which sink temperature is used for a radiative sky sink (deep space as a safe bound, or a site effective sky temperature as a tighter one).

### 1C. Verdict on the suspicions stated in the prompt

| Suspicion in the prompt | Result of testing it |
|---|---|
| Q2: dispersion destroys `b_ch` and may need charging | Confirmed, conditional on C17(a); it completes the account, no double count (C4). |
| Q4: the asymmetry favours the incumbent | Partly refuted. True for omitted terms only; false for over-charged included terms and for the net of all asymmetries (C7). |
| Q6: omissions make the test a lower bound | Wording refuted (it is an upper bound on two channels, neither bound on the total); consequence confirmed (C10). |
| Q6: a dilution-dependent bound may be needed | Refuted for validity (Landsberg overestimates diffuse light, which is safe); confirmed only for tightness. New caveat: Carnot, not Landsberg, is the provable bound for filtered light (C13). |
| Q7: `CExC` may already include infrastructure | Conditional on the data source (C16). |

---

## 2. Derivations

### D1 (Q1). What `CExC − b_ch` is

Exergy balance over the whole chain that delivers 1 mol of product, all exergies against the same reference environment at `Tref` [J/mol]:

`Σ_k r_k·b_k = b_product + Σ b_byproducts + B_waste + B_destroyed`

where `r_k` is the amount of natural resource `k` drawn per mol of product. By definition `CExC = Σ_k r_k·b_k`. With no by-products,

`CExC − b_product = B_waste + B_destroyed`.

Waste exergy is destroyed when the waste equilibrates with the environment, so the entropy generated in the universe is

`S_gen = (CExC − b_product)/Tref` [J/(K·mol)] (Gouy–Stodola, K9).

Toy chain, illustrative: ore exergy 30 kJ/mol, fuel 900 kJ/mol, delivered electricity 200 kJ/mol generated at exergy efficiency 0.4, product `b` = 400 kJ/mol. Then `CExC` = 30 + 900 + 200/0.4 = 1430 kJ/mol; generation destroys 300 kJ/mol; the smelter destroys 30 + 900 + 200 − 400 = 730 kJ/mol; the sum 1030 kJ/mol equals `CExC − b` [R1], or 3454.64 J/(K·mol) [R2]. A delivered-energy account of the same chain sees only 730 kJ/mol; the cumulative factor of the electricity is 2.5 [R3]. This is the mechanism of C2.

By-product variant: a by-product with exergy 100 kJ per mol of product, credited by substitution at 250 kJ, gives a net `CExC` of 1180 kJ/mol and `CExC − b` = 780 kJ/mol, while the chain actually lost 1430 − 400 − 100 = 930 kJ/mol [R4]. Hence condition (iii) of C1.

Double-count and omission audit between the four quantities named in Q1:

| Pair | Double count? | Omission? |
|---|---|---|
| `CExC` and `b_ch` | No. `b_ch` is a subset of `CExC` that is still present in the product; subtracting it removes a credit, not a cost. | The credit is never reversed when the exergy is later destroyed (C4). |
| `w_ext` and `w_conv` inside `w_lost,prec` | No, provided `w_conv` is the lost work of the conversion step only (inputs minus the exergy gain of the precursor). `w_conv ≥ 0` by the second law. | If the precursor's own chemical exergy differs from the elemental `b_ch` (alloying, compound formation), the difference is unassigned. Small. |
| `w_lost,prec` and `Σ_g,mfg,eff` | Possible, through scrap (C3). | Possible, through scrap (C3). |
| Material terms versus `Σ_g,mfg,eff`, `Σ_comp`, `Σ̇τ` | No. | Upstream losses of delivered carriers (C2). |

Decision flip for C2, illustrative: both sides dissipate all delivered electricity at `T0` = 298.15 K; `P_g` = 10 W, `P_s` = 12 W, `τ` = 10 years = 315 576 000 s; the candidate's material terms exceed the incumbent's by 4.0e6 J/K. On the local basis the operational advantage is 2 116 894.2 J/K [R5] and the candidate loses by 1 883 105.8 J/K [R6]. On a cumulative basis with `r_el` = 3.0 the advantage triples and the candidate wins by 2 350 682.6 J/K [R7].

Yield example for C3, illustrative: `n` = 20 mol net, yield 0.6, `w_ext` = 1820 kJ/mol, `w_conv` = 100 kJ/mol, `w_rm` = 50 kJ/mol, scrap recovery 0.95. Scrap is 13.333 mol; its correct burden is 3180.0 kJ (10 665.8 J/K); charging it as fresh virgin precursor would give 25 600.0 kJ (85 862.8 J/K); omitting it gives zero [R8].

### D2 (Q2). Extraction charged once: ledger over m replacements

One element, amount `n` per unit, recovery `R`. Sub-accounts for remelt, conversion, transport and manufacturing are pure destruction with no stock and are left out here. Assumption: dispersal takes the element to the dead state, so the full `b` is destroyed (C17a). All entries in J.

| Event | Resource exergy in | Framework charge | Actual destruction | Metal exergy held afterwards |
|---|---|---|---|---|
| Build first unit | `n·CExC` | `n·(CExC − b)` | `n·(CExC − b)` | `n·b` |
| Each retirement and rebuild, `j = 1..m` | `(1 − R)·n·CExC` | `(1 − R)·n·(CExC − b)` | `(1 − R)·n·(CExC − b)` for make-up `+ (1 − R)·n·b` for dispersal | `n·b` |
| Horizon, case H1: last unit still in service | 0 | 0 | 0 | `n·b` |
| Horizon, case H2: last unit retired, no successor | 0 | 0 | `(1 − R)·n·b` | `R·n·b` |

Sums.

- Resource exergy in: `IN = n·CExC·[1 + m(1 − R)]`.
- Framework charge: `F = n·(CExC − b)·[1 + m(1 − R)]`. Extraction is charged `1 + m(1 − R)` times, as stated.
- Closure requires `IN − stock = destruction`.
  - H1: `IN − n·b = n·(CExC − b)·[1 + m(1 − R)] + m(1 − R)·n·b = F + m(1 − R)·n·b`. The framework is short by `m(1 − R)·n·b`.
  - H2: `IN − R·n·b = F + (m + 1)(1 − R)·n·b`. The framework is short by `(m + 1)(1 − R)·n·b`.
  - Algebra for H2: `−b[1 + m(1 − R)] + b(1 − R)(m + 1) = −b − mb + mRb + mb + b − mRb − Rb = −R·b`, so `F + (m + 1)(1 − R)·n·b = n·[CExC·(1 + m(1 − R)) − R·b] = IN − R·n·b`.

Consequence of each choice:

| Choice | Total extraction-related charge (case H2) | Closes? |
|---|---|---|
| A. As written: never charge `b` | `F` | No; short by `(m + 1)(1 − R)·n·b` |
| B. Charge `(1 − R)·b` at every dispersal, make-up at `CExC − b` | `F + (m + 1)(1 − R)·n·b = IN − R·n·b` | Yes, exactly |
| C. Make-up at full `CExC`, `(1 − R)·b` only at the final retirement | `n(CExC − b) + m(1 − R)·n·CExC + (1 − R)·n·b` (equal to B) | Yes, exactly |
| D. Make-up at full `CExC` and `(1 − R)·b` at every dispersal | B `+ m(1 − R)·n·b` | No; double counts `m(1 − R)·n·b` |

Numbers, illustrative: `n` = 2.0 mol, `CExC` = 1500 kJ/mol, `b` = 400 kJ/mol, `R` = 0.8, `m` = 3, `T0` = 298.15 K. `F` = 3520 kJ (11 806.14 J/K) [R9]. `IN` = 4800 kJ; with the last unit in service the stock is 800 kJ and the gap is 480 kJ [R10]. With the last unit retired the stock is 640 kJ and choice B gives 4160 kJ (13 952.71 J/K) = 4800 − 640 [R11]. Choice D gives 4640 kJ, 480 kJ too many [R12]. The identity is checked for random inputs in R13.

Effect on the comparison, illustrative: incumbent `n(x)` = 0.5 mol, `R` = 0.5, `b` = 300 kJ/mol gives an omitted 75 kJ (251.55 J/K); candidate `n` = 20 mol, `R` = 0.9, `b` = 380 kJ/mol, `m` = 3 gives an omitted 3040 kJ (10 196.21 J/K). Correcting both moves the balance 9944.66 J/K against the candidate [R15]. The present omission therefore favours the candidate in this example.

Caveats against my own claim. (1) If dispersed metal stays metallic over the horizon, the entropy has not yet been generated; charging it is then a commitment convention (C17). (2) The identity needs `CExC` to include the ore's own exergy; a table that counts energy carriers only would understate `IN` by the ore exergy. (3) Possible overlap with the `K·sqrt(τ)` terms (see C4).

### D3 (Q3). Mapping to named allocation approaches

Per mol of one material, quality ratios set to 1, disposal burden `E_D` = 0 unless C4 is adopted (then `E_D = b`):

| Approach | Burden of one life cycle |
|---|---|
| Cut-off, recycled content, "100:0" (K31, K32, K43) | `(1 − R1)·E_V + R1·E_rec + (1 − R2)·E_D` |
| End-of-life recycling, avoided burden, "0:100" (K33, K40) | `(1 − R2)·E_V + R2·E_rec + (1 − R2)·E_D` |
| 50:50 (K38, K39) | `(1 − R1/2)·E_V + (R1/2)·E_rec + (R2/2)·(E_rec − E_V) + (disposal share)·E_D` |
| Circular footprint formula, material part (K36, K37) | `(1 − R1)·E_V + R1·[A·E_rec + (1 − A)·E_V] + (1 − A)·R2·(E_rec − E_V) + (1 − R2)·E_D` |
| Closed loop within one system (K29 clause 4.3.4.3) | `(1 − R)·E_V + R·E_rec` per unit in steady state |
| Framework, whole horizon | `E_V·[1 + m(1 − R)] + (m + 1)·R·E_rec` |

Rewriting the framework total: `E_V·[(m + 1)(1 − R) + R] + (m + 1)·R·E_rec = (m + 1)·[(1 − R)·E_V + R·E_rec] + R·E_V`.

Reading: replacements inside the horizon are treated as a closed loop, which needs no allocation. The first unit is fully virgin (`R1` = 0). The terminal recovered stock is remelted at the system's expense and handed on without credit. In circular-footprint terms the terminal unit corresponds to `A` = 0 with the quality ratio of the outgoing secondary material set to zero, which is not a standard parameter set. In cut-off terms it is a cut-off whose boundary sits after reprocessing instead of at the point where scrap is generated.

Closest named approach: closed-loop recycling for the interior of the horizon, and cut-off (no credit) at the two ends, with the one deviation that the scrap generator pays the terminal remelt.

Numbers, illustrative: `E_V` = 1100 kJ/mol, `E_rec` = 50 kJ/mol, `R` = 0.8. Single life with `R1` = 0: framework 1140; cut-off 1100; avoided burden 260; 50:50 680; circular footprint with an illustrative `A` = 0.2 gives 428 kJ/mol [R16]. Chain of four units (`m` = 3): framework 1920; cut-off chain 1880 (difference 40 = `R·E_rec`); avoided-burden chain 1040 (difference 880 = `R·E_V`) [R17]. Identity checked for random inputs in R18.

Is the difference defensible? As a physical ledger of entropy generated inside the boundary, yes: there are no negative entries in such a ledger, so "no credit" is natural. Two objections remain. First, a physical ledger at time `τ` should not contain the remelt of a unit that is still in service. Second, the incumbent is the `m = 0` case, where the convention is harsher than every named method; under avoided burden a scarce element with high recovery would carry a much smaller burden, which makes the candidate's win harder. The choice must therefore be reported with a sensitivity case (C18).

Exergy-specific allocation. I know of no separate, widely adopted exergy rule for end-of-life allocation. What exists: (1) by-products inside `CExC` handled by substitution of a replaced process in Szargut's work (K1, K2; exact section UNSURE); (2) partition of co-products in proportion to exergy content, the usual "physical relationship" choice for heat and power; (3) exergetic life-cycle assessment, which sums life-cycle irreversibility and treats recycling by system expansion (K15, K16); (4) studies that quantify the exergy and quality loss of recycling loops themselves (K21–K24); (5) entropy production proposed directly as the measure of resource consumption (K19, K20), which is the closest published relative of the framework's J/K ledger; (6) exergy replacement cost for dispersed minerals (K25, K26). Whether Szargut prescribes a rule for scrap inputs is UNSURE.

### D4 (Q4). Asymmetry: proposition and counterexample

Proposition. Let the true incumbent total be `Σ_s,true = Σ_s,charged + Δ_omit − Δ_over`, with `Δ_omit ≥ 0` the omitted stages (conversion, manufacturing, tooling, computation, non-`x` elements) and `Δ_over ≥ 0` any overstatement in the stages that are charged. The reported test is `Σ_g < Σ_s,charged + λ`. The true test is `Σ_g < Σ_s,charged + Δ_omit − Δ_over + λ`. If `Δ_over = 0`, reported win implies true win, because the right-hand side only grows. If `Δ_over > Δ_omit`, a reported win can be a true loss. So "always favours the incumbent" holds if and only if nothing that is charged is overstated.

Counterexample (a), illustrative. The incumbent contains `x` as an oxide, `n(x)` = 0.5 mol. Tabulated for the metal: `CExC` = 2000 kJ/mol, `b` = 800 kJ/mol. For the oxide, per mol of `x`: `CExC` = 500 kJ/mol, `b` = 60 kJ/mol; incumbent processing loses 250 kJ per mol of `x`.
- Framework charge: 0.5 × (2000 − 800) = 600 kJ, or 2012.41 J/K.
- Symmetric, true chain: 0.5 × (500 − 60 + 250) = 345 kJ, or 1157.14 J/K.
- Overcharge: 855.27 J/K [R19].
- If the candidate total net of common terms is 1500 J/K, the framework reports a win (1500 < 2012.41) while the symmetric boundary gives a loss (1500 > 1157.14) [R20].

The physical basis is that reducing an oxide to metal is usually the most lossy step of a metal chain, so a product that never needs the metal should not be charged for it. This counterexample assumes the framework uses the elemental `CExC(x)` whatever the form of `x` in `s` (UNSURE).

Counterexample (b), inside the framework's own inequality: the omitted incumbent stages may be smaller than the incumbent-side overstatement from `λ_ℰ` double counting (R38) or than the candidate-side understatement from uncharged dispersion (R15). The net bias then favours the candidate.

One-sidedness. With `Δ_over = 0` the test is valid for acceptance only. Random trials in R21 confirm zero "win becomes loss" flips and a non-zero number of "loss becomes win" flips when `Δ_omit` is added.

Minimal symmetric boundary: cradle to end of life on both sides with one rule set. For every element of each side, extraction plus conversion to the form used; transport on total mass; manufacturing including yield; amortised tooling; computation on both sides or neither; the same EOL rule. Processes that are identical on both sides may be dropped from both (K29, comparison requirements). Where incumbent data are missing, enter a stated lower bound and label the verdict one-sided.

### D5 (Q5). Dead-state transformations

(1) Gouy–Stodola and location. For an irreversibility with entropy generation `S_gen` [J/K] in surroundings at `T0,k`, the lost work is `W_lost = T0,k·S_gen` [J]. Entropy generated is a fact about the process; lost work depends on the sink. Therefore

`Σ_total = Σ_k W_lost,k/T0,k` [J/K],

and for tabulated upstream chains `Σ_upstream = (CExC − b°)/Tref`. An exergy-basis statement against one declared `T0*`, `B_lost = T0*·Σ_total`, gives the same ordering.

(2) Thermo-mechanical exergy [J/mol]. `b_ph = (h − h0) − T0·(s − s0)` with `h0 = h(T0, p0)`, `s0 = s(T0, p0)`. For a new dead state `(T0', p0')`:

`b_ph' − b_ph = (h0 − h0') − T0'·(s − s0') + T0·(s − s0)`.

(3) Chemical exergy, temperature change at fixed reference composition and pressure. For the reference reaction of the substance, `b = −ΔG_r(T0) + R·T0·Σ_j ν_j·ln(a_j terms)`. Gibbs–Helmholtz: `d(ΔG_r/T)/dT = −ΔH_r/T²`. With constant `ΔH_r`:

`ΔG_r(T0) = (T0/Tref)·ΔG_r° + (1 − T0/Tref)·ΔH_r°`.

The concentration terms scale exactly with `T0`. With `d° = −ΔH_r°` (enthalpy of devaluation):

`b(T0) = (T0/Tref)·b° + (1 − T0/Tref)·d°` [J/mol].

General form without the constant-`ΔH_r` assumption: `b(T0)/T0 = b°/Tref + ∫_{Tref}^{T0} ΔH_r(T)/T² dT`.

Example, illustrative: `b°` = 400 kJ/mol, `d°` = 420 kJ/mol, `T0` = 250 K gives `b(T0)` = 403.230 kJ/mol [R22]; the same value follows from `ΔS_r° = (ΔH_r° − ΔG_r°)/Tref` = −67.08 J/(mol·K) and `−ΔG_r(T0) = −ΔH_r° + T0·ΔS_r°` [R23].

(4) Chemical exergy, change of reference-species chemical potentials at fixed `T0`. Write the reference reaction as `i → Σ_j ν_ij·(reference species j)`, with negative `ν_ij` for co-reactants taken from the environment. Then `b_i = g_i(T0, p0) − Σ_j ν_ij·μ_j,env` and

`Δb_i = −Σ_j ν_ij·Δμ_j,env`, with `Δμ_j,env = R·T0·ln(p_j'/p_j)` for an ideal-gas reference species.

Example, illustrative: metal `M + ½ O2 → MO`, so `ν_O2 = −½`. Lowering the ambient oxygen partial pressure from 20.39 kPa to 1.0e-5 Pa at 298.15 K raises the exergy of O2 by 53 138 J/mol and lowers `b(M)` by 26 569 J/mol if the oxide stays the reference species [R26]. At low enough oxygen pressure the metal, not the oxide, is the stable form and the reference species itself changes. This is why a locally referenced `b_ch` in low Earth orbit is not a usable resource measure.

(5) `CExC` is not transformable. `CExC = Σ_k r_k·b_k`, where both the resource exergies `b_k` and the draw `r_k` belong to a specific chain operating in a specific environment. A different environment changes each `b_k` and would change the technology, hence `r_k`. No shift formula exists; the only defensible use for an Earth supply chain is the tabulated value, converted to entropy with `Tref`.

(6) When is the decision independent of `T0`? If every term were a fixed lost work divided by one `T0`, the inequality would be invariant. It is not, because operational lost work depends on `T0` and upstream losses are fixed at `Tref`.

Decision flip, illustrative: Earth-side lost work 900 kJ (candidate) and 600 kJ (incumbent); physical operational entropy generation in orbit 1500 J/K (candidate) and 2700 J/K (incumbent). Correct entropy basis: 3018.61 + 1500 = 4518.61 J/K against 2012.41 + 2700 = 4712.41 J/K; candidate wins by 193.80 J/K. Framework with `T0` = 200 K: 4500 + 1500 = 6000 J/K against 3000 + 2700 = 5700 J/K; candidate loses by 300 J/K [R24, R25].

(7) Non-equilibrium environment. In orbit the surroundings are not one reservoir (sunlight, planetary infrared, deep space). No unique dead state exists; `T0` must be declared as the reservoir to which heat is finally rejected, and every other reservoir becomes a resource to be listed in the budget of D6.

### D6 (Q6). Bounds and directions for the recovery test

Logic. Let `B_avail` be the true maximum exergy the route can draw and `B_req` the true minimum it needs. Feasible implies `B_req ≤ B_avail`. The test declares INFEASIBLE when `L > U`. That verdict is sound if and only if `L ≤ B_req` and `U ≥ B_avail`. Errors that raise `U` or lower `L` only weaken the test (some infeasible routes are "not excluded"), which is safe for a necessary condition. Errors that lower `U` or raise `L` can produce a false INFEASIBLE, which is unsafe.

| Item | Bound type | Direction |
|---|---|---|
| `η_L·q_solar` for the full, undiluted solar spectrum | Upper bound on work from that radiation | Safe |
| `η_L·q_solar` applied to diffuse or diluted sunlight | Overestimate | Safe, loose |
| `η_L·q_solar` applied to spectrally filtered sunlight | Can be exceeded, by at most `(x/3)(1 − x³)` | Slightly unsafe; use `1 − x` for a proof |
| `η_L` fixed at 0.933 when `T0 < 300 K` | Underestimate | Unsafe |
| `η_L` fixed at 0.933 when `T0 > 300 K` | Overestimate | Safe |
| `q_thermal·(1 − T0/T_source)`, `T_source ≥ T0`, conducted or radiated heat | Upper bound (Carnot; for radiation it exceeds the Petela factor by `(y/3)(1 − y³)`, `y = T0/T_source`) | Safe |
| Same formula with `T_source < T0` | Negative, true value positive | Unsafe |
| Omitted cold sinks, wind, chemical gradients, stored or imported exergy | Missing non-negative terms | Unsafe |
| `A` below the largest available area | Underestimate | Unsafe |
| Perfect storage; all intercepted exergy given to recovery | Overestimate | Safe |
| `ΔG_recovery` at true activities (`ΔG° + R·T·ln Q`) | Lower bound on the requirement | Safe |
| `ΔG_recovery` above the true minimum | Overestimate of the requirement | Unsafe |

Landsberg or Petela factor. A reversible converter receives blackbody radiation (energy flux `e_s = σTs⁴`, entropy flux `(4/3)σTs³`), emits blackbody radiation at `T0`, and rejects heat `Q` at `T0`:

- energy: `σTs⁴ = σT0⁴ + Q + W`
- entropy, reversible: `(4/3)σTs³ = (4/3)σT0³ + Q/T0`

so `W = σTs⁴·[1 − (4/3)x + (1/3)x⁴]`, `x = T0/Ts`. Values: 0.933335 for (300 K, 6000 K), which is the framework's 0.933; 0.931130 for (298.15 K, 5772 K); 0.953800 for (200 K, 5772 K); 0.999307 for (3 K, 5772 K) [R27]. At 1361 W/m² and `T0` = 200 K the fixed factor gives 1269.81 W/m² where the bound is 1298.12 W/m² [R36].

Provable bound per radiation mode. For a mode of frequency `ν` with photon occupation `n`, energy `hν·n` and entropy `k·σ(n)`, `σ(n) = (1 + n)ln(1 + n) − n·ln n`. Reversible work against ambient occupation `n0`:

`W_mode = hν·(n − n0) − T0·k·[σ(n) − σ(n0)]`.

Since `k·dσ/dn = hν/T_b(n)` with `T_b` the brightness temperature, and `T_b` increases with `n`, `k·[σ(n) − σ(n0)] ≥ hν·(n − n0)/T_b(n)`, hence

`W_mode ≤ hν·(n − n0)·(1 − T0/T_b(n)) ≤ hν·n·(1 − T0/Ts)` whenever `T_b ≤ Ts`.

Scattering and absorption cannot raise brightness temperature, so `(1 − T0/Ts)·q_solar` bounds any terrestrial sunlight. Carnot is 0.948345 at (298.15 K, 5772 K), which is 0.017216 above Landsberg [R28]. The per-mode inequality is checked numerically in R35.

Dilution. In reduced variables `u = hν/(k·Ts)`, `n_s(u) = 1/(e^u − 1)`, `n0(u) = 1/(e^{u/x} − 1)`, for a beam of fixed étendue:

`ψ = ∫ u²·{u·(n − n0) − x·[σ(n) − σ(n0)]} du / ∫ u³·n_solar du`.

- Full blackbody, `n = n_s`: `ψ = 1 − (4/3)x + (1/3)x⁴` exactly [R32].
- High-pass filtered, undiluted (`n = n_s` for `u ≥ 2.266`, about 1.1 µm; ambient below): hand estimate `ψ ≈ 0.9355`, above Landsberg and below Carnot [R33]. From `ψ ≈ 1 − x·(1 + N/D)` with `N = ∫ −u²·ln(1 − e^{−u}) du`, `D = ∫ u³/(e^u − 1) du` over `u ≥ u_c`, `N/D ≈ 0.2479`.
- Sunlight spread over the hemisphere, `n = ε·n_s` with `ε` = 2.1627e-5, against an ambient-temperature sky background (`n = max(ε·n_s, n0)`): hand estimate `ψ ≈ 0.734` [R34a]. The Landsberg factor overstates it by about a quarter, which is the safe direction.
- Same, but with no thermal background in the sky (`n = ε·n_s` at all `u`): `ψ ≈ 0.838` [R34b]. The difference from the previous case is the cold-sky resource, `(1/3)x⁴/ε ≈ 0.1097` of the solar flux. For small `n`, `S/E ≈ [2ζ(3)·(1 − ln ε) + π⁴/15 − π⁴/180]/(π⁴/15)` in units of `k/(k·Ts)`.

Cold radiative sink. Mirror image of the Landsberg balance: ambient heat at `T0` is free, the converter exchanges radiation with a sky at `T_c`:

- energy: `σT_c⁴ + Q = σT0⁴ + W`
- entropy: `(4/3)σT_c³ + Q/T0 = (4/3)σT0³`

so `W = σ·[(1/3)T0⁴ − (4/3)T0·T_c³ + T_c⁴]` per unit sky-facing area, zero at `T_c = T0`. At `T0` = 300 K: `σT0⁴` = 459.300 W/m²; limit for `T_c → 0` is 153.100 W/m²; a single blackbody emitter fed by a Carnot engine reaches `(27/256)·σT0⁴` = 48.442 W/m² at an emitter temperature of 225 K; an effective sky at 270 K allows 8.007 W/m² [R29]. I recall the 153.1 and 48.4 W/m² values from K67 but the citation is UNSURE; the derivation above stands on its own.

False-infeasible example, illustrative: 1 m², 24 h, mean solar irradiance 200 W/m², no thermal source. Framework budget 0.933 × 200 × 86 400 = 16.122 MJ. A demand of 20 MJ is declared INFEASIBLE. Adding the deep-space cold-sink bound, 13.228 MJ, gives 29.350 MJ and the route is not excluded. With a 270 K effective sky the extra is only 0.692 MJ (total 16.814 MJ) and the verdict stands [R30]. So the suspicion is right in logic, and its practical weight depends on the sink temperature chosen (C24).

Sign error example: `T_source` = 250 K, `T0` = 300 K, 100 W/m². Framework term −20 W/m²; correct +20 W/m² [R31].

Note on consistency with the dead state: if a reservoir colder than `T0` is available without limit, `T0` was not the dead state and should be redefined. A radiative sky sink is flux-limited, so it stays a separate budget line.

### D7 (Q7). `λ_ℰ`: average, marginal, double count

Let infrastructure exergy be `B_infra(N) = F + v·N` [J] for `N` functional units over the infrastructure life, `F` fixed and `v` proportional.

- Average share: `B_infra/N = F/N + v`. This is `T0·λ_ℰ`.
- Marginal effect of removing `ΔN ≪ N` units: `v·ΔN`. Per unit: `v`.
- Removing all `N` units and not rebuilding: `F + v·N`. Per unit: `F/N + v`, the average.

So `λ_ℰ` is the correct per-unit figure only for the all-or-nothing case, which is what "credited only if x leaves the whole system" describes, provided `F` is avoidable and dedicated. Illustrative: `F` = 4.0e13 J, `v` = 2.0e4 J/unit, `N` = 1.0e9 units, `T0` = 298.15 K: average 6.0e4 J/unit, `λ` = 201.241 J/K; marginal 67.080 J/K [R37].

System-level form. The decision "remove `x` everywhere" is right when `Σ_k N_k·(Σ_g,k − Σ_s,k) < B_infra,avoidable/Tref`. A per-unit test with a uniform `λ` in every application is sufficient for this but not necessary, and it lets a low-`n(x)` application claim the same credit as a high-`n(x)` one. Illustrative: 9.0e8 units with 0.1 mol and 1.0e8 units with 5 mol sharing 6.0e13 J. Per unit: 201.241 J/K each. Per mole: 34.109 J/K and 1705.432 J/K [R39].

Double count. If the `CExC(x)` source includes capital goods, `n(x)·CExC(x)` already contains `n(x)·B_infra/N_mol`, which is the same average share; `Σ_s + λ_ℰ` then counts it twice, overstating the incumbent by `λ_ℰ`. Illustrative: with 150 J/K of omitted incumbent stages and a double-counted 201.241 J/K, the net bias is 51.241 J/K in the candidate's favour [R38]. Conditions under which there is no double count: the `CExC` source excludes capital goods, or `B_infra` covers only assets outside the `CExC` boundary (for example exploration, or downstream logistics).

Asymmetry. Supply chains of the candidate's elements also have infrastructure. A term that appears only for `x` is a one-sided penalty on the incumbent unless the corresponding share is charged to the candidate.

---

## 3. Computation spec

All inputs are illustrative, made-up but physically plausible. Constants: `Tref` = 298.15 K; gas constant 8.314462618 J/(mol·K); Stefan–Boltzmann constant 5.670374419e-8 W/(m²·K⁴); `Ts` = 5772 K unless stated. Random checks use `numpy.random.default_rng(0)`. Expected values are hand arithmetic to be reproduced. `abs()` denotes absolute value.

| Row | Quantity | Method or formula | Inputs with units | Sanity check or expected range | Tolerance | Supports claim |
|---|---|---|---|---|---|---|
| R1 | Toy-chain `CExC`, stage losses, closure | `CExC = b_ore + b_fuel + W_el/eta_el`; `loss_gen = W_el/eta_el − W_el`; `loss_smelt = b_ore + b_fuel + W_el − b`; check `loss_gen + loss_smelt == CExC − b` | `b_ore` = 30 kJ/mol; `b_fuel` = 900 kJ/mol; `W_el` = 200 kJ/mol; `eta_el` = 0.4; `b` = 400 kJ/mol | `CExC` = 1430; losses 300 and 730; sum 1030 kJ/mol; all positive | 1e-9 relative | C1 |
| R2 | Entropy generated by the toy chain | `(CExC − b)/Tref` | from R1; `Tref` = 298.15 K | 3454.64 J/(K·mol) | ±0.01 J/(K·mol) | C1 |
| R3 | Delivered-basis loss and electricity cumulative factor | `loss_smelt` from R1; `r_el = 1/eta_el` | from R1 | 730 kJ/mol; `r_el` = 2.5; delivered loss < cumulative loss | 1e-9 relative | C2 |
| R4 | By-product substitution mismatch | `CExC_net = CExC − credit`; `apparent = CExC_net − b`; `actual = CExC − b − b_bp`; `mismatch = actual − apparent` | R1 inputs; `b_bp` = 100 kJ/mol; `credit` = 250 kJ/mol | 1180; 780; 930; mismatch 150 kJ/mol (non-zero) | 1e-9 relative | C1 |
| R5 | Operational advantage, local basis | `(P_s − P_g)·tau/T0` | `P_g` = 10 W; `P_s` = 12 W; `tau` = 10 × 365.25 × 86400 s = 315 576 000 s; `T0` = 298.15 K | 2 116 894.2 J/K; positive | ±0.5 J/K | C2 |
| R6 | Margin `Σ_g − Σ_s`, local basis | `D − R5` | `D` = 4.0e6 J/K (candidate material terms minus incumbent's) | +1 883 105.8 J/K; sign positive, candidate loses | ±0.5 J/K | C2 |
| R7 | Margin, cumulative basis | `D − r_el·R5` | `r_el` = 3.0 | −2 350 682.6 J/K; sign negative, candidate wins; sign opposite to R6 | ±1.5 J/K | C2 |
| R8 | Scrap burden: correct, double-counted, omitted | `n_scrap = n·(1/y − 1)`; correct `= n_scrap·[(1 − R_scrap)·w_ext + R_scrap·w_rm + w_conv]`; double `= n_scrap·(w_ext + w_conv)`; each also divided by `Tref` | `n` = 20 mol; `y` = 0.6; `w_ext` = 1820 kJ/mol; `w_conv` = 100 kJ/mol; `w_rm` = 50 kJ/mol; `R_scrap` = 0.95 | `n_scrap` = 13.3333 mol; 3180.0 kJ (10 665.8 J/K); 25 600.0 kJ (85 862.8 J/K); omitted = 0; ordering 0 < correct < double | ±0.1 kJ; ±0.5 J/K | C3 |
| R9 | Framework extraction charge | `F = n·(CExC − b)·(1 + m·(1 − R))`; also `F/Tref` | `n` = 2.0 mol; `CExC` = 1500 kJ/mol; `b` = 400 kJ/mol; `R` = 0.8; `m` = 3 | 3520 kJ; 11 806.14 J/K | 1e-9 relative; ±0.01 J/K | C4, C5 |
| R10 | Closure gap, last unit in service | `IN = n·CExC·(1 + m·(1 − R))`; `stock = n·b`; `gap = IN − stock − F`; compare with `m·(1 − R)·n·b` | R9 inputs | `IN` = 4800 kJ; stock 800 kJ; gap 480 kJ; equals `m(1 − R)nb` | 1e-9 relative | C4 |
| R11 | Corrected charge, last unit retired | `B = F + (m + 1)·(1 − R)·n·b`; check `B == IN − R·n·b`; also `B/Tref` | R9 inputs | 4160 kJ; `IN − 640` = 4160 kJ; 13 952.71 J/K | 1e-9 relative; ±0.01 J/K | C4 |
| R12 | Double-count variant (choice D) | `Dd = n·(CExC − b) + m·(1 − R)·n·CExC + (m + 1)·(1 − R)·n·b`; `excess = Dd − B` | R9 inputs | 4640 kJ; excess 480 kJ `= m(1 − R)nb` | 1e-9 relative | C4 |
| R13 | Random check of the closure identity | For 1000 draws compare `n·[(CExC − b)(1 + m(1 − R)) + b(1 − R)(m + 1)]` with `n·[CExC(1 + m(1 − R)) − R·b]`; also choice C equals choice B | `n` ~ U(0.1, 50) mol; `b` ~ U(10, 1000) kJ/mol; `CExC = b·(1 + U(0.1, 50))`; `R` ~ U(0, 1); `m` integer in 0..10 | max relative difference ≈ machine precision | < 1e-12 relative | C4 |
| R14 | Random check of the full closed form | Build `Σ_g,init + m·R_g + Σ_g,EOL` literally from the prompt's formulas for 3 elements; compare with the closed form in C5; also extract the multiplier of `w_ext,i` and compare with `1 + m(1 − R_i)` | per element `n_i` ~ U(0.1, 50) mol, `w_ext,i` ~ U(100, 5000) kJ/mol, `w_conv,i` ~ U(0, 500) kJ/mol, `w_rm,i` ~ U(10, 200) kJ/mol, `R_i` ~ U(0, 1); `M_G` ~ U(0.1, 10) kg; `b_transport` ~ U(0.1, 5) MJ/kg; `Σ_g,mfg,eff`, `Σ_tooling`, `Σ_comp` ~ U(0, 1e4) J/K; `N_units` integer 1..1000; `m` 0..10; `T0` = 298.15 K; 1000 draws | max relative difference ≈ machine precision | < 1e-12 relative | C5 |
| R15 | Omitted dispersion terms on each side and net shift | incumbent `n_x·(1 − R_x)·b_x`; candidate `(m + 1)·n·(1 − R)·b`; net `= candidate − incumbent`; each divided by `Tref` | incumbent: `n_x` = 0.5 mol, `R_x` = 0.5, `b_x` = 300 kJ/mol; candidate: `n` = 20 mol, `R` = 0.9, `b` = 380 kJ/mol, `m` = 3 | 75 kJ (251.55 J/K); 3040 kJ (10 196.21 J/K); net 2965 kJ (9944.66 J/K), positive, i.e. against the candidate | ±0.01 J/K | C4, C7 |
| R16 | Single-life burden under five conventions | framework `E_V + R·E_rec`; cut-off `E_V` (R1 = 0); avoided burden `(1 − R)·E_V + R·E_rec`; 50:50 `E_V + (R/2)·(E_rec − E_V)`; circular footprint `E_V + (1 − A)·R·(E_rec − E_V)` | `E_V` = 1100 kJ/mol; `E_rec` = 50 kJ/mol; `R` = 0.8; `A` = 0.2 (illustrative, not asserted as a default); `E_D` = 0; quality ratios 1 | 1140; 1100; 260; 680; 428 kJ/mol; framework is the largest | 1e-9 relative | C6, C18 |
| R17 | Four-unit chain totals | framework `E_V·(1 + m(1 − R)) + (m + 1)·R·E_rec`; cut-off chain `E_V + m·[(1 − R)·E_V + R·E_rec]`; avoided-burden chain `(m + 1)·[(1 − R)·E_V + R·E_rec]` | R16 inputs; `m` = 3 | 1920; 1880; 1040 kJ/mol; differences 40 (`= R·E_rec`) and 880 (`= R·E_V`) | 1e-9 relative | C6 |
| R18 | Random check of the mapping identity | compare `E_V·(1 + m(1 − R)) + (m + 1)·R·E_rec` with `(m + 1)·[(1 − R)·E_V + R·E_rec] + R·E_V` | `E_V` ~ U(100, 5000); `E_rec` ~ U(10, 500) kJ/mol; `R` ~ U(0, 1); `m` 0..10; 1000 draws | ≈ machine precision | < 1e-12 relative | C6 |
| R19 | Incumbent charge: framework versus symmetric chain | framework `n_x·(CExC_met − b_met)`; symmetric `n_x·(CExC_ox − b_ox + w_mfg)`; each divided by `Tref`; difference | `n_x` = 0.5 mol; `CExC_met` = 2000 kJ/mol; `b_met` = 800 kJ/mol; `CExC_ox` = 500 kJ/mol x; `b_ox` = 60 kJ/mol x; `w_mfg` = 250 kJ/mol x | 600 kJ → 2012.41 J/K; 345 kJ → 1157.14 J/K; overcharge 855.27 J/K (positive) | ±0.01 J/K | C7 |
| R20 | Verdict flip | evaluate `S_g < S_s` for both values of R19 | `S_g` = 1500 J/K (candidate total net of common terms) | True against 2012.41; False against 1157.14 | exact booleans | C7 |
| R21 | One-sidedness of omission bias | 10 000 draws: `S_g`, `S_s` ~ U(0, 1e4) J/K; `d_omit` ~ U(0, 5e3) J/K; reported `S_g < S_s`; true `S_g < S_s + d_omit`; count (reported win, true loss) and (reported loss, true win) | as stated | first count exactly 0; second count > 0 | exact | C7 |
| R22 | Chemical exergy at a shifted dead-state temperature | `b(T0) = (T0/Tref)·b0 + (1 − T0/Tref)·d0` | `b0` = 400 kJ/mol; `d0` = 420 kJ/mol; `T0` = 250 K; `Tref` = 298.15 K | 403.230 kJ/mol; lies between `b0` and `d0` | ±0.001 kJ/mol | C9 |
| R23 | Gibbs–Helmholtz cross-check of R22 | `dS = (dH − dG)/Tref` with `dG = −b0`, `dH = −d0`; `b(T0) = −(dH − T0·dS)` | R22 inputs | `dS` = −67.08 J/(mol·K); result equals R22 | ±0.01 J/(mol·K); 1e-9 relative against R22 | C9 |
| R24 | Entropy assigned to an Earth-side loss under two divisors | `W/Tref` and `W/T0`; ratio | `W` = 600 kJ; `Tref` = 298.15 K; `T0` = 200 K | 2012.41 J/K; 3000.00 J/K; ratio 1.49075 | ±0.01 J/K; ±1e-5 | C8 |
| R25 | Verdict flip from the divisor | correct `W_g/Tref + S_op,g` versus `W_s/Tref + S_op,s`; framework `W_g/T0 + S_op,g` versus `W_s/T0 + S_op,s`; margins `g − s` | `W_g` = 900 kJ; `W_s` = 600 kJ; `S_op,g` = 1500 J/K; `S_op,s` = 2700 J/K; `Tref` = 298.15 K; `T0` = 200 K | correct 4518.61 vs 4712.41, margin −193.80 J/K (wins); framework 6000 vs 5700, margin +300 J/K (loses); opposite signs | ±0.02 J/K | C8 |
| R26 | Reference-composition shift for oxygen | `d_bO2 = Rgas·T0·ln(p_old/p_new)`; `d_bM = −0.5·d_bO2`; also `bO2_std = Rgas·T0·ln(101.325 kPa/p_old)` | `T0` = 298.15 K; `p_old` = 20.39 kPa; `p_new` = 1.0e-5 Pa | `d_bO2` = 53 138 J/mol; `d_bM` = −26 569 J/mol; `bO2_std` ≈ 3974 J/mol (commonly tabulated near 3.97 kJ/mol, UNSURE) | ±5 J/mol | C9 |
| R27 | Landsberg factor at four dead states | `eta = 1 − (4/3)·x + (1/3)·x**4`, `x = T0/Ts` | (300 K, 6000 K); (298.15 K, 5772 K); (200 K, 5772 K); (3 K, 5772 K) | 0.933335; 0.931130; 0.953800; 0.999307; increases as `T0` falls | ±2e-6 | C12 |
| R28 | Carnot factor and gap to Landsberg | `1 − x`; gap `= (x/3)·(1 − x**3)` and also by subtraction from R27 | `T0` = 298.15 K; `Ts` = 5772 K | 0.948345; gap 0.017216; both gap computations agree | ±2e-6 | C13 |
| R29 | Cold radiative sink bounds | `sig·Ta**4`; ultimate `sig·[(1/3)Ta**4 − (4/3)Ta·Tc**3 + Tc**4]` at `Tc` = 0 and 270 K; single-emitter limit `max over Te of sig·(Ta·Te**3 − Te**4)` by fine scan, compare with `(27/256)·sig·Ta**4` at `Te = 0.75·Ta` | `Ta` = 300 K; `Tc` = 0 K and 270 K | 459.300; 153.100; 8.007; 48.442 W/m² at `Te` = 225 K; bound is zero at `Tc = Ta` and non-negative on [0, Ta] | ±0.005 W/m² | C10 |
| R30 | False-infeasible example | `U_fw = eta·q·A·t`; `U_cold = P_cold·A·t` for the two sinks of R29; verdicts `demand > U` | `eta` = 0.933; `q` = 200 W/m² (24 h mean); `A` = 1 m²; `t` = 86 400 s; demand 20 MJ | `U_fw` = 16.122 MJ (infeasible); with deep-space sink +13.228 MJ = 29.350 MJ (not excluded); with 270 K sky +0.692 MJ = 16.814 MJ (still infeasible) | ±0.002 MJ | C10, C24 |
| R31 | Thermal term for a cold source | framework `q·(1 − T0/Tsrc)`; corrected `q·(T0/Tsrc − 1)` | `q` = 100 W/m²; `T0` = 300 K; `Tsrc` = 250 K | −20 W/m²; +20 W/m² | 1e-9 relative | C11 |
| R32 | Spectral integral reproduces Landsberg | `psi = W/E`; `E = ∫u³·n_s du`; `W = ∫u²·{u·(n − n0) − x·[sg(n) − sg(n0)]} du`; `n_s = 1/expm1(u)`; `n0 = 1/expm1(u/x)` (0 where `u/x` > 700); `sg(n) = (1 + n)·log1p(n) − n·log(n)`, 0 at `n` = 0; trapezoid on `u = logspace(−4, log10(150), 200001)`; here `n = n_s` | `x` = 298.15/5772 | equals R27 second value, 0.931130; also `E` ≈ π⁴/15 = 6.49394 | ±1e-5 | C13 |
| R33 | Exergy fraction of high-pass filtered, undiluted sunlight | same integrals with `n = n_s` for `u ≥ u_c`, `n = n0` below; `E` integrated over `u ≥ u_c` only | `x` = 298.15/5772; `u_c` = 2.266 (about 1.1 µm) | strictly between R27 (0.931130) and R28 (0.948345); hand estimate 0.9355; energy fraction above `u_c` ≈ 0.7655 | ±0.001 on the estimate; ordering must hold exactly | C13 |
| R34a | Exergy fraction of hemispherically diluted sunlight, ambient sky background | same integrals with `n = maximum(eps·n_s, n0)`; `E = eps·∫u³·n_s du` | `x` = 298.15/5772; `eps` = 2.1627e-5 | hand estimate 0.734; must be < R27 | ±0.01 on the estimate | C13 |
| R34b | Same without thermal sky background, and cold-sky share | `n = eps·n_s` for all `u`; also `share = (1/3)·x**4/eps`; cross-check `share` against `(sig·T0**4/3)/(eps·sig·Ts**4)` | as R34a; `T0` = 298.15 K; `Ts` = 5772 K | `psi` ≈ 0.838; `share` = 0.10973; `eps·sig·Ts**4` ≈ 1361.2 W/m²; `sig·T0**4/3` ≈ 149.36 W/m²; `psi(R34b) − psi(R34a)` within 0.02 of `share` | ±0.01 on `psi`; ±1e-4 on `share` | C10, C13 |
| R35 | Per-mode Carnot bound | for random `u` ~ U(0.05, 20), `n` = `f·n_s(u)` with `f` ~ logU(1e-8, 1), keep cases `n > n0`; check `u·(n − n0) − x·[sg(n) − sg(n0)] ≤ u·(n − n0)·(1 − x·ln((1 + n)/n)/u)` and that the right side ≤ `u·n·(1 − x)`; 10 000 draws | `x` = 298.15/5772 | zero violations (allow 1e-12 relative slack) | exact count 0 | C13 |
| R36 | Fixed versus computed Landsberg factor in a cold dead state | `0.933·q` and `eta(T0, Ts)·q` | `q` = 1361 W/m²; `T0` = 200 K; `Ts` = 5772 K | 1269.81 W/m²; 1298.12 W/m²; fixed < computed | ±0.02 W/m² | C12 |
| R37 | Average and marginal infrastructure share | `avg = F/N + v`; `marg = v`; each divided by `Tref` | `F` = 4.0e13 J; `v` = 2.0e4 J/unit; `N` = 1.0e9 units | 6.0e4 J/unit → 201.241 J/K; 2.0e4 J/unit → 67.080 J/K; avg > marg | ±0.001 J/K | C15 |
| R38 | Net bias with double-counted infrastructure | `lambda − d_omit` | `lambda` = 201.241 J/K (R37); `d_omit` = 150 J/K | +51.241 J/K, positive, i.e. net in the candidate's favour | ±0.001 J/K | C16, C7 |
| R39 | Allocation per unit versus per mole | per unit `B/(N1 + N2)`; per mole `B/(N1·n1 + N2·n2)` times `n_k`; each divided by `Tref`; check `N1·share1 + N2·share2 == B` | `B` = 6.0e13 J; `N1` = 9.0e8 units, `n1` = 0.1 mol; `N2` = 1.0e8 units, `n2` = 5 mol | per unit 201.241 J/K each; per mole 34.109 and 1705.432 J/K; closure to `B` | ±0.001 J/K; 1e-9 relative on closure | C15 |

Notes for the implementer: R13, R14, R18, R21 and R35 are identity or inequality checks and need no physical realism. R32–R35 are the only rows needing numerical quadrature; if R32 misses its tolerance, refine the grid before reading R33–R34. R33, R34a and R34b carry hand estimates from series expansions and are the least certain expected values in the table.

---

## 4. Citations

Certainty "sure" means I am confident the work exists and supports the stated use; section numbers given as "not known" were not recalled. "UNSURE" means existence, bibliographic detail or the attributed content needs checking. Nothing here was looked up in this stage.

| Id | Author(s) | Year | Title | Section or equation | Cited for | Certainty |
|---|---|---|---|---|---|---|
| K1 | Szargut, J.; Morris, D. R.; Steward, F. R. | 1988 | Exergy Analysis of Thermal, Chemical, and Metallurgical Processes (Hemisphere) | not known | Definition of cumulative exergy consumption, cumulative degree of perfection, tables of `CExC` and standard chemical exergy; by-product treatment by replaced process | sure |
| K2 | Szargut, J. | 2005 | Exergy Method: Technical and Ecological Applications (WIT Press) | not known | Same as K1, later statement; thermo-ecological cost | sure |
| K3 | Szargut, J.; Morris, D. R. | 1987 | Cumulative exergy consumption and cumulative degree of perfection of chemical processes. Int. J. Energy Research 11(2), 245–261 | not known | `CExC` and its ratio to product exergy | sure |
| K4 | Szargut, J. | 1989 | Chemical exergies of the elements. Applied Energy 32(4), 269–286 | not known | Reference species and standard chemical exergy | sure |
| K5 | Morris, D. R.; Szargut, J. | 1986 | Standard chemical exergy of some elements and compounds on the planet Earth. Energy 11(8), 733–755 | not known | Standard reference environment | sure |
| K6 | Rivero, R.; Garfias, M. | 2006 | Standard chemical exergy of elements updated. Energy 31(15), 3310–3326 | not known | Updated element exergies; shows table dependence on reference choices | sure |
| K7 | Szargut, J.; Ziębik, A.; Stanek, W. | 2002 | Depletion of the non-renewable natural exergy resources as a measure of the ecological cost. Energy Conversion and Management 43(9–12), 1149–1163 | not known | Non-renewable-only indicator, contrast with all-resource `CExC` (C1 condition i) | sure |
| K8 | Kotas, T. J. | 1985 | The Exergy Method of Thermal Plant Analysis (Butterworths) | Appendix on chemical exergy; equation not known | Temperature correction of chemical exergy of the form used in D5(3) | UNSURE (book exists; location and exact form of the formula not confirmed) |
| K9 | Bejan, A. | 2016 | Advanced Engineering Thermodynamics, 4th ed. (Wiley) | chapter on exergy; chapter on solar energy; numbers not known | Gouy–Stodola theorem; comparison of Petela, Spanner and Jeter efficiencies | sure |
| K10 | Bejan, A.; Tsatsaronis, G.; Moran, M. | 1996 | Thermal Design and Optimization (Wiley) | chapter 3 (not confirmed) | Dead state, chemical exergy definitions | sure |
| K11 | Gouy, G. | 1889 | Sur l'énergie utilisable. Journal de Physique 8, 501–518 | not known | Historical origin of the lost-work theorem | UNSURE |
| K12 | Bösch, M. E.; Hellweg, S.; Huijbregts, M. A. J.; Frischknecht, R. | 2007 | Applying cumulative exergy demand (CExD) indicators to the ecoinvent database. Int. J. LCA 12(3), 181–190 | not known | Database-based cumulative exergy indicator; inherits the database's treatment of infrastructure (C16) | sure |
| K13 | Dewulf, J.; Bösch, M. E.; De Meester, B.; Van der Vorst, G.; Van Langenhove, H.; Hellweg, S.; Huijbregts, M. A. J. | 2007 | Cumulative Exergy Extraction from the Natural Environment (CEENE): a comprehensive life cycle impact assessment method for resource accounting. Environ. Sci. Technol. 41(24), 8477–8483 | not known | Alternative cumulative exergy indicator | sure |
| K14 | Dewulf, J.; Van Langenhove, H.; Muys, B.; Bruers, S.; Bakshi, B. R.; Grubb, G. F.; Paulus, D. M.; Sciubba, E. | 2008 | Exergy: its potential and limitations in environmental science and technology. Environ. Sci. Technol. 42(7), 2221–2232 | not known | Review; limits of exergy as a resource measure, reference-environment dependence | sure |
| K15 | Cornelissen, R. L.; Hirs, G. G. | 2002 | The value of the exergetic life cycle assessment besides the LCA. Energy Conversion and Management 43(9–12), 1417–1424 | not known | Life-cycle irreversibility as the indicator | sure |
| K16 | Cornelissen, R. L. | 1997 | Thermodynamics and sustainable development: the use of exergy analysis and the reduction of irreversibility (PhD thesis, University of Twente) | not known | Origin of exergetic LCA | UNSURE (title wording) |
| K17 | Finnveden, G.; Östlund, P. | 1997 | Exergies of natural resources in life-cycle assessment and other applications. Energy 22(9), 923–931 | not known | Ore exergy as a resource input | sure |
| K18 | Ayres, R. U.; Ayres, L. W.; Martinás, K. | 1998 | Exergy, waste accounting, and life-cycle analysis. Energy 23(5), 355–363 | not known | Waste exergy as loss; exergy in LCA | sure |
| K19 | Gößling-Reisemann, S. | 2008 | What is resource consumption and how can it be measured? Theoretical considerations. J. Industrial Ecology 12(1), 10–25 | not known | Entropy production proposed as the measure of resource consumption (closest relative of a J/K ledger) | sure |
| K20 | Gößling-Reisemann, S. | 2008 | What is resource consumption and how can it be measured? Application of entropy analysis to copper production. J. Industrial Ecology 12(4), 570–582 | not known | Worked metal-chain entropy analysis | UNSURE (volume and pages) |
| K21 | Amini, S. H.; Remmerswaal, J. A. M.; Castro, M. B.; Reuter, M. A. | 2007 | Quantifying the quality loss and resource efficiency of recycling by means of exergy analysis. J. Cleaner Production 15(10), 907–913 | not known | Exergy treatment of recycling loops | UNSURE |
| K22 | Castro, M. B. G.; Remmerswaal, J. A. M.; Brezet, J. C.; Reuter, M. A. | 2007 | Exergy losses during recycling and the resource efficiency of product systems. Resources, Conservation and Recycling 52(2), 219–233 | not known | Same | UNSURE |
| K23 | Ignatenko, O.; van Schaik, A.; Reuter, M. A. | 2007 | Exergy as a tool for evaluation of the resource efficiency of recycling systems. Minerals Engineering 20(9), 862–874 | not known | Same | UNSURE |
| K24 | Dewulf, J.; Van der Vorst, G.; Denturck, K.; Van Langenhove, H.; Ghyoot, W.; Tytgat, J.; Vandeputte, K. | 2010 | Recycling rechargeable lithium ion batteries: critical analysis of natural resource savings. Resources, Conservation and Recycling 54(4), 229–234 | not known | Cumulative exergy accounting applied to recycling versus virgin supply | UNSURE |
| K25 | Valero, A.; Valero, A. | 2014 | Thanatia: The Destiny of the Earth's Mineral Resources (World Scientific) | not known | Exergy replacement cost of dispersed minerals (C17 option c) | sure |
| K26 | Valero, A.; Valero, A.; Domínguez, A. | 2013 | Exergy replacement cost of mineral resources. J. Environmental Accounting and Management 1(2), 147–158 | not known | Same | UNSURE |
| K27 | Hau, J. L.; Bakshi, B. R. | 2004 | Expanding exergy analysis to account for ecosystem products and services. Environ. Sci. Technol. 38(13), 3768–3777 | not known | Allocation questions in cumulative exergy accounting | sure |
| K28 | Gutowski, T. G.; Branham, M. S.; Dahmus, J. B.; Jones, A. J.; Thiriez, A.; Sekulic, D. P. | 2009 | Thermodynamic analysis of resources used in manufacturing processes. Environ. Sci. Technol. 43(5), 1584–1590 | not known | Exergy accounting of manufacturing steps (context for `Σ_g,mfg,eff`) | sure |
| K29 | ISO | 2006 | ISO 14044:2006 Environmental management — Life cycle assessment — Requirements and guidelines | 4.3.4.3 (allocation procedures for reuse and recycling); 4.2.3.3 (cut-off criteria) and 4.2.3.7 (comparisons between systems) to be confirmed | Closed-loop and open-loop procedures; equivalence of boundaries in comparisons | sure (clause 4.3.4.3); other clause numbers to be checked |
| K30 | ISO | 2012 | ISO/TR 14049:2012 Illustrative examples on how to apply ISO 14044 to goal and scope definition and inventory analysis | not known | Worked recycling allocation examples | UNSURE (section) |
| K31 | Ekvall, T.; Tillman, A.-M. | 1997 | Open-loop recycling: criteria for allocation procedures. Int. J. LCA 2(3), 155–162 | not known | Taxonomy of cut-off, 50/50 and related procedures | sure |
| K32 | Frischknecht, R. | 2010 | LCI modelling approaches applied on recycling of materials in view of environmental sustainability, risk perception and eco-efficiency. Int. J. LCA 15(7), 666–671 | not known | Recycled-content versus end-of-life recycling approach | sure |
| K33 | Atherton, J. | 2007 | Declaration by the metals industry on recycling principles. Int. J. LCA 12(1), 59–60 | not known | Metals industry position for the end-of-life recycling approach | sure |
| K34 | Allacker, K.; Mathieux, F.; Manfredi, S.; Pelletier, N.; De Camillis, C.; Ardente, F.; Pant, R. | 2014 | Allocation solutions for secondary material production and end of life recovery: proposals for product policy initiatives. Resources, Conservation and Recycling 88, 1–12 | not known | Side-by-side formulas of the named approaches | sure |
| K35 | Allacker, K.; Mathieux, F.; Pennington, D.; Pant, R. | 2017 | The search for an appropriate end-of-life formula for the purpose of the European Commission Environmental Footprint initiative. Int. J. LCA 22(9), 1441–1458 | not known | Derivation and comparison of end-of-life formulas | sure |
| K36 | European Commission | 2021 | Commission Recommendation (EU) 2021/2279 on the use of the Environmental Footprint methods | Annex I, circular footprint formula; section number not known | Circular footprint formula and the allocation factor `A` (no default value is asserted here) | sure |
| K37 | Zampori, L.; Pant, R. | 2019 | Suggestions for updating the Product Environmental Footprint (PEF) method. EUR 29682 EN, JRC115959 | section on the circular footprint formula; number not known | Same formula, technical statement | sure |
| K38 | European Commission | 2013 | Commission Recommendation 2013/179/EU on the use of common methods to measure and communicate the life cycle environmental performance of products and organisations | annex with the end-of-life formula; number not known | 50:50-type end-of-life formula | UNSURE (annex and exact form) |
| K39 | Lindfors, L.-G. et al. | 1995 | Nordic Guidelines on Life-Cycle Assessment. Nord 1995:20, Nordic Council of Ministers | not known | Early statement of the 50/50 rule | UNSURE (whether this is the origin) |
| K40 | Weidema, B. | 2001 | Avoiding co-product allocation in life-cycle assessment. J. Industrial Ecology 4(3), 11–33 | not known | System expansion and avoided burden | sure |
| K41 | Ekvall, T.; Weidema, B. P. | 2004 | System boundaries and input data in consequential life cycle inventory analysis. Int. J. LCA 9(3), 161–171 | not known | Marginal versus average data (C15, C23) | sure |
| K42 | Finnveden, G.; Hauschild, M. Z.; Ekvall, T.; Guinée, J.; Heijungs, R.; Hellweg, S.; Koehler, A.; Pennington, D.; Suh, S. | 2009 | Recent developments in Life Cycle Assessment. J. Environmental Management 91(1), 1–21 | not known | Attributional versus consequential modelling | sure |
| K43 | Wernet, G.; Bauer, C.; Steubing, B.; Reinhard, J.; Moreno-Ruiz, E.; Weidema, B. | 2016 | The ecoinvent database version 3 (part I): overview and methodology. Int. J. LCA 21(9), 1218–1230 | not known | Cut-off system model: recyclable materials leave burden-free | sure |
| K44 | Nordelöf, A.; Poulikidou, S.; Chordia, M.; Bitencourt de Oliveira, F.; Tivander, J.; Arvidsson, R. | 2019 | Methodological approaches to end-of-life modelling in life cycle assessments of lithium-ion batteries. Batteries 5(3), 51 | not known | Compact comparison of cut-off, avoided burden, 50:50 and circular footprint formula | UNSURE (author list and article number) |
| K45 | Ekvall, T.; Björklund, A.; Sandin, G.; Jelse, K.; Lagergren, J.; Rydberg, M. | 2020 | Modeling recycling in life cycle assessment. Swedish Life Cycle Center report | not known | Survey of recycling allocation methods | UNSURE |
| K46 | BSI | 2011 | PAS 2050:2011 Specification for the assessment of the life cycle greenhouse gas emissions of goods and services | annex on recycling (letter not confirmed) | Recycled-content and closed-loop approximation methods | UNSURE (annex) |
| K47 | CEN | 2019 | EN 15804:2012+A2:2019 Sustainability of construction works — Environmental product declarations — Core rules for the product category of construction products | modules A–C and D | No-credit product stage with benefits beyond the boundary reported separately | sure |
| K48 | World Steel Association | 2017 | Life cycle inventory methodology report for steel products | not known | End-of-life recycling approach with scrap credit | UNSURE (year, exact title) |
| K49 | Frischknecht, R.; Althaus, H.-J.; Bauer, C.; Doka, G.; Heck, T.; Jungbluth, N.; Kellenberger, D.; Nemecek, T. | 2007 | The environmental relevance of capital goods in life cycle assessments of products and services. Int. J. LCA 12 (Special Issue 1), 7–17 | not known | Size of capital-goods contributions; whether databases include them (C16) | sure |
| K50 | European Commission, Joint Research Centre | 2010 | ILCD Handbook: General guide for Life Cycle Assessment — Detailed guidance. EUR 24708 EN | chapter on recycling; number not known | Provisions for modelling recycling and for attributional versus consequential studies | sure |
| K51 | Petela, R. | 1964 | Exergy of heat radiation. J. Heat Transfer 86(2), 187–192 | not known | `1 − (4/3)x + (1/3)x⁴` for blackbody radiation | sure |
| K52 | Petela, R. | 2003 | Exergy of undiluted thermal radiation. Solar Energy 74(6), 469–488 | not known | Scope of the formula: undiluted radiation | sure |
| K53 | Landsberg, P. T.; Tonge, G. | 1979 | Thermodynamics of the conversion of diluted radiation. J. Physics A: Math. Gen. 12(4), 551–562 | not known | Dilution factor; entropy and conversion bound for diluted radiation | sure |
| K54 | Landsberg, P. T.; Tonge, G. | 1980 | Thermodynamic energy conversion efficiencies. J. Applied Physics 51(7), R1–R20 | not known | Landsberg efficiency; mode entropy of radiation | sure |
| K55 | Press, W. H. | 1976 | Theoretical maximum for energy from direct and diffuse sunlight. Nature 264, 734–735 | not known | Bound for direct versus diffuse sunlight | sure |
| K56 | Bejan, A. | 1987 | Unification of three different theories concerning the ideal conversion of enclosed radiation. J. Solar Energy Engineering 109(1), 46–51 | not known | Relation between Petela, Spanner and Jeter results | sure |
| K57 | Jeter, S. M. | 1981 | Maximum conversion efficiency for the utilization of direct solar radiation. Solar Energy 26(3), 231–236 | not known | Carnot-form bound for direct radiation | sure |
| K58 | Spanner, D. C. | 1964 | Introduction to Thermodynamics (Academic Press) | not known | `1 − (4/3)x` form | UNSURE |
| K59 | De Vos, A. | 2008 | Thermodynamics of Solar Energy Conversion (Wiley-VCH) | not known | Landsberg limit and its conditions | sure |
| K60 | Green, M. A. | 2003 | Third Generation Photovoltaics: Advanced Solar Energy Conversion (Springer) | not known | Landsberg limit near 93.3 % and Carnot limit near 95 % for 6000 K and 300 K | sure |
| K61 | Candau, Y. | 2003 | On the exergy of radiation. Solar Energy 75(3), 241–247 | not known | Exergy of arbitrary (non-blackbody) radiation | sure |
| K62 | Kabelac, S.; Drake, F.-D. | 1992 | The entropy of terrestrial solar radiation. Solar Energy 48(4), 239–248 | not known | Entropy of direct and diffuse terrestrial sunlight | UNSURE |
| K63 | Chu, S. X.; Liu, L. H. | 2009 | Analysis of terrestrial solar radiation exergy. Solar Energy 83(8), 1390–1404 | not known | Spectral exergy-to-energy ratio of terrestrial sunlight | UNSURE |
| K64 | Wright, S. E.; Rosen, M. A.; Scott, D. S.; Haddow, J. B. | 2002 | The exergy flux of radiative heat transfer for the special case of blackbody radiation. Exergy, An International Journal 2(1), 24–33 | not known | Exergy of radiative transfer; Petela factor versus Carnot factor | UNSURE |
| K65 | Pons, M. | 2012 | Exergy analysis of solar collectors, from incident radiation to dissipation. Renewable Energy 47, 194–202 | not known | Lower exergy content of diffuse radiation | UNSURE |
| K66 | Byrnes, S. J.; Blanchard, R.; Capasso, F. | 2014 | Harvesting renewable energy from Earth's mid-infrared emissions. PNAS 111(11), 3927–3932 | not known | Work from radiative exchange with a cold sky | sure |
| K67 | Buddhiraju, S.; Santhanam, P.; Fan, S. | 2018 | Thermodynamic limits of energy harvesting from outgoing thermal radiation. PNAS 115(16), E3609–E3615 | not known | Limits of about 48.4 and 153.1 W/m² at 300 K against a 3 K sky | UNSURE (the two numbers and page range) |
| K68 | Rosen, M. A.; Dincer, I. | 2004 | Effect of varying dead-state properties on energy and exergy analyses of thermal systems. Int. J. Thermal Sciences 43(2), 121–133 | not known | Sensitivity of exergy results to the dead state | sure |
| K69 | Gaggioli, R. A. | 2012 | The dead state. Int. J. Thermodynamics 15(4), 191–199 | not known | Definition of the dead state for non-equilibrium surroundings | UNSURE |
| K70 | Planck, M. | 1914 | The Theory of Heat Radiation (English translation by M. Masius) | not known | Entropy of a radiation mode as a function of occupation | sure |
| K71 | Rosen, P. | 1954 | Entropy of radiation. Physical Review 96(3), 555 | not known | Mode entropy `(1 + n)ln(1 + n) − n·ln n` | UNSURE |

Totals: 71 entries, 24 marked UNSURE (K8, K11, K16, K20, K21, K22, K23, K24, K26, K30, K38, K39, K44, K45, K46, K48, K58, K62, K63, K64, K65, K67, K69, K71).

---

## 5. Things I could not verify (UNSURE register)

1. Whether the framework uses elemental `CExC(x)` regardless of the form of `x` in the incumbent (basis of counterexample (a) in C7).
2. Whether `n_i` is gross or net and what exactly `Σ_g,mfg,eff` contains (C3).
3. Whether the `K·sqrt(τ)` terms include chemical exergy of material lost in service (possible overlap with C4).
4. Which `CExC` source is used: whether it includes ore exergy, renewables, by-product credits and capital goods (C1, C16).
5. Units of `ΔG_recovery` and the meaning of `n_rec` (C14).
6. Whether the thermal term is clamped at zero in the implementation (C11).
7. Realistic values of `r_el` (C2) and of the exergy-to-energy ratio of real clear-sky direct sunlight relative to `η_L` (C13).
8. Whether Szargut gives an explicit rule for scrap inputs in `CExC` (D3).
9. The hand estimates in R33, R34a and R34b.
10. All citation entries marked UNSURE in section 4, and the clause numbers flagged in K29.
