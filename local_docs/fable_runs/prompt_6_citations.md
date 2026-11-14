# Prompt 6 S3: citation and input check

Everything here is a claim at level `derived` (unverified). Method: web search snippets and a few fetched pages. arxiv.org, api.crossref.org and most publisher pages were not opened; Springer, Wiley, ScienceDirect and ASME records were read through search snippets only. WebFetch of ebin.pub (503), philarchive.org (403) and the NIST copy of the ASM chapter (404) failed, so no book table was read directly. "Secondary" below means a paper or site quoting the primary source.

## Summary

| Table | Verdict counts |
|---|---|
| MEMORY (M01 to M32) | confirmed 14, differs 2, UNSURE 16 |
| LOOKUP (L01 to L07) | planner range contains or matches the source 5 (L02, L03, L04, L05, L07), UNSURE 2 (L01, L06) |
| Citations (43) | verified 31, exists but may not say this 10, UNSURE 2, not found 0 |

Inputs that differ or are doubtful, most consequential first:

1. **M03, Basquin exponent b of 2024-T4.** Plan: -0.102 (m = 9.804). One secondary table of "published values" (PhilArchive, Trent, snippet only) gives sigma_f' = 900 MPa and b = -0.124 (m = 8.06) for 2024-T4. The plan's sigma_f' = 900 MPa agrees with that table; b does not. I could not read Dowling Table 9.1 itself, so which is right is open. This shifts every life computed from sigma_a0 and m (rows B, C, E).
2. **M18, expansion mismatch metal minus alumina.** Plan: 7e-6 /K (range 5e-6 to 8e-6). For an aluminium alloy substrate the sources give 2024 at 22.8e-6 to 23.2e-6 /K and alumina at 8.1e-6 /K (engineeringtoolbox, Misumi, samaterials; room-temperature alumina can be lower, 4.6e-6 at 20 C in one patent), so the mismatch is about 15e-6 /K (22.8 - 8.1 = 14.7). 7e-6 fits a Ni-base or Fe-Cr substrate, not Al. It affects the thermal-mismatch stress in D5/D6 by a factor of about 2.
3. **M02, M29, M09, M11:** M02 is supported only by the secondary table above. M29 (25 to 35 % of air value) is consistent with a secondary statement but the ASM text was not read, and a vendor page gives the opposite emphasis (20 to 40 % loss). M09 and M11 were not confirmed (see table).
4. **L04:** the planner's "888.2" is 888.4 in the textbook tables (an exergoecology table shows 888.20, so the two spellings both occur). 795.7 is the revised value.

Everything else the plan quoted from memory that I could check was right (ISO 9223 Al limits, Magnus coefficients, DNV D-curve constants, MIL-HDBK-5 2024-T3 equation, R, FKM 0.3, E647 1e-10 m/cycle, Tedmon and Opila-Hann records).

LOOKUP sources openly downloadable: L03 (older DNV-RP-C203 PDFs are public at rules.dnv.com and in university copies; copyright DNV, no open licence stated), L05 (Opila and Hann 1997 as NASA CR-204668 on NTRS, US government report, scanned PDF; Tedmon 1966 is paywalled), L07 (MIL-HDBK-5J on everyspec.com; US government document; the same equation is in MIL-HDBK-5H posted at ae.metu.edu.tr). Not openly downloadable as data: L01 (ASM Handbook, copyright; a copy of the Bucci chapter is hosted at materialsdata.nist.gov, licence not stated, figures only), L02 (figures in papers; NASGRO is licensed), L04 (book), L06 (tables inside paywalled papers, no repository found).

## Table 1: MEMORY inputs

