# 规则来源结构审计报告

日期：2026-08-03
状态：只读审计 + 教师经验规则补充（研究/研究对象）

## 一、当前规则来源结构

graduation_design/
├── school_rules/      学校硬约束（08 检查标准等）
├── expert_rules/      教师经验增强（研究/研究对象等）
└── result/
    ├── content_check/ 执行层（区域识别 + 三级判断）
    ├── rules/         模板经验与生成规则
    └── review/        纠偏规则与验证方案

## 二、原有毕业设计经验规则保留情况

- task_book 经验：保留（工作区经验库 + skill）
- 成果教师经验：保留（result/rules/teacher_correction_rules.md、review/result_skill_correction_rules.json）
- 虚拟对象规则：保留（result/rules/content_rules.json、工作区 virtual_object_rules.json）
- 学校候选规则：保留（school_rules/content_rules.json，未转正式）
- 已删除项：content_check/forbidden_expression_rules.json（独立词库，内容已并入 school_rules/expert_rules，非丢失）

## 三、三者关系

- 学校规则：硬约束，是判断依据
- 教师经验：经验增强，补充学校未细化的表达（研究/研究对象）
- 模板规则：格式约束（结构、样式、表格、命名）
- 三者不能互相替代；检测器合并 school_rules + expert_rules 执行

## 四、风险结论

- 未发现规则覆盖、删除、回退；
- 已新增教师经验规则：正文禁止“研究对象”，建议“设计对象”；“研究”字眼作为 warning 按语境判断；
- 承诺页“研究成果”等固定文字由区域规则排除，不误报。
