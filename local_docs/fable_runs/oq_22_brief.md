# OQ-22 check brief: does GMS-100's Σ_init price a scarce catalyst? (`sonnet`)

Context file (`local_docs/`, never cited by the spec). Written 2026-11-15 by the orchestrator. User decision 2026-11-15: run the OQ-22 check now, one `sonnet` agent, then an `opus` review. It is not a Fable prompt. Its result decides whether Fable reserve (a) is needed (`orchestration/fable_delegation_plan.md` §4 note after the matrix). It must land before the GMS-310 Part C brief.

## Why

Prompt 5 (`prompt_5_answer.md` G2.6) found that, if Σ_init is cumulative energy demand (CED), a Pt or Ir loading at mg/cm² is worth only about 1 to 3 mV of overpotential at continuous duty, against 30 to 118 mV per decade of exchange current. If GMS-100's own terms give the same, E18's sentence "the substitution case rests on scarcity (Σ_init), not on Σ̇" is reversed, and GMS-100 does not price scarcity. Nobody has evaluated GMS-100's terms for this case. Prompt 8 (D4) added a second task for the same element: decompose the CExC source's supply-chain exergy, and estimate B_infra's parts, to find which of configurations A, B and C (`prompt_8_review.md`, "Fit with the spec" (c)) the spec is in.

## Files you read (only these)

- `docs/spec/1xx_framework/GMS_100_lifecycle_framework.md`, sections 1.2 to 4 (lines 145 to 634) and the Open items (from line 758). These define every term you compute. Use them as written.
- `local_docs/fable_runs/prompt_5_answer.md`, claim G2.6 only (search for "**G2.6**"), and `prompt_5_code/d3_break_even_overpotential.py` with `prompt_5_code/data/d3_cumulative_energy_demand.csv` and `prompt_5_code/data/usgs_mcs2026_world_production.csv`. You may reuse these data files (copy the rows you use into your own `data/` with their source line).
- `local_docs/fable_runs/prompt_8_review.md`, section "Fit with the spec", item (c), and the section "What still needs external checking".

## Conventions (use these; do not choose others)

1. **Basis.** One component position = 1 m² of geometric electrode area of one cell (illustrative). Every term is per m². T₀ = 298.15 K. Report each Σ term in J/K per m² and each break-even in mV.
2. **The comparison.** Side s (incumbent material): the scarce catalyst x on its electrode. Side g (candidate geometry): a non-scarce catalyst (Ni and Fe; take NiFe layered double hydroxide, or NiFe oxide, at 1 to 5 mg/cm² total, declare the composition you use) on the same electrode. Both sides deliver the same current density j for the same operating time τ. The operating difference is the activation term of E12(b): Σ̇_g − Σ̇_s = j·Δη/T₀ per m², with Δη = η_g − η_s the overpotential penalty of the candidate (Δη ≥ 0 assumed).
3. **Break-even.** The candidate wins if Δη < Δη_be with
   Δη_be = T₀·[Σ_s,init + Σ_s,EOL + λ_ℰ(x) − Σ_g,init − Σ_g,EOL] / (j·τ).
   Use EQ-LIFECYCLE-INCUMBENT-INITIAL-CAPITAL, EQ-LIFECYCLE-INCUMBENT-EOL, EQ-LIFECYCLE-GEOMETRY-INITIAL-CAPITAL, EQ-LIFECYCLE-GEOMETRY-EOL and EQ-LIFECYCLE-SUPPLY-CHAIN-COST exactly. No replacement on either side (τ_wearout = ∞ on both; GMS-100 evaluates the incumbent unreplaced; a candidate replacement would only lower Δη_be, say so). K_ox = 0 on both sides. For side g, set tooling and design computation to 0 and use w_lost,prec and Σ_g,mfg^eff values you can source or bound; they are expected to be small, so show that they are, with a stated upper bound.