| Id | Verdict | Source / note |
|---|---|---|
| M01 | confirmed | SI 2019 exact: R = N_A k_B = 8.314462618... J/(mol K). Recall only; no search. |
| M02 | confirmed (secondary only) | sigma_f' = 900 MPa for 2024-T4 in a PhilArchive table of "published values" (snippet; attributed source not visible). Dowling Table 9.1 not read. Dowling's title for Table 9.1 confirmed through an ebin.pub snippet ("Constants for Stress-Life Curves for Various Ductile Engineering Metals"); Example 9.4 uses 2024-T4. |
| M03 | differs | b = -0.124 in the same secondary table (m = 1/0.124 = 8.06); plan -0.102 (m = 9.804). Not confirmed against Dowling. Another 2024-T4 paper fits other values (-0.1044 appears in a snippet, parameter unclear). |
| M04 | confirmed | MatWeb ASM data sheet for 2024-T4 quotes fatigue strength 138 MPa at 5e8 cycles (RR Moore, completely reversed). Convention holds. |
| M05 | UNSURE | Sources I saw give 69 to 73 GPa for 2024 (one paper uses 69, another 72, Wikipedia about 73). Not tied to one source. |
| M06 | UNSURE | 2780 kg/m3 is the usual handbook value; no source opened. |
| M07 | UNSURE | 26.98 g/mol is the standard atomic weight (26.982); recall only. |
| M08 | confirmed | ISO 9223:2012 Table 2, aluminium, g/(m2 a): C1 negligible, C2 <= 0.6, C3 0.6 to 2, C4 2 to 5, C5 5 to 10, CX > 10. Sources: RRCAP/AIT slides, Zinkinfo Benelux table, iTeh sample PDF of the standard. Note the standard gives C1 as negligible; the plan starts at C2, which is consistent. |
| M09 | UNSURE | Search returned no resistance-coefficient source. My recall (not evidence): Cu 0.00393, pure Al 0.0043 /K; plan 0.0040 for Al is at the edge of its own +-0.0003, and alloy 2024 has a lower value than pure Al. |
| M10 | UNSURE | Al2O3/Al 1.28, Cr2O3/Cr 2.07, NiO/Ni 1.65 are the usual textbook values (Wikipedia/Pilling-Bedworth pages were in results, values not read). Not confirmed. |
| M11 | UNSURE | TEMA water table via accessengineeringlibrary snippet: seawater 0.00009 (up to 115 C heating medium, water <= 52 C), 0.0002 above that; brackish 0.0002 to 0.0005; treated cooling tower 0.0002 to 0.0004; untreated 0.0005 to 0.0009. Other sources give seawater 0.0005 or 0.00018 to 0.00035. Values are in the plausible band but sources conflict by edition. Full table is copyrighted. |
| M12 | confirmed | Alduchov and Eskridge 1996, eq. 21: e_s = 6.1094 hPa exp(17.625 T/(243.04 + T)), T in C; 610.94 Pa form appears in a 2018 AMS paper. Sources: Wikipedia vapour-pressure page and OSTI/Semantic Scholar record. |
| M13 | UNSURE | Not searched; my recall is that ISO 9223 defines time of wetness as RH > 80 % and T > 0 C. |
| M14 | confirmed (caveat) | Manson and Halford 1981 abstract confirmed; the 0.4 appears as the exponent on N_f in the damage-curve crack-length form (PMC article). The explicit (N1/N2)^0.4 exponent form was not shown in any snippet. |
| M15 | confirmed (arithmetic only) | 2 x 1.12 / pi = 0.7130. The handbook source of the factors was not checked. |
| M16 | confirmed | ASTM E647: operational DeltaK_th is the DeltaK at da/dN = 1e-10 m/cycle (search summary of the standard, scribd copy; one paper quotes it as 1e-7 mm/cycle, the same). |
| M17 | UNSURE | Not searched. alpha-alumina E about 380 GPa, nu about 0.25 is typical; nu varies 0.22 to 0.26 by source. |
| M18 | differs | See summary item 2: about 15e-6 /K for Al substrate (22.8e-6 to 23.2e-6 minus 8.1e-6). 7e-6 holds only for a Ni-base or Fe-Cr substrate. |
| M19 | UNSURE | Grid is a planner range; no source. |
| M20 | UNSURE | Grid is a planner range; no source. |
| M21 | UNSURE | Not searched. |
| M22 | UNSURE | Lazan 1968 exists and states D = J sigma^n; an example in a J. Phys. Conf. Ser. paper quotes n about 3.2 for low-carbon steel. For aluminium 2 to 3 not confirmed. |
| M23 | confirmed | 25 C = 298.15 K is the standard reference temperature convention. |
| M24 | UNSURE | Planner grid; no source. |
| M25 | confirmed | Godard 1960 abstract: "data supporting a cube-root-in-time rate curve for the pitting of aluminum in water". |
| M26 | confirmed (caveat) | FKM Table 2.4.3: D_M = 0.3 for non-welded steel and steel castings; a secondary source (McKelvey, Lee, Barkey 2012) says 0.3 also for aluminium, 1.0 for cast irons; welded 0.5 comes from a calculator site only. Scribd copy of the table is garbled. 6th edition not read. |
| M27 | confirmed as energy, not exergy | Primary aluminium embodied energy 170 to 220 MJ/kg (MDPI review; Energies 2026 paper), 191 MJ/kg (Wellington table), 210 +- 10 (compilation); range 150 to 230 across regions. No exergy figure found (Balomenos et al. 2011 would be the source to open). |
| M28 | confirmed | m = 3 is the DNV-RP-C203 slope for welded joints in air (curve D, N <= 1e7). m = 12 for b = -0.085: 1/0.085 = 11.76, so "m = 12" is a rounding. |
| M29 | UNSURE | Secondary (ion-beam paper citing the ASM Handbook 19 Bucci chapter): axial fatigue limit of 2024 and 7075 sheet is "3 to 4 times lower" in seawater than air, ratio 0.25 to 0.33 (R = 0, cycle count not stated). A vendor page says 20 to 40 % loss. The ASM statement itself was not read. |
| M30 | confirmed (arithmetic) | 1675.7 / 2 = 837.85 kJ/mol Al. The formation enthalpy value is recall. |
| M31 | UNSURE | No source for 5 MPa sqrt(m) for a high-temperature alloy. |
| M32 | UNSURE | Planner grid; no source. |

