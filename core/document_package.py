# -*- coding: utf-8 -*-
"""学生毕业设计全生命周期档案对象。"""
import json
import os
import time
from dataclasses import asdict, dataclass, field

from student_profile import StudentProfile


@dataclass
class DocumentItem:
    code: str = ""
    document_type: str = ""
    filename: str = ""
    docx_path: str = ""
    pdf_path: str = ""
    template_source: str = ""
    status: str = "planned"
    generated_at: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class StudentGraduationArchive:
    archive_id: str
    profile: StudentProfile
    direction: str
    package_dir: str
    lifecycle_status: str = "created"
    documents: dict = field(default_factory=dict)
    timeline: list = field(default_factory=list)
    consistency_report: dict = field(default_factory=dict)
    template_report: dict = field(default_factory=dict)
    validation_report: dict = field(default_factory=dict)

    def add_event(self, event, detail):
        self.timeline.append({
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "event": event,
            "detail": detail,
        })

    def register_document(self, item):
        self.documents[item.code] = item
        self.add_event("register_document", "%s %s" % (item.code, item.document_type))

    def update_status(self, status):
        self.lifecycle_status = status
        self.add_event("update_status", status)

    def to_dict(self):
        return {
            "archive_id": self.archive_id,
            "student_profile": self.profile.to_dict(),
            "direction": self.direction,
            "package_dir": self.package_dir,
            "lifecycle_status": self.lifecycle_status,
            "documents": [item.to_dict() for item in sorted(self.documents.values(), key=lambda x: x.code)],
            "timeline": self.timeline,
            "consistency_report": self.consistency_report,
            "template_report": self.template_report,
            "validation_report": self.validation_report,
        }

    def save(self, path):
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
        return path