# -*- coding: utf-8 -*-
"""经验注册表：登记已验证经验与来源文件（只读，不固化新经验）。"""
import json
import os


class ExperienceRegistry:
    def __init__(self, registry_path, project_root=None):
        self.registry_path = registry_path
        self.project_root = project_root or self._default_project_root()
        self.entries = []
        self._load()

    @staticmethod
    def _default_project_root():
        # CourseAgent/core/experience_registry.py -> 课程材料优化
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def _load(self):
        if not os.path.isfile(self.registry_path):
            raise FileNotFoundError("registry not found: %s" % self.registry_path)
        with open(self.registry_path, encoding="utf-8") as f:
            data = json.load(f)
        self.entries = data.get("experiences", [])

    def resolve(self, rel_path):
        if not rel_path:
            return None
        normalized = rel_path.replace("/", os.sep)
        return os.path.normpath(os.path.join(self.project_root, normalized))

    def for_document_type(self, document_type):
        return [e for e in self.entries if document_type in e.get("document_types", [])]

    def all(self):
        return list(self.entries)