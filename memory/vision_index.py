# -*- coding: utf-8 -*-
"""Vision Template Index：模板视觉结构索引，持久化 JSON。"""
import json
import os
import time


class VisionTemplateIndex:
    def __init__(self, path=None):
        if path is None:
            base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "memory")
            path = os.path.join(base, "vision_templates.json")
        self.path = path

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save(self, data):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def index(self, template_id, structure, course="", kind=""):
        data = self._load()
        data[template_id] = {
            "template_id": template_id,
            "course": course,
            "kind": kind,
            "structure": structure,
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        self._save(data)
        return template_id

    def get(self, template_id):
        return self._load().get(template_id)

    def search(self, course=None, kind=None):
        items = list(self._load().values())
        if course:
            items = [i for i in items if i.get("course") == course]
        if kind:
            items = [i for i in items if i.get("kind") == kind]
        return items