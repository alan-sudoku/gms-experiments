# OQ-22 check: does GMS-100's Σ_init price a scarce catalyst?

Level: every statement is a claim at level `derived` (unverified). Written 2026-11-15 by the `sonnet` agent. Scripts in `oq_22_code/`; outputs in `oq_22_code/outputs/`. Pointers "A3", "B4" are section headers inside `outputs/oq22_part_a.txt` and `outputs/oq22_part_b.txt`.

## Summary

- Central case (j = 1 A/cm², τ = 8e4 h, R_rec = 0.9, r_el = 1), GMS-100's terms, all source rows, λ_ℰ = 0 and λ_ℰ estimate: **Ir 0.10 to 1.62 mV** (0.2 to 2 mg/cm²: 0.098 to 0.16, 0.58 to 0.81, 1.17 to 1.62), **Pt 0.066 to 0.76 mV** (0.1 mg/cm²: 0.066 to 0.15; 0.5 mg/cm²: 0.42 to 0.76). Every row is **nearly free** (< 10 mV).
- Cause: Σ_s,init = n(CExC − b_ch) is the supply-chain energy of 0.1 to 2 mg/cm² (about 1e7 J/K per m² at most) set against j·τ = 2.9e12 C/m². CExC (CED stand-in, 1.7e5 to 3.3e5 MJ/kg) would have to be 25 times (Ir 2 mg/cm²) to 340 times (Pt 0.1 mg/cm²) larger, or j·τ 25 to 340 times smaller, to reach 30 mV (A6).
- λ_ℰ (b_infra bracket 2e9 to 7e10 J/kg, MEMORY) adds 0.8 to 29 percent; the b_infra needed for 30 mV is 25 to 355 times CExC (4e12 to 9e13 J/kg). R_rec, −b_ch (3e-6 of CExC), r_el = 2.5 (÷2.5) and the g side (2 to 26 percent at the 50 MJ/m² manufacturing bound) do not change a class.
- 10 mV is reached inside the duty grid only by Ir 1 and 2 mg/cm² and Pt 0.5 mg/cm² (j = 0.2 A/cm², τ = 2e4 h: up to 24 mV for Ir 2 mg/cm² with λ_ℰ = 0; 31 to 32 mV with λ_ℰ-hi). 30 mV is reached at one corner only (Ir 2 mg/cm², λ_ℰ-hi, g_low, low duty).
- Not a GMS-100 term: with Pt's exergy replacement cost (4.49e6 MJ/kg, 18x the CED) Pt at 0.5 mg/cm² is 8.2 mV at the central case, 16 mV at the G2.6 point, 164 mV at low duty. Ir ERC: not readable. So E18's "the substitution case rests on scarcity (Σ_init)" is reversed for this case under GMS-100's own terms: Σ_init prices embodied supply-chain energy, not scarcity.
- Part B (Pt): configuration is a **mix of B (probable, not shown) and C (certain in kind)**, not A. The CED source fails REQ-LIFECYCLE-CEXC-SOURCE items 4 and 6 as published (and 1, 2, 5).

## Part A

### Inputs

| Input | Value | Unit | Status | Source |
|---|---|---|---|---|
| CED Pt supply mix / primary ZA / primary RU / secondary | 243000 / 308000 / 327000 / 11900 | MJ/kg | LOOKUP | Nuss and Eckelman 2014, SI S1 Table S38, "CED [MJ/kg]", rows Pt TOTAL, Pt (ZA), Pt (RU), Pt (secondary); re-downloaded 2026-11-15; `data/ced_nuss_eckelman_2014.csv` |
| CED Ir supply mix / ZA / RU | 169000 / 165000 / 175000 | MJ/kg | LOOKUP | same, Ir rows |
| CED Ni total, Fe (pig iron) | 111, 23.1 | MJ/kg | LOOKUP | same, Ni TOTAL, Fe TOTAL |
| b_ch Pt, Ir, Ni, Fe | 140.97, 256.56, 232.71, 376.99 | kJ/mol | LOOKUP | Szargut et al. 2005, Exergoecology Portal Table 1 (2026-11-15); `data/bch_szargut_2005.csv` |
| ERC Pt; Ni; Fe | 4491688; 761; 17.75 | MJ/kg | LOOKUP | IntechOpen ch. 62189 Table 1 (Pt); Torres et al. 2026 Zenodo dataset (Ni, Fe). Ir: no value |
| Pt M&M cost (extra Pt row) | 291667 | MJ/kg | LOOKUP | IntechOpen ch. 62189 Table 1 |
| Allocation shares (revenue, mass) | Table S30, S28 sums | – | LOOKUP | Nuss and Eckelman SI S28, S30; `data/nuss_pgm_allocation.csv` |
| CED to CExC factor κ | 1.0 (0.8 to 1.5 swept) | – | MEMORY (UNSURE) | assumed; CED is energy, not exergy, in every row that uses it |
| Molar masses | 195.084, 192.217, 58.693, 55.845 | g/mol | MEMORY (UNSURE) | standard values |
| b_transport | 1e6 | J/kg | scenario | inside the spec range 0.5e6 to 1.5e6 |
| R_rec central; w_lost,remelt | 0.9; 0.049 × CExC | – | scenario; proxy UNSURE | ratio of Pt secondary to primary CED (LOOKUP) used as proxy |
| Side g: NiFe oxyhydroxide, Ni:Fe 3:1 molar (Ni 0.759, Fe 0.241 by mass) | g_low 1 mg/cm², g_high 5 mg/cm² metal | – | declared | w_lost,prec = 1× or 3× (CExC − b_ch); B_mfg = 0 or 50 MJ/m² (MEMORY UNSURE bounds); tooling = computation = 0; R_rec(Ni) = R_rec(Fe) = 0 |
| b_infra bracket | 2.1e9 / 2.1e10 / 7.1e10 | J/kg | MEMORY (UNSURE) | Part B |

