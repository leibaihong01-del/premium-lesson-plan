# -*- coding: utf-8 -*-
"""PDF空间证据层独立验证：只做事实提取，不做任何质量判断。"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core"))

from pdf_layout_evidence import extract_pdf_evidence, reference_layout_evidence
from result_document_parser import parse as parse_result

COURSEAGENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = os.path.dirname(COURSEAGENT)
WS = os.path.join(PROJECT, "毕业设计智能制作工作区")
DIRECTION = "03_电梯系统"
STUDENT = "陈家宝"
TOPIC = "橘子洲南站自动扶梯扶手带检修方案设计"
PACKAGE = os.path.join(WS, "06_输出成果", DIRECTION, STUDENT + "_毕业设计完整成果包")
PROCESS = os.path.join(PACKAGE, "_过程记录")
RESULT_PDF = os.path.join(PROCESS, "02 %s 毕业设计成果 %s.pdf" % (STUDENT, TOPIC))
RESULT_DOCX = os.path.join(PACKAGE, "02 %s 毕业设计成果 %s.docx" % (STUDENT, TOPIC))
OUTPUT_DIR = os.path.join(COURSEAGENT, "output")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    evidence = extract_pdf_evidence(RESULT_PDF)
    model = parse_result(RESULT_DOCX, RESULT_PDF)
    references = model.get("references", [])
    mapping = reference_layout_evidence(evidence, references)

    pages_out = []
    if "pages" in evidence:
        for page in evidence["pages"]:
            lines = []
            for idx, line in enumerate(page.get("lines", []), 1):
                lines.append({
                    "line_id": line.get("line_id") or "p%s_l%03d" % (page.get("page"), idx),
                    "text": line.get("text", ""),
                    "bbox": {
                        "x0": line.get("x0"),
                        "x1": line.get("x1"),
                        "top": line.get("y0"),
                        "bottom": line.get("y1"),
                    },
                })
            pages_out.append({"page_number": page.get("page"), "lines": lines})

    candidates = []
    for m in mapping:
        if m.get("error"):
            continue
        lines = []
        ref_text = references[m["reference_index"]].get("text", "") if m["reference_index"] < len(references) else ""
        lines.append({"text": ref_text.split("\n")[0][:80], "page": m.get("page"),
                      "x0": m.get("first_line_x")})
        if m.get("continuation_x") is not None:
            lines.append({"text": "续行", "page": m.get("page"), "x0": m.get("continuation_x")})
        candidates.append({"reference_id": m.get("reference_no", "").strip("[]"),
                           "lines": lines})

    payload = {
        "document": os.path.basename(RESULT_PDF),
        "extractor": {"library": "pdfplumber"},
        "pages": pages_out,
        "reference_candidates": candidates,
    }
    json_path = os.path.join(OUTPUT_DIR, "pdf_layout_test.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    total_lines = sum(len(p["lines"]) for p in pages_out)
    cn_lines = sum(1 for p in pages_out for l in p["lines"] if any("\u4e00" <= ch <= "\u9fff" for ch in l["text"]))
    report = []
    report.append("# PDF空间证据层测试报告")
    report.append("")
    report.append("## 1. 环境")
    report.append("")
    report.append("- Python：%s" % sys.version.split()[0])
    report.append("- pdfplumber：available")
    report.append("- fitz：not used")
    report.append("")
    report.append("## 2. 提取结果")
    report.append("")
    report.append("- PDF页数：%s" % evidence.get("page_count", "?"))
    report.append("- 文本行数量：%s" % total_lines)
    report.append("- 中文文本行数量：%s" % cn_lines)
    report.append("- 参考文献候选数量：%s" % len(candidates))
    report.append("")
    report.append("## 3. 样例展示")
    report.append("")
    sample_normal = None
    sample_ref = candidates[0] if candidates else None
    for p in pages_out:
        for l in p["lines"]:
            if not any("\u4e00" <= ch <= "\u9fff" for ch in l["text"]):
                continue
            sample_normal = {"page": p["page_number"], "text": l["text"][:60], "x0": l["bbox"]["x0"]}
            break
        if sample_normal:
            break
    if sample_normal:
        report.append("- 普通正文行：page=%s text=%s x0=%s" % (sample_normal["page"], sample_normal["text"], sample_normal["x0"]))
    if sample_ref:
        report.append("- 参考文献条目：id=%s" % sample_ref["reference_id"])
        for line in sample_ref["lines"]:
            report.append("  - page=%s text=%s x0=%s" % (line["page"], line["text"], line["x0"]))
    report.append("")
    report.append("## 4. 结论")
    report.append("")
    report.append("本阶段仅完成空间事实提取，未做任何格式/质量判断。")
    md_path = os.path.join(OUTPUT_DIR, "PDF空间证据层测试报告.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report))

    print(json.dumps({
        "pages": evidence.get("page_count"),
        "lines": total_lines,
        "cn_lines": cn_lines,
        "reference_candidates": len(candidates),
        "json": json_path,
        "report": md_path,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())