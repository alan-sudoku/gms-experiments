# gms-experiments

This repository is the full record of 11 computational experiments. Each one tests claims made in GMS. GMS is a specification, still being drafted, for deciding when an architected geometry can replace a chemical element in an engineering component (for example an aluminium lattice in place of solid copper). It does this by comparing the lifecycle irreversibility (entropy generated, in J/K) of the two options. The GMS specification is in a separate repository that is not public yet. This repository stands on its own.

For each experiment you will find the question, the plan, the scripts, their saved outputs, a check of the cited sources, the answer, an independent review and the decision taken.

**Every result here is at validation level `derived`.** That means it was shown by reasoning or computation only, not by measurement. Agreement between stages or reviewers does not raise the level. Simulation results count as `derived` too.

## Status and contents

The repository is being reorganised into one folder per experiment (`exp_001_...` to `exp_011_...`). Until that is done, the runs live under `local_docs/fable_runs/` with their original file names. (`fable_runs` is a historic name, after the AI model used for the design and analysis stages of the first runs.) The original question texts are in `local_docs/fable_questions.md`.

| # | Planned folder | Question | Current prefix | Read first |
|---|---|---|---|---|
| 1 | `exp_001_ac_conduction` | Does an aluminium micro-lattice with struts thinner than the skin depth carry alternating current with less loss than solid copper? | `prompt_1a_*` | `prompt_1a_synthesis.md` |
| 2 | `exp_002_heat_sink_catalysis` | Can geometry let aluminium replace copper in an air-cooled heat sink, and nickel–iron replace platinum-group metals as a water-electrolysis catalyst? | `prompt_1b_*` | `prompt_1b_synthesis.md` |
| 3 | `exp_003_exergy_accounting` | Is the GMS lifecycle exergy accounting (end-of-life charges, allocation, reference environment, recovery test) internally consistent? | `prompt_2_*` | `prompt_2_synthesis.md` |
| 4 | `exp_004_lattice_fatigue` | How should fatigue loss, thermal-expansion mismatch and fatigue life be modelled for a strut lattice, and does fatigue matter in the entropy balance? | `prompt_3_*` | `prompt_3_synthesis.md` |
| 5 | `exp_005_solver_lemmas` | Do five lemmas that the planned GMS verdict solver relies on hold, or is there a counterexample? | `prompt_4_*` | `prompt_4_synthesis.md` |
| 6 | `exp_006_class_gate` | Can engineering functions be split into those that need a specific element and those that geometry can serve with a substitute (tested on conduction, heat transfer, catalysis, photon and neutron shielding, energy storage and magnets)? | `prompt_5_*` | `prompt_5_synthesis.md` |
| 7 | `exp_007_degradation_combination` | How should several degradation mechanisms (oxidation, corrosion, fatigue) be combined into one loss rate and one wear-out life? | `prompt_6_*` | `prompt_6_synthesis.md` |
| 8 | `exp_008_entropy_currency` | When two designs lose energy at sites with different ambient temperatures, should the losses be compared as lost work or as entropy? | `prompt_7_*` | `prompt_7_synthesis.md` |
| 9 | `exp_009_infrastructure_share` | How should the credit for avoided recycling infrastructure be shared when several products use the same recovery loop? | `prompt_8_*` | `prompt_8_synthesis.md` |
| 10 | `exp_010_incumbent_wearout` | How should the comparison treat an incumbent part that wears out and is replaced during the service life? | `prompt_9_*` | `prompt_9_synthesis.md` |
| 11 | `exp_011_material_scarcity` | Does the GMS charge for making a component register the scarcity of a catalyst metal such as iridium or platinum? | `oq_22_*` | `oq_22_synthesis.md` |

Short answers (all `derived`; the synthesis files give the numbers and conditions):

1. Not supported. A lattice whose struts are joined at nodes behaves like a conductor of lower conductivity, so it loses to solid copper. Insulated, transposed strands help either metal equally.
2. Heat sink: valid with a narrower scope. Aluminium plate fins need 1.4–2.1 times the fan air power to match copper; the lattice part is unsupported, not disproved. Catalysis: invalid as stated.
3. Repairable. The end-of-life terms must charge the dispersed material, and the energy-recovery test cannot declare a design infeasible.
4. Fatigue loss is not negligible in general. Life must be computed from the local strut stress, not the average stress.
5. No counterexample found. Conditions were added to two lemmas and the wording of one was corrected.
6. Valid with a narrower scope. The two-class split does not hold; a per-case threshold and compensation test does.
7. Adding loss rates is acceptable with stated limits. Taking the shortest life over separate load cases is not.
8. Compare as lost work.
9. The current rule loses the whole joint gain in its own example. A three-way rule (pass, fail, or conditional on the other products) is sound, once one gap in the current rules is closed.
10. Evaluating with the incumbent never replaced gives an upper bound: if the candidate wins then, it wins whatever the incumbent's life. The current "no outcome" rule is too strict.
11. Nearly free in the central case (below 10 mV of break-even overpotential). For iridium at high loading it can exceed that with current metal prices, intermittent duty, a depletion term or the shared-loop rule.

