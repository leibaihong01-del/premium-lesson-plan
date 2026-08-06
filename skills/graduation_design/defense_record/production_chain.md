# DefenseRecord 生产链路说明

版本：1.0
状态：候选，默认关闭?DEFENSE_LAYOUT_NORMALIZE=1 启用?
入口：DefenseSkillRunner

## 生产链路

1. 模板复制?保留模板页面、表格、字体、行距?
2. 字段替换?替换学生姓名、学号、课题、站点?
3. 模板骨架驱动规范化?以模板27段单元格为标准，学生内容映射到question_slot_1/2?answer_slot_1/2?conclusion_slot?student_info?固定区域来自模板?
4. 输出检查?'段结构、单页输出、字段完整、固定区域保持?

## 模板骨架

- 骨架模型：CourseAgent/experiments/defense_learning/analysis/defense_template_skeleton.json
- 段落数：27
- 映射规则：学生内容只进变量槽位，禁止扩写、禁止新增或删除模板段落?

## 开关与回退

- 启用：DEFENSE_LAYOUT_NORMALIZE=1
- 默认：关闭?异常时自动回退原流程?

## 回归证据

- 王欢模板骨架版：1 页?27 段?字段全部通过?
- 报告：defense_template_normalizer_report.md
