# Result Skill CHANGELOG

## v1.2 (2026-08-05)

### Added

- 项目真实性与主体关联约束规则 v0.2（result_fact_rules.md）
- 参考文献格式统一规则（result_reference_format_rules.md）
- 模板 DNA 保护规则（result_template_dna_rules.md）
- 内容迁移质量规则（result_content_quality_rules.md）
- Result Quality Memory（result_quality_memory.json）

### Changed

- 生产流程拆分为 TemplateInstanceBuilder + ContentAdapter
- 模板实例化优先，禁止封面移植、强制字体、新增分节

### 原因

王欢成果 baseline 暴露：模板 DNA 破坏、虚构事实风险、参考文献格式不统一。
