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

1. **模板解析**：读取目标材料对应模板的页面、字体、颜色、标题、表格、分页规则。
2. **内容映射**：建立课程标准 → 教学项目 → 教学任务 → 教学进度 → 教案的对应关系，检查缺失、重复与不一致。详见 [references/mapping-workflow.md](references/mapping-workflow.md)。
3. **教学重构**：按 90 分钟闭环与岗位能力重构教学过程，融入任务驱动、岗位情境、实践环节、过程评价与课程思政；禁止直接复制原教案。
4. **格式生成**：复制对应模板文件，run 级填充内容，执行颜色、字体、表格、行高与分页规则。
5. **质量审核**：执行修改回查、结构/颜色/思政/分页检查、Word 转 PDF、逐页 PNG 检查，输出审核报告与运行日志。详见 [references/quality-audit.md](references/quality-audit.md)。

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
- [references/mapping-workflow.md](references/mapping-workflow.md)：课标→项目→任务→进度→教案映射方法与检查项。
- [references/mapping-table-rules.md](references/mapping-table-rules.md)：批量生成映射表 .xlsx 的结构与检查逻辑。
- [references/quality-audit.md](references/quality-audit.md)：修改回查、格式/内容/思政/分页审核、PDF-PNG 视觉检查与运行日志。
- [references/iterations.md](references/iterations.md)：迭代学习日志，记录每次任务沉淀的规则。
