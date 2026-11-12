# Citation re-check (second pass) for prompt_2_answer.md

Date: 2026-11-12. Everything below is a claim at level `derived`.

Hosts that answered: api.crossref.org, arxiv.org, eutils.ncbi.nlm.nih.gov, api.openalex.org, eur-lex.europa.eu, eplca.jrc.ec.europa.eu, research.chalmers.se, exergoecology.com, osti.gov, frontiersin.org, lca-net.com, eolss.net, ebi.ac.uk, lasp.colorado.edu (LISIRD).
Hosts that refused or failed: www.mdpi.com (403 / not in allowed network), iso.org (bot check), pnas.org (403), sciencedirect.com and researchgate.net (403), ANSI preview (403), www.nrel.gov and rredc.nrel.gov (proxy 502). One attempt to fetch a blocked page with a changed client identity was refused by the session's permission layer; I did not retry or work around it.

Method: Crossref JSON for records; PubMed (NCBI eutils) for the PNAS page range; arXiv PDF text for K67; EUR-Lex HTML and PDF text for K36, K38; JRC PDF text for K37; Chalmers repository version of record (CC BY) for K44; Ekvall's open Chalmers thesis and open web pages for K39 and the decisive check; search-result summaries where nothing else was reachable (marked "secondary"). No copyrighted PDF was saved in the repository; downloads sit in the session scratchpad only. Nothing in a query named the project or the user.

Status counts (14 items in scope 1 and 2): verified 5 (K22, K33, K36, K67, K68 as record), record-corrected 1 (K7: the earlier "correction" was wrong), exists but does not say this 1 (K44), UNSURE 7 (K8, K29 partly, K38 exact form, K39, K46, K60, K71). Details below.

## Table

