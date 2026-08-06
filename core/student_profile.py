# -*- coding: utf-8 -*-
"""Student Profile：学生主数据唯一数据源。"""
from dataclasses import asdict, dataclass, field

REQUIRED_FIELDS = ["school", "college", "major", "class_name", "student_name",
                   "student_id", "advisor", "topic"]


@dataclass
class StudentProfile:
    school: str = ""
    college: str = ""
    major: str = ""
    class_name: str = ""
    student_name: str = ""
    student_id: str = ""
    advisor: str = ""
    topic: str = ""
    direction: str = ""
    extra: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data):
        data = dict(data or {})
        if "class" in data and "class_name" not in data:
            data["class_name"] = data.pop("class")
        extra_keys = set(data.keys()) - set(asdict(cls()).keys())
        extra = {k: data[k] for k in extra_keys}
        core = {k: data.get(k, "") for k in asdict(cls()).keys() if k != "extra"}
        return cls(**core, extra=extra)

    def to_dict(self):
        result = asdict(self)
        result["class"] = result.pop("class_name")
        result.pop("extra")
        return result

    def validate(self):
        missing = [f for f in REQUIRED_FIELDS if not getattr(self, f, "")]
        return missing