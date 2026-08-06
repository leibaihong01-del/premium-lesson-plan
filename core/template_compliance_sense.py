# -*- coding: utf-8 -*-
"""TemplateComplianceSense：只消费 DocumentStructure，比较模板结构与生成结构。"""

RESULT_MARKERS = ["长沙轨道交通职业学院", "毕业设计真实性承诺", "目  录", "参考文献"]
EXPECTED_TABLE = {
    "01": (18, 14),
    "03": (16, 13),
    "04": (1, 1),
}


class TemplateComplianceSense:
    name = "Template Compliance Sense"

    def check(self, structures, template_structures=None):
        checks = []
        for code, item in (structures or {}).items():
            structure = item.get("structure", {}) if isinstance(item, dict) else item
            tables = structure.get("tables", [])
            if code == "02":
                full = structure.get("full_text", "")
                ok = all(k in full for k in RESULT_MARKERS)
                checks.append({
                    "document": code,
                    "document_type": "毕业设计成果",
                    "check": "fixed_pages_and_template",
                    "pass": ok,
                    "detail": "固定页标记齐全" if ok else "缺少固定页标记",
                })
                continue
            expected = EXPECTED_TABLE.get(code)
            if not expected:
                checks.append({"document": code, "check": "table", "pass": True, "detail": "无固定表约束"})
                continue
            ok = bool(tables) and tables[0].get("rows_count") == expected[0] and tables[0].get("cols_count") == expected[1]
            checks.append({
                "document": code,
                "document_type": {
                    "01": "毕业设计任务书", "03": "毕业设计成绩评定表", "04": "毕业设计答辩记录表"
                }.get(code, ""),
                "check": "table_structure",
                "pass": ok,
                "detail": "期望 %sx%s / 实际 %sx%s" % (
                    expected[0], expected[1],
                    tables[0].get("rows_count") if tables else "?",
                    tables[0].get("cols_count") if tables else "?"),
            })
        status = "pass" if all(c["pass"] for c in checks) else "fail"
        return {"sense": self.name, "status": status, "checks": checks}