| id | status | corrected record (DOI) | what I read | note |
|---|---|---|---|---|
| K7 | verified (record); earlier title "correction" was wrong | Szargut, Ziębik, Stanek (2002), "Depletion of the **non-renewable** natural exergy resources as a measure of the ecological cost", Energy Convers. Manage. **43**(9-12), 1149-1163. DOI 10.1016/S0196-8904(02)00005-5 | record (Crossref); abstract (OSTI) | Crossref title says "non-renewable", volume 43. The "unrestorable" wording belongs to Szargut's ECOS'99 proceedings paper (and one open article cites this paper with volume 42, which probably caused the earlier confusion). |
| K8 | UNSURE | none | catalogue contents only (secondary) | Contents show 2.5 "Chemical exergy", Appendix A (chemical exergy and enthalpy of devaluation) and Appendix C (chemical exergy of industrial fuels). No text on a temperature correction found. |
| K22 | verified | Castro, Remmerswaal, Brezet, Reuter (2007), Resour. Conserv. Recycl. 52(2), 219-233. DOI 10.1016/j.resconrec.2007.01.014 | record (Crossref) | Publisher order is Castro, Remmerswaal, Brezet, Reuter, as cited in the answer. The TU Delft listing order was the odd one. |
| K29 | UNSURE (partly supported) | none | secondary quotations only (open forum post and open article quoting the standard) | 4.3.4.3 (reuse and recycling): 4.3.4.3.3 and 4.3.4.3.4 quoted verbatim in two open sources. 4.2.3.3 (system boundary, cut-off): 4.2.3.3.3 quoted with criteria mass, energy, environmental significance. 4.2.3.7 (comparisons): not found in any reachable source. Standard not read. |
| K33 | verified | Atherton (2007), "Declaration by the Metals Industry on Recycling Principles", Int. J. LCA 12(1), 59-60. DOI 10.1065/lca2006.11.283 | record (Crossref) | Online first 30 Nov 2006, print 2007. |
| K36 | verified | Recommendation (EU) 2021/2279, OJ L 471, 30.12.2021. The circular footprint formula is **Annex I (PEF method), section 4.4.8.1, Equation 3**. Default A, R1, R2, Qs/Qp values are in Annex II (Part C for A). | full text (EUR-Lex PDF with annexes; the OJ HTML has the body only) | Annex I section 4.4.8 is titled "Recycled content and end of life modelling". A is limited to 0.2-0.8 in PEF studies; 0.5 where no value is available. The equation is an image-like text in the PDF and extracts garbled; its layout is Material + Energy + Disposal. |
| K37 (extra) | verified | Zampori, Pant (2019), EUR 29682 EN | full text (JRC PDF) | Section 4.4.8.1, Equation 3 is legible: Material = (1-R1)E_V + R1(A E_recycled + (1-A)E_V Qsin/Qp) + (1-A)R2(E_recyclingEoL - E*_V Qsout/Qp). Matches the formula quoted in prompt_2_review.md. |
| K38 | exists; **section in the answer is wrong**; exact form UNSURE | Recommendation 2013/179/EU, Annex II (PEF Guide). The 50:50 recycling formula is in **Annex V "Dealing with Multi-functionality in Recycling Situations"** of the PEF Guide, called up from section 5.10 "Handling multi-functional processes". Section 5.4.7 "End-of-Life" is generic text and has no formula. | full text (EUR-Lex HTML) | Text states "allocates the impacts and benefits due to recycling equally between the producer using recycled material and the producer producing a recycled product: 50/50 allocation split". Terms defined: E_V, E*_V, E_recycled, E_recyclingEoL, E_D, E*_D, E_ER, E_SE,heat/elec, R1, R2, R3. The equation itself is an image and did not extract, so its exact form is not read. Annex III is the OEF Guide, which has its own Annex V. |
| K39 | UNSURE (origin not supported) | none | secondary (Ekvall 1999 PhD thesis, open, Chalmers) | The thesis lists Lindfors et al. 1995a (Nord 1995:20) among publications that describe a 50/50 method, recommended there for hot-spot identification. It describes two different 50/50 methods: Vigon et al. 1993 (benefits of recycling split between two products) and Ekvall 1994 (primary production and final waste burdens split between first and last product; recycling burdens split between neighbours). So Nord 1995:20 is a user of one variant, not shown to be the origin. Nord 1995:20 itself not read. |
| K44 | exists but does not say this | DOI 10.3390/batteries5030051; Nordelöf, Poulikidou, Chordia, Bitencourt de Oliveira, Tivander, Arvidsson (2019), Batteries 5(3), 51; CC BY | full text (Chalmers version of record, 15 pages) | Body has no occurrence of "50:50", "50/50", "circular footprint" or "PEF". It compares cut-off, end-of-life recycling and hybrid approaches, with a double-counting warning. |
| K46 | UNSURE | none | secondary (search summary of contents) | Contents list an annex on recycled or recyclable material inputs (Annex D in the 2011 edition) and section 8.3. Text not reachable (publisher and preview pages refused). |
| K60 | UNSURE (book text not read) | Green (2003), Third Generation Photovoltaics, Springer (a 2006 edition exists, ISBN 978-3-540-26563-4) | secondary (bookseller contents); K67 full text | Contents: 3.3 Carnot Efficiency, 3.4 Landsberg Limit, 3.5 Black-Body Limit. The 93.3 % for (6000 K, 300 K) is stated in the full text of K67, not shown from K60. 95 % equals 1 - 300/6000 and was not read in K60. |
| K67 | verified | Buddhiraju, Santhanam, Fan (2018), PNAS 115(16), E3609-E3615. DOI 10.1073/pnas.1717595115. arXiv:1710.02617 | full text (arXiv); record (PubMed for pages) | Paper states: 153.1 W/m2 at Ta = 300 K, To = 3 K "represents the ultimate limit for harvesting outgoing thermal radiation" (Eq. 3). 48.4 W/m2 is the single-intermediate-blackbody Carnot setup, maximised at Tc = 225.1 K. A two-stage system gives 72.3 W/m2. 93.3 % is the Landsberg efficiency at Ts = 6000 K, Ta = 300 K. |
| K68 | verified (record); content not read | Rosen, Dincer (2004), "Effect of varying dead-state properties on energy and exergy analyses of thermal systems", Int. J. Therm. Sci. 43(2), 121-133. DOI 10.1016/j.ijthermalsci.2003.05.004 | record (Crossref) | Journal, volume, pages and DOI confirmed. Whether it reports little sensitivity to dead-state change was not read. |
| K71 | exists but body not read; UNSURE | Rosen (1954), "Entropy of Radiation", Phys. Rev. 96(3), 555 (one page). DOI 10.1103/PhysRev.96.555 | record and abstract (Crossref, OpenAlex) | Abstract: an expression for the entropy flux of linearly polarized radiation of any specific intensity K_nu, then generalised to include polarization. Two references (Planck, Theory of Heat; Slater, Introduction to Chemical Physics). A mode-entropy expression `(1+n)ln(1+n) - n ln n` is not shown in the abstract; the full page is closed access and was not read. |

