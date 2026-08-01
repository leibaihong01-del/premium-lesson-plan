# CourseAgent V1.0 阶段5.2：DeepSeek增强试点方案

版本：V1.0（设计稿）    日期：2026-08-02    状态：只设计，不写代码，等待人工确认
依据：AGENTS.md、ADR-005、《CourseAgent_V1.0升级架构设计.md》《CourseAgent_V1.0实施计划.md》

## 需求预审记录（ADR-005）

- 需求复述：设计一次可控的 DeepSeek 试验，验证“DeepSeek 能否提升 Translator 的需求理解与任务转译能力”，范围仅 Translator 单点，不做全链路接入。
- 信息完整性检查：明确输入（评测集、Prompt资产、现有Adapter/Router/Translator）、输出（设计文档）、约束（不写代码、不改Workflow、LLM必须走Adapter+Router、输出必须过Evaluation）。
- 第一性原理审查：真实问题是“规则转译缺口（基线5/10通过率）”；不是全面接模型，而是先验证收益；过度设计风险已识别（Vision/Embed/MiMo不进入本阶段）。
- 人工确认：本方案需人工确认后才进入5.2-A执行。

---

## 1. 试点目标

- 解决什么问题：规则 Translator 对复杂自然语言、缺失信息与隐性约束的识别不足（基线评测5/10通过）。
- 为什么需要 DeepSeek：需要语义理解来补齐“32学时、教案封面、评分≥95、申报书结构”等规则未捕获信息。
- 不使用LLM的限制：规则无法穷举表达模式，需求理解天花板明显，难以提升复杂任务转译质量。

## 2. 当前流程与增强后流程对比

现状：

```text
输入 → 规则Translator → Workflow
```

增强：

```text
输入 → 需求预审 → Router → DeepSeek Adapter → Translator增强 → TaskSpec → Workflow → Evaluation
```

原则：规则路径保留为基础路径、fallback路径、质量校验路径。

## 3. 接入范围

本阶段允许修改（实施阶段，非现在）：

- core/translator.py：启用/增强 `enrich_spec_with_llm()` 调用点；
- config/models.yaml：开启 deepseek.enabled（仅试点环境）；
- evaluation/runners/：新增 deepseek_runner.py（复用 mock_llm_runner 框架）；
- tests/：新增 DeepSeek 小规模评测测试。

不允许修改：

- agents/、modules/、capabilities/、state/、memory/ 核心实现；
- Orchestrator/Workflow 全链路；
- 其他模型（GLM/MiMo）与 Vision/Embed。

## 4. Prompt 设计

- system prompt：复用 `prompts/translator/system.md`（角色、JSON输出契约、约束）。
- translator prompt模板：复用 `prompts/translator/user_template.json`（request、user_profile 占位符）。
- 输入格式：原始需求 + 规则转译的 TaskSpec（作为上下文）+ 用户画像摘要。
- 输出格式：按 user_template 的 output_schema 输出 JSON，解析失败即回退规则。
- 版本管理：prompt 版本与 manifest 绑定；变更必须升版本并记录 change_log；评测报告记录 prompt_version。

## 5. Evaluation 方案

基于 `evaluation/cases/translator_cases.json`（v1.0，10案例）比较三模式：

- 规则 Baseline（已有：5/10）；
- DeepSeek 增强；
- Hybrid（规则通过则用规则，否则用 DeepSeek）。

指标：内容质量、结构完整、任务符合度、成本、响应时间。

决策规则：DeepSeek/Hybrid 必须优于或等于规则基线，且成本、延迟在预算内，才允许扩大接入。

## 6. 成本控制

- token限制：单次调用 max_tokens=512，输入裁剪到合理长度；
- 调用次数限制：每任务≤3次，试点总量≤50次；
- 缓存策略：相同输入指纹（request hash）复用结果；
- fallback策略：health_check非enabled、超时、解析失败、JSON校验失败均回退规则。

## 7. 风险分析

- LLM幻觉：输出必须通过 JSON Schema + 规则校验，不通过重试或回退；
- 输出不稳定：temperature=0.2，单次采样，不采用多次投票；
- 成本不可控：预算上限+调用计数+成本日志；
- Prompt漂移：版本化+评测回归；
- Memory污染：LLM 输出先校验，再经规则/人工确认后才写入 Memory。

## 8. 回滚方案

- 关闭 `config/models.yaml` 的 deepseek.enabled；
- Translator 自动走纯规则路径（enrich 默认不启用）；
- 删除 deepseek_runner 与试点测试不影响 Workflow；
- 回归测试（现有25+项）必须通过。

## 9. 实施步骤

- 5.2-A 设计确认：本方案人工确认；
- 5.2-B Mock测试：用 mock adapter 验证 enrich 与评测链路（不调用真实API）；
- 5.2-C 真实DeepSeek小规模调用：≤10案例、≤50次、预算与日志；
- 5.2-D Evaluation比较：规则 vs DeepSeek vs Hybrid 对比报告；
- 5.2-E 决定是否扩大接入：按评测指标与成本决策，不达标则维持规则路径。

---

本文件仅为设计，未创建或修改任何代码与现有文件；完成后停止，等待人工确认。
