# Questions for a frontier model (limited-access window)

Context file (`local_docs/`, never cited by the spec). Written 2026-11-12, at the GMS-100 round 2 point of Phase 1.

## How to use the answers (S16)

Whatever the model answers is a claim at level `derived`. It does not raise any validation level, and it does not settle an open question by itself. Each prompt therefore asks for **checkable output**: numbered claims, a test or computation that would falsify each one, and citations with equation or page numbers that we verify ourselves before anything enters `data/sources.bib`. Decisions that follow go through the normal route (user decision, drafting notes §A, review record).

## Selection

Picked for: real uncertainty in the project, a high cost if we are wrong, a need for deep reasoning across physics and literature, and timing (the target document is not drafted yet or is about to be accepted, so a fix is cheap now).

| # | Question | Why it is worth frontier-model time | Blocks |
|---|---|---|---|
| 1 | Does the Class II transport thesis survive its own physics? Split in two: 1a AC skin effect, 1b conjugate heat and electrocatalysis | Could invalidate GMS-310 Part A and the `al_vs_cu_busbar` golden scenario. Nobody has reviewed it; GMS-310 is not drafted yet | W2b GMS-310, Phase 6, Phase 7 scenarios |
| 2 | Is the GMS-100 exergy accounting coherent, and which published allocation practice does it match? | Round 2 is the last review before acceptance. Four open questions (OQ-9, OQ-10, OQ-11, b_ch of dispersed material) and the Phase 5 anchoring requirement depend on it. Contains one suspected logic flaw in the recovery test | GMS-100 acceptance, Phase 5 exit |
| 3 | Lattice fatigue micromechanics (plan Q2, E2, E3) | Named blocker for GMS-220 `active`; needs a structural-mechanics specialist we do not have | GMS-220 `active`, fatigue-based scenarios |
| 4 | (optional) Red-team the breakeven solver lemmas | Executable tests (SymPy, hypothesis) are a cheaper route to `cross-checked`. Use leftover budget only | GMS-400 brief |
| 5 | Is the Class I / Class II demarcation sound and decidable? | The framework's central claim, and the gate decides which scenarios reach the solver. Prompts 1a and 1b found no Class II case where geometry beats the incumbent under the fairness rule (E19). Class I examples look regime-dependent (photon attenuation in the Compton regime; shape anisotropy in magnets). GMS-300 is not drafted | W2b GMS-300 brief, GMS-500, every scenario |
| 6 | How do several degradation mechanisms combine (OQ-20)? | Rates are summed and τ_wearout is the minimum over fatigue load cases with no Miner summation (GMS-220); interacting mechanisms (corrosion fatigue, scale cracking, section loss) may make both non-conservative, and the error direction differs per side | GMS-400 and GMS-500 briefs, OQ-20 owner |
| 7 | (narrow) Which entropy currency across environments (OQ-13)? | E15 uses one evaluation T₀; the alternative divides each loss by its own T₀. They disagree in about 5 % of random cases; a choice of currency that computation cannot settle | GMS-100 revision if OQ-13 flips, any off-Earth scenario |

Not worth the window: drafting the 11 documents, writing lints or test boilerplate (the `AI_value_work.md` items 1, 4 and 5). Our own pipeline already does these, and `spec_lint` exists.

Use one fresh conversation per prompt. Paste the prompt as written; each is self-contained.

**Run order:** 1a (done), then 2, 1b, 3; 4 only with leftover budget. The order follows the drafting loop; see `local_docs/orchestration/fable_delegation_plan.md` §4. Prompts 5–7 added 2026-11-14 (user); proposed order 5, 6, 7, each before the brief it feeds (5 before GMS-300, 6 before GMS-400 and GMS-500; 7 is a low-budget run, §5.1 style).

**Weighing 1a:** the suspicion stated in it is our own unverified reasoning, and its numbers can be checked without the model (a 2-D electromagnetic simulation of the A3 cases). The model's value there is whether any regime or fairer comparison rescues the claim, the correct restated claim, and a falsifying test we can run.

---

## Prompt 1a: Class II transport thesis, AC conduction

