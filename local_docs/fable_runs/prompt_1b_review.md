# Prompt 1b review (stage S5, independent adversarial reviewer)

Context file (`local_docs/`, never cited by the spec). Written 2026-11-13. Inputs: `fable_questions.md` (Prompt 1b block), `prompt_1b_answer.md`, `prompt_1b_plan.md`, `prompt_1b_code/` (S2 scripts, `gms_core.py`, S4 `s4_*.py`, `outputs/`, `outputs/issues.md`), `prompt_1b_citations.md`. My scripts and outputs: `prompt_1b_review_code/` (`rv1`–`rv6`, numpy and plain Python, outputs in `prompt_1b_review_code/outputs/`).

**Status of everything here: claim at level `derived` (unverified).** I agree with most of the answer, but my agreement is not validation. My independent checks use different code and in places different closures. They use the same air properties and, where noted, the same unconfirmed correlation constants. No measurement was made.

## Summary verdict

1. Reproducible. All 18 scripts re-ran byte-identical to the saved outputs. Every number I traced from the answer to an output matches. An independent re-implementation gives the headline Cu plate 0.2679 K/W at 0.1 W and the Al/Cu penalty of 9.3–21.2 %. With other friction and Nusselt forms the headline is 0.266; with a 2-D height-unmixed air closure it is 0.272 and the penalty becomes 10–26 %.
2. The B verdict (valid with restated scope; no Al design matches Cu at equal envelope and fan power; the lattice part is unsupported, not disproved) and the C verdict (invalid as stated) both follow from the evidence. The B1.6 argument that device plus sink generate (Q + W_fan)/T₀ for every design is correct. So is T_hot as the flux-weighted harmonic mean. So is the C-side j₀ ambiguity (factor 1.43e6).
3. MAJOR 1: claim C3.3 is wrong in the regime the prompt sets. At 1 A/cm² a cell runs above the thermoneutral voltage, so I·η/T₀ is the correct marginal generation, not an overstatement.
4. MAJOR 2: the answer misses partial substitution. With a concentrated source, a 30 × 30 mm copper slug (12 % of the copper) recovers about 64 % of the Al–Cu peak-resistance gap. The restated claim B treats the element question as all-or-nothing.
5. No BLOCKER. 0 BLOCKER, 2 MAJOR, 11 MINOR.

## Findings

