# Source check against local copies (Prompt 2 citations, with a note on Prompt 1b)

Date: 2026-11-13. Context file (`local_docs/`, never cited by the spec). **Everything here is a claim at level `derived`.** "Seen" means the passage or value was read in the source copy named, at the page given; it is checked against a page image where the note says so. It does not raise any level.

Builds on `prompt_2_citations.md` (S3), `prompt_2_citations_recheck.md` (A) and `prompt_2_citations_reconcile.md`. Rows those files settled (K7, K22, K33, K36-K38, K67) are not repeated.

## Sources used

All in `<gms_data_source>/` (outside the repo; supplied by the user). No full table is copied here; only the values used, with page references.

| File | What it is | Licence or terms seen |
|---|---|---|
| `doi.org_10.1002.pdf` | Szargut, J. (1987), "Analysis of cumulative exergy consumption", Int. J. Energy Res. 11(4), 541-547. DOI 10.1002/er.4440110410 (Crossref). Scan with an Acrobat OCR layer. | Wiley, copyright 1987. Not open. |
| `Szargut2005.pdf` | Szargut, Valero, Stanek, Valero, "Towards an International Reference Environment of Chemical Exergy". Footer: "Preprint submitted to Elsevier Science, 25 October 2005". 22 pages, TeX. | None stated. Linked from exergoecology.com as the "complete methodology". |
| `Reference Environment — The Exergoecology Portal.txt` (and `.html`) | Saved page with "Table 1: Chemical exergy of the Elements. Source: Szargut et al. 2005", 85 rows, kJ/mol. | Footer "Copyright 2018, iCIRCE. All Rights Reserved." |
| `es0711415-file002.pdf` | Supporting information of Dewulf et al. (2007), CEENE (K13), 34 pages. | ACS supporting information; no licence statement in the file. Not open. |
| `LCIA Implementation v3.12.pdf` | Sonderegger, T., "Implementation of Life Cycle Impact Assessment Methods in the ecoinvent Database v3.12" (2025.11.05), 71 pages. | No licence text found in the extracted text. |
| `lcia/` | Clone of `ecoinvent/lcia` (GitHub): mapped characterisation-factor CSVs for v3.9.1, 3.10, 3.11, 3.12. | README: CC BY-NC 4.0. `metadata.json` in all four versions: CC BY-NC 3.0. The two disagree. |
| `doi.org_10.1205_psep.04290.pdf` | Zhu, Feng, Shen (2005), PSEP 83(B3), 257-261. | Elsevier/IChemE. Not open. |
| `v119n12p1071.pdf` (and the image folder `Energy distribution in HC FeMn and SiMn energy vs exergy analyses_files/` of its SciELO page) | Larssen, T.A., Tangstad, M., Kero, I.T. (2019), "Energy distribution in HC FeMn and SiMn production: energy vs exergy analyses", J. S. Afr. Inst. Min. Metall. 119(12), 1071-1076. DOI as printed: 10.17159/2411-9717/788/2020. 6 pages. | No licence statement found in the extracted text. |

Tools: `pdftotext -layout`; pdfplumber word positions for tables; RapidOCR for the 1987 scan; page images rendered and read for every value or sentence marked "image-checked". Crossref (`api.crossref.org/works/...`) for records; only DOIs and title words were sent.

## 1. Table

