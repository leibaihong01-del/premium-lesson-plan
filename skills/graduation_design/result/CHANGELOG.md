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

## 2026-08-06 生产模式接入（候选）

### Added

- 默认生产流程正式接入 Result Skill?StudentProfile ? DocumentPackage ? TemplateInstanceBuilder ? ContentAdapter ? Visual Baseline检查 ? DOCX/PDF）?
- 样式优先级：黄金模板样式 > Result规则 > 来源内容格式?
- Structural Compliance + Visual Compliance 验收要求?

依据： Result 黄金模板迁移验证 v0.2（A级视觉基准）?

## 2026-08-06 模板实例化生产路径固化

### Added

- TemplateInstanceBuilder 唯一生产路径?
- 已通过多学生实例化验证（王欢、汪子涵）?
- 内容迁移主体一致性检查规则?

## 2026-08-06 缺陷分析与规则补充（v1.3-preparation）

### Added

- 内容迁移边界规则?
- Heading检查粒度（styles/numbering）?
- DocumentFinalizer设计（vE0.1）?
- 参考文献结构检查?
- 三项DNA回归验证规则?
- 版本追踪与生产闭环规则?

## 2026-08-06 唯一成果输出方式固化（v1.3）

### Added

- result_production_strategy_v1.3.md，作为唯一成果输出方式?
- DocumentFinalizer（verified）?
- 三项DNA回归验证与v0.2对比?

## 2026-08-06 v1.5 模板对齐与内容规则沉淀

### Added

- 封面固定区域保护：正文格式规则不得覆盖封面标题字号
- 两字一级标题两字中间空两格（引  言、总  结）
- 正文表格对齐模板：Normal Table(18) + 4998pct + 表格内容(33) + 宋体/TNR 五号 + 水平垂直居中
- 表注编号表X.Y，样式表注，宋体/TNR 五号，keepNext
- 专科毕业设计学术词黑名单：本文/本研究/本课题/本论文/实验结果表明/研究对象/笔者/该研究/课题研究
- 虚构线路名清洗：真实城市地铁/线路名 → 某轨道交通线路/某地铁某线路，封面校名保留

### Changed

- result_content_quality_rules.md 增加专科毕业设计表达规范
- result_content_subject_consistency_rules.md 增加虚构线路名清洗示例
- result_quality_memory.json 沉淀 v1.5 规则经验

### 依据

- 王欢 v1.5 模板对比人工反馈：封面被改、两字标题间距丢失、表格/表注偏离模板、正文出现真实地铁名
## 2026-08-06 v1.5 中文标点字体与正文全角经验

### Added

- 中文标点必须宋体渲染：中文 Run 的 ascii/hAnsi/eastAsia 均设宋体，并加 w:hint="eastAsia"；
- 验证方式升级：必须用渲染后 PDF 提取引号字符实际字体（SimSun），不能只看 rPr 属性；
- 正文标点全角化，参考文献保持半角；
- 标题纯样式继承，目录更新不再被直接字体污染；
- 质量引擎 run_fonts 允许宋体/微软雅黑。

### 依据

- 王欢 v1.5 第五章引号实测仍为 Times New Roman；修复后 PDF 实测为 SimSun。
## 2026-08-06 v1.5 冻结为唯一输出方式

### 冻结

- 毕业设计成果唯一输出方式：result_production_strategy_v1.5.md；
- 唯一生产入口：tools/result_v1.4_pipeline.py（v1.5 规则版）；
- v1.5 FREEZE_NOTE 状态：已确认，正式冻结。

### 保留

- v1.4、v0.2、黄金模板均不覆盖。