The files use labels from the private GMS repository, such as document numbers (`GMS-100`), open questions (`OQ-13`) and decision numbers (`E15`). Each synthesis restates what it needs, so you can follow it without the spec. Stages are labelled S1 to S6: S1 design, S2 execute, S3 source check, S4 analyse, S5 review, S6 decision. Their rules are in `local_docs/orchestration/fable_delegation_plan.md`.

## File conventions (current layout)

All paths below are under `local_docs/fable_runs/`. `<p>` stands for a prefix such as `prompt_3`.

| File | Contents |
|---|---|
| `<p>_plan.md` | Design: claims, derivations, the checks to compute and the sources to verify |
| `<p>_code/` | Scripts. `outputs/<script>.txt` holds each script's saved stdout. `outputs/issues.md` lists problems the scripts raised |
| `<p>_citations.md` | Check that each cited source exists and says what it is cited for |
| `<p>_answer.md` | The answer and verdict |
| `<p>_review.md`, `<p>_review_code/` | Independent review and the reviewer's own scripts (same `outputs/` rule) |
| `<p>_synthesis.md` | Summary of answer and review, and the decisions taken |

Exceptions:

- **Experiment 1** was a single pass: no plan or citations file. `prompt_1a_external/` and `prompt_1a_simulation_runbook.md` hold a test run with external field solvers (see below).
- **Experiments 5 and 11** have a `<p>_brief.md` instead of a plan; one agent did design, scripts and answer. Experiment 5 also has a cross-check with an independent SciPy evaluator (`prompt_4_xcheck*`).
- **Experiments 8, 9 and 10** were answered without tools (no code, no web search): `<p>_web_answer.md`, then a review with scripts. Experiment 4 also has two such answers (`prompt_3_q1_web_answer.md`, `prompt_3_q2_web_answer.md`).
- **Experiment 3** has extra source checks: `prompt_2_citation_gemini_check.md`, `prompt_2_citations_recheck*.md`, `prompt_2_citations_reconcile.md` and `source_check_2026_11_13.md`.
- **Experiments 6 and 7** have `<p>_citations_code/` folders with the source-check scripts. They have no `outputs/` folder; Experiment 6's results sit under `prompt_5_citations_code/data/`.
- `oq_22_review_code/rv01_independent_check.txt` is saved next to its script, not in `outputs/`.
- `prompt_1a_external/L1_fasthenry_lattice/outputs/l1_pilot_partial.txt` is the output of `l1_partial_record.py`; `l1_lattice.py` has no saved output.
- `prompt_2_review_code/outputs/rerun/` holds the reviewer's re-runs of `prompt_2_code`, not reference outputs.
- Helper modules (`gms_core.py`, `common.py`, `xc_common.py`, `p6_common.py`, `rainflow_util.py`, `oq22_common.py`, `common/simtools.py`) print nothing and have no saved output.

## Reproduce

You need Python 3.12 (the outputs were made with 3.12.3). From the repository root:

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Run each script from its own folder and compare its stdout with the saved output:

```sh
cd local_docs/fable_runs/prompt_3_code
PYTHONHASHSEED=0 ../../../.venv/bin/python p3_q4_limits.py | diff - outputs/p3_q4_limits.txt
```

No output from `diff` means an exact match. To check a whole folder, run this from the repository root (set `dir` to any `*_code` folder):

```sh
PY="$(pwd)/.venv/bin/python"; dir=prompt_3_code
cd "local_docs/fable_runs/$dir"
for s in *.py; do
  out="outputs/${s%.py}.txt"
  [ -f "$out" ] || { echo "skip  $s (no saved output)"; continue; }
  if PYTHONHASHSEED=0 "$PY" "$s" 2>/dev/null | diff -q - "$out" >/dev/null
  then echo "same  $s"; else echo "DIFF  $s"; fi
done
```

The loop skips scripts with no saved output, which includes the helpers, the data builders and the two scripts that download from the web. Most scripts finish in under a second. The longest take a few minutes: `prompt_1a_code/a2_strand_bundle_scan.py` about 4 min, `prompt_4_xcheck_code/x3_box_worst_case.py` about 2.5 min. Running Experiment 5's property tests creates `prompt_4_code/.hypothesis/`, which ignores itself in git.