```text
You are reviewing a physics claim in an engineering framework. I want an adversarial, quantitative assessment, not encouragement. Treat everything below as an unverified claim.

FRAMEWORK. A candidate "architected geometry" (e.g. an additively manufactured lattice of a common element) is compared with an incumbent solid material containing a scarce element x. The comparison is total entropy generation over the service life, Σ = Σ_init + Σ̇·τ + ..., in J/K, where operational terms are Σ̇ = (power dissipated)/T₀. The framework claims that geometry can replace an element when the function is "transport-governed". This prompt covers its AC conduction claim.

CLAIM A (AC conduction). Joule dissipation per unit length Σ̇ = I_rms²·R_ac/T₀ with
  R_ac = R_dc · ξ · [sinh(2ξ) + sin(2ξ)] / [cosh(2ξ) − cos(2ξ)],  ξ = t_w/δ,  δ = sqrt(ρ_el/(π f μ)).
"At f > 5 kHz thick solid copper bars suffer current constriction. An architected aluminium micro-lattice with strut thickness t_w < δ_Al suppresses eddy currents, enabling aluminium (σ = 3.77e7 S/m) to outperform copper (σ = 5.96e7 S/m) in AC operation."

My suspicion (also unverified): if the lattice is homogenizable, it behaves as a conductor with effective conductivity σ_eff ≈ ρ̄σ_Al/τ (ρ̄ relative density, τ a tortuosity factor). Eddy currents inside each strut are suppressed, but the macroscopic skin effect at the bar scale remains, with δ_eff = sqrt(1/(π f μ σ_eff)). In the thick limit the resistance per unit length scales as 1/(σ_eff·δ_eff·P) ∝ 1/sqrt(σ_eff), which is worse than solid aluminium and solid copper of the same envelope. Without transposition (as in Litz wire), parallel struts do not share current evenly. If this is right, any advantage comes from macro-shape (perimeter, hollow or laminated sections), not from the lattice.

Questions for A:
 A1. Is the quoted R_ac expression the right model for a lattice of struts? State which geometry and field boundary condition it was derived for (e.g. a foil with field on one side, Dowell's layer model) and what replaces it for a 3-D strut lattice, including the proximity effect between struts.
 A2. Is my suspicion correct, wrong, or incomplete? Derive the effective-medium result, state where homogenization breaks down, and say whether ANY lattice regime beats a solid copper bar of the same outer envelope at equal I_rms. Compare also against the fair alternatives a designer would actually use: a hollow copper or aluminium tube, laminated strips, Litz wire.
 A3. Give a worked comparison: rectangular busbar envelope 10 mm × 100 mm, f = 10 kHz and 100 kHz, I_rms = 1 kA. Compute R_ac per metre for: solid Cu, solid Al, Al lattice at ρ̄ = 0.3 (state your σ_eff assumption), and a thin-walled Al section of equal mass. Show formulas and numbers so I can check them.
 A4. Name an independent open-source tool (e.g. a 2-D FEM magnetics solver) and a specific setup that would test A2 and A3, and the result that would falsify your conclusion.
 A5. Verdict: is "lattice suppresses skin effect so Al beats Cu" a valid substitution mechanism, a mechanism only at the macro-shape level, or invalid? What restated claim, if any, would be correct?

OUTPUT FORMAT
- Numbered claims (A1.1, A1.2, ...). For each: the claim, your confidence (high/medium/low), and the computation or experiment that would falsify it.
- Citations only with author, year, title, and equation or page number. Mark any citation you are not certain exists as UNSURE. Do not invent references.
- Finish with a one-paragraph verdict: valid / valid with restated scope / invalid, and the restated claim.
```

---

## Prompt 1b: Class II transport thesis, conjugate heat and electrocatalysis

```text
You are reviewing physics claims in an engineering framework. I want an adversarial, quantitative assessment, not encouragement. Treat everything below as an unverified claim.

FRAMEWORK. A candidate "architected geometry" (e.g. an additively manufactured lattice of a common element) is compared with an incumbent solid material containing a scarce element x. The comparison is total entropy generation over the service life, Σ = Σ_init + Σ̇·τ + ..., in J/K, where operational terms are Σ̇ = (power dissipated)/T₀. The framework claims that geometry can replace an element when the function is "transport-governed". This prompt covers two of its claims.

CLAIM B (conjugate heat transfer). An air-cooled electronics heat sink: replace a solid copper fin heat sink (k ≈ 390 W/m/K; e.g. skived fins) with an additively manufactured aluminium heat sink (AlSi10Mg, k roughly 120–180 W/m/K depending on heat treatment: please confirm) using a gyroid/TPMS lattice or pin-fin array with a larger wetted area. Entropy generation (sign already corrected):
  Ṡ_gen = q·A·(1/T_coolant − 1/T_hot) + V̇·ΔP/T₀.
"Larger wetted area compensates for the lower conductivity; the price is fan (pumping) exergy."
 B1. Is the entropy expression complete for this comparison (conduction through base and fins, air temperature rise along the flow, mixing)? Is it right to evaluate pumping work at T₀ and heat transfer at the two temperatures? What single temperature should T_hot be for a heat sink with a non-uniform base?
 B2. At equal heat load, equal envelope and equal fan power, can the Al lattice reach the same or lower thermal resistance (base-to-air) as the Cu fin sink? Use a fin-efficiency argument and state the governing dimensionless groups. Give a worked estimate for a 100 W load on a 60 mm × 60 mm base, 30 mm fin height.
 B3. Which openly published datasets or correlations could anchor this: thermal resistance vs pressure drop or fan power for AM aluminium lattice/TPMS/pin-fin heat sinks and for copper fin sinks, and TPMS/gyroid Nusselt and friction-factor correlations? Say whether the data is in open-access papers, supplementary files or public repositories, or only in figures. Give exact references I can look up; mark any you are unsure exist.

CLAIM C (electrocatalysis). Replace platinum with high-surface-area NiFe foam: j_local = J_apparent / R_f, R_f = A_real/A_proj, and
  η_act = (R T/(α F))·arcsinh(j_local/(2 j₀))   (assumes symmetric transfer coefficients),
  Σ̇_act = I·η_act/T₀, I = J_apparent·A_proj.
 C1. Is the Pt → NiFe substitution chemically like-for-like (which reaction, which electrolyte)? If Pt and NiFe serve different reactions or pH regimes, say so.
 C2. Given typical exchange current densities, what roughness factor would NiFe need to match Pt's activation overpotential at 1 A/cm² apparent? Is that R_f physically reachable, and what limits it (mass transport, bubble blockage, ohmic loss in the foam, utilisation depth)?
 C3. What does the activation-only model omit that would change the verdict?

OUTPUT FORMAT
- Numbered claims (B1.1, B1.2, ..., C1.1, ...). For each: the claim, your confidence (high/medium/low), and the computation or experiment that would falsify it.
- Citations only with author, year, title, and equation or page number. Mark any citation you are not certain exists as UNSURE. Do not invent references.
- Finish with a one-paragraph verdict per claim: valid / valid with restated scope / invalid, and the restated claim.
```

