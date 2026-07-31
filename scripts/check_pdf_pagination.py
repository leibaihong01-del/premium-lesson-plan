#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check PDF pagination: page count, blank tail, overflow and page-bottom gaps."""
import argparse
import sys

import pdfplumber
import pypdfium2 as pdfium


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--max-mid-gap", type=float, default=40)
    ap.add_argument("--max-first-gap", type=float, default=110)
    args = ap.parse_args()
    issues = []
    doc = pdfium.PdfDocument(args.pdf)
    pages = len(doc)
    last = doc[len(doc) - 1].render(scale=1.0).to_pil().convert("L")
    px = last.load()
    w, h = last.size
    dark = sum(1 for y in range(h) for x in range(w) if px[x, y] < 200)
    ink = 100 * dark / (w * h)
    doc.close()
    with pdfplumber.open(args.pdf) as pdf:
        gaps = []
        last_idx = len(pdf.pages) - 1
        for i, pg in enumerate(pdf.pages):
            rects = [r for r in pg.rects if 70 < r["bottom"] < 790]
            if rects:
                bottom = max(r["bottom"] for r in rects)
                gap = 770 - bottom
                gaps.append(gap)
                if i != last_idx:
                    limit = args.max_first_gap if i == 0 else args.max_mid_gap
                    if gap > limit:
                        issues.append(f"P{i + 1}底部空白{gap:.0f}pt超标")
            chars = pg.chars
            if chars:
                x1 = max(c["x1"] for c in chars)
                y1 = max(c["bottom"] for c in chars)
                if x1 > pg.width + 1 or y1 > pg.height + 1:
                    issues.append(f"P{i + 1}越界")
        last_lines = [l for l in (pdf.pages[-1].extract_text() or "").splitlines() if l.strip()]
        if ink < 1.5 and len(last_lines) <= 1:
            issues.append("空白尾页")
    print(
        "pages:",
        pages,
        "midMax:",
        round(max(gaps[:-1]), 1) if len(gaps) > 1 else 0,
        "lastGap:",
        round(gaps[-1], 1) if gaps else None,
    )
    if issues:
        print("ISSUES:", "; ".join(issues))
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
