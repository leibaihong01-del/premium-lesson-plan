# -*- coding: utf-8 -*-
"""Vision Constraint Planner 测试。"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from planner.vision_constraint_planner import VisionConstraintPlanner


class TestVisionPlanner(unittest.TestCase):
    def test_plan_injects_vision_plan(self):
        result = {"ok": True, "analysis": {"sections": ["教学目标", "教学评价"],
                                           "page_size": "A4", "layout_elements": ["title"]}}
        planner = VisionConstraintPlanner(result)
        spec, plan = planner.plan({"raw": "生成课程文档"})
        self.assertEqual(plan["planning_stage"], "vision_constraint_planning")
        self.assertIn("教学目标", plan["required_sections"])
        self.assertTrue(spec["planning_injected"])
        self.assertIn("vision_plan", spec)


if __name__ == "__main__":
    unittest.main()