## Reproduction status

Audited on 2026-11-15 at commit `4d159f7`, from a fresh clone with the pinned `requirements.txt`, each script run from its own folder.

**164 of 194 scripts reproduce their saved output exactly.** Of the other 30, none that ran shows a changed result. The 13 that could not run (missing data or solver, needs an argument, downloads) are listed below with the reason.

| # | Prefix | Scripts | Exact | Numbers differ | Missing data or solver | Needs an argument | Downloads | No saved output |
|---|---|---|---|---|---|---|---|---|
| 1 | `prompt_1a` | 17 | 9 | 4 | 3 | 0 | 0 | 1 |
| 2 | `prompt_1b` | 25 | 24 | 0 | 0 | 0 | 0 | 1 |
| 3 | `prompt_2` | 10 | 10 | 0 | 0 | 0 | 0 | 0 |
| 4 | `prompt_3` | 10 | 10 | 0 | 0 | 0 | 0 | 0 |
| 5 | `prompt_4` | 15 | 13 | 0 | 0 | 0 | 0 | 2 |
| 6 | `prompt_5` | 53 | 39 | 2 | 3 | 4 | 2 | 3 |
| 7 | `prompt_6` | 42 | 38 | 0 | 1 | 0 | 0 | 3 |
| 8 | `prompt_7` | 5 | 5 | 0 | 0 | 0 | 0 | 0 |
| 9 | `prompt_8` | 6 | 6 | 0 | 0 | 0 | 0 | 0 |
| 10 | `prompt_9` | 7 | 7 | 0 | 0 | 0 | 0 | 0 |
| 11 | `oq_22` | 4 | 3 | 0 | 0 | 0 | 0 | 1 |
| | **Total** | **194** | **164** | **6** | **7** | **4** | **2** | **11** |

**Numbers differ (6).**

- Timing only: `prompt_1a_code/a2_transposed_bundle.py`, `prompt_1a_code/a3_busbar_rac.py`, `prompt_1a_review_code/r1_vie_independent.py` and `prompt_5_code/f6_buildup_mc.py` print wall-clock times. Only those figures differ.
- `prompt_1a_code/a2_hf_limit_bem.py`: two numbers differ by 1.8e-15 (relative), which is floating-point rounding.
- `prompt_5_review_code/r1_answer_numbers.py` scans the answer file for numbers. It now reports 584 numbers checked instead of 578, because `prompt_5_answer.md` was edited after the output was saved. No result changed.

**Needs a command-line argument (4).** These failed in the audit only because they were run without one. Run them like this, from the repository root:

```sh
cd local_docs/fable_runs/prompt_5_citations_code
../../../.venv/bin/python parse_nist.py data/nist           # NIST X-ray attenuation tables: mu/rho and the W/C ratio
../../../.venv/bin/python sears.py data/nist/sears.html     # rows of the Sears (1992) neutron cross-section table
../../../.venv/bin/python xcom_fit.py data/xcom             # XCOM photoelectric Z and energy exponents, Klein-Nishina check
cd ../prompt_5_review_code
../../../.venv/bin/python r0_rerun_all.py "$(mktemp -d)/p5_rerun"
```

The first three have no saved output; their figures appear in `prompt_5_citations.md` and `prompt_5_answer.md` (for example the W/C ratio of 29.3 at 100 keV). `r0_rerun_all.py` copies `prompt_5_code/` into the folder you name and re-runs every script there. It **deletes that folder first** if it exists, so give it a new path. It takes about 3–4 minutes. Its result matches `outputs/r0_rerun_all.txt` except for the timing column and the three items whose input files are missing (below): the builders `f0_build_xcom_csv` and `n0_build_crust_csv`, and `a1_conductor_area_mass`.

**Downloads from the web (2).** Not run in the audit.

