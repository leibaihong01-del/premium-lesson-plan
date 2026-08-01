# -*- coding: utf-8 -*-
"""文档工程 Agent：读取任务与填充定义并生成文件。"""
import json
import os

from modules.document_writer import generate_document


def write_document(template_path, output_path, fills_path=None, fills=None, kind="lesson"):
    if fills is None:
        if fills_path and os.path.exists(fills_path):
            with open(fills_path, encoding="utf-8") as f:
                fills = json.load(f)
        else:
            fills = []
    return generate_document(template_path, output_path, fills, project_kind=kind)