4. **Costing boundary (OQ-9).** GMS-100 charges side s extraction of x and transport only. Catalyst synthesis, ink and coating on side s are omitted. Omitting them lowers Σ_s, so Δη_be as computed is a lower bound under GMS-100's boundary. If you can bound the omitted stages from a source, report Δη_be with them added as a separate column, marked "outside GMS-100's boundary".
5. **Duty grid.** j ∈ {0.2, 0.5, 1, 2} A/cm² (2e3, 5e3, 1e4, 2e4 A/m²); τ ∈ {2e4, 4e4, 8e4} h of operation at j. Central case: j = 1 A/cm², τ = 8e4 h, for both elements. Report the G2.6 point (j = 0.5 A/cm², τ = 8e4 h) as well.
6. **Loadings.** Ir (acidic PEM anode, as Ir or IrO₂; declare which form your CExC refers to, condition 5 of REQ-LIFECYCLE-CEXC-SOURCE): 0.2, 1 and 2 mg Ir/cm². Pt (PEM cathode): 0.1 and 0.5 mg Pt/cm². These are scenario values for the check, not sourced design values.
7. **CExC.** GMS-100 needs cumulative exergy consumption per mole for the chemical form used. Find the openly readable sources for Pt and Ir (and Ni, Fe for side g): a CExC table, or CED as a stand-in. For each source, test the six conditions of REQ-LIFECYCLE-CEXC-SOURCE one by one (met / not met / not stated, with the evidence). If you use CED as a stand-in, say so in every row that uses it, and give the CED-to-CExC factor you assume, with its source or UNSURE. Report both the primary-route rows and the supply-mix row where the source has both (G2.6 shows why). Report the by-product allocation rule of each source (condition 3); Ir is a co-product of Pt-group and Ni mining, so if a source gives Ir under more than one allocation (mass, economic), compute Δη_be under each.
8. **b_ch.** Take b_ch of Pt, Ir, Ni and Fe from the same reference environment as the CExC source (condition 2). If no b_ch exists at the CExC source's reference environment, use Szargut's standard values, mark the row "condition 2 not met", and report b_ch's share of CExC so its effect is visible.
9. **End of life.** R_rec(x) ∈ {0, 0.5, 0.9, 0.95}; w_lost,remelt(x) from a source if you find one, else bound it and mark UNSURE. Note that by GMS-100's terms a low R_rec on side s adds only b_ch(x) at dispersal, not CExC; say how large that is.
10. **λ_ℰ.** λ_ℰ(x) = B_infra(x)/(T₀·N_alloc(x)). Estimate it through b_infra, the avoidable loop exergy per kilogram of x passing through the loop over τ_infra, so that λ_ℰ ≈ b_infra·m″_x/T₀ when every position has the same loading (state this assumption). Report Δη_be twice: with λ_ℰ = 0 (f₀ of REQ-LIFECYCLE-SHARED-INFRASTRUCTURE-VERDICT, the unconditional case) and with your λ_ℰ estimate. Also report the b_infra (J/kg) that would be needed for Δη_be = 30 mV at the central case.
11. **Carrier basis (OQ-15).** Material terms are cumulative; the operating term is delivered electricity. Report Δη_be as GMS-100 states it (r_el = 1) and, as a diagnostic only, with the operating term multiplied by r_el = 2.5 (Δη_be divided by 2.5).
12. **Scarcity diagnostic (not a GMS-100 term).** If you can find an openly readable exergy replacement cost (ERC, Thanatia) for Pt and Ir, report Δη_be with CExC replaced by CExC + ERC, in a separate table headed "not a GMS-100 term". This shows what a scarcity-pricing term would change. If you cannot read a value, say so; do not use a value from memory.
13. **Classes, fixed before any number is computed.** For each row of the central set (convention 5 central case, every loading, every source row, λ_ℰ = 0 and with the estimate, r_el = 1): "nearly free" if Δη_be < 10 mV; "priced" if Δη_be > 30 mV; "between" otherwise. 30 mV is the lowest Tafel slope per decade of exchange current named in G2.6; 10 mV is a third of it. Report the classes; do not change the thresholds.

## Part A: Σ_init of the loading (OQ-22)

Compute every term of convention 3 for every loading, source row and duty point; the table of Δη_be over the duty grid; the classes of convention 13; and, for the central case, the factor by which each lever (CExC, loading, j·τ, λ_ℰ, R_rec) would have to change for Δη_be to reach 30 mV. Reproduce G2.6's 0.84 to 1.5 mV for Pt at 0.5 mg/cm², 0.5 A/cm², 8e4 h from its inputs as a check of your arithmetic, and then say what GMS-100's terms change relative to it (the − b_ch, the EOL term, λ_ℰ, side g).

