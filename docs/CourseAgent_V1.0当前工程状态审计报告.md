# CourseAgent V1.0 当前工程状态审计报告

日期：2026-08-02
方式：只读审计，未修改任何代码、配置、文档
Git 标签：v1.0-baseline（工作区干净）

## 1. 当前目录结构

| 目录 | 实际状态 |
|---|---|
| agents/ | 存在。planner / writer / reviewer / learner / light_judge / router_agent / preflight（新增） |
| capabilities/ | 存在。competition / research / achievements 能力模块 |
| config/ | 存在。agent_rules.yaml、models.yaml |
| core/ | 存在。orchestrator.py、translator.py、memory.py、skill.py、evolution.py 等 |
| docs/ | 存在。设计、实施、ADR、审计与基线文档 |
| evaluation/ | 存在。cases / metrics / runners / reports |
| input/ | 存在。输入文件 |
| memory/ | 存在。JSON 记忆与 index.py |
| models/ | 存在。base.py、registry.py、deepseek.py |
| modules/ | 存在。模板解析、文档生成、格式/内容检测、打包、路由辅助等 |
| output/ | 存在。输出文件 |
| prompts/ | 存在。manifest.yaml、translator/system.md、translator/user_template.json |
| reports/ | 存在。检测与评审报告 |
| router/ | 存在。decision.py |
| state/ | 存在。store.py 任务状态持久化 |
| tests/ | 存在。10 个测试文件 |
| tools/ | 存在。自检、Skill 审计、升级审批、知识监控等 |
| workflow/ | 不存在。实际工作流位于 core/orchestrator.py |
| translator/ | 不存在。实际转译实现位于 core/translator.py |

## 2. 当前运行链路

以代码实际为准，当前主链路为：

```text
用户输入
  ↓
Orchestrator.translate / run_document / run_capability
  ↓
core/translator.parse（规则关键词转译）
  ↓
TaskSpec
  ↓
文档闭环：reviewer.review → intent_alignment.check → packager.package → learner.learn
  ↓
Memory 沉淀
```

说明：

- Preflight Agent 已存在（agents/preflight.py），但 Orchestrator 未调用；
- Router 已存在（router/decision.py），但 Orchestrator 未调用；
- DeepSeek Adapter 已存在，但 Orchestrator 未调用；
- 当前链路是纯 Rule Workflow。

## 3. DeepSeek 当前接入状态

- models/deepseek.py：DeepSeekAdapter 存在，支持 generate()、health_check()、retry、timeout、cost 统计；默认 enabled=false，API Key 仅环境变量。
- models/__init__.py：已导出 DeepSeekAdapter。
- evaluation/runners/deepseek_runner.py：存在，按 rule / hybrid / deepseek 三种模式对比；deepseek 模式调用 core/translator.translate_with_enhancement。
- 是否进入 Workflow：否。Orchestrator 中无任何 deepseek 相关引用。
- 哪些模块可以调用模型：
  - core/translator.enrich_spec_with_llm；
  - core/translator.translate_with_enhancement；
  - evaluation/runners/deepseek_runner.py；
  - tests/test_deepseek.py（mock）。
- 哪些模块仍是 Rule 实现：
  - Orchestrator 主流程；
  - core/translator.parse；
  - agents/planner、writer、reviewer、learner；
  - modules/ 文档处理与检测；
  - capabilities/。

## 4. Router 当前状态

- router/decision.py 已实现 decide(spec, enabled_providers, compute_level)：
  - convert / audit → rule；
  - optimize / plan / generate → 有 provider 且 excellent → hybrid，否则 llm 或回退 rule；
  - high 算力且 provider 可用 → llm；
  - 默认 → rule。
- fallback_strategy() 可将 llm / hybrid 统一回退 rule。
- 是否被 Workflow 调用：否。Orchestrator 未引用 router/decision。
- 当前决策依据：任务 intent、quality、可用 provider、compute_level。
- 是否支持 Rule / LLM / Hybrid：支持（函数层），但尚未接入运行时。

