# Delegation plan: frontier-model question runs

Context file (`local_docs/`, never cited by the spec). Written 2026-11-12. The questions are in `local_docs/fable_questions.md`; answers, code and reviews go in `local_docs/fable_runs/`.

## 1. Purpose

Fable access is limited. Spend it only on judgement: which mechanism governs, which comparisons are fair, new derivations, deciding what to compute, the restated claim and the verdict. Everything mechanical goes to a cheaper model. Run **one prompt at a time**.

Lesson from Prompt 1a: the Fable writer did everything itself (about 50 minutes, 286k tokens, 70 tool calls). Most of that was writing and debugging a 2-D solver, sweeps, convergence runs and citation lookups. The tight loop between reasoning and computation did catch one error (a Litz formula 35 % low), so the final Fable pass below exists to keep that check.

Lesson from Prompt 2 (staged run, 2026-11-12): Fable used 362k tokens (S1 188k with 6 tool calls, about 20 min mostly thinking with no log entries; S4 174k), more than the single-pass 1a, because Prompt 2 is almost all judgement. Fable tool calls fell from 70 to 17, and computation and citation searches moved to Sonnet. What paid off: S2's `issues.md` (an unclear row, a near-tautological check, two inconsistent inputs) gave S4 its work list, and S5 found what S4 missed (a BLOCKER that is a convention choice, a misread scope for λ_ℰ, checks true by construction). Tell S2 that a check comparing an expression with itself must be flagged, not passed. S2 and S3 depend only on S1 and can run in parallel. The session's network blocks arxiv.org, exergoecology.com and api.crossref.org, so S3 works from search snippets for those.

Lesson from Prompt 1b (staged run, 2026-11-13): Fable used about 560k tokens (S1 216k with 7 tool calls, 23 min; S4 344k), more than Prompt 2. S4 was large because S2 raised many issues (3 FAILs, about 18 identity or plausibility-only checks, sweeps that did not bracket the optimum, inconsistent inputs) and S3 corrected several inputs S1 had quoted from memory (Pt j₀ about 3× high, AlSi10Mg data sheet values, embodied-energy basis). Tell S1 to make sweep ranges wide enough to bracket the optimum and to mark every input quoted from memory so S3 checks it first. The first S4 attempt hit the 5-hour usage limit before writing anything; it resumed with SendMessage after the reset, so launch Fable stages early in a usage window. S5 again found what S4 missed (a sign of scope in C3.3; partial substitution as a fair design).

## 2. Roles

The orchestrator is the main session. It launches every agent itself, because a subagent may not be able to launch agents of its own. It also commits after each stage and reports to the user.

| Stage | Role | Model | Effort | Does | Must not |
|---|---|---|---|---|---|
| S1 | Planner | `fable` | high | Claims, derivations, a computation spec, a citation list | Write or run code; search the web |
| S2 | Implementer | `sonnet` | default | Write and run scripts exactly to the spec; save outputs; report spec problems | Change the physics or the spec; interpret results beyond the spec's checks |
| S3 | Citation checker | `sonnet` (`haiku` for pure existence checks) | default | Check that each citation exists and plausibly says what it is cited for; for data, check whether it is openly downloadable | Add new sources as evidence; send any project or personal detail in a search |
| S4 | Finaliser | `fable` | high | Read S2 outputs and S3 results; revise claims where the numbers or sources disagree; write the answer and verdict | Redo S2 work; re-derive what S1 already settled unless a result contradicts it |
| S5 | Reviewer | `opus` | high | Independent adversarial review: re-run all scripts, check derivations, look for missed regimes, check citations | Edit the writer's files |
| S6 | Orchestrator | main session | — | Read the answer and review; summarise for the user; propose decisions | Change the spec, plan or drafting notes without the user's approval |

**When to skip S4.** If every S2 check passes and S3 finds every citation, the orchestrator may ask the user whether to skip S4. In that case S1 plus the outputs is the answer. Never skip S5.

## 3. Hand-off files

