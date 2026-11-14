#!/usr/bin/env python3
"""S5 review, task (1b): find every numeric token in prompt_5_answer.md and look for it in the committed outputs.
A number counts as found if its exact text appears in any outputs/*.txt or *.csv (after stripping thin spaces),
or if a printed number in the outputs rounds to it (same number of decimals). Prints the not-found tokens with
their answer line, for manual triage. Heuristic only: a found number may still be quoted out of context.
Usage: python3 r1_answer_numbers.py   Level: derived.
"""
import os, re, glob
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.normpath(os.path.join(HERE, ".."))
ans = open(os.path.join(R, "prompt_5_answer.md"), encoding="utf-8").read().splitlines()
blob = ""
for f in glob.glob(os.path.join(R, "prompt_5_code", "outputs", "*")) + glob.glob(os.path.join(R, "prompt_5_code", "data", "*.csv")):
    blob += open(f, encoding="utf-8", errors="replace").read() + "\n"
out_nums = set(re.findall(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", blob.replace(",", "")))
out_vals = []
for t in out_nums:
    try: out_vals.append(float(t))
    except ValueError: pass
out_vals = sorted(set(out_vals))
import bisect
def found(tok):
    t = tok.replace(" ", "").replace(" ", "").replace(" ", "")
    if t in blob: return True
    try: v = float(t)
    except ValueError: return True
    if v == 0: return True
    dec = len(t.split(".")[1].split("e")[0]) if "." in t else 0
    tol = 0.5 * 10 ** (-dec) if "e" not in t.lower() else abs(v) * 0.005
    i = bisect.bisect_left(out_vals, v - tol)
    while i < len(out_vals) and out_vals[i] <= v + tol:
        return True
    # percent or scaled forms (e.g. 0.937 printed as 93.7)
    for s in (100, 0.01, 1e3, 1e-3, 1e6, 1e-6):
        w = v * s; tl = tol * s
        i = bisect.bisect_left(out_vals, w - abs(tl))
        if i < len(out_vals) and out_vals[i] <= w + abs(tl): return True
    return False
skip_sections = ("## 5. Citations",)
insec = True; nf = []; ntot = 0
for ln_no, line in enumerate(ans, 1):
    if line.startswith("## 5. Citations"): insec = False
    if line.startswith("## 6."): insec = True
    if not insec: continue
    # join thin-space thousands "243 000" -> 243000
    l2 = re.sub(r"(\d) (\d{3})(?!\d)", r"\1\2", line)
    l2 = l2.replace("·10", "e").replace("×10", "e")
    for m in re.finditer(r"(?<![A-Za-z_\-\d.])(\d+\.\d+(?:e[-+]?\d+)?|\d+e[-+]?\d+|\d{3,})(?![\d])", l2):
        tok = m.group(1)
        ntot += 1
        if not found(tok): nf.append((ln_no, tok, line.strip()[:140]))
print("numeric tokens checked (outside the citation table): %d; not found in outputs/data: %d" % (ntot, len(nf)))
for ln_no, tok, ctx in nf: print("  line %4d  %-12s | %s" % (ln_no, tok, ctx))