## Table 2: LOOKUP inputs

| Id | Verdict | Source / note |
|---|---|---|
| L01 | UNSURE | Source: ASM Handbook Vol. 19, Bucci et al. "Selecting Aluminum Alloys to Resist Failure by Fracture Mechanisms" (pp. 771 to 812), figure "Axial stress fatigue strength of 0.8 mm 2024, 7075, and clad sheet in air and seawater, R = 0", plus a second air-versus-seawater comparison figure. Numbers not read (figure only, OCR copy on materialsdata.nist.gov; WebFetch 404). Secondary ratio 0.25 to 0.33 would lie inside the planner's k8 range 0.25 to 0.6 but is not tied to 1e8 cycles. k5 (1e5 cycles) not found. Another candidate: Baragetti (Univ. Bergamo, open PDF, 7075-T6 air vs 3.5 % NaCl) shows a 50 to 70 MPa strength drop for 1e4 to 1e6 cycles, data stop near 1e6. Openly downloadable only as figures; not tabulated; ASM copyright. |
| L02 | within range | 2024-T3 DeltaK_th about 3 MPa sqrt(m) at R = 0.1 (NASA/ASTM symposium paper); about 3 MPa sqrt(m) at R = 0 (thin-sheet closure analysis); 2.1 MPa sqrt(m) K_max in ambient air and 3.3 in vacuum at 20 kHz. Planner range 2 to 5, baseline 3.0 contains them. Best table source: Mackay, Eng. Fract. Mech. 1979 (2024-T3 and 7075-T6 clad, R 0.05 to 0.6), numbers not read. Paywalled journals; NASA paper open on NTRS. |
| L03 | matches | DNV-RP-C203, curve D, air: m1 = 3, log a1 = 12.164 for N <= 1e7; m2 = 5, log a2 = 15.606; fatigue limit 52.63 MPa at 1e7. Free corrosion: m = 3, log a = 11.687, no knee. Same row in 2008 edition; free-corrosion table is Table 2-3 (2008, 2011) and Table 2-4 (2016). Seen through search summary of the 2016 PDF (fenix.tecnico.ulisboa.pt) and the 2008 PDF (rules.dnv.com); I did not open the PDFs. Note the monopile-specific 2024 curve D differs (m1 = 3.45, log a1 = 13.043, m2 = 5.7, log a2 = 17.325, knee 3e6), and the CP curve has log a1 = 11.764. Openly downloadable (older editions); copyright DNV; no open licence. |
| L04 | within range (888.2 vs 888.4) | 888.4 kJ/mol Al: older Szargut value (textbook tables); 795.7 kJ/mol: revised value in Szargut's 2007 Polish handbook "Egzergia" (MIT appendix lists 795.7 and notes it as updated against the 2005 English edition). Another site lists 796.10 and one proposal gives 790.39. Rivero and Garfias 2006 found aluminium among the few elements changed. The planner's "795.7 or 888.2" holds, and 795.7 is the current one on this evidence. Source is books and a MIT appendix PDF (no licence stated). |
| L05 | within range | Opila and Hann 1997 (NASA CR-204668, open on NTRS, scanned; I OCRed it, text saved as `prompt_6_citations_code/data/raw/opila_hann_1997.txt`, PDF in the same folder, both gitignored). Table III k_p in 50 % H2O / 50 % O2: 1.05e-3 to 5.57e-3 mg2/(cm4 h) at 1200 to 1400 C (OCR; column assignment of some rows is uncertain). Table IV k_l (paralinear fits): 1.43e-3 to 7.75e-3 mg SiO2/(cm2 h). Converted to thickness units by `prompt_6_citations_code/l05_convert.py` (my stoichiometry alpha = 3.0055 for SiC + 1.5 O2 -> SiO2 + CO, rho(SiO2) = 2.2 g/cm3; both are my assumptions): k_p' 5.4e-17 to 2.9e-16 m2/s, k_l 1.8e-12 to 9.8e-12 m/s. Planner ranges 1e-17 to 1e-15 m2/s and 1e-12 to 1e-10 m/s contain these. Tedmon 1966 (Cr, Fe-Cr) numbers not found (paywalled). |
| L06 | UNSURE | No open dataset found. Sankaran et al. (2001) and Dolley et al. (2000) give results in tables and figures inside paywalled papers. Corrosion Science 2004 paper on pit-to-crack transition in pre-corroded 7075-T6 has data in its Tables 1 and 2 (paywalled). A Materials Commons dataset (DOI 10.13011/m3-rcyy-gx13, ODC-By) exists for 7075-T6 fatigue but is not about pitting. The 2 to 10 life factor was not verified. |
| L07 | matches | MIL-HDBK-5H CN1, unnotched 2024-T3 bare sheet 0.090 in, axial, Fig. 3.2.3.1.8(e): log Nf = 11.1 - 3.97 log(S_eq - 15.8), S_eq = S_max (1 - R)^0.56, ksi; also on kaspercalc.com. Equation identical to the plan's. MIL-HDBK-5J itself was not opened (5H figure marked "printed without change", 5J likely same; UNSURE). Standard deviation of log life 0.90, 107 samples; caution about extrapolating to other R. Open: US government handbook, public (everyspec.com, METU copy). |