| # | Severity | Location | Finding | Evidence or script |
|---|---|---|---|---|
| 1 | MAJOR | C3.3 (plan D10) | "Σ̇_act = I·η/T₀ overstates the generation when the cell runs warm (factor T₀/T_cell = 0.844)" is false whenever the heat from the overpotential is rejected to the environment. That is the case for any cell above the thermoneutral voltage (about 1.48 V). Alkaline and PEM cells at 1 A/cm² run at about 1.7–2.0 V (typical range, not checked, UNSURE). The marginal heat from a larger η then goes to the coolant at T₀, so the Pt-vs-NiFe difference generates exactly ΔI·η/T₀, the prompt's form. The T₀/T_cell credit holds only below thermoneutral, where the overpotential heat replaces heat that would otherwise be supplied at T_cell. The answer's own B1.6 argument (all dissipation ends at T₀) contradicts the first clause. | Exergy balance in "Derivation checks" (D10) |
| 2 | MAJOR | B2.8, restated claim B, verdict B | The answer misses a fair design: Al fins with copper only where the heat enters. 20 × 20 mm source, t_b = 5 mm, 0.1 W, peak resistance: all-Cu 0.350; Cu base with Al (k = 150) fins 0.387 (0.161 kg Cu, 47 % of the all-Cu copper); Al base with a 30 × 30 × 5 mm Cu slug 0.409 (0.040 kg Cu, 12 %); 40 × 40 mm slug 0.395 (0.072 kg, 21 %); all-Al 0.512. The slugs come from a 3-D finite-volume solve, checked against the exact series to 0.02 % on R_max. "An aluminium base adds 0.07–0.22 K/W that no fin geometry recovers" holds for fin geometry. But for the framework's question (can geometry replace element x?) the answer is "it can cut x by about 90 % for about 36 % of the gap", and the verdict paragraph does not say so. | `rv3_spreading.py` (c), (d) |
| 3 | MINOR | B2.12 | "The model is, if anything, generous to aluminium and to lattices" is half right. The 1-D closure mixes the air over the fin height. In laminar 1.3 × 30 mm plate channels nothing does that, but in a lattice it is roughly true. A 2-D closure (each height strip keeps its own temperature) raises plate R_fa by 1.7 % (Cu) and 3.8 % (Al k = 150) at 0.1 W. The Al/Cu ratio becomes 1.10–1.26 instead of 1.09–1.21, which strengthens B2.4. Against the plate targets of the 2-D closure, the gyroid χ needed to equal Al plate fins falls from 0.34 to 0.29–0.30 (c_f 0.3–0.1), the laminar-tube level. So the closure is generous to plates relative to lattices. Conclusions unchanged. | `rv1` (0), P = 0.1 W rows; `rv4` (d) |
| 4 | MINOR | B2.6 | The χ thresholds rest on the Hashin–Shtrikman upper bound for k_eff, which flatters the gyroid. With k_eff = kρ̄/2 the thresholds rise to 0.84 (Cu) and 0.45 (Al plate) at c_f = 0.3. With kρ̄/3, Cu is unreachable at c_f = 0.3 and the Al-plate threshold is 0.60. Together with finding 3, the Al-plate threshold is uncertain by about −0.05 to +0.26. The low confidence on B2.6 is appropriate. The precise 0.32–0.37 band is not. | `rv4_gyroid.py` |
| 5 | MINOR | C1.4, C2.10, verdict C | Lu and Zhao 2015 (full text read via Europe PMC) give 0.24 and 0.27 V at 0.5 and 1 A/cm² in **10 M KOH**, "according to the Tafel plot", from a polarisation curve with 75 % iR compensation. In 30 wt% KOH they give 0.27 V at 0.1 A/cm² and 0.34 V at 0.3 A/cm² with 32 mV/dec, which extrapolates to about 0.357 V at 1 A/cm² (my extrapolation). The answer calls 0.27 V "measured" and, in C2.10, pairs the 10 M point with the 30 wt% slope (the paper gives 33 and 28 mV/dec in 0.1 and 1 M KOH). The verdict band 0.27–0.47 V stands; its low end is a 10 M KOH Tafel-plot value. | `rv5_electrode.py` (e); full text via Europe PMC |
| 6 | MINOR | B2.11, C3.5 | Both energy comparisons set primary-energy CED (MJ/kg) against electricity one-for-one. The plan's D10 says this favours the substitution; the answer drops that caveat. With any primary-energy factor for electricity above 1, the fan penalty in B2.11 grows and the break-even overpotential in C3.5 shrinks. Both conclusions get stronger. | Plan D10 text; `s4_c_inputs.txt` (d), (e) |
| 7 | MINOR | B1.5 | The numbers use S2's circular-equivalent closed form. The exact rectangular series gives a harmonic–arithmetic gap of 0.005 K (Cu) and 0.029 K (Al), inside the stated bound of 0.014 and 0.086 K. Using T_max overstates the entropy term by 5.4 % and 9.3 %, against 5.8 % and 10.2 % in the answer. The closed form under-predicts the source-mean base resistance by 5–6 % and R_max by 1–2 %. | `rv3_spreading.py` (a), (b) |
| 8 | MINOR | B2.8 | "A 10 mm base lowers it to 0.097 at k = 150" keeps 30 mm fins, so the envelope grows by 5 mm and the equal-envelope constraint is broken. At equal envelope (10 mm base, 25 mm fins, re-optimised) the Al peak resistance is 0.487 against 0.512 with the 5 mm base; Cu is 0.350. The conclusion holds; the number is out of scope. | `rv6_regimes.py` (c) |
| 9 | MINOR | B2.7, B2.12, "regimes not tested" | The answer lists a mass limit as a regime where a lattice may win. At equal mass (0.119 kg, the Al k = 150 optimum) the best copper sink (1 mm base, 15 fins) gives 0.542 K/W uniform and 0.873 K/W with the 20 mm source. Al plate fins give 0.314 and 0.512. Under a mass limit, **plain Al plate fins** win by a factor of about 1.7; no lattice is needed. So the regime changes the Al-vs-Cu verdict but not the lattice verdict. | `rv6_regimes.py` (b) |
| 10 | MINOR | B2.7 list of untested regimes | Natural convection is irrelevant at this load. In a 60 × 60 × 30 mm envelope the optimum vertical fins give R ≥ 3.9 K/W (isothermal fins, h about 6.6 W/m²K), so 100 W would mean a rise of at least 386 K. The constants are from memory (UNSURE), but the order of magnitude is not in doubt. | `rv6_regimes.py` (d) |
| 11 | MINOR | B2.7 (fan curve, from B13) | B13 put the fixed 0.1 W designs on the fan curve without re-optimising them. Re-optimised on three linear fan curves (30 Pa/8 L/s, 60/12, 150/20; assumed), Al/Cu is 1.135, 1.160 and 1.197 (k = 150) and 1.21, 1.25 and 1.31 (k = 100). This confirms the verdict, and the penalty grows with fan strength. | `rv6_regimes.py` (a) |
| 12 | MINOR | C2.7 | The a_v·j₀ band 1.3e6–5.1e6 A/m³ is for pores with ε = 0.5 only. A foam-like ε = 0.9 needs 5.5e5–1.2e6. The verdict is unchanged; the text should state ε. | `rv5_electrode.py` (c) |
| 13 | MINOR | C1, C3.2 (missed comparison) | Conventional alkaline cells run at about 0.2–0.5 A/cm² (domain knowledge, not checked, UNSURE). A NiFe anode at 1 A/cm² is a zero-gap alkaline or AEM condition. The like-for-like comparison at the prompt's 1 A/cm² is an AEM or zero-gap NiFe anode against a PEM IrOx anode, at cell level. The answer says the verdict depends on cell voltage but computes no cell-level comparison. | – |

