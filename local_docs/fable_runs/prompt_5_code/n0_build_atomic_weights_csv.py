#!/usr/bin/env python3
"""Data preparation (offline): parse data/raw/nist_atomic_weights.html into data/nist_atomic_weights.csv.
Source: NIST, Atomic Weights and Isotopic Compositions for All Elements (IUPAC standard atomic weights), 
https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl , access 2026-11-14. For elements with an interval the midpoint is stored
(raw interval kept); relative half-width is below 0.1% for every element used in this plan.
"""
import os, re, html
HERE = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(HERE, "data", "raw", "nist_atomic_weights.html"), encoding="latin-1").read()
t = html.unescape(re.sub(r"<[^>]*>", "\n", t)).replace("\xa0", " ")
lines = [l.strip() for l in t.splitlines() if l.strip()]
rows = {}; z = sym = None
for l in lines:
    m = re.match(r"Atomic Number = (\d+)", l)
    if m: z = int(m.group(1)); continue
    m = re.match(r"Atomic Symbol = (\w+)", l)
    if m: sym = m.group(1); continue
    m = re.match(r"Standard Atomic Weight = (.*)", l)
    if m and z is not None and z not in rows:
        raw = m.group(1).strip()
        iv = re.match(r"\[([0-9.]+),([0-9.]+)\]", raw)
        if iv: val = 0.5*(float(iv.group(1)) + float(iv.group(2)))
        else:
            mv = re.match(r"([0-9.]+)", raw); val = float(mv.group(1)) if mv else float("nan")
        rows[z] = (sym, val, raw)
with open(os.path.join(HERE, "data", "nist_atomic_weights.csv"), "w") as f:
    f.write("# source: NIST Atomic Weights and Isotopic Compositions for All Elements (IUPAC standard atomic weights); url https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl ; access date 2026-11-14\n")
    f.write("# note: interval entries stored as midpoint; 'raw' column holds the string as printed\nZ,symbol,A_r,raw\n")
    for z, (s, v, raw) in sorted(rows.items()): f.write('%d,%s,%.6f,"%s"\n' % (z, s, v, raw))
print(len(rows), "elements")
