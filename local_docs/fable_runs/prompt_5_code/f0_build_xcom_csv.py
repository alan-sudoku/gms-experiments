#!/usr/bin/env python3
"""Data preparation (offline): convert raw NIST XCOM / NISTIR 5632 HTML downloads in data/raw/
into CSV lookup files in data/. Reads only data/raw/*.html as text (never executes anything).

Spec rows served: F1-F7. No physics here; only parsing.
Outputs: data/xcom_z<ZZZ>.csv (partial + total, cm2/g, standard XCOM grid with edge rows),
         data/nist_comtab_water.csv, data/nist_comtab_concrete.csv, data/nist_eltab_z<ZZ>.csv (totals).
"""
import re, os, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "data", "raw")
DATA = os.path.join(HERE, "data")
NUM = r"[0-9]\.[0-9]{3,5}E[+-][0-9]{2}"

def text_of(fn):
    s = open(os.path.join(RAW, fn), encoding="latin-1").read()
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]*>", " ", s)
    return H.unescape(s).replace("\xa0", " ")

def xcom(z, name):
    t = text_of("xcom_z%d.html" % z)
    rows = []
    for line in t.splitlines():
        line = line.strip()
        # data rows: optionally "<Z> <edge>" then energy and 7 values; plain rows are glued together
        m = re.match(r"^(?:(\d+)\s+([KLMN]\d?)\s+)?((?:%s){8})$" % NUM, line.replace(" ", "")) if False else None
        toks = re.findall(NUM, line)
        if len(toks) == 8 and re.fullmatch(r"(?:\d+\s+[KLMN]\d?\s+)?(?:%s\s*){8}" % NUM, line):
            edge = ""
            me = re.match(r"^(\d+)\s+([KLMN]\d?)\s", line)
            if me: edge = me.group(2)
            rows.append([edge] + [float(x) for x in toks])
    return rows

def write_xcom(z, sym, ver):
    rows = xcom(z, sym)
    fn = os.path.join(DATA, "xcom_z%03d.csv" % z)
    with open(fn, "w") as f:
        f.write("# source: Berger M.J., Hubbell J.H., Seltzer S.M., Chang J., Coursey J.S., Sukumar R., Zucker D.S., Olsen K. "
                "XCOM: Photon Cross Sections Database, NIST Standard Reference Database 8 (XGAM), web form, Method=Elem Z=%d (%s), "
                "output in cm2/g, standard grid plus edges.\n" % (z, sym))
        f.write("# url: https://physics.nist.gov/cgi-bin/Xcom/xcom2 (POST to /cgi-bin/Xcom/xcom3_1); raw page data/raw/xcom_z%d.html\n" % z)
        f.write("# version: %s\n" % ver)
        f.write("# access date: 2026-11-14\n")
        f.write("# note: at an absorption edge XCOM prints two rows with the same energy: first the pre-edge row (edge column empty), then the post-edge row labelled with the shell (K, L1, ...). Row order is preserved.\n")
        f.write("edge,E_MeV,coherent,incoherent,photoelectric,pair_nuclear,pair_electron,total_with_coh,total_without_coh\n")
        for r in rows:
            f.write(",".join([r[0]] + ["%.4E" % x for x in r[1:]]) + "\n")
    return len(rows)

def comtab(fn_html, fn_csv, title, extra):
    t = text_of(fn_html)
    nums = []
    out = []
    # table lines: energy  mu/rho  muen/rho, with optional edge labels like "11 K"
    toks = t.split("\n")
    buf = []
    for line in toks:
        line = line.strip()
        if not line: continue
        buf.append(line)
    # flatten to tokens
    flat = " ".join(buf)
    flat = re.sub(r"\b(\d+)\s+([KLMN]\d?)\b", r" EDGE\2 ", flat)
    parts = flat.split()
    i = 0; rows = []; edge = ""
    while i < len(parts):
        p = parts[i]
        if p.startswith("EDGE"):
            edge = p[4:]; i += 1; continue
        if re.fullmatch(r"[0-9]\.[0-9]{5}E[+-][0-9]{2}", p) and i + 2 < len(parts) \
           and re.fullmatch(r"[0-9]\.[0-9]{3}E[+-][0-9]{2}", parts[i+1]) and re.fullmatch(r"[0-9]\.[0-9]{3}E[+-][0-9]{2}", parts[i+2]):
            rows.append((edge, float(p), float(parts[i+1]), float(parts[i+2]))); edge = ""; i += 3
        else:
            i += 1
    # edge labels precede the row they belong to in this layout only approximately; keep them informational
    with open(os.path.join(DATA, fn_csv), "w") as f:
        f.write("# source: Hubbell J.H., Seltzer S.M. (2004) Tables of X-Ray Mass Attenuation Coefficients and Mass Energy-Absorption Coefficients (version 1.4), NIST, originally NISTIR 5632 (1995); %s\n" % title)
        f.write("# url: %s\n" % extra)
        f.write("# version: NIST web edition of NISTIR 5632 tables (version 1.4 per NIST; page text does not state it, UNSURE)\n")
        f.write("# access date: 2026-11-14\n")
        f.write("# note: mu/rho includes coherent scattering. edge column is informational only (label printed next to row in raw HTML).\n")
        f.write("edge,E_MeV,mu_rho_cm2_g,muen_rho_cm2_g\n")
        for r in rows:
            f.write("%s,%.5E,%.3E,%.3E\n" % r)
    return len(rows)

def tab1():
    t = text_of("tab1.html").split()
    with open(os.path.join(DATA, "nist_tab1_za.csv"), "w") as f:
        f.write("# source: Hubbell J.H., Seltzer S.M., Tables of X-Ray Mass Attenuation Coefficients and Mass Energy-Absorption Coefficients, NIST, Table 1 (material constants for elemental media: Z/A, I, density)\n")
        f.write("# url: https://physics.nist.gov/PhysRefData/XrayMassCoef/tab1.html\n# version: NIST web edition (UNSURE: v1.4)\n# access date: 2026-11-14\n")
        f.write("Z,symbol,Z_over_A,I_eV,density_g_cm3\n")
        for z in ["6","13","26","29","50","56","64","74","82","83"]:
            i = t.index(z)
            # layout: Z sym name... Z/A I rho ; name may have several words
            j = i + 2
            while not re.fullmatch(r"0\.[0-9]{5}", t[j]): j += 1
            f.write("%s,%s,%s,%s,%s\n" % (z, t[i+1], t[j], t[j+1], t[j+2]))

if __name__ == "__main__":
    tab1()
    ver = "XCOM web service output, page does not print a version number (UNSURE: XCOM 3.1, Berger et al. 2010 online edition)"
    for z, s in [(6,"C"),(13,"Al"),(26,"Fe"),(29,"Cu"),(50,"Sn"),(56,"Ba"),(64,"Gd"),(74,"W"),(82,"Pb"),(83,"Bi")]:
        print("xcom", z, s, write_xcom(z, s, ver))
    base = "https://physics.nist.gov/PhysRefData/XrayMassCoef/"
    print("water", comtab("c_water.html", "nist_comtab_water.csv", "Table 4, Water, Liquid", base + "ComTab/water.html"))
    print("concrete", comtab("c_concrete.html", "nist_comtab_concrete.csv", "Table 4, Concrete, Ordinary", base + "ComTab/concrete.html"))
    for z in [6,13,26,29,50,74,82]:
        print("el", z, comtab("z%02d.html" % z, "nist_eltab_z%02d.csv" % z, "Table 3, element Z=%d" % z, base + "ElemTab/z%02d.html" % z))