Rounding only (not counted): B1.2 gives "36–43 %", but the pin value is 43.5 %, so the range is 36.5–43.5 %.

## Reproducibility

All S2 and S4 scripts re-ran with Python 3.13.18 and numpy 2.5.3, writing to a scratch directory. A `cmp` against `prompt_1b_code/outputs/` showed all 18 files byte-identical (`b01`–`c09`, `s4_b_plate`, `s4_b_pin_gyroid`, `s4_c_inputs`).

| Answer number | Source | Re-run | Independent check (`rv*`) |
|---|---|---|---|
| Cu plate 0.268 K/W, 38 × 0.3 mm, 3.86 L/s, 25.9 Pa, η 0.73, NTU 1.76 (B2.10) | b05 | identical | rv1: 0.2679 with the same correlations in new code; 0.2662 with Shah plate friction and Nu = 7.54 (set B); 0.2725 with the 2-D closure |
| Al/Cu 1.09–1.21 at 0.1 W (k 200–100); 1.12–1.13 heat treated (B2.4) | b05, s4p (b) | identical | rv1: 1.093–1.212 (S, 1-D); 1.094–1.212 (B, 1-D); 1.104–1.264 (2-D). Equal t_min 0.3 mm: 1.08–1.21 (1-D), 1.10–1.26 (2-D) |
| PF12 ratios 1.11–1.28 (B2.4) | s4p (a2) | identical | not re-checked (PF12 constants UNSURE) |
| Mixing share 42.4 / 40.2 / 43.5 / 36.5 % (B1.2) | b16 | identical | rv2: same values from the closed form; Cu 0.419 with the 2-D stratified exhaust; Cu share 0.40–0.45 over 0.01–1 W; leading-order (1/C)/(2R) within 2 points |
| E(T_mean) vs E(T_lm) 0.7–1.3 % (B1.2) | b16 | identical | arithmetic only |
| Pump 3.7 % (B1.3); 1.2 % and 4.8 % (B1.8) | b16, b18 | identical | arithmetic (309.10/298.15 − 1 = 3.67 %) |
| T_hot gap 0.014 / 0.086 K; T_max overstatement 5.8 / 10.2 % (B1.5) | b14 (B17) | identical | rv3: 0.005 / 0.029 K; 5.4 / 9.3 % (finding 7) |
| Base R_sp,max 0.081 (Cu), 0.155–0.304 (Al); penalty 0.125 at k = 150 (B2.8) | b14 | identical | rv3 exact series: 0.0825, 0.2076 (k = 150), 0.3047 (k = 100); penalty 0.1251 |
| Peak rises 39 / 55 / 60 / 65 K (B2 table) | b14 (B15) | identical | not re-derived for pin and gyroid |
| Pins 46–58 % over Cu at 0.1 W; 1.30 minimum in extended sweep (B2.5) | b07, s4g (a2) | identical | not re-implemented (constants UNSURE); f_K never active (0 of 30) confirmed in output |
| Gyroid χ_min: Cu 0.659, Al plate 0.342 (c_f 0.3); 0.535 / 0.351 (c_f 0.1), at k = 150, 0.1 W, a ≤ 10 mm (B2.6) | s4g (b) | identical | rv4: 0.659 / 0.342 and 0.535 / 0.346 (finer ρ̄ grid); sensitivity in findings 3 and 4 |
| Plate optimum's own χ (context for B2.6) | – | – | rv4: Cu 0.318, Al 0.321 (j/f_app, channel friction only) |
| Air power for equal function 0.137–0.205 W (Al plates), 0.265 (gyroid), 0.460 (pin); 24–67 MJ (B2.11) | b12 | identical | arithmetic checked (0.4215 W × 1.578e8 s = 66.5 MJ) |
| Fan-curve R 0.230 / 0.267 / 0.310 / 0.377 (B2.7) | b10 (B13) | identical | rv6: re-optimised designs give the same ranking (finding 11) |
| Equal-flow, 60 Pa cap: 0.232 / 0.252 / 0.287 / 0.362 (B2.7) | s4g (c) | identical | – |
| Utilisation 0.29 / 0.19 / 0.11 / 0.07 (C2.6) | c06 | identical | rv5 finite volume plus Newton: 0.2924 / 0.1864 / 0.1120 / 0.0667, equal to the closed form |
| η_min floor formula; R_eff 190–770 (foam) (C2.7) | c06, s4i (c) | identical | rv5: thick-electrode finite volume agrees with b·acosh(…) to < 3.1e-5 relative in 5 cases; R_eff 338 and 414 for the foam cases |
| a_v·j₀ 1.3e6–5.1e6 (alkaline Pt/C), 3e9–1.3e10 (acid) (C2.7) | s4i (c) | identical | rv5: 3.0e6 and 5.1e6 at ε = 0.5 (κ = 62); 2.65e9 at ε = 0.9; finding 12 |
| R_f 60–600, 6e3–6e4, 6e5–7e6 (C2.3) | c01, s4i (a) | identical | rv5 (d): same |
| Pt/C acid η 4.28 / 2.14 / 1.17 / 0.59 mV (C2.4) | s4i (a) | identical | rv5 (d): same |
| j₀ 1.045e-4 vs 7.30e-11, ratio 1.43e6 (C2.10) | s4i (b) | identical | rv5 (d): same |
| Break-even 0.08–1.14 mV (Pt), 1.1–2.4 mV (Ir) (C3.5) | s4i (d) | identical | arithmetic (121.5 MJ/m² ÷ 1.44e12 J/m²/V = 0.084 mV) |