## Table 3: Citations

Verdict key: verified = exists and the bibliographic record or abstract supports the cited use. "may not say" = exists, but what the plan cites it for was not seen in what I read.

| # | Verdict | Source / note |
|---|---|---|
| 1 | verified | de Groot and Mazur, Non-Equilibrium Thermodynamics, North-Holland, 1962, 510 pp (Meixner review, Z. Elektrochem. 66). Chapter not checked. |
| 2 | UNSURE | Bejan 1996, CRC Press: only a citation in a review found (titled "Entropy Production Minimization" there). No catalogue record read. |
| 3 | verified | Basquin 1910, Proc. ASTM 10, 625 to 630 (CiNii, SciSpace record; SciSpace lists it as open access). |
| 4 | verified | Palmgren 1924, VDI-Z 68(14), 339 to 341 (STLE critique of ISO 281, Springer reference lists). |
| 5 | verified | Miner 1945, J. Appl. Mech. 12(3), A159 to A164, DOI 10.1115/1.4009458; abstract states failure at 100 % damage. |
| 6 | verified | Manson and Halford 1981, Int. J. Fract. 17, 169 to 192, DOI 10.1007/BF00053519. Equation number not found. |
| 7 | verified | Fatemi and Yang 1998, Int. J. Fatigue 20(1), 9 to 34, DOI 10.1016/S0142-1123(97)00081-9; survey of six damage-theory classes incl. nonlinear damage-curve approaches. |
| 8 | exists but may not say this | Schütz 1996, Eng. Fract. Mech. 54(2), 263 to 300. Open text (University of Washington copy) says Miner's rule was often found inaccurate and Miner claimed conservative results; I did not see a numeric range of Miner sums. |
| 9 | verified | Haibach 1970, LBF TM 50/70 (Google Books record); slope k' = 2k - 1 below the knee is described in an axle-fatigue paper as the Haibach modification. |
| 10 | exists but may not say this | FKM guideline: D_M = 0.3 in Table 2.4.3 (garbled scan, secondary confirmations); 6th edition (2012) and section not read; aluminium and welded values rest on secondary sources. |
| 11 | verified | ASTM E1049-85, rainflow in Section 5.4 (range-pair and rainflow defined); current as E1049-85(2023). |
| 12 | verified | Smith, Watson, Topper 1970, J. Materials 5(4), 767 to 778. |
| 13 | exists but may not say this | Dowling 4th ed.: Table 9.1 title confirmed; 2024-T4 row not read (see M02, M03). |
| 14 | exists but may not say this | MIL-HDBK-5J exists. The equation was found in MIL-HDBK-5H (Fig. 3.2.3.1.8(e)); 5J figure number not confirmed. |
| 15 | verified | Lazan 1968, Pergamon, 317 pp, ISBN 0080029345; D = J sigma^n confirmed; stress-history effect not checked. Archive.org has a borrowable copy. |
| 16 | verified | Wagner 1933, Z. Phys. Chem. B21, 25 to 41, DOI 10.1515/zpch-1933-2105. |
| 17 | exists but may not say this | Pilling and Bedworth 1923, J. Inst. Met. 29, 529 to 591 exists and introduces the volume-ratio criterion. The specific ratios in M10 are not from this paper. |
| 18 | verified | Tedmon 1966, J. Electrochem. Soc. 113(8), 766 to 768, DOI 10.1149/1.2424115; abstract describes parabolic growth with linear volatilisation, limiting thickness k_d/k_s. Equation number not seen. |
| 19 | verified | Opila and Hann 1997, J. Am. Ceram. Soc. 80(1), 197 to 205; I read the NASA reprint by OCR (paralinear form, limiting thickness k_p/(2 k_l), Tables III and IV). |
| 20 | verified | Lowell et al. 1991, Oxid. Met. 36, 81 to 112, DOI 10.1007/BF00938457; spalling model compared with random-site model. |
| 21 | exists but may not say this | Smialek 2003, Acta Mater. 51(2), 469 to 483; abstract covers parabolic growth, constant spall area fraction, maximum weight change and a 1:3 ratio of cycles; a long-run linear rate is not stated in the abstract. |
| 22 | exists but may not say this | Evans 1995, Int. Mater. Rev. 40(1), 1 to 40, DOI 10.1179/imr.1995.40.1.1; abstract is about growth stresses and their effect on diffusion. A strain-energy spallation criterion is not in the abstract (a related Evans and Lobb 1984 Corros. Sci. paper on "conditions for the initiation of oxide-scale cracking and spallation" appeared in results; candidate). |
| 23 | exists but may not say this | Schütze, Wiley 1997, 192 pp, ISBN 978-0-471-95904-5; contents list critical strains and oxide-scale damage diagrams; no values seen. |
| 24 | exists but may not say this | Hancock and Nicholls 1988, Mater. Sci. Technol. 4(5), 398 to 406, DOI 10.1179/mst.1988.4.5.398; abstract: composite defect size, stress intensity factor of growing scales. The form eps_c = K_Ic/(f E sqrt(pi c)) is plausible but not seen. |
| 25 | verified | Kitagawa and Takahashi 1976, ASM, Boston, 627 to 631 (Springer reference lists). |
| 26 | verified | El Haddad, Topper, Smith 1979, Eng. Fract. Mech. 11(3), 573 to 584, DOI 10.1016/0013-7944(79)90081-X. |
| 27 | verified | Kondo 1989, Corrosion 45(1), 7 to 11, DOI 10.5006/1.3577891; pit growth, pit-to-crack transition. |
| 28 | verified | Harlow and Wei 1994, AIAA J. 32(10), 2073 to 2079 (some lists give 2082), DOI 10.2514/3.12254. |
| 29 | verified | Godard 1960, Can. J. Chem. Eng. 38(5), 167 to 173, DOI 10.1002/cjce.5450380507. Abstract supports the cube-root-in-time pitting curve. |
| 30 | verified | Sankaran, Perez, Jata 2001, Mater. Sci. Eng. A 297(1-2), 223 to 229; 7075-T6 pre-pitted lives against predicted lives. The life-reduction factor was not seen. Data not openly downloadable (see L06). |
| 31 | verified | Dolley, Lee, Wei 2000, Fatigue Fract. Eng. Mater. Struct. 23(7), 555 to 560, DOI 10.1046/j.1460-2695.2000.00323.x. Abstract not seen; the 2024-T3 content rests on how it is cited elsewhere. |
| 32 | verified | Gangloff 1990, NACE-10, pp. 55 to 109 (some lists 55 to 106). |
| 33 | verified | Wei and Landes 1969, Mater. Res. Stand. 9(7), 25 to 27 (later pages 44, 46); superposition model described in secondary sources. Order of authors varies in lists. |
| 34 | verified | Suresh, Zamiski, Ritchie 1981, Metall. Trans. A 12, 1435 to 1443, DOI 10.1007/BF02643688; oxide-induced closure explains near-threshold behaviour (in 2 1/4 Cr-1 Mo steels). |
| 35 | verified | ISO 9223:2012 Table 2 gives the aluminium classes (see M08). Humidity threshold not searched (M13). |
| 36 | verified | DNV-RP-C203 (see L03). |
| 37 | UNSURE | ASM Handbook Vol. 19 (1996) exists and the Bucci chapter has the air versus seawater figures; the M29 percentage and the L02 delta-K_th values were not read in it. |
| 38 | verified (secondary) | Szargut, Morris, Steward 1988, Hemisphere; Al 888.4 kJ/mol older value, 795.7 revised (see L04). Book not opened. |
| 39 | verified | ASTM E647 (see M16). |
| 40 | verified | ASTM G96-90(2018): Test Method A is electrical resistance, giving cumulative metal loss; resistance rises as the element cross-section falls. Full text paywalled. The plan's R ~ 1/(h0 - h) is the ER principle, not a quoted equation. |
| 41 | verified | Alduchov and Eskridge 1996, J. Appl. Meteorol. 35(4), 601 to 609 (see M12). |
| 42 | verified (clause, not table) | EN 1999-1-3:2007+A1:2011 clause 6.4 "Effect of exposure conditions": detail category downgraded for some alloy and exposure combinations; one source says two categories lower for sea water. Table values not read. Free 2007 PDF at phd.eng.br (copyright CEN). EN 1999-1-3:2023 now supersedes it; clause numbers may differ. |
| 43 | exists but may not say this | TEMA standards exist, and water fouling values appear in the 0.00009 to 0.0009 band (see M11), but editions disagree and the table is copyrighted. |

