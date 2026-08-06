# V0.7 Experience Gate 强制门设计

版本：0.7-gate
状态：正式加入 V0.7，作为经验进入 Memory 的强制门

## 一、原则

任何经验进入 Memory 前，必须通过 Experience Gate 的 Evidence Quality Check。

否则案例越多，污染风险越大。

## 二、强制检查

1. Evidence Quality Check：
   - source_verified=true 才可进入；
   - 来源文件存在；
   - 文件版本明确；
   - 解析结果可靠；
2. Generalization Check：
   - 单案例/多案例标记；
   - 可迁移性；
3. Conflict Detection：
   - 新旧经验冲突；
   - 同领域冲突。

## 三、真实案例

| 案例 | source_verified | 状态 |
|---|---|---|
| 汪子涵参考文献基准 | false | invalid_evidence，禁止进入 |
| 杨振海参考文献基准 | true | candidate，可进入 evidence_checked |

## 四、状态流转

```
candidate
  ↓ Evidence Quality Check 通过
evidence_checked
  ↓ 多案例验证 + 人工确认
validated_experience
  ↓ 长期稳定
stable_knowledge → long_term_knowledge
```

未通过 → invalid，记录原因，不得进入 Memory。

## 五、与 V0.7 集成

- V0.7 冻结范围新增 Experience Gate 为强制门；
- 自动治理只筛选，人工确认仍是稳定知识最终入口；
- 新能力默认关闭，但经验固化流程必须启用该门。
