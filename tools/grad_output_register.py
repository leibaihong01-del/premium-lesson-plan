# -*- coding: utf-8 -*-
"""GraduationAgent 输出登记：把学生档案复制到 outputs 并登记。"""
import argparse, json, os, shutil, time

SUB_MAP = {
    "01_毕业设计任务书": "任务书",
    "02_毕业设计成果": "成果",
    "03_指导记录": "指导记录",
    "04_查重报告": "查重报告",
    "05_答辩及成绩评定": "答辩及成绩评定",
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--direction", required=True, help="如 01")
    ap.add_argument("--student-id", required=True, help="如 001")
    ap.add_argument("--student-name", required=True)
    ap.add_argument("--ws", default=os.environ.get("GRAD_WS", r"D:\Users\leibaihong\Desktop\课程材料优化\毕业设计智能管理工作区"))
    args = ap.parse_args()

    target_root = os.path.join(args.ws, "outputs", "方向" + args.direction,
                               "学生" + args.student_id + "_" + args.student_name)
    copied = []
    for src_sub, dst_sub in SUB_MAP.items():
        s = os.path.join(args.source, src_sub)
        d = os.path.join(target_root, dst_sub)
        if os.path.isdir(s):
            os.makedirs(d, exist_ok=True)
            for f in os.listdir(s):
                sp = os.path.join(s, f)
                if os.path.isfile(sp):
                    shutil.copy2(sp, os.path.join(d, f))
                    copied.append({"name": f, "student": args.student_name,
                                   "direction": "方向" + args.direction,
                                   "path": os.path.join(dst_sub, f),
                                   "status": "完成", "checked": False,
                                   "time": time.strftime("%Y-%m-%d %H:%M:%S")})
    registry_path = os.path.join(args.ws, "output_registry.json")
    reg = {"version": "1.0", "entries": []}
    if os.path.exists(registry_path):
        try:
            with open(registry_path, encoding="utf-8") as f:
                reg = json.load(f)
        except Exception:
            reg = {"version": "1.0", "entries": []}
    reg.setdefault("entries", []).extend(copied)
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
    print("COPIED", len(copied))
    print("TARGET", target_root)
    print("REGISTRY_ENTRIES", len(reg["entries"]))

if __name__ == "__main__":
    main()