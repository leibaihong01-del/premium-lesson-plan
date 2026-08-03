# CourseAgent Skill资产登记报告

版本：1.0
日期：2026-08-03
检查方式：资产扫描 + Git 状态确认

## 一、当前 Skill 列表

| Skill | 状态 | 版本 | 位置 |
|---|---|---|---|
| premium-lesson-plan（精品课程材料生成） | Production | v1.0 | 插件：premium-lesson-plan；仓库登记：skills/premium_course_materials |
| task-book（毕业设计任务书） | Frozen | v1.0 | skills/graduation_design/task_book |
| document_management | 公共规则（非业务 Skill） | v1.0 | skills/document_management |
| vision_quality_check | Candidate | 未定版 | skills/vision_quality_check（未登记） |
| vision_understanding | Candidate | 未定版 | skills/vision_understanding（未登记） |
| agent_evolution | Candidate | 未定版 | skills/agent_evolution（未登记） |

## 二、毕业设计任务书状态

- 状态：Frozen（冻结基线）
- 版本：v1.0
- 标签：v1.0-taskbook-baseline
- 目录：skills/graduation_design/task_book/
- 内容：skill 定义、README、版本说明、工作流、模板规则、内容规则、命名规则、审核规则、脱敏验证摘要、manifest

## 三、Git 状态

- 分支：master
- 远程：未配置 remote
- 相关提交：
  - 4a86f1f feat: freeze graduation design task book skill v1.0 baseline
  - 625b402 docs: add architecture v1.1, skill registry and taskbook asset status report
- 本次操作：资产整理提交（待执行）

## 四、资产缺失清单（不虚构）

1. task_book 缺独立回归评估目录（evaluation/skills/task_book/），内部审核规则已有；
2. task_book 缺实际模板 docx（保留在工作区，未入库以避免体积与隐私风险）；
3. task_book 缺独立 prompts 目录（当前依赖工作区模块与经验库）；
4. vision_* 与 agent_evolution 未登记、未审查隐私，暂不纳入资产库；
5. graduation_design 遗留文件（reviewer.py、template_mapping.yaml 等）含潜在隐私，未登记，需清理后再评估。

## 五、GitHub 同步

- 当前未配置 remote，未推送；
- 待提供远程地址后执行 push 并核验。
