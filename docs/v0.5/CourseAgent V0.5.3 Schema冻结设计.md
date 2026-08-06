# CourseAgent V0.5.3 Schema 冻结设计

版本：0.5.3-draft
状态：冻结评审稿；经确认后作为 V0.5.3 核心数据模型基线
依据：《V0.5.2 邱志豪案例验证报告》与《V0.5.1 架构审查报告》

## 一、冻结目标

- 完成 Template Knowledge Model 最终结构；
- 验证 Generation Plan 可描述内容分配、页面规划、风险预测、调整建议；
- 验证 Experience Candidate 可记录案例、问题、根因、证据、策略、结果；
- 形成编码实施边界，冻结后再进入代码实现。

## 二、Template Knowledge Model（最终 JSON 结构）

```json
{
  "schema_version": "0.5.3",
  "template_id": "task_book_golden_v1",
  "template_type": "task_book",
  "source_evidence": {
    "source_file": "02_模板文件/01 杨振海 毕业设计任务书 ....docx",
    "parsed_at": "",
    "parsed_by": "template_intelligence_layer",
    "golden_case_ref": ["王欢", "汪子涵", "邱志豪"]
  },
  "structure": {
    "table": {"rows": 18, "cols": 14},
    "regions": [
      {
        "name": "基本信息",
        "row_range": [0, 3],
        "fixed": true,
        "semantic_role": "identity_region"
      },
      {
        "name": "设计目标",
        "row_index": 4,
        "page_expected": 1,
        "fixed": false,
        "semantic_role": "goal_statement"
      },
      {
        "name": "设计任务",
        "row_index": 5,
        "page_expected": 1,
        "fixed": false,
        "semantic_role": "task_decomposition"
      },
      {
        "name": "时间安排",
        "row_range": [6, 12],
        "page_expected": [1, 2],
        "fixed": true,
        "semantic_role": "timeline_section"
      },
      {
        "name": "预期成果",
        "row_index": 13,
        "page_expected": 2,
        "fixed": false,
        "semantic_role": "output_requirement"
      },
      {
        "name": "签字审核区",
        "row_range": [14, 17],
        "page_expected": 2,
        "fixed": true,
        "semantic_role": "approval_region"
      }
    ],
    "binding": [
      {"from": "表注", "to": "表格首行", "invariant": true},
      {"from": "预期成果", "to": "签字审核区", "invariant": true}
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
          "chars_per_line": 0,
          "note": "由解析器按列宽与字号计算"
        },
        "allow_expand": false
      },
      {
        "name": "设计任务",
        "row_height_twips": 5102,
        "height_rule": "atLeast",
        "max_chars": 199,
        "recommended_chars": [150, 199],
        "max_non_empty_paragraphs": 7,
        "blank_paragraph_slack": 3,
        "text_wrap_estimate": {
          "mode": "char_width_based",
          "column_width_twips": 0,
          "chars_per_line": 0,
          "note": "由解析器按列宽与字号计算"
        },
        "allow_expand": false
      },
      {
        "name": "预期成果",
        "row_height_twips": 795,
        "height_rule": "atLeast",
        "max_chars": 224,
        "recommended_chars": [224, 224],
        "max_non_empty_paragraphs": 11,
        "blank_paragraph_slack": 0,
        "text_wrap_estimate": {
          "mode": "char_width_based",
          "column_width_twips": 0,
          "chars_per_line": 0,
          "note": "固定内容，无缩减余量"
        },
        "allow_expand": false
      }
    ]
  },
  "semantic_roles": {
    "identity_region": "学生/学院/课题/指导教师信息",
    "goal_statement": "设计目标表述",
    "task_decomposition": "设计任务分解",
    "timeline_section": "固定进度安排",
    "output_requirement": "成果要求与形式",
    "approval_region": "签字与审核意见",
    "field": ["TOC", "PAGE"]
  },
  "invariants": [
    "总页数=2页",
    "时间安排结构不可破坏",
    "表格18行x14列不可变化",
    "签字审核区固定",
    "预期成果与签字区同页",
    "设计目标/设计任务/预期成果必须在各自页容量内"
  ],
  "generation_constraint": {
    "mode": "budget_based",
    "priorities": [
      "fixed_region_first",
      "capacity_before_generation",
      "blank_paragraph_slack_budget"
    ],
    "actions": [
      "按区域字符/段落预算分配内容",
      "超过容量前触发风险与调整建议",
      "固定区域不得扩展",
      "空段落按 slack 预算使用"
    ]
  }
}
```

### 字段来源说明