Rows S2 flagged as identities or plausibility-only (B02, B03 (iii), B04, B08, B11, B13 bound, B14 (i), B15, B16 (iv), B18 (a), (c), B20, C03, C11, C12, C13): the answer lists them as non-evidence in §0 and does not lean on them. Three places come close but say so in the text: B1.6 cites the 0.33540 W/K identity "for scale"; C2.1 says the S2 check confirms the code only; B2.12 is a comparison of two approximations. B2.6 rests on a plausibility-only model (B09) and is correctly held at low confidence.

## Derivation checks

- **B1.1 / D1, the stream balance.** Correct. For the sink alone, Ṡ_gen,1 = C ln(T_out/T_in) − Q/T_hot + V̇ΔP/T_in, which equals Q(1/T_lm − 1/T_hot) + … exactly for constant c_p. The plume term C[(T_out − T₀)/T₀ − ln(T_out/T₀)] = Q(1/T₀ − 1/T_lm) is the right mixing generation. With the 2-D closure the exhaust is stratified (319.0–325.3 K for Cu). Mixing then includes inter-strip mixing, but this changes the share by only 0.1 point (`rv2` (b)).
- **B1.6, device plus sink is (Q + W_fan)/T₀ for every design.** Correct under the stated conditions: steady state, Q a fixed electrical dissipation, every energy stream ending at T₀, and no useful heat. It follows from Gouy–Stodola applied to work input: everything that enters as work is dissipated. Its consequence is the strongest point of the answer. The prompt's thermal term only allocates generation between device and sink. At equal function the only operating discriminator is ΔW_fan,elec/T₀, plus any temperature-dependent device loss (B1.7). Caveat: if the device dissipation Q rises with temperature (leakage), the sink does change the total. The answer names this but does not size it.
- **B1.5 / D2, T_hot as flux-weighted harmonic mean.** Correct. The entropy inflow is ∫q″/T_s dA, so T_hot = Q/∫(q″/T_s)dA. The arithmetic mean differs by about Var(T)/T̄. The exact series gives 0.005 K (Cu) and 0.029 K (Al), negligible against the 2–5 K by which T_max exceeds the mean (`rv3` (b)).
- **B1.3 / D3, pumping at T₀.** Correct. Dissipation at T_air plus rejection to T₀ sums to V̇ΔP/T₀. Replacing V̇ΔP with W_fan,elec (B1.4) is also correct.
- **Fin and closure method (`gms_core.py`).** The plate fin (m² = 2h/(kt), adiabatic tip at the shroud, overall surface efficiency with ε-NTU on G = h(ηA_f + A_b)), the pin fin (m² = 4h/(kd)) and the gyroid porous fin (m² = h·a_sf/k_eff) are standard. I re-derived the Ergun rewrite (133.33/Re_h + 2.333) and the Hashin–Shtrikman void bound 2ρ̄/(3 − ρ̄); both are correct. The V̇ solver (bisection on V̇·ΔP = P) is sound, and my log-space bisection reproduces V̇ to all printed digits. The mixed-air assumption is the main model-form choice; it is quantified in finding 3.
- **D10 / C3.3, entropy of the overpotential.** The exergy balance below thermoneutral is correct: extra electrical exergy Iη in, heat saved at T_cell worth Iη(1 − T₀/T_cell), net loss IηT₀/T_cell. Above thermoneutral, the marginal Iη leaves as heat rejected to T₀, and the loss is Iη, i.e. Σ̇ = Iη/T₀. The answer's first clause ("overstates when the cell runs warm") is therefore wrong at 1 A/cm² (finding 1).
- **C2.1, matching condition.** Correct. With equal α, η_cand = η_Pt requires (J/R_c)/j₀,c = (J/R_Pt)/j₀,Pt for both the asinh and the Tafel forms, independent of J.
- **C2.10 and C3.1, the Tafel/asinh j₀ ambiguity.** Correct and decisive. The symmetric asinh form fixes b = 2.303RT/(0.5F) = 118 mV/dec at 25 °C. Fitting one point (0.27 V, J/R_f = 0.02 A/cm²) gives j₀ = 1.045e-4 under that form and 7.30e-11 at 32 mV/dec. "Typical j₀" therefore has no meaning for NiFe until the slope is fixed. Minor caveat: the point is in 10 M KOH and the slope in 30 wt% (finding 5).
- **C2.6 and C2.7, porous electrode.** The closed forms are correct. Utilisation: E = sin 2θ/(2θ) with 2θ tan θ = δ follows from u″ = A e^u with no ionic flux at the back. The thick-electrode floor b·acosh(1 + J²/(4κ_eff a j₀ b)) is the first integral of κη″ = 2aj₀ sinh(η/b). Both are confirmed by an independent finite-volume Newton solution (`rv5` (a), (b)). Not modelled: gas in the pores beyond a Bruggeman factor, concentration gradients, and a finite matrix conductivity. The first two make the cap lower, so it is an upper bound on the benefit of area, as the answer says.