## Part B: CExC and B_infra decomposition (Prompt 8 D4)

For one element, Pt (or Ir if its data are better; say why you chose it):

1. For the CExC (or CED) source used in Part A: does it include capital goods (infrastructure processes)? If yes, what share of the total, and can it be removed? Which monitoring, assaying and maintaining flows does it contain? Split its supply-chain exergy (or energy) into capital (fixed, and proportional to throughput), operating, and maintenance parts as far as the source or its documentation allows, and by stage (mining, concentration, smelting, refining) where it gives that. Say which parts you could not split.
2. Estimate B_infra(x) for the same element, split into sunk (establishing the existing loop), avoidable-fixed (monitoring, assaying, maintaining over τ_infra, and re-establishing within τ_infra) and variable (proportional to throughput) parts. Use stated assumptions and sources (for example sustaining capital, mine life, refinery energy). Give b_infra for convention 10 and the avoidable fraction α of the fixed part. Everything here is an order-of-magnitude estimate: give a bracket, mark every input from memory UNSURE, and say if a part cannot be estimated at all.
3. From 1 and 2, say which configuration the spec is in for this source: A (source without capital goods; loop flows outside CExC), B (capital goods inside CExC), C (loop operating flows inside CExC), or a mix, with the evidence. Say which conditions of REQ-LIFECYCLE-CEXC-SOURCE (items 4 and 6) the source fails as published, and what an evaluation would have to remove.

## Method rules

- Mark every input as LOOKUP (with source, table, row or column, and access date) or MEMORY (UNSURE). Check MEMORY inputs first.
- A check that compares an expression with itself, or that is true by construction, must be flagged as such, not reported as a pass.
- Sweeps must bracket the 10 mV and 30 mV thresholds where the inputs allow; say where they cannot.
- Downloads: put each in its own new directory under `oq_22_code/data/raw/` (not committed), keep your scripts outside it, and run any Python that reads downloaded files with `-I`. Record every source in `oq_22_code/data/SOURCES.md` (URL, access date, licence if stated, what you took). Only small CSVs you derive from sources go in `oq_22_code/data/`.
- The session's network may block some hosts (earlier runs: arxiv.org, exergoecology.com, api.crossref.org). If a source is unreachable, say so and use search snippets only as UNSURE.

## Files you write (only these)

All under `local_docs/fable_runs/`:

- `oq_22_code/*.py`: standalone scripts (one per part, or per group of rows). Docstring: purpose, part and convention numbers, inputs and their status (LOOKUP or MEMORY), assumptions, how to run. Each runs with `<gms-local>/.venv/bin/python <path>` from any directory and needs no files outside `oq_22_code/` except the Prompt 5 data files named above (copy them in if simpler).
- `oq_22_code/data/*.csv`, `oq_22_code/data/SOURCES.md`.
- `oq_22_code/outputs/<script>.txt`: saved stdout of each script.
- `oq_22_code/outputs/issues.md`: ambiguities in this brief or the spec, failed or identity checks, unreachable sources. Empty file if none.
- `oq_22_answer.md`. Format:
  - Summary (at most 8 lines): the central-case Δη_be range for Ir and for Pt, its class, and what drives it.
  - Part A: inputs table (value, unit, LOOKUP or MEMORY, source); term table per loading (each Σ term in J/K per m²); Δη_be table over the duty grid; classes; lever factors; the G2.6 reproduction and what GMS-100's terms change; the r_el and ERC diagnostics.
  - Part B: source conditions table (six conditions × each source); the decomposition; the B_infra estimate with α and b_infra; the configuration (A, B, C or mix) and its evidence.
  - "Identity checks": checks true by construction.
  - "Not settled": what you could not compute or source, and the single input whose change would most move the classes.
  Every number points to the script and output line that produces it.

## Common rules

Read only the files named here. Do not edit files you were not told to write. Do not commit. Do not install anything. Every number you state must be reproducible from a saved script. If you search the web, search only titles, authors and technical terms; never include any project or personal detail. Mark anything you could not verify as UNSURE. Everything you produce is a claim at level `derived` (unverified).

Final message: list of scripts, the central-case Δη_be per loading and its class, the configuration found in Part B, and the issues.
