# -*- coding: utf-8 -*-
"""任务状态存储：任务ID、状态保存、断点恢复、运行日志。"""
import json
import os
import time
import uuid


class TaskStore:
    def __init__(self, root=None):
        self.root = root or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "state", "tasks")
        self.log_root = os.path.join(os.path.dirname(self.root), "logs")
        os.makedirs(self.root, exist_ok=True)
        os.makedirs(self.log_root, exist_ok=True)

    def _path(self, task_id):
        return os.path.join(self.root, task_id + ".json")

    def new(self, spec=None):
        task_id = uuid.uuid4().hex[:12]
        record = {
            "task_id": task_id,
            "spec": spec or {},
            "state": "PENDING",
            "steps": [],
            "artifacts": [],
            "trace": [],
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.save(record)
        return record

    def save(self, record):
        record["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self._path(record["task_id"]), "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        return record

    def load(self, task_id):
        p = self._path(task_id)
        if not os.path.exists(p):
            return None
        with open(p, encoding="utf-8") as f:
            return json.load(f)

    def delete(self, task_id):
        p = self._path(task_id)
        if os.path.exists(p):
            os.remove(p)
            return True
        return False

    def list(self):
        return sorted(f[:-5] for f in os.listdir(self.root) if f.endswith(".json"))

    def resume(self, task_id):
        """断点恢复：返回记录及最后完成的步骤。"""
        record = self.load(task_id)
        if record is None:
            return None
        last = record["steps"][-1] if record.get("steps") else None
        return {"record": record, "last_step": last}

    def append_log(self, task_id, line):
        with open(os.path.join(self.log_root, task_id + ".log"), "a", encoding="utf-8") as f:
            f.write(time.strftime("%H:%M:%S") + " " + line + "\n")
