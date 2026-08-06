# 邱志豪四产物最终版本调用链验证报告

时间：2026-08-06
性质：最终确认版本生产调用验证

## 一、实际调用链

| 产物 | Skill | 版本 | 调用入口 | 模板 | 规则 |
|---|---|---|---|---|---|
| 01 任务书 | task_book | v1.1 | TaskBookSkillRunner | 01 杨振海毕业设计任务书 | 字段替换 + 内容迁移 + 页面语义检查 |
| 02 成果 | result | v0.2 生产路径 | 黄金模板 → TemplateInstanceBuilder → 字段替换 → 内容迁移 → Visual Baseline | 02 杨振海毕业设计成果 | template_style_precedence / template_dna / visual_dna / subject_consistency |
| 03 成绩评定表 | evaluation | v1.0 | EvaluationSkillRunner | 04 杨振海成绩评定表 | 字段替换 + 模板保护 |
| 04 答辩记录表 | defense_record | v0.9-candidate-production | DefenseSkillRunner + DEFENSE_LAYOUT_NORMALIZE=1 | 05 杨振海答辩记录表 | 骨架驱动规范化 + DNA v0.2 |

## 二、生成结果

| 产物 | DOCX | PDF | 页数 |
|---|---|---|---|
| 01 | 是 | 是 | 3 |
| 02 | 是 | 是 | 16 |
| 03 | 是 | 是 | 1 |
| 04 | 是 | 是 | 1 |

## 三、与已验证版本差异说明

- task_book：使用 V0.7 TaskBookSkillRunner（已验证 v1.1），与历史 v03 入口不同，但模板与规则一致；
- evaluation：使用已验证 v1.0 入口，无差异；
- defense_record：使用 v0.9-candidate-production 路径，无差异；
- result：严格使用 v0.2 TemplateInstanceBuilder 生产路径，未使用旧 ResultSkillRunner 默认路径；已应用模板样式优先级与 Visual DNA 规则。

## 四、结论

最终确认版本 Skill 可被生产链正确调用，四产物完整生成。
