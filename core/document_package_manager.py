# -*- coding: utf-8 -*-
"""档案生命周期管理：创建、登记文档、写状态、触发包级验收。"""
import os
import time

from document_package import DocumentItem, StudentGraduationArchive
from package_validator import PackageValidator
from student_profile import StudentProfile


class DocumentPackageManager:
    def __init__(self, base_output_dir, profile, direction, archive_id=None):
        self.base_output_dir = base_output_dir
        self.profile = profile if isinstance(profile, StudentProfile) else StudentProfile.from_dict(profile)
        self.direction = direction
        stamp = time.strftime("%Y%m%d%H%M%S")
        self.archive_id = archive_id or "dpil-%s-%s" % (stamp, self.profile.student_name)
        self.package_dir = os.path.join(base_output_dir, direction, self.profile.student_name + "_毕业设计完整成果包")
        self.process_dir = os.path.join(self.package_dir, "_过程记录")
        os.makedirs(self.process_dir, exist_ok=True)
        self.archive = StudentGraduationArchive(
            archive_id=self.archive_id,
            profile=self.profile,
            direction=direction,
            package_dir=self.package_dir,
        )
        self.archive.add_event("create_archive", self.package_dir)

    def register_document(self, code, document_type, docx_path, pdf_path=None, template_source=""):
        if not os.path.isfile(docx_path):
            raise FileNotFoundError(docx_path)
        item = DocumentItem(
            code=code,
            document_type=document_type,
            filename=os.path.basename(docx_path),
            docx_path=docx_path,
            pdf_path=pdf_path or "",
            template_source=template_source,
            status="generated",
            generated_at=time.strftime("%Y-%m-%dT%H:%M:%S"),
        )
        self.archive.register_document(item)
        return item

    def write_lifecycle_state(self):
        path = os.path.join(self.process_dir, "document_package_lifecycle.json")
        self.archive.save(path)
        return path

    def validate(self, trace_dir=None):
        validator = PackageValidator()
        report = validator.validate(self.archive, trace_dir=trace_dir)
        self.archive.validation_report = report
        status = "deliverable" if report.get("package_status") == "pass" else "revision"
        self.archive.update_status(status)
        self.write_lifecycle_state()
        return report