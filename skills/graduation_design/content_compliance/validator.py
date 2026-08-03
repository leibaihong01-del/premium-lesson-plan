# -*- coding: utf-8 -*-
"""毕业设计内容规范校验器（框架）：区域识别 -> 规则匹配 -> 差异分析。

规则仅从同目录 rules.json 加载，不硬编码业务规则。
"""
import json
import os
import re

DEFAULT_RULES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rules.json")


class ComplianceValidator:
    def __init__(self, rules_path=None):
        self.rules_path = rules_path or DEFAULT_RULES
        with open(self.rules_path, encoding="utf-8") as f:
            self.data = json.load(f)
        self.rules = self.data.get("rules", [])

    def match_rule(self, rule, text):
        rtype = rule.get("type")
        if rtype == "banned_expression":
            hits = [e for e in rule.get("expressions", []) if e and e in text]
            return hits
        if rtype == "min_length":
            if len(re.sub(r"\\s", "", text or "")) < int(rule.get("min_chars", 0)):
                return ["正文字数不足"]
        return []

    def analyze(self, texts):
        """texts: [(region, text)] -> issues"""
        issues = []
        for region, text in texts:
            for rule in self.rules:
                if rule.get("region") != region:
                    continue
                hits = self.match_rule(rule, text)
                for hit in hits:
                    issues.append({
                        "rule_id": rule["id"],
                        "region": region,
                        "expression": hit,
                        "reason": rule.get("reason"),
                        "source": rule.get("source"),
                        "confidence": rule.get("confidence"),
                        "suggestion": rule.get("correct_expression"),
                    })
        return issues