## Datasets named in the brief

| Dataset | Openly downloadable? | Licence |
|---|---|---|
| Corrosion-fatigue S-N, environment versus air (Al alloys) | No. Figures in ASM Handbook 19 (copy of the Bucci chapter on materialsdata.nist.gov); Baragetti PDF (Univ. Bergamo) shows S-N plots to about 1e6 cycles; NACA/NASA air-only 2024-T3 and 7075-T6 data to 1e8 cycles on NTRS (TN D-111, reanalysed in arXiv 1909.10741). No tabulated file found. | ASM copyright; NASA reports public domain |
| Paralinear oxidation data | Opila and Hann 1997: tables (k_p, k_l, thicknesses) inside the NASA CR reprint, open on NTRS; raw TGA curves only as figures. Tedmon 1966: paywalled. | US government report, none stated |
| Pre-pitted fatigue life versus pit depth | No repository file found; tables in paywalled papers (Corrosion Science 2004 pit-to-crack transition paper, Sankaran 2001, Dolley 2000). | publisher copyright |

## Files written

- `<gms-local>/local_docs/fable_runs/prompt_6_citations_code/l05_convert.py` (run with `.venv/bin/python`, reproduces L05 conversion)
- `<gms-local>/local_docs/fable_runs/prompt_6_citations_code/ocr_pdf.py` (OCR helper, run with `~/.venvs/gms_pdf/bin/python`)
- `<gms-local>/local_docs/fable_runs/prompt_6_citations_code/data/raw/opila_hann_1997.pdf` and `.txt` (gitignored)