---

## Prompt 2: GMS-100 exergy accounting coherence

```text
Review the exergy accounting of a lifecycle comparison framework. I want logical and thermodynamic consistency checks, and a mapping to established practice in exergy analysis and LCA. Treat everything as unverified.

SETUP. Dead state T₀. All costs are entropy-generation equivalents in J/K (lost work / T₀, Gouy–Stodola). A candidate geometry g (elements i, amounts n_i) is compared with an incumbent material s containing scarce element x (amount n(x)). Geometry wins at horizon τ when
  Σ_g(τ) < Σ_s(τ) + λ_ℰ(x),   λ_ℰ(x) = B_infra(x)/(T₀·N_alloc(x)),
where λ_ℰ is a per-functional-unit share of the supply-chain infrastructure exergy for x, credited only if x leaves the whole system.

Per side:
  Σ_g(τ) = Σ_g,init + Σ̇_g τ + m(τ)[R_g + K_g sqrt(τ_w)] + K_g sqrt(τ − m τ_w) + Σ_g,EOL      (m(τ) replacements, wear-out life τ_w)
  Σ_s(τ) = Σ_s,init + Σ̇_s τ + K_s sqrt(τ) + Σ_s,EOL                                        (incumbent never replaced)
Material terms:
  w_lost,ext(x) = CExC(x) − b_ch(x)    (cumulative exergy consumption minus standard chemical exergy, per mol)
  Σ_s,init = [n(x)·(CExC − b_ch) + M_s·b_transport]/T₀
  Σ_s,EOL  = (n(x)/T₀)·R_rec·w_lost,remelt          (recovered fraction remelted; unrecovered fraction 1 − R_rec dispersed, not replaced)
  Σ_g,init = [Σ_i n_i·w_lost,prec,i + M_G·b_transport]/T₀ + Σ_g,mfg,eff + Σ_tooling/N_units + Σ_comp/N_units
             (w_lost,prec includes extraction lost work; Σ_g,mfg,eff covers manufacturing including yield losses)
  Σ_g,EOL  = (1/T₀)·Σ_i n_i·R_rec,i·w_lost,remelt,i           (unit in service at the horizon)
  Σ^ret_EOL = (1/T₀)·Σ_i n_i·[R_rec,i·w_lost,remelt,i + (1 − R_rec,i)·w_lost,ext,i]   (retired unit: restores full inventory for its successor)
  R_g = [Σ_i n_i·w_conv,i + M_G·b_transport]/T₀ + Σ_g,mfg,eff + Σ^ret_EOL,   w_conv = w_lost,prec − w_lost,ext
Stated conventions: virgin extraction is charged 1 + m(1 − R_rec) times; the incumbent is charged extraction of x and transport only, while the candidate also pays precursor, manufacturing, tooling and computation (acknowledged asymmetry, said to favour the incumbent); computation is charged delivered electricity only.

Recovery budget test (a separate check on whether a chemical recovery route for x can be powered by on-site environmental exergy):
  Ḃ_intercepted(t) = A·[η_L·q_solar(t) + q_thermal(t)·(1 − T₀/T_source(t))],  η_L = Landsberg efficiency ≈ 0.933
  Decision: if ΔG_recovery(x) > (1/n_rec)·∫ Ḃ_intercepted dt, the recovery route is INFEASIBLE; otherwise it is not excluded (stated as a necessary condition only).
  Stated open item: exergy from heat sinks colder than T₀ is not included.

QUESTIONS
 Q1. Mixing bases. Σ_init uses cumulative exergy consumption (CExC, an upstream resource indicator) while operational terms are local entropy generation. Is subtracting b_ch (treating chemical exergy as retained in the product) consistent with how CExC tables are constructed? Is anything double counted or omitted between CExC, b_ch, w_lost,prec and Σ_g,mfg,eff?
 Q2. Dispersion. When the unrecovered fraction 1 − R_rec is dispersed, its chemical exergy b_ch is destroyed. Should Σ_EOL and Σ^ret_EOL charge it? Show the consequence of each choice for extraction being charged once, i.e. whether charging b_ch on dispersion plus (CExC − b_ch) on make-up double counts or exactly completes the account.
 Q3. Allocation. Map the EOL and replacement convention above onto named approaches in the LCA literature (cut-off / recycled content, end-of-life recycling / avoided burden, 50:50, circular footprint formula, and any exergy-specific allocation, e.g. in Szargut's cumulative exergy work or later exergy-LCA papers). Which one is it closest to, where does it differ, and is the difference defensible? I need citable references (author, year, title, section) that I can check.
 Q4. Boundary asymmetry. Is it true that charging the incumbent only extraction + transport always favours the incumbent? Construct a counterexample if not. What minimal symmetric boundary would you recommend?
 Q5. Dead state. CExC and b_ch are tabulated for a standard reference environment, but the framework lets the dead state differ (e.g. low Earth orbit). What is the correct way to transform them, or is the comparison only meaningful at the standard reference environment? Give the equations.
 Q6. Recovery test logic. The decision "fails → infeasible" is only valid if Ḃ_intercepted is an UPPER bound on the exergy available. Omitting cold sinks (and wind, chemical gradients, stored exergy) makes it a lower bound in those cases, so the test could wrongly declare a feasible route infeasible. Confirm or refute. Separately: for unconcentrated or diffuse terrestrial sunlight, is the Landsberg factor (undiluted blackbody) still a valid upper bound, or is a dilution-dependent bound (e.g. Petela-type) needed? Which direction errs safe for a necessary condition?
 Q7. λ_ℰ. Is crediting a per-unit share of infrastructure exergy for removing x from one product a coherent marginal quantity? Under what conditions does it double count with CExC (which may already include infrastructure)?

OUTPUT FORMAT
- Numbered findings with severity (BLOCKER / MAJOR / MINOR), the exact term affected, and a corrected expression where you propose one.
- For each proposed correction, a small numeric example (made-up but stated values) showing the difference.
- Citations with author, year, title and section or equation number; mark UNSURE where you are not certain the source exists or says this. Do not invent references.
- Separate "logic/consistency findings" (checkable by algebra) from "convention choices" (where practice differs and we must pick).
```

