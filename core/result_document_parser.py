# -*- coding: utf-8 -*-
"""Result Document Parser：只消费 DocumentStructure，执行成果语义理解，不直接读取 Word/PDF。"""
from document_structure_parser import parse as parse_structure
from result_semantic_analyzer import ResultSemanticAnalyzer


def parse(path_docx, path_pdf=None):
    structure = parse_structure(path_docx, path_pdf, document_type="result")
    analyzer = ResultSemanticAnalyzer()
    semantic = analyzer.analyze(structure)
    model = dict(structure)
    model.update({
        "document_type": "result",
        "title": semantic["metadata"]["title"],
        "sections": semantic["sections"],
        "references": semantic["references"],
        "reference_count": len(semantic["references"]),
        "captions": semantic["figures"],
        "body_paragraphs": semantic["body_paragraphs"],
        "body_chars": semantic["body_chars"],
        "body_font_sizes": semantic["body_font_sizes"],
        "body_east_asia_fonts": semantic["body_east_asia_fonts"],
        "fixed_markers": semantic["fixed_markers"],
        "semantic": semantic,
        "semantic_trace": analyzer.trace,
    })
    return model