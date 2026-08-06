# -*- coding: utf-8 -*-
"""DocumentConsistencySense：只消费 DocumentStructure，跨文档身份与课题一致性。"""

FIELD_BY_DOC = {
    "01": ["student_name", "student_id", "topic", "advisor", "class_name", "major"],
    "02": ["student_name", "student_id", "topic", "advisor", "class_name", "major"],
    "03": ["student_name", "student_id", "topic", "advisor", "class_name", "major"],
    "04": ["student_name", "topic", "advisor"],
}


class DocumentConsistencySense:
    name = "Document Consistency Sense"

    @staticmethod
    def _field_evidence(structure, field):
        fields = structure.get("fields", {})
        evidence = structure.get("evidence", [])
        value = ""
        source = None
        if field in fields:
            value = fields[field].get("value", "")
            source = fields[field].get("source")
        if not value:
            full = structure.get("full_text", "")
            # 仅作为低置信兜底，不替代字段提取
            fallback = None
            return None, None, False
        ev = next((e for e in evidence if e.get("field") == field), None)
        if ev:
            source = {"type": ev.get("source_type"), "location": ev.get("source_location")}
        return value, source, True

    @staticmethod
    def _full_text_contains(structure, value):
        if not value:
            return False
        return value in structure.get("full_text", "")

    def check(self, structures, profile=None):
        checks = []
        field_map = {}
        for code, item in (structures or {}).items():
            structure = item.get("structure", {}) if isinstance(item, dict) else item
            for field in FIELD_BY_DOC.get(code, []):
                value, source, found = self._field_evidence(structure, field)
                if found:
                    field_map.setdefault(field, []).append({
                        "document": code,
                        "value": value,
                        "source": source,
                        "confidence": "high",
                    })
                elif profile is not None:
                    expected = getattr(profile, field, "") or ""
                    present = self._full_text_contains(structure, expected)
                    field_map.setdefault(field, []).append({
                        "document": code,
                        "value": expected if present else None,
                        "source": "full_text",
                        "confidence": "low" if present else None,
                    })

        for field, entries in field_map.items():
            values = {e["value"] for e in entries if e.get("value")}
            consistent = len(values) <= 1
            checks.append({
                "field": field,
                "result": "pass" if consistent else "fail",
                "documents": entries,
            })
        status = "fail" if any(c["result"] == "fail" for c in checks) else "pass"
        return {"sense": self.name, "status": status, "checks": checks}