---

## Prompt 3: lattice fatigue micromechanics (plan Q2, E2, E3)

Status (2026-11-13): Q1 and Q2 were answered by low-budget Fable runs (`local_docs/fable_runs/prompt_3_q1_web_answer.md`, `prompt_3_q2_web_answer.md`); the S1 pass for Q3–Q5 takes them as input. Q4 was restated: its first version (macroscopic σ_a = 20 MPa) exceeds the lattice collapse strength (about 7 MPa bending-dominated, 17 MPa stretch-dominated; orchestrator arithmetic, UNSURE), so its dissipation figure (about 3.8e4 J/K per year at 1 Hz) described a part that would not survive.

```text
I need a structural-mechanics assessment of a fatigue model for additively manufactured metal lattices (e.g. gyroid or octet truss, relative density ρ̄ = 0.1–0.4) bonded to or co-printed with a different material. Treat all formulas as unverified.

CURRENT MODEL
 Hysteresis dissipation (entropy generation rate):
   Σ̇ = ν·V·ψ·σ_a²/(2·E·T₀),  σ_a = Δσ/2,  ψ = specific damping capacity ΔU/U (1e-3 to 1e-2).
   Default "macroscopic" form: V = V_envelope, E = E_eff, σ_a = macroscopic stress amplitude.
   Alternative: V = V_struts, E = E_s, σ_a = strut-level stress.
 Effective modulus: E_eff ≈ E_s·ρ̄² (Gibson–Ashby, bending-dominated).
 Thermal mismatch stress for diurnal cycling ΔT across a bimaterial interface: the original text used Δσ ≈ E_eff·|α₁ − α₂|·ΔT; we believe the solid-constituent moduli should govern, but the exact form is open.
 Life: Basquin, σ_a = σ_f'·(2N)^b, τ_wearout = N/ν.

QUESTIONS
 1. Dissipation. Are the macroscopic and strut-level forms equivalent (same total energy) for a homogenized lattice? Derive the relation, including the knock-down between macroscopic and local strut stress for bending- versus stretch-dominated lattices (state the scaling with ρ̄). Which form is correct to use with a ψ measured on solid coupons?
 2. Thermal mismatch. Give the correct mismatch stress for (a) a lattice co-printed on a solid substrate of a different alloy, (b) a bimaterial strut, (c) a lattice in a housing of another material. Include constraint (uniaxial, biaxial E/(1−ν)), compliance of the lattice, and where the peak stress sits (node, interface, first cell row). State which modulus governs and why.
 3. Fatigue life. Is Basquin with macroscopic stress amplitude acceptable for AM lattices? Summarise how the published lattice-fatigue literature normalises S–N data (e.g. by yield strength or by ρ̄), the role of as-built surface roughness and porosity, and whether a knock-down factor is standard. Give references I can check (author, year, title, figure or equation).
 4. Materiality. For an AlSi10Mg lattice, ρ̄ = 0.2, envelope 1e-3 m³, ψ = 5e-3, T₀ = 300 K, at ν = 1 Hz and separately ν = 1 per day. First check that the load case is elastic and survivable: compare the macroscopic σ_a with the lattice collapse strength, and the peak strut stress with the fatigue strength, for bending- and stretch-dominated cells. Use the largest σ_a that passes both (expected order 1–2 MPa). At that σ_a, compute Σ̇ in W/K with E_eff = E_s·ρ̄² and with E_eff = ρ̄·E_s/9 (octet), and the total entropy generated over the life τ_wearout = N/ν. Compare with plausible manufacturing and material terms (order 1e3–1e5 J/K for a ~1 kg part). Is fatigue dissipation ever material to the comparison, or does fatigue matter only through τ_wearout?
 5. Recommend ONE default form for each of: dissipation, mismatch stress, life. For each, state assumptions, validity range, and the public dataset or test that would anchor it.

OUTPUT FORMAT
- Numbered claims with confidence and a falsifying test.
- Equations in plain text with units.
- Citations with author, year, title and equation/figure number; mark UNSURE where not certain. Do not invent references.
```

