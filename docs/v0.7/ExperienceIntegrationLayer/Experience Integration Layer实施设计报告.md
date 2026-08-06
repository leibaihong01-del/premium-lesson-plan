# CourseAgent V0.7 Experience Integration Layer 实施设计报告

版本：0.7-eil-design-v1
状态：设计稿（未编码）
目标：解决 `knowledge_isolated=true`，让已固化经验真实进入生成链路
原则：不破坏 V0.3/V0.4/V0.6；新能力默认关闭；先设计审计再编码；经验调用必须有真实证据

## 一、背景与问题

毕业设计完整成果包验证已覆盖：任务书、成果、成绩评定表、答辩记录表。

链路审计结论：

- 经验已经固化；
- 但生产链路没有真实加载；
- 状态：`knowledge_isolated=true`；
- 存在“报告声明使用经验，但代码未加载”的伪调用。

## 二、核心目标

从“案例学习 → 经验保存”升级为：

```text
经验保存
 ↓
经验检索
 ↓
生成调用
 ↓
质量检查
 ↓
问题修正
 ↓
经验反馈
```

形成真实闭环。

## 三、必须遵守原则

1. 不允许伪调用：所有经验调用必须写入 `experience_trace.json`，记录经验、来源文件、作用阶段、影响结果。
2. 不修改旧生产链路：V0.3 生成器、V0.4 链路、V0.6 验证能力保持不变；新增 V0.7 Experience Integration Layer，默认关闭。
3. 经验不是规则硬编码：保存问题类型、判断依据、适用范围、解决策略、验证结果；不保存固定数值。
4. 经验调用可控：`experience_integration_enabled=false` 时系统恢复旧流程。
5. 先分析再编码：本报告为设计稿，等待人工确认后进入编码。

## 四、总体架构

```text
Student Profile（唯一数据源）
        ↓
Document Package Manager
        ↓
task_context / document_type / template
        ↓
ExperienceLoader
        ↓
Applicable Experience Set
        ↓
Skill Runner（按文档类型）
  ├── Template Understanding
  ├── Experience Loading
  ├── Generation（复用旧生成器，不修改）
  ├── Quality Sense
  ├── Revision Planner
  └── Validation
        ↓
单文件 Trace
        ↓
Document Package Quality Sense（跨文档一致性与交付验收）
        ↓
Experience Usage Audit
```## 五、经验加载矩阵

| 文档类型 | 必须加载的经验 | 来源 |
|---|---|---|
| 任务书 | TaskBook TKM、Page Semantic Layout Experience、Document Quality Sense | v06 data、经验固化报告 |
| 成果 | Result TKM、Result Quality Memory、Reference Quality Sense、Golden Case Experience、Document Quality Sense | result/rules、result/memory |
| 成绩评定表 | Evaluation Form TKM、Evaluation Quality Memory | evaluation_form Skill |
| 答辩记录表 | Defense Record TKM、Defense Quality Memory | defense_record Skill |

## 六、真实运行追踪

每次生成必须输出：

- `experience_trace.json`：本次调用了哪些经验、来源文件、作用阶段、影响结果；
- `generation_trace.json`：文档类型、Skill、模板来源、经验加载、质量检查、修正动作、最终验证；
- `experience_usage_report.md`：经验是否存在、是否加载、是否使用、是否影响结果。
- document_package_validation_report.json：包级一致性、模板符合性、交付完整性。

经验真实性审计规则：

- 生成报告中的经验声明必须能在 `experience_trace.json` 找到对应记录；
- `experience_loaded` 为空或与声明不一致时，审计判为 fail；
- 审计 fail 的成果不得进入交付目录。

## 七、Result Agent 专项

成果不能按任务书逻辑处理，单独建立 Result Agent：

### 内容层
- 章节逻辑
- 专业内容
- 技术路线
- 任务匹配

### 格式层
- 标题
- 目录
- 页码
- 图表
- 分页

### 引用层（Reference Quality Sense）
- 文献数量
- 格式
- 隐藏字符
- 网页污染
- 悬挂缩进
- 首行/续行对齐

## 八、实施阶段

| 阶段 | 内容 | 验收 |
|---|---|---|
| P1 | ExperienceLoader + 经验注册表 + 双 Trace | 任何生成任务可输出真实 experience_trace.json |
| P2 | 毕业设计成果接入（Result Agent） | 五项经验全部真实加载并影响生成/检查 |
| P3 | 任务书接入 | 页面语义布局经验进入生成 |
| P4 | 成绩评定表 + 答辩记录表合并为 Graduation Administrative Document Skill | 模板驱动型文档统一走同一 Runner |

