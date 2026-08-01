# CourseAgent V1.0 阶段5.2-E 小范围验证实施方案（设计）

日期：2026-08-02
状态：设计已完成，待进入代码实现
模式：小范围验证，不接管 Workflow

## 一、定位与目标

验证 DeepSeek 是否能够提升：

1. 需求理解；
2. Translator 质量；
3. TaskSpec 质量。

目标不是替换 Workflow，而是先做可回滚、可量化的小范围验证。

## 二、执行原则

1. 保留现有 Rule Workflow 作为主链路；
2. DeepSeek 只作为增强节点接入；
3. 所有 LLM 输出必须经过 Evaluation；
4. 保留 Fallback 机制；
5. 每一步可回滚。

## 三、Git 版本管理

- 在 CourseAgent 目录初始化 Git 仓库；
- 通过 .gitignore 排除 __pycache__、input、output、state/tasks、state/logs、.env、*.log；
- 提交当前状态并打标签 v1.0-baseline；
- 后续代码变更基于该基线，回滚使用 git checkout v1.0-baseline 或配置开关关闭。

## 四、DeepSeek 独立评测设计

### 1. 外部测试案例

- 新增 evaluation/cases/translator_external_v1.0.json；
- 10 个外部案例，与阶段5.2 会话内案例集相互独立；
- 覆盖课程标准、教学进度计划、教案、实训、课件、题库、竞赛、教研、审核等场景；
- 每个案例包含 input 与 expected TaskSpec。

### 2. 对比模式

| 模式 | 说明 |
|---|---|
| rule | 纯规则 Translator |
| hybrid | 规则通过则保持规则；规则不通过才启用 LLM 增强 |
| deepseek | 强制 DeepSeek 增强；不可用时自动回退规则并标记 |

### 3. 指标与独立性

- 指标：内容质量、结构完整、任务符合度、成本、失败案例；
- 统一使用 evaluation/metrics.py 规则评分，不依赖 DeepSeek 自评；
- 输出 evaluation/reports/translator_external_verification_v*.md/json；
- 建议人工抽验 3 个案例作为最终确认。

### 4. Runner

- 新增 evaluation/runners/deepseek_runner.py；
- 无 API Key 或模型未启用时，deepseek 模式自动回退规则并记录 llm_enabled=false。

## 五、接入点设计

优先两个接入点，不接管 Orchestrator：

### 1. Preflight Agent

- 新增 agents/preflight.py；
- 执行需求预审四步：需求复述、信息完整性检查、第一性原理审查、确认状态；
- 输出 preflight 报告，标记 needs_confirmation；
- 仅作为增强节点，不阻塞主链路。

### 2. Translator 增强

- 在 core/translator.py 新增 translate_with_enhancement(request, user_profile, adapter, enabled)；
- 流程：规则 parse → 可选 LLM enrich → 任何异常/无效输出回退规则；
- 返回 (spec, route, enhanced)，默认 enabled=False。

## 六、风险控制

### DeepSeek Adapter 加固

- retry：失败自动重试（max_retries，指数退避）；
- timeout：可配置；
- cost 统计：记录 calls、input_tokens、output_tokens、cost；
- fallback：generate 失败抛异常，由 Translator 增强层回退规则；
- health_check：未启用 / 无 Key / base_url 未配置均返回不可用状态。

### 配置开关

- config/models.yaml：deepseek 默认 enabled=false，新增 max_retries、retry_delay、价格参数；
- config/agent_rules.yaml：新增 translator.llm_enhance_enabled=false、preflight.enabled=true。

## 七、实施步骤

| 步骤 | 内容 |
|---|---|
| 5.2-E-1 | Git 基线 v1.0-baseline |
| 5.2-E-2 | DeepSeek Adapter 加固（retry/timeout/cost/fallback） |
| 5.2-E-3 | 外部案例集 + deepseek_runner + 对比报告 |
| 5.2-E-4 | Preflight Agent + Translator 增强接线 |
| 5.2-E-5 | 全量测试 + 小范围验证报告 + 人工抽查 |

## 八、验证与回滚

- 验证：现有 7 个测试 + 新增测试全部通过；外部评测报告生成；配置开关默认关闭，主链路行为不变；
- 回滚：设置 llm_enhance_enabled=false 即恢复纯规则；代码回滚使用 git checkout v1.0-baseline。

## 九、范围边界

- 不修改 Orchestrator 主流程；
- 不默认启用 DeepSeek；
- 不删除任何现有模块；
- 本次实现仅新增与加固，不重构。