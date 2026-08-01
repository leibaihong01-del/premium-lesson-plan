# -*- coding: utf-8 -*-
"""Memory 结构化索引：在 JSON 之上建立索引与查询，保留原存储。"""
import json
import os
import time


class MemoryIndex:
    def __init__(self, memory, index_path=None):
        self.memory = memory
        parent = os.path.dirname(memory.root)
        self.index_path = index_path or os.path.join(parent, "index.json")

    def rebuild(self, namespaces=None):
        namespaces = namespaces or self.memory.namespaces
        idx = {}
        for ns in namespaces:
            data = self.memory._load(ns)
            if isinstance(data, dict):
                keys = list(data.keys())
                count = len(data)
            elif isinstance(data, list):
                keys = [e.get("id") for e in data if isinstance(e, dict)]
                count = len(data)
            else:
                keys, count = [], 0
            idx[ns] = {"count": count, "keys": keys[:200], "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")}
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(idx, f, ensure_ascii=False, indent=2)
        return idx

    def get(self, ns):
        if not os.path.exists(self.index_path):
            return None
        with open(self.index_path, encoding="utf-8") as f:
            return json.load(f).get(ns)

    def search(self, ns, text):
        meta = self.get(ns)
        if not meta or not meta.get("count"):
            return []
        return self.memory.search(ns, text)
