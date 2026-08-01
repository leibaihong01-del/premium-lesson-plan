# CourseAgent 当前技术状态报告

日期：2026-08-02
方式：只读代码核查，未修改任何代码
项目根目录：D:\Users\leibaihong\Desktop\课程材料优化\CourseAgent

## 0. 结论摘要

- 项目结构完整，共 67 个 Python 文件；
- 7 个测试文件全部通过（exit=0）；
- 项目不是 Git 仓库，无版本控制；
- Model Adapter、Router、State、Memory Index、Prompt、Evaluation 基础层已实现；
- LLM 增强尚未接入运行时 Workflow，DeepSeek 默认关闭；
- 阶段 5.2-E（是否扩大 DeepSeek 接入）仍等待人工决策。

## 1. 项目目录结构

| 目录 | 主要职责 |
|---|---|
| agents/ | planner、writer、reviewer、learner、light_judge、router_agent |
| capabilities/ | achievements、competition、research 能力模块 |
| config/ | agent_rules.yaml、models.yaml |
| core/ | orchestrator、translator、memory、skill、evolution、intent_alignment、problem_solver 等 |
| docs/ | 架构设计、实施计划、阶段方案、ADR、迁移文档 |
| evaluation/ | cases、metrics、runners、run_evaluation、run_comparison、reports |
| input/ | 输入文件 |
| memory/ | JSON 记忆与索引 |
| models/ | base、registry、deepseek 模型适配层 |
| modules/ | 模板解析、文档生成、格式检测、打包、路由辅助等 |
| output/ | 输出文件 |
| prompts/ | prompt 资产 |
| reports/ | 检测报告 |
| router/ | decision 路由 |
| state/ | 任务状态持久化 |
| tests/ | 7 个测试文件 |
| tools/ | 自检、知识监控、Skill 审计、升级审批等工具 |

根目录文件：main.py、batch_excellence.py、batch_score.py、README.md、requirements.txt。

## 2. Python 模块结构

- 67 个 Python 文件，覆盖 Agent 角色、能力、核心大脑、模型层、路由层、状态层、记忆层、工具层与评测层。
- 入口：main.py（总控）、core/orchestrator.py（任务闭环）。
- 模块间依赖：Orchestrator → Translator/Memory/Agents/Modules；Router 与 ModelAdapter 已独立成层，但尚未被 Orchestrator 调用。

## 3. 关键模块核对

### models/

| 文件 | 状态 | 说明 |
|---|---|---|
| models/base.py | 已实现 | ModelAdapter：generate()、health_check() 已实现；vision()、embed() 为 V1.0 预留，抛出 NotImplementedError |
| models/registry.py | 已实现 | ModelRegistry：register / get / list / clear |
| models/deepseek.py | 已实现 | DeepSeekAdapter：urllib 调用 chat/completions；enabled=false 默认关闭；API Key 仅从环境变量读取；未在 models/__init__.py 导出，也未注册进默认 Registry |
| models/__init__.py | 已实现 | 仅导出 ModelAdapter、ModelRegistry |

### router/

| 文件 | 状态 | 说明 |
|---|---|---|
| router/decision.py | 已实现 | decide()：rule / llm / hybrid 三策略；fallback_strategy() 统一回退规则 |
| router/__init__.py | 已实现 | 导出 decide、fallback_strategy |

### state/

| 文件 | 状态 | 说明 |
|---|---|---|
| state/store.py | 已实现 | TaskStore：new / save / load / delete / list / resume / append_log；JSON 存于 state/tasks，日志存于 state/logs |
| state/__init__.py | 已实现 | 导出 TaskStore |
| 集成情况 | 未接线 | Orchestrator 仍是内存状态机，未使用 TaskStore 做任务生命周期持久化 |

### memory/

| 文件 | 状态 | 说明 |
|---|---|---|
| core/memory.py | 已实现 | Memory：统一命名空间 put / get / add / search / query / counts / 用户偏好 |
| memory/index.py | 已实现 | MemoryIndex：结构化索引 rebuild / get / search；search 仍委托 JSON 子串匹配，未做语义检索 |