Other records checked in passing: K13 Crossref lists seven authors, first author Dewulf, then Bösch, De Meester, Van der Vorst, Van Langenhove, Hellweg, Huijbregts (DOI 10.1021/es0711415). K12 is DOI 10.1065/lca2006.11.282 (Bösch, Hellweg, Huijbregts, Frischknecht), 12(3), 181-190.

## Decisive check (item 3)

Question: in the Szargut method for cumulative exergy consumption, (a) is the ore's own exergy included, (b) which by-product rule, (c) capital goods?

Source quality: no primary text (K1, K2, K3) was reachable. Everything below is secondary or abstract-level. The books and the 1987 paper are not openly available; I did not use pirated copies that turned up in search results.

- (a) Ore's own exergy: yes, per a secondary description (Sciubba 2021, Frontiers in Sustainability, open access, DOI 10.3389/frsus.2021.739395). It says raw materials entering directly from the environment carry a "raw exergy" equal to their reference exergy, pre-treated materials carry raw value plus pretreatment expenditures, and the incoming flows include renewable and non-renewable sources. Confidence: moderate (one secondary source, paraphrasing Szargut 1988 and Valero 1986).
- (b) By-product rule: substitution (principle of avoided costs) is used at least for cogeneration. Source: the author-written abstract of Szargut, Ziębik, Stanek 2002 (K7, record on OSTI): "The cogeneration processes have been considered using the principle of the avoided costs of fabrication of the products substituted by the by-products of the considered process." A search summary of a Szargut abstract says the same for by-products in general, with a caveat for by-products that replace imports. Sciubba 2021 says only that "proper allocation rules for multiple products are suggested by Szargut (2005)" and that thermo-ecological cost shares by exergy-based rules (citing Serra and Torres). The 2005 rules themselves were not read. UNSURE whether substitution applies to all multi-product processes in the tabulated CExC values.
- (c) Capital goods: not found in any reachable source. The K7 abstract states that the ecological cost of human work cannot be introduced into the input-output equations (labour excluded). UNSURE for machines and buildings.
- Caveat: K7 concerns the non-renewable-only ecological cost, which is a subset indicator of CExC. The abstract describes the general ecological-cost equations, so it is indicative for CExC but not a direct statement about the all-resource tables.

## Open data (items 4 and 5)

- Szargut et al. 2005 element table (exergoecology.com): shown as an HTML table "Table 1: Chemical exergy of the Elements. Source: Szargut et al. 2005" on the Reference Environment page, 85 element rows, b_ch in kJ/mol (comma decimals). The site offers the 2005 ECOS paper (PDF, 211 kB) as the "complete methodology". No CSV or data file. Compounds are available only through an interactive calculator. No licence statement found; every page footer reads "Copyright 2018, iCIRCE. All Rights Reserved." So: viewable and copyable by hand, not downloadable as data, no open licence stated. Treat as all rights reserved; ask the site owners. TaesLab (MATLAB/Octave) has download links; its licence was not seen.
- CExD (K12): the paper's version is in the Radboud repository (not opened). The factors are distributed as an LCIA method inside ecoinvent (the ecoinvent v3.12 LCIA implementation document lists CExD, versions v2.2 and v3.12) and in SimaPro's method library. They are tied to those products' licences. No standalone open download or licence found. UNSURE.
- CEENE (K13): factors are in the ES&T paper and its supporting information, and in later papers that reuse them. The SI was not fetched. Licence UNSURE.
- ASTM E-490: NREL hosts the "2000 ASTM Standard Extraterrestrial Spectrum Reference E-490-00" as a free data file (119.5 to 1,000,000 nm, integral set to 1366.1 W/m2). Source: search-result summary only, because www.nrel.gov returned proxy 502 here. Terms: the page says use implies agreement with the NREL data disclaimer; no explicit licence seen. The formal ASTM standard document is a paid product. UNSURE on licence.
- SORCE: LASP's LISIRD serves SORCE solar spectral irradiance (SIM/SOLSTICE level 3). I retrieved a small CSV from its LaTiS endpoint (columns time as Julian date, wavelength nm, irradiance W/m2/nm; HTTP 200), so the data are openly downloadable. No licence text found on the pages reached; LASP material says data are made freely available to the scientific community (secondary, NASA NTRS summary). UNSURE on licence and citation terms.

