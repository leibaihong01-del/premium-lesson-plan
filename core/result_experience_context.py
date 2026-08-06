# -*- coding: utf-8 -*-
"""ResultExperienceContext：成果生成专用经验中间对象（只读消费）。"""
from dataclasses import dataclass, field


@dataclass
class ResultExperienceContext:
    document_type: str = "result"
    student_name: str = ""
    template_source: str = ""
    golden_cases: list = field(default_factory=list)
    quality_rules: list = field(default_factory=list)
    reference_rules: list = field(default_factory=list)
    academic_rules: list = field(default_factory=list)
    tkm: dict = field(default_factory=dict)
    loaded_experience: list = field(default_factory=list)
    missing_experience: list = field(default_factory=list)
    generation_stage: str = "planning"

    def to_dict(self):
        return {
            "document_type": self.document_type,
            "student_name": self.student_name,
            "template_source": self.template_source,
            "golden_cases": self.golden_cases,
            "quality_rules": self.quality_rules,
            "reference_rules": self.reference_rules,
            "academic_rules": self.academic_rules,
            "tkm": self.tkm,
            "loaded_experience": self.loaded_experience,
            "missing_experience": self.missing_experience,
            "generation_stage": self.generation_stage,
        }