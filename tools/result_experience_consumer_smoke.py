# -*- coding: utf-8 -*-
"""P3-A 验证：陈家宝成果经验消费，不修改旧生成结果。"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core"))

from result_experience_consumer import ResultExperienceConsumer

COURSEAGENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = os.path.dirname(COURSEAGENT)
WS = os.path.join(PROJECT, "毕业设计智能制作工作区")
DIRECTION = "03_电梯系统"
RESULT_DOCX = os.path.join(WS, "06_输出成果", DIRECTION, "陈家宝_毕业设计完整成果包",
                           "02 陈家宝 毕业设计成果 橘子洲南站自动扶梯扶手带检修方案设计.docx")
INFO_PATH = os.path.join(WS, "03_需要修改文件整理", DIRECTION, "陈家宝", "学生信息.json")
TRACE_DIR = os.path.join(COURSEAGENT, "output", "experience_traces")
TASK_ID = "p3a_result_consumer_20260805"


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    with open(INFO_PATH, encoding="utf-8") as f:
        info = json.load(f)

    before = sha256(RESULT_DOCX)

    # 默认配置应为关闭：消费层不加载经验
    default_consumer = ResultExperienceConsumer()
    default_ctx = default_consumer.build_context(info["姓名"], "02 杨振海 毕业设计成果 ...docx")
    print("default_enabled=", default_consumer.enabled)
    assert default_ctx.loaded_experience == []
    assert default_ctx.missing_experience == []

    # 显式开启：真实加载
    consumer = ResultExperienceConsumer(enabled=True)
    ctx = consumer.build_context(info["姓名"], "02 杨振海 毕业设计成果 黄兴南路站AFC闸机设备检修方案设计.docx")
    trace = consumer.trace(ctx, TASK_ID)
    os.makedirs(TRACE_DIR, exist_ok=True)
    trace_path = os.path.join(TRACE_DIR, "result_experience_trace.json")
    with open(trace_path, "w", encoding="utf-8") as f:
        json.dump(trace, f, ensure_ascii=False, indent=2)

    after = sha256(RESULT_DOCX)
    unchanged = before == after

    loaded_names = [e["name"] for e in ctx.loaded_experience]
    missing_names = [m["name"] for m in ctx.missing_experience]
    print("LOADED=", loaded_names)
    print("MISSING=", missing_names)
    print("UNCHANGED=", unchanged)
    print("TRACE=", trace_path)
    assert "Result TKM" in loaded_names
    assert "Golden Case Experience（王欢成果）" in loaded_names
    assert "Reference Quality Sense" in loaded_names
    assert "Result Quality Memory" in missing_names
    assert "Academic Requirement Knowledge Model" in missing_names
    assert unchanged
    return 0


if __name__ == "__main__":
    sys.exit(main())