- `prompt_5_code/n1_fetch_endf_sigma.py` downloads ENDF/B-VII.1 pointwise neutron cross sections for 53 nuclides from NNDC Sigma (https://www.nndc.bnl.gov/sigma/). The files from the original run (accessed 2026-11-14) are tracked in `prompt_5_code/data/raw/endf_sigma/`. Running the script overwrites them; use `git diff` to see whether the server's data changed.
- `prompt_5_citations_code/xref.py` queries the Crossref API for the bibliographic records of 28 cited works. The recorded result is `prompt_5_citations_code/data/crossref/out.txt`.

**Missing data or external solver (7).**

- `prompt_5_code/a1_conductor_area_mass.py` reads `data/a1_iec60228_class2.csv`, values from the standard IEC 60228:2004, Table 2. The standard is copyrighted, so the file was removed. The values used are printed in `outputs/a1_conductor_area_mass.txt` and will be written into the script.
- `prompt_5_code/f0_build_xcom_csv.py` needs `data/raw/tab1.html` (NIST X-ray mass attenuation coefficients, Table 1, https://physics.nist.gov/PhysRefData/XrayMassCoef/tab1.html). It is redistributable and will be added. The copy used had sha256 `dc83772b8e7c7f8bc2c1781314db264f896f90bf7d5a2a02808143d11855b91b`.
- `prompt_5_code/n0_build_crust_csv.py` needs `data/raw/wiki_abund.txt`, the wikitext of the Wikipedia page "Abundances of the elements (data page)". It will be added under its own CC BY-SA licence. The copy used had sha256 `4e4af9d1f40aff9162e4772ef332f9b95f6de0d9fb22cc77f94c635e3e3ad7a2`.
- `prompt_1a_external/L1_fasthenry_lattice/l1_lattice.py`, `l1_partial_record.py` and `s2_sanity/s2_sanity.py` drive external field solvers: FastHenry2, GetDP and gmsh. GetDP and FastHenry2 are not pip-installable (a prebuilt binary and a build from source); gmsh has a PyPI wheel (4.15.2 was used) but is not pinned here. The scripts expect the binaries in `~/opt/sim/bin/` and write work files to `~/opt/sim/work/`. `prompt_1a_external/README.md` lists the versions and build steps. The outputs are recorded in the `outputs/` folders next to the scripts.
- `prompt_6_citations_code/ocr_pdf.py` needs PyMuPDF and RapidOCR (`rapidocr_onnxruntime`), which are not pinned. It turns a scanned PDF into text (`python ocr_pdf.py in.pdf out.txt`); its input PDFs are excluded for copyright.

The analysis scripts read the tracked derived CSV files, not the raw files. The missing raw files therefore block only the data-builder scripts, and every analysis script downstream of them still runs.

**No saved output (11).** Seven are the helper modules listed above; they print nothing. `prompt_5_code/n0_build_atomic_weights_csv.py` and `n0_build_sears_csv.py` rebuild tracked CSV files; after running them, `git status` shows no change. `prompt_5_citations_code/derived_checks.py` (small arithmetic checks) and `prompt_6_citations_code/l05_convert.py` (unit conversion of published oxidation constants) print a few lines with no saved copy to compare against.

## Data and licences

**Included.** Data files whose licence allows redistribution are in the repository, each with its source URL and access date in the file header or the generating script:

- NIST XCOM photon cross sections and NIST X-ray mass attenuation tables (NISTIR 5632), as downloaded HTML pages in `prompt_5_code/data/raw/` and `prompt_5_citations_code/data/`.
- NIST atomic weights, and the Sears (1992) neutron cross-section table as reproduced by NIST NCNR.
- NNDC Sigma ENDF/B-VII.1 cross sections (164 files in `prompt_5_code/data/raw/endf_sigma/`).
- Derived CSV tables (for example `prompt_5_code/data/*.csv`, `oq_22_code/data/*.csv`), each with a header that states where its values come from (for example the USGS Mineral Commodity Summaries 2026).

In the new layout these move to `data/public/` in each experiment, and each experiment gets a `data/SOURCES.md` with URL, retrieval date, sha256 and licence. Two exist already: `oq_22_code/data/SOURCES.md` and `prompt_6_code/data/SOURCES.md`.

**Not included.** Files whose licence does not allow redistribution, or whose licence is unknown: paywalled papers, textbook scans, standards (such as IEC 60228), commercial life-cycle data and non-commercial (CC BY-NC) data. For these the repository keeps only the values used, quoted with a table or page reference, in the derived CSV headers and the source-check files.

**Getting them.** Per-experiment fetch scripts are being added. They will download each excluded file that has a stable public URL and check its sha256. For a source with no public URL, use your own copy of the cited reference. The `SOURCES.md` files will record the sha256 of each copy used, so you can confirm that yours is identical.

**Licence** (see `LICENSE`): scripts and code are under the MIT licence. Text, documentation and derived data are under CC BY 4.0. Third-party data keeps its own licence, as recorded in each experiment's `data/SOURCES.md`; nothing here relicenses it.

## How these experiments were run

Each experiment went through fixed stages: question, design, execute, verify sources, analyse, independent review and decision. AI agents (language models) did the stages from design to review, each with its own limits; for example, the agent that runs the scripts may not change the physics, and the reviewer may not edit the other agents' files. A human chose or approved every question and took every decision. Review is the stage that changed conclusions: every review recorded major findings (none blocking), and in experiments 6 to 11 the review changed the conclusion. The method is documented in [`METHOD.md`](METHOD.md).
