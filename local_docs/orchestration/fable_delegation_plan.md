# Delegation plan: frontier-model question runs

Context file (`local_docs/`, never cited by the spec). Written 2026-11-12. The questions are in `local_docs/fable_questions.md`; answers, code and reviews go in `local_docs/fable_runs/`.

## 1. Purpose

Fable access is limited. Spend it only on judgement: which mechanism governs, which comparisons are fair, new derivations, deciding what to compute, the restated claim and the verdict. Everything mechanical goes to a cheaper model. Run **one prompt at a time**.

Lesson from Prompt 1a: the Fable writer did everything itself (about 50 minutes, 286k tokens, 70 tool calls). Most of that was writing and debugging a 2-D solver, sweeps, convergence runs and citation lookups. The tight loop between reasoning and computation did catch one error (a Litz formula 35 % low), so the final Fable pass below exists to keep that check.

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
| 1b heat sink, catalysis | B: completeness of Ṡ_gen; fair comparison at equal envelope and fan power; governing groups. C: Pt vs NiFe chemistry; required roughness factor; omitted effects | Fin efficiency and thermal resistance for the 100 W, 60 × 60 mm, 30 mm-fin case (Cu fins vs Al lattice or pin fins); pumping power; R_f needed to match Pt at 1 A/cm² | TPMS/gyroid Nu and friction correlations; AM Al heat-sink datasets and whether they are open; electrocatalysis j₀ sources (`sonnet`: needs judgement on open access) | Yes | Largest saving: the computations are simple |
| 2 GMS-100 accounting | Almost all the work: Q1–Q7 findings, corrected expressions, conventions vs logic | The small numeric examples for each proposed correction | LCA allocation methods (cut-off, avoided burden, 50:50, circular footprint formula), Szargut-type cumulative exergy, Petela dilution (`sonnet`) | Short, or skip if checks pass | Time-sensitive: should land before GMS-100 round 2 acceptance |
| 3 lattice fatigue | Macro vs strut dissipation; mismatch stress cases (a)–(c); Basquin applicability; one default per form | Materiality numbers (question 4); stress-knock-down scaling vs ρ̄; mismatch stress examples | Lattice fatigue S–N normalisation papers; Gibson–Ashby; bimaterial mismatch (`sonnet`) | Yes | — |
| 4 solver lemmas (optional) | Skip Fable | `sonnet`: SymPy and hypothesis checks of C1–C5, saved as scripts; report any counterexample | — | Only if a counterexample appears and needs interpretation | Executable checks are the main route to `cross-checked` (plan §9.3) |

Order: 1b, 2, 3, then 4 if budget remains. Prompt 2 may run before 1b if GMS-100 round 2 is about to start.

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
| 1b | — | — | — | — | — | — |
| 2 | — | — | — | — | — | — |
| 3 | — | — | — | — | — | — |
| 4 | — | — | — | — | — | — |

Session start prompt for a new session:

> Read `local_docs/orchestration/fable_delegation_plan.md` and act as the orchestrator it describes. Start from §7: Prompt 1a is done and its decisions are recorded. Ask me before starting the next prompt (1b by default, or 2 if GMS-100 round 2 is about to start).
