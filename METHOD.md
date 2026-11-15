# Method

This file says how an experiment is run in this repo. An experiment tests a claim of the GMS spec, and the steps below make each result traceable and reproducible.

Every result is at validation level `derived`: shown by reasoning or computation, not by measurement. An experiment never raises a level, however many reviewers agree.

## The seven stages

Models are defaults. Use what you have, but keep the roles apart.

| Stage | Output | Default agent and model | Must not |
|---|---|---|---|
| 1. Question | `question.md` | The human, or an orchestrator with the human's approval | Start before the claim and the spec items are named |
| 2. Design | `design.md` | Strongest available model | Run code. Search the web |
| 3. Execute | `checks/`, `outputs/` | A mid-size model such as Sonnet | Change the physics or the design. Interpret beyond the design's checks |
| 4. Verify sources | `sources.md` | A mid-size model such as Sonnet. A small model such as Haiku for existence checks only | Add new sources as evidence. Send project details in a search |
| 5. Analyse | `answer.md` | Strongest available model | Redo Execute. Re-derive what Design already settled, unless a result contradicts it |
| 6. Review | `review.md`, `review_checks/` | Strongest available model, high effort, fresh context | Edit anyone else's files |
| 7. Decide | `decision.md` | The orchestrator proposes. The human decides | Change the spec, plan or notes before the human agrees |

Run the stages in order. Commit the files of each stage before the next one starts.

## Rules per stage

### Common rules

- Read only the files the stage names. Do not edit files you were not told to write.
- Every number must be reproducible from a saved script.
- Mark anything you could not verify as UNSURE.
- Every result is a claim at level `derived`.

### Design

- Write numbered claims before any result exists. Each claim has a confidence and a falsifying test: the computation that would show it wrong.
- Be adversarial towards the claim under test and towards any suspicion stated in the question.
- Give derivations for each claim.
- Write a computation spec. One row per quantity: method or formula, inputs with units, sanity check or expected range, tolerance, and the claim it supports.
- Mark every input as MEMORY (quoted from memory, to be checked) or LOOKUP (to be read from a named source).
- Make sweep ranges wide enough to bracket the optimum.
- List the citations: author, year, title, and what each is cited for.

### Execute

- One script per check, or per group of rows. Each has a docstring with purpose, spec row IDs and assumptions.
- Scripts run with `python3 <path>` from any directory.
- Save the stdout of each script in `outputs/<script>.txt`.
- Follow the design exactly. Do not change formulas or inputs.
- If a row is unclear, a sanity check fails or a tolerance is missed, write it in `outputs/issues.md` and carry on. Do not resolve it yourself.
- Flag a check that compares an expression with itself. It is an identity, not a pass.
- Never re-baseline an output silently. If a saved output changes, say why in `issues.md`.

### Verify sources

- For each citation, check that the work exists. Check that its title, abstract or record plausibly says what it is cited for.
- For data, check whether it is openly downloadable and under which licence.
- Check every MEMORY input first.
- Grade each row: verified, not found, exists but may not say this, or UNSURE.
- Search only titles, authors and technical terms. Never send project or personal details.
- Candidates you find may be listed in a separate section. They are not evidence.

### Analyse

- Read the design, the outputs, `issues.md` and `sources.md`. Do not redo the computations.
- Where a result contradicts a claim, revise the claim and say so. End with a section "Changed since design".
- Point every number at the script that produces it.
- Quote each verdict magnitude from the output line that defines it, and state the case it covers.
- A procedure revised on its own test cases must say that the test is in-sample.

### Review

- Work independently and adversarially. Agreement with the answer is not validation.
- Re-run every script. Compare with the saved outputs and with every number in the answer.
- Write your own checks in `review_checks/`, with their own outputs.
- Check each derivation. Look for regimes and fair comparisons the answer missed.
- Mark each claim agree, disagree or unsupported. Say whether the verdict follows.
- Spot-check the sources.
- Rate findings BLOCKER, MAJOR or MINOR. Say what still needs measurement or an independent tool, and name the single most decisive check.
- Do not edit the files you review.

### Decide

- Read the answer and the review, not the agents' transcripts.
- Give the human a short synthesis: the verdict, where the reviewer disagrees, what it means for the spec, and the decisions needed.
- Propose. The human decides. Record each decision (D1, D2, ...) with the place it was recorded.

## Skipping stages

- Never skip Review.
- Analyse may be skipped with the human's approval when every check passes and every source is found. Design plus the outputs is then the answer.
- No-tools mode, for a narrow question: Question, Analyse, Review, Decide. The answer is written without tools, so its numbers come from reasoning alone.

## Lessons

- Quote each verdict magnitude from the output line that defines it, and state the case it covers. Reviewers found wrong magnitudes that the author's own outputs already contradicted.
- A no-tools answer cannot see the spec's own construction or its open items. Give the reviewer the spec text the answer could not read.
- Ask the reviewer to test each proposed rule against a case where every alternative is wrong.
- Ask the reviewer to look for the minimal safe rule hidden in the claims, not only to test the verdict.
- When a brief fixes a central case, ask for the boundary of the conclusion over every parameter. A fixed central case can hide a regime.
- Test the exact case the decision names, not a nearby one.
- A dense grid is not a root finder. Cross-check solver results with an independent solver.
- Re-read a brief's worked example against the spec before launching.
- If an agent stops early, check its files before resuming it. They may already be complete.

## Layout of a new experiment

Create a folder `exp_NNN_<slug>/` at the repository root, numbered after the last experiment. File and folder names use `_`.

```
exp_NNN_<slug>/
  question.md       claim, spec IDs under test, the gms-local commit tested, prior expectation
  design.md         claims with falsifying tests, computation spec, inputs (MEMORY / LOOKUP)
  checks/           one script per check
    outputs/        saved stdout per script, and issues.md
  sources.md        source check (several checks: sources/<name>.md)
  answer.md         several answers: answer/<name>.md
  review.md
  review_checks/    reviewer's scripts, with their own outputs/
  decision.md       D1 ... Dn, who decided, where each was recorded
  data/
    SOURCES.md      one row per file: licence, URL, retrieved date, sha256
```

Record the `gms-local` commit you tested in `question.md`. Cite spec items by their IDs.

## Data rule

Commit a data file only if its licence allows redistribution. Otherwise cite the source and its URL in `data/SOURCES.md`, and leave the file out.

## Earlier runs

The 11 runs under `local_docs/fable_runs/` were run with an earlier version of this method, described in `local_docs/orchestration/fable_delegation_plan.md`.
