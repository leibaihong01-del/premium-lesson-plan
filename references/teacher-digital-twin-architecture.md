# 优秀高职教师数字孪生智能体架构

## 一、总体架构

Teacher Core Brain（总控）→ Skill Manager → 教学/科研/竞赛/成果/文件/知识/分析 Skills → Memory → Knowledge → Self-Evolution。

## 二、Agent模块划分

需求转译、满意度预测、Problem Solver、质量检测、技能管理、自我进化、用户模型、知识更新；各能力模块以六件套Skill化（执行器/评价器/反思器/优化器/经验库/进化器）。

## 三、设计文档

`课程材料优化/CourseAgent/docs/`：00_Master需求文档、05_教师大脑架构设计V1.0（架构图、模块划分、Skill体系、数据结构、路线图）。

## 四、实现状态

Skill六件套抽象已落地（core/skill.py 注册表 + tools/skill_demo.py）：竞赛/分析/教案Skill 已注册并冒烟通过，评价器可自动发现结构缺口并触发进化记录。

skill_factory 默认注册7个能力单元（教学资源/文件/分析/竞赛/科研/成果/知识），skill_audit 审计通过；Skill注册表为应用内能力清单，与Windows注册表无关。
