# -*- coding: utf-8 -*-
"""GraduationAgent 模板差异分析与合规检查：学校官方模板 vs 优化模板。"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from tools.word_template_inspector import inspect_docx

OFFICIAL = {
    "taskbook": "01 xxx 毕业设计任务书 轨道交通受流设备检修方案设计.docx",
    "result": "02 xxx 毕业设计成果 轨道交通受流设备检修方案设计.docx",
    "defense": "04 xxx 毕业设计成绩评定表  答辩记录表 轨道交通受流设备检修方案设计.docx",
    "guidance": "05 xxx 毕业设计指导记录表 轨道交通受流设备检修方案设计.docx",
}

def labels_of(spec):
    out = set()
    for t in spec.get("tables", []):
        for row in t.get("rows_sample", []):
            if row:
                out.add(str(row[0]).strip())
    return out

def main(ws=None):
    ws = ws or os.environ.get("GRAD_WS", r"D:\Users\leibaihong\Desktop\课程材料优化\毕业设计智能管理工作区")
    idx_path = os.path.join(ws, "00_系统配置", "template_index.json")
    with open(idx_path, encoding="utf-8") as f:
        idx = json.load(f)
    official_dir = os.path.join(ws, "01_学校模板", "学校官方模板")
    opt_dir = os.path.join(ws, "01_学校模板", "优化模板")
    results = []
    for tpl in idx.get("templates", []):
        rid = tpl["id"]
        if rid not in OFFICIAL:
            continue
        opt_path = os.path.join(ws, tpl["file"])
        off_path = os.path.join(official_dir, OFFICIAL[rid])
        off_spec = inspect_docx(off_path) if os.path.exists(off_path) else {}
        opt_spec = inspect_docx(opt_path) if os.path.exists(opt_path) else {}
        sec_ok = [s for s in off_spec.get("sections", [])] == [s for s in opt_spec.get("sections", [])]
        tables_ok = True
        for a, b in zip(off_spec.get("tables", []), opt_spec.get("tables", [])):
            if a["rows"] != b["rows"] or a["cols"] != b["cols"] or a["merge_signature"] != b["merge_signature"]:
                tables_ok = False
        missing = sorted(labels_of(off_spec) - labels_of(opt_spec))
        results.append({
            "id": rid, "name": tpl["name"],
            "sections_equal": sec_ok, "tables_equal": tables_ok,
            "missing_fields": missing,
            "note": "优化模板当前为学校官方副本" if (sec_ok and tables_ok and not missing) else "存在差异，需人工复核",
        })
    report = {"version": "1.0", "results": results}
    out_json = os.path.join(ws, "00_系统配置", "模板差异分析结果.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    for r in results:
        print(r)
    print("REPORT", out_json)

if __name__ == "__main__":
    main()