### prompts/

| 文件 | 状态 | 说明 |
|---|---|---|
| prompts/manifest.yaml | 已实现 | v1.0，登记 translator.system、translator.user_template |
| prompts/translator/system.md | 已实现 | 系统 Prompt，定义 JSON 输出契约 |
| prompts/translator/user_template.json | 已实现 | 用户模板与 output_schema |

### evaluation/

| 文件 | 状态 | 说明 |
|---|---|---|
| evaluation/cases/translator_cases.json | 已实现 | v1.0，10 个真实课程建设案例 |
| evaluation/metrics.py | 已实现 | 规则评分，不依赖 LLM 自评：content / structure / task_match / cost / evaluate |
| evaluation/run_evaluation.py | 已实现 | 规则基线评测入口 |
| evaluation/run_comparison.py | 已实现 | 兼容入口，转发 Mock Harness |
| evaluation/runners/mock_llm_runner.py | 已实现 | Mock LLM Evaluation Harness，确定性模拟，未来可替换为 DeepSeekAdapter |
| evaluation/runners/deepseek_runner.py | 未实现 | 尚未建立外部 DeepSeek 独立评测 runner |
| evaluation/reports/ | 已生成 | 规则基线、Mock 对比、会话内 DeepSeek 对比、失败案例 |

## 4. 已实现功能

- Agent 角色：planner / writer / reviewer / learner / light_judge / router_agent；
- 核心闭环：Orchestrator 文档任务闭环与能力模块闭环；
- 需求转译：规则 Translator + 可选 enrich_spec_with_llm；
- 记忆系统：JSON Memory + 用户偏好 + 结构化索引；
- 模型层：统一 ModelAdapter 接口、Registry、DeepSeek Adapter；
- 路由层：规则 / LLM / Hybrid 决策与降级；
- 状态层：TaskStore 持久化能力（待集成）；
- Prompt 资产：manifest + translator prompt；
- 评测：10 案例、规则指标、基线/Mock/会话内对比报告；
- 工具：自检、Skill 审计、知识监控、升级审批等；
- 模块：模板解析、文档生成、格式/内容检测、打包等。

## 5. 未实现设计

- vision()、embed()（V1.0 明确预留）；
- GLM、MiMo 具体 Adapter（config 已占位，代码未实现）；
- DeepSeek 默认注册进 Registry 与 models/__init__.py 导出；
- Orchestrator 接入 Router + ModelAdapter + DeepSeek；
- 独立 deepseek_runner（外部 API 复测）；
- Memory 语义检索（当前仅结构化索引）；
- TaskStore 与 Orchestrator 的任务生命周期集成；
- 文档修复循环中的真实修复动作（当前循环只重新 review 同一文件）；
- Git 版本控制。

## 6. 设计与实现差异

| 设计项 | 设计状态 | 实现状态 |
|---|---|---|
| LLM Enhanced Agent | 设计完成 | 基础层完成，运行时未接线 |
| 统一模型接口 | 设计完成 | base/registry/deepseek 已实现 |
| 模型路由 | 设计完成 | decision 已实现，未接入主流程 |
| 任务状态持久化 | 设计完成 | TaskStore 已实现，Orchestrator 未集成 |
| Memory 结构化 → 语义检索 | 设计演进路线 | 仅结构化索引 |
| Prompt 资产化 | 完成 | manifest + translator 已建立 |
| Evaluation 体系 | 完成基线 | 基线/Mock/会话内对比已产出，外部复测未做 |
| 自动修复 | 设计 max_loops=3 | 循环存在，但未真正修改文档 |
| 多模型（GLM/MiMo） | 未来扩展 | 仅 config 占位 |

## 7. 测试状态

- tests/ 下 7 个测试文件全部通过（exit=0）：
  - test_comparison.py、test_deepseek.py、test_evaluation.py、test_memory_index.py、test_model_adapter.py、test_router.py、test_state.py；