Form: Ir as metal ("Ir at refinery"); condition 5 is not met for IrO₂, the usual anode form (A0). Pt as metal.

### Term table per loading (J/K per m², supply-mix row, central duty, R_rec = 0.9; A2)

| x | mg/cm² | Σ_s,init | Σ_s,EOL | λ_ℰ mid (lo to hi) | Σ_g,init (high; low 2.9e3) | Σ_g,EOL (high) |
|---|---|---|---|---|---|---|
| Ir | 0.2 | 1.134e6 | 5.0e4 | 9.6e4 (9.6e3 to 3.3e5) | 2.11e5 | 777 |
| Ir | 1 | 5.67e6 | 2.50e5 | 4.8e5 (4.8e4 to 1.65e6) | 2.11e5 | 777 |
| Ir | 2 | 1.134e7 | 5.0e5 | 9.6e5 (9.6e4 to 3.3e6) | 2.11e5 | 777 |
| Pt | 0.1 | 8.15e5 | 3.6e4 | 6.9e4 (6.9e3 to 2.4e5) | 2.11e5 | 777 |
| Pt | 0.5 | 4.08e6 | 1.80e5 | 3.4e5 (3.4e4 to 1.2e6) | 2.11e5 | 777 |

Transport term in Σ_s,init: 7 to 67 J/K per m² (≤ 5e-6 of Σ_s,init). Σ_g,init (high) = 62.9 MJ/m²: precursor 4.3e4, transport 280, manufacturing 1.68e5 J/K per m². Upper bound on w_lost,prec and Σ_mfg is MEMORY; with it the g side is 1.9 percent (Ir 2) to 26 percent (Pt 0.1) of Σ_s,init (A2), so it is not negligible at the lowest loadings and both cases are reported.

### Central case and classes (mV; j = 1 A/cm², τ = 8e4 h, r_el = 1; A3)

λ_ℰ = 0 columns span the rows mix/ZA/RU and g_high/g_low; λ_ℰ columns span λ_ℰ-mid with g_high to λ_ℰ-hi with g_low. Class of every one of the 2×2×(3 or 4) rows per loading: nearly free.

| x, mg/cm² | λ_ℰ = 0 | λ_ℰ estimate | class |
|---|---|---|---|
| Ir 0.2 | 0.098 to 0.127 | 0.107 to 0.162 | nearly free |
| Ir 1 | 0.576 to 0.634 | 0.625 to 0.810 | nearly free |
| Ir 2 | 1.174 to 1.269 | 1.271 to 1.621 | nearly free |
| Pt 0.1 | 0.066 to 0.118 | 0.073 to 0.151 | nearly free |
| Pt 0.5 | 0.419 to 0.592 | 0.454 to 0.757 | nearly free |

Pt row of Thanatia M&M (exergy, 291667 MJ/kg): 0.507 / 0.528 mV (λ_ℰ = 0, g_high / g_low) at 0.5 mg/cm², also nearly free. The G2.6 point (j = 0.5 A/cm², τ = 8e4 h) is twice the central value: Pt 0.5 mg/cm² 0.84 mV (λ_ℰ = 0, g_high), 0.95 mV (λ_ℰ mid, g_low); Ir 2 mg/cm² 2.41 to 2.65 mV (A4).

