#!/usr/bin/env python3
"""Data preparation (offline): parse the raw Sears (1992) table page data/raw/sears_list.html into data/sears_1992_table1.csv.
Source: V.F. Sears, 'Neutron scattering lengths and cross sections', Neutron News 3(3), 1992, 26-37 (Table 1), as
reproduced by NIST NCNR https://www.ncnr.nist.gov/resources/n-lengths/list.html (access 2026-11-14).
Columns kept: isotope label, natural abundance (percent; '---' for natural-element rows; half-life text for radioisotopes),
absorption cross section for 2200 m/s neutrons (barn, uncertainty in parentheses stripped), and the raw string.
"""
import os, re, html
HERE = os.path.dirname(os.path.abspath(__file__))
raw = open(os.path.join(HERE, "data", "raw", "sears_list.html"), encoding="latin-1").read()
rows = []
for chunk in re.split(r"<tr>", raw, flags=re.I):
    if "<td>" not in chunk: continue
    cells = [html.unescape(re.sub(r"<[^>]*>", "", c)).strip() for c in chunk.split("<td>")[1:]]
    if len(cells) != 8: continue
    label, conc, absxs = cells[0], cells[1], cells[7]
    if not re.fullmatch(r"\d*[A-Z][a-z]?", label): continue
    m = re.match(r"^([<>]?[0-9.eE+-]+)", absxs.replace(" ", ""))
    val = m.group(1) if m else ""
    rows.append((label, conc, val, absxs))
with open(os.path.join(HERE, "data", "sears_1992_table1.csv"), "w") as f:
    f.write("# source: Sears V.F. (1992) Neutron scattering lengths and cross sections, Neutron News 3(3) 26-37, Table 1, as reproduced at NIST NCNR\n")
    f.write("# url: https://www.ncnr.nist.gov/resources/n-lengths/list.html\n# edition: 1992 (web copy; page date not stated, UNSURE)\n# access date: 2026-11-14\n")
    f.write("# note: abs_xs_b is the absorption cross section for 2200 m/s neutrons in barn (uncertainty dropped); conc is natural abundance in percent for isotopes, '---' for natural-element rows\n")
    f.write("label,conc,abs_xs_b,raw_abs\n")
    for r in rows: f.write(",".join('"%s"' % x if "," in x else x for x in r) + "\n")
print(len(rows), "rows")