| 字段 | 来源 |
|---|---|
| row_range / page_expected | 模板表格行结构与 PDF 页面实测 |
| row_height_twips / height_rule | 模板 tblGrid/trHeight 解析 |
| max_chars / recommended_chars | 黄金模板内容实测（245/199/224） |
| max_non_empty_paragraphs | 黄金模板段落统计 |
| blank_paragraph_slack | V0.5.2 邱志豪验证发现：空段落是超页关键变量 |
| text_wrap_estimate | 验证发现：仅字符数不足以预测换行 |
| generation_constraint | 由空间约束与不变式推导的区域生成策略 |

## 三、Generation Plan（最终 JSON 结构）

```json
{
  "schema_version": "0.5.3",
  "plan_id": "plan_qzh_taskbook_v1",
  "template_id": "task_book_golden_v1",
  "content_allocation": {
    "设计目标": {
      "recommended_chars": [100, 245],
      "recommended_paragraphs": 6,
      "fixed": false
    },
    "设计任务": {
      "recommended_chars": [150, 199],
      "recommended_paragraphs": 7,
      "fixed": false
    },
    "预期成果": {
      "fixed_chars": 224,
      "fixed_paragraphs": 11
    },
    "时间安排": {
      "fixed": true
    }
  },
  "page_plan": {
    "page1": ["基本信息", "设计目标", "设计任务", "时间安排(前半)"],
    "page2": ["时间安排(后半)", "预期成果", "签字审核区"]
  },
  "risk_prediction": {
    "page_overflow_risk": "high",
    "risk_reason": [
      "课题名长度超过黄金样本",
      "设计任务接近容量上限",
      "内容区尾部空段落占用第2页空间",
      "预期成果无缩减余量"
    ]
  },
  "adjustment_recommendations": [
    "设计目标控制在 245 字符内",
    "设计任务控制在 199 字符内",
    "空段落使用不超过 3/3/0",
    "预期成果与签字区不得扩展"
  ],
  "recommended_strategy": "plan_then_generate"
}
```

### 覆盖检查

- 内容分配：`content_allocation` ✅
- 页面规划：`page_plan` ✅
- 风险预测：`risk_prediction` ✅
- 调整建议：`adjustment_recommendations` ✅

## 四、Experience Candidate（最终 JSON 结构）

```json
{
  "schema_version": "0.5.3",
  "case_id": "qiu_zhihao_taskbook",
  "problem": "固定页模板生成失败（首次渲染3页）",
  "problem_layer": "template_space_constraint",
  "root_cause": "生成阶段未考虑模板空间约束",
  "evidence": [
    "05_质量检查/邱志豪任务书V0.3内部审核/internal_audit.md",
    "05_质量检查/邱志豪任务书V0.3内部审核/render_check.pdf"
  ],
  "strategy": "生成前页面规划、区域容量预测、内容长度控制",
  "result": {
    "before": {"pages": 3, "pages_ok": false},
    "after": {"pages": 2, "pages_ok": true},
    "effect_score": 95
  },
  "feedback_source": "auto_detection",
  "validation_status": "candidate",
  "created_at": ""
}
```

### 覆盖检查

- 案例：`case_id` ✅
- 问题：`problem` ✅
- 根因：`problem_layer` + `root_cause` ✅
- 证据：`evidence` ✅
- 策略：`strategy` ✅
- 结果：`result` ✅

## 五、与 V0.4 链路关系

| V0.4 能力 | V0.5.3 关系 |
|---|---|
| `profile.py` 模板画像 | 升级为 Template Knowledge Model 解析基础 |
| `clean.py` Document IR | 复用为任务理解输入 |
| v03 任务书生成器 | 执行层，读取 plan 的调整建议（可选） |
| `diff.py` / `content_quality.py` | 产生验证结果，供 Experience Candidate 记录 |
| PDF 渲染检查 | 提供 evidence 与 before/after 页数 |

接口边界：

- V0.5.3 新模块默认关闭；
- plan 只作为可选输入，不修改 v03/v04 生成器；
- candidate 只写入经验候选目录，不升级 Skill。

## 六、编码实施边界

本期实现范围：

1. Template Knowledge Model 解析器（只读模板 → JSON）；
2. Generation Plan 构建器（容量对比 → plan）；
3. Experience Candidate 写入器（验收结果 → candidate）。

本期不实现：

- Strategy Selector；
- 上下文老虎机；
- A/B 评估；
- 经验自动升级 Skill；
- 自动修改现有生成链路。

编码检查点：

- Schema 冻结后进入实现；
- 邱志豪案例作为回归样例；
- 新模块开关默认关闭；
- 不改变 V0.4/V0.3 行为。