Allocation (A5), Ir 2 mg/cm², λ_ℰ = 0, g_high: revenue (published) ZA 1.17 mV, RU 1.25; PGM-by-revenue-then-mass ZA 2.04, RU 1.09; mass over PGM, Cu and Ni: about 0 (the rule prices Ir like Ni, 970 and 110 MJ/kg); Δη_be < 0. Pt 0.5 mg/cm²: 0.54 (ZA, revenue), 0.49 (PGM mass), 0.27 (RU, PGM mass). All nearly free.

### Duty grid (A4; supply-mix row, λ_ℰ = 0 and g_high, mV, rows j, columns τ = 2e4 / 4e4 / 8e4 h)

| j (A/cm²) | Ir 2 | Ir 1 | Ir 0.2 | Pt 0.5 | Pt 0.1 |
|---|---|---|---|---|---|
| 0.2 | 24.07 / 12.03 / 6.02 | 11.82 / 5.91 / 2.95 | 2.01 / 1.01 / 0.50 | 8.37 / 4.19 / 2.09 | 1.32 / 0.66 / 0.33 |
| 0.5 | 9.63 / 4.81 / 2.41 | 4.73 / 2.36 / 1.18 | 0.81 / 0.40 / 0.20 | 3.35 / 1.67 / 0.84 | 0.53 / 0.26 / 0.13 |
| 1 | 4.81 / 2.41 / 1.20 | 2.36 / 1.18 / 0.59 | 0.40 / 0.20 / 0.10 | 1.67 / 0.84 / 0.42 | 0.26 / 0.13 / 0.07 |
| 2 | 2.41 / 1.20 / 0.60 | 1.18 / 0.59 / 0.30 | 0.20 / 0.10 / 0.05 | 0.84 / 0.42 / 0.21 | 0.13 / 0.07 / 0.03 |

With λ_ℰ-hi and g_low (A4): Ir 2 mg/cm² reaches 31.3 mV at the first corner, Ir 1 15.7, Pt 0.5 11.3. Over all rows, g cases and λ_ℰ in {0, hi}: maxima Ir 0.2 3.2 mV, Ir 1 16.2, Ir 2 32.4 (3 of 72 points above 30), Pt 0.1 3.0, Pt 0.5 15.1. The 10 mV threshold is bracketed for Ir 1, Ir 2 and Pt 0.5; the 30 mV threshold only for Ir 2 (and then only with λ_ℰ-hi). For Ir 0.2 and Pt 0.1 the grid cannot bracket 10 mV; A6 gives the factors.

### Lever factors for Δη_be = 30 mV (central, supply-mix row, λ_ℰ = 0, g_high; A6)

| Case | base (mV) | CExC | loading | j·τ | b_infra needed | R_rec |
|---|---|---|---|---|---|---|
| Ir 2 | 1.203 | ×24.5 | ×24.5 (49 mg/cm²) | ÷24.9 (3.2e3 A h/cm²) | 4.1e12 J/kg (24.5× CExC) | cannot (1.15 to 1.21 mV) |
| Ir 1 | 0.591 | ×49 | ×49 | ÷50.8 | 8.5e12 J/kg | cannot |
| Ir 0.2 | 0.101 | ×245 | ×245 | ÷300 | 4.3e13 J/kg | cannot |
| Pt 0.5 | 0.419 | ×68.2 (10 mV at ×22.8) | ×68.2 (34 mg/cm²) | ÷71.7 | 1.7e13 J/kg (70× CExC) | cannot (0.400 to 0.421 mV) |
| Pt 0.1 | 0.066 | ×341 | ×341 | ÷453 | 8.6e13 J/kg | cannot |

The b_infra bracket is 2e9 to 7e10 J/kg (0.008 to 0.29 × CExC): short of the needed value by a factor 84 (Ir 2) to 1200 (Pt 0.1) even at the high corner (needed/hi = 24.5/0.29 for Ir 2). κ swept 0.8 to 1.5 moves Pt 0.5 from 0.33 to 0.64 mV, Ir 2 from 0.96 to 1.82 mV.

### G2.6 reproduction (A1) and what GMS-100's terms change

