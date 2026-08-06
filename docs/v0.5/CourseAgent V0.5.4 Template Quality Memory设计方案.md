# CourseAgent V0.5.4 Template Quality Memory 设计方案（复审修订版）

版本：0.5.4-review
状态：Schema 设计稿，未编码
原则：新增能力默认关闭；不影响 V0.4/V0.3 稳定生产链路；不改变已冻结的 V0.5.3 Schema。

## 〇、设计三问自检

1. 是否与 V0.5.3 接上：是。TKM 提供“模板约束”，TQM 提供“优秀成果表现规律”，两者共同输入 Generation Planner，不独立成视觉模块。
2. 是否把“优秀”定义清楚：是。用可解释的质量原则与特征阈值定义优秀，不用“和王欢长得像”。
3. 是否控制范围：是。本阶段只做 Schema + 黄金案例索引，不做 AI 视觉、OCR、截图比较、复杂评分。

## 一、背景

V0.5.3 已解决“是否符合模板”；V0.5.4 需要解决“是否接近优秀人工成果”，因此新增 Template Quality Memory。

## 二、与 V0.5.3 关系

```
Template Knowledge Model（模板要求什么）
        |
        |（模板约束）
        ↓
Generation Planner
        ↑
        |
Template Quality Memory（优秀成果应该是什么样）
        |
        ↓
黄金案例经验
```

边界：

- TKM 保存模板结构、空间、语义角色、不变式；
- TQM 保存优秀成果的表现规律：视觉特征、内容策略、布局规律、质量阈值；
- TQM 不保存模板结构；模板结构只属于 TKM。

## 三、“优秀”定义

优秀 = 可解释的质量特征，而不是与某个样本的相似度：

1. 页面利用率合理：2 页无空白页、无溢出；
2. 重点区域占比符合教师习惯：设计任务区域高、预期成果与签字区固定在第 2 页；
3. 内容密度适中：区域字符数、非空段落数落在合理区间；
4. 表格不破坏模板：行数、列数、行高、布局与模板一致；
5. 信息层级清晰：标题、区域角色、语义顺序明确；
6. 内容策略合理：设计目标如何组织、设计任务如何分解、哪些区域紧凑、哪些区域允许展开。

因此未来 Reviewer 比较的是“质量特征”，不是图片相似。

## 四、数据模型：quality_memory.json

```json
{
  "schema_version": "0.5.4",
  "template_id": "task_book_golden_v1",
  "golden_samples": [
    {
      "case_id": "wang_huan_taskbook",
      "quality_level": "golden",
      "source": "毕业设计智能制作工作区/06_输出成果/V0.3_王欢任务书验证",
      "reason": "页面利用率、内容密度、表格稳定、层级清晰均达标",
      "applicable_scope": ["task_book", "AFC方向"],
      "accepted_at": "2026-08-04"
    }
  ],
  "visual_features": {
    "pages": 2,
    "page_balance": "page1=基本信息+设计目标+设计任务+时间安排前段；page2=时间安排后段+预期成果+签字区",
    "content_density": "设计目标246字符/6段；设计任务201字符/7段；预期成果224字符/11段",
    "table_layout": {"rows": 18, "cols": 14, "stable": true},
    "row_heights": {"设计目标": 3670, "设计任务": 5102, "预期成果": 795},
    "blank_ratio": "低，无异常空白",
    "title_position": "与模板一致"
  },
  "content_features": {
    "设计目标": {
      "recommended_chars": [230, 260],
      "paragraphs": 6,
      "expression": "总目标+分项目标+最终成果目标",
      "strategy": "先总后分，覆盖知识/能力/素养/成果"
    },
    "设计任务": {
      "recommended_chars": [190, 220],
      "task_count": 6,
      "granularity": "逐项可执行",
      "strategy": "资料收集→文档撰写→结构原理→检修周期→作业流程→工具材料"
    },
    "预期成果": {
      "fixed_chars": 224,
      "paragraphs": 11,
      "note": "固定内容，无缩减余量"
    },
    "紧凑区域": ["基本信息", "时间安排", "签字审核区"],
    "允许扩展区域": ["设计任务"（受限扩展）]
  },
  "layout_features": {
    "region_ratio": {
      "基本信息": "固定",
      "设计目标": "行高3670",
      "设计任务": "行高5102",
      "时间安排": "固定6行",
      "预期成果+签字区": "第2页"
    },
    "cross_page": "仅时间安排允许跨页",
    "blank_regions": "无异常空白"
  },
  "acceptance_threshold": {
    "pages": 2,
    "design_goal": {"chars": [230, 260], "non_empty_paragraphs": 6},
    "design_task": {"chars": [190, 220], "non_empty_paragraphs": 7},
    "expected_result": {"chars": 224, "non_empty_paragraphs": 11},
    "table": {"rows": 18, "cols": 14},
    "no_blank_page": true,
    "no_overflow": true,
    "signature_on_page2": true
  }
}
```

