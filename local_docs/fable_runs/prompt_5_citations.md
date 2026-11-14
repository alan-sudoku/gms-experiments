# Prompt 5, S3: citation and input check

Date: 2026-11-14. Level of everything in this file: `derived` (unverified). Checker: S3 agent, independent of `prompt_5_code/` (not read).

## Header

- Hosts used: physics.nist.gov (XrayMassCoef element tables Z = 6, 13, 26, 29, 50, 56, 64, 74, 82, 83 and Table 1 densities; XCOM form, POST to `xcom3_1`), www.ncnr.nist.gov (Sears 1992 table), api.crossref.org, journals.plos.org (Nuss and Eckelman Supporting Information S1, Table S38), kps.fsv.cvut.cz (a copy of ICE v2.0 Summary Tables), www.osti.gov/etdeweb (INDC(NDS)-440 PDF), en.wikipedia.org (CRC crustal abundance data page; secondary), and general web search (titles, authors, technical terms only).
- Method: numeric inputs were fetched as files and parsed by scripts, then compared with the planner's value or range. Bibliographic records were checked by Crossref query or web search. A claim stays UNSURE where no primary text was read.
- Scripts (all under `<scratch>/s3/code/`): `parse_nist.py` (W/C ratios, F2, F3, F7 numbers; run with `python3 -I parse_nist.py <s3>/nist`), `xcom_fit.py` (F4 and Klein-Nishina check; `<s3>/xcom`), `sears.py` (Sears table; `<s3>/nist/sears.html`), `xref.py` (Crossref), `derived_checks.py` (arithmetic on N3, N4, N5, H1, H2, G3.7).
- Downloaded data (data only, never run): `<s3>/nist/`, `<s3>/xcom/`, `<s3>/ice/ice.pdf`, `<s3>/nuss/s1.bin`, `<s3>/indc/indc.pdf`, `<s3>/crossref/out.txt`. `<s3>` = `<scratch>/s3`.
- Could not reach or did not read: Mughabghab Atlas 2006 and 2018 (book, paywalled), IEC 60228, IEC 60028, ANSI/ANS-6.4.3-1991, Linden and Reddy, Lamarsh and Baratta, Incropera (only a secondary scan was found), Coey 2010 and 2011 table text, Skomski and Coey 1993 and 2016 text, Skomski et al. 2010, Xia et al. 2009 full text, Gilliam et al. 2007 correlation, Ellmer 2012, Reay et al., Attix, Kraus et al., Bejan, Ashby, Pourbaix, Shultis and Faw. TARA (Trinity College repository) returned a Cloudflare challenge for the Skomski and Coey 1993 PDF; no attempt was made to get around it. USGS Mineral Commodity Summaries were not queried (production half of Row N6 is not checked). `www-nds.iaea.org` was not tried.
- A note on the INDC(NDS)-440 file: it lists the (n,gamma) channel only. It does not give the (n,alpha) absorption of B-10 or Li-6, so it cannot test the 1/v claim for B-10 (Row N2).

## Part 1: MEMORY inputs

Verdict key: C = confirmed within the row's tolerance (or the planner's range); D = differs (both values given); U = UNSURE (no primary source read). "Source" names what was actually used: P = primary table or paper, S = secondary, K = own arithmetic from other inputs.

