# GraduationDesign Skill

毕业设计文档专家能力包，按文档类型独立封装。

| 文档类型 | Skill | 状态 |
|---|---|---|
| 毕业设计任务书 | taskbook | v1.0 已建成 |
| 毕业设计成果 | result | v1.1 已升级（索引化） |
| 毕业设计成绩评定表 | evaluation_form | v1.0 已建成（默认关闭） |
| 毕业设计答辩记录表 | defense_record | v1.0 已建成（默认关闭） |

每个文档类型遵循同一套能力结构：模板解析 → 规则 → 生成 → 内部审核 → 交付 → 经验迭代。

## 标准机制

所有毕业设计类 Skill 默认采用双版本交付：AI生成版（原始样本）+ 人工修订版（学习样本），差异分析后升级规则。

## 新增能力

- EvaluationFormGenerationSkill：成绩评定表模板填充与质量检查，调用 Evaluation Form TKM 与 Quality Memory。
- DefenseRecordGenerationSkill：答辩记录表模板保持与区域填充，调用 Defense Record TKM 与 Quality Memory。
- Document Quality Sense 检查链路：Table Structure Sense / Region Integrity Sense / Character Style Sense / Template Consistency Sense。
- Output Naming Sense：检查文件名规范、学生姓名、题目、编号、目录结构与学生隔离，输出 output_validation_report.json；学生成果目录由 StudentProjectRegistry 管理，不写死专业方向。

新 Skill 默认关闭，不修改 V0.4/V0.6 旧生产链路，不自动固化经验。
