# -*- coding: utf-8 -*-
"""优化学习 Agent：写入成功/失败/规则更新记忆并生成复盘日志。"""
import json
import os
import time


def _load(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return []


def _save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def learn(run_result, memory_dir, reports_dir):
    os.makedirs(memory_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    entry = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "file": run_result.get("file"),
        "score": run_result.get("total_score"),
        "final": run_result.get("final"),
        "issues": run_result.get("issues"),
        "loops": run_result.get("loops"),
    }
    if run_result.get("final") == "PASS":
        arr = _load(os.path.join(memory_dir, "success.json"))
        arr.append(entry)
        _save(os.path.join(memory_dir, "success.json"), arr)
    else:
        arr = _load(os.path.join(memory_dir, "failure.json"))
        arr.append(entry)
        _save(os.path.join(memory_dir, "failure.json"), arr)
    if run_result.get("issues") and any(run_result["issues"].values()):
        arr = _load(os.path.join(memory_dir, "failures.json"))
        arr.append(entry)
        _save(os.path.join(memory_dir, "failures.json"), arr)
    if run_result.get("rules_updated"):
        arr = _load(os.path.join(memory_dir, "rule_update.json"))
        arr.extend(run_result["rules_updated"])
        _save(os.path.join(memory_dir, "rule_update.json"), arr)
    improvements = _load(os.path.join(memory_dir, "improvements.json"))
    suggestion = run_result.get("improvement", "继续执行生成→检测→修复→沉淀闭环")
    improvements.append({
        "time": entry["time"],
        "suggestion": suggestion,
        "applied": False,
    })
    # 自主迭代：同一建议出现 >=2 次时自动沉淀为规则
    from collections import Counter
    counts = Counter(item.get("suggestion") for item in improvements)
    auto_rules = []
    for item in improvements:
        if item.get("suggestion") == suggestion and counts[suggestion] >= 2 and not item.get("applied"):
            item["applied"] = True
            auto_rules.append({
                "time": entry["time"],
                "rule": suggestion,
                "source": "learner.auto",
            })
    if auto_rules:
        rules = _load(os.path.join(memory_dir, "rule_update.json"))
        rules.extend(auto_rules)
        _save(os.path.join(memory_dir, "rule_update.json"), rules)
    _save(os.path.join(memory_dir, "improvements.json"), improvements)
    reflection = os.path.join(reports_dir, "reflection.md")
    with open(reflection, "w", encoding="utf-8") as f:
        f.write("# Agent 复盘日志\n\n")
        f.write(f"- 文件：{entry['file']}\n")
        f.write(f"- 综合得分：{entry['score']}\n")
        f.write(f"- 结论：{entry['final']}\n")
        f.write(f"- 修复循环次数：{entry['loops']}\n")
        f.write(f"- 改进建议：{improvements[-1]['suggestion']}\n")
    return reflection