---

## Prompt 4 (optional): solver lemma red-team

Use only if budget remains. Executable tests are the main route to `cross-checked` for these claims (plan §9.3).

```text
Find counterexamples or gaps in these mathematical claims. Prefer concrete numeric counterexamples to prose.

f on segment m, local time Δt = τ − t_m ∈ [0, τ_w), t_m = m·τ_w:
  f(Δt) = a·(t_m + Δt) + K_g·sqrt(Δt) − K_s·sqrt(t_m + Δt) + d_m',   d_m' = d₀ + m·R_g + m·K_g·sqrt(τ_w),   K_g, K_s, R_g ≥ 0.
Geometry wins where f < 0.

Claims:
 C1. f'' has at most one zero on (0, τ_w), only when K_s > K_g, at Δt = t_m/(ρ − 1), ρ = (K_s/K_g)^(2/3); so f has at most 3 roots per segment.
 C2. f(t_m⁻) − f(t_m) = −R_g at every boundary (f jumps up by R_g).
 C3. Long-run average slope ā = a + (R_g + K_g·sqrt(τ_w))/τ_w. If ā > 0 geometry eventually loses permanently; if ā < 0 it eventually wins permanently; if ā = 0 it eventually wins when K_s > 0 and is periodic when K_s = 0.
 C4. For fixed τ ≥ τ_w, the cost h(s) = K_g·[m·sqrt(s) + sqrt(τ − m·s)], m = floor(τ/s), is strictly decreasing in s = τ_w; m·R_g is non-increasing in s. Hence a shorter τ_w is never favourable to geometry (used to order optimistic/pessimistic inputs in interval screening).
 C5. Interval screening: if f is evaluated at a "pessimistic" corner (each coefficient at the bound worst for geometry) and an "optimistic" corner, then winning set(pessimistic) ⊆ winning set(any input in the box) ⊆ winning set(optimistic). Is f monotone in every coefficient (a, K_g, K_s, d₀, R_g, τ_w, λ) pointwise in τ, including across segment boundaries where m changes with τ_w?

For each claim: proof sketch or counterexample, and any edge case (K_g = 0, a = 0, τ < τ_w, ties at τ = j·τ_w) where it fails.
```

---

## Prompt 5: Class I / Class II demarcation (GMS-300 gate)

Written 2026-11-14. Feeds the GMS-300 brief (W2b). The "findings so far" paragraph summarises Prompts 1a and 1b (`fable_runs/prompt_1a_synthesis.md`, `prompt_1b_synthesis.md`) and E19; it is our own unverified analysis and is stated as such in the prompt.