G2.6 inputs reproduce: 0.844 (mix), 1.069 (ZA), 1.135 (RU), 1.493 mV (upper bound), against 0.84, 1.07, 1.13, 1.5 in the claim. **This is an arithmetic reproduction with the claim's own formula, not an independent check.** Changes by GMS-100's terms at that point (Pt mix, g_high, R_rec = 0.9): −b_ch lowers Σ_s,init by 3e-4 percent; the EOL term (remelt proxy, UNSURE) adds 4.4 percent of Σ_s,init (at R_rec = 0 only b_ch: 3e-4 percent); λ_ℰ adds 8.5 percent (mid) to 29 percent (hi) of the extraction term; side g subtracts 5.2 percent (g_high) or 0.07 percent (g_low). Net: 0.837 mV (λ_ℰ = 0, g_high) and 0.909 mV (λ_ℰ mid), both against 0.844 for G2.6's formula. GMS-100's terms do not move the claim.

### r_el and ERC diagnostics

- r_el = 2.5 (A7a): every value ÷2.5, e.g. Ir 2 mg/cm² 1.20 to 0.48 mV, Pt 0.5 mg/cm² 0.42 to 0.17 mV. No class moves toward "priced".
- ERC, not a GMS-100 term (A7b): Pt 0.1 mg/cm²: 1.60 mV (central), 3.19 (G2.6 point), 31.9 (j = 0.2 A/cm², τ = 2e4 h, priced); Pt 0.5 mg/cm²: 8.19 (nearly free), 16.4 (between), 164 (priced). ERC is 18.5× the CED and 15.4× the M&M cost. A scarcity-pricing term of ERC's size would move the central case close to the 10 mV line for 0.5 mg/cm² and into "between" at j = 0.5 A/cm². Ir: no readable ERC, not computed.
- Omitted side-s stages (outside GMS-100's boundary, no source bound found; A7c): with an illustrative multiplier ω = 1 on the extraction work, Δη_be doubles at most (Ir 2 mg/cm² 2.4 mV, Pt 0.5 mg/cm² 0.84 mV). The GMS-100 values are lower bounds under its boundary.
- b_ch share of CExC (A7d): Pt 3e-4 percent, Ir 8e-4 percent, Ni 3.6 percent, Fe 29 percent; "condition 2 not met" in all rows (CED has no reference environment). Dispersal at low R_rec adds only b_ch(x): 0.72 MJ/kg Pt (12 J/K per m² at 0.5 mg/cm²), 1.33 MJ/kg Ir (90 J/K per m² at 2 mg/cm²), 3e-6 of the extraction term.
- R_rec (A7e): 0 to 0.95 changes Δη_be by 5 percent at most (remelt proxy 4.9 percent of CExC, UNSURE).

## Part B (Pt; chosen because only Pt has stage-resolved operating-energy data (Buchspies et al. 2017), a secondary CED row, ERC and M&M values)

### Source conditions, REQ-LIFECYCLE-CEXC-SOURCE (B1)

| Condition | S1 Nuss and Eckelman CED | S2 Bösch CExD (ecoinvent) | S3 Thanatia M&M Pt | S4 Buchspies 2017 (energy only) |
|---|---|---|---|---|
| 1 ore exergy | not met (CED is energy carriers) | met by definition (metals category), factors not read | not stated | not applicable |
| 2 same reference environment | not met (no environment) | partly (Szargut-based, 298.15 K; table not read) | stated (Szargut with improvements) | not applicable |
| 3 by-product rule | met: revenue 2006 to 2010 (Table S30) | not stated | not stated | not met (6E mixture) |
| 4 capital goods | not stated (SI silent; ecoinvent usually includes, UNSURE) | not stated | not stated | met by omission (energy carriers only) |
| 5 chemical form | met for metal; not met for IrO₂, Pt/C | not stated | element only | mixture |
| 6 monitoring/assaying/maintaining flows | not stated | not stated | not stated | partly (all site energy included) |

### Decomposition (B2, B3)

- CED Pt mix 243000 MJ/kg by stage, if the stage split of delivered energy applies (Buchspies: mine 34, concentrator 26, smelter and converter 28, refinery 12 percent): 82600, 63200, 68000, 29200 MJ/kg. Assumption not exact (electricity, 75 percent of energy, carries an upstream factor of about 3.1 in Buchspies' data).
- Capital goods, maintenance, fixed vs throughput-proportional: **no source read splits them.** The CED row gives one number per kg; Buchspies gives operating energy only (no capital).
- Independent check (not by construction): Buchspies 2015 CED fossil 6.0e5 MJ/kg 6E PGE against the Nuss/ecoinvent burden of 3.2e5 MJ/kg PGM (2.8e5 PGM share): ratio 1.9 to 2.1. The CED row may understate the current chain by up to 2× (UNSURE); that would not change any class.

### B_infra estimate (B4; all inputs MEMORY, UNSURE; corners lo / mid / hi)

| MJ per kg Pt | lo | mid | hi |
|---|---|---|---|
| capital goods share c of the source energy | 0.01 | 0.05 | 0.30 |
| operating, variable | 2.0e5 | 1.7e5 | 1.0e5 |
| operating, fixed (ventilation, cooling, holding, utilities; f_op 0.17 / 0.27 / 0.39) | 4.1e4 | 6.3e4 | 6.7e4 |
| loop capital in source: sunk / avoidable | 1.9e3 / 4.9e2 | 6.7e3 / 5.5e3 | 2.2e4 / 5.1e4 |
| avoidable-fixed | 4.1e4 | 6.8e4 | 1.2e5 |
| α = avoidable-fixed / fixed part | 0.95 | 0.91 | 0.84 |
| fraction α_x that leaves with Pt | 0.05 | 0.30 | 0.60 |
| **b_infra** | 2.1e9 J/kg | 2.1e10 J/kg | 7.1e10 J/kg |

b_infra/CExC = 0.008 / 0.085 / 0.29. α is the avoidable fraction of the fixed part, 0.84 to 0.95 (the fixed operating flows are avoidable; only capital has a sunk part). α_x, the Pt-attributable share, is the largest unknown (loop shared with Pd, Rh, Ni, Cu). Cannot be estimated from the sources read: true fixed fractions, loop capital inventory, recycling loop, sunk fraction, α_x.

### Configuration (B5)

**A mix of B and C.** C is in the data in kind: the CED row is built from mine, concentrator, smelter and refinery operating data, which contain the fixed flows (ventilation, cooling, pumping, holding): 17 to 27 percent of the row in the bracket (inference, not a statement of the source). B is probable (ecoinvent unit processes usually carry infrastructure, MEMORY UNSURE; SI silent): 1 to 30 percent of the row. Not A. The spec cannot tell A from C because the source gives no split. Fails as published: condition 4 (capital goods undeclared, probably included) and condition 6 (flows undeclared, fixed operating flows contained), also 1, 2, 5. To meet 4 and 6 an evaluation would remove from CExC(Pt): loop capital 2.4e3 to 7.3e4 MJ/kg (mid 1.2e4) and the avoidable fixed operating flows counted in B_infra, 2.0e3 to 4.0e4 MJ/kg (mid 1.9e4). Effect on Part A: λ_ℰ added on top of this CED double counts the flows already inside CExC (the λ_ℰ columns are then an upper bound by 0.8 / 8.5 / 29 percent); moving them from CExC into λ_ℰ leaves Δη_be unchanged. With λ_ℰ = 0 under B, CExC returns an average share of loop capital (1 to 30 percent of Σ_s,init) to the incumbent: the item 4 bypass.

## Identity checks (true by construction; not counted as passes)

- G2.6 reproduction uses the claim's own formula (A1).
- Δη_be from J/K terms equals the direct J/m² form (A8).
- The 30 mV lever solution reproduces 30 mV (A6).
- g-side mass fractions sum to 1 (A8). Avoidable-fixed + sunk + variable = e_tot (B4).
- Real checks (independent inputs): Thanatia Pt M&M / Nuss CED mix = 1.20; Ni M&M / Ni CED = 1.04; Szargut 2005 vs 2007 b_ch for Ni (equal) and Fe (0.7 percent); S28 Ir mass share 0.0025 percent vs S30 0.003 percent; Buchspies/Nuss ratio 1.9 (A8, B3). These agree to the stated tolerances; they do not validate κ.

## Not settled

- CED is a stand-in for CExC; κ = 1 is MEMORY. No Pt or Ir CExC table was read. Bösch CExD factors and Calvo et al. 2018 Table 1 were not reachable.
- Ir ERC not readable. Omitted side-s stages not bounded from a source. Side-g manufacturing bound (50 MJ/m²), precursor factor (3×), w_lost,remelt proxy, c, a_cap, α_x, fixed fractions: all MEMORY.
- Part B cannot say how much of a CED row is capital goods or fixed flows; the configuration is argued from how the inventory is built, not from a published split.
- The single input whose change would most move the classes: the CExC (or CED) magnitude of the incumbent catalyst relative to j·τ. It would have to rise 25 times (Ir 2 mg/cm²) or 68 times (Pt 0.5 mg/cm²) to reach "priced" at the central case; no input read is that uncertain (Buchspies vs Nuss differ by 2×; allocation rules by 1.7× for Ir except the mass rule, which lowers it). The only input that changes a class by itself is the duty (j·τ at the low-duty corner), or a scarcity term of ERC's size (Pt).