## 九、迁移与回退

- 新增配置开关：`experience_integration_enabled`，默认 false；
- 旧入口脚本不改动；V0.7 Runner 作为新入口，默认不接管；
- 关闭开关后，生成路径完全回退到旧流程；
- 每个阶段先以验证案例运行，通过后保留开关关闭状态等待人工启用。

## 十、风险分析

| 风险 | 影响 | 对策 |
|---|---|---|
| 伪调用 | 审计失效 | experience_trace 由代码自动写入，审计门禁校验 |
| 单案例经验过拟合 | 迁移失败 | 经验进入注册表前必须多案例验证 |
| 旧生成器输出与经验冲突 | 误改正文 | Quality Sense 只报告偏差，Revision 只做最小局部修正 |
| Word 目录/页码不稳定 | 渲染失败 | 独立 finalization 步骤，失败降级为人工会审项 |
| 开关误开 | 生产变化 | 默认 false，版本登记 + 回归测试 |

## 十一、验收标准

1. 经验真实调用：代码加载，不是报告声明。
2. 生成稳定：同一输入两次生成差异可控。
3. 可追溯：任何结果能回答“为什么这样生成、用了什么经验”。
4. 可回退：关闭 `experience_integration_enabled` 恢复旧流程。
5. 无破坏：V0.3/V0.4/V0.6 脚本未被修改。

## 十二、禁止事项

- 禁止大规模重构；
- 禁止删除旧生成器；
- 禁止直接修改 V0.3 生产逻辑；
- 禁止未验证直接固化经验；
- 禁止继续无限增加案例训练。

## 十三、毕业设计文档包一致性与交付验收机制

### 13.1 Student Profile 主数据层

生成前建立唯一学生主数据：

```json
{
  "student_name": "邱志豪",
  "student_id": "202421044713",
  "major": "城市轨道交通机电技术",
  "class": "24级机电技术2班",
  "advisor": "瞿曌",
  "topic": "太平街口站电梯常见故障分析与检修方案设计"
}
```

规则：

- Student Profile 是唯一数据源；
- 任务书、成果、成绩评定表、答辩记录表全部从同一对象读取身份字段；
- 禁止每个文档自行生成姓名、学号、课题。

### 13.2 Document Package Manager

- 管理一个学生的一整套毕业设计材料；
- 负责目录、编号、命名、版本与交付组织；
- 每个 Skill 只负责单文档，包级由 Manager 统一调度。

### 13.3 Document Consistency Sense

跨文档检查：

| 字段 | 任务书 | 成果 | 成绩评定表 | 答辩记录表 |
|---|---|---|---|---|
| 姓名 | 一致 | 一致 | 一致 | 一致 |
| 学号 | 一致 | 一致 | 一致 | 一致 |
| 专业 | 一致 | 一致 | 一致 | 一致 |
| 班级 | 一致 | 一致 | 一致 | 一致 |
| 指导教师 | 一致 | 一致 | 一致 | 一致 |
| 课题名称 | 一致 | 一致 | 一致 | 一致 |

任何一项不一致，包级状态判为 fail。

### 13.4 Template Compliance Sense

检查生成文件是否来自正确模板：

- 任务书：18×14 表格、页数、字体、签字区域；
- 成果：学校论文模板、固定页、参考文献区域；
- 成绩评定表：16×13 表格、签字区域；
- 答辩记录表：固定区域、单表结构。

同时登记模板版本与来源，禁止混用模板版本。

### 13.5 Diff Engine

模板原文件与生成文件逐项对比：

- 结构：表格数量、行列、合并单元格；
- 样式：字体、字号、加粗、对齐、行距；
- 页面：页数、区域位置、签字区域。

输出：Template Difference Report。

### 13.6 Package Validator

生成完整学生文件夹后执行：

- 文件是否齐全；
- 命名是否正确；
- 人员是否一致；
- 主题是否一致；
- 模板是否一致；
- PDF 是否正常打开。

输出：document_package_validation_report.json。

### 13.7 Document Package Quality Sense

- 统一验收：单文件 Sense + 跨文件一致性 + 模板符合性 + 交付完整性；
- 只有包级验收通过，整套材料才可进入交付；
- 该能力解决“单文件都通过、但整套学生档案不可用”的问题。

## 十四、本阶段输出

本报告为设计稿；等待人工确认后进入 P1 编码。