```text
You are reviewing the central demarcation claim of an engineering framework. I want an adversarial, quantitative assessment, not encouragement. Treat everything below as an unverified claim.

FRAMEWORK. A candidate "architected geometry" g (e.g. an additively manufactured lattice of common elements) is compared with an incumbent solid material s that contains a scarce element x. The comparison is total entropy generation over the service life, in J/K: Σ = Σ_init + Σ̇·τ + replacement and degradation terms + Σ_EOL, with operational terms Σ̇ = (power dissipated)/T₀. Comparisons are made at equal function. Fairness rule: any design feature that does not depend on removing x (cross-section shape, connection topology, transposition, wall thickness) is available to the incumbent too.

GATE (unverified). Before any comparison a function is classified.
 Class I, "intrinsic invariants": geometry cannot substitute; x is retained. Examples given:
  (1) resonant neutron capture cross-section σ_n(E) (B-10, Cd, Gd versus C or Al);
  (2) photon attenuation by the core-electron photoeffect, μ/ρ ∝ Z⁴/E³: "attenuating 100 keV photons with low-Z carbon metamaterials needs 25–30× the mass of tungsten";
  (3) primary-cell energy density set by valence redox (1–4 eV/atom) versus double-layer capacitance (about 0.002 eV/atom);
  (4) spontaneous exchange coupling J_ex (magnetism), listed without detail.
 Class II, "transport extremals": geometry can substitute. Examples given: thermal resistance (Fourier), viscous dissipation (Navier–Stokes), AC skin-depth crowding (Maxwell), local overpotential and current density (electrocatalysis).
 Findings so far (our own analyses, unverified): in three Class II cases (AC busbar, Al lattice versus Cu; air-cooled heat sink, additively manufactured Al lattice versus Cu fins; NiFe foam versus Pt or Ir-oxide catalysts) the geometric candidate did not beat the incumbent at equal function once the incumbent could use the same geometry. Where geometry helped, the benefit was open to either material, or was paid for in operating work (fan power), or the chemistry was not like-for-like.

QUESTIONS
 G1. Is "transport-governed" a sound criterion for substitutability? State a test that can be decided from the governing equations and constitutive coefficients, for example: is the performance limit set by an intrinsic coefficient that enters the figure of merit with no geometric compensation, or by boundary shape? For each Class II domain, say when geometry can compensate a lower coefficient (k, σ_el, j₀) and at what price (mass, volume, pumping work, ohmic or mass-transport loss), with the scaling law of that price.
 G2. Under the fairness rule, does Class II substitution ever pay? Give the regimes, if any, where geometry lets a less scarce element match a scarcer one while the incumbent is free to use the same geometry, with an order-of-magnitude example for each. If there are none, say so, and state what remains of Class II (for example geometry as a way to use less of x rather than to replace it).
 G3. Check each Class I example.
  (2) Give the mass attenuation ratio W versus C at 100 keV, 500 keV, 1 MeV and 5 MeV, and say where Class I membership fails.
  (1) Can geometry (moderation, self-shielding, spectral shaping) change how much resonant absorber is needed, and which element is actually the scarce one in typical absorber choices?
  (3) Is EDLC versus intercalation a geometry question at all?
  (4) Coercivity and energy product depend partly on microstructure and shape anisotropy (e.g. Alnico, nanocomposite exchange-spring magnets). Which part of the magnetic function is invariant and which is geometric?
 G4. Should the gate classify a (function, operating regime) pair instead of a function? Propose the gate as a decision procedure of at most 5 steps, each checkable from inputs a scenario can supply, with three outcomes: Class I (retain x), Class II (compare), out of scope.
 G5. Verdict: valid / valid with restated scope / invalid, and the restated demarcation in at most 3 sentences.

OUTPUT FORMAT
- Numbered claims (G1.1, G1.2, ...). For each: the claim; equation in plain text with SI units where relevant; confidence (high/medium/low); the computation or experiment that would falsify it.
- Citations only with author, year, title, and equation, table or page number. For attenuation data name the table you rely on and mark values quoted from memory UNSURE. Do not invent references.
- Finish with the verdict paragraph and the proposed gate procedure.
```

---

## Prompt 6: combining degradation mechanisms (OQ-20)

Written 2026-11-14. Feeds the GMS-400 and GMS-500 briefs and the choice of owner for OQ-20. The model summarised in the prompt is GMS-220 (rates summed over load cases; τ_wearout the minimum over load cases, no Miner summation) and GMS-230 (parabolic and linear terms; paralinear sum as an upper bound; feature loss by recession not modelled).

