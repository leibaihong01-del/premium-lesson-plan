# -*- coding: utf-8 -*-
"""DocumentStructure：统一文档结构模型（所有 Quality Sense 的唯一输入）。"""


def empty_document_structure(document_type="", source_path="", pdf_path=""):
    return {
        "document_id": "",
        "document_type": document_type,
        "source_path": source_path,
        "pdf_path": pdf_path,
        "paragraphs": [],
        "tables": [],
        "pages": {},
        "styles": {},
        "fields": {},
        "evidence": [],
        "full_text": "",
        "sections_count": 0,
    }