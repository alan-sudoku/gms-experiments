#!/usr/bin/env python3
"""S5 review, task (1): re-run every prompt_5_code script in a scratch copy and diff against committed outputs.
Usage: python3 r0_rerun_all.py <scratch_dir>
Copies prompt_5_code/ to <scratch_dir>, runs data builders (offline, from data/raw), then every analysis
script with stdout -> outputs/<name>.txt (n1_fetch_endf_sigma.py is skipped: it needs the network).
Prints a diff summary (identical / differing lines, first differing lines). Level: derived.
"""
import os, sys, shutil, subprocess, difflib, time
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "prompt_5_code"))
S = sys.argv[1]
if os.path.exists(S): shutil.rmtree(S)
shutil.copytree(SRC, S, ignore=shutil.ignore_patterns("__pycache__"))
# keep committed copies for the diff
shutil.copytree(os.path.join(S, "outputs"), os.path.join(S, "outputs_committed"))
shutil.copytree(os.path.join(S, "data"), os.path.join(S, "data_committed"), ignore=shutil.ignore_patterns("raw"))
builders = ["f0_build_xcom_csv", "n0_build_atomic_weights_csv", "n0_build_crust_csv", "n0_build_sears_csv"]
for b in builders:
    r = subprocess.run([sys.executable, b + ".py"], cwd=S, capture_output=True, text=True)
    print("builder %-32s rc=%d" % (b, r.returncode))
for fn in sorted(os.listdir(os.path.join(S, "data_committed"))):
    a = open(os.path.join(S, "data", fn)).read(); c = open(os.path.join(S, "data_committed", fn)).read()
    print("  data/%-40s %s" % (fn, "identical" if a == c else "DIFFERS"))
order = ["a1_conductor_area_mass", "a2_kelvin_optimum", "a3_break_even_embodied", "a4_duty_crossover",
         "b1_b2_skin_dowell", "b3_ac_ratio_strip", "c1_fin_efficiency", "c2_c3_optimum_fin", "c4_pumping_price",
         "d1_overpotential", "d2_porous_electrode", "d3_break_even_overpotential", "e1_voxel_conduction",
         "f1_mass_attenuation", "f2_ratio_crossings", "f3_thickness_ratio", "f4_photoelectric_exponents",
         "f5_nonuniform_shield", "f6_buildup_mc", "f7_kedge_window", "h1_h2_redox_dl_energy", "h3_ragone_crossover",
         "m1_m2_ceiling_hardness", "m3_shape_anisotropy", "m4_exchange_spring", "m5_magnet_circuit",
         "n1_thermal_ri", "n2_one_over_v_test", "n3_self_shielding", "n4_moderation", "n5_water_vs_cd",
         "n6_abundance_production", "p1_heat_pipe", "t1_transparent_conductor", "j1_gate_matrix", "s4_checks"]
print("\nscript                         rc  secs  lines(new/old)  differing  ")
for name in order:
    t0 = time.time()
    r = subprocess.run([sys.executable, name + ".py"], cwd=S, capture_output=True, text=True)
    out = os.path.join(S, "outputs", name + ".txt")
    open(out, "w").write(r.stdout)
    old = open(os.path.join(S, "outputs_committed", name + ".txt")).read().splitlines()
    new = r.stdout.splitlines()
    d = [l for l in difflib.unified_diff(old, new, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    print("%-30s %2d %5.0f  %5d/%-5d  %4d" % (name, r.returncode, time.time() - t0, len(new), len(old), len(d)))
    if r.stderr.strip(): print("   stderr:", r.stderr.strip().splitlines()[-1][:150])
    for l in d[:8]: print("   ", l[:170])
# n1_values.csv
a = open(os.path.join(S, "outputs", "n1_values.csv")).read(); c = open(os.path.join(S, "outputs_committed", "n1_values.csv")).read()
print("\noutputs/n1_values.csv", "identical" if a == c else "DIFFERS")