## Candidate sources found (listed, not used as evidence)

- Balomenos et al. 2011, "Energy and Exergy Analysis of the Primary Aluminum Production Processes" (for an exergy figure behind M27).
- Mackay 1979, Eng. Fract. Mech., "Fatigue crack propagation rate at low DeltaK of two aluminum sheet alloys, 2024-T3 and 7075-T6" (DeltaK_th against R, for L02).
- Mayer et al., "Slow fatigue crack growth in 2024-T3 and Ti-6Al-4V at low and ultrasonic frequency", Int. J. Mater. Res. 2003 (threshold in air versus vacuum).
- Evans and Lobb 1984, Corros. Sci. 24, "Conditions for the initiation of oxide-scale cracking and spallation" (possible source for the strain-energy criterion cited to Evans 1995).
- Opila, "Oxidation and Volatilization of Silica Formers in Water Vapor", NASA NTRS 20020070889 (k_l expressions).
- Smialek and Auping 2002, Oxid. Met. 57, COSP for Windows; "Simplified Paralinear Oxidation Analyses" (ResearchGate) for approximations k_p ~ 4.1 DeltaW_max^2/t_max and k_l ~ 1.2 DeltaW_max/t_max.
- Kinetics of high-temperature oxidation and chromia volatilization for a binary Ni-Cr alloy, Oxid. Met. (K_p and K_v per temperature, 1000 to 1300 C).
- Larrosa, Akid, Ainsworth 2018, "Corrosion-fatigue: a review of damage tolerance models", Int. Mater. Rev. (pit-to-crack models, overview of Kondo, Harlow-Wei).
- Materials Commons PRISMS-Fatigue dataset (7075-T6, ODC-By), not about pitting but an open fatigue dataset.
- NACA/NASA TN D-111 and arXiv 1909.10741 (2024-T3 and 7075-T6 air S-N to 1e8 cycles; the second notes T3, T351 and T4 tempers have nearly identical fatigue properties, which bears on using T4 constants for M02, M03).
- Wellington (NZ) embodied-energy coefficients PDF (191 MJ/kg virgin aluminium).