## Missed regimes

| Regime | Computed by answer? | S5 result | Effect on verdict |
|---|---|---|---|
| Partial substitution (Cu slug or Cu base with Al fins) | no | Concentrated source: 0.387–0.409 K/W with 12–47 % of the copper, against 0.350 all-Cu and 0.512 all-Al (`rv3`) | Changes how claim B should be restated: geometry does not replace Cu, but a small amount of Cu placed at the source recovers most of the gap (finding 2) |
| Mass-limited instead of volume-limited | named, not computed | Al plate beats Cu at equal mass by about 1.7× (`rv6` (b)) | Reverses Al vs Cu; no lattice needed (finding 9) |
| Fan curve instead of fixed air power | yes (B13, fixed designs) | Re-optimised: Al/Cu 1.135–1.197 (k = 150), penalty grows with fan strength (`rv6` (a)) | None |
| Natural convection | named, not computed | ≥ 3.9 K/W, infeasible at 100 W (`rv6` (d)) | Removes it from the list |
| Equal envelope with a thicker Al base | no (10 mm case broke the envelope) | 0.487 against 0.512 and Cu 0.350 (`rv6` (c)) | None |
| Turbulent or impinging flow | no | Not computed. Within the laminar model the Al penalty grows with air power (k = 100: 1.15 at 0.01 W to 1.29 at 1 W; k = 200: 1.07 to 1.13, from `b05`), and higher h lowers fin efficiency, so turbulence probably widens the gap (UNSURE). Impingement with short flow paths is where pin arrays are reported to do relatively better (Kim, Kim and Oh 2008, as summarised by S3; not read by me) | Open; most likely to change the lattice verdict |
| Non-uniform source | yes (B2.8) | Confirmed by an exact series (finding 7) | None |
| PEM vs alkaline vs AEM, cell level | partly (C1.2, C3.2 qualitative) | Not computed (finding 13) | None on "invalid as stated"; it matters for any restated claim C |
| Temperature-dependent device loss (leakage) | named (B1.7) | Not computed | Could make the thermal term matter; needs device data |