All paths are under `local_docs/fable_runs/`; `<p>` is the prompt id (`1b`, `2`, `3`, `4`). File names use `_`.

| File | Written by | Content |
|---|---|---|
| `prompt_<p>_plan.md` | S1 | Numbered claims with confidence and falsifying test; derivations; computation spec (table below); citation list |
| `prompt_<p>_code/*.py` | S2 | One standalone script per spec row, or per group of rows. Docstring: purpose, spec row ids, assumptions. Runs with `python3 <path>` from any directory. numpy and plain Python only; install nothing |
| `prompt_<p>_code/outputs/*.txt` | S2 | Saved stdout of each script |
| `prompt_<p>_code/outputs/issues.md` | S2 | Spec ambiguities, failed checks, deviations. Empty file if none |
| `prompt_<p>_citations.md` | S3 | One row per citation: verified / not found / exists but may not say this / UNSURE, with a note |
| `prompt_<p>_answer.md` | S4 | The final answer in the prompt's OUTPUT FORMAT; every number points to the script that produces it |
| `prompt_<p>_review.md` | S5 | Review (format in §5) |
| `prompt_<p>_review_code/*.py` | S5 | The reviewer's independent checks |

Computation spec format (S1 writes it, S2 follows it):

| Row | Quantity | Method or formula | Inputs with units | Sanity check or expected range | Tolerance | Supports claim |
|---|---|---|---|---|---|---|

## 4. Matrix per prompt

| Prompt | S1 Fable plan | S2 Sonnet compute | S3 citations | S4 Fable final | Notes |
|---|---|---|---|---|---|
| 1a AC conduction | (done in one pass: writer did all stages) | — | — | — | Done. Answer, review and synthesis in `local_docs/fable_runs/`; decisions recorded as E13, plan V10, Q16 |
| 1b heat sink, catalysis (done) | B: completeness of Ṡ_gen; fair comparison at equal envelope and fan power; governing groups. C: Pt vs NiFe chemistry; required roughness factor; omitted effects | Fin efficiency and thermal resistance for the 100 W, 60 × 60 mm, 30 mm-fin case (Cu fins vs Al lattice or pin fins); pumping power; R_f needed to match Pt at 1 A/cm² | TPMS/gyroid Nu and friction correlations; AM Al heat-sink datasets and whether they are open; electrocatalysis j₀ sources (`sonnet`: needs judgement on open access) | Yes | Largest saving: the computations are simple |
| 2 GMS-100 accounting | Almost all the work: Q1–Q7 findings, corrected expressions, conventions vs logic | The small numeric examples for each proposed correction | LCA allocation methods (cut-off, avoided burden, 50:50, circular footprint formula), Szargut-type cumulative exergy, Petela dilution (`sonnet`) | Short, or skip if checks pass | Time-sensitive: should land before GMS-100 round 2 acceptance |
| 3 lattice fatigue | Macro vs strut dissipation; mismatch stress cases (a)–(c); Basquin applicability; one default per form | Materiality numbers (question 4); stress-knock-down scaling vs ρ̄; mismatch stress examples | Lattice fatigue S–N normalisation papers; Gibson–Ashby; bimaterial mismatch (`sonnet`) | Yes | — |
| 4 solver lemmas (optional) | Skip Fable | `sonnet`: SymPy and hypothesis checks of C1–C5, saved as scripts; report any counterexample | — | Only if a counterexample appears and needs interpretation | Executable checks are the main route to `cross-checked` (plan §9.3) |

Order (user, 2026-11-12): **2, 1b, 3**, then 4 if budget remains. Each answer feeds the drafting loop just before its document: Prompt 2 before GMS-100 round 2 and acceptance (the next loop step); Prompt 3 before or during W2a (GMS-220); Prompt 1b before W2b (GMS-310 Part B and C briefs).

## 5. Agent prompt templates

Fill in `<p>` and the paths. Every template includes these **common rules**:

> Read only the files named here. Do not edit files you were not told to write. Do not commit. Every number you state must be reproducible from a saved script. If you search the web, search only titles, authors and technical terms; never include any project or personal detail. Mark anything you could not verify as UNSURE. Everything you produce is a claim at level `derived` (unverified).

