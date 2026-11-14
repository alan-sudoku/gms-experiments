#!/usr/bin/env python3
"""Data preparation (offline): extract the C1 column (crust, 'CRC Handbook') of the first table of the Wikipedia data page raw wikitext
data/raw/wiki_abund.txt into data/crust_abundance_secondary.csv (mg/kg = kg/kg x 1e6).
STATUS: SECONDARY reproduction of the CRC Handbook of Chemistry and Physics table 'Abundance of Elements in the Earth's Crust and in the Sea'
(Wikipedia attributes column C1 to the CRC Handbook; edition not stated on the page, UNSURE). NOT an accepted primary LOOKUP; used only as a
cross-check beside the planner's values. Source URL https://en.wikipedia.org/wiki/Abundances_of_the_elements_(data_page), access 2026-11-14.
"""
import re, os
HERE = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(HERE, "data", "raw", "wiki_abund.txt"), encoding="utf-8").read()
first = t.split("==Earth bulk continental crust and upper continental crust==")[1].split("\n==")[0]
rows = re.split(r"\n\|-\n", first)
out = {}
for r in rows:
    m = re.search(r"<!--\s*(\d+)\s+([A-Z][a-z]?)\s*-->", r)
    if not m: continue
    z, sym = int(m.group(1)), m.group(2)
    c1 = re.search(r"<!--C1-->[^\n]*?data-sort-value=\"([0-9.eE+-]+)\"", r)
    if c1: out[sym] = (z, float(c1.group(1))*1e6)
with open(os.path.join(HERE, "data", "crust_abundance_secondary.csv"), "w") as f:
    f.write("# SECONDARY source: Wikipedia 'Abundances of the elements (data page)', column C1 = CRC Handbook crust mass fraction (kg/kg x 1e6 = mg/kg); url https://en.wikipedia.org/wiki/Abundances_of_the_elements_(data_page); access 2026-11-14; CRC edition not stated (UNSURE)\n")
    f.write("# NOT an accepted primary lookup (see issues_b.md)\nsymbol,Z,crust_mg_per_kg\n")
    for s, (z, v) in sorted(out.items(), key=lambda kv: kv[1][0]): f.write("%s,%d,%.6g\n" % (s, z, v))
print(len(out), "elements")
