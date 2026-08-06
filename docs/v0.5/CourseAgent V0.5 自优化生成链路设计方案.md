# CourseAgent V0.5 自优化生成链路设计方案

版本：0.5-draft
状态：设计稿，未编码
适用范围：毕业设计任务书、成果及其他模板重构型文档

## 一、当前问题分析

### 1. 现状

当前链路：

```
资料输入 → 生成 → 检查 → 修复 → 交付
```

已验证案例：王欢任务书、汪子涵任务书、邱志豪任务书；成果案例：王欢、汪子涵、邱志豪。

### 2. 核心问题

当前系统能够检测和修复问题，但缺少“生成前智能规划”：

- 模板被当成 Word 文件处理，而不是带空间约束的知识对象；
- 内容生成前不做区域容量与页数预测，超页后靠后处理补救；
- 每个问题形成一条修复规则，容易演变为 if 规则堆积；
- 经验以“案例结论”记录，未抽象为“问题层 + 根因 + 策略”。

### 3. 邱志豪案例启示

邱志豪任务书首次生成 3 页、模板 2 页。如果只沉淀“删除空段落规则”，下一次遇到不同超页原因仍会失败。

正确经验应抽象为：

```
问题：固定页模板生成失败
根因：生成阶段未考虑模板空间约束
策略：生成前进行页面规划、区域容量预测、内容长度控制
```

## 二、目标

将生成链路升级为：

```
理解 → 规划 → 生成 → 验证 → 诊断 → 学习 → 优化
```

最终目标不是“遇到问题增加规则”，而是“通过多个案例总结最佳生成路径，并自动选择更优方案”。

## 三、总体架构

```
资料输入
    ↓
任务理解层（复用 Document IR 元数据）
    ↓
Template Intelligence Layer（模板智能解析）
    ↓
Generation Planner Agent（生成规划）
    ↓
Strategy Selector（策略选择）
    ↓
现有生成链路（v03 任务书 / v04 成果）
    ↓
多层验收（内容 / 模板 / 视觉 / 学院 / 交付）
    ↓
问题诊断（Problem Diagnoser）
    ↓
Experience Optimizer（经验优化）
    ↓
策略评分更新 → 下一次规划优化
```

## 四、模块设计

### 模块1：Template Intelligence Layer

目标：将 Word 模板转换为结构化模板知识，输出 `template_schema.json`。

功能：

1. 识别页面数量、页面尺寸、页边距；
2. 识别表格结构、单元格位置、固定区域；
3. 识别字体、字号、段落规则；
4. 计算区域容量（行数、字符数估算）；
5. 输出页面约束、区域定义、容量限制、格式规则。

设计原则：模板解析与内容生成解耦；模板 Schema 可缓存，不重复解析。

### 模块2：Generation Planner Agent

目标：生成前规划内容分配、页面布局与风险预测，输出 `generation_plan.json`。

输入：学生信息、课题、模板 Schema、历史案例统计。

输出内容：

- 内容分配：每个区域的字数/行数预算；
- 页面规划：第一页/第二页内容边界；
- 风险预测：超页风险、区域容量不足、格式冲突；
- 建议策略：直接生成或规划后生成。

### 模块3：Experience Optimizer

目标：从案例中学习，输出 `experience_record.json`。

输入：案例结果（case、problem、cause、solution、effect_score）。

输出：

```
案例
  ↓
问题
  ↓
原因（按问题层归类）
  ↓
解决策略
  ↓
效果评分
  ↓
验证状态
```

注意：不直接修改 Skill；只形成经验记录与候选策略。

### 模块4：Strategy Selector

目标：根据历史案例成功率选择最佳生成路径。

策略示例：

```
方案A：直接生成（历史成功率 70%）
方案B：规划后生成（历史成功率 95%）
```

选择逻辑：

- 样本量足够时选择成功率高的策略；
- 样本量不足时采用保守策略或默认策略；
- 每次验证后更新策略评分。

## 五、数据结构

### template_schema.json（示例）

```json
{
  "template_type": "task_book",
  "page_constraint": 2,
  "regions": [
    {"name": "设计目标", "max_lines": 5, "allow_expand": false},
    {"name": "设计任务", "max_lines": 8, "allow_expand": true},
    {"name": "时间安排", "fixed": true}
  ],
  "format_rules": {
    "body_size": "12pt",
    "font_cn": "宋体",
    "font_en": "Times New Roman"
  }
}
```

### generation_plan.json（示例）

```json
{
  "content_allocation": {
    "设计目标": {"chars": 100},
    "设计任务": {"chars": 300},
    "时间安排": {"fixed": true}
  },
  "page_plan": {
    "page1": ["基本信息", "设计目标"],
    "page2": ["设计任务", "时间安排", "签字区"]
  },
  "risk_prediction": {
    "page_overflow_risk": "high",
    "reasons": ["设计任务可能过长", "表格容量不足"]
  }
}
```

### experience_record.json（示例）

```json
{
  "case": "邱志豪",
  "problem": "固定页模板生成失败",
  "cause_layer": "template_space_constraint",
  "cause": "生成阶段未考虑模板空间约束",
  "solution": "生成前页面规划与区域容量预测",
  "effect_score": 95,
  "validation": "candidate"
}
```

## 六、调用流程

```
1. 读取学生信息、课题、模板路径
2. Template Intelligence Layer 生成 template_schema.json
3. Generation Planner Agent 生成 generation_plan.json
4. Strategy Selector 选择生成策略
5. 调用现有 v03/v04 生成链路
6. 多层验收
7. 问题诊断归类（问题层、根因、所属模块）
8. Experience Optimizer 生成经验候选
9. 策略评分更新
```

## 七、与现有代码关系

| 现有能力 | V0.5 定位 |
|---|---|
| v04 `profile.py` 模板画像 | 升级为 Template Intelligence Layer 基础能力 |
| v04 `clean.py` Document IR | 复用为任务理解层 |
| v03 任务书生成 / v04 成果生成 | 保留为执行层 |
| `content_quality.py`、`diff.py` | 复用为验收层 |
| 规则候选 `experience/candidates` | 升级为 Experience Optimizer 输入 |
| `workflow.yaml` | 扩展策略选择入口 |

## 八、实施原则

1. 新模块默认关闭，通过配置开关启用；
2. 可独立测试，不影响现有稳定流程；
3. 不直接修改现有 Skill 规则；
4. 所有优化必须经案例验证；
5. 禁止大量 if 规则堆积，优先按“问题层 + 根因 + 策略”建模。
