# CourseAgent V0.5.2 实施边界设计

版本：0.5.2-draft
状态：实施范围收敛稿
原则：避免过度工程化；保留长期架构方向；新能力默认关闭，不影响 V0.4 稳定生产链路。

## 一、必须实现能力

### 1. Template Knowledge Model（核心）

- 模板结构：分区、固定区域、区域绑定关系；
- 模板空间：页面约束、区域容量、可扩展标记；
- 模板语义角色：heading/body/caption/reference/field；
- 模板不变式：表注与表格绑定、目录必须为 TOC 域等；
- 输出 `template_knowledge_model.json`。

### 2. Generation Planner（轻量版）

- 输入：学生信息、课题、Template Knowledge Model、可选案例参考；
- 输出 `generation_plan.json`：
  - 区域内容分配（字数/行数预算）；
  - 页面风险预测（超页/容量不足）；
  - 建议生成策略（直接生成 或 规划后生成）。
- 本期只做“可解释的容量预测与风险提示”，不做复杂决策。

### 3. Case Retriever（轻量索引版）

- 建立案例索引：文档类型、专业方向、课题长度、模板约束、已知风险；
- 按特征简单匹配 Top-K 案例；
- 为 Planner 提供历史参考，不做机器学习；
- 输出 `case_reference.json`。

### 4. Experience System（轻量记录版）

- 支持三类反馈来源：auto_detection / manual_review / final_acceptance；
- 输出 `experience_candidate.json` 与 `feedback_record.json`；
- 只记录与沉淀候选，不自动升级 Skill；
- 所有经验保留来源、验证状态、证据链接。

## 二、暂不实现能力

- Strategy Selector 算法实现；
- 上下文老虎机 / 多臂老虎机；
- A/B 评估系统；
- 策略自动切换；
- 经验自动升级为正式 Skill 规则；
- 模板漂移自动检测（本期仅记录模板版本号）；
- 复杂相似度模型 / 向量检索。

## 三、模块依赖关系

```
Template Knowledge Model
          ↓
Generation Planner ──→ Case Retriever
          ↓
现有 v03/v04 生成链路（默认仍直接执行）
          ↓
现有验收层（diff/content/PDF）
          ↓
Experience System（候选记录）
```

依赖约束：

- Planner 可选，默认关闭；
- Case Retriever 仅被 Planner 调用；
- Experience System 只读取验收结果，不反向修改生成器；
- 所有新模块通过配置开关启用。

## 四、数据结构定义

### template_knowledge_model.json

```json
{
  "template_id": "task_book_golden_v1",
  "template_type": "task_book",
  "page_constraint": 2,
  "structure": {
    "sections": ["封面信息", "设计目标", "设计任务", "时间安排", "签字区"],
    "fixed_regions": ["时间安排", "签字区"],
    "binding": [
      {"from": "表注", "to": "表格首行", "invariant": true}
    ]
  },
  "space": {
    "regions": [
      {"name": "设计目标", "max_lines": 5, "allow_expand": false},
      {"name": "设计任务", "max_lines": 8, "allow_expand": true}
    ]
  },
  "semantic_roles": {
    "heading": ["Heading1", "Heading2", "Heading3"],
    "body": "正文内容",
    "caption": "表注",
    "reference": "参考文献",
    "field": ["TOC", "PAGE"]
  },
  "format_rules": {
    "body_size": "12pt",
    "font_cn": "宋体",
    "font_en": "Times New Roman"
  }
}
```

### generation_plan.json

```json
{
  "plan_id": "plan_qzh_taskbook_v1",
  "template_id": "task_book_golden_v1",
  "content_allocation": {
    "设计目标": {"chars": 100, "lines": 5},
    "设计任务": {"chars": 300, "lines": 8},
    "时间安排": {"fixed": true}
  },
  "risk_prediction": {
    "page_overflow_risk": "high",
    "reasons": ["设计任务内容可能超过8行", "固定页不可扩展"]
  },
  "recommended_strategy": "plan_then_generate"
}
```

### case_reference.json

```json
{
  "case_id": "qiu_zhihao_taskbook",
  "document_type": "task_book",
  "direction": "电梯系统",
  "known_risks": ["页面溢出", "区域容量不足"],
  "effective_measures": ["生成前容量预测", "尾部空段落收敛"],
  "validation": "candidate"
}
```

### experience_candidate.json / feedback_record.json

```json
{
  "case_id": "qiu_zhihao_taskbook",
  "problem_layer": "template_space_constraint",
  "root_cause": "生成阶段未考虑模板空间约束",
  "strategy": "生成前页面规划与区域容量预测",
  "feedback_source": "auto_detection",
  "outcome": "success",
  "evidence": ["render_check.pdf", "internal_audit.md"],
  "validation_status": "candidate"
}
```

## 五、单案例验证方案

验证对象：邱志豪任务书（历史问题：3 页超模板 2 页）。

步骤：

1. 对任务书模板生成 Template Knowledge Model；
2. 使用 Planner 生成计划，应预测“超页风险高”；
3. 复用现有 v03 任务书生成链路生成 DOCX；
4. 验收：页数、结构、命名、渲染；
5. 生成 Experience Candidate；
6. 对比：启用 Planner 提示与不启用时的首轮达标情况；
7. 通过标准：
   - Template Knowledge Model 可解释；
   - 超页风险预测命中；
   - 未影响 V0.4/V0.3 现有生成行为；
   - 新增模块可独立关闭。

## 六、进入编码前检查清单

- [ ] Template Knowledge Model JSON Schema 已冻结；
- [ ] 新模块目录已建立且默认关闭（配置开关）；
- [ ] Case Retriever 轻量索引结构已定义；
- [ ] Experience Candidate 三通道反馈字段已定义；
- [ ] 邱志豪案例基线数据已准备；
- [ ] 不影响现有 v03/v04 链路的验证用例已明确；
- [ ] 阶段验收标准（单案例验证通过）已确认。

## 七、结论

V0.5.2 先做“可解释的模板知识 + 轻量规划 + 经验候选”，不实现策略自动选择。待 3 个以上案例验证后，再评估 Strategy Selector 与 A/B 评估。