**S1 planner (`fable`, high).**
> Read `local_docs/fable_questions.md`, section "Prompt `<p>`", the fenced text block only. Do not answer it in full yet. Write `local_docs/fable_runs/prompt_<p>_plan.md` with: (1) numbered claims, each with confidence and the computation or test that would falsify it; (2) derivations needed for the claims; (3) a computation spec in the table format of `local_docs/orchestration/fable_delegation_plan.md` §3, specific enough that another engineer can implement it without asking (formulas, inputs with units, sanity checks, tolerances); (4) a citation list (author, year, title, what it is cited for). Do not write or run code. Do not search the web. Be adversarial toward the claim in the prompt and toward any suspicion stated in it.

**S2 implementer (`sonnet`).**
> Read `local_docs/fable_runs/prompt_<p>_plan.md`, the computation spec only. Implement every row as standalone scripts in `local_docs/fable_runs/prompt_<p>_code/`, run each with `python3 <path>`, and save stdout to `outputs/<script>.txt`. Follow the spec exactly. Do not change formulas or inputs. If a row is ambiguous, a sanity check fails or a tolerance is missed, record it in `outputs/issues.md` and continue; do not resolve it yourself. Final message: list of scripts, pass/fail per spec row, and issues.

**S3 citation checker (`sonnet` or `haiku`).**
> Read the citation list in `local_docs/fable_runs/prompt_<p>_plan.md`. For each entry, check by web search that the work exists, and whether its title, abstract or bibliographic record plausibly supports what it is cited for. For datasets, check whether the data is openly downloadable (repository, supplementary file) or only shown in figures, and the licence if stated. Write `local_docs/fable_runs/prompt_<p>_citations.md`, one row per entry: verified / not found / exists but may not say this / UNSURE, with a note. Do not add new sources as evidence; you may list candidates you found in a separate section.

**S4 finaliser (`fable`, high).**
> Read `local_docs/fable_questions.md` section "Prompt `<p>`" (fenced block), your plan `prompt_<p>_plan.md`, the outputs in `prompt_<p>_code/outputs/` (including `issues.md`) and `prompt_<p>_citations.md`. Do not redo the computations. Where a result contradicts a claim in the plan, revise the claim and say so. Where a needed number is missing, you may write one small script in the same folder; save its output. Write `local_docs/fable_runs/prompt_<p>_answer.md` in the prompt's OUTPUT FORMAT, with every number pointing to its script, and a final section "Changed since plan".

**S5 reviewer (`opus`, high).** The same brief as the Prompt 1a review, adapted per prompt:
> You are an independent, adversarial reviewer. Inputs: the prompt's fenced block, `prompt_<p>_answer.md`, `prompt_<p>_plan.md`, `prompt_<p>_code/` and its outputs, `prompt_<p>_citations.md`. Do not edit them. Tasks: (1) re-run every script and compare with the saved outputs and with every number in the answer; (2) check the method of any solver or non-trivial computation, with your own independent check where it matters most (saved in `prompt_<p>_review_code/`); (3) check each derivation, especially those the answer marks as unchecked; (4) look for regimes or fair comparisons the answer missed that would change the verdict; (5) agree / disagree / unsupported for each numbered claim, and whether the verdict and any restated claim follow; (6) spot-check citations. Agreement with the answer is not validation. Say which conclusions still need an independent tool or measurement, and the single most decisive check. Write `prompt_<p>_review.md`: Summary verdict (5 lines max); Findings table (#, severity BLOCKER/MAJOR/MINOR, location, finding, evidence or script); Reproducibility table; Derivation checks; Missed regimes; Citations; What still needs external checking.

### 5.1 Low-budget web run: Prompt 3, Q2 first, then Q1 if budget remains

