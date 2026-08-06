# CourseAgent V0.7 多文档经验成长系统设计方案

冻结状态：已冻结（V0.7 经验记忆基础版）

版本：0.7-draft
状态：设计稿，未编码
定位：V0.6 单文档闭环验证之后，将多类毕业设计材料纳入同一成长框架。

## 一、设计目标

- 不同类型毕业设计材料分别形成经验闭环；
- 不把所有文档混在一起学习；
- 文档类型级经验模型 + 跨文档共享经验；
- 新增材料类型时只新增“文档经验域”，不重造 Agent。

## 二、总体路线

```
V0.6  单文档闭环验证（任务书）
  ↓
V0.7  多文档经验成长
  ↓
V0.8  经验驱动生成
  ↓
V1.0  毕业设计智能制作 Agent
```

## 三、文档类型级经验模型

### 文档类型识别

输入：文档类型关键词/模板标识。

自动选择对应经验域：

- task_book → TaskBook Memory
- result → ResultDocument Memory
- evaluation_form → EvaluationForm Memory
- defense_record → DefenseRecord Memory
- guidance_record → GuidanceRecord Memory
- proposal_report → ProposalReport Memory
- midterm_check → MidtermCheck Memory

### 经验域示例

| 文档类型 | 学习重点 |
|---|---|
| 任务书 | 页数控制、表格空间、设计任务拆解、时间安排、内容密度 |
| 成果 | 章节结构、技术路线、故障分析逻辑、方案深度、图表比例、参考文献 |
| 成绩评定表 | 指标填写规律、分值合理性、评语模板、完整性、签字保护 |
| 答辩记录表 | 提问覆盖、回答质量描述、教师评语、成绩依据 |
| 指导记录表 | 指导过程、问题记录、签字区域 |
| 开题报告/中期检查表 | 结构、进度、问题与整改 |

## 四、经验库结构

```
CourseAgent Knowledge Memory
├── TaskBook Memory
├── Result Memory
├── Evaluation Memory
├── Defense Memory
├── Guidance Memory
├── Proposal/Midterm Memory
└── Common Document Quality Memory
```

每个文档域结构：

```json
{
  "type": "task_book",
  "memory_scope": "毕业设计任务书",
  "template_ids": [],
  "experiences": [],
  "golden_samples": [],
  "acceptance_thresholds": {}
}
```

### Common Document Quality Memory

可跨文档共享：

- Word 排版；
- 表格控制；
- 页数控制；
- 标点规范；
- 字体渲染；
- 目录最终化。

### 专属经验隔离

示例：

- 成果“参考文献数量”不得迁移到成绩评定表；
- 任务书“设计任务拆解”不得迁移到答辩记录表；
- 共享经验由通用层维护，专属经验按文档域隔离。

## 五、统一成长闭环

每类文档执行同一闭环：

```
模板解析
 ↓
优秀案例解析
 ↓
生成认知模型
 ↓
规划生成
 ↓
输出文档
 ↓
质量对比
 ↓
问题诊断
 ↓
局部优化
 ↓
经验候选
 ↓
人工审核固化
```

## 六、知识复用策略

新增学校/模板时：

- 已掌握“任务书这类文档该怎么做”；
- 只需学习学校 A 的模板约束、格式规范、特殊要求；
- 更新 template_ids 与经验适用范围；
- 不重新学习通用经验。

复用原则：

- 文档类型经验 = 通用 + 学校模板差异；
- 经验带 `applicable_scope` 与 `transfer_level`；
- 跨学校复用先校验模板兼容性。

## 七、V0.7 模块建议

1. DocumentTypeRouter：识别文档类型，选择经验域；
2. ExperienceDomainRegistry：注册/隔离各文档经验域；
3. CommonQualityMemory：共享排版/表格/标点经验；
4. DomainSpecificMemory：各文档专属经验；
5. ExperienceGate：人工审核唯一入口；
6. ExperienceRetriever：按文档类型/问题层/策略检索。

## 八、实施边界

本阶段：

- 只做设计，不编码；
- 不修改 V0.4/V0.3/V0.6 已有模块；
- 新能力默认关闭；
- 人工确认是长期知识库唯一入口。

暂不实现：

- 多文档自动批量学习；
- 自动跨域迁移；
- 自动升级经验；
- 复杂评分/相似度；
- Strategy Selector/A/B 评估。

## 九、路线里程碑

### V0.7.1 经验域注册

- DocumentTypeRouter；
- 任务书经验域完整化；
- 成果经验域启动。

### V0.7.2 共享经验层

- Common Document Quality Memory；
- 跨文档复用排版/表格/标点经验；
- 专属经验隔离校验。

### V0.7.3 多文档闭环

- 成绩评定表/答辩记录表等按同一闭环跑通；
- 每个文档域独立验证；
- 经验候选统一进入审核流程。

### V0.7.4 经验驱动生成

- Planner 按文档类型检索经验；
- 生成时引用已验证经验；
- 质量下降可回退。

## 十、验收原则

- 每类文档有独立经验域；
- 跨文档共享与专属隔离清晰；
- 新增文档类型只需注册新域；
- 经验固化必须人工确认；
- 不破坏现有稳定生产链路。