```text
Assess how several degradation mechanisms should be combined in a lifecycle comparison model. Treat all formulas below as unverified, and be adversarial toward them.

SETTING. One unit of a part is in service from age 0. There are two sides: a candidate geometry g and an incumbent material s; each has its own unit. The lifetime cost of each side, in entropy generation (J/K), contains irreversibility rates and a wearout life (after which the unit is replaced by a new one and every clock restarts). Mechanisms are modelled separately:
 - Oxidation (parabolic): metal recession h = sqrt(2·k_p·t_age); each mole of metal consumed costs b_degrad/T₀, giving Σ_ox = K_ox·sqrt(t_age), K_ox in J/K/s^0.5. Scales on separate parts of the surface: coefficients K summed. Paralinear case (scale grows and is lost at a constant rate): the parabolic and linear terms are summed as an upper bound.
 - Active corrosion (linear): h = r_corr·t_age; constant rate Σ̇_corr.
 - Cyclic loading: hysteresis dissipation Σ̇_fat = Σ_l ν_l·V·ψ·σ_a,l²/(2·E·T₀), summed over load cases l (valid for distinct frequencies or uncorrelated loads). Life per load case from Basquin, σ_a = σ_f'·(2N)^b, τ_l = N_l/ν_l. Wearout life τ_wearout = min over load cases; no damage summation.
 - Transport: steady operational dissipation Σ̇_op = P_loss/T₀ (Joule, pumping, heat transfer).
 Current combination rule: Σ̇ = Σ̇_corr + Σ̇_fat + Σ̇_op (rates add); oxidation coefficients add; τ_wearout from fatigue only. A feature consumed by recession is called a wearout mechanism but is not modelled. Reaction heat already counted in b_degrad is not counted again as heat-transfer dissipation.

QUESTIONS
 M1. Additivity of rates. For which pairs is Σ̇_total = Σ_i Σ̇_i exact, a bound (state the direction), or wrong? Consider: (a) operational dissipation that rises as a scale thickens or a section thins (time-dependent electrical or contact resistance, fouling); (b) hysteresis that rises with fatigue damage; (c) scale cracking or spallation under cyclic strain (breakaway, parabolic turning linear); (d) temperature coupling (dissipation heats the part; k_p and r_corr are Arrhenius). Give the coupled form where it matters and a criterion for when the sum is adequate.
 M2. Wearout under several mechanisms. Is the minimum over load cases acceptable, or is linear damage summation (Palmgren–Miner) needed, and how far off can each be? Then interacting mechanisms: corrosion fatigue, oxidation-assisted crack initiation, section loss raising the stress amplitude (σ_a ∝ 1/(h₀ − h(t)) for a wall of thickness h₀), an environment that removes the fatigue limit. Give a screening rule for τ_wearout and quantify how non-conservative "minimum of separate mechanisms" can be (factor on life) in one worked example with stated inputs (e.g. an aluminium alloy in humid or saline air, σ_a near the endurance level, r_corr = 1–10 µm/year, wall or strut thickness 0.3–3 mm).
 M3. Direction of error per side. The verdict compares g with s, so an error that is conservative for one side is non-conservative for the comparison when it hits the other. For each simplification above, say which side it favours, and whether a construction with an upper bound for g and a lower bound for s is available.
 M4. Recommend ONE default combination rule for rates and ONE for wearout life for a first edition: validity range, the cases it must reject or flag, and the public dataset or test that would anchor it (for example corrosion-fatigue S–N data in environment versus air; paralinear oxidation data).

OUTPUT FORMAT
- Numbered claims (M1.1, M1.2, ...). For each: statement; equation in plain text with SI units; confidence (high/medium/low); the test or computation that would falsify it.
- Worked numbers with all inputs stated, so they can be recomputed.
- Citations with author, year, title and equation or figure number; mark UNSURE where not certain. Do not invent references.
- End with "Open points": at most 5 lines.
```

---

## Prompt 7 (narrow): entropy currency across environments (OQ-13)

Written 2026-11-14. Low-budget run (`fable_delegation_plan.md` §5.1 style: one `fable` agent with no tools, block passed verbatim). Background: E15 (GMS-100) adopted currency (A); OQ-13 keeps (B) open; the 5 % disagreement is from `fable_runs/prompt_2_review_code/rv02_dead_state_currency.py`.

```text
Answer one narrow thermodynamics question. Work from first principles. Do not use web search, code execution or any other tool. Treat every formula below as unverified, and be adversarial toward it.

SETTING
A lifecycle comparison ranks two designs by total irreversibility over the service life, reported in J/K. Losses occur in environments with different dead-state temperatures: upstream extraction and manufacturing on Earth (cumulative exergy consumption tabulated at a standard reference environment, T_ref = 298.15 K), and operation elsewhere (for example a spacecraft whose effective environment temperature T₀ is between 150 and 290 K, or a cold climate).

TWO CANDIDATE CURRENCIES (both unverified)
 (A) Lost-work currency: Σ = Σ_k W_lost,k / T₀,eval, with one evaluation temperature for the whole comparison; upstream losses are lost work at the reference environment of their data source.
 (B) Entropy currency: Σ = Σ_k W_lost,k / T₀,k = Σ_k S_gen,k, each loss divided by the dead-state temperature of the environment where it occurred (Gouy–Stodola applied per environment).
 A random-case comparison found that (A) and (B) rank the two designs differently in about 5 % of cases with T₀ between 150 and 290 K.

QUESTION
 1. Which quantity, if either, is the meaningful thing to minimise when the purpose is to compare the resource cost of two designs? Distinguish entropy generation from lost work, which depends on the reservoir the work is referred to. In what sense is entropy from different environments commensurable, and lost work not (or the reverse)?
 2. Can cumulative exergy consumption tabulated at T_ref be turned into entropy generation by dividing by T_ref, and is adding that to operational S_gen at another T₀ consistent?
 3. For each currency, give an example (two designs, stated numbers) where it ranks them in a way that is clearly wrong for a resource comparison, and say why.
 4. One-line verdict: which currency for a first edition, its validity range, and when the two differ by enough to flip a verdict.

OUTPUT FORMAT (strict, keep it short)
- At most 8 numbered claims, most important first, so that a cut-off reply is still useful. Total reply under 1,200 words.
- Each claim: statement; equation in plain text with SI units; confidence (high / medium / low); one test or computation that would falsify it.
- Derivations: only the steps needed to check each claim, no general survey.
- No literature review. If you lean on a known result (Gouy–Stodola, Szargut's cumulative exergy), name it in one line and mark it UNSURE if you are not certain of the exact form. Do not invent references.
- End with "Open points": at most 3 lines on what this answer could not settle.
```

