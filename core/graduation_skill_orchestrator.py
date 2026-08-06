# -*- coding: utf-8 -*-
"""GraduationSkillOrchestrator：V0.7 毕业设计生产统一调度入口（不再调用旧 V0.3 生成入口）。"""
import json
import os
import time

from document_package_manager import DocumentPackageManager
from graduation_skill_runners import DefenseSkillRunner, EvaluationSkillRunner, ResultSkillRunner, TaskBookSkillRunner
from student_profile import StudentProfile


class GraduationSkillOrchestrator:
    def __init__(self, profile, project_root, workspace, direction, package_name=None, regenerate=True):
        self.profile = profile if isinstance(profile, StudentProfile) else StudentProfile.from_dict(profile)
        self.project_root = project_root
        self.ws = workspace
        self.direction = direction
        self.regenerate = regenerate
        self.name = self.profile.student_name
        self.topic = self.profile.topic
        self.courseagent_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        suffix = package_name or "毕业设计完整成果包"
        self.package_dir = os.path.join(self.ws, "06_输出成果", direction, self.name + "_" + suffix)
        self.process_dir = os.path.join(self.package_dir, "_过程记录")
        os.makedirs(self.process_dir, exist_ok=True)
        self.student_dir = os.path.join(self.ws, "03_需要修改文件整理", direction, self.name)
        self.trace = {
            "student": self.name,
            "entry": "GraduationSkillOrchestrator",
            "old_v03_called": False,
            "skills": [],
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }

    def run(self):
        self._execute_skills()
        self._validate_package()
        self.write_skill_execution_trace()
        return self.trace

    def _execute_skills(self):
        runners = [
            TaskBookSkillRunner(self.profile, self.ws, self.courseagent_root, self.project_root),
            ResultSkillRunner(self.profile, self.ws, self.courseagent_root, self.project_root),
            EvaluationSkillRunner(self.profile, self.ws, self.courseagent_root, self.project_root),
            DefenseSkillRunner(self.profile, self.ws, self.courseagent_root, self.project_root),
        ]
        for runner in runners:
            try:
                result = runner.run(self.student_dir, self.package_dir, self.process_dir)
                entry = {"name": runner.name, "status": "executed", "output": result.get("output")}
                if "page_semantic" in result:
                    entry["page_semantic"] = result["page_semantic"]
                if "quality" in result:
                    entry["quality_status"] = result["quality"].get("quality_status")
            except Exception as e:
                entry = {"name": runner.name, "status": "failed", "error": repr(e)}
            self.trace["skills"].append(entry)
        self.trace["package_dir"] = self.package_dir

    def _validate_package(self):
        base_out = os.path.join(self.ws, "06_输出成果")
        manager = DocumentPackageManager(base_out, self.profile, self.direction,
                                         archive_id="dpil-%s-%s" % (time.strftime("%Y%m%d"), self.name))
        for code, doc_type in [("01", "毕业设计任务书"), ("02", "毕业设计成果"),
                               ("03", "毕业设计成绩评定表"), ("04", "毕业设计答辩记录表")]:
            docx = os.path.join(self.package_dir, "%s %s %s %s.docx" % (code, self.name, doc_type, self.topic))
            pdf = os.path.join(self.process_dir, "%s %s %s %s.pdf" % (code, self.name, doc_type, self.topic))
            manager.register_document(code, doc_type, docx, pdf, template_source="")
        report = manager.validate(trace_dir=self.process_dir)
        self.trace["package_validation"] = report

    def write_skill_execution_trace(self):
        path = os.path.join(self.process_dir, "skill_execution_trace.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.trace, f, ensure_ascii=False, indent=2)
        return path