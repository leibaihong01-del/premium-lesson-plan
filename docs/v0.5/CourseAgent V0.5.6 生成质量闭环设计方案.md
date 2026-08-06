# CourseAgent V0.5.6 生成质量闭环设计方案

版本：0.5.6-draft
状态：设计稿，未编码
原则：先设计闭环，再编码；不修改 V0.4/V0.3；新增能力默认关闭。
定位：Experience Evolution 是生成质量闭环的一部分，不是独立模块。

## 一、设计目标

回答核心问题：

> 一个案例从输入到最终优秀输出，中间如何自动学习和改进？

目标不是“保存更多经验”，而是：

> 每做一次任务，下一次做类似任务就更接近专家水平。

## 二、总体闭环

```
① 文档理解（Document Understanding）
    模板结构 / 内容结构 / 页面布局 / 表格关系 / 优秀案例特征
        ↓
② 生成认知模型
    有哪些区域、每个区域写什么、写多少、怎么排版、接近什么优秀样本
        ↓
③ Generation Planner
    页面安排 / 内容策略 / 字数预算 / 风险预测
        ↓
④ Writer
    生成 DOCX（复用现有 v03/v04 链路）
        ↓
⑤ Reviewer
    生成版本 VS 黄金版本：结构 / 内容 / 视觉 / 空间
        ↓
⑥ 自动诊断
    为什么不像黄金版本：差异层 / 根因 / 可执行调整
        ↓
⑦ 优化生成
    调整后生成第二版（有界迭代，默认最多 2 轮）
        ↓
⑧ 经验沉淀
    形成候选策略；类似任务自动优先采用
```

## 三、模块拆解

### A. Document Understanding

- 解析模板 → TKM；
- 解析黄金案例 → TQM；
- 解析内容规律 → 内容策略索引；
- 输出：Document Cognitive Model（生成认知模型）。

认知模型内容：

```
template_id
regions（含容量、语义角色、生成策略）
golden_references（适用范围、迁移级别）
content_strategy（目标组织、任务拆分、紧凑/扩展区域）
```

### B. Generation Planner

- 输入：学生信息、课题、认知模型、风险历史；
- 输出：Generation Plan（含 golden_reference_id、预算、页面规划、风险预测、调整建议）。

### C. Writer

- 复用现有 v03 任务书生成器 / v04 成果生成器；
- 可选读取 Generation Plan；
- 默认关闭，不改变现有行为。

### D. Reviewer

- 不检查“是否报错”，而检查“与黄金版本差距”；
- 对比维度：
  - 结构差异：区域、表格、固定页；
  - 内容差异：密度、段落数、任务粒度、表达方式；
  - 视觉差异：页面平衡、空白、标题位置；
  - 空间差异：页数、区域占比、跨页、空段落占用。

### E. Auto Diagnoser

- 对差异分类：
  - template_space_constraint
  - content_model
  - word_structure
  - generation_strategy
  - reviewer_capacity
- 输出：
  - 差异位置；
  - 差异数值；
  - 根因；
  - 调整建议；
  - 是否可自动修正。

### F. Revision Planner

- 接收诊断结果；
- 生成 Revision Plan；
- 执行有界重生成；
- 默认最多 2 轮，防止无限循环。

### G. Experience System

- 记录候选经验；
- 人工确认后更新 TQM golden_samples；
- 通过策略评分影响后续 Planner；
- 属于闭环的第 ⑧ 阶段，不是独立“经验进化”。

## 四、与 V0.5.5 关系

| V0.5.5 模型 | V0.5.6 使用位置 |
|---|---|
| TKM | ① 文档理解 |
| TQM | ① 文档理解 + ⑤ Reviewer |
| Generation Plan | ③ 生成规划 |
| Experience Candidate | ⑧ 经验沉淀 |

新增模型：

- document_cognitive_model.json
- gap_report.json
- diagnosis_record.json
- revision_plan.json

## 五、数据流

```
TKM + TQM + 内容规则
        ↓
document_cognitive_model.json
        ↓
generation_plan.json
        ↓
Writer → version1.docx
        ↓
Reviewer → gap_report.json
        ↓
Auto Diagnoser → diagnosis_record.json
        ↓
Revision Planner → revision_plan.json
        ↓
Writer → version2.docx
        ↓
Reviewer（达标）
        ↓
Experience Candidate
```

## 六、邱志豪示例（证据驱动诊断）

- 生成前：Planner 预测高超页风险；
- 第一版：3 页；
- 对比黄金：页数 3 vs 2，设计任务行 10 段（7 非空 + 3 空段），黄金同为 10 段（7 非空 + 3 空段）；
- 正确诊断：不是“任务拆分粒度过细”，而是“空段落与换行估算导致第 2 页容量不足”；
- 调整建议：按 blank_paragraph_slack 收敛空段落，并复核换行估算；
- 第二版：2 页，达标。

说明：自动诊断必须以证据为准，不能套用用户示例中的“任务粒度”结论。

## 七、编码边界

本期设计阶段：

- 冻结新增 4 类 Schema；
- 确定闭环模块接口；
- 默认关闭，不接入生产。

后续编码范围（经评审后）：

- Document Understanding 轻量实现；
- Reviewer 差异计算；
- Auto Diagnoser 规则化诊断（基于问题层）；
- Revision Planner 有界迭代；
- Experience Candidate 写入。

暂不实现：

- AI 视觉模型；
- OCR；
- 自动截图比较；
- 复杂评分/相似度算法；
- Strategy Selector；
- A/B 评估；
- 无限自动重生成。

## 八、风险分析

| 风险 | 说明 | 缓解 |
|---|---|---|
| 过度迭代 | 自动重生成无限循环 | 默认最多 2 轮 |
| 黄金过拟合 | 强制向单一样本靠拢 | TQM 多样本 + transfer_level |
| 误诊 | 诊断套用示例结论 | 所有诊断必须附证据 |
| 隐私 | 学生数据进入经验 | 案例脱敏 |
| 回归 | 新闭环影响现有链路 | 默认关闭，独立测试 |
