# 毕业设计成果专家能力包 v0.1

名称：GraduationDesign Result Skill v1.0
类型：复杂文档（模板保真重构：固定页 + 正文重构 + 格式继承）
状态：Active（已冻结基线）

## 能力清单

1. 模板解析：18 页 / 4 分节 / 6 表格 / 固定页（封面、真实性承诺及指导教师声明、目录、摘要）
2. 生成策略：学生成果初稿为内容底稿 + 模板格式标准化，禁止新增事实
3. 标题规则：一级 `1 引言`（Heading 1）、二级 `1.1 设计背景`（Heading 2）、条目 `（一）`（正文内容）
4. 格式规则：正文 12pt 宋体/Times New Roman，标题 15/16pt 黑体加粗
5. 内容逻辑：虚拟地点不得作为真实资料收集、调研、运行数据来源
6. 命名继承：[序号 ]学生姓名 毕业设计成果 选题名称.docx
7. 内部审核：内容 / 结构 / 格式 / 命名 / 内容逻辑 / 固定页缺口会审
8. 双版本交付：AI生成版（原始样本）+ 人工修订版（学习样本），详见 review_loop.md

## 执行入口

工作区模块：`00_系统配置/模块/v03/run_result_case.py`

参数：GRAD_STUDENT、GRAD_DIRECTION、GRAD_SEQ（默认 01）

## 模板保真重构

内容重新组织，但 Word 母版结构必须继承：模板复制 → 固定页字段替换 → 正文/参考文献替换 → 自动目录 → 保留分节/页码/页眉页脚。策略见 rules/result_generation_strategy.yaml。

## 规则来源

学校规范依据层：`../school_rules/`；成果内容合规执行层：`content_check/`（规则从 school_rules 加载，不维护独立违禁词库）。

## 正式生成入口

模板保真重构器（result_reference_builder.py）是正式生成入口；初稿标准化（result_generator.py）仅作内容预处理，不作为最终 Word 基版。


## v1.1 升级（索引化，通用规则）

新增能力入口（按需加载，不全文加载）：

- 工作流：`workflow.yaml`
- 内容规则：`rules/content_rules.yaml`
- 表格规则：`rules/table_rules.yaml`
- 目录规则：`rules/toc_rules.yaml`
- 学院规范：`rules/college_rules.yaml`
- 专业词库：`knowledge/profession_terms.yaml`
- 案例索引：`memory/golden_cases_index.md`、`memory/failure_cases_index.md`

执行模式：autonomous（自动扫描/定位/修复/渲染/报告，最终一次性汇报）。
验收模式：DOCX 结构检查 + PDF 视觉检查双通道。
原则：经验不进 Skill 正文，只进 memory 案例层。

## v1.2 升级（模板保护与内容质量）

当前版本：1.2

新增能力：

- 模板实例化优先：TemplateInstanceBuilder + ContentAdapter 两阶段分拆
- 项目真实性与主体关联约束（v0.2）
- 参考文献格式统一
- 内容迁移质量检查

使用规则：

- `rules/result_fact_rules.md`
- `rules/result_reference_format_rules.md`
- `rules/result_template_dna_rules.md`
- `rules/result_content_quality_rules.md`
- `memory/result_quality_memory.json`

生产流程：黄金模板复制 ? 字段替换 ? 内容迁移 ? 格式检查?