## 五、风险对照

### 风险1：TQM 与 TKM 混在一起

结论：未混用。

- TKM：模板结构、空间、语义角色、不变式；
- TQM：优秀成果表现规律、内容策略、质量阈值；
- 禁止把“模板结构”写进 TQM。

### 风险2：只记录格式，不记录内容策略

结论：已补充内容策略。

- 设计目标：先总后分；
- 设计任务：资料收集→撰写→结构原理→检修周期→作业流程→工具材料；
- 紧凑区域 vs 允许扩展区域明确区分。

### 风险3：王欢变成唯一模板

结论：王欢只是黄金样本之一，不是唯一标准。

生成策略应为：

```
模板约束
+
相似优秀案例（按方向/文档类型检索）
+
当前任务特点
=
生成策略
```

- 电梯故障分析与 AFC 故障分析不一定完全一样；
- golden_samples 必须支持多个样本与 `applicable_scope`；
- 不允许“复制王欢”，只允许参考质量特征与内容策略。

## 六、调用流程

```
Generation Planner
      │ 读取
      ▼
TKM（模板约束） + TQM（优秀规律） + 当前任务特点
      │
      ▼
generation_plan.json
      │
      ▼
现有 v03/v04 生成链路（默认不受影响）
      │
      ▼
Reviewer（按 TQM 质量特征对比）
      │
      ▼
偏差报告
      │
      ▼
Experience System（人工确认后更新 golden_samples）
```

## 七、王欢黄金样本分析（为什么优秀）

- 页面利用率：2 页无空白页、无溢出；
- 内容密度：设计目标 246 字符/6 段、设计任务 201 字符/7 段、预期成果 224 字符/11 段；
- 重点区域占比：设计任务行高 5102，为最大内容区；预期成果与签字区固定在第 2 页；
- 表格稳定：18×14、行高 3670/5102/795，未破坏模板；
- 信息层级：基本区→目标→任务→时间→成果→签字，顺序清晰；
- 内容策略：目标先总后分，任务按执行路径分解，表达具体可执行。

## 八、后续编码边界

本阶段只实现：

- quality_memory.json Schema；
- 黄金案例索引（含 applicable_scope）；
- 默认关闭，不接入生成链路。

暂缓：

- AI 视觉模型；
- OCR 重新识别；
- 自动截图比较；
- 自动评分模型；
- 相似度算法；
- 自动更新 golden_samples。

## 九、风险分析

| 风险 | 说明 | 缓解 |
|---|---|---|
| 黄金样本过拟合 | 单一方向特征被当成全局标准 | golden_samples 多样本 + applicable_scope |
| 人工标注成本 | 优秀案例需人工确认 | 先以现有验收案例为候选 |
| 特征口径漂移 | 不同版本模板特征不同 | quality_memory 绑定 template_id |
| 数据隐私 | 学生信息进入记忆 | 案例记录脱敏 |
| 阈值误用 | 内容差异被误判为质量下降 | 阈值只提示不阻断 |
