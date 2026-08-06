# -*- coding: utf-8 -*-
"""DocumentFieldExtractor：从 DocumentStructure 中识别身份/指导/课题字段，保留证据链。"""
import re

FIELD_LABELS = {
    "student_name": ["姓名"],
    "student_id": ["学号"],
    "class_name": ["班级名称", "班级"],
    "major": ["专业名称", "专业"],
    "college": ["二级学院", "学院"],
    "advisor": ["校内指导教师", "指导教师", "指导老师"],
    "topic": ["选题名称", "课题名称", "设计题目", "项目名称"],
}

INLINE_PATTERNS = {
    "student_name": re.compile(r"姓名[:：]\s*([^\s（(]+)"),
    "student_id": re.compile(r"学号[:：]\s*([^\s（(]+)"),
    "class_name": re.compile(r"班级[:：]\s*([^\s（(]+)"),
    "major": re.compile(r"专业[:：]\s*([^\s（(]+)"),
    "advisor": re.compile(r"指导教师[:：]\s*([^\s（(]+)"),
    "topic": re.compile(r"(?:选题名称|课题名称)[:：]\s*([^\n\r]+)"),
}


def _norm(text):
    return re.sub(r"[\s:：（）()【】\[\]]", "", text or "")


class DocumentFieldExtractor:
    def extract(self, structure):
        fields = {}
        evidence = []
        for table in structure.get("tables", []):
            tid = table.get("table_id")
            for row in table.get("row_cells", []):
                cells = [c.get("text", "").strip() for c in row]
                for ci, text in enumerate(cells):
                    if not text:
                        continue
                    norm = _norm(text)
                    for key, labels in FIELD_LABELS.items():
                        if key in fields:
                            continue
                        if any(label in norm for label in labels) and len(norm) <= 14:
                            value = ""
                            if ci + 1 < len(cells) and cells[ci + 1]:
                                value = cells[ci + 1].strip()
                            if not value and "：" in text:
                                value = text.split("：", 1)[1].strip()
                            if value:
                                fields[key] = {
                                    "value": value,
                                    "source": {
                                        "type": "table",
                                        "id": tid,
                                        "row": row[0].get("row") if row and row[0].get("row") is not None else None,
                                        "col": ci + 1,
                                    },
                                    "confidence": "high",
                                }
                                evidence.append({
                                    "field": key,
                                    "value": value,
                                    "source_type": "table",
                                    "source_location": "table:%s,row:%s,col:%s" % (
                                        tid, row[0].get("row") if row and row[0].get("row") is not None else "?",
                                        ci + 1),
                                    "confidence": "high",
                                })
                            break

        full_text = structure.get("full_text", "")
        for key, pattern in INLINE_PATTERNS.items():
            if key in fields:
                continue
            m = pattern.search(full_text)
            if m:
                value = m.group(1).strip()
                fields[key] = {"value": value, "source": {"type": "text"}, "confidence": "medium"}
                evidence.append({"field": key, "value": value, "source_type": "text",
                                 "source_location": "full_text:regex", "confidence": "medium"})

        structure["fields"] = fields
        structure["evidence"] = evidence
        return structure