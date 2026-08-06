# Document Quality Sense（文档质量感知层）设计方案

版本：0.6.6-draft
状态：架构设计，未编码
原则：不修改 V0.4/V0.6 链路；王欢案例只用于提炼可迁移质量认知，不写死为固定规则。

## 一、总体模型

Document Quality Sense =
模板符合性
+ 信息结构合理性
+ 页面语义完整性
+ 视觉平衡
+ 阅读体验

关系：

```
TKM + TQM + Quality Sense → Generation Planner
```

## 二、能力组成

### 1. Page Semantic Quality

判断：

- 信息单元是否完整；
- 关联内容是否同页；
- 是否存在语义拆分。

示例：

```json
{
  "section_relation": "same_page",
  "reason": "目标与任务属于同一信息单元"
}
```

### 2. Region Integrity Quality

判断：

- 表格区域；
- 内容区域；
- 时间安排区域；
- 是否被不合理拆分。

### 3. Visual Balance Quality

判断：

- 页面密度；
- 空白比例；
- 内容集中度；
- 视觉重心。

### 4. Reading Flow Quality

判断阅读逻辑是否自然：

```
目标 → 任务 → 过程 → 成果
```

## 三、与 Reviewer 的关系

Reviewer 输出质量等级：

- L1：模板合规（页数/表格/容量）；
- L2：结构合理（区域归属/同页关系/信息单元）；
- L3：黄金质量（语义完整+视觉平衡+阅读流畅）。

结构通过但页面语义拆分时：

- 状态：L1 通过、L2 未达；
- 处理：进入 deviation 分析，不判定为优秀。

## 四、经验沉淀

Quality Sense 发现的问题不能直接成为长期规则：

```
发现问题
  ↓
experience_candidate
  ↓
人工确认
  ↓
long_term_quality_memory
```

## 五、边界

- 本阶段只做架构与案例验证；
- 不修改代码；
- 不修改 V0.4/V0.6；
- 新能力默认关闭。
