# -*- coding: utf-8 -*-
"""PDF Layout Evidence：从 PDF 提取页面、文本块、行与坐标（旁路验证能力）。"""
import os
import re


def extract_pdf_evidence(pdf_path):
    if not pdf_path or not os.path.isfile(pdf_path):
        return {"error": "pdf_missing"}
    try:
        import pdfplumber
    except Exception as e:
        return {"error": "pdfplumber_missing", "detail": repr(e)}
    pages = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for pi, page in enumerate(pdf.pages):
                words = page.extract_words()
                blocks = []
                lines = []
                # 按 top 聚类为视觉行
                grouped = {}
                for w in words:
                    key = round(w["top"] / 3.0) * 3
                    grouped.setdefault(key, []).append(w)
                for gi, (top_key, ws) in enumerate(sorted(grouped.items())):
                    ws.sort(key=lambda x: x["x0"])
                    text = "".join(w["text"] for w in ws)
                    x0 = min(w["x0"] for w in ws)
                    x1 = max(w["x1"] for w in ws)
                    y0 = min(w["top"] for w in ws)
                    y1 = max(w["bottom"] for w in ws)
                    lines.append({
                        "line_id": "p%s_line%s" % (pi + 1, gi + 1),
                        "text": text,
                        "x0": round(x0, 1),
                        "x1": round(x1, 1),
                        "y0": round(y0, 1),
                        "y1": round(y1, 1),
                    })
                pages.append({
                    "page": pi + 1,
                    "words_count": len(words),
                    "lines": lines,
                    "blocks": blocks,
                })
    except Exception as e:
        return {"error": "extract_failed", "detail": repr(e)}
    return {"pages": pages, "page_count": len(pages)}


def reference_layout_evidence(pdf_evidence, references):
    """把参考文献文本映射到 PDF 视觉行，输出首行/续行坐标。"""
    if not pdf_evidence or "pages" not in pdf_evidence:
        return []
    markers = []
    for ref in references:
        m = re.match(r"^\s*[\[（(]?(\d+)[\]）)]?", ref.get("text", ""))
        markers.append(m.group(1) if m else "")
    results = []
    for idx, ref in enumerate(references):
        marker = markers[idx]
        if not marker:
            results.append({"reference_index": idx, "paragraph_id": ref.get("index"), "error": "no_marker"})
            continue
        found = None
        page_no = None
        for page in pdf_evidence.get("pages", []):
            for line in page.get("lines", []):
                text = line.get("text", "")
                if text.startswith(marker + " ") or text.startswith("[" + marker + "]") or text.startswith(marker + "."):
                    found = line
                    page_no = page.get("page")
                    break
            if found:
                break
        if not found:
            results.append({"reference_index": idx, "paragraph_id": ref.get("index"), "error": "not_found"})
            continue
        # 从该行开始收集后续行，直到出现下一个文献编号
        lines = []
        capture = False
        for page in pdf_evidence.get("pages", []):
            for line in page.get("lines", []):
                text = line.get("text", "")
                if line is found:
                    capture = True
                if capture:
                    if lines and re.match(r"^\s*[\[（(]?\d+[\]）)]?", text):
                        break
                    lines.append(line)
        if not lines:
            lines = [found]
        first_line_x = lines[0].get("x0")
        continuation_x = lines[1].get("x0") if len(lines) > 1 else None
        offset = round((continuation_x - first_line_x), 1) if continuation_x is not None else None
        results.append({
            "reference_index": idx,
            "reference_no": "[" + marker + "]",
            "paragraph_id": ref.get("index"),
            "page": page_no,
            "first_line_x": round(first_line_x, 1) if first_line_x is not None else None,
            "continuation_x": round(continuation_x, 1) if continuation_x is not None else None,
            "offset_pt": offset,
            "line_count": len(lines),
        })
    return results