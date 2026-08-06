# CourseAgent V0.5.7 生成质量闭环 Schema 冻结设计

版本：0.5.7-draft
状态：冻结评审稿，未编码
依据：V0.5.6 生成质量闭环设计方案
原则：保持 V0.5.5 已有 Schema 稳定；新增闭环数据结构；不进入代码实现。

## 一、冻结目标

新增并冻结四类闭环数据模型：

1. Document Cognitive Model（生成认知模型）
2. Gap Report（差距报告）
3. Diagnosis Record（诊断记录）
4. Revision Plan（修正计划）

## 二、Document Cognitive Model

```json
{
  "schema_version": "0.5.7",
  "document_type": "task_book",
  "template_context": {
    "template_id": "task_book_golden_v1",
    "page_constraint": 2,
    "regions": ["基本信息", "设计目标", "设计任务", "时间安排", "预期成果", "签字审核区"]
  },
  "quality_context": {
    "golden_reference_ids": ["wang_huan_taskbook"],
    "applicable_scope": {"document_types": ["task_book"]},
    "acceptance_threshold": {
      "pages": 2,
      "design_goal": {"chars": [230, 260], "non_empty_paragraphs": 6}
    }
  },
  "task_context": {
    "major": "电梯系统",
    "topic": "太平街口站电梯常见故障分析与检修方案设计",
    "difficulty": "medium",
    "keywords": ["电梯", "故障分析", "检修方案"]
  },
  "generation_hint": {
    "strategy": "plan_then_generate",
    "risk_focus": ["blank_paragraph_slack", "text_wrap_estimate"]
  }
}
```

字段说明：

- `template_context`：模板知识，来自 TKM；
- `quality_context`：优秀规律与阈值，来自 TQM；
- `task_context`：当前任务特征，来自学生信息与课题；
- `generation_hint`：规划与风险关注点。

作用：Planner 必须同时使用三类上下文做取舍，不能只按模板或只按黄金样本生成。

## 三、Gap Report

```json
{
  "schema_version": "0.5.7",
  "gap_id": "",
  "case_id": "",
  "gap_type": "deviation",
  "severity": "high",
  "dimension": "space",
  "location": {
    "region": "设计任务",
    "page": 1,
    "row_index": 5
  },
  "expected": {"pages": 2, "non_empty_paragraphs": 7},
  "actual": {"pages": 3, "non_empty_paragraphs": 7},
  "delta": {"pages": "+1"},
  "judged_reasonable": false,
  "evidence": ["render_check.pdf", "internal_audit.md"],
  "recommendation": "收敛空段落并复核换行估算"
}
```

字段说明：

- `gap_type`：
  - `violation`：违反模板硬约束（如页数、固定结构、语义角色）；
  - `deviation`：偏离优秀样本分布，但可能合理；
- `judged_reasonable`：偏差是否合理；
- `severity`：high/medium/low；
- `evidence`：必须附检测证据，禁止无证据判定。

原则：`violation` 必须修正；`deviation` 先判断是否合理，合理则不强制修正。

## 四、Diagnosis Record

```json
{
  "schema_version": "0.5.7",
  "diagnosis_id": "",
  "case_id": "",
  "phenomenon": "第2页溢出，生成3页",
  "direct_cause": "内容高度超过区域容量",
  "root_cause": "生成阶段未控制内容密度和空段预算",
  "problem_layer": "template_space_constraint",
  "evidence_chain": [
    {"evidence": "render_check.pdf", "support": "3页"},
    {"evidence": "region_analysis", "support": "空段占用容量"}
  ],
  "confidence": "high",
  "adjustment_strategy": "按空白段预算收敛，并复核换行估算"
}
```

字段说明：

- 三级诊断链：`phenomenon` → `direct_cause` → `root_cause`；
- `problem_layer` 保持 V0.5.5 问题层分类；
- `evidence_chain` 支持可追溯；
- `confidence`：high/medium/low。

禁止只记录“超页”；必须记录直接原因与根本原因。

## 五、Revision Plan

```json
{
  "schema_version": "0.5.7",
  "revision_id": "",
  "case_id": "",
  "revision_scope": [
    {"region": "设计任务", "action": "调整内容密度"},
    {"region": "空段落", "action": "按 slack 预算收敛"}
  ],
  "protected_regions": [
    "student_info",
    "schedule",
    "signature"
  ],
  "modification_strategy": {
    "mode": "local_patch",
    "max_rounds": 2,
    "regenerate": false
  },
  "expected_outcome": {
    "pages": 2,
    "gap_types_resolved": ["violation"]
  }
}
```

字段说明：

- `revision_scope`：只列出需要修改的区域；
- `protected_regions`：禁止修改区域；
- `modification_strategy.mode`：`local_patch`，禁止全文重写；
- `max_rounds`：默认 2，防止无限重生成；
- `regenerate`：默认 false，表示局部修正优先。

## 六、与 V0.5.5 关系

| V0.5.5 模型 | V0.5.7 使用 |
|---|---|
| TKM | 生成 cognitive_model.template_context |
| TQM | 生成 cognitive_model.quality_context |
| Generation Plan | 输出后进入 Writer |
| Experience Candidate | 由 Revision Plan/验收结果生成 |

V0.5.7 不修改 V0.5.5 四个已冻结 Schema，只新增闭环数据结构。

## 七、数据流

```
TKM + TQM + 学生/课题
        ↓
Document Cognitive Model
        ↓
Generation Plan
        ↓
Writer → version1
        ↓
Reviewer → Gap Report
        ↓
Diagnosis Record（现象→直接原因→根本原因）
        ↓
Revision Plan（修改区域+保护区域）
        ↓
局部修正 → version2
        ↓
Reviewer 通过
        ↓
Experience Candidate
```

## 八、编码边界

本阶段：

- 只冻结 Schema；
- 不进入代码实现；
- 不影响 V0.4/V0.3。

后续编码范围：

- Cognitive Model 构建器；
- Gap Report 生成器；
- 三级诊断器；
- Revision Plan 构建器；
- 局部修正执行器（默认关闭）。

暂不实现：

- AI 视觉、OCR、截图比较；
- 自动评分/相似度；
- Strategy Selector；
- A/B 评估；
- 无限自动重生成；
- 自动更新黄金样本。

## 九、冻结检查

- [x] Document Cognitive Model 包含模板/黄金/当前任务三类上下文；
- [x] Gap Report 区分 violation / deviation；
- [x] Diagnosis Record 支持三级根因链；
- [x] Revision Plan 支持修改区域/保护区域/局部修正；
- [x] V0.5.5 Schema 保持稳定；
- [x] 编码边界与暂缓范围明确。

经确认后作为 V0.5.7 闭环数据模型基线。
