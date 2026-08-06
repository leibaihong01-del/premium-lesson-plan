# GitHub Skill Regression Report

- 学生：戴吉祥
- Skill版本：v1.0-result-baseline
- Commit：ed58bee / e30468f

| 指标 | GitHub Skill版 | 王欢最终验收版 | 邱志豪最终验收版 |
|---|---|---|---|
| 正文字数 | 3782 | 12101 | 6974 |
| 章节数 | 25 | 38 | 28 |
| 表格数 | 14 | 6 | 6 |
| 参考文献 | 1 | 8 | 6 |
| 正文字号 | [12.0] | [15.0, 16.0, 26.0] | [15.0, 16.0, 26.0] |
| TOC | True | True | True |

## 生成链

- 入口：result_reference_builder（GitHub Skill v1.0 声明的模板保真重构）
- Prompt：prompts/manifest.yaml + prompts/translator/system.md
- 依赖：template_schema.json / result_generation_strategy.yaml / audit_rules.json