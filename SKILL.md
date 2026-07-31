---
name: premium-lesson-plan
description: Generate and audit high-quality vocational course materials (.docx), including curriculum standards, teaching progress plans, lesson-plan covers, lesson plans, and practice-session lesson plans, from retained Word templates, curriculum standards, progress plans, and original documents. Use when Codex needs to create, batch-generate, rebuild, or audit course documents for vocational courses, apply template-consistent formatting (fonts, colors, tables, pagination), map curriculum standards to progress plans and lessons, or distill course-material generation rules. Triggers include 课程标准、教学进度计划、教案封面、教案、实训教案、课程材料生成、教学重构、模板格式继承、批量生成、教案审核。
---

# 精品课程材料生成

按保留模板与规则库生成并审核高职精品课程材料：课程标准、教学进度计划、教案封面、课程教案、实训教案。

## 输入

- 课程标准（优化版或原始版）.docx
- 教学进度计划（优化版或原始版）.docx
- 原始教案 .docx（每课一份）
- 教案模板 .docx（39 行 × 6 列，教案格式基准）
- 课程标准模板、进度计划模板、封面模板（存在时使用）

## 可生成材料

| 材料 | 核心规则 |
|---|---|
| 课程标准 | [references/curriculum-standard-rules.md](references/curriculum-standard-rules.md) |
| 教学进度计划 | [references/progress-plan-rules.md](references/progress-plan-rules.md) |
| 教案封面 | [references/cover-rules.md](references/cover-rules.md) |
| 课程教案（16 课） | [references/lesson-plan-rules.md](references/lesson-plan-rules.md) |
| 实训教案（模块+考核） | [references/lesson-plan-rules.md](references/lesson-plan-rules.md) |

## 处理流程

0. **任务资源评估**：任务开始先输出【任务资源评估】（当前任务、已有知识、需要读取、预计新增计算、是否可复用、优化方案），按“已有知识 > 知识摘要 > 索引定位 > 原始文件”规划读取。详见 [references/green-ai-rules.md](references/green-ai-rules.md)。
1. **模板解析**：读取目标材料对应模板的页面、字体、颜色、标题、表格、分页规则。
2. **内容映射**：建立课程标准 → 教学项目 → 教学任务 → 教学进度 → 教案的对应关系，检查缺失、重复与不一致。详见 [references/mapping-workflow.md](references/mapping-workflow.md)。
3. **教学重构**：按 90 分钟闭环与岗位能力重构教学过程，融入任务驱动、岗位情境、实践环节、过程评价与课程思政；禁止直接复制原教案。
4. **格式生成**：复制对应模板文件，run 级填充内容，执行颜色、字体、表格、行高与分页规则。
5. **质量审核**：执行修改回查、内容/格式/身份/逻辑/视觉检查、Word 转 PDF、逐页 PNG 检查，输出审核报告与运行日志。身份审核检查课程名称、编码、专业、学时、章节等模板残留，防止跨课程信息污染。详见 [references/quality-audit.md](references/quality-audit.md) 与 [references/sample-file-rules.md](references/sample-file-rules.md)。

## 输出

- 精品课程材料 .docx（课程标准、进度计划、封面、教案、实训教案）
- 质量审核报告 .md
- 批量生成运行日志 .xlsx
- 规则库（references/ 目录）

## 关键规则

- 模板优先级最高：复制模板生成，禁止重建版式、禁止增删行列。
- 文字修改必须 run 级完成，禁止整段替换格式。
- 思政融入行红色、随堂练习蓝色、任务/知识点与阶段标签紫色、正文深灰。
- 90 分钟链：2+3+7+5+48+20+3+2；教学做一体任务合计 48 分钟。
- 每批生成后执行分页测量与空白尾页检查，单文件独立 Word 转换并记录日志。
- 样板文件具有模板基准、课程实例、质量验证三重属性：模板基准禁止修改，课程实例必须正确；生成后执行身份一致性检查，模板残留信息自动修正。

## 脚本工具

