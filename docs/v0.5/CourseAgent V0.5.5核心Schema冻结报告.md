# CourseAgent V0.5.5 核心 Schema 冻结报告

版本：0.5.5
状态：冻结评审稿，经确认后作为 V0.5.5 数据模型基线
原则：先冻结数据模型，再编码；不修改 V0.4/V0.3 生产链路；新增模块默认关闭。

## 一、冻结范围

本次冻结四类核心数据模型：

1. Template Knowledge Model（模板约束）
2. Template Quality Memory（优秀成果规律）
3. Generation Plan（生成计划）
4. Experience Candidate（经验候选）

## 二、最终 Schema

### 1. Template Knowledge Model

```json
{
  "schema_version": "0.5.5",
  "template_id": "task_book_golden_v1",
  "template_type": "task_book",
  "source_evidence": {
    "source_file": "",
    "parsed_at": "",
    "parsed_by": "template_intelligence_layer"
  },
  "structure": {
    "table": {"rows": 18, "cols": 14},
    "regions": [
      {"name": "设计目标", "row_index": 4, "page_expected": 1,
       "fixed": false, "semantic_role": "goal_statement"}
    ],
    "binding": [
      {"from": "表注", "to": "表格首行", "invariant": true}
    ]
  },
  "space": {
    "page_constraint": 2,
    "regions": [
      {
        "name": "设计目标",
        "row_height_twips": 3670,
        "height_rule": "atLeast",
        "max_chars": 245,
        "recommended_chars": [100, 245],
        "max_non_empty_paragraphs": 6,
        "blank_paragraph_slack": 3,
        "text_wrap_estimate": {
          "mode": "char_width_based",
          "column_width_twips": 0,
          "chars_per_line": 0
        },
        "allow_expand": false
      }
    ]
  },
  "semantic_roles": {
    "goal_statement": "设计目标表述",
    "task_decomposition": "设计任务分解"
  },
  "invariants": ["总页数=2页", "时间安排结构不可破坏"],
  "generation_constraint": {
    "mode": "budget_based",
    "priorities": ["fixed_region_first", "capacity_before_generation", "blank_paragraph_slack_budget"]
  }
}
```

### 2. Template Quality Memory

```json
{
  "schema_version": "0.5.5",
  "template_id": "task_book_golden_v1",
  "golden_samples": [
    {
      "case_id": "wang_huan_taskbook",
      "quality_level": "golden",
      "source": "",
      "reason": "页面利用率、内容密度、表格稳定、层级清晰均达标",
      "applicable_scope": {"document_types": ["task_book"], "directions": ["AFC"]},
      "transfer_level": "structure_only",
      "accepted_at": ""
    }
  ],
  "visual_features": {
    "pages": 2,
    "content_density": {},
    "table_layout": {"rows": 18, "cols": 14, "stable": true},
    "blank_ratio": "low",
    "title_position": "fixed"
  },
  "content_features": {
    "设计目标": {
      "recommended_chars": [230, 260],
      "paragraphs": 6,
      "expression": "先总后分",
      "strategy": "总目标+分项目标+最终成果目标"
    }
  },
  "layout_features": {
    "region_ratio": {},
    "cross_page": "仅时间安排允许跨页",
    "blank_regions": "无异常空白"
  },
  "acceptance_threshold": {
    "pages": 2,
    "design_goal": {"chars": [230, 260], "non_empty_paragraphs": 6},
    "table": {"rows": 18, "cols": 14},
    "no_blank_page": true,
    "no_overflow": true
  }
}
```

### 3. Generation Plan

