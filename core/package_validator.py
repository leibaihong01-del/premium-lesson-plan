# -*- coding: utf-8 -*-
"""PackageValidator：编排 DocumentStructure 解析 + 包级 Sense + 文件完整性验收。"""
import json
import os

from document_structure_parser import parse as parse_structure
from document_consistency_sense import DocumentConsistencySense
from template_compliance_sense import TemplateComplianceSense

DOC_TYPE_BY_CODE = {
    "01": "毕业设计任务书",
    "02": "毕业设计成果",
    "03": "毕业设计成绩评定表",
    "04": "毕业设计答辩记录表",
}


class PackageValidator:
    def validate(self, archive, trace_dir=None):
        profile = archive.profile
        checks = []
        issues = []
        structures = {}

        missing_codes = [c for c in DOC_TYPE_BY_CODE if c not in archive.documents]
        checks.append({"check": "completeness", "pass": not missing_codes,
                       "detail": "缺失：" + "、".join(missing_codes) if missing_codes else "齐全"})
        if missing_codes:
            issues.append("缺少文档：" + "、".join(missing_codes))

        for code in sorted(archive.documents):
            item = archive.documents[code]
            expected = "%s %s %s %s.docx" % (code, profile.student_name, DOC_TYPE_BY_CODE[code], profile.topic)
            naming_ok = item.filename == expected
            checks.append({"check": "naming_%s" % code, "pass": naming_ok, "detail": item.filename})
            if not naming_ok:
                issues.append("命名错误：" + item.filename)
            pdf_ok = bool(item.pdf_path) and os.path.isfile(item.pdf_path)
            checks.append({"check": "pdf_%s" % code, "pass": pdf_ok, "detail": item.pdf_path or "未提供"})
            if not pdf_ok:
                issues.append("PDF缺失：" + code)
            try:
                structures[code] = {
                    "structure": parse_structure(item.docx_path, item.pdf_path or None,
                                                 document_type=DOC_TYPE_BY_CODE[code]),
                }
            except Exception as e:
                structures[code] = {"structure": {"full_text": "", "tables": [], "fields": {}, "evidence": []},
                                    "error": repr(e)}
                issues.append("解析失败：" + code)

        consistency = DocumentConsistencySense().check(structures, profile=profile)
        template = TemplateComplianceSense().check(structures)
        archive.consistency_report = consistency
        archive.template_report = template
        checks.append({"check": "document_consistency", "pass": consistency["status"] == "pass", "detail": consistency["status"]})
        checks.append({"check": "template_compliance", "pass": template["status"] == "pass", "detail": template["status"]})
        if consistency["status"] != "pass":
            issues.append("跨文档身份/课题不一致")
        if template["status"] != "pass":
            issues.append("模板符合性失败")

        trace_files = []
        if trace_dir and os.path.isdir(trace_dir):
            trace_files = sorted(f for f in os.listdir(trace_dir) if f.startswith("experience_trace_") and f.endswith(".json"))

        all_pass = all(c["pass"] for c in checks)
        report = {
            "schema_version": "0.7-package-validation-v1",
            "student": profile.student_name,
            "documents": len(archive.documents),
            "checks": {
                "consistency": consistency["status"],
                "template": template["status"],
                "experience_trace": "pass" if trace_files else "review",
                "file_integrity": "pass" if all(c["pass"] for c in checks if c["check"].startswith(("pdf_", "naming_", "completeness"))) else "fail",
            },
            "package_status": "pass" if all_pass else "fail",
            "issues": issues,
            "evidence": consistency.get("checks", []),
            "experience_traces": trace_files,
        }
        os.makedirs(archive.package_dir, exist_ok=True)
        out = os.path.join(archive.package_dir, "_过程记录", "document_package_validation_report.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        archive.validation_report = report
        return report