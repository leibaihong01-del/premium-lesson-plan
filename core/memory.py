# -*- coding: utf-8 -*-
"""记忆系统：统一命名空间读写与用户偏好模型。"""
import json
import os
import time


class Memory:
    def __init__(self, root=None):
        self.root = root or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "memory", "system")
        os.makedirs(self.root, exist_ok=True)
        self.namespaces = [
            "tasks", "decisions", "rules", "failures", "successes",
            "improvements", "user_preferences", "templates", "problems",
            "solutions", "best_practices", "lessons_learned",
        ]

    def _path(self, ns):
        return os.path.join(self.root, ns + ".json")

    def _load(self, ns):
        p = self._path(ns)
        if os.path.exists(p):
            try:
                with open(p, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save(self, ns, data):
        with open(self._path(ns), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def put(self, ns, key, value):
        data = self._load(ns)
        data[key] = value
        self._save(ns, data)
        return key

    def get(self, ns, key):
        return self._load(ns).get(key)

    def add(self, ns, value):
        data = self._load(ns)
        if not isinstance(data, list):
            data = [] if not data else [data]
        entry = {"id": ns + "-" + str(len(data) + 1), "time": time.strftime("%Y-%m-%d %H:%M:%S")}
        entry.update(value if isinstance(value, dict) else {"value": value})
        data.append(entry)
        self._save(ns, data)
        return entry["id"]

    def search(self, ns, text):
        data = self._load(ns)
        items = data if isinstance(data, list) else list(data.values())
        return [it for it in items if text in str(it)]

    def query(self, ns, text):
        """查询别名，与 search 一致（向后兼容）。"""
        return self.search(ns, text)

    def counts(self):
        """各命名空间条目数（结构化索引基础）。"""
        return {
            ns: (len(self._load(ns)) if isinstance(self._load(ns), (list, dict)) else 0)
            for ns in self.namespaces
        }

    def remember_user(self, preference):
        prefs = self._load("user_preferences")
        prefs.setdefault("preferences", {}).update(preference)
        prefs["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self._save("user_preferences", prefs)
        return prefs

    def user_profile(self):
        return self._load("user_preferences")
