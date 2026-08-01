# -*- coding: utf-8 -*-
"""高算力档视觉检查：PDF 页数、空白尾页、越界与底部空白。"""
import os

import pdfplumber
import pypdfium2 as pdfium


def check_pdf(pdf_path, max_mid_gap=40, max_first_gap=110):
    if not os.path.exists(pdf_path):
        return {"ok": False, "issues": ["PDF不存在"]}
    issues = []
    doc = pdfium.PdfDocument(pdf_path)
    pages = len(doc)
    last = doc[len(doc) - 1].render(scale=1.0).to_pil().convert("L")
    px = last.load()
    w, h = last.size
    dark = sum(1 for y in range(h) for x in range(w) if px[x, y] < 200)
    ink = 100 * dark / (w * h)
    doc.close()
    with pdfplumber.open(pdf_path) as pdf:
        gaps = []
        for i, pg in enumerate(pdf.pages):
            rects = [r for r in pg.rects if 70 < r["bottom"] < 790]
            if rects:
                bottom = max(r["bottom"] for r in rects)
                gap = 770 - bottom
                gaps.append(gap)
                if i != len(pdf.pages) - 1:
                    limit = max_first_gap if i == 0 else max_mid_gap
                    if gap > limit:
                        issues.append(f"P{i+1}底部空白{gap:.0f}pt超标")
            chars = pg.chars
            if chars:
                x1 = max(c["x1"] for c in chars)
                y1 = max(c["bottom"] for c in chars)
                if x1 > pg.width + 1 or y1 > pg.height + 1:
                    issues.append(f"P{i+1}越界")
        last_lines = [l for l in (pdf.pages[-1].extract_text() or "").splitlines() if l.strip()]
        if ink < 1.5 and len(last_lines) <= 1:
            issues.append("空白尾页")
    return {
        "pages": pages,
        "ok": not issues,
        "issues": issues,
        "mid_max": round(max(gaps[:-1]), 1) if len(gaps) > 1 else 0,
        "last_gap": round(gaps[-1], 1) if gaps else None,
    }
