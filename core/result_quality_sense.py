# -*- coding: utf-8 -*-
"""Result Quality Sense：只消费 DocumentStructure / ResultSemanticStructure，不做文档解析。"""
import re

EXPECTED_BODY_FONT = 12.0
EXPECTED_SECTIONS = 4
EXPECTED_TABLES = 6
FORBIDDEN_PATTERNS = ["本文研究了", "本文研究", "本文", "本研究", "笔者", "论文", "学术研究", "课题研究", "文献研究", "研究成果"]
PLACEHOLDER_PATTERNS = ["待完善", "待补充", "XXX", "TODO", "后续添加"]


def _bigrams(text):
    text = re.sub(r"\s+", "", text or "")
    return {text[i:i+2] for i in range(max(0, len(text) - 1))}


class BaseSense:
    name = "BaseSense"

    def check(self, model, profile=None, context=None, **kwargs):
        return {"sense": self.name, "status": "unknown", "checks": []}


class ContentQualitySense(BaseSense):
    name = "Content Quality Sense"

    def check(self, model, profile=None, context=None, taskbook_structure=None):
        full = model.get("full_text", "")
        fields = model.get("fields", {})
        evidence = model.get("evidence", [])
        checks = []

        if profile is not None:
            for key, value in [
                ("student_name", profile.student_name),
                ("student_id", profile.student_id),
                ("class_name", profile.class_name),
                ("advisor", profile.advisor),
                ("topic", profile.topic),
            ]:
                field = fields.get(key, {})
                field_value = field.get("value", "")
                ev = next((e for e in evidence if e.get("field") == key), None)
                if field_value and value and value in field_value:
                    checks.append({"type": "student_identity", "field": key, "value": field_value,
                                   "source": ev.get("source_location") if ev else None,
                                   "status": "pass"})
                elif field_value or (value and value in full):
                    checks.append({"type": "student_identity", "field": key,
                                   "value": field_value or value, "source": "full_text",
                                   "status": "pass"})
                else:
                    checks.append({"type": "student_identity", "field": key, "value": None,
                                   "status": "fail"})

        topic_ok = bool(profile and profile.topic and profile.topic in full)
        checks.append({"type": "task_match", "field": "topic", "present": topic_ok,
                       "status": "pass" if topic_ok else "fail"})

        task_text = ""
        if taskbook_structure is not None:
            for table in taskbook_structure.get("tables", []):
                for row in table.get("row_cells", []):
                    if not row:
                        continue
                    ri = row[0].get("row")
                    if ri in (4, 5) and len(row) > 1:
                        task_text += (row[1].get("text") or "") + "\n"
        if task_text.strip():
            cov = len(_bigrams(full) & _bigrams(task_text)) / max(1, len(_bigrams(task_text)))
            checks.append({"type": "task_match", "field": "taskbook_coverage",
                           "coverage": round(cov, 3), "status": "pass" if cov >= 0.15 else "review"})
        else:
            checks.append({"type": "task_match", "field": "taskbook_source", "status": "review",
                           "detail": "任务书未提供或未解析到设计目标/任务"})

        for pat in FORBIDDEN_PATTERNS:
            if pat in full:
                checks.append({"type": "content_rule", "rule": "forbidden_expression",
                               "expression": pat, "status": "fail"})
        for pat in PLACEHOLDER_PATTERNS:
            if pat in full:
                checks.append({"type": "content_rule", "rule": "placeholder",
                               "expression": pat, "status": "fail"})

        status = "fail" if any(c.get("status") == "fail" for c in checks) else (
            "review" if any(c.get("status") == "review" for c in checks) else "pass")
        return {"sense": self.name, "status": status, "checks": checks}


class StructureQualitySense(BaseSense):
    name = "Structure Quality Sense"

    def check(self, model, profile=None, context=None, **kwargs):
        checks = []
        sections = model.get("sections", [])
        headings = [s for s in sections if s.get("level") in (1, 2)]
        level1 = [s for s in headings if s.get("level") == 1]
        level2 = [s for s in headings if s.get("level") == 2]

        checks.append({"type": "heading_count", "level1": len(level1), "level2": len(level2),
                       "status": "pass" if len(level1) >= 5 and len(level2) >= 5 else "review"})

        nums = []
        for s in headings:
            m = re.match(r"^(\d+(?:\.\d+)*)", s.get("section", "").strip())
            if m:
                nums.append(m.group(1))
        dup = sorted({n for n in set(nums) if nums.count(n) > 1})
        if dup:
            checks.append({"type": "heading_duplicate", "numbers": sorted(set(dup)), "status": "fail"})

        toc_ok = model.get("toc_field_present", False)
        checks.append({"type": "toc_field", "present": toc_ok,
                       "status": "pass" if toc_ok else "fail"})

        captions = model.get("captions", [])
        table_caps = [c for c in captions if c.get("type") == "表注"]
        figure_caps = [c for c in captions if c.get("type") == "图注"]
        checks.append({"type": "caption_count", "table": len(table_caps), "figure": len(figure_caps),
                       "status": "pass" if table_caps else "review"})

        ref_ok = model.get("reference_count", 0) > 0
        checks.append({"type": "references_present", "count": model.get("reference_count", 0),
                       "status": "pass" if ref_ok else "fail"})

        tkm_tables = None
        if context is not None and hasattr(context, "tkm"):
            tkm_tables = context.tkm.get("tables")
        tables_count = len(model.get("tables", []))
        expected = tkm_tables or EXPECTED_TABLES
        checks.append({"type": "table_count", "generated": tables_count, "expected": expected,
                       "status": "pass" if tables_count == expected else "review"})

        status = "fail" if any(c.get("status") == "fail" for c in checks) else (
            "review" if any(c.get("status") == "review" for c in checks) else "pass")
        return {"sense": self.name, "status": status, "checks": checks}


class LayoutQualitySense(BaseSense):
    name = "Layout Quality Sense"

    def check(self, model, profile=None, context=None, template_pdf_path=None, **kwargs):
        checks = []
        pdf = model.get("pages", {})
        pages = pdf.get("count")
        expected_pages = None
        if template_pdf_path and template_pdf_path != "":
            try:
                import os
                if os.path.isfile(template_pdf_path):
                    from pypdf import PdfReader
                    expected_pages = len(PdfReader(template_pdf_path).pages)
            except Exception:
                expected_pages = None
        checks.append({"type": "page_count", "generated": pages, "expected": expected_pages,
                       "status": "pass" if pages and expected_pages and pages == expected_pages else "review"})

        per_page = pdf.get("per_page_chars", [])
        blank = [i + 1 for i, n in enumerate(per_page) if n == 0]
        checks.append({"type": "blank_pages", "pages": blank, "status": "review" if blank else "pass"})

        sizes = model.get("body_font_sizes", [])
        checks.append({"type": "body_font_size", "sizes": sizes,
                       "status": "pass" if EXPECTED_BODY_FONT in sizes else "review"})

        sections_count = model.get("sections_count")
        checks.append({"type": "sections_count", "count": sections_count,
                       "status": "pass" if sections_count == EXPECTED_SECTIONS else "review"})

        status = "fail" if any(c.get("status") == "fail" for c in checks) else (
            "review" if any(c.get("status") == "review" for c in checks) else "pass")
        return {"sense": self.name, "status": status, "checks": checks}