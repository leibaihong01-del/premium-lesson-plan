# -*- coding: utf-8 -*-
"""批量质量评分：对多份 docx 执行四维评分并输出专家评分报告。"""
import argparse
import glob
import json
import os
import shutil
import sys

import yaml

from agents import reviewer, router_agent
from modules import runtime


ROOT = os.path.dirname(os.path.abspath(__file__))
REPORTS = os.path.join(ROOT, "reports")
OUTPUT = os.path.join(ROOT, "output")
CONFIG = os.path.join(ROOT, "config", "agent_rules.yaml")


def main():
    ap = argparse.ArgumentParser(description="批量质量评分")
    ap.add_argument("--template", required=True)
    ap.add_argument("--dir", default=None, help="扫描目录")
    ap.add_argument("--files", nargs="*", default=None)
    ap.add_argument("--profile", choices=["auto", "low", "medium", "high"], default="auto")
    ap.add_argument("--requirement", choices=["normal", "formal", "excellent"], default="excellent")
    args = ap.parse_args()

    with open(CONFIG, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    weights = config["quality"]["weights"]
    minimum = config["quality"]["minimum_score"]
    os.makedirs(REPORTS, exist_ok=True)
    os.makedirs(OUTPUT, exist_ok=True)

    files = list(args.files or [])
    if args.dir:
        files += sorted(glob.glob(os.path.join(args.dir, "*.docx")))

    def is_lesson(f):
        name = os.path.basename(f)
        return ("教案（第" in name or "教案样板（第" in name or "实训教案" in name) and "优化版" in name

    files = [f for f in files if os.path.exists(f) and is_lesson(f)]

    results = []
    work = os.path.join(OUTPUT, "_batch_work.docx")
    cache_path = os.path.join(REPORTS, "review_cache.json")
    reused_count = 0
    level_count = {}
    for i, f in enumerate(files, 1):
        cached, reused = runtime.cached_review(f, args.template, cache_path)
        if reused:
            rep = runtime.normalize_cached(cached)
            rep["file"] = os.path.basename(f)
            results.append(rep)
            reused_count += 1
            level_count["low(缓存)"] = level_count.get("low(缓存)", 0) + 1
            print(f"[{i}/{len(files)}] {rep['file']} -> {rep['total_score']} {rep['final']} (缓存)")
            continue
        meta = {"task_type": "practice" if "实训" in os.path.basename(f) else "lesson",
                "domain": "education", "pages": 0, "tables": 39,
                "images": 1, "file_count": 1, "complex_layout": True}
        route = router_agent.route(meta, args.requirement, force_profile=args.profile)
        level = route.get("recommended_compute", "medium")
        level_count[level] = level_count.get(level, 0) + 1
        shutil.copy2(f, work)
        try:
            rep = reviewer.review(work, args.template, REPORTS, weights)
        except Exception as exc:
            rep = {
                "file": os.path.basename(f),
                "template_score": 0, "content_score": 0,
                "teaching_score": 0, "format_score": 0,
                "total_score": 0, "final": "REPAIR_REQUIRED",
                "issues": {"error": str(exc)},
            }
        rep["file"] = os.path.basename(f)
        runtime.put_cache(cache_path, f, args.template, rep)
        router_agent.record(meta, rep["total_score"], rep["final"] == "PASS", 1, level)
        results.append(rep)
        print(f"[{i}/{len(files)}] {rep['file']} -> {rep['total_score']} {rep['final']} (等级:{level})")

    avg = round(sum(r["total_score"] for r in results) / len(results), 1) if results else 0
    report_md = os.path.join(OUTPUT, "专家评分报告.md")
    with open(report_md, "w", encoding="utf-8") as f:
        f.write("# 专家评分报告\n\n")
        f.write(f"评分文件数：{len(results)}    平均分：{avg}    达标线：{minimum}\n\n")
        f.write("| 文件 | 模板30 | 内容25 | 教学25 | 格式20 | 总分 | 结论 |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for r in results:
            f.write(f"| {r['file']} | {r['template_score']} | {r['content_score']} | "
                    f"{r['teaching_score']} | {r['format_score']} | {r['total_score']} | {r['final']} |\n")
        failed = [r for r in results if r["final"] != "PASS"]
        f.write(f"\n结论：{'全部达标' if not failed else f'{len(failed)} 份需要返工'}\n")
    with open(os.path.join(REPORTS, "quality_report_all.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("专家评分报告:", report_md, "| 平均分:", avg, "| 缓存复用:", reused_count, "/", len(files),
          "| 等级分布:", level_count)
    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
