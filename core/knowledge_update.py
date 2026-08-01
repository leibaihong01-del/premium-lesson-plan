# -*- coding: utf-8 -*-
"""知识更新Agent：来源登记、内容导入、影响分析、规则升级建议。"""
import time


TRACKED_DOMAINS = ["职业教育政策", "国家教学标准", "行业发展", "教学改革趋势", "AI技术"]


class KnowledgeUpdateAgent:
    def __init__(self, memory):
        self.memory = memory

    def _list(self, ns):
        data = self.memory._load(ns)
        return data if isinstance(data, list) else []

    def register_source(self, name, domain, url=""):
        sources = self._list("knowledge_sources")
        sources.append({"name": name, "domain": domain, "url": url, "checked_at": None})
        self.memory._save("knowledge_sources", sources)

    def ingest_update(self, domain, title, summary, impact=""):
        entry = {
            "domain": domain,
            "title": title,
            "summary": summary,
            "impact": impact or self.analyze_impact(domain, summary),
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        updates = self._list("knowledge_updates")
        updates.append(entry)
        self.memory._save("knowledge_updates", updates)
        if entry["impact"] != "无影响":
            level = "L2" if "工作流" in entry["impact"] else "L1"
            rules = self._list("rules")
            rules.append({
                "level": level,
                "rule": f"[知识更新-{domain}] {title}",
                "approval": "auto" if level == "L1" else "pending_verify",
                "time": entry["time"],
            })
            self.memory._save("rules", rules)
        return entry

    def analyze_impact(self, domain, summary):
        if any(k in summary for k in ("新标准", "新政策", "新规")):
            return "标准/政策变化，需更新课程规则（工作流级）"
        if any(k in summary for k in ("新案例", "新技术", "新方法")):
            return "建议更新教学案例与资源库"
        return "无影响"

    def status(self):
        sources = self._list("knowledge_sources")
        updates = self._list("knowledge_updates")
        return {"tracked_domains": TRACKED_DOMAINS, "sources": len(sources), "updates": len(updates)}