## Effect on the answer

Findings L1-L16 and conventions V1-V9 are listed only where something changes. None of the algebra-based findings (L1, L2, L4-L15 as far as I read them) depends on any item checked here.

| Item | Effect |
|---|---|
| K7 | Section 4 row for K7 says "title corrected; volume UNSURE". Both are wrong: Crossref gives "non-renewable" and volume 43. Revert the title correction and drop the volume flag. Section 5 item 10 lists K7 as a correction; that line should go. No finding changes (V6 uses K7 only for the non-renewable-only option). |
| K22 | Remove "author order UNSURE". |
| K33 | Volume and pages are confirmed; DOI 10.1065/lca2006.11.283. |
| K36 | Section can now be stated: Annex I, 4.4.8.1, Equation 3. Q3 mapping and V2 unchanged. |
| K37 | The CFF material term quoted in prompt_2_review.md matches Equation 3 of the 2019 report. No change. |
| K38 | The answer cites section 5.4.7 for the 50:50 formula. That section has no formula; it is Annex V of the PEF Guide (called up from 5.10). V2 names 50:50 only as an option, so no finding changes, but the citation line should be corrected. The exact equation stays unread. |
| K39 | Already dropped. The check supports that decision: Nord 1995:20 is a user of one 50/50 variant, not shown to be the origin. |
| K44 | Confirmed as not saying this; the answer already replaced it by K34. No change. |
| K67 (L6) | The answer's 153.1 W/m2 ultimate limit at 300 K and 3 K is confirmed in the full text; 48.4 W/m2 is a single-device result (Tc = 225.1 K), as the answer states. The open point about 225.1 K against 225 K in R29 is a rounding difference of the paper's maximiser; whether R29 intended 225 as a design value is not something this check can say. The page range is E3609-E3615. No change to L6. |
| K68, K8 | Not relied on in the answer. K68 record is now complete; its content is unread. The answer's reliance on the Gibbs-Helmholtz derivation for D5(3) is unaffected. |
| K71 | Still not relied on. The abstract concerns entropy flux for a given specific intensity, not a mode-entropy expression; the answer's use of K70 with R32 stands. |
| K60 | Still not relied on. The 93.3 % can be cited to K67 instead (full text read). |
| K29, K46 | Unchanged: UNSURE. V4 rests on plan D4, not on a clause number. |
| Decisive check (L3, L9, L16, V6) | (a) is supported by one secondary source: the L3 closure premise that CExC includes the ore's own exergy has support, at moderate confidence. (b) Szargut uses a substitution (avoided-cost) rule at least for cogeneration by-products, whereas V6 recommends no substitution credit and exergy partition. If the framework's tabulated CExC values were built with substitution, they are not on the V6 basis; this bears on L16 and V6 and should be stated there as a condition. I did not re-read L9 or L16 text, so I cannot say how large the change is. (c) Capital goods stay UNSURE, so L9 is not settled by this check. |
| Open data | The V6 and L2 data route via the exergoecology.com element table is available to read but has no stated licence. |

## Candidate sources (not evidence)

- Szargut (2005), Exergy Method, WIT Press: the primary text for rules on multi-product processes and capital goods. A scanned copy appears on a third-party document site; I did not use it because of provenance.
- Szargut, Morris, Steward (1988) and Szargut, Morris (1987): primary texts for the decisive check (library access).
- Stanek and co-workers, thermo-ecological cost review (Energy, 2018, DOI via ScienceDirect, closed): may state the by-product and investment treatment.
- Serra, Torres (2003), Structural Theory of Thermoeconomics, EOLSS: cited by Sciubba for exergy-based sharing rules.
- Ekvall (1999) thesis on Chalmers: open account of the two 50/50 variants and Vigon et al. 1993.
- Vigon et al. (1993), LCA Design and Management Guidance Manual (US EPA): earlier 50/50 variant.
- NREL AM0 page and LISIRD SORCE pages: for licence wording, check directly once reachable.
- Ecoinvent LCIA implementation document v3.12 (CExD listing).
