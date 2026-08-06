# -*- coding: utf-8 -*-
"""Vision Constraint Planner：把视觉约束注入文档生成前的任务规划。"""
import copy

from context.vision_context import VisionContext


class VisionConstraintPlanner:
    def __init__(self, vision_result=None, context=None):
        self.context = context or VisionContext(vision_result)

    def plan(self, task_spec):
        spec = self.context.inject(task_spec)
        structure = self.context.structure
        plan = {
            "planning_stage": "vision_constraint_planning",
            "required_sections": list(structure.get("sections") or []),
            "layout_constraints": list(structure.get("layout_elements") or []),
            "page_size": structure.get("page_size", "A4"),
            "notes": list(structure.get("notes") or []),
            "generation_strategy": "template_aware",
        }
        spec["vision_plan"] = plan
        return spec, plan