## Citations

Spot-checks (only titles, authors, DOIs and technical terms were searched):

| Ref | What I checked | Result |
|---|---|---|
| R64 Lu and Zhao 2015, Nat. Commun. 6, 6616 | Full text (Europe PMC XML) | 0.24 and 0.27 V at 0.5 and 1 A/cm² **in 10 M KOH, "according to the Tafel plot"**, 75 % iR compensation; roughness factor 50; 30 wt% KOH: 0.27 V at 0.1, 0.34 V at 0.3 A/cm², 32 mV/dec; 33 and 28 mV/dec in 0.1 and 1 M KOH. S3's reading is correct; the answer's use needs the caveat in finding 5 |
| R27 EOS AlSi10Mg data sheet | Search-engine extract of the EOS page | 100/110 as manufactured, 165/155 T6, 160/165 stress relieved W/m/K. Matches S3 and B2.9. Other suppliers: 113 (3D Systems), 120–160 (AddUp) |
| R56 Durst et al. 2014 ("about 100 × slower in alkali") | Search; RSC HTML blocked (403) | Not read. Secondary support only: Zheng, Sheng, Zhuang, Xu and Yan 2016, Sci. Adv. 2, e1501602, states the hydrogen oxidation and evolution kinetics in alkali are "two orders of magnitude slower than that in acid on Pt". The factor stays UNSURE in its primary source |
| R55 Durst et al. 2015, JES 162(1) F190 | Search | Record exists; Table II values (0.135 at 313 K, 0.26 at 353 K) not seen by me, UNSURE beyond S3's reading |
| R42 Reynolds et al. 2023, IJHMT | Search | Record and abstract (sheet gyroid, one Nu–Re curve per TPMS type, correlation proposed) exist; authors not shown on the listing I saw; fluid not seen (UNSURE, as S3 said) |