Use when little Fable budget is left (user, 2026-11-13: about 4%). Q2 (thermal mismatch) goes first (user, 2026-11-13). Its form (E3) is the open part of plan Q2, while E2's macroscopic default is already set. Most of Q1 is standard theory: energy equivalence between the two scales, and the ρ̄^1.5 or ρ̄ knock-down. The Opus S1 pass can draft it, and S5 checks it.

Run each question in a new claude.ai chat: paste its block as it is, with no files attached. One chat per question means a cut-off loses only one answer. Alternative used for Q2 (2026-11-13): the orchestrator spawns one Agent per question with `model: fable` and effort `high` (as for S1 and S4 in §2), passing the block verbatim and forbidding all tools; it saves the final message as returned.

1. Chat 1: the Q2 block. Save the reply as it is to `local_docs/fable_runs/prompt_3_q2_web_answer.md`, including a cut-off reply.
2. Chat 2, only if the usage meter still shows room after chat 1: the Q1 block. Save the reply to `local_docs/fable_runs/prompt_3_q1_web_answer.md`.

The rest of Prompt 3 goes through the normal S1–S5 pipeline later: Q3 to Q5, plus Q1 if chat 2 does not run. That S1 pass receives the web answers as input, and S5 reviews them. Every answer is a claim at level `derived`.

**Q4's inputs: restated 2026-11-13 in `fable_questions.md`.** The original materiality case in `fable_questions.md` Prompt 3 Q4 (Al, ρ̄ = 0.2, macroscopic σ_a = 20 MPa) is not elastic. The values below are orchestrator arithmetic with strength constants quoted from memory, so they are UNSURE:
- Lattice collapse strength: about 0.3·ρ̄^1.5·σ_y ≈ 6.7 MPa if bending-dominated, about ρ̄·σ_y/3 ≈ 17 MPa if stretch-dominated (σ_y ≈ 250 MPa for AlSi10Mg).
- Strut stress at 20 MPa: about 224 MPa bending-dominated, about 100 MPa stretch-dominated.
- The prompt's own formula gives Σ̇ ≈ 1.2e-3 W/K at 1 Hz, about 3.8e4 J/K per year. Dissipation therefore looks material, but the part would not survive the load.

Q4 now asks for the largest σ_a that is elastic and survivable (about 1–2 MPa macroscopic), Σ̇ with both the ρ̄² and the octet ρ̄/9 moduli, and the entropy integrated over τ_wearout. A `sonnet` S2 run does the arithmetic.

**Q2 block (chat 1).**

```text
Answer one narrow structural-mechanics question. Work from first principles. Do not use web search, code execution or any other tool. Treat every formula below as unverified, and be adversarial toward it.

SETTING
Additively manufactured metal lattice (gyroid or octet truss), relative density ρ̄ = 0.1–0.4, solid modulus E_s, Poisson ratio ν_s, expansion α_s, joined to a second material (E_2, ν_2, α_2). Uniform diurnal temperature swing ΔT = 10–50 K.

CURRENT MODEL (unverified)
 Original text: Δσ ≈ E_eff·|α₁ − α₂|·ΔT, with E_eff ≈ E_s·ρ̄² (Gibson–Ashby, bending-dominated).
 Our belief: the solid-constituent moduli govern, not E_eff; the exact form is open.
 The stress feeds a Basquin life σ_a = σ_f'·(2N)^b, so what matters is the local peak stress amplitude in the metal.

QUESTION
 2a. Lattice co-printed on, or bonded to, a solid substrate of another alloy (substrate much stiffer, or comparable).
 2b. A bimaterial strut (two alloys along or across the strut axis).
 2c. A lattice in a housing of another material, in contact on its outer faces only (bonded vs sliding).
 For each: the macroscopic and the local strut mismatch stress; the constraint (uniaxial E, biaxial E/(1−ν), triaxial); the role of lattice compliance and the stiffness ratio; where the peak sits (node, interface, first cell row, free edge) and over what distance it decays; which modulus governs and why.
 2d. One-line verdict: one default screening formula, its validity range, and when it is non-conservative by more than a factor 2.

OUTPUT FORMAT (strict, keep it short)
- At most 8 numbered claims, most important first, so that a cut-off reply is still useful. Total reply under 1,200 words.
- Each claim: statement; equation in plain text with SI units; confidence (high / medium / low); one test or computation that would falsify it.
- Derivations: only the steps needed to check each claim, no general survey.
- No literature review. If you lean on a known result, name it in one line and mark it UNSURE if you are not certain of the exact form. Do not invent references.
- End with "Open points": at most 3 lines on what this answer could not settle.
```

