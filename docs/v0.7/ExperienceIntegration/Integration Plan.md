# Integration Plan（经验接入生产链路方案）

版本：0.7-integration-v1
原则：不修改 V0.4/V0.6/V0.3 旧生产链路；新增 V0.7 经验调用层，默认关闭；经验只读；先分析后实施；人工确认后才能固化新经验。

## 一、目标

让已固化经验真正进入生成链路，形成：

```text
输入
 ↓
Template Understanding（加载 TKM）
 ↓
Generation Planning（加载 Quality Memory / Golden Case）
 ↓
Content Generation（复用 V0.3 生成器，不修改）
 ↓
Quality Sense（Document / Reference / Character / Page Semantic）
 ↓
Revision Planner（根据经验约束给出修正）
 ↓
Final Validation
 ↓
Output Naming Sense
```

## 二、总体方案

新增独立的 V0.7 Skill runner（默认关闭），内部复用旧生成器，但不修改它们：

| 新模块 | 职责 | 复用 |
|---|---|---|
| ExperienceLoader | 读取 TKM / Quality Memory / validated experience | 无 |
| ResultGenerationSkillRunner | 成果生成编排 | result_reference_builder.py（正式入口） |
| TaskBookGenerationSkillRunner | 任务书生成编排 | v03 taskbook_generator + v06 planner（临时启用） |
| EvaluationFormSkillRunner | 成绩评定表编排 | 现有模板填充逻辑 |
| DefenseRecordSkillRunner | 答辩记录表编排 | 现有模板填充逻辑 |
| QualitySenseExecutor | 统一执行各项 Sense | 自写检查升级为正式执行器 |
| RevisionPlanner | 根据 Sense 输出修正计划 | 最小局部修正 |

## 三、实施顺序

### P1 经验注册与加载

1. 建立 `result_quality_memory.json`（从 result/rules 与 golden case 提炼）。
2. 建立 `experience_registry.json`，登记全部已验证经验与文件位置。
3. 实现 ExperienceLoader：加载 TKM、Quality Memory、Golden Case、Reference Quality Experience。

### P2 成果链路接入

1. 用 result_reference_builder.py 作为成果正式生成入口。
2. 生成前：ExperienceLoader 注入 Result TKM、Result Quality Memory、Golden Case。
3. 生成后：执行 Document Quality Sense、Reference Quality Sense、Character Style Sense。
4. 有偏差时：RevisionPlanner 生成最小修正计划，执行后重新验证。
5. 参考文献区域必须调用 reference_quality_experience（悬挂缩进、续行对齐、污染清理）。

### P3 任务书链路接入

1. 在 TaskBookSkillRunner 中加载 Page Semantic Layout Invariant。
2. 生成后校验：第一页 设计目标+设计任务，第二页 预期成果+设计进程+签字。
3. 发现跨页时进入 Revision Planner，不直接接受结构通过。

### P4 成绩评定表 / 答辩记录表 Skill 可执行化

1. 把当前临时脚本封装为 EvaluationFormSkillRunner / DefenseRecordSkillRunner。
2. 显式加载 evaluation_form/defense_record 的 TKM 与 Quality Memory。
3. 内置 Table Structure Sense、Region Integrity Sense、Character Style Sense、Output Naming Sense。

### P5 回归验证

用王欢、邱志豪、汪子涵、陈家宝四个案例回归：

- 同一经验在不同案例是否生效；
- 问题是否由“事后修复”前移到“生成前预防”；
- 输出是否满足 Output Naming Sense；
- 全部通过后才讨论是否默认启用。

## 四、验收标准

1. 生成链路日志记录每个节点的经验加载项。
2. knowledge_used 与经验文件必须真实可追溯，禁止只写声明。
3. 同一文档生成两次结果稳定。
4. 历史问题（姓名加粗、参考文献缩进、任务书跨页、成果固定页缺失）不再复现。
5. 不修改 V0.3/V0.4/V0.6 任何既有脚本。

## 五、边界

- V0.7 Skill runner 默认关闭；
- 经验加载为只读；
- 不自动升级经验；
- 不自动修改 Skill/Prompt/长期知识；
- 每次接入一个文档类型，验证后再接入下一个。