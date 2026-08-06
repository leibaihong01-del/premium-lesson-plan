# -*- coding: utf-8 -*-
"""Result Quality Pipeline：统一调度解析、质量感知、经验、学院要求与修订规划。"""
import json
import os
import time

from document_structure_parser import parse as parse_structure
from result_document_parser import parse
from result_quality_sense import ContentQualitySense, LayoutQualitySense, StructureQualitySense
from reference_quality_sense import ReferenceQualitySense
from academic_requirement import AcademicRequirementChecker
from revision_planner import RevisionPlanner
from experience_trace import build_experience_effects


class ResultQualityPipeline:
    name = "ResultQualityPipeline"

    def __init__(self, output_dir=None):
        self.output_dir = output_dir
        self.content_sense = ContentQualitySense()
        self.structure_sense = StructureQualitySense()
        self.layout_sense = LayoutQualitySense()
        self.reference_sense = ReferenceQualitySense()
        self.academic_checker = AcademicRequirementChecker()
        self.revision_planner = RevisionPlanner()

    def run(self, profile, document_path, pdf_path=None, template_path=None, template_pdf_path=None,
            taskbook_path=None, experience_context=None):
        model = parse(document_path, pdf_path)
        template_model = parse(template_path, template_pdf_path) if template_path else None
        taskbook_structure = parse_structure(taskbook_path, document_type="task_book") if taskbook_path else None

        content_report = self.content_sense.check(model, profile=profile, context=experience_context,
                                                  taskbook_structure=taskbook_structure)
        structure_report = self.structure_sense.check(model, profile=profile, context=experience_context)
        layout_report = self.layout_sense.check(model, profile=profile, context=experience_context,
                                                template_structure=template_model)
        reference_report = self.reference_sense.check(model)
        academic_report = self.academic_checker.check(model, content_report=content_report,
                                                      reference_report=reference_report)

        reports = {
            "content": content_report,
            "structure": structure_report,
            "layout": layout_report,
            "reference": reference_report,
            "academic": academic_report,
        }
        revision_plan = self.revision_planner.plan(reports)

        quality_status = "pass"
        for r in reports.values():
            if r.get("status") == "fail":
                quality_status = "fail"
            elif r.get("status") == "review" and quality_status == "pass":
                quality_status = "review"

        result_report = {
            "schema_version": "0.7-result-quality-v1",
            "document_type": "result",
            "document_path": document_path,
            "student": profile.student_name if profile else None,
            "quality_status": quality_status,
            "checked_items": sum(len(r.get("checks", [])) + len(r.get("requirements", [])) for r in reports.values()),
            "passed": sum(1 for r in reports.values() if r.get("status") == "pass"),
            "failed": sum(1 for r in reports.values() if r.get("status") == "fail"),
            "review": sum(1 for r in reports.values() if r.get("status") == "review"),
            "reports": reports,
            "model_summary": {
                "title": model.get("title"),
                "pages": (model.get("pages") or {}).get("count"),
                "sections": len(model.get("sections", [])),
                "tables": len(model.get("tables", [])),
                "references": model.get("reference_count", 0),
                "body_chars": model.get("body_chars", 0),
                "toc_field": model.get("toc_field_present", False),
            },
        }

        trace = self._trace(profile, experience_context, result_report, revision_plan)
        if self.output_dir:
            os.makedirs(self.output_dir, exist_ok=True)
            self._write(self.output_dir, "result_quality_report.json", result_report)
            self._write(self.output_dir, "reference_quality_report.json", reference_report)
            self._write(self.output_dir, "document_quality_report.json", {
                "sense": "Document Quality Sense",
                "status": layout_report.get("status"),
                "content": content_report,
                "structure": structure_report,
                "layout": layout_report,
            })
            self._write(self.output_dir, "academic_requirement_report.json", academic_report)
            self._write(self.output_dir, "revision_plan.json", revision_plan)
            self._write(self.output_dir, "quality_pipeline_trace.json", trace)
        return {
            "quality_status": quality_status,
            "result_quality_report": result_report,
            "reference_quality_report": reference_report,
            "academic_requirement_report": academic_report,
            "revision_plan": revision_plan,
            "quality_pipeline_trace": trace,
        }

    def _trace(self, profile, context, result_report, revision_plan):
        experience_used = []
        experience_missing = []
        if context is not None:
            experience_used = [e.get("name") for e in context.loaded_experience]
            experience_missing = [m.get("name") for m in context.missing_experience]
        applicable_like = None
        if context is not None:
            applicable_like = {"experiences": context.loaded_experience, "enabled": True}
        effects = build_experience_effects(applicable_like, reports=result_report.get("reports", {})) if applicable_like is not None else []
        return {
            "schema_version": "0.7-quality-pipeline-trace-v1",
            "document": "%s成果" % (profile.student_name if profile else ""),
            "pipeline": self.name,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "experience_used": experience_used,
            "experience_missing": experience_missing,
            "experience_effects": effects,
            "quality_status": result_report.get("quality_status"),
            "checked_items": result_report.get("checked_items"),
            "passed": result_report.get("passed"),
            "failed": result_report.get("failed"),
            "review": result_report.get("review"),
            "issues": [a.get("issue") for a in revision_plan.get("actions", [])],
            "revision_generated": bool(revision_plan.get("actions")),
            "revision_auto_apply": False,
        }

    @staticmethod
    def _write(out_dir, name, payload):
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
