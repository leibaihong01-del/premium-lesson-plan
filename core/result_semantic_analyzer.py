# -*- coding: utf-8 -*-
"""ResultSemanticAnalyzer：消费 DocumentStructure，输出成果语义结构（不读取 Word/PDF）。"""
import re


def _heading_level(text, style=None):
    t = (text or "").strip()
    if style and re.search(r"\d", style or "") and ("Heading" in style or "heading" in style or "标题" in style):
        return int(re.search(r"\d", style).group(0))
    m = re.match(r"^(\d+(?:\.\d+)*)", t)
    if m:
        return m.group(1).count(".") + 1
    if re.match(r"^（[一二三四五六七八九十]+）", t):
        return 3
    if re.match(r"^[一二三四五六七八九十]+、", t):
        return 1
    if t in ("参考文献", "摘要", "结论", "总结", "致谢", "附录"):
        return 1
    return None


class ResultSemanticAnalyzer:
    def __init__(self):
        self.sections = []
        self.references = []
        self.captions = []
        self.metadata = {}
        self.trace = []

    def analyze(self, structure):
        paragraphs = structure.get("paragraphs", [])
        sections = []
        references = []
        captions = []
        body_paras = 0
        body_chars = 0
        body_font_sizes = set()
        body_east_asia_fonts = set()
        in_ref = False

        for p in paragraphs:
            text = p.get("text", "")
            style = p.get("style", "")
            idx = p.get("index")
            lvl = _heading_level(text, style)
            if text == "参考文献":
                in_ref = True
                sections.append({"section": text, "level": 1, "start_page": None,
                                 "evidence": "paragraph_%s" % idx})
                continue
            if in_ref and text:
                references.append({
                    "index": idx,
                    "text": text,
                    "style": style,
                    "left_indent_emu": p.get("left_indent_emu"),
                    "first_line_indent_emu": p.get("first_line_indent_emu"),
                    "line_spacing": p.get("line_spacing"),
                    "font_sizes": sorted({r.get("size_pt") for r in p.get("runs", []) if r.get("size_pt")}),
                    "chars": len(text),
                })
                continue
            if re.match(r"^(表|图)\s*\d+(\.\d+)*", text):
                captions.append({"index": idx, "type": "表注" if text.startswith("表") else "图注",
                                 "text": text[:60]})
            if lvl:
                sections.append({"section": text, "level": lvl, "start_page": None,
                                 "evidence": "paragraph_%s" % idx})
            elif text:
                body_paras += 1
                body_chars += len(text)
                for r in p.get("runs", []):
                    if r.get("size_pt"):
                        body_font_sizes.add(round(r["size_pt"], 1))
                    if r.get("east_asia"):
                        body_east_asia_fonts.add(r["east_asia"])

        fixed_markers = {}
        full = structure.get("full_text", "")
        for k in ["长沙轨道交通职业学院", "毕业设计真实性承诺", "目  录", "摘要", "参考文献"]:
            fixed_markers[k] = k in full

        semantic = {
            "document_type": "graduation_result",
            "cover": {"fields": structure.get("fields", {})},
            "metadata": {
                "title": paragraphs[0].get("text", "") if paragraphs else "",
                "toc_field_present": structure.get("toc_field_present", False),
                "sections_count": structure.get("sections_count", 0),
                "pages": (structure.get("pages") or {}).get("count"),
            },
            "sections": sections,
            "references": references,
            "tables": structure.get("tables", []),
            "figures": captions,
            "evidence": structure.get("evidence", []),
            "body_paragraphs": body_paras,
            "body_chars": body_chars,
            "body_font_sizes": sorted(body_font_sizes),
            "body_east_asia_fonts": sorted(body_east_asia_fonts),
            "fixed_markers": fixed_markers,
        }
        self.trace = [
            {"field": e.get("field"), "value": e.get("value"), "source": e.get("source_location"),
             "used_by": ["DocumentConsistencySense", "ContentQualitySense"]}
            for e in structure.get("evidence", [])
        ]
        return semantic