---

## Prompt 8 (narrow): infrastructure credit shared by several products (OQ-14)

Written 2026-11-15; approved by the user the same day. Low-budget run (`fable_delegation_plan.md` §5.1 style: one `fable` agent with no tools, block passed verbatim). Background: E16 (GMS-100) keeps U2's average share and applies λ_ℰ only when x leaves every product that shares B_infra(x); OQ-14 keeps the multi-product veto open. The example numbers are from `fable_runs/prompt_2_review_code/rv03_ledger_and_misc.py` D1–D3 (made-up inputs).

```text
Answer one narrow lifecycle-accounting question. Work from first principles. Do not use web search, code execution or any other tool. Treat every formula below as unverified, and be adversarial toward it.

SETTING
A lifecycle comparison decides, per product, whether a candidate design g should replace an incumbent design s. The incumbent uses a scarce element x; the candidate does not. Costs are total irreversibility per component position, in J/K. The candidate is preferred if
   Σ_g < Σ_s + λ,
where λ is a one-off credit per position for the supply infrastructure of x (mines, refineries) that would no longer be needed if x were no longer used.

CURRENT RULE (unverified)
 λ = B_infra/(T_ref·N_alloc): the infrastructure's cumulative exergy B_infra (J) shared equally over the N_alloc positions that use x, T_ref = 298.15 K.
 λ applies only if x leaves every product that shares the infrastructure (all-or-nothing). Whenever λ > 0, the cumulative exergy of x itself must exclude capital goods, so the infrastructure is not counted twice.

THE PROBLEM
 Two products share the infrastructure. B_infra = F + v·N with fixed part F = 4e13 J and variable part v = 2e4 J per position; N = N1 + N2, N1 = 9e8, N2 = 1e8 positions. Then λ = (F + v·N)/(T_ref·N) = 201.24 J/K per position. The per-position penalty of switching, d_k = Σ_g − Σ_s, is d1 = 150 J/K for product 1 and d2 = 400 J/K for product 2.
 Per-product test: product 1 passes (150 < 201.24), product 2 fails (400 > 201.24). So x stays in product 2, the infrastructure stays, and the credit given to product 1 is not earned.
 System test (both switch): N1·d1 + N2·d2 = 1.75e11 J/K < B_infra/T_ref = 2.01e11 J/K, so switching both is worth it.
 Marginal alternative: λ = v/T_ref = 67.08 J/K, which under-credits by 134.16 J/K per position when both switch.

QUESTION
 1. What is the right decision object when products share infrastructure: a per-product test, a system test over all products, or a test over subsets of products that switch together? Is this a cooperative cost-allocation problem, and does any per-product λ exist that makes every per-product test agree with the system test? If so, under what conditions; if not, why not?
 2. A per-product specification can only use inputs an analyst of one product can know. Give a per-product rule and its validity condition, or show that none exists and say what the specification must report instead (for example a bracket between λ = v/T_ref and the average share, or a verdict conditional on the other products switching).
 3. Which of these change the answer, and how: F only partly avoidable; infrastructure in discrete capacity steps; x also used by products outside the comparison; the products switching at different times.
 4. One-line verdict: the rule for a first edition, its validity range, and when it is wrong by enough to flip a verdict.

OUTPUT FORMAT (strict, keep it short)
- At most 8 numbered claims, most important first, so that a cut-off reply is still useful. Total reply under 1,200 words.
- Each claim: statement; equation in plain text with SI units; confidence (high / medium / low); one test or computation that would falsify it.
- Derivations: only the steps needed to check each claim, no general survey.
- No literature review. If you lean on a known result (for example Shapley value, the core of a cost game), name it in one line and mark it UNSURE if you are not certain of the exact form. Do not invent references.
- End with "Open points": at most 3 lines on what this answer could not settle.
```
