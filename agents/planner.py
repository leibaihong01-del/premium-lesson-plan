# -*- coding: utf-8 -*-
"""项目经理 Agent：任务分析、工作步骤、风险预测、检测标准。"""
import json
import os
import time


def analyze_task(config, task, template_path, source_path, reports_dir):
    os.makedirs(reports_dir, exist_ok=True)
    plan = {
        "plan_id": "P-" + time.strftime("%Y%m%d%H%M%S"),
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "task": task,
        "inputs": {
            "template": template_path,
            "source": source_path,
        },
        "steps": [
            "解析模板结构",
            "分析输入资料",
            "生成文档",
            "质量检测",
            "失败修复（循环）",
            "打包输出",
            "复盘与经验沉淀",
        ],
        "risks": [
            "模板结构识别不足导致格式偏差",
            "内容越界或课程身份残留",
            "分页空白尾页",
            "多源资料冲突",
        ],
        "checks": [
            "模板符合度",
            "内容完整度",
            "教学专业度",
            "格式规范度",
        ],
        "minimum_score": config.get("quality", {}).get("minimum_score", 95),
        "max_loops": config.get("repair", {}).get("max_loops", 3),
    }
    path = os.path.join(reports_dir, "plan.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    return plan, path
