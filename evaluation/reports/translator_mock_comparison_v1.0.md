# Translator Mock 对比报告（Evaluation框架验证）

案例版本 v1.0    Prompt版本 v1.0

| 模式 | 通过率 | 内容质量 | 结构完整 | 任务符合度 | 失败 |
|---|---|---|---|---|---|
| rule | 5/10 | 0.63 | 1.0 | 0.7 | 5 |
| llm | 7/10 | 0.74 | 1.0 | 0.8 | 3 |
| hybrid | 7/10 | 0.72 | 1.0 | 0.8 | 3 |

说明：Mock LLM Evaluation Harness：仅验证Evaluation比较框架；真实DeepSeek接入后替换simulate_llm
