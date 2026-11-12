# Prompt 2 citation re-check: brief

Context file (`local_docs/`, never cited by the spec). Written 2026-11-12 by the orchestrator. The first citation check (`prompt_2_citations.md`) could not reach arxiv.org, exergoecology.com or api.crossref.org and read abstracts only. The user then allowed those hosts for the cloud environment (all three return 200, checked 2026-11-12). A `sonnet` agent was launched with the brief below. Its output is `prompt_2_citations_recheck.md`. If that file is missing or has items marked "not checked (run stopped early)", rerun the brief for those items only, and update the file in place.

## Brief (as given to the agent)

Read: `local_docs/fable_runs/prompt_2_citations.md`; `prompt_2_answer.md` sections "4. Citations" and "5. Changed since plan"; `prompt_2_review.md` sections "Citations" and "What still needs external checking". Read nothing else in the repo.

Check these items, using full text or primary records where openly reachable (Crossref JSON: `https://api.crossref.org/works/<DOI>`):

1. Not verified:
   - K8 (Kotas): where the chemical-exergy temperature correction is.
   - K29 (ISO 14044:2006): clauses 4.3.4.3, 4.2.3.3 and 4.2.3.7.
   - K39 (Nordic Guidelines, Nord 1995:20): whether it is the origin of the 50/50 rule.
   - K44 (Nordelöf et al. 2019): whether the body compares 50:50 or the circular footprint formula.
   - K46 (PAS 2050:2011): which annex covers recycled material.
   - K60 (Green 2003 §3.4): the 93.3 % and 95 % figures.
   - K68 (Rosen & Dincer 2004): the journal record.
   - K71 (Rosen 1954, Phys. Rev. 96, 555): Crossref gives the title "Entropy of Radiation". Does it contain a mode-entropy expression?
2. Uncertain records:
   - K7: the volume.
   - K22: the author order.
   - K33: the volume and pages.
   - K67 (arXiv 1710.02617): the page range; whether it states 153.1 W/m² at 300 K / 3 K as the ultimate limit; what the 48.4 W/m² and 225.1 K figures are.
   - K38: the exact 50:50 formula in Annex II §5.4.7 of 2013/179/EU.
   - K36: where the circular footprint formula sits in 2021/2279.
3. Decisive check (review): does Szargut's CExC (K1–K3, or open secondary descriptions) include the ore's own exergy? Which by-product allocation rule does it use? Does it include capital goods? State whether each answer comes from the primary text or from a secondary source.
4. Open data: is the Szargut et al. 2005 chemical-exergy table on exergoecology.com downloadable, and under what licence? Are the CExD (K12) and CEENE (K13) factors openly downloadable, and under what licence?
5. Is the ASTM E-490 or a SORCE extraterrestrial solar spectrum openly downloadable (URL, licence)? Do not compute anything.

Rules:
- Search only titles, authors and technical terms; never include any project or personal detail.
- Do not edit existing files and do not commit.
- No new sources as evidence; list candidates separately.
- No copyrighted PDFs in the repository.
- Mark anything not verified as UNSURE. Everything is level `derived`.

Output `prompt_2_citations_recheck.md`:
- a header with the date, the hosts used and the method;
- a table with one row per item: id | status | corrected record with DOI | what was read | note;
- sections "Decisive check (item 3)", "Open data (items 4–5)", "Effect on the answer" (per finding L1–L16 and convention V1–V9) and "Candidate sources (not evidence)".

The agent was told to write the file early and update it after every one or two items, so a cut-off run leaves a partial record.