**Q1 block (chat 2, optional).**

```text
Answer one narrow structural-mechanics question. Work from first principles. Do not use web search, code execution or any other tool. Treat every formula below as unverified, and be adversarial toward it.

SETTING
Additively manufactured metal lattice (gyroid or octet truss), relative density ρ̄ = 0.1–0.4, solid modulus E_s, under cyclic load at frequency ν, reference temperature T₀.

CURRENT MODEL (unverified)
 Hysteresis dissipation as an entropy generation rate:
   Σ̇ = ν·V·ψ·σ_a²/(2·E·T₀),  σ_a = Δσ/2,  ψ = specific damping capacity ΔU/U (1e-3 to 1e-2).
 Default "macroscopic" form: V = V_envelope, E = E_eff, σ_a = macroscopic stress amplitude.
 Alternative "strut-level" form: V = V_struts = ρ̄·V_envelope, E = E_s, σ_a = strut-level stress amplitude.
 Effective modulus: E_eff ≈ E_s·ρ̄² (Gibson–Ashby, bending-dominated).

QUESTION
 1a. For a homogenized lattice, are the macroscopic and strut-level forms equivalent, meaning the same stored elastic energy per cycle and so the same dissipation? Derive the relation between them.
 1b. Give the knock-down between macroscopic stress and peak or representative strut stress for bending-dominated and for stretch-dominated lattices, with its scaling in ρ̄. Distinguish the energy-equivalent (volume-averaged) strut stress from the peak surface stress. Say which one enters the dissipation and which one enters fatigue life.
 1c. ψ is measured on solid coupons, usually in uniaxial or bending tests. Which form is correct to use with that ψ? State what is lost when a lattice strut is loaded in bending (non-uniform stress through the section, stress-dependent ψ) and whether a correction factor is needed.
 1d. Give a one-line verdict: which form should be the default, and under what condition the two forms disagree by more than a factor of 2.

OUTPUT FORMAT (strict, keep it short)
- At most 8 numbered claims, most important first, so that a cut-off reply is still useful. Total reply under 1,200 words.
- Each claim: statement; equation in plain text with SI units; confidence (high / medium / low); one test or computation that would falsify it.
- Derivations: only the steps needed to check each claim, no general survey.
- No literature review. If you lean on a known result (for example Gibson–Ashby scaling), name it in one line and mark it UNSURE if you are not certain of the exact form or exponent. Do not invent references.
- End with "Open points": at most 3 lines on what this answer could not settle.
```

## 6. Orchestrator procedure

