# CourseAgent 稳定测试基线 v1.0

日期：2026-08-02
Git 标签：v1.0-baseline
说明：保存当前已验证稳定状态，作为后续开发与回滚基线。

## 一、测试结果

- 测试文件总数：10
- 通过：10
- 失败：0

测试文件列表：

- test_comparison.py
- test_deepseek.py
- test_deepseek_runner.py
- test_evaluation.py
- test_json_encoding.py
- test_memory_index.py
- test_model_adapter.py
- test_preflight.py
- test_router.py
- test_state.py

## 二、Evaluation 状态

- 规则基线：5/10 通过（内容质量 0.63，结构完整 1.0，任务符合度 0.7）；
- 外部独立案例：rule / hybrid / deepseek 均为 3/10（当前 DeepSeek 默认关闭，deepseek 模式回退规则）；
- Mock 对比：rule 5/10、llm 7/10、hybrid 7/10；
- 会话内 DeepSeek：rule 5/10、llm 10/10、hybrid 10/10（存在同模型偏差，仅作流程验证）；
- Evaluation 入口：run_evaluation.py、run_comparison.py、runners/deepseek_runner.py 均正常运行。

## 三、编码治理状态

- 扫描范围：evaluation/、prompts/、config/；
- JSON 文件总数：7；
- 当前 BOM 文件数：0；
- 已转换：evaluation/cases/translator_external_v1.0.json；
- 加载层：统一 utf-8-sig，兼容 UTF-8 与 UTF-8 BOM；
- 新增测试：test_json_encoding.py；
- 报告：evaluation/reports/Encoding_Report.md。

## 四、当前架构状态

- 主链路：Rule Workflow（规则 Translator + Orchestrator）；
- 模型层：ModelAdapter、ModelRegistry、DeepSeekAdapter（默认 disabled）；
- 路由层：rule / llm / hybrid 决策与 fallback；
- 状态层：TaskStore 已实现（未接入 Orchestrator 主流程）；
- 记忆层：JSON Memory + MemoryIndex 结构化索引；
- Prompt：manifest v1.0 + translator system/user template；
- Evaluation：案例集、指标、runner、报告；
- 5.2-E 小范围验证：Preflight Agent 与 Translator 增强入口已新增，默认关闭，不接管 Workflow。

## 五、回滚方式

- 代码回滚：git checkout v1.0-baseline；
- 功能回滚：config/agent_rules.yaml 中 translator.llm_enhance_enabled=false；
- 模型关闭：config/models.yaml 中 deepseek.enabled=false。