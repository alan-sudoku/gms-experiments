"""OCR a scanned PDF page range to text. Usage: python ocr_pdf.py in.pdf out.txt"""
import sys, fitz, numpy as np
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
doc = fitz.open(sys.argv[1])
out = []
for i, p in enumerate(doc):
    pix = p.get_pixmap(dpi=200)
    img = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)
    res, _ = ocr(img)
    out.append(f"=== page {i+1} ===")
    if res:
        for box, txt, sc in sorted(res, key=lambda r: (round(r[0][0][1]/15), r[0][0][0])):
            out.append(txt)
open(sys.argv[2], "w").write("\n".join(out))
print(len(doc), "pages")
