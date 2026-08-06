# Result Pipeline Audit Report

版本：0.7-result-audit-v1
日期：2026-08-05
对象：毕业设计成果生成链路
结论：成果当前存在三条实际路径；正式声明的 result_reference_builder.py 未被完整包调用；经验文件真实存在但未进入生成。

## 一、当前成果真实入口

| 路径 | 入口脚本 | 说明 | 是否当前生产 |
|---|---|---|---|
| V0.3 学习/生产路径 | v03/run_result_case.py | result_generator 初稿标准化 + result_audit 自动修复 | 是 |
| 正式重构器（Skill 声明入口） | v03/result_reference_builder.py | 模板保真重构，SKILL.md 声明为正式入口 | 否（未被默认调用） |
| V0.7 完整成果包路径 | v06/run_v07_complete_package_*.py | 黄金模板前页 + V0.3 成果正文合并，自写检查 | 是（完整包验证使用） |

关键事实：

- run_result_case.py 使用 result_generator.generate()，其行为是复制学生成果初稿并做样式标准化；
- result_generator 以初稿为 Word 基版，违反 result_generation_strategy.yaml 的 forbidden 项“以学生初稿作为 Word 基版”；
- result_reference_builder.py 已实现模板保真重构、TOC 域、参考文献样式迁移，但当前完整包脚本未调用；
- 陈家宝完整成果包实际由 run_v07_complete_package_chenjiabao.py 的 build_result() 完成“黄金模板前页 + 正文合并”，属于临时旁路，不是正式 Skill 入口。

## 二、使用到的脚本清单

| 脚本 | 职责 | 可复用 |
|---|---|---|
| v03/result_generator.py | 初稿标准化 | 作为内容预处理复用 |
| v03/result_reference_builder.py | 模板保真重构 | 正式生成入口，应接入 |
| v03/result_audit.py | 结构/格式/内容/固定页审核 | Quality Pipeline 可复用 |
| v03/result_revision.py | 章节分页 + TOC 更新 | Finalization 可复用 |
| v03/document_converter.py | DOCX→PDF | PDF 渲染复用 |
| v03/pdf_probe.py | 页数/尺寸/文本边界 | PDF 检查复用 |
| CourseAgent/modules/template_parser.py | 页面/表格/页眉页脚解析 | Template Understanding 复用 |
| CourseAgent/modules/format_checker.py | 表格签名/样式检查 | Format Sense 复用 |
| skills/graduation_design/result/content_check/validator.py | 区域化内容合规 | 内容层复用 |
| skills/graduation_design/result/content_check/validator.py | 学校/专家规则加载 | ARKM 数据基础 |

## 三、ExperienceLoader 可插入点

| 阶段 | 插入点 | 建议 |
|---|---|---|
| 生成前 | run_result_case.py 调用 generate 前 / complete_package 脚本 build_result 前 | 注入 ResultExperienceContext，只读，不改生成器 |
| 生成后 | result_audit 之后 / build_result 之后 | 注入 Reference/Document Quality Sense 检查结果 |
| 交付前 | PackageValidator 之前 | 把 result_experience_trace 纳入包级验收证据 |

原则：P3-A 只加旁路，不修改旧脚本。

## 四、可复用经验与模块

| 经验 | 文件 | 状态 |
|---|---|---|
| Result TKM | skills/graduation_design/result/rules/template_schema.json | available |
| Golden Case Experience | skills/graduation_design/result/memory/golden_cases/wanghuan.md | available |
| Reference Quality Sense | skills/graduation_design/result/memory/reference_quality_experience.json + docs/v0.7/ReferenceQualitySense/reference_quality_sense_schema.json | available |
| 成果规则集 | result/rules/typography.yaml、toc_rules.yaml、table_rules.yaml、content_rules.yaml、college_rules.yaml、audit_rules.json | available |
| Document Quality Sense | docs/v0.6/DocumentQualitySense/quality_sense_schema.json | available |
| Result Quality Memory | 未发现 result_quality_memory.json | missing |
| Academic Requirement Knowledge Model | 未发现 ARKM 文件 | missing |

## 五、审计结论

1. 经验文件真实存在，但当前三条成果生成路径均未加载；
2. 正式入口 result_reference_builder.py 被 Skill 文档声明，但未被实际调用；
3. P3-A 应新增旁路 Result Experience Consumer，不改旧脚本，先证明经验进入；
4. Result Quality Memory 与 ARKM 缺失必须如实标记 missing，不得伪加载；
5. P3-B 再接入 Quality Pipeline，P3-C 再正式接入 Reference Quality Sense。