## 5. Translator 当前状态

- core/translator.parse：规则关键词实现（意图、领域、质量、禁止词、模板、报告闭环），输出 TaskSpec（goal / intent / domains / deliverables / quality / constraints / compute_hint / confidence / raw）。
- core/translator.enrich_spec_with_llm：可选 LLM 增强，解析 JSON 后合并字段，异常回退原 spec。
- core/translator.translate_with_enhancement：新增小范围验证入口，默认 enabled=False，返回 (spec, route, enhanced)。
- Prompt 调用情况：prompts/ 资产已建立，但 Workflow 未调用；仅 evaluation/runners/mock_llm_runner.py 读取 user_template.json 作模板验证。
- 外部 translator 配置：无独立 translator/ 目录；配置在 config/agent_rules.yaml（translator.llm_enhance_enabled=false）。
- TaskSpec 生成流程：当前生产路径为规则 parse；LLM 增强仅测试与评测路径可用。

## 6. Evaluation 当前状态

- 案例数量：
  - evaluation/cases/translator_cases.json：10 个；
  - evaluation/cases/translator_external_v1.0.json：10 个（外部独立案例）。
- 指标：evaluation/metrics.py 提供 structure / content / task_match / cost / evaluate，全部为规则评分，不依赖 LLM 自评。
- Baseline 运行方式：python evaluation/run_evaluation.py 输出规则基线报告与失败案例。
- 模型对比能力：
  - run_comparison.py：Mock 对比（rule 5/10、llm 7/10、hybrid 7/10）；
  - deepseek_runner.py：外部独立案例对比（当前未启用 DeepSeek，rule/hybrid/deepseek 均为 3/10，deepseek 模式回退规则）；
  - 会话内 DeepSeek 对比报告存在：rule 5/10、llm 10/10、hybrid 10/10（存在同模型偏差，仅作流程验证）。

## 7. 当前技术债和风险

- 架构风险：Router、ModelAdapter、DeepSeek、Preflight 均为独立存在，未接入 Orchestrator；LLM 层当前只是“能力存在”，不是“运行能力”。
- 模块耦合：Orchestrator 直接依赖 agents、modules、docx 等，缺少依赖注入；若接入 Router/Adapter 需要小步改造。
- 文档修复循环：run_document 中 repair 循环只重新 review 同一文件，未真正修改文档，可能空转。
- 任务状态：TaskStore 已实现，但 Orchestrator 未使用，任务恢复仍依赖文件与会话库。
- Memory：JSON 无 schema 校验，索引为结构化索引，非语义检索；存在污染风险。
- DeepSeek 接入风险：外部 API 独立评测尚未执行（无 Key/未启用）；会话内评测存在同模型偏差；无运行时预算上限，只有 usage 统计。
- 命名差异：设计文档中的 workflow/、translator/ 目录与实际实现（core/orchestrator.py、core/translator.py）不一致，容易造成误导。

## 8. 给下一阶段建议

针对《CourseAgent_V1.0阶段5.2_DeepSeek模型治理与增强试点》：

### 第一优先级

1. 用真实 DeepSeek API（或经 CCSwitch 的独立通道）运行 evaluation/runners/deepseek_runner.py，产出外部独立对比报告；
2. 设定并执行 token/成本预算，验证 retry/timeout/fallback/cost 统计；
3. 保持 deepseek.enabled=false 默认关闭，Rule Workflow 不受影响。

### 第二优先级

1. 以“可选增强节点”方式接入 Preflight + Translator 增强：
   - config 开关控制；
   - Router 决策；
   - 规则优先、LLM 失败回退；
   - LLM 输出必须过 Evaluation；
2. 接入时保持 Orchestrator 主链路不变，只扩展 translate 路径。

### 暂不建议

- 全面接管 Orchestrator；
- 同时接入 GLM / MiMo；
- 引入语义检索或大规模重构；
- 在外部验证完成前默认启用 DeepSeek。

本报告为只读审计结果，未修改任何文件，未提交 Git。