| # | Row | Quantity | Planner value | Value found | Source (author, year, location) | Verdict |
|---|---|---|---|---|---|---|
| 1 | A1 | sigma_Cu, annealed copper standard | 5.80e7 S/m | 58.0 MS/m at 20 C (IACS definition) | S: Wikipedia "Copper conductor" and a search snippet; IEC 60028 itself not read | C (S) |
| 2 | A1 | sigma_Al, 61% IACS | 3.54e7 S/m | 0.61 x 5.80e7 = 3.538e7 (K). Search snippets give 3.5 to 3.77e7 for 1350 (61 to 64% IACS) | S: vendor and patent pages | C for the 61% IACS arithmetic. Real conductor grades spread by up to +6.5%, so the 3% tolerance of A1 depends on the grade chosen |
| 3 | A1 | rho_Cu, rho_Al | 8 960, 2 700 kg/m3 | Cu 8.960 g/cm3, Al 2.699 g/cm3 | P: NIST XrayMassCoef Table 1 (`tab1.html`) | C |
| 4 | A3 | e_Al primary, central value | 200 MJ/kg | ICE v2.0 virgin Al 218 (general 155, cast virgin 226, extruded virgin 214). Nuss and Eckelman 2014: primary Al 194 (158 to 246), market mix "Al TOTAL" 131 | P: Hammond and Jones 2011, ICE v2.0 Summary Tables (Aluminium block); Nuss and Eckelman 2014, S1 Table S38, column "CED [MJ/kg]" | C inside planner range 150 to 220. D from the central value: 218 is +9%, 194 is -3% |
| 5 | A3 | e_Cu primary | 55 MJ/kg | ICE v2.0 virgin Cu 57.0 (EU tube and sheet 42.0, recycled 16.5). Nuss and Eckelman: Cu total 53.7 (42.1 to 68.6); individual primary routes 44.9 to 87.8 | as above | C |
| 6 | A3, G2.4 | e_Al secondary | 20 MJ/kg | ICE v2.0 recycled Al 29.0 (cast 25.0, extruded 34.0). Nuss and Eckelman: new scrap 8.3, old scrap 23.8 | as above | C inside planner range 10 to 30. The central value 20 is between the two sources; the A4 crossover (J2 tau)* scales with e, so 29 gives a different number (UNSURE magnitude, about +45% on e_s rho_s - e_g rho_g changes) |
| 7 | A3 | e_Cu secondary (range 10 to 20) | 10 to 20 | ICE v2.0 recycled Cu 16.5. Nuss and Eckelman: Cu secondary 28.1 (23.6 to 33.7) | as above | C with ICE. D with Nuss (28.1 outside the range) |
| 8 | G2.6, D3 | e_x for Pt, central | 2.4e5 MJ/kg | Nuss and Eckelman: Pt ZA 308 000 (219 000 to 414 000); Pt RU 327 000; Pt secondary 11 900. Ir ZA 165 000, Ir RU 175 000 | P: S1 Table S38 (file `nuss/s1.bin`, CC BY 4.0) | D. 2.4e5 is 22% below the primary-ZA value 3.08e5; the planner range 1e5 to 3e5 excludes 3.08e5 and 3.27e5. Ir is inside. Effect on Delta-eta_be: scales linearly, so +28% |
| 9 | C1 | k_Cu 400, k_Al 237, k_6063 200, k_AlSi10Mg 130 (range 100 to 180) W/(m K) | as stated | not retrieved | no source read | U |
| 10 | C2 | rho(AlSi10Mg) | 2 670 kg/m3 | not retrieved | no source read | U |
| 11 | C4 | Air at 300 K: rho, mu, k, c_p, Pr | 1.177 kg/m3; 1.846e-5 Pa s; 0.0263; 1 007; 0.707 | Incropera Table A.4 (300 K): 1.1614; 184.6e-7; 26.3e-3; 1.007 kJ/(kg K); 0.707 | S: a scan of the 6th-edition tables found by search (not the book). K: ideal gas at 101.325 kPa and 300 K gives 1.1766 | C for mu, k, c_p, Pr. D for rho: 1.177 (ideal gas) against 1.1614 (Incropera), -1.3%. The planner's 1.177 is the ideal-gas value, not Incropera's table value; row C4 tolerance on h is 1% |
| 12 | D2 | Specific area a of metal foam | 5e3 to 1e4 m2/m3 | not retrieved | no source read | U |
| 13 | F3 | rho_W | 19.3 g/cm3 | 19.30 | P: NIST Table 1 | C |
| 14 | F3 | rho_graphite 1.70 (commercial), 2.26 (crystal) | as stated | not retrieved | no source read (2.26 is the standard crystal value, checker memory) | U |
| 15 | F7, G3.5 | K-edges Sn, W, Pb | 29.2, 69.5, 88.0 keV | 29.200, 69.525, 88.0045 keV | P: NIST XrayMassCoef element pages z50, z74, z82 (edge rows) | C |
| 16 | N3 | rho: Cd 8.65, Gd 7.90 g/cm3 | as stated | Cd 8.650; Gd 7.900 | P: NIST Table 1 | C |
| 17 | N3 | rho B4C 2.52, structural steel 7.8 g/cm3 | as stated | not retrieved | no source read | U |
| 18 | N3 | Sigma_a: Cd 117, B4C 84, Gd 1 480, 1 wt% B steel 3.3 cm-1 (these are in the Expected column, not MEMORY, but they check the densities) | as stated | Cd 116.8; B4C 84.3; Gd 1 504 (+1.6% on 1 480); steel 3.33 | K: `derived_checks.py` with Sears 1992 sigma and the densities above | C |
| 19 | G3.7 | sigma_a(B-10)/sigma_a(C) ~1e6; sigma_a(nat Cd)/sigma_a(Al) ~1e4 | as stated | 3 835 / 0.0035 = 1.10e6; 2 520 / 0.231 = 1.09e4 | P: Sears 1992 (NCNR table) | C |
| 20 | G3.8, N5 | Thermal diffusion length of water | 2.8 cm (range 2.7 to 2.9) | 2.85 cm (handbook value, sqrt of 8.1 cm2, used by Lamarsh's table per a code port; LLNL Table 2-2). Measured 2.725 +/- 0.03 (von Dardel and Sjostrand), 2.77 +/- 0.04 (DeJuren and Rosenwasser, NIST), 2.761 (PHYSOR 2020 average) | S: search snippets; Lamarsh table itself not read | C inside 2.7 to 2.9 |
| 21 | N5, G3.8 | Sigma_a(water) 0.0222 cm-1, x sqrt(pi)/2 = 0.0197 | as stated | 0.02219 and 0.01967 | K: N_H sigma_H with Sears sigma_H = 0.3326 b | C |
| 22 | N4, G3.8 | Collisions 2 MeV to 0.0253 eV: H 18, D 25, C 115; 1/v gain 6 000 to 6 290 | as stated | 18.19, 25.07, 115.27 (A = 56: 515); sqrt(1e6/0.0253) = 6 287 | K: `derived_checks.py` (xi formula of D8). Lamarsh table not read | C for arithmetic. Whether the textbook prints the same values is U |
| 23 | G3.9, N6 | Crustal abundance of B 10 mg/kg and the N6 list (Al 82 300, Fe 56 300, Cu 60, Co 25, Li 20, Pb 14, B 10, Nd 41.5, Gd 6.2, Dy 5.2, Hf 3.0, Sn 2.3, W 1.25, In 0.25, Cd 0.15, Ag 0.075, Pt 0.005, Ir 0.001) | as stated | identical for every listed element. Extra: Ni 84, C 200, Sm 7.05, Eu 2.0, Bi 0.0085 | S: Wikipedia data page quoting the CRC Handbook, 85th ed. (2005). The 97th ed. cited in the plan was not read. The page flags Pt and Bi as the least certain column reads | C (S) for the ordering B > Cd, Ag, In, Hf, Gd (10 against 0.15, 0.075, 0.25, 3.0, 6.2) |
| 24 | H1 | Li/SOCl2 theoretical specific energy | about 1 470 Wh/kg (UNSURE) | 1 473 Wh/kg from 4 F x 3.65 V / M(4Li + 2SOCl2 = 265.7 g) (K). A secondary page also states 1 470 | K plus S. Linden and Reddy Table 1.2 not read | C for the arithmetic (+0.2%). U for the handbook table |
| 25 | H1 | Other cell voltages (Zn/MnO2 1.5, LiCoO2 3.7, LiFePO4 3.3, Pb/PbO2 2.05 V) | as stated | not retrieved | no source read | U |
| 26 | H2 | a = 0.142 nm; geometric SSA 2 630 m2/g; C_sp ceiling about 550 F/g | as stated | SSA = 2 627 m2/g; 21 uF/cm2 x 2 627 m2/g = 552 F/g (K) | K: `derived_checks.py` (units of its printed SSA are thousand m2/g) | C for the geometry. The "published 2 630" is reproduced by the formula |
| 27 | H2 | C_dl = 21 uF/cm2 and 550 F/g attributed to Xia et al. 2009 | as stated | The paper exists (Nature Nanotechnology 4, 505). Its abstract speaks of quantum capacitance with a non-zero minimum at the Dirac point; no snippet shows 21 uF/cm2 or 550 F/g | S: abstract and index pages | U (see Part 3 entry 42) |
| 28 | H2 | Activated carbon 100 to 200 F/g, SSA 1 500 to 2 500 m2/g | as stated | not retrieved | no source read | U |
| 29 | H3 | Double-layer cell 4 to 8 Wh/kg, 5 to 15 kW/kg; Li-ion cell 150 to 260 Wh/kg, 0.3 to 3 kW/kg | as stated | not retrieved | no source read | U |
| 30 | M1, G3.12 | mu0 Ms of Nd2Fe14B | 1.61 T | 1.61 T, citing Coey. The ceiling mu0 Ms^2/4 = 515.7 kJ/m3 (K), against the plan's "about 512" (+0.7%) | S: ESM 2024 lecture slides quoting Coey 2011 | C (S) |
| 31 | M1 | mu0 Ms of Fe 2.15, Fe65Co35 2.43 to 2.45, SmCo5 1.05 to 1.14, Sm2Co17 1.25, Ba ferrite 0.48 | as stated | Ba ferrite ceiling 0.48^2/(4 mu0) = 45.8 kJ/m3 (K) matches "about 45". Fe ceiling 919.6 kJ/m3 and Fe65Co35 (2.43 T) 1 174.7 kJ/m3 (K); 1 174.7 / 3 = 391.6, matching the plan's "390 to 400" for the 1/12 limit. The input values themselves were not retrieved | K for the derived ceilings | U for the five input values |
| 32 | M1 | Realised (BH)max: NdFeB 400 to 474, ferrite 30 to 40, Alnico 5 40 to 44, Alnico 9 72 to 84 kJ/m3 | as stated | not retrieved | no source read | U |
| 33 | M2 | K1(SmCo5) 17.2 MJ/m3 | 17.2 | "about 17.2 MJ/m3" in an Sm-Co anisotropy paper that cites Coey | S: search snippet | C (S). Other K1 values and the published kappa_h (1.54, 4.3, 1.35, 0.41 to 0.45, 0.12) not retrieved: U |
| 34 | M4 | Sm2Fe17N3: mu0 M_h 1.55 T, K_h 12 MJ/m3; Nd2Fe14B A about 8 pJ/m, K 4.9 MJ/m3; Fe65Co35 2.43 T | as stated | not retrieved | no source read | U |
| 35 | G3.12, M4 | 1 090 kJ/m3 at f_h about 9% (Sm2Fe17N3 with Fe65Co35) | as stated | The paper exists; its abstract was not seen | no source read | U |
| 36 | M5 | NdFeB B_r 1.35 T, 7 500 kg/m3, H_cJ >= 900 kA/m; ferrite B_r 0.41 T, 4 900 kg/m3, H_cJ 250 to 400 kA/m | as stated | not retrieved | no source read | U |
| 37 | T1 | ITO resistivity 1 to 2e-6 ohm m, T 85 to 90% at 100 to 200 nm; In mass fraction 0.74; film density 7 140 kg/m3 | as stated | not retrieved. The In fraction arithmetic (90:10 In2O3:SnO2) was not recomputed | no source read | U |
| 38 | G2.7, P1 | Heat pipe k_eff 1e4 to 1e5 W/(m K); water at 60 C properties | as stated | not retrieved | no source read | U |

Counts for Part 1 (38 rows; the planner's "about 33" is a rough count and some planner items are split here): confirmed 21 (rows 1-7, 11, 13, 15, 16, 18-24, 26, 30, 33; rows 4, 6, 7 and 11 are confirmed only against the planner's range or only for part of the quantity, see the table); differs 1 clean (row 8, Pt) plus differences inside rows 4, 7 and 11; UNSURE 16 (rows 9, 10, 12, 14, 17, 25, 27-29, 31, 32, 34-38). 8 of the confirmed rows rest on secondary sources.

## Part 2: LOOKUP inputs

### 2a. Source existence, edition, access

| Source | Exists | Current edition or version | Access |
|---|---|---|---|
| NIST X-ray mass attenuation (Hubbell and Seltzer, NISTIR 5632 data, element tables) | yes | web pages `ElemTab/z*.html`, Table 3 | open; fetched without a login; NIST data page, licence statement not read |
| NIST XCOM (SRD 8) | yes | online, partial cross sections per element via the form | open; output only through the web form (one element per request), no bulk download seen; licence not stated on the pages read |
| Sears 1992 (Neutron News 3(3), 26-37) | yes (Crossref, DOI 10.1080/10448639208218770) | the NCNR page quotes pp. 29-37 and the table is the 1992 data | open at NCNR (https://www.ncnr.nist.gov/resources/n-lengths/); licence not stated |
| Mughabghab INDC(NDS)-440 (2003) | yes | February 2003; capture channel only | open (https://www.osti.gov/etdeweb/servlets/purl/20332542, 10 pages shown as the report PDF); licence not stated |
| Mughabghab, Atlas of Neutron Resonances, 5th ed. 2006 | yes | 5th ed., 1 372 pp, Elsevier, April 2006. A later edition exists (6th, 2018) per checker memory, not confirmed this session: UNSURE | paywalled book |
| ENDF/B-VIII.0 | yes (Nucl. Data Sheets 148, 1-142, DOI 10.1016/j.nds.2018.02.001; full text open at eScholarship and OSTI) | VIII.0 (2018); a later VIII.1 exists per the POINT2025 record seen in Crossref | data libraries open from NNDC (not fetched); paper open |
| JENDL-5 | yes (J. Nucl. Sci. Technol. 60(1), 1-60, DOI 10.1080/00223131.2022.2141903) | JENDL-5, released 2021/2022 | paper on T&F full text; library download not checked |
| Hammond and Jones, ICE v2.0 | yes | v2.0 (Jan 2011). A newer v3.0 (2019, published by Circular Ecology) exists per checker memory: UNSURE | Summary Tables PDF open (copy at kps.fsv.cvut.cz); footer "(c) University of Bath 2011", no open licence stated |
| Nuss and Eckelman 2014 | yes | PLoS ONE 9(7) e101298; per-kg CED is in S1 Table S38 and Fig. 3A | open, CC BY 4.0 (Crossref) |
| Incropera Tables A.4, A.6 | book (6th ed. 2007; 7th and 8th exist) | A.4 values found in a scan only | paywalled; a copy found on Scribd and Slideshare was not used as source |
| CRC Handbook | book | 97th ed. 2016 cited; later editions exist | paywalled; an open mirror of the 85th-ed. numbers is Wikipedia |
| USGS Mineral Commodity Summaries | yes (annual) | latest edition not checked | open, US Government publication; not queried |
| ANSI/ANS-6.4.3-1991 | yes, listed as historical on the ANSI store (GlobalSpec: inactive; 132 pages) | 1991 only; UNLV theses describe updates for low-Z, compounds and high-Z | paywalled |

### 2b. Spot checks of the planner's UNSURE ranges

| Row | Quantity | Planner range | Source value | In/out | Source |
|---|---|---|---|---|---|
| A1 | IEC 60228 class 2 table: Al area / Cu area at equal R, 1.6 to 1.7 | 1.6 to 1.7 | not read | UNSURE | IEC 60228 paywalled. From the sigma inputs: 5.80/3.54 = 1.64 |
| A3 | e: primary Al 150 to 220; secondary Al 10 to 30; primary Cu 35 to 75; secondary Cu 10 to 20 (MJ/kg) | as stated | ICE: 218 / 29.0 / 57.0 / 16.5. Nuss: 194 (131 mix) / 8.3 and 23.8 / 53.7 (45 to 88 by route) / 28.1 | ICE inside all four. Nuss: Al primary inside; secondary Al new scrap 8.3 outside (below 10), old scrap inside; Cu primary inside (88 on the Au-Ag route outside); secondary Cu 28.1 outside | ICE v2.0 Summary Tables; Nuss S1 Table S38 |
| C4 | Air 300 K | see Part 1 row 11 | as there | rho outside 1% (-1.3%), rest inside | Incropera scan |
| D2 | sigma_ion of 30 wt% KOH at 80 C, 120 to 150 S/m | as stated | not read | UNSURE | Gilliam et al. 2007 not retrieved |
| D3 | CED Pt 1e5 to 3e5 MJ/kg; Ir same order | as stated | Pt 3.08e5 (ZA), 3.27e5 (RU); Ir 1.65e5, 1.75e5 | Pt outside (above 3e5); Ir inside | Nuss S1 Table S38 |
| F1 | mu/rho (cm2/g) at 0.1, 0.5, 1, 5 MeV | C 0.148-0.155, 0.086-0.088, 0.063-0.064, 0.0265-0.0275; W 4.3-4.6, 0.135-0.141, 0.065-0.067, 0.040-0.042 | C 0.1514, 0.08715, 0.06361, 0.02708; W 4.438, 0.1378, 0.06618, 0.04103 | all 8 inside | NIST element tables z06, z74 (with coherent scattering) |
| F1 | W/C ratios 29, 1.6, 1.04, 1.5 | as stated | 29.31, 1.581, 1.040, 1.515 | inside | same |
| F1 | Klein-Nishina check, 2% | sigma_KN(1 MeV) 0.2112 b; C 0.0635 | 0.21121 b; mu/rho 0.06354 (table incoherent 0.06358; total w/o coherent 0.06358) at 1 MeV; 0.08699 at 0.5 MeV (table 0.08699) | inside (0.07% and 0.0%) | `xcom_fit.py` |
| F2 | Interval where W/C < 2 | about 0.4 and about 6 MeV | lower crossing 0.403 MeV; upper crossing 7.56 MeV (log-log interpolation, 4 000-point grid on the NIST rows) | lower inside; upper outside the planner's +/-10% (7.56 vs 6, +26%) | `parse_nist.py` |
| F2 | Minimum of W/C | 0.98 to 1.05 at 1.5 to 2 MeV | 0.965 at 1.50 MeV | outside (below 0.98) | same. The grid minimum falls on a table point (1.5 MeV) |
| F2 | W/C at 10 MeV | 2.2 to 2.6 | 2.42 | inside | same |
| F3 | Thickness-basis minimum | about 8.5 (2.26) and about 11 (1.70); never below 7 | 8.24 (rho_C 2.26) and 10.96 (1.70), both at 1.5 MeV | inside (8.24 is 3% below 8.5, within the row's 5%) | `parse_nist.py`, rho_W 19.3 |
| F4 | Z exponent per mass at 100 keV | 2.8 to 3.6 | 3.25 (all seven elements); 3.04 without C | inside | XCOM partial photoelectric (`xcom_fit.py`) |
| F4 | Energy exponent of W photoelectric 0.1 to 0.5 MeV | -2.6 to -3.1 | -2.645 (log-log fit of six points); -2.637 from the end points | inside, near the edge | same |
| F4 | Carbon Compton fraction at 100 keV | >= 0.85 | incoherent/total (with coherent) = 0.968 | inside | same |
| F6 | ANS-6.4.3 buildup comparison; x_C/x_W at 1 MeV 1.1 to 1.4 | as stated | not read | UNSURE | standard paywalled |
| F7 | 60 keV: Sn 6 to 7, Pb 4.8 to 5.2, W 3.6 to 3.8 | as stated | Sn 6.564, Pb 5.021, W 3.713 | inside | NIST tables (interpolated, 60 keV is a grid point or between points; below all three edges except Sn) |
| F7 | 80 keV: W 7.6 to 8.0, Sn 2.9 to 3.2, Pb 2.3 to 2.5 | as stated | W 7.81, Sn 3.029, Pb 2.419 | inside | same |
| F7 | 100 keV: Pb 5.4 to 5.7, W 4.3 to 4.6, Sn 1.6 to 1.8 | as stated | Pb 5.549, W 4.438, Sn 1.676 | inside | same |
| F7 | Ranking in G3.5 | Sn > Pb > W at 60; W > Sn > Pb at 80; Pb > W > Sn at 100 | same orderings. Extra: Gd 11.75 leads at 60 keV; at 80 keV Gd 5.57 is second after W 7.81 and Ba 3.96, Sn 3.03, Pb 2.42 | holds for the three-element ranking. G3.5 as worded (three elements) holds; with Gd included, Gd leads at 60 keV | same |
| N1 | B-10 3 835 to 3 845 | as stated | 3 835 (Sears) | inside | Sears 1992 |
| N1 | nat B 760 to 770 | | 767 (8) | inside | Sears |
| N1 | C 0.0034 to 0.0039 | | 0.0035 (Sears), 3.53 mb for C-12 (INDC-440) | inside | both |
| N1 | Al 0.230 to 0.233 | | 0.231 (Sears), 231 mb (INDC-440) | inside | both |
| N1 | H 0.332 to 0.333 | | 0.3326 | inside | both |
| N1 | Cd-113 19 900 to 20 700 | | 20 600 (400) | inside | both |
| N1 | nat Cd 2 450 to 2 530 | | 2 520 (50) | inside | both |
| N1 | Gd-157 253 000 to 255 000 | | 254 000 (815) in INDC-440; 259 000 (700) in Sears 1992 | inside with INDC-440; outside with Sears (the two sources differ by 2%). The row says Sears is the cross-check | both |
| N1 | Gd-155 60 300 to 61 100 | | 60 900 (500) INDC-440; 61 100 (400) Sears | inside (Sears at the upper edge) | both |
| N1 | nat Gd 48 800 to 49 700 | | 48 890 (104) INDC-440; 49 700 (125) Sears | inside (Sears at the edge) | both |
| N1 | Hf 104 to 106 | | 104.1 | inside | both |
| N1 | In 193 to 194 | | 193.8 | inside | both |
| N1 | Ag 63 to 64 | | 63.3 | inside | both |
| N1 | Li-6 938 to 941 | | 940 (4) | inside | Sears (INDC-440 does not list the (n,alpha) channel) |
| N1 | Dy 940 to 1 000 | | 994 (13) Sears; 943 (15) INDC-440 | inside | both |
| N1 | Eu 4 500 to 4 600 | | 4 530 (40) Sears; 4 565 (100) INDC-440 | inside | both |
| N1 | Sm 5 600 to 5 950 | | 5 922 (56) Sears; 5 670 (100) INDC-440 | inside | both |
| N1 | Isotopic checks, 3% | nat B 0.199 x sigma(B-10); nat Cd 0.1222 x sigma(Cd-113); nat Gd | 763 vs 767 (0.5%); 2 517 vs 2 520 (0.1%); Sears-based 49 576 vs 49 700 (0.25%) | inside | `derived_checks.py` |
| N2 | RI(B-10) 1 720 to 1 730 b | as stated | not found. INDC-440 gives only (n,gamma) RI (B-10 capture listing 0.22 b). No source found for 1 722 | UNSURE | |
| N2 | RI Cd 50 to 100 b (nat) | as stated | Cd-113 RI 390 +/- 40 b (capture); no nat Cd RI line in the file | UNSURE. Cd-113 RI 390 is not a test of the natural-Cd range, which is lower because of the abundance | INDC-440 |
| N2 | RI Gd 380 to 410 b | | nat Gd 390 +/- 10 | inside | INDC-440 |
| N2 | RI Hf 1 900 to 2 000 | | 1 992 +/- 50 | inside | INDC-440 |
| N2 | RI In 3 100 to 3 300 | | 3 167 +/- 100 (In-000); In-115 3 300 | inside | INDC-440 |
| N2 | RI Ag 740 to 770 | | In-isotope lines: Ag-107 100 +/- 48, Ag-109 1 400 +/- 48; abundance-weighted 726 (K, 51.84/48.16) | outside (about -2% to -6%) by this method; the file lacks an Ag-000 RI line, so UNSURE | INDC-440, `derived_checks.py` |
| N3 | Sigma_a Cd 117, B4C 84, Gd 1 480, steel 3.3 | as stated | 116.8, 84.3, 1 504, 3.33 | inside (Gd +1.6%) | `derived_checks.py` |
| N4 | Textbook collisions | 18, 25, 115 | 18.2, 25.1, 115.3 (K) | inside +/-1 | K. Lamarsh not read |
| N5 | L water | 2.7 to 2.9 | 2.73 to 2.85 | inside | search snippets |
| N6 | Crustal abundance | list in the plan | identical | inside | Wikipedia mirror of CRC 85th ed. |
| N6 | Annual production (USGS) | not stated | not read | UNSURE | |
| H1 | Li/SOCl2 about 1 470 Wh/kg | 2% | 1 473 (K); secondary page 1 470 | inside | |
| H2 | SSA 2 630 +/- 10; C_sp about 550 | | 2 627 m2/g; 552 F/g | inside | K |
| H3 | Ranges | | not read | UNSURE | |
| M1 | mu0 Ms and ceilings | Nd2Fe14B 1.61; ceiling 512; Ba ferrite ceiling 45 | 1.61 T (S); 515.7 and 45.8 kJ/m3 (K) | inside +/-2% | |
| M2 | K1 SmCo5 17.2; Fe, Co, Nd2Fe14B, Ba ferrite | | SmCo5 17.2 (S); the rest not read | one inside; others UNSURE | |
| M3 | Skomski et al. 2010 statement of mu0 Ms^2/12 | | not read | UNSURE | |
| P1 | Water at 60 C: rho 983, sigma 0.066, h_fg 2.36e6, mu 4.7e-4 | | not read | UNSURE | Incropera A.6 not retrieved |
| T1 | ITO | | not read | UNSURE | |

## Part 3: citation list

Verdicts: V = verified (record and details correct); N = not found; X = exists but may not say this; U = UNSURE. "Open data" notes apply to datasets.

| # | Entry | Verdict | Note |
|---|---|---|---|
| 1 | Hubbell and Seltzer 1995, NISTIR 5632 | V (data), U (printed Table 3 numbering) | The NIST element pages (`ElemTab/z*.html`) carry a link "Back to table 3", consistent with "Table 3". Open on the web, gave all F1, F2, F7 numbers. The NIST site's current version label (1.4, 2004) was not read |
| 2 | Berger, Hubbell, Seltzer et al., XCOM; NBSIR 87-3597 | V (database) | XCOM exists and returned partial cross sections (coherent, incoherent, photoelectric, nuclear pair, electron pair, total with and without coherent). Open, one element per web request; no bulk file or licence statement seen. NBSIR number not independently checked: U |
| 3 | Klein and Nishina 1929 | V | Crossref: Z. Phys. 52 (11-12), 853-868, DOI 10.1007/bf01366453. Equation number U; the planner's closed formula reproduced tabulated Compton values to 0.07% (Part 2b) |
| 4 | Attix 1986 | U | Book (Wiley, 1986) exists per checker memory; no source read. Chapter and equation number U |
| 5 | ANSI/ANS-6.4.3-1991 | X | Exists (ANSI store: historical; data 0.015 to 15 MeV, to 40 mfp). Authors Trubey, Eisenhauer, Foderaro, Gopinath, Harima, Hubbell, Shure, Su (NIST record). Tungsten appears covered (a paper compares tungsten buildup with the standard). Carbon not confirmed; whether the standard tabulates both C and W is U. Paywalled. Table numbers U. The plan's F6 check (iv) cannot rely on it without that confirmation |
| 6 | Shultis and Faw 2000 | U | Book not read; reissue by ANS in 2000 per checker memory. Appendix letter U |
| 7 | Jensen 1906 | V | Crossref: Acta Math. 30, 175-193, DOI 10.1007/bf02418571 |
| 8 | Mughabghab 2006, Atlas, 5th ed. | V | Elsevier, April 2006, 1 372 pp. RI basis: 0.5 eV to the top of the resolved region (EXFOR note). Paywalled |
| 9 | Mughabghab 2003, INDC(NDS)-440 | V | Report exists, February 2003, BNL, IAEA contract 11376/USA. Open PDF at OSTI. Capture channel only; it does not give the (n,alpha) data of B-10 or Li-6, so for rows N1 and N2 it covers Cd, Gd, Hf, In, Ag, Sm, Eu, Dy but not B-10 |
| 10 | Sears 1992 | V | Crossref: Neutron News 3(3), 26-37, DOI 10.1080/10448639208218770. NCNR page says pp. 29-37 for the table. Table 1 numbering U. Open at NCNR |
| 11 | Brown et al. 2018, ENDF/B-VIII.0 | V | Nucl. Data Sheets 148, 1-142, DOI 10.1016/j.nds.2018.02.001. Open full text. Library download not fetched |
| 12 | Iwamoto et al. 2023, JENDL-5 | V | J. Nucl. Sci. Technol. 60(1), 1-60, DOI 10.1080/00223131.2022.2141903 (one aggregator lists issue 4; most list issue 1) |
| 13 | Lamarsh and Baratta 2001 | U | Book, 3rd ed. 2001 exists per checker memory. A code port of its exercises uses a water thermal diffusion area 8.1 cm2 "from Tables 5.2 and 5.3", consistent with "Table 5.2" for diffusion parameters. Slowing-down table number U |
| 14 | Bell and Glasstone 1970 | U | Book exists per checker memory (Van Nostrand Reinhold, 1970). Section for E3 U |
| 15 | Dowell 1966 | V | Crossref: Proc. IEE 113(8), 1387 (end page 1394 not shown in the record), DOI 10.1049/piee.1966.0236. Equation number U |
| 16 | Thomson (Kelvin) 1881 | V | Report of the British Association, 51st meeting (York, Aug and Sep 1881), Sec. A, pp. 526-528, per Thomson's Mathematical and Physical Papers vol. 5; also Lum. Elec. 5 (12 Oct 1881) 65-66; Nature 24, 489-492 gives a summary. Some bibliographies date the volume 1882 |
| 17 | IEC 60028, 1925 | U | The value 58.0 MS/m at 20 C is the IACS definition (found via secondary pages); the standard number was not independently checked. Withdrawn, paywalled |
| 18 | IEC 60228 | U | Not read. Edition year (2004) not checked. Paywalled |
| 19 | Incropera et al. 2007, 6th ed. | V for Table A.4 values (via a scan), U for the rest | A.4 at 300 K matches (Part 1 row 11). Table 8.1 (Nu = 7.54) and A.6 not seen. Paywalled |
| 20 | Schmidt 1926 | V | Z. VDI 70, Heft 26 pp. 885-889 and Heft 28 pp. 947-951 (Springer chapter listing; other papers write 885-947). Optimum fin attributed to Schmidt by later papers; beta = 1.4192 not seen in the results |
| 21 | Kraus, Aziz, Welty 2001 | U | Book exists per checker memory. beta = 1.4192 and chapter not verified |
| 22 | Bejan 1996 | U | Book exists per checker memory. Chapter U |
| 23 | Murray 1926 | V | Crossref: PNAS 12(3), 207-214, DOI 10.1073/pnas.12.3.207. The record title is "The Physiological Principle of Minimum Work"; the subtitle "I. The vascular system..." was not in the record |
| 24 | Hashin and Shtrikman 1962 | V | Crossref: J. Appl. Phys. 33(10), 3125-3131, DOI 10.1063/1.1728579. The title is about magnetic permeability. The theorem applies to conductivity by analogy; equation number U |
| 25 | Newman and Tobias 1962 | V | Crossref: J. Electrochem. Soc. 109(12), 1183, DOI 10.1149/1.2425269. End page 1191 not shown |
| 26 | de Levie 1963 | V | Crossref: Electrochim. Acta 8(10), 751-780, DOI 10.1016/0013-4686(63)80042-0 |
| 27 | Trasatti 1972 | V (record), U (table or figure) | Crossref: J. Electroanal. Chem. 39(1), 163-184, DOI 10.1016/s0022-0728(72)80485-6. The record title is shortened; a 1971 paper with the same short title is vol. 33, 351-378. Whether exchange currents are in a table or only in the volcano figure is U |
| 28 | Sheng, Gasteiger, Shao-Horn 2010 | V | Crossref: J. Electrochem. Soc. 157(11), B1529, DOI 10.1149/1.3483106 |
| 29 | McCrory et al. 2013 | V | Crossref: J. Am. Chem. Soc. 135(45), 16977-16987, DOI 10.1021/ja407115p. Table numbers U |
| 30 | Gilliam et al. 2007 | V | Crossref: Int. J. Hydrogen Energy 32(3), 359-364, DOI 10.1016/j.ijhydene.2006.10.062. The correlation values were not read |
| 31 | Pourbaix 1974 | U | Book exists per checker memory. Not read |
| 32 | Nuss and Eckelman 2014 | V | PLoS ONE 9(7), e101298, CC BY 4.0. Correction: the per-kg CED table is S1 Table S38 (supporting Word file `journal.pone.0101298.s001`), column "CED [MJ/kg]". The main text has Fig. 3A as a figure and Table 1 (global totals) |
| 33 | Hammond and Jones 2011 | V | ICE v2.0, Summary Tables (8 pages) read. Aluminium virgin 218, recycled 29.0; copper virgin 57.0, recycled 16.5, general 42.0. Open copy without a stated licence. A v3.0 exists per checker memory: U |
| 34 | Ashby 2011 | U | Book exists per checker memory. Chapters U |
| 35 | Coey 2011 | V | Crossref: IEEE Trans. Magn. 47(12), 4671-4681, DOI 10.1109/tmag.2011.2166975. Table number U; a lecture source quotes Nd2Fe14B mu0 Ms = 1.61 T from it |
| 36 | Coey 2010 | U | Book exists per checker memory. Not read |
| 37 | Skomski and Coey 2016 | V (record), X (definition of kappa) | Crossref: Scripta Mater. 112, 3-8, DOI 10.1016/j.scriptamat.2015.09.021. Search snippets define kappa = K1/(mu0 Ms^2), with kappa > 1 as the rule; other papers cite the square-root form. The plan uses the square root; which form the paper's Table 1 prints is U. The planner's published kappa_h list could not be checked |
| 38 | Skomski and Coey 1993 | V (record), U (content) | Crossref: Phys. Rev. B 48(21), 15812-15816, DOI 10.1103/physrevb.48.15812. 1 090 kJ/m3, Sm2Fe17N3 and equation numbers not seen |
| 39 | Kneller and Hawig 1991 | V | Crossref: IEEE Trans. Magn. 27(4), 3588-3600, DOI 10.1109/20.102931 |
| 40 | Stoner and Wohlfarth 1948 | V | Crossref: Phil. Trans. R. Soc. A 240(826), 599-642, DOI 10.1098/rsta.1948.0007. (An IEEE Trans. Magn. 1991 reprint exists, DOI 10.1109/tmag.1991.1183750, pp. 3475-3518.) |
| 41 | Skomski et al. 2010 | V (record), U (content) | Crossref: J. Appl. Phys. 107(9), DOI 10.1063/1.3337657, title as in the plan. Whether it states a mu0 Ms^2/12 limit was not seen: U. If it does not, the plan's own derivation (D9) stands alone |
| 42 | Xia et al. 2009 | V (record), X (cited numbers) | Nature Nanotechnol. 4(8), 505-509, DOI 10.1038/nnano.2009.177. The abstract concerns quantum capacitance with a minimum at the Dirac point; it does not mention 21 uF/cm2 or 550 F/g. The "550 F/g" is likely a later derived figure for graphene (derived here from 21 uF/cm2 x geometric SSA = 552 F/g). Whether 21 uF/cm2 is stated in the paper's text is U |
| 43 | Linden and Reddy 2002 | U | Book, 3rd ed. 2001 or 2002 (check): the search results cite "3rd ed. (2001)" in patents. Table 1.2 not read. 1 470 Wh/kg for Li/SOCl2 was found in a secondary page (a patsnap article), and equals the stoichiometric value |
| 44 | Christen and Carlen 2000 | V | Crossref: J. Power Sources 91(2), 210-216, DOI 10.1016/s0378-7753(00)00474-2 |
| 45 | Augustyn, Simon, Dunn 2014 | V | Crossref: Energy Environ. Sci. 7(5), 1597-1614, DOI 10.1039/c3ee44164d |
| 46 | Haacke 1976 | V | Crossref: J. Appl. Phys. 47(9), 4086-4089, DOI 10.1063/1.323240 |
| 47 | Ellmer 2012 | V | Crossref: Nature Photonics 6(12), 809-817, DOI 10.1038/nphoton.2012.282. Values not read |
| 48 | Reay, Kew, McGlen 2014 | U | Book exists per checker memory. Not read |
| 49 | Haynes (ed.) 2016, CRC 97th | U | Edition per checker memory. The N6 numbers were read from a mirror of the 85th ed., not the 97th |
| 50 | USGS Mineral Commodity Summaries | U | Exists (annual, US Government, open). Not queried |

Counts for Part 3 (50 entries): verified 28 (1-3, 7-12, 15, 16, 20, 23-26, 28-30, 32, 33, 35, 39, 40, 44-47); verified as a record but content not seen 3 (27, 38, 41); verified record and the cited content doubtful 2 (37, 42); exists but may not say this 1 (5); partly verified 1 (19); UNSURE 15 (4, 6, 13, 14, 17, 18, 21, 22, 31, 34, 36, 43, 48, 49, 50); not found 0.

## Part 4: candidates (not evidence)

- ICE v2.0 Summary Tables and Nuss and Eckelman S1 Table S38 are both open and have per-kg values for the same metals (Al, Cu, Pt, Ir, Sn, Pb, Nd, Gd, Dy, Eu, Sm, W, Hf, Ag, In, Cd and others), with 95% intervals. Table S38 carries primary and secondary rows. For row A3 and D3, the Nuss table is the better single source because it has uncertainty ranges and an open licence (CC BY 4.0).
- INDC(NDS)-440 (open OSTI PDF) replaces the paywalled Atlas for the capture channel of Cd, Gd, Hf, In, Ag, Sm, Eu, Dy. For the (n,alpha) elements B-10 and Li-6, ENDF/B-VIII.0 or the Sears table are the open alternatives; resonance integrals for those would need the NNDC (not tried).
- NIST XrayMassCoef element pages (open) give mu/rho and mu_en/rho for all F-rows; XCOM gives partial cross sections for F4 and F6 without needing ANSI/ANS-6.4.3.
- For ANS-6.4.3 buildup factors: the UNLV theses (found by search) describe updates to the standard and its coverage; also ORNL RSICC DLC-129 (geometric-progression coefficients derived from the standard) is open and could replace the paywalled standard. Not read.
- The LLNL "Hand Calculation Methods for Nuclear Criticality Safety" (Table 2-2) gives thermal diffusion lengths (H2O 2.85 cm) in an open document; DeJuren and Rosenwasser (J. Res. NBS 51, 203, open at nvlpubs.nist.gov) measured L = 2.77 +/- 0.04 cm. Both are open substitutes for the Lamarsh table in row N5.
- For Kelvin's law, the collected papers (Thomson, Mathematical and Physical Papers, vol. 5) are digitised at quod.lib.umich.edu (found by search).
- For Skomski and Coey 1993, Trinity College's repository (TARA) hosts a PDF, but it returned a challenge page here.

## Summary

- Part 1 (38 rows): confirmed 21, differs 1 clean (e_Pt) plus differences inside three confirmed rows (e_Al central 200 against 218 and 194; air density 1.177 against 1.1614; secondary Cu with Nuss 28.1 against range 10 to 20), UNSURE 16 (no primary source read).
- Part 2: every F1 and F7 value is inside the planner's range. Outside or at the edge: F2 upper crossing 7.56 MeV (planner about 6), F2 minimum 0.965 (planner 0.98 to 1.05), N1 Gd-157 under Sears (259 000, planner 253 000 to 255 000; INDC-440 254 000 is inside), D3 Pt CED 3.08e5 and 3.27e5 (planner up to 3e5), N2 Ag RI by isotope weighting 726 (planner 740 to 770), A3 secondary Al new scrap 8.3 (planner 10 to 30). Not checkable: IEC table, Gilliam, ANS buildup, Skomski, Ellmer, Reay, USGS production, B-10 RI.
- Part 3 (50 entries): 28 verified, 3 record verified and content not seen, 2 record verified and cited content doubtful (37, 42), 1 exists but may not say this (5), 1 partly verified (19), 15 UNSURE (books and standards not read), 0 not found.
- Needing attention first: (1) e_Pt for row D3 (+28%); (2) F2 crossings and minimum, since G3.2 quotes "0.4 to 6 MeV" and "near 1.0"; the table gives 0.40 to 7.6 MeV and a minimum of 0.965; (3) the 1 090 kJ/m3 and mu0 Ms^2/12 statements (Skomski 1993, 2010), neither seen; (4) the Xia 21 uF/cm2 attribution; (5) whether ANS-6.4.3 contains carbon; (6) the B-10 resonance integral (no source found).
