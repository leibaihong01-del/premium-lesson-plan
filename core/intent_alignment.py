# -*- coding: utf-8 -*-
"""满意度预测（Intent Alignment）：判断结果是否用户真正想要。"""
import re


FORBIDDEN_TERMS = ["设备维修", "联锁故障处理", "CBTC参数配置", "信号设备检修", "越界内容"]
ESSENTIAL_SECTIONS = ["教学目标", "教学重难", "教学过程", "教学反思", "思政", "作业"]


def check(spec, report, text=""):
    issues = []
    checks = {}
    # 文字要求
    req_match = 0
    total_req = 0
    for d in spec.get("domains", []):
        total_req += 1
        if d in text or d in str(spec.get("deliverables")):
            req_match += 1
    checks["文字要求"] = req_match >= total_req if total_req else True
    if not checks["文字要求"]:
        issues.append("交付领域与需求不一致")
    # 约束
    forbidden_hits = [t for t in FORBIDDEN_TERMS if t in text]
    checks["禁止内容"] = not forbidden_hits
    if forbidden_hits:
        issues.append("出现越界内容：" + "、".join(forbidden_hits))
    # 隐含目标
    checks["质量达标"] = report.get("total_score", 0) >= 95
    if not checks["质量达标"]:
        issues.append("质量评分低于95")
    if spec.get("quality") == "excellent":
        checks["思政"] = "思政" in text
        checks["岗位"] = "岗位" in text
        if not checks["思政"]:
            issues.append("精品要求缺少思政元素")
        if not checks["岗位"]:
            issues.append("精品要求缺少岗位能力关联")
    # 优秀教师标准
    checks["结构完整"] = all(s in text for s in ESSENTIAL_SECTIONS)
    if not checks["结构完整"]:
        issues.append("教学结构要素不完整")
    score = round(100 * sum(1 for v in checks.values() if v) / max(1, len(checks)), 1)
    return {
        "alignment_score": score,
        "aligned": score >= 90 and not issues,
        "checks": checks,
        "issues": issues,
        "recommendation": "可以输出" if score >= 90 and not issues else "建议优化后再输出",
    }
