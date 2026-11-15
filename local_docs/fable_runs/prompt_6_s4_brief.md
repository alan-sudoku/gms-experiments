# Prompt 6 S4 brief (finaliser, `fable` high)

Context file. Written 2026-11-15 by the orchestrator from `local_docs/orchestration/fable_delegation_plan.md` §5, plus the work list from S2 and S3. Budget: capped re-runs (user, 2026-11-15).

## Common rules

Read only the files named here. Do not edit files you were not told to write. Do not commit. Every number you state must be reproducible from a saved script. If you search the web, search only titles, authors and technical terms; never include any project or personal detail. Mark anything you could not verify as UNSURE. Everything you produce is a claim at level `derived` (unverified).

## Task (§5 finaliser)

Repo: `<gms-local>`. Read:

- `local_docs/fable_questions.md`, section "Prompt 6: combining degradation mechanisms (OQ-20)", the fenced block only;
- your plan `local_docs/fable_runs/prompt_6_plan.md`;
- the outputs in `local_docs/fable_runs/prompt_6_code/outputs/`, including `issues.md` and `row_status.md` (the per-domain `issues_A_B.md`, `issues_C.md`, `issues_D.md` only where `issues.md` points to them);
- `local_docs/fable_runs/prompt_6_citations.md`.

Do not redo the computations. Where a result contradicts a claim in the plan, revise the claim and say so. Where a needed number is missing, you may write a small script in `local_docs/fable_runs/prompt_6_code/`, named `s4_*.py`, and save its stdout to `outputs/s4_*.txt`. Run scripts with `python3 <path>`. Write `local_docs/fable_runs/prompt_6_answer.md` in the prompt's OUTPUT FORMAT, with every number pointing to its script, and a final section "Changed since plan".

## Budget cap

Fable budget is limited for this run. Write **at most two** `s4_*` scripts. Do not re-run the full row set for corrected inputs. Recompute only the headline numbers the verdict depends on. For every other row affected, state the direction and rough size of the change and mark it "not recomputed". Spend the budget on judgement, not computation.

## Work list (from S2 and S3)

1. **M03 differs.** b for 2024-T4: the plan uses −0.102 (m = 9.804); a secondary table gives −0.124 (m = 8.06) with the same σ_f' = 900 MPa. Dowling Table 9.1 was not read, so which is right is open. This moves σ_a0 (108.703 MPa), m and every C and E row. Report the headline numbers (σ_a0, the C1/C2 baseline, F_min, F_env, the E4 margin, and anything else the verdict rests on) for both values, and say whether the verdict or any M4 default changes. Do not pick one value as confirmed.
2. **M18 differs.** Δα for Al against alumina is about 15e-6/K (22.8e-6 − 8.1e-6), not 7e-6 (7e-6 fits a Ni-base or Fe-Cr substrate). That roughly doubles the D5/D6 mismatch stress. Restate D5/D6 and any claim that rests on them.
3. **L01 and L06 have no open source** (figures in ASM or paywalled papers only). F_env = 154 therefore rests on the planner's range, not on data. Say so where F_env is used, and give the sensitivity across the planner's range if it decides anything.
4. **A11 (b) FAIL.** Rainflow ratio vs the idealised concurrent-hysteresis ratio differs by more than 10 % in 11 of 24 cases (worst −65.5 %); the bound test passes in all 24. Decide whether the claim was wrong or the test was mis-posed, and revise.
5. **C7 and C10 sweeps did not bracket.** Say what the unbracketed sweep can and cannot support; do not claim an optimum or worst case outside the swept range.
6. **C13 (b): cube-root pit life is shorter than linear,** against the plan's expectation. Explain or revise.
7. **C14 null case undecided.** Decide it or say what input is missing.
8. **E5: the weighted sum is undefined in the spec.** Say what definition you used and that the spec must fix it.
9. **E4: the reading of "0.3·τ₀".** State the reading you adopt, the alternative, and whether the E4 margin (0.181) depends on it.
10. **30 rows hold identity checks** (column "Identity checks flagged" in `row_status.md`). They confirm arithmetic only. Do not count them as evidence for a claim.
11. **In-sample tests.** Where a procedure or default (for example the M4 default rules) is revised on its own test cases, say that the test is in-sample and that an out-of-sample test is still needed.

## Final message

Short: the verdict, claims changed since plan (count and IDs), `s4_*` scripts written, and open points.