S3's "Inputs to recheck" items that carry input values into the answer:

- AlSi10Mg conductivity: confirmed (above).
- Pt/C j₀ in acid at 298 K: not re-read; the answer uses S3's corrected 0.06–0.07.
- Lu and Zhao values: confirmed, with the electrolyte caveat.
- CED values (Nuss and Eckelman 2014, Table S38): not re-read; arithmetic re-checked.

Still UNSURE, and carrying B numbers, are the correlation constants nobody has read in a primary source:

- Shah–London polynomial and the 3.44 term
- Stephan constants
- Khan et al. pin forms
- Jakob/Holman friction
- Lee et al. spreading (now checked against an exact series to within 2 % on R_max)
- Teertstra PF12
- Bejan–Sciubba 2.7

My set-B check shows the plate headline is insensitive to the friction and Nusselt forms (within 0.6 %). That covers the plate result only; the pin result has no such check.

## What still needs external checking

1. **The single most decisive check:** a ducted wind-tunnel test, or a conjugate 3-D CFD with a resolved fin–channel geometry, of the optimised Cu plate sink (38 × 0.3 mm) against an Al (k ≈ 150–165) plate sink and an LPBF sheet-gyroid sink in the same 60 × 60 × 35 mm envelope, on R_th against fan power over 0.03–0.3 W of air power. It settles the 9–21 % (or 10–26 %) plate penalty, the mixed-against-unmixed closure question, and the gyroid's real j/f (the parametric χ, c_f and k_eff), which is the only route by which the lattice part of claim B could survive.
2. Measured effective conductivity of thin-walled LPBF AlSi10Mg sheet gyroids (Catchpole-Smith 2019 and Sélo 2020 full texts) to replace the Hashin–Shtrikman bound (finding 4).
3. A 3-D conduction calculation, or a test, of a Cu-slug or Cu-base hybrid with Al fins under a concentrated source (finding 2), including the Cu–Al contact resistance, which I did not model.
4. Primary-source values for the correlation constants listed above, especially the pin friction and Nusselt forms, which have no independent check.
5. For claim C: a cell-level comparison at 1 A/cm² (AEM or zero-gap NiFe anode against PEM IrOx anode) with measured high-frequency resistance, and measured KOH conductivities at 25 and 80 °C. The porous-electrode cap uses an assumed κ.
6. Fan efficiency against operating point for 60 mm class fans, and the duty cycle. Both scale every fan-energy number linearly.