| id | previous status (latest file) | status now | what was read | note |
|---|---|---|---|---|
| K3 | S3: verified, DOI 10.1002/er.4440110410 | **verified, DOI corrected** | Crossref records for both DOIs; local PDF of the issue 4 paper | Szargut, Morris (1987), "Cumulative exergy consumption and cumulative degree of perfection of chemical processes", IJER 11(2), 245-261 is **DOI 10.1002/er.4440110207**. The DOI in the S3 row (10.1002/er.4440110410) belongs to Szargut (1987), "Analysis of cumulative exergy consumption", IJER 11(4), 541-547, which is the local PDF. The answer's K3 line carries no DOI, so only `prompt_2_citations.md` is wrong. The 541-547 paper cites K3 as "Szargut J. and Morris D. R. (1986)" (in press at the time). |
| new (K3b) | not in the list | candidate, read | full paper (7 pages), OCR plus page images for the quoted sentences | Szargut (1987), IJER 11(4), 541-547, DOI 10.1002/er.4440110410. A primary Szargut text on CExC. Bears on the decisive check (a) and (c), see section 2. |
| K4 | S3: verified (record) | unchanged | exergoecology page bibliography link; Szargut et al. 2005 preprint Tables 2-5 | The page links "Szargut 1989" to PII 0306261989900160, which matches K4. The preprint lists a "Szargut 1989" column beside its own values (secondary to K4; K4 itself not read). |
| K5 | S3: verified (record) | unchanged | exergoecology page bibliography link | The page labels it "Morris and Szargut 1987" but links PII 0360544286900137 (= 0360-5442(86)90013-7), the Energy 1986 paper. K5's 1986 is right; the page's year is wrong. |
| K6 | S3: verified (record) | unchanged; cited use supported by a secondary source | Szargut et al. 2005 preprint, p. 13 text and Tables 3 and 4 (pp. 19, 20), image-checked | The preprint compares "This proposal", "Szargut 1989", "Valero et al. 2002" and "Rivero and Garfias 2004" side by side. It states (p. 13) that Rivero and Garfias found an influence of seawater salinity, with deviations "usually less than 1,6%". The column is "Rivero and Garfias 2004" (likely the ECOS 2004 paper in its reference list), not the cited 2006 Energy paper. Values seen, see section 3. |
| K12 | S3: verified (record); open data UNSURE; reconcile: CExD licence UNSURE | **verified (implementation seen); open-data question settled** | ecoinvent v3.12 implementation report, section 11 (pp. 41-42), Table 7 (p. 20); `lcia/` directory listing for all four versions | CExD is implemented in ecoinvent v3.12 ("Method Versions 2021"), based on Bösch et al. (2007), DOI 10.1065/lca2006.11.282. Table 16 categories: energy resources (non-renewable biomass, fossil, nuclear; renewable biomass, solar, water, wind), **material resources: metals, minerals, water**, total. Oil and gas CFs were updated with energy-to-exergy ratios of 0.94 (natural gas, 40 MJ/Sm3 HHV -> 37.6 MJ) and 1.015 (crude oil, 46 MJ/kg -> 46.7 MJ). **CExD is not in the `ecoinvent/lcia` repository**: no file in 3.9.1, 3.10, 3.11 or 3.12 contains it (nor CED). So B's "CC BY-NC 4.0 on GitHub" covers the repository, not CExD. No open copy of the CExD factors found; they are distributed inside ecoinvent. Infrastructure treatment (the C16 use) is not stated in section 11. |
| K13 | S3: verified (record); recheck: seven authors, Dewulf first; SI not fetched, licence UNSURE | **verified (SI read); licence: not open** | SI contents (p. 1), S1 (from p. 2), S4 (p. 10), S6 (p. 17) | S1 groups the X factors (MJex per unit of resource) into eight headings: renewable resources, fossil fuels, nuclear energy, metal ores, minerals (and mineral aggregates), water resources, land occupation (and transformation), atmospheric resources. S4: metal-ore factors are per kg of metal in the ground, built from the chemical exergy of representative minerals with allocated mole fractions. Recomputed (derived): Cu from chalcopyrite, chalcocite and bornite (0.5 x 1536 + 0.125 x 655.1 + 0.05 x 3085 kJ/mol over 63.54 g/mol) = 15.8 MJex/kg, as listed; Al from boehmite, gibbsite and diaspore = 0.47 MJex/kg, as listed. Author order on the SI title page (Dewulf, De Meester, Van der Vorst, Van Langenhove, Bösch, Hellweg, Huijbregts) differs from Crossref's (Dewulf, Bösch, De Meester, ...). The plan's K13 line follows Crossref; keep it. |
| exergoecology table | recheck and reconcile: HTML only, all rights reserved | unchanged; values cross-checked | `.txt` copy of the page; preprint Tables 2-5 | See section 3. Licence unchanged: all rights reserved. |
| new | not in the list | candidate | Larssen, Tangstad, Kero (2019): abstract, introduction, exergy-method paragraph (PDF text only) | Staged energy and exergy balances of submerged-arc furnaces for HC FeMn and SiMn. Abstract: exergy destruction 13.7 % (HC FeMn) and 10.8 % (SiMn); energy and exergy analyses point to the same recovery sites. Standard chemical exergies taken from Szargut et al. (2005) via exergoecology.com, with T0 = 25 °C, p0 = 1 atm. So it is an applied user of the section 3 table. Not tied to any K row; a worked metallurgical example next to K1 and K28. **The printed DOI (10.17159/2411-9717/788/2020) is not registered**: doi.org handle API returns "handle not found" (responseCode 100), Crossref returns 404, and a Crossref title search does not find the paper. Cite it by journal, volume, issue and pages as printed. |
| new | not in the list | candidate | Zhu, Feng, Shen (2005) abstract and introduction | Proposes cumulative exergy consumption for treatment of emissions (CExCT) and an equivalent CExC (ECExC) against an acceptable emission level. Not tied to any K row; a lead for waste-exergy treatment next to K18. Not read beyond p. 1. |

## 2. Decisive check (Szargut CExC): what the primary 1987 text says

Source: Szargut (1987), IJER 11(4), 541-547 (K3b). Quotations image-checked.