```json
{
  "schema_version": "0.5.5",
  "plan_id": "",
  "case_id": "",
  "template_id": "",
  "golden_reference_id": "wang_huan_taskbook",
  "content_allocation": {
    "设计目标": {
      "recommended_chars": [230, 260],
      "recommended_paragraphs": 6,
      "blank_paragraph_slack": 3,
      "text_wrap_estimate": {"chars_per_line": 0},
      "fixed": false
    }
  },
  "page_plan": {
    "page1": ["基本信息", "设计目标", "设计任务", "时间安排前段"],
    "page2": ["时间安排后段", "预期成果", "签字审核区"]
  },
  "risk_prediction": {
    "page_overflow_risk": "high",
    "risk_reason": []
  },
  "adjustment_recommendations": [],
  "recommended_strategy": "plan_then_generate"
}
```

### 4. Experience Candidate

```json
{
  "schema_version": "0.5.5",
  "case_id": "",
  "problem": "",
  "problem_layer": "template_space_constraint",
  "root_cause": "",
  "evidence": [],
  "strategy": "",
  "result": {
    "before": {},
    "after": {},
    "effect_score": 0
  },
  "feedback_source": "auto_detection | manual_review | final_acceptance",
  "validation_status": "candidate",
  "created_at": ""
}
```

## 三、字段说明

| 字段 | 所属模型 | 说明 | 来源 |
|---|---|---|---|
| row_index/page_expected | TKM | 区域位置与预期页 | 模板结构解析 |
| height_rule | TKM | atLeast/exact 软硬约束 | 模板行高解析 |
| blank_paragraph_slack | TKM/Plan | 空段落容量预算 | V0.5.2 验证发现 |
| text_wrap_estimate | TKM/Plan | 换行估算 | V0.5.2 验证发现 |
| source_evidence | TKM | 数据来源可追溯 | V0.5.2 验证发现 |
| golden_reference_id | Plan | 参考黄金样本 | V0.5.4 验证发现 |
| applicable_scope | TQM | 适用文档类型/方向 | V0.5.4 验证发现 |
| transfer_level | TQM | 可迁移级别 | V0.5.4 验证发现 |
| problem_layer | Experience | 问题所属层 | V0.5.1 审查 |
| feedback_source | Experience | 三类反馈来源 | V0.5.1 审查 |

### transfer_level 取值

- `structure_only`：只迁移结构/布局规律；
- `content_strategy`：可迁移内容组织策略；
- `not_transferable`：仅当前方向/案例适用。

## 四、模块关系

```
TKM（模板约束）
   +
TQM（优秀规律）
   ↓
Generation Planner
   ↓
Generation Plan
   ↓
现有 v03/v04 生成链路（默认关闭，不接入）
   ↓
Reviewer
   ↓
Experience Candidate
   ↓
人工确认后更新 TQM golden_samples
```

## 五、数据流

1. 解析模板 → TKM；
2. 加载黄金案例 → TQM；
3. 学生信息+课题+TKM+TQM → Generation Plan；
4. Plan 可选输入现有生成链路；
5. 验收结果 → Experience Candidate；
6. 人工确认 → TQM golden_samples 更新。

## 六、编码范围

本期编码实现：

- TKM 解析器（只读模板 → JSON）；
- TQM 加载器（读取 golden_samples 与阈值）；
- Generation Plan 构建器（容量对比 + 黄金参考 + 风险预测）；
- Experience Candidate 写入器（验收结果 → candidate）。

## 七、暂不实现范围

- Strategy Selector；
- 上下文老虎机；
- A/B 评估；
- AI 视觉模型；
- OCR 重新识别；
- 自动截图比较；
- 自动评分模型；
- 相似度算法；
- 经验自动升级 Skill；
- 修改 V0.4/V0.3 生产链路。

## 八、冻结检查

- [x] 四类核心模型已合并；
- [x] 吸收 golden_reference_id、applicable_scope、transfer_level、blank_paragraph_slack、text_wrap_estimate；
- [x] 字段来源可追溯；
- [x] 编码范围与暂缓范围明确；
- [x] 新增能力默认关闭。

经确认后，V0.5.5 作为 V0.5 编码前数据模型基线。
