# -*- coding: utf-8 -*-
"""DocumentRouter：规则式路由，按文档类型选择 PipelineExecutor。"""
import os
import sys


class DocumentRouter:
    def __init__(self, core_path=None):
        self.core_path = core_path or os.path.dirname(os.path.abspath(__file__))
        if self.core_path not in sys.path:
            sys.path.insert(0, self.core_path)
        self.pipelines = {}

    def register(self, document_type, pipeline):
        self.pipelines[document_type] = pipeline

    def route(self, document_profile):
        doc_type = document_profile.get("document_type", "")
        if doc_type not in self.pipelines:
            raise KeyError("no pipeline for document_type=%s" % doc_type)
        return self.pipelines[doc_type]

    def build_result_pipeline(self, output_dir=None):
        from result_quality_pipeline import ResultQualityPipeline
        return ResultQualityPipeline(output_dir=output_dir)