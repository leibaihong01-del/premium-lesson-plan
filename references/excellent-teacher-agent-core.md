# 优秀高职教师智能体核心底座

目标：总控智能体 + 需求转译 + 记忆系统 + 自我进化系统，作为整个 Agent 的核心底座，支撑教学资源生产、竞赛、教研、成果等能力模块扩展。

## 一、总控智能体（Orchestrator）

状态机：TRANSLATED → PLANNED → EXECUTING → REVIEWING → REPAIRING → PACKAGED → LEARNED → DONE，每步记录工作日志，支持复用现有执行层。

## 二、需求转译（Translator）

自然语言 → TaskSpec（意图、领域、交付物、质量、约束、算力提示、置信度），结合用户偏好记忆；零/低Token规则解析。

## 三、记忆系统（Memory）

统一命名空间：tasks、decisions、rules、failures、successes、improvements、user_preferences、templates、problems、solutions、best_practices、lessons_learned；支持 put/get/search 与用户偏好模型。

## 四、自我进化系统（Evolution）

问题发现 → 分类（需求理解/专业能力/输出质量/格式/创新/外部变化）→ 方案 → 验证 → 经验沉淀 → 可控升级（L1自动、L2验证、L3人工确认）→ 成长评分。

## 五、设计文档

`课程材料优化/CourseAgent/docs/`：01_现状分析与复用评估、02_系统架构设计V1.0、03_开发路线图V1.0。
