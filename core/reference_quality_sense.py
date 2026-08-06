# -*- coding: utf-8 -*-
"""Reference Quality Sense：Word结构 + PDF视觉空间证据联合判断。"""
import datetime
import re

from pdf_layout_evidence import reference_layout_evidence

POLLUTION_WORDS = ["查看", "全文", "链接", "访问", "URL", "http", "https", "网页"]
HIDDEN_CONTROL = [chr(c) for c in range(0, 32) if c not in (9, 10, 13)]
HANGING_OFFSET_PT = 15.0


class ReferenceQualitySense:
    name = "Reference Quality Sense"

    @staticmethod
    def _evidence_id(prefix, idx):
        return "%s-%s-%03d" % (prefix, datetime.date.today().strftime("%Y%m%d"), idx)

    def check(self, model):
        refs = model.get("references", [])
        checks = []

        checks.append({"type": "reference_count", "count": len(refs),
                       "status": "pass" if refs else "fail"})

        numbers = []
        for r in refs:
            m = re.match(r"^\s*\[?(\d+)\]?", r.get("text", ""))
            if m:
                numbers.append(int(m.group(1)))
        dup = sorted({n for n in numbers if numbers.count(n) > 1})
        missing = [i for i in range(1, max(numbers) + 1) if i not in set(numbers)] if numbers else []
        checks.append({"type": "numbering", "duplicate": dup, "missing": missing,
                       "status": "fail" if (dup or missing) else "pass"})

        pollution = []
        nbsp = 0
        hidden = 0
        for r in refs:
            text = r.get("text", "")
            for w in POLLUTION_WORDS:
                if w in text:
                    pollution.append({"word": w, "context": text[:60]})
            nbsp += text.count("\u00a0")
            hidden += sum(1 for ch in text if ch in HIDDEN_CONTROL)
        checks.append({"type": "content_pollution", "words": pollution,
                       "nbsp_count": nbsp, "hidden_chars": hidden,
                       "status": "fail" if (pollution or nbsp or hidden) else "pass"})

        # DOCX 结构证据：悬挂缩进属性
        docx_visual = []
        for r in refs:
            if r.get("chars", 0) > 60:
                left = r.get("left_indent_emu")
                first = r.get("first_line_indent_emu")
                docx_visual.append({
                    "paragraph_id": r.get("index"),
                    "left_indent_emu": left,
                    "first_line_indent_emu": first,
                    "hanging_applied": bool(left is not None and first is not None and first < 0),
                })
        checks.append({"type": "docx_hanging_indent", "items": docx_visual,
                       "status": "pass" if docx_visual and all(i["hanging_applied"] for i in docx_visual) else "review"})

        # PDF 空间证据：首行/续行坐标
        spatial = []
        layout = model.get("layout_evidence")
        if layout:
            for ev in reference_layout_evidence(layout, refs):
                if ev.get("offset_pt") is None:
                    continue
                offset = ev["offset_pt"]
                ok = offset >= HANGING_OFFSET_PT
                spatial.append({
                    "evidence_id": self._evidence_id("REF", ev.get("reference_index", 0) + 1),
                    "reference_no": ev.get("reference_no"),
                    "paragraph_id": ev.get("paragraph_id"),
                    "page": ev.get("page"),
                    "first_line_x": ev.get("first_line_x"),
                    "continuation_x": ev.get("continuation_x"),
                    "offset_pt": offset,
                    "status": "pass" if ok else "review",
                    "problem_type": "reference_layout" if not ok else None,
                    "root_cause": "hanging_indent_not_applied" if not ok else None,
                    "recommendation": "set_hanging_indent_from_template（当前模板约0.74cm）" if not ok else None,
                })
        checks.append({"type": "pdf_visual_hanging_indent", "items": spatial,
                       "status": "review" if any(s["status"] == "review" for s in spatial) else "pass"})

        status = "fail" if any(c.get("status") == "fail" for c in checks) else (
            "review" if any(c.get("status") == "review" for c in checks) else "pass")
        return {"sense": self.name, "status": status, "checks": checks}