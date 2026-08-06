# CourseAgent V0.5.1 架构审查报告

版本：0.5.1-draft
状态：架构复审稿
审查对象：《CourseAgent V0.5 自优化生成链路设计方案》《毕业设计生成经验系统设计》《V0.5实施路线图》

## 一、总体结论

V0.5 设计方向正确：从“生成→检查→修复”升级为“理解→规划→生成→验证→诊断→学习→优化”，并且坚持新模块默认关闭、不破坏现有链路。

但当前设计仍偏“模块愿望清单”，存在四个结构性缺口：

1. Template Schema 仍是格式描述，不是模板知识模型；
2. Generation Planner 缺少历史案例检索能力；
3. Strategy Selector 可能退化为规则判断；
4. Experience Optimizer 缺少反馈通道与反馈来源建模。

结论：暂不建议直接进入完整编码阶段；应先完成 V0.5.1 修订设计，再进行 Template Knowledge Model 原型验证。

## 二、当前设计优点

- 分层清晰：理解/规划/生成/验证/诊断/学习/优化；
- 新模块默认关闭，可独立测试；
- 经验以“问题层 + 根因 + 策略”建模，避免 if 规则堆积；
- 邱志豪案例根因抽象正确，未把“删除空段落”写死；
- 策略评分包含样本量与置信度，具备可解释性基础。

## 三、审查发现与修改建议

### 1. Template Schema 需升级为 Template Knowledge Model

问题：当前设计主要描述页面、区域、容量、字体，属于“格式 + 空间”描述，缺少结构关系与语义角色。

建议升级为三层知识模型：

```json
{
  "template_type": "task_book",
  "structure": {
    "sections": ["封面信息", "设计目标", "设计任务", "时间安排", "签字区"],
    "fixed_regions": ["时间安排", "签字区"],
    "binding": {
      "表注": ["表格首行", "表格内容"]
    }
  },
  "space": {
    "page_constraint": 2,
    "regions": [
      {"name": "设计目标", "max_lines": 5, "allow_expand": false},
      {"name": "设计任务", "max_lines": 8, "allow_expand": true}
    ],
    "capacity_model": "chars_per_line_by_region"
  },
  "semantic_roles": {
    "heading": "Heading1/2/3",
    "body": "正文内容",
    "caption": "表注",
    "reference": "参考文献",
    "field": "TOC/PAGE"
  }
}
```

- 结构：表达模板部件、固定区域、部件间绑定关系；
- 空间：表达页面容量、区域容量、可扩展性；
- 语义角色：表达内容元素应映射到哪个 Word 语义结构；
- 不变式：如“表注不得与表格分离”“目录必须为 TOC 域”。

### 2. Generation Planner 缺少案例检索能力

问题：规划器输入只写“历史案例”，未定义如何检索、相似度如何计算、如何复用。

建议增加 Case Retriever：

- 索引对象：template_schema、generation_plan、experience_record、diff_report 摘要；
- 检索特征：文档类型、专业方向、课题长度、模板容量、历史风险；
- 相似度：按特征加权计算；
- 输出：Top-K 相似案例及其策略、风险、效果评分；
- 规划器将检索结果作为约束，避免从零预测。

检索能力是“自优化”的前提：没有检索，规划器无法真正复用历史经验。

### 3. Strategy Selector 不得设计成规则判断

问题：当前“样本量>=3 选高分策略，否则用默认策略”仍是确定性规则，不是策略选择。

建议改为基于数据的策略选择器：

- 使用多臂老虎机或上下文老虎机建模；
- 探索/利用平衡：保留少量探索样本；
- 按上下文评分：文档类型、专业方向、风险等级、历史策略效果；
- 不确定性处理：样本量不足时降权，而不是固定走默认；
- 每次生成后回写 outcome，形成策略闭环；
- 输出必须可解释：为什么选 A、B 的历史效果与置信度。

判断标准：策略选择逻辑应只依赖“数据 + 策略模型”，不依赖 if-else 规则链。

### 4. Experience Optimizer 需支持三类反馈

问题：当前经验记录只有“案例结果”，未区分反馈来源，无法判断经验可信度。

建议增加反馈通道建模：

```json
{
  "feedback_source": "auto_detection | manual_review | final_acceptance",
  "feedback_detail": {
    "auto_detection": {"gate": "diff_report", "signal": "TOC制表位丢失"},
    "manual_review": {"reviewer": "teacher", "comment": "表注与表格跨页"},
    "final_acceptance": {"accepted": true}
  },
  "outcome": "success | fail | partial",
  "weight": 1.0,
  "timestamp": ""
}
```

- 自动检测反馈：来自 diff.py、content_quality.py、PDF 渲染检查；
- 人工评价反馈：来自教师/评审人，优先级最高；
- 最终验收反馈：来自交付门禁，决定经验是否进入正式规则；
- 冲突处理：人工反馈与自动检测冲突时，人工反馈优先并记录。

## 四、其他补充缺口

1. 模板版本管理：模板变更后必须检测漂移，旧 Schema 不得继续使用；
2. 规划-生成契约：generation_plan 必须被生成器执行，不能只是建议；
3. 根因证据链：每个经验记录应关联具体检测报告/差异报告，可追溯；
4. 评估装置：设置留存案例与 A/B 对比，避免策略自证；
5. 数据治理：案例记录保持脱敏，不写入未审核长期 Memory。

## 五、是否可以进入编码阶段

建议：暂不进入完整编码。

通过条件：

1. 完成 Template Knowledge Model 数据结构冻结；
2. 完成 Case Retriever 检索方案；
3. 完成 Strategy Selector 策略模型（非规则判断）；
4. 完成三通道反馈 Schema；
5. 通过留存案例评估基准。

若需渐进推进，可先编码 Template Knowledge Model 原型并做单案例验证，其余模块保持默认关闭。