- [scripts/check_lesson_structure.py](scripts/check_lesson_structure.py)：校验教案 docx 的 39×6 结构、列宽、合并、90 分钟链、教学做一体 48 分钟、颜色、反思区与尾部段落。
  `python scripts/check_lesson_structure.py 教案.docx --template 模板.docx`
- [scripts/check_pdf_pagination.py](scripts/check_pdf_pagination.py)：检查 PDF 页数、空白尾页、越界与逐页底部空白。
  `python scripts/check_pdf_pagination.py 教案.pdf --max-mid-gap 40 --max-first-gap 110`
- [scripts/convert_one.ps1](scripts/convert_one.ps1)：单文件 Word 转 PDF，独立 Word 实例，失败不阻塞批次。
  `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/convert_one.ps1 -Src 教案.docx -Pdf 教案.pdf`

## 示例资产

`assets/templates/` 存放本课程四类保留模板（教案、课程标准、教学进度计划、教案封面），作为格式基准与示例：

- `assets/templates/lesson-plan-template.docx`
- `assets/templates/curriculum-standard-template.docx`
- `assets/templates/progress-plan-template.docx`
- `assets/templates/cover-template.docx`

其他课程应先解析并提供自己的模板，再按相同流程生成。

## 持续学习与迭代

- 任务开始前读取 [references/iterations.md](references/iterations.md) 中的最近规则，避免重复踩坑。
- 每次任务完成后，将新发现的问题、规则、修复方法与验证结果追加到 [references/iterations.md](references/iterations.md)，格式：日期 + 问题 + 规则/修复 + 验证结果。
- 批量任务前先按 [references/mapping-table-rules.md](references/mapping-table-rules.md) 生成映射表，检查缺失、重复与不一致。
- 规则或文档变更后运行 skill-creator 的 `quick_validate.py` 校验技能结构。
- 迭代循环：生成 → 审核 → 记录学习 → 更新规则库 → 复测。

## 参考文档

- [references/lesson-plan-rules.md](references/lesson-plan-rules.md)：教案页面、字体、颜色、标题、表格、思政、教学设计、分页规则库。
- [references/curriculum-standard-rules.md](references/curriculum-standard-rules.md)：课程标准结构、封面、表格与内容一致性规则。
- [references/progress-plan-rules.md](references/progress-plan-rules.md)：教学进度计划表头、表格与学时规则。
- [references/cover-rules.md](references/cover-rules.md)：教案封面与页眉页脚图片保留规则。
- [references/layout-rules.md](references/layout-rules.md)：课程文档通用排版优化规则（表格、页面、文字、视觉检查）。
- [references/experience-rules.md](references/experience-rules.md)：持续优化与经验迭代机制、版本管理与沉淀规则。
- [references/curriculum-standard-verification.md](references/curriculum-standard-verification.md)：课程建设智能诊断层规则（权威优先级、生成前/中/后校验、人机协同）。
- [references/professional-basic-course-rules.md](references/professional-basic-course-rules.md)：专业基础课程通用规则模板（课程定位、内容深度、项目、实训、思政、衔接）。
- [references/mapping-workflow.md](references/mapping-workflow.md)：课标→项目→任务→进度→教案映射方法与检查项。
- [references/mapping-table-rules.md](references/mapping-table-rules.md)：批量生成映射表 .xlsx 的结构与检查逻辑。
- [references/quality-audit.md](references/quality-audit.md)：修改回查、格式/内容/思政/分页审核、PDF-PNG 视觉检查与运行日志。
- [references/iterations.md](references/iterations.md)：迭代学习日志，记录每次任务沉淀的规则。
- [references/sample-file-rules.md](references/sample-file-rules.md)：样板文件生命周期、三重属性、修改权限分类与身份一致性检查。
- [references/agent-project-manager-mode.md](references/agent-project-manager-mode.md)：AI 项目经理模式、任务分层、知识库四层结构与智能审核闭环。
- [references/green-ai-rules.md](references/green-ai-rules.md)：绿色计算、分层读取、先索引后读取、任务资源评估与增量修改。
- [references/codex-running-protocol-v1.md](references/codex-running-protocol-v1.md)：Codex 运行协议 Step 0-3、主动纠错、持续上下文调用与人机协同。