- **(a) Ore's own exergy: supported at definition level (primary).** p. 541: "The CExC-index expresses the sum of exergy values of natural resources delivered to the system in all the links of the chain of production processes, per unit of the product under consideration (Szargut and Morris, 1986). ... CExC of the products of every process equals the sum of CExC of the delivered semi-finished products plus the exergy of natural resources taken immediately from the environment." So resource exergy, ore included, enters CExC by definition. This replaces A's single secondary source (Sciubba 2021) for (a). It does not show what any particular tabulated CExC value contains.
- **(b) By-product rule: not addressed.** The paper says only that "the allocation of the intermediate product between the subsequent processes can be presented in the individual single circles" (p. 543), with no rule. Status unchanged (A: substitution at least for cogeneration, from the K7 abstract).
- **(c) Capital goods: optional, usually omitted in the sequence method (primary).** p. 542: "Usually th[e] production of machines and installations for the transformation of materials is omitted in the sequence scheme." p. 543: "If the exergy requirement for the production of machines and installations is not omitted, the name of machines and installation can be given inside a rombus ...". Scope: this concerns the sequence (process-analysis) method. The paper does not say whether the balanced-equation method behind CExC tables includes them. B's lead ("usually omitted") now has primary support for the sequence method only.
- Also on p. 542: the transformation of fuels for transport and the winning of raw materials "are not analysed in detail, and hence the CExC connected with these processes can be only globally estimated."
- CEENE side (K13, S4): metal ores are charged with the chemical exergy of their minerals, so CEENE also includes the ore's own exergy.

## 3. Element exergy table: website against the 2005 preprint

- Website table (`.txt`): 85 rows. Preprint Tables 2-5 (pp. 18-21) parsed with pdfplumber; doubtful values read off page images.
- **80 of 85 values are identical.** Five differ by 0.01 kJ/mol (preprint value image-checked on p. 19): Cd 293.38 (web) vs 293.37 (preprint); Cl2 124.02 vs 124.03; Hg 115.00 vs 114.99; Ni 232.71 vs 232.70; Pb 232.41 vs 232.40. Recorded as a disagreement between two renderings of one source; not resolved.
- Label errors in the preprint (printed, image-checked): Table 3 (p. 19) labels the Rb+ row "Ru" (value 388.89 = website Rb; website Ru is 318.45). Table 4 (p. 20) labels fluorine "Fl" (481.54 = website F2).
- The preprint is a submitted manuscript dated 25 October 2005, not the published ECOS 2005 paper listed as a candidate in the reconcile file. Whether the published values differ is unknown.
- Reference dependence (for K6 and plan D7 (ii)), seen in the preprint (columns: this proposal, Szargut 1989, Rivero and Garfias 2004). Al, F, S and Cu image-checked; Fe, Pt and Ir from pdfplumber text only: Al 796.10 (this proposal, reference species Al2SiO5) vs 888.20 (Szargut 1989) vs 795.7 (Rivero and Garfias 2004), a change of 10.4 % against Szargut 1989 (derived). F 481.54 vs 504.90 vs 505.8. S 607.05 vs 609.6 vs 609.3 (p. 13 attributes the S change to a sulphate molality 2.5 times higher). Cu 134.25 vs 134.2; Fe 376.99 vs 374.8 vs 374.3; Pt 140.97 vs 141 vs 141.2; Ir 256.56 vs 246.80 vs 247.

## 4. Effect on round 2 (proposals for the user)

No finding changes. Citation lines and two supports only.

| Item | Proposal |
|---|---|
| K3 | **Applied 2026-11-13 (user approved):** DOI in `prompt_2_citations.md` row K3 corrected to 10.1002/er.4440110207. The answer's K3 line needs no change. |
| K3b | Optional: add Szargut (1987), IJER 11(4), 541-547, DOI 10.1002/er.4440110410, as the primary source for decisive check (a) and for (c) in the sequence method. |
| Synthesis D7 (i), (iv) | No change in wording. (i) "includes the ore's exergy" now has primary support at definition level. (iv) "declare capital-goods inclusion" is supported: Szargut's own sequence method treats it as optional and usually omits it. |
| Synthesis D7 (ii) | No change. Section 3 gives a concrete size for the reference-environment effect (Al about 10 % between Szargut 1989 and the 2005 proposal). |
| L9 | Unchanged. Whether a given `CExC` table includes capital goods still depends on the source used; K12 (ecoinvent CExD) inherits ecoinvent's infrastructure, which section 11 does not state. |
| Open data (OQ-6) | CExD: not openly available (absent from `ecoinvent/lcia`). CEENE: published only as ACS supporting information, no open licence. Element table: website all rights reserved; the 2005 preprint carries no licence. `ecoinvent/lcia` licence text is inconsistent (4.0 in README, 3.0 in `metadata.json`). |

## 5. Prompt 1b

Nothing in this folder checks a Prompt 1b row. The `lcia/` CSVs hold characterisation factors per elementary flow, not inventories, so they cannot give per-kg cumulative energy demand of Cu, Al, Pt or Ir (R79). CED is implemented in ecoinvent v3.12 (report section 10) but is not in the repository either.

## 6. Not done

- K1, K2 (books), K4 and K5 (journal papers): not in the folder; still record-level.
- Larssen et al. (2019): read at abstract and method level only; its tables and balances not checked.
- Exergoecology Eq. 1: an image on the page, not in the `.txt`; not read.