- 评测报告：
  - 规则基线：5/10（0.5），内容质量 0.63，结构完整 1.0，任务符合度 0.7；
  - Mock 对比：rule 5/10、llm 7/10、hybrid 7/10；
  - 会话内 DeepSeek：rule 5/10、llm 10/10、hybrid 10/10；
  - 注意：会话内评测存在同模型偏差，不能作为扩大接入的唯一依据。

## 8. 最近修改文件

| 文件 | 修改时间 |
|---|---|
| docs/migration/*（启动器/脚本/手册） | 2026-08-02 01:26-01:46 |
| docs/Codex_C盘迁移至D盘_Phase3_前置检查报告.md | 01:20 |
| docs/Codex_C盘迁移至D盘_Phase2_迁移方案.md | 01:17 |
| docs/Codex_C盘迁移审计_Phase1.md | 01:15 |
| docs/CourseAgent_V1.0阶段5.2-E_独立复核材料.md | 01:11 |
| docs/CourseAgent_V1.0阶段5.2-E_复核与决策清单.md | 01:10 |
| evaluation/reports/translator_deepseek_incontext_v1.0.* | 01:06 |
| evaluation/runners/mock_llm_runner.py | 00:55 |
| evaluation/reports/translator_mock_comparison_v1.0.* | 00:54 |
| evaluation/run_comparison.py | 00:50 |
| docs/CourseAgent_V1.0阶段5.2_DeepSeek增强试点方案.md | 00:48 |

结论：迁移开始前最后一次代码改动是 evaluation 层（00:50-00:55）；迁移期间未修改 CourseAgent 代码。

## 9. Git 状态

- CourseAgent 目录无 .git；
- 项目根目录无 .git；
- 结论：当前不是 Git 仓库，无分支、无提交记录，代码缺少版本控制与回滚能力。

## 10. TODO/FIXME

- README.md L59：visual_checker 标记为高算力档；
- docs/05_教师大脑架构设计V1.0.md：T-xxx 示例占位；
- 未发现代码内 TODO/FIXME/HACK/XXX。

## 11. 配置文件

### config/agent_rules.yaml

- 质量权重：模板 30 / 内容 25 / 教学 25 / 格式 20；
- 最低分：95；
- 修复轮次上限：3；
- 计算档位：low / medium / high。

### config/models.yaml

- 默认 provider 为空；
- deepseek：enabled=false，model=deepseek-chat，base_url 空，api_key_env=DEEPSEEK_API_KEY，timeout=30；
- glm / mimo：enabled=false，占位；
- 文件内无任何 API Key。

## 12. 依赖环境

- requirements.txt：python-docx、pyyaml、pdfplumber、pypdfium2；
- 运行时 Python：3.12.13；
- 已安装：pyyaml 6.0.3；
- 说明：DeepSeek Adapter 仅使用标准库 urllib，不依赖额外 SDK。

## 13. 风险点

1. 会话内 DeepSeek 评测存在同模型偏差，LLM 10/10 不能直接作为扩大依据；
2. LLM 层未接入 Orchestrator，当前生产路径仍是纯规则；
3. 文档修复循环未真正修复文件，max_loops 可能空转；
4. 无 Git，代码变更不可追踪、不可回滚；
5. JSON Memory 无 schema 校验，存在污染风险；
6. TaskStore 未集成，任务恢复仍依赖文件与 Codex 会话库；
7. DeepSeek Adapter 无重试、无成本统计、无独立 runner；
8. 5.2-E 决策未完成，后续阶段存在边界偏移风险。

## 14. 下一步建议

1. 先完成 5.2-E 人工决策（当前默认建议：不扩大，保持规则路径）；
2. 若扩大：先实现 evaluation/runners/deepseek_runner.py 外部复测，再接入 Translator 增强，保持规则 fallback；
3. 将 Router + ModelAdapter 接入 Orchestrator，作为可选增强路径，不替代规则；
4. 集成 TaskStore 到 Orchestrator，实现任务 ID、断点恢复、运行日志；
5. 修复文档闭环中的真实修复动作；
6. 初始化 Git 仓库，建立提交基线；
7. Memory 语义检索放后续阶段，不阻塞当前闭环。

本报告仅为技术状态核查，未生成代码、未做重构。