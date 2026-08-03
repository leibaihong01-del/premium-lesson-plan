# CourseAgent 长期架构规划方案 V1.1

版本：V1.1
日期：2026-08-03
状态：架构认知统一稿（不涉及代码改动）
变更：V1.0 已废弃，V1.1 修正 Skill 起点与演进顺序。

## 0. 第一性原理审查

三个根本问题：

1. CourseAgent 的长期目标是什么？
   把“大模型能力”沉淀为“可复用、可验证、可演进的工程能力”，以低成本高质量完成职业教育教学与毕业设计文档生产。

2. 当前最缺的是什么？
   不是更多模块，而是“能力如何沉淀”的底层规则：什么进 Skill、什么进 Capability、什么进 Experience，以及如何被调用和验证。

3. 现有设想的逻辑问题是什么？
   - 五层概念（Agent/Workflow/Skill/Capability/Experience）存在重叠，容易形成目录树架构；
   - Skill 与 Capability 边界不清会导致 Skill 膨胀与代码重复；
   - Experience 若只是“记录”不会变成生成能力；
   - 一次性脚本散落，Skill 与执行代码分离；
   - 为未来需求提前建设模块属于过度设计。

结论：不推翻现有系统，采用“三层引擎 + 标准 Skill 插件”收敛。

## 1. 当前架构评价

已完成且应保留：

- 精品课程材料生成已形成成熟业务 Skill（premium-lesson-plan），覆盖课程标准、教学进度计划、教案封面、课程教案、实训教案。
- 毕业设计任务书完整闭环：模板解析 → 生成 → 人工修改 → 差异分析 → 经验提炼 → 规则升级 → 再次生成验证。
- 任务书 Skill v1.0 已冻结并打标签：v1.0-taskbook-baseline。
- 已有 Router、Workflow、Capability、Evaluation、Memory、Providers 等基础骨架。
- 内部审核、命名继承、虚拟对象中和、只交付 Word 等规则已沉淀。

需要收敛的问题：

- skills/ 与 capabilities/ 职责不清；
- 经验分散在 memory/system、工作区经验库、Skill rules 多处；
- 毕业设计检测代码在工作区而非 CourseAgent 仓；
- 评估体系偏翻译任务，毕业设计链路缺少统一回归入口；
- Skill Registry 尚未建立，Skill 资产缺少统一登记入口。

## 2. 长期架构设计

三层模型：

```text
认知层 Understanding（LLM 学习）
执行层 Execution（Skill + Capability 生产）
进化层 Evolution（Experience）
```

调用关系：

```text
需求 → Router（选 Skill）
     → Skill 编排 Capability + 规则
     → 内部审核（内容/结构/格式/命名/内容逻辑）
     → 自动修正（最多 N 轮）
     → 交付 DOCX
     → 人工反馈 → Experience 提炼 → 版本升级
```

目标目录形态（渐进调整）：

```text
CourseAgent/
  agents/        薄决策层
  skills/        业务专家包 + registry.yaml
  capabilities/  公共原子能力
  experience/    版本化经验库
  core/          工作流/技能运行/审核引擎
  evaluation/    回归评估
  providers/     模型与外部工具接入
```

## 3. Skill 边界原则

创建 Skill 的条件：

- 同一业务场景重复出现；
- 模板与规则可固化；
- 有验收标准；
- 至少完成一次“AI → 人工 → 差异 → 沉淀”闭环。

不创建 Skill：

- 字体规则、表格处理、Word 生成、页面检查 → 公共 Capability；
- 单次任务、临时脚本；
- 未经验证的经验；
- 仅为未来需求预留的空 Skill。

防膨胀原则：Skill 应“薄”，规则外置，公共逻辑下沉 Capability，一个 Skill 对应一个业务对象。

## 4. Capability 设计原则

- 原子、无业务假设、可复用、确定性优先；
- 文档工程能力：template_parser、docx_generator、format_checker、consistency_checker、naming_check、render_check；
- 知识获取能力（公共层，非业务 Skill）：textbook_parser、ppt_parser、web_research、knowledge_builder；
- 禁止在 Skill 内复制 Capability 逻辑；
- 未产生真实需求前不建设。

## 5. Experience 进化机制

五步管线：发现问题 → 原因分析 → 通用性判断 → 规则提炼 → 版本升级。

- 单案例特殊修改不沉淀；
- 模板规律、专业规律、生成规律进入正式经验库；
- 候选规则先入临时观察区，验证后转正；
- 最新有效版本作为生成默认依据，旧版本保留追踪演化；
- 示例：虚拟地点不得作为真实资料收集来源，已升级为 v1.0 正式规则并验证生效。

## 6. 知识获取体系

三层知识来源：教师主动提供（权威）、联网检索（背景）、历史生成经验（专家规则）。

融合原则：权威优先；检索内容标注来源并确认；经验作为生成规则，不替代权威。

## 7. 领域 Skill 能力资产现状

### 已有业务 Skill

#### 1. PremiumLessonPlanSkill

- 状态：已实现（production）
- 定位：CourseAgent 第一个业务 Skill
- 作用：验证模板驱动生成、专业规则调用、经验沉淀、质量检查闭环
- 资产位置：Codex 插件 `premium-lesson-plan`（`D:/AI/Codex/UserData/codex-home/skills/premium-lesson-plan`）
- 仓库登记：`skills/registry.yaml`

#### 2. TaskBookSkill

- 状态：冻结基线（frozen）
- 定位：毕业设计领域第一个标准 Skill
- 作用：验证同一 Skill 方法论能否跨业务领域迁移
- 资产位置：`skills/graduation_design/task_book`
- Git 标签：v1.0-taskbook-baseline
- 仓库登记：`skills/registry.yaml`

### 后续规划

毕业设计领域：TaskBookSkill → AchievementSkill → ProposalSkill → DefenseSkill → EvaluationSkill → GuidanceRecordSkill

精品课程领域：PremiumLessonPlanSkill → CourseStandardSkill → TeachingPlanSkill → PPTDesignSkill → QuestionBankSkill

## 8. 未来演进路线

阶段0（已完成）：精品课程材料生成 Skill（premium-lesson-plan）作为 CourseAgent 第一个业务 Skill 投入生产。

阶段1（已完成）：毕业设计任务书 Skill v1.0 冻结（v1.0-taskbook-baseline），验证跨领域范式复用。

阶段2：成果 Skill。按同一范式完成“AI 生成 → 人工批阅 → 差异分析 → 规则沉淀”。

阶段3：毕业设计完整能力体系与全流程编排。

阶段4：精品课程领域扩展。

阶段5：职业教育领域专家 Agent：核心引擎不变，业务能力以 Skill 插件方式扩展。

## 9. 明确不做的

- 不提前建设未验证的模块；
- 不为未来需求创建空 Skill；
- 不把评估报告当交付物；
- 不把学习阶段的人工流程复制到生产阶段。

## 10. 结论

CourseAgent 的核心不是“有什么模块”，而是“培养了多少专家 Skill”。

```text
                CourseAgent
                    |
        -------------------------
        |                       |
   精品课程专家             毕业设计专家
 premium-lesson-plan      task-book
        |                       |
        -------------------------
                    |
             公共Capability
                    |
             Experience进化
```

架构收敛为：薄 Agent + 标准 Skill 插件 + 公共 Capability + 版本化 Experience + 两级审核。
