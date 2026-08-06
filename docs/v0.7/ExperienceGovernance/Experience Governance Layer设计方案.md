# Experience Governance Layer 设计方案

版本：0.7-gov-draft
状态：设计稿，未编码
目标：防止错误案例解析导致错误经验进入长期 Memory。

## 一、定位

Experience Governance Agent 位于经验候选进入长期知识库之前，是自动质量监管层。

```
Experience Candidate
        ↓
Experience Governance Agent
  1. Evidence Verification
  2. Generalization Check
  3. Conflict Detection
  4. Lifecycle 管理
        ↓
只允许通过治理的经验进入长期 Memory
```

## 二、能力

### 1. Evidence Verification

检查：

- 来源文件是否存在；
- 文件版本是否明确；
- 数据可信度；
- 解析结果可靠性；
- 是否 source_verified。

示例：汪子涵参考文献分析被标记 `source_verified=false`、`invalid_evidence`，不得进入经验库。

### 2. Generalization Check

判断：

- 单案例规律；
- 多案例规律；
- 是否可迁移；
- 是否仅适用于特定模板/方向。

### 3. Conflict Detection

检测：

- 新旧经验冲突；
- 同领域规则冲突；
- 适用范围重叠但结论相反。

### 4. Experience Lifecycle

状态流转：

```
candidate
  ↓ 证据通过
evidence_checked
  ↓ 多案例验证 + 人工确认
validated_experience
  ↓ 长期稳定
stable_knowledge
```

异常状态：

- invalid：证据不足/解析不可信；
- deprecated：被新经验取代或验证失败。

## 三、原则

- 禁止错误经验进入长期 Memory；
- 自动治理只负责筛选与标记；
- 人工确认仍是 stable_knowledge 的最终入口；
- 所有状态变化保留审计记录。