1. Before each stage, make sure the previous stage's files exist. Launch the stage with the template; run agents in the background and wait for the completion notice.
2. After each stage: commit its files with a message `local_docs: prompt <p> S<n> <role>` and push to the session's branch.
3. After S5: read the answer and the review (not the agents' transcripts). Give the user a short synthesis: verdict, where the reviewer disagrees, what it means for the spec (documents, open questions, scenarios), and decisions needed. Propose; do not change the spec, plan or drafting notes until the user agrees.
4. Record user decisions in the usual places: `local_docs/drafting_notes_0.1.md` §A for spec decisions, `local_docs/plan_v2.md` change table for plan changes, `local_docs/orchestration/orchestrator_state.md` §4 for brief notes.
5. Update §7 below, commit, and ask the user before starting the next prompt.

## 7. Status

| Prompt | S1 | S2 | S3 | S4 | S5 | Synthesis to user |
|---|---|---|---|---|---|---|
| 1a | single-pass writer (`fable`, high), `86af299` | in writer pass | in writer pass (existence only, no full text) | in writer pass | `opus` high, done: `prompt_1a_review.md` (0 BLOCKER, 4 MAJOR) | done: `prompt_1a_synthesis.md`; D1–D3 decided and recorded (E13, plan V10, Q16) |
| 1b | `fable` high, `1ce8e11`: 45 claims, 33 rows, 82 citations | `sonnet`, `bea5811`: 33 rows, 3 FAIL (B05, B06, C08), about 18 identity or plausibility-only checks, issues in `issues.md` | `sonnet`, `f488c89`: 72 verified, 3 may not say this, 6 UNSURE, 1 not found; 4 inputs corrected | `fable` high, `0e7ee55` (resumed after the usage limit): B valid with restated scope, C invalid as stated; 19 claims changed; 3 `s4_*` scripts | `opus` high, `659f787`: `prompt_1b_review.md` (0 BLOCKER, 2 MAJOR, 11 MINOR) | done: `prompt_1b_synthesis.md`; D1–D6 decided and recorded (E17, E18, V11, Q17/OQ-16, OQ-4 resolved, GMS-310 brief note); Prompt 2 Gemini citation check reconciled (`prompt_2_citations_reconcile.md`, no fix-item change) |
| 2 | `fable` high, `030e6d1`: 16 findings + 8 conventions, 40 rows, 71 citations | `sonnet`, `1f4daf0`: 40/40 PASS, 6 ambiguities in `issues.md` | `sonnet`: 63 verified, 1 may not say this, 7 UNSURE, 0 not found | `fable` high: `prompt_2_answer.md`, 1 BLOCKER + 7 MAJOR; 4 added checks (`s4_*`) | `opus` high, done: `prompt_2_review.md` (0 BLOCKER, 3 MAJOR, 9 MINOR; L1 re-graded to a convention) | done: `prompt_2_synthesis.md`; D1–D7 decided and recorded (E14–E16, OQ-13 to OQ-15, round 2 fix items); citation re-check with the newly allowed hosts (`sonnet`) done, `prompt_2_citations_recheck.md` (brief `prompt_2_citations_recheck_brief.md`); effect noted in `orchestrator_state.md` §4 (D7) |
| 3 | Low-budget runs (§5.1): Q2 done as a `fable` high agent with no tools (`prompt_3_q2_web_answer.md`: 8 claims; about 79k tokens, 3 min); Q1 done the same way (`prompt_3_q1_web_answer.md`: 8 claims; about 73k tokens, 2 min). Q4's inputs restated (§5.1). S1 for Q3–Q5 with both answers as input: `fable` high, `84323a6` (about 153k tokens, 17 min, 11 tool calls): 26 claims, 32 rows, 65 citations (3 stated gaps); did not read the GMS-220 draft (user, 2026-11-14) | `sonnet`, `8f31706`: 32 rows in 6 pure-Python scripts (system `python3` has no numpy); FAILs mostly rounding in expected values; 11 identity checks flagged; substantive issues in `issues.md` (S term omitted in mismatch expectations, Timoshenko shifts the R7 crossover, R14/R30 sweeps do not bracket every case) | `sonnet`, two passes, `b8c48fe`: 56 verified, 5 exist (content not checked), 2 may not say this, 2 gaps, 0 not found; as-built σ_w7 has no direct source; α_s (Z) 26.6e-6/K above range; Dallago 2018 undercuts stretch-over-bending ordering | — | — | — |
| 4 | — | — | — | — | — | — |

Session start prompt for a new session:

> Read `local_docs/orchestration/fable_delegation_plan.md` and act as the orchestrator it describes. Start from §7: Prompts 1a, 2 and 1b are done and their decisions are recorded. Prompt 3 is in progress: Q1 and Q2 were answered by low-budget Fable runs (§5.1) and Q4 was restated; next is S1 for Q3–Q5 with those answers as input, which needs fresh Fable budget. Ask me before starting it. One prompt per session: when its decisions are recorded, hand off (update §7 and this prompt), and merge to `main`.
