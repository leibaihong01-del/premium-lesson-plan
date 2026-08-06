# -*- coding: utf-8 -*-
"""Word 模板净化：移除批注、修订痕迹、隐藏文字，生成正式生成模板。"""
import os, re, shutil, zipfile
from lxml import etree

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
      "pr": "http://schemas.openxmlformats.org/package/2006/relationships"}

REMOVE_TAGS = [
    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}commentRangeStart",
    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}commentRangeEnd",
    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}commentReference",
    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}del",
    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}delText",
    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPrChange",
    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPrChange",
    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tblPrChange",
    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}trPrChange",
    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tcPrChange",
    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}bookmarkStart",
    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}bookmarkEnd",
]
UNWRAP_TAG = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ins"
VANISH = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}vanish"
RUN = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r"

DROP_PARTS = ("word/comments.xml", "word/commentsExtended.xml", "word/people.xml",
              "word/commentsIds.xml", "word/commentsExtensible.xml")

def purify_document(xml_bytes):
    root = etree.fromstring(xml_bytes)
    for tag in REMOVE_TAGS:
        for el in root.iter(tag):
            parent = el.getparent()
            if parent is not None:
                parent.remove(el)
    for el in list(root.iter(UNWRAP_TAG)):
        parent = el.getparent()
        if parent is None:
            continue
        idx = parent.index(el)
        for child in list(el):
            parent.insert(idx, child)
            idx += 1
        parent.remove(el)
    for run in list(root.iter(RUN)):
        rPr = run.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr")
        if rPr is not None and rPr.find(VANISH) is not None:
            parent = run.getparent()
            if parent is not None:
                parent.remove(run)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)

def purify(src, dst):
    zin = zipfile.ZipFile(src, "r")
    names = zin.namelist()
    drop = set(DROP_PARTS)
    data = {}
    doc_name = "word/document.xml"
    for name in names:
        raw = zin.read(name)
        if name == doc_name:
            raw = purify_document(raw)
        data[name] = raw
    zin.close()
    # drop comment parts
    for name in drop:
        data.pop(name, None)
    # fix document rels
    rels_name = "word/_rels/document.xml.rels"
    if rels_name in data:
        rels = etree.fromstring(data[rels_name])
        for rel in list(rels):
            target = rel.get("Target") or ""
            if any(p.split("/")[-1] in target for p in drop):
                rels.remove(rel)
        data[rels_name] = etree.tostring(rels, xml_declaration=True, encoding="UTF-8", standalone=True)
    # fix content types
    ct_name = "[Content_Types].xml"
    if ct_name in data:
        ct = etree.fromstring(data[ct_name])
        for ov in list(ct):
            pn = ov.get("PartName") or ""
            if any(("/" + p.split("/")[-1]) in pn for p in drop):
                ct.remove(ov)
        data[ct_name] = etree.tostring(ct, xml_declaration=True, encoding="UTF-8", standalone=True)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, raw in data.items():
            zout.writestr(name, raw)
    return dst

def stats(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "replace")
    return {
        "comments": xml.count("commentRangeStart") + xml.count("commentReference"),
        "ins": xml.count("<w:ins "),
        "del": xml.count("<w:del "),
    }

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    args = ap.parse_args()
    purify(args.src, args.dst)
    print("PURIFIED", args.dst, stats(args.dst))