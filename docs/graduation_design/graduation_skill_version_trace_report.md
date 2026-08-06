# 四产物 Skill 最终版本溯源检查报告

时间：2026-08-06
性质：只读溯源，不修改代码 / Skill / 成果

## 一、版本溯源表

| Skill | Runner 入口 | 实际调用文件 | 实际模板 | 实际规则 | 当前版本 | 人工最终确认版本 | 是否一致 |
|---|---|---|---|---|---|---|---|
| task_book | TaskBookSkillRunner | core/graduation_skill_runners.py | 01 杨振海毕业设计任务书 | 字段替换 + 内容迁移 + 页面语义检查 | version.json 1.0 / SKILL v1.1 | v1.1（唯一生产路径 = taskbook_generator / v03/run_taskbook_case.py） | 不一致 |
| evaluation | EvaluationSkillRunner | core/graduation_skill_runners.py | 04 杨振海成绩评定表 | 字段替换 + 模板保护 | v1.0 | v1.0 | 一致 |
| defense_record | DefenseSkillRunner + DEFENSE_LAYOUT_NORMALIZE=1 | core/graduation_skill_runners.py + core/defense_template_normalizer.py | 05 杨振海答辩记录表 | 骨架驱动规范化 + DNA v0.2 | v0.9-candidate-production | v0.9-candidate-production | 一致 |
| result | v0.2 TemplateInstanceBuilder 生产路径 | 黄金模板 → 模板实例化 → 字段替换 → 内容迁移 → Visual Baseline（未用旧 ResultSkillRunner） | 02 杨振海毕业设计成果 | template_style_precedence / template_dna / visual_dna / subject_consistency | v1.2（生产模式）/ v0.2 生产路径 | v0.2 生产路径 | 一致 |

## 二、重点确认：Result

- SKILL.md 已写入 `TemplateInstanceBuilder Production Path`；
- 实际调用链与 v0.2 生产路径一致；
- 未使用旧 ResultSkillRunner 默认路径；
- 规则文件均已加载。

结论：Result 溯源通过。

## 三、差异说明

task_book 存在版本不一致：

1. SKILL.md v1.1 声明唯一生产路径为 `taskbook_generator（v03/run_taskbook_case.py）`；
2. 本次端到端实际调用的是 `TaskBookSkillRunner`（V0.7 Runner）；
3. version.json 仍为 1.0，未同步到 1.1。

模板与内容规则一致，但入口与确认版本不同。

## 四、结论

- evaluation：一致；
- defense_record：一致；
- result：一致（TemplateInstanceBuilder Production Path 确认）；
- task_book：入口不一致，需后续对齐或更新 SKILL 记录。

待 task_book 版本对齐后，再重新执行邱志豪端到端生产验证。
