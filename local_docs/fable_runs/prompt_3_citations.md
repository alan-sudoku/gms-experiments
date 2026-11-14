# Prompt 3, S3 citation check

Context file (`local_docs/`, never cited by the spec). Every statement is a claim at level `derived` (unverified). Method: web search snippets and abstract pages only. No full text was opened, no PDF was downloaded, no WebFetch was used. All numbers below are what a snippet reported; none was checked against a paper's own tables. arxiv.org, exergoecology.com and api.crossref.org were not tried; nothing here depends on them. Only titles, authors and technical terms were searched.

Coverage: second pass done. Every one of the 65 entries and the previously unsearched inputs now has at least one search, at snippet or abstract level only. Where a search returned only citing papers (no abstract) the row says so.

## (a) Inputs table

Status words: confirmed (inside the reported range and basis matches), in range (planner value lies inside what is reported but the basis differs or is unclear), out of range, unverified.

| Input | Planner value | Found value or range, with basis | Source | Status |
|---|---|---|---|---|
| σ_w7 as-built surface, amplitude, 1e7 | 60 MPa (40 to 100) | No source found that gives a rough as-built fatigue strength at 1e7 on an amplitude basis. Reported: machined and polished L-PBF AlSi10Mg, Sf = 125 MPa at 1e7 (Nicoletto-type study, snippet, stress ratio not stated); a JMST 2020 study 130 MPa at 1e7 for machined SLM material; "as-built with no machining can be used safely below 70 MPa" (snippet, source not identified, basis unclear); EOS sheet 110 MPa at 2e7, fully reversed, turned and machined samples (older sheet: 97 ± 7 MPa, Z). Aboulkhair 2016: as-built samples (Ra 17.1 µm) did not reach 3e7 cycles at any maximum stress range from 63 to 220 MPa; if that range is a stress range at R = 0.1 (basis not confirmed), the amplitude is at most about 31 MPa, which is below the planner's 40 MPa lower bound. | Aboulkhair 2016 record; EOS data sheet; snippets above | UNSURE. 60 is plausible but not confirmed. The lower bound of 40 may be too high for rough as-built material. S2 should add 30 MPa to the sweep. |
| σ_w7 machined, amplitude | 135 MPa (90 to 150) | 125 to 130 MPa (above); EOS 110 MPa at 2e7. 135 is 4 to 8 % above the two 1e7 values and 23 % above the EOS value. | as above | In range (at the upper end). Basis: the 135 is derived from the uniform material law, not measured. |
| As-built to machined ratio | 0.4 to 0.6 Ti, 0.5 to 0.8 AlSi10Mg (FROM MEMORY) | 70/125 = 0.56 from the two snippets above (different studies). Roughness gave 60 to 80 % lower life than machined in a 2024 L-PBF AlSi10Mg study (snippet; this is a life ratio, not a strength ratio). Ti-6Al-4V ratio not searched. | snippets | In range for AlSi10Mg (weak); Ti unverified |
| σ_y (LPBF AlSi10Mg) | 250 MPa (200 to 280) | EOS current sheet, as built: Rp0.2 270 MPa (XY), 233 MPa (Z), via a Forge Labs summary of the EOS sheet. Older EOS sheet about 250 MPa XY. A review snippet: 210 to 240 MPa. | EOS data sheet, Forge Labs summary, review snippet | Confirmed (inside range; orientation dependent) |
| σ_u | 400 MPa (330 to 460) | EOS: 461 MPa (XY), 466 MPa (Z). Review snippet: 400 to 450 MPa. | as above | In range, at the low end. 430 to 460 is the more common as-built value; this raises σ_f' = 1.67·σ_u to 720 to 770 MPa and the machined σ_w7 to 146 to 156 MPa. |
| E_s | 70 GPa (65 to 75) | EOS: 75 GPa (XY), 70 GPa (Z) | EOS data sheet (Forge Labs summary) | Confirmed |
| ρ_s | 2670 | Modelling papers use 2670 to 2680 kg/m³ | snippets | Confirmed |
| α_s | 21e-6 /K (20 to 23e-6) | Dilatometry study (OSTI report): 22.8e-6 /K in-plane (XY), 26.6e-6 /K out-of-plane (Z) as built; isotropic after stress relief. Temperature range not given in the snippet. | OSTI thermal characterisation report | In range for XY; Z (26.6e-6) is outside the planner's 20 to 23e-6 range. Add 27e-6 to the sweep. |
| k | 130 W/(m·K) (100 to 170) | A simulation paper uses 100 W/(m·K); conductivity is 10 to 20 % anisotropic and rises 15 to 18 % with density and with heat treatment. No measured table value retrieved. | PMC and ScienceDirect snippets | UNSURE (value not found; 100 to 170 plausible) |
| c_p | 900 J/(kg·K) | One source cites 739 J/(kg·K) at 20 °C and 922 at 400 °C (Li and Gu, via a snippet); another simulation uses 1140. The 739 at room temperature looks low for an Al alloy and may be a snippet error. | snippets | UNSURE (conflicting); it enters only the melt floor of D9 |
| ν_s, h_f, T_liq | 0.33, 397 kJ/kg, 873 K | not found in these searches | none | UNSURE (not found) |
| σ_f' = 1.67·σ_u, b = −0.095 (uniform material law, Al and Ti alloys) | 668 MPa, −0.095 | The constants are reported as σ_f' = 1.67·σ_u and b = −0.095 for aluminium and titanium alloys in the Bäumel and Seeger law (secondary sources: a ScienceDirect topic page and a Ti2AlNb paper's table, which also lists ε_f' = 0.35, c = −0.69). The law is an estimate from tensile strength for wrought alloys. A critique exists (Blackmore 2009, Eng. Integr.; not opened). No source found that applies it to LPBF AlSi10Mg. Check: 668·(2e7)^−0.095 = 135 MPa, close to the 125 to 130 measured on machined L-PBF specimens. That agreement is one data point. | Bäumel and Seeger 1990 (record only); secondary sources | Confirmed as the stated constants of the law; applicability to LPBF AlSi10Mg unverified |
| b as-built = −0.1434 | derived | not in any source; follows from the planner's σ_w7 = 60 | none | derived only |
| Gibson–Ashby C1 = 1 | 1 | "C1 about 1.0" for modulus of open-cell metallic foams (snippet) | secondary snippets | Confirmed (secondary) |
| Gibson–Ashby C_pl = 0.3 | 0.3 | σ_pl/σ_ys = 0.3·(ρ/ρ_s)^(3/2) for open cells (snippets, Ashby 2006 and a Wiley chapter) | secondary snippets | Confirmed (secondary) |
| Gibson–Ashby buckling 0.05 | 0.05 | σ_el ≈ 0.05·E·(ρ/ρ_s)^2, stated in Ashby 2006 as the more refined constant (snippet) | Ashby 2006 (eclass copy) | Confirmed (secondary) |
| Octet E = ρ̄E_s/9, yield ρ̄σ_y/3 (Deshpande 2001) | derived in D2 | abstract confirms analytical expressions for the three cubic moduli but not these values; the planner derived them | Deshpande 2001 abstract | Unverified (values not in abstract) |
| BCC closed forms E* = (√3π/2)·E_s·(d/L)^4 and σ_pl = (4√2/3)·σ_y·(d/L)^3, attributed to Ushijima 2011 | derived in D3 | The paper exists and presents an analytical model for E* and σ_pl of BCC micro-lattices under compression, with FE for BCC and BCCZ. Its exact formulas were not seen. A later paper says the Ushijima model includes only axial and bending effects and errs by up to 42 % as aspect ratio increases. Hence an attribution of exactly these closed forms is not confirmed, and applicability at l/d about 4.5 (ρ̄ = 0.2) is doubtful. | Semantic Scholar and ResearchGate records | Unverified (attribution); caution on applicability |
| Normalised endurance ratio, lattices | 0.15 to 0.25 (Hrabe), about 0.2 (Amin Yavari 2013), up to 0.6 (Bobbert 2017) | Hrabe 2011: 0.15 to 0.25 at 1e6, R = 0.1, 15 Hz, EBM Ti-6Al-4V, ρ̄ 0.17 to 0.40 (the abstract calls it "normalized fatigue strength"; that it is σ_max over yield was not confirmed). Amin Yavari 2013: normalised endurance limit below 0.2 for all four SLM structures (68 to 84 % porosity), solid about 0.4, power law R² = 0.94. Amin Yavari 2015: other AM porous materials about 0.2 of yield or plateau; a snippet reports up to 0.6 for some structures (the same sentence is in Bobbert 2017's abstract, so the attribution is doubtful); cube cells did not fail at 1e6 at 80 % of yield. An MSEC paper on porous Ti-6Al-4V reports 0.5 to 0.55 at 1e6. A snippet reports annealed EBM meshes at about 0.5. | Hrabe 2011; Amin Yavari 2013, 2015; Bobbert 2017; MSEC 2016 (record seen, not in the citation list) | Partly confirmed. The 0.6 is in Bobbert 2017's abstract, as the planner said (TPMS; stress basis not seen). The literature spread is 0.15 to 0.6, wider than the planner's 0.14 to 0.24. |
| Stress basis of those ratios | σ_max at R = 0.1 (planner says "usually") | Hrabe 2011 used R = 0.1; Aboulkhair uses stress range; Lietaert 2018 used R = 0.1, −1 and 10. | records | In range of the planner's statement. At R = 0.1, σ_a = 0.45·σ_max, so 0.2·σ_y at σ_max is 0.09·σ_y as an amplitude, below the planner's 0.14 to 0.16 amplitude prediction by a factor of about 1.6. Inside the factor of 3 that R27 allows. |
| Fatigue fracture entropy Al 6061-T6 | 4 MJ/(m³·K) | About 4 MJ/(m³·K) (Naderi 2010); 4.07 average for bending fatigue (Amiri and Khonsari 2012, as cited in snippet); about 60 for 304L. Stated as independent of amplitude, frequency, geometry. | LSU repository snippet, ResearchGate | Confirmed (secondary snippet). Defined from low-cycle tests; C13 already says so. |
| Lazan exponent n_d | 2 (sweep 2 to 3) | n between 2 and 4, 2.3 "generally used" (secondary snippet). No aluminium J or n found. | PMC and IOP snippets | In range of the sweep |
| ψ = 5e-3 for Al alloys | prompt | Loss factors: pure Al 2e-5 to 2e-3, dural 4e-4 to 1e-3 (secondary snippet). Check the convention: if these are loss factors η, then ψ = 2π·η gives 2.5e-3 to 6e-3 for dural. Whether the prompt's ψ is η or 2π·η is not stated anywhere I read. | secondary snippet | UNSURE (convention) |
| NASA fatigue knock-down for as-built surface | none assumed | A conference slide on NASA-STD-6030 lists cyclic stress limits of 80 % of the fatigue limit for improved surfaces and 60 % for as-built surfaces in HCF (secondary; not opened in the standard). | NASA TRISMAC 2021 slide (NTRS) | Candidate; see (c) |
| LPBF specific energy | 50 to 500 MJ/kg | Reported 55 to 569 MJ/kg across studies; machine-level 300 to 500 MJ/kg for Al; industrial SLM500 jobs 41 to 56 kWh/kg (148 to 200 MJ/kg); one nominal figure about 600 MJ/kg; Kellens benchmark 80 to 140 kWh/kg. An outlier gate-to-gate study gives 0.44 to 1.95 kWh/kg (1.6 to 7 MJ/kg), probably a narrower boundary. Faludi 2017: electricity dominates per-part impact. | LCA snippets (ResearchGate, Springer, ScienceDirect) | In range (the upper end can exceed 500; extend to 600) |
| Primary Al embodied energy | 200 MJ/kg (150 to 220) | 150 to 210 MJ/kg typical; 157 MJ/kg European average; DoITPoMS bottom-up 260; CSIRO over 200; bulk AlSi10Mg embodied 189. | snippets | Confirmed |
| Ti-6Al-4V σ_y | 950 MPa | As-built LPBF yield 761 to 1119 MPa across studies, about 820 MPa vertical; post-heat-treated 960 to 970 MPa in one study. | snippets | In range (orientation and heat treatment dependent) |
| Ti-6Al-4V σ_w, as-built, 1e6 to 1e7 | 200 MPa (150 to 300) | Rough as-built 150 to 300 MPa; stress-relieved 190 MPa at 1e7; machined, polished or HIP-treated 450 to 600 MPa; HIP plus chemical etching about 450 MPa. Stress ratio often not stated. | snippets | In range |

Inputs flagged out of range: none is shown to be outside its swept range. One is at risk: σ_w7 (as-built) lower bound 40 MPa, see the first row. Inputs flagged for a changed central value: σ_u (400, typical 430 to 460).

## (b) Citation rows

Status: verified (exists, record or abstract plausibly supports the use); exists, may not say this; not found; UNSURE. "Verified" is title and abstract level only. Planner's equation and figure numbers were not checked.

| # | Entry | Status | Note |
|---|---|---|---|
| 1 | Hrabe 2011 | verified | Abstract: EBM Ti-6Al-4V, R = 0.1, 15 Hz, normalised strength 0.15 to 0.25 at 1e6, solid about 0.4. Normalisation basis not stated in snippet. |
| 2 | Li 2012 | exists, content not checked | Abstract snippet gives only the first sentence (mesh arrays, porosity 60 to 85 %, EBM). Ratcheting and the power law were not seen. |
| 3 | Amin Yavari 2013 | verified | Normalised S-N similar across four porosities; power law R^2 0.94; endurance limit below 0.2 (solid 0.4). |
| 4 | Amin Yavari 2015 | verified | Collapse within a cell type, not across (snippet). The sentence "some reached up to 60 % of yield" appeared in the snippet for this paper but is also the sentence in Bobbert 2017's abstract (see 12); the attribution to this paper is unreliable. |
| 5 | Zargarian 2016 | verified, with a caveat | Mater. Sci. Eng. C 60, 339 to 347. It is an FE simulation (failure-event algorithm), not an experiment; diamond, rhombic dodecahedron, truncated cuboctahedron, rho 0.1 to 0.3, compression. S-N follows a power law whose coefficient depends on rho, geometry and bulk fatigue properties, and whose exponent depends only on the bulk material. Fatigue strength proportional to modulus. Validated against literature data only. |
| 6 | Zhao 2016 | verified | Cell shape strongly affects fatigue; cyclic ratcheting dominates. |
| 7 | Van Hooreweder and Kruth 2017 | verified | Local stress method; CoCr and Ti-6Al-4V diamond cells only. |
| 8 | Van Hooreweder et al. 2017 | verified | Diamond cells, Ti6Al4V, 125 samples in 4 conditions including HIP plus chemical etching; local stress S-N approach; significant improvement. Numbers not seen. |
| 9 | Lietaert 2018 | verified | Diamond cells; R = 0.1, -1, 10. Tension-tension worse than compression-compression via local mean tensile stress. Supports C24. |
| 10 | de Krijger 2017 | verified | Diamond Ti-6Al-4V, R = 0.1, 0.3, 0.5, 0.7, 0.8. S-N shifts up as R rises; stress amplitude governs life; AM notches make life insensitive to mean stress; R behaviour differs from bulk. This cuts against applying a Goodman factor (C18, R25) to lattice struts; see S4 notes. |
| 11 | Ahmadi 2018 | verified | Co-Cr, three unit cells; normalised S-N depends more on material than topology; material effect up to 2-fold. |
| 12 | Bobbert 2017 | verified | Four TPMS types. Its abstract (PubMed 28213101) says other AM porous biomaterials have endurance limits of about 20 % of yield or plateau stress and some of these TPMS reached up to 60 %. So the planner's attribution of the 0.6 to Bobbert is right. Whether it is sheet-type is not stated in the snippet. Stress basis (R, max vs amplitude) not seen. |
| 13 | Benedetti 2021 | verified | Review; failure at nodes, roughness, lack of fusion (secondary summary). Normalisation by the solid's fatigue strength not seen. |
| 14 | Dallago 2018 | verified, with a caveat | Highlights: fatigue strength affected mainly by sharp notches; in fully reversed tests the advantage of stretching-dominated over bending-dominated structures was not found. The "local stress on as-built geometry" use is not shown in the snippet. The finding conflicts with C22's higher stretch-cell ratio (0.24 against 0.16); see S4 notes. |
| 15 | Dallago 2019 | verified | Int. J. Fatigue 124, 348 to 360; fully reversed fatigue of Ti-6Al-4V SLM cellular specimens; surface morphology, geometrical accuracy and defects. Imperfection as notch source plausible from the record. |
| 16 | Hedayati 2016 | verified | FE-based S-N prediction from unit cell type (abstract fragments). |
| 17 | Burr 2020 | exists, may not say this | Abstract: S-EBM lattices, cascading strut failure and a "grace period"; not a local approach from as-built strut data. EBM Ti-6Al-4V. |
| 18 | Zadpoor 2019 | verified | Review. |
| 19 | Boniotti 2019 | verified (record) | AlSi7Mg, not AlSi10Mg; defects and local irregularities control strut fatigue; strength equals local fatigue limit at hot spots. |
| 20 | AlSi10Mg lattice fatigue dataset | see (c) | |
| 21 | Brandl 2012 | verified | 91 samples, builds 0, 45, 90 degrees, T6 and platform heating; no 1e7 value retrieved. |
| 22 | Aboulkhair 2016 | verified | As-built did not reach 3e7 at max stress range 63 to 220 MPa; Ra 17.1 um. |
| 23 | Mower and Long 2016 | verified | As-fabricated SLM AlSi10Mg and DMLS Ti-6Al-4V fatigue strength significantly inferior to conventional; multiple cracks from surface defects, voids, microcracks. A truncated snippet puts SLM AlSi10Mg at about 60 % of a comparison material (which one is unknown). |
| 24 | Romano 2018 | verified | Defect-based modelling of HCF for L-PBF AlSi10Mg; competition between surface and internal defects in machined specimens. PDF on the Polimi repository. |
| 25 | Beretta and Romano 2017 | verified | AlSi10Mg and Ti-6Al-4V; defect-size sensitivity; Kitagawa-Takahashi at 5e6 cycles; AM behaves like traditional material in the presence of defects. |
| 26 | Uzan 2017 | exists, content not checked | Record seen only through citing papers (Mater. Sci. Eng. A 704, 229 to 237). A shot-peening follow-up reports a maximum fatigue limit of 110 MPa (secondary). |
| 27 | Tang and Pistorius 2017 | verified | Oxide-driven pores initiate fatigue cracks; life comparable to cast Al. |
| 28 | Yadollahi and Shamsaei 2017 | verified (record) | Review; process defects including roughness limit fatigue use (via citing papers; abstract not seen). |
| 29 | Pegues 2018 | verified | LPBF and EBM Ti-6Al-4V; roughness acts as micro-notches; roughness effect larger in smaller-diameter specimens (via a citing paper), which supports the thin-strut concern. |
| 30 | Persenot 2019 | verified (record) | As-built EBM Ti-6Al-4V thin parts, three orientations; found through citing papers. |
| 31 | Murakami 2002 | verified | Book exists; sqrt(area) model; chapter 5.8 summary. |
| 32 | Arola and Williams 2002 | verified | Roughness to effective stress concentration via Neuber and Arola-Ramulu; sinusoidal micro-notch model; 2 % error reported. Machined surfaces. |
| 33 | Kempen 2012 | verified (record) | Yield value not extracted; open PDF on lirias.kuleuven.be. |
| 34 | EOS data sheet | verified, conditions differ | Current: 110 MPa at 2e7, fully reversed, machined samples; older: 97 +/- 7 MPa (Z). |
| 35 | NASA-STD-6030 (2021) | verified (existence); no lattice knock-down found | See (c). |
| 36 | ISO 13314:2011 | verified | Title as given; compression test for porous and cellular metals with porosity 50 % or more; vendor guide says it is used for AM lattices. |
| 37 | Basquin 1910 | verified (bibliographic) | Proc. ASTM 10, 625 to 630 (some list part II). |
| 38 | Bäumel and Seeger 1990 | verified | Constants via secondary sources only. |
| 39 | Dowling 4th ed. | verified (existence) | Chapters include stress-based and strain-based fatigue and damping. Goodman, Morrow and notch-factor chapters not individually confirmed. Year given as 2012 or 2013. |
| 40 | Gibson and Ashby 1997 | verified through secondary sources | Constants from Ashby 2006 and a Wiley chapter, not the book. |
| 41 | Ashby 2006 | verified | Contains the 0.05 constant. E ≈ rho E_s/3 not checked. |
| 42 | Deshpande 2001 (octet) | verified (abstract) | Analytical and FE elastic properties and yield surfaces, elastic buckling approximated; stretching-dominated; analytical expressions for the three cubic moduli. The specific values E = rho E_s/9, G = rho E_s/12, yield rho sigma_y/3 are not in the abstract and were not checked. |
| 43 | Deshpande 2001 (foam topology) | verified | Node connectivity 6 (2D) and 12 (3D); at rho 0.1 stretching foam about 10x as stiff and 3x as strong as bending. |
| 44 | Ushijima 2011 | exists, may not say this | Real paper; analytical BCC E* and sigma_pl exist; exact forms not seen; later critique: up to 42 % error at larger aspect ratio. |
| 45 | Gümrük and Mines 2013 | exists, content not checked | 316L BCC SLM micro-lattice, 200 um struts; abstract not seen; "node effects" unconfirmed. |
| 46 | Leary 2016 | exists, content not checked | Highlights: parameters, manufacturability limits, failure modes (experiment and simulation) for AlSi12Mg lattices. Measured moduli against C1 not shown. |
| 47 | Maskery 2016 | verified | Uniform and graded density SLM Al-Si10-Mg lattices, quasi-static, energy absorption 5.7 to 6.3 MJ/m^3. The cell type is not stated in the snippet. |
| 48 | Al-Ketan 2018 | verified | Made from maraging steel; Kelvin, octet, Gibson-Ashby strut types; skeletal and sheet TPMS; sheet-TPMS near stretching-dominated, skeletal bending-dominated. Exponents not seen. Not aluminium. |
| 49 | Yan 2015 | verified | AlSi10Mg gyroid by DMLS, volume fraction 5 to 20 %, cell 3 to 7 mm; strength equation built on Gibson-Ashby for a 3 mm cell. Candidate for gyroid constants (planner's gap in section 6). |
| 50 | Timoshenko 1925 | verified | Bimetal strip theory; shear stresses local to ends within about the total thickness (from a citing patent). |
| 51 | Stoney 1909 | verified | |
| 52 | Suhir 1986 | verified | Normal stresses and interfacial shear and peel stresses under uniform heating or cooling. |
| 53 | Freund and Suresh 2003 | verified | Year 2003 (online) or 2004 (print) in different catalogues. Film stress and substrate curvature are in the contents. |
| 54 | Bogy 1971 | verified | J. Appl. Mech. 38(2), 377 to 386; singularity order depends on material mismatch and wedge angles. |
| 55 | Hutchinson and Suo | verified | Year is 1991 on Semantic Scholar and 1992 on other records. Volume 29, pp. 63 to 191. Interface mixed-mode criteria. The "debond force scales with compliant layer's modulus" use was not checked. |
| 56 | Lazan 1968 | exists, values not found | D = J sigma^n confirmed; n 2 to 4; no aluminium J or n. |
| 57 | Zhang, Perez, Lavernia 1993 | verified (record) | J. Mater. Sci. 28, 2395 to 2404; damping capacity compilation; Al-alloy values were not seen. |
| 58 | Zener 1937, 1938 | verified | Part I phys. Rev. 52, 230; Part II (1938) seen in related results. |
| 59 | Nowick and Berry 1972 | verified | |
| 60 | Naderi, Amiri, Khonsari 2010 | verified | About 4 MJ/(m^3 K) for Al 6061-T6. |
| 61 | Rosa, Manzoni, Casati 2018 | verified | 316L lattices have higher damping than bulk in the selected amplitude and frequency range; no numbers; the authors plan work below 1e-4 strain and at high frequency. |
| 62 | Damping of LPBF AlSi10Mg | see (c) | |
| 63 | Gutowski 2009 | verified | Exergy and energy of manufacturing processes; free PDF on MIT site. |
| 64 | Faludi 2017 | verified (existence); values not seen | |
| 65 | Kellens 2017 | verified | Procedia CIRP 61, 582 to 587; LCI overview for SLM, SLS, EBM, FDM, SLA. Secondary snippet: Kellens suggested 80 to 140 kWh/kg as a typical benchmark (288 to 504 MJ/kg). |

Tally (65 entries, second pass): verified 56; exists, content not checked 5 (2, 26, 45, 46, 56); exists, may not say this 2 (17, 44); not found 0; gap entries 2 (20, 62; see (c)); UNSURE not searched 0.

## (c) The three gaps

**Damping capacity of LPBF AlSi10Mg.** Found measurements exist but none in the form ψ at a stated stress amplitude.
- "Modulating the damping capacity of SLMed AlSi10Mg through stress-relieving thermal treatments" (ScienceDirect S0167844220300744): damping falls as the heat-treatment temperature rises (snippet only; no value).
- A Laser Induced Eng. paper (LIE 51, 187 to 203) studies laser power, scan speed and hatch effects on modal damping: maximum modal damping 1.0348 % (a damping ratio, 290 W, 2.2 m/s, 150 µm hatch).
- A ResearchGate paper reports damping ratios ζ = 0.013 to 0.311 % per mode, converted to loss factors, and says dissipation depends strongly on mode shape (source title not identified).
- These are modal, small-amplitude, in-air ratios. Converting a ratio ζ to ψ needs ψ = 4π·ζ (for ψ = ΔW/W); the planner should confirm which definition GMS-000 uses. No amplitude dependence or 20 to 60 MPa data seen. For bulk Al, one secondary snippet gives loss factors of 4e-4 to 1e-3 (dural).
- So ψ = 5e-3 is still an untested value for this alloy. The modal ratios imply a range that straddles it (the converted numbers are my arithmetic and UNSURE).

**AlSi10Mg lattice fatigue dataset.** One candidate found: "Experimental Evaluation of Fatigue Strength of AlSi10Mg Lattice Structures Fabricated by AM", Aerospace 2023, 10(5), 400 (doi 10.3390/aerospace10050400): truss lattices, SLM, uniaxial compression fatigue. Whether it has a data table, a repository or only figures was not checked. MDPI Aerospace is open access under CC BY (general knowledge about the journal, not verified for this paper). Others: a computational auxetic AlSi10Mg study (Metals 2020, 10, 945); an octet-truss compression fatigue study with three orientations (title not captured); a 2025 review "Fatigue failure mechanisms and life prediction of additive manufactured metallic lattices" (Virtual and Physical Prototyping). No Zenodo, Mendeley or Figshare repository was found. Boniotti 2019 (AlSi7Mg) is the closest peer-reviewed dataset by alloy family, and shows data in figures; its availability was not checked.

**Knock-down standard.** NASA-STD-6030 (2021) exists. I found no lattice-specific knock-down in it. Secondary sources say: HCF stress limits of 80 % (improved surface) and 60 % (as-built surface) of the applicable fatigue limit (a conference slide; the full list of rows was cut off); an AM knock-down of 1.20 until B-basis (a review, secondary); NASA-HDBK-5026 (2024) gives fatigue analysis factors of 4 (low cycle) and 10 (high cycle) per its summary. Lattices are probably handled by part-specific qualification. This is not confirmed; the standard was not opened. Revision A was reported in progress.

## Candidates (not evidence; found while searching)

- Aerospace 2023, 10(5), 400, AlSi10Mg lattice fatigue (above).
- "Porous Ti6Al4V alloys with enhanced normalized fatigue strength for biomedical applications", Mater. Sci. Eng. C (2016), 0.5 to 0.55 at 1e6.
- Nicoletto-type papers on as-built AlSi10Mg surfaces: Int. J. Fatigue and Procedia Structural Integrity (2020) "Influence of as-built surfaces on the fatigue behavior of AlSi10Mg ..." (ScienceDirect S2452321620302602); and the Springer 2024 "Fatigue life of L-PBF AlSi10Mg: effects of surface roughness and porosity" (s40964-024-00759-x).
- NASA-HDBK-5026 (2024), guidance on strength, fatigue and fracture for AM hardware.
- A 2024 FFEMS paper on compressive fatigue and acoustic emission of Ti-6Al-4V LPBF lattices (Raghavendra 2024).
- "Mechanical properties of lattice materials for fatigue-tolerant design and fabrication" (ResearchGate record).
- "Strain-based method for fatigue failure prediction of additively manufactured lattice structures", Sci. Rep. 2023.

## For S4 (replaces the earlier list)

1. No entry is now UNSURE for "not searched". Five entries (2, 26, 45, 46, 56) are confirmed to exist but their abstracts were not seen; two (17, 44) may not say what they are cited for; two are gaps (20, 62).
2. The as-built σ_w7 of 60 MPa still has no direct source. Machined values of 110 to 130 MPa are sourced; the as-built to machined ratio of about 0.56 combines two studies. Aboulkhair's as-built result could put the amplitude near 30 MPa if the quoted range is at R = 0.1. Widen the sweep to 30 MPa.
3. The 0.6 endurance ratio is in Bobbert 2017's abstract (planner right). The first-pass note that it belonged to Amin Yavari 2015 is withdrawn.
4. Dallago 2018 reports no advantage of stretching-dominated over bending-dominated cells in fully reversed fatigue (Ti-6Al-4V SLM, cubic-cell variants). C22's higher ratio for stretch cells (0.24 against 0.16) and the ordering in C5 (octet survives roughly 4x higher amplitude than bending cells) are therefore not supported by this entry; present them as model results only.
5. de Krijger 2017: for diamond Ti-6Al-4V lattices, S-N curves shift with R but life is governed by stress amplitude, and AM notches make life insensitive to mean stress. A Goodman factor in R25 and C18 (up to 2.7x) may overstate the mean-stress effect for as-built lattices; keep it as a conservative bound and say so. Lietaert 2018 gives the opposite emphasis (local mean tensile stress shortens tension-tension life), so the literature is mixed.
6. Zargarian 2016 is an FE study validated against literature data, not an experiment; do not cite it as test data. Its finding that the S-N exponent depends only on the bulk material supports using a single b per material.
7. Burr 2020 (progressive-failure framework, EBM) and Ushijima 2011 (formulas unconfirmed; up to 42 % error at larger aspect ratio) remain "may not say this".
8. Ahmadi 2018 (material type matters more than topology) and Amin Yavari 2015 (collapse within cell type only) disagree on normalisation across topologies; state both.
9. Inputs: α_s out of the sweep for the Z direction (26.6e-6 /K as built); c_p conflicting (739 or 922 J/(kg K)) and k not found; LPBF energy up to about 570 to 600 MJ/kg; primary Al and Ti values confirmed. Check ψ and loss-factor conventions (η, ζ, ψ differ by 2 and 2π) before using any measured damping.
10. Yan 2015 (AlSi10Mg DMLS gyroid lattices, Gibson-Ashby based strength equation) is a candidate for the gyroid gap in section 6 of the plan; it is static, not fatigue.
11. EOS fatigue values (110 and 97 MPa) are machined-sample values, not as-built.
12. Everything in the file is level `derived`.
