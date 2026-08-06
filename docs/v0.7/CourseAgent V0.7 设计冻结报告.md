# CourseAgent V0.7 设计冻结报告

版本：0.7-frozen
状态：已冻结（经验记忆基础版）
定位：V0.7 为经验积累阶段，不进入自动进化阶段。

## 一、冻结目标

让系统具备稳定、可审核、可积累的多文档经验记忆能力，为后续 V0.8 经验驱动生成提供事实基础。

## 二、保留能力

1. 案例闭环结果转经验候选；
2. 经验分析；
3. 经验分类存储；
4. 人工审核；
5. 已验证经验调用。

## 三、禁止能力

- 自动修改生成策略；
- 自动修改 Skill；
- 自动更新 Prompt；
- 自动升级长期知识；
- 自动策略选择。

## 四、经验状态

```
candidate
    ↓ 人工审核通过
approved_candidate
    ↓ 独立验证通过
validated_experience
    ↓ 人工确认
long_term_knowledge
```

人工确认是进入长期知识库的唯一入口。

## 五、当前边界

- 只实现经验候选、分析、分类、审核、调用；
- 不自动更新生成链路；
- 不自动升级 Skill/Prompt/策略；
- 不破坏 V0.4/V0.3/V0.6 已有能力；
- 新能力默认关闭。

## 六、V0.8 启动条件（等待积累）

需满足预设验证条件后再启动 V0.8 经验驱动生成设计：

1. 每个文档经验域至少有 1 个 `validated_experience`；
2. 至少 1 个经验经独立案例验证无回归；
3. 任务书/成果经验候选累计达到设定阈值；
4. 人工确认经验库可信；
5. 设计评审通过。

## 七、冻结结论

V0.7 作为经验记忆基础版本冻结：

- 系统负责收集、分析、分类、审核、调用经验；
- 自动进化能力全部关闭；
- V0.8 经验驱动生成设计在条件满足后再启动。

## 八、新增强制门：Experience Gate

- 经验进入 Memory 前必须通过 Evidence Quality Check；
- 真实案例：汪子涵基准 source_verified=false → invalid；杨振海基准 source_verified=true → candidate；
- 自动治理只筛选，人工确认仍是长期知识唯一入口。

## 九、新增能力：Reference Quality Sense

- 闭环：Reference Understanding → Diagnosis → Revision → Validation；
- 基准：杨振海成果模板（source_verified=true）；
- 禁止固定数值死规则；
- invalid_evidence 不得参与经验学习。
