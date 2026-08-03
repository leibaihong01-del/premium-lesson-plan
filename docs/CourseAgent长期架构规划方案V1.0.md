# CourseAgent 长期架构规划方案 V1.0

版本：V1.0
日期：2026-08-03
状态：架构认知统一稿（不涉及代码改动）

## 0. 第一性原理审查

先回答三个根本问题：

1. CourseAgent 的长期目标是什么？
   把“大模型能力”沉淀为“可复用、可验证、可演进的工程能力”，最终以低成本高质量完成职业教育教学与毕业设计文档生产。

2. 当前最缺的是什么？
   不是更多模块，而是“能力如何沉淀”的底层规则：什么进 Skill、什么进 Capability、什么进 Experience，以及它们如何被调用和验证。

3. 现有设想的逻辑问题是什么？
   - Agent / Workflow / Skill / Capability / Experience 五层概念存在重叠，容易形成“目录树架构”而不是能力架构。
   - Skill 与 Capability 边界不清：如果把字体、表格、Word 生成都做成 Skill，会出现 Skill 数量膨胀与重复代码。
   - Experience 与 Memory 边界不清：经验若只是“记录”，不会自动变成生成能力。
   - 一次性脚本散落在工作区，与 Skill 规则分离，不利于版本管理与回归。
   - 为未来需求提前建设模块（联网检索、PPT 解析等）属于过度设计。

结论：不推翻现有系统，采用“三层引擎 + 标准 Skill 插件”收敛。

## 1. 当前架构评价

已完成且应保留：

- 任务书完整闭环：模板解析 → 生成 → 人工修改 → 差异分析 → 经验提炼 → 规则升级 → 再次生成验证。
- 任务书 Skill v1.0 已冻结并打标签：v1.0-taskbook-baseline。
- 已有 Router、Workflow、Capability、Evaluation、Memory、Providers 等基础骨架。
- 内部审核、命名继承、虚拟对象中和、只交付 Word 等规则已沉淀。

需要收敛的问题：

- skills/ 与 capabilities/ 职责不清；
- 经验分散在 memory/system、工作区经验库、Skill rules 多处；
- 毕业设计检测代码（v03）在工作区而非 CourseAgent 仓，Skill 与执行代码分离；
- 评估体系目前偏翻译任务，毕业设计链路缺少统一回归入口。

## 2. 长期架构设计

推荐三层模型，而不是五层：

```text
认知层 Understanding（LLM 学习）
  - 新任务理解、新模板分析、复杂推理
  - 人工修改差异分析、经验提炼
  - 高成本、低频、只在能力未固化时使用

执行层 Execution（Skill + Capability 生产）
  - Skill：业务专家包，组合规则 + Capability + 流程
  - Capability：公共原子能力，确定性优先
  - 低成本、高频、批量生产

进化层 Evolution（Experience）
  - 问题 → 原因 → 通用性判断 → 规则提炼 → 验证 → 版本升级
  - 经验是经过验证的规则版本，不是记录
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

目标目录形态（渐进调整，不立即重构）：

```text
CourseAgent/
  agents/        薄决策层
  skills/        业务专家包（taskbook v1.0 为范式）
  capabilities/  公共原子能力
  experience/    版本化经验库
  core/          工作流/技能运行/审核引擎
  evaluation/    回归评估
  providers/     模型与外部工具接入
```

## 3. Skill 边界原则

创建 Skill 的条件：

- 同一业务场景重复出现（如多份任务书）；
- 模板与规则可固化；
- 有验收标准（人工验收或自动检查）；
- 至少完成一次“AI → 人工 → 差异 → 沉淀”闭环。

不创建 Skill：

- 字体规则、表格处理、Word 生成、页面检查 → 公共 Capability；
- 单次任务、临时脚本；
- 未经验证的经验；
- 仅为未来需求预留的空 Skill。

TaskBookSkill 为什么成立：固定模板、明确字段、批量复用、已有完整闭环与基线标签。

防膨胀原则：Skill 应“薄”，规则外置，公共逻辑下沉 Capability，一个 Skill 对应一个业务对象。

## 4. Capability 设计原则

- 原子、无业务假设、可复用、确定性优先；
- 文档工程能力：
  - template_parser
  - docx_generator
  - format_checker
  - consistency_checker
  - naming_check
  - render_check（PDF 仅内部验证）
- 知识获取能力（公共层，非业务 Skill）：
  - textbook_parser
  - ppt_parser
  - web_research
  - knowledge_builder
- 禁止在 Skill 内复制 Capability 逻辑；
- 未产生真实需求前不建设，例如 web_research 仅在需要联网检索时实现。

## 5. Experience 进化机制

五步管线：

```text
发现问题 → 原因分析 → 通用性判断 → 规则提炼 → 版本升级
```

- 单案例特殊修改不沉淀；
- 模板规律、专业规律、生成规律才进入正式经验库；
- 候选规则先进入临时观察区，经下一次生成或历史案例验证后转正；
- 版本迭代：最新有效版本作为生成默认依据，旧版本保留用于追踪演化；
- 示例：虚拟地点不得作为真实资料收集来源，已从“无约束”升级为 v1.0 正式规则并验证生效。

落地要求：

- experience/ 下分 rules/、cases/、versions/；
- 每个 Skill 启动时读取最新有效版本索引；
- 新增经验导致质量下降时自动降权或回退。

## 6. 知识获取体系

三层知识来源：

1. 教师主动提供（权威）：优秀案例、教材、PPT、学校文件、标准规范；
2. 联网检索（背景）：行业资料、技术标准、背景知识；
3. 历史生成经验（专家规则）：修改经验、质量标准、通用规则。

融合原则：

- 权威优先，教师与学校文件高于检索结果；
- 检索内容需标注来源并经过确认；
- 经验只作为生成规则，不替代权威要求；
- 三层统一进入“模板规则 + 内容规则 + 专业规则 + 审核规则”四类知识槽位。

## 7. 未来演进路线

阶段1（已完成）：任务书 Skill v1.0 冻结，标签 v1.0-taskbook-baseline。

阶段2：成果 Skill。按同一范式先完成“成果 AI 生成 → 人工批阅 → 差异分析 → 规则沉淀”。

阶段3：毕业设计完整能力体系：TaskBook、Achievement、Defense、Evaluation、GuidanceRecord 五个 Skill，并实现全流程编排。

阶段4：课程建设领域扩展：课程标准、教学进度计划、教案、PPT、题库，复用同一 Skill 范式与 document_engineering 能力。

阶段5：职业教育领域专家 Agent：核心引擎不变，业务能力以 Skill 插件方式扩展。

全流程一键生成可行，但前提是逐步积累：模板库、学生数据、规则库、人工验收样本；实现路径是“先逐个 Skill，再编排 Workflow”。

## 8. 明确不做的

- 不提前建设未验证的模块；
- 不为未来需求创建空 Skill；
- 不把评估报告当交付物；
- 不把学习阶段的人工流程复制到生产阶段；
- 不因架构讨论停止当前已冻结能力的维护。

## 9. 结论

CourseAgent 的“操作系统”应收敛为：

```text
薄 Agent + 标准 Skill 插件 + 公共 Capability + 版本化 Experience + 两级审核
```

任务书 Skill v1.0 是第一个“专家插件”范式，后续成果、答辩、成绩表、课程标准、教案均按此范式生长。
