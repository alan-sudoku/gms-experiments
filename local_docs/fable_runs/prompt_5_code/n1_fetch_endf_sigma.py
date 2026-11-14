#!/usr/bin/env python3
"""Data-preparation script (network): download reconstructed pointwise ENDF/B-VII.1
cross sections from NNDC Sigma (https://www.nndc.bnl.gov/sigma/) for the nuclides used in row N1.

Spec rows: N1 (and N2, N3, N5 which read N1 values). This script only DOWNLOADS text data
(never executes it) into data/raw/endf_sigma/<nuclide>_mt<MT>.txt. The analysis script
n1_thermal_ri.py reads those files offline.
MTs fetched when present: 102 (n,gamma), 103 (n,p), 105 (n,t), 107 (n,alpha).
Access date of the stored files: 2026-11-14.
"""
import re, os, sys, time, urllib.request, urllib.parse, http.cookiejar

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", "raw", "endf_sigma")
BASE = "https://www.nndc.bnl.gov/sigma/"
NUCLIDES = ("H-1 Li-6 B-10 B-11 C-12 C-13 Al-27 Fe-54 Fe-56 Fe-57 Fe-58 Ag-107 Ag-109 "
            "Cd-106 Cd-108 Cd-110 Cd-111 Cd-112 Cd-113 Cd-114 Cd-116 In-113 In-115 "
            "Sm-144 Sm-147 Sm-148 Sm-149 Sm-150 Sm-152 Sm-154 Eu-151 Eu-153 "
            "Gd-152 Gd-154 Gd-155 Gd-156 Gd-157 Gd-158 Gd-160 "
            "Dy-156 Dy-158 Dy-160 Dy-161 Dy-162 Dy-163 Dy-164 "
            "Hf-174 Hf-176 Hf-177 Hf-178 Hf-179 Hf-180 C-0:C").split()   # file name C-0 (query "C") = natural carbon (ENDF/B-VII.1 has no C-12/C-13)
if len(sys.argv) > 1:
    NUCLIDES = sys.argv[1:]      # optional subset
MTS = [102, 103, 105, 107]

def opener():
    cj = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def get(op, url, data=None):
    if data is not None:
        data = urllib.parse.urlencode(data).encode()
    for attempt in range(3):
        try:
            with op.open(urllib.request.Request(url, data=data), timeout=90) as r:
                return r.read().decode("latin-1")
        except Exception as e:
            time.sleep(2)
    raise RuntimeError("failed " + url)

def main():
    os.makedirs(OUT, exist_ok=True)
    log = []
    for entry in NUCLIDES:
        nuc, _, query = entry.partition(":")
        query = query or nuc
        op = opener()
        if all(os.path.exists(os.path.join(OUT, "%s_mt%d.txt" % (nuc, mt))) for mt in (102,)):
            continue
        html = get(op, BASE + "basicresults.jsp",
                   dict(target=query, z="", a="", reaction="n", quantity="cs", library="endfb7.1", sub="Submit"))
        ids = set(re.findall(r"evalid=(\d+)&mf=3&mt=102\"", html))
        if len(ids) != 1:
            log.append((nuc, "NO_UNIQUE_EVALID", sorted(ids))); continue
        ev = ids.pop()
        have = sorted(set(int(m) for m in re.findall(r"evalid=%s&mf=3&mt=(\d+)\"" % ev, html)))
        for mt in MTS:
            if mt not in have:
                continue
            fn = os.path.join(OUT, "%s_mt%d.txt" % (nuc, mt))
            if os.path.exists(fn):
                continue
            get(op, BASE + "getPlot.jsp?evalid=%s&mf=3&mt=%d&nsub=Neutron%%20reactions" % (ev, mt))
            pd = get(op, BASE + "getPlotData.jsp")
            m = re.search(r'href="(temp/endf-6-\d+\.txt)"', pd)
            if not m:
                log.append((nuc, mt, "NO_LINK")); continue
            txt = get(op, BASE + m.group(1))
            with open(fn, "w") as f:
                f.write("# source: NNDC Sigma, evalid %s, MF3 MT%d; url %s%s; access 2026-11-14\n" % (ev, mt, BASE, m.group(1)))
                f.write(txt)
            log.append((nuc, mt, "ok", ev, len(txt)))
    for l in log: print(l)

if __name__ == "__main__":
    main()
