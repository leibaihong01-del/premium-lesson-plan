# CourseAgent V1.0 阶段5.0：Prompt管理与Evaluation体系设计方案

版本：V1.0（设计稿）    日期：2026-08-02    状态：只设计，不写代码，等待人工确认
依据：AGENTS.md；《CourseAgent_V1.0阶段复盘报告.md》

## 一、为什么需要 Prompt 资产化

1. **可比较**：没有版本化 Prompt，就无法区分“模型变强”还是“Prompt变好”；
2. **可验证**：Prompt 是模型输出的主要变量，必须与评测集绑定；
3. **可回归**：模型升级、供应商切换后，需用同一 Prompt 版本复测；
4. **可治理**：统一管理版本、用途、输入输出契约，避免散落在调用代码里；
5. **低成本**：先做最小资产化，不引入复杂平台。

结论：在接入 DeepSeek 之前先建立实验基础，否则无法证明 LLM 收益。

## 二、目录设计

```text
CourseAgent/
├── prompts/
│   ├── manifest.yaml        # Prompt 清单（id、版本、用途、兼容模型）
│   └── translator/
│       ├── system.md        # 系统角色 Prompt
│       └── user.json        # 用户 Prompt 模板 + 输出 JSON Schema
└── evaluation/
    ├── cases/
    │   └── translator_cases.json   # 评测集（≥10案例）
    ├── metrics.py            # 指标计算（设计）
    ├── run_evaluation.py     # 评测入口（设计）
    └── reports/              # 评测报告输出
```

原则：prompts 只存放模板与版本元数据；evaluation 只存放案例、指标与运行结果。

## 三、Translator 评测集设计

10 个真实课程建设任务案例（字段：id、输入、期望intent、期望domains、期望quality、约束、交付物）：

| id | 输入 | 期望 intent/domains/quality | 关键约束 |
|---|---|---|---|
| T-01 | 请优化《城市轨道交通概论》课程标准，按精品课程要求，不要加入设备维修内容，输出审核报告 | optimize/课程标准/excellent | 禁止设备维修、闭环报告 |
| T-02 | 生成《城市轨道交通信号基础》教学进度计划，32学时 | generate/教学进度计划/normal | 32学时 |
| T-03 | 把旧教案转换为精品教案，模板在01_模板文件 | convert/教案/excellent | 模板优先 |
| T-04 | 生成教案封面，课程：城市轨道交通运营管理，专业：城市轨道交通运营管理 | generate/教案封面/normal | 课程、专业信息 |
| T-05 | 为《城市轨道交通概论》第3课生成课件PPT | generate/课件/normal | 与教案一致 |
| T-06 | 生成实训任务书（实训模块1） | generate/实训/normal | 安全交底、步骤、记录表 |
| T-07 | 生成题库：9项目+综合实训，附答案 | generate/题库/normal | 覆盖全部项目 |
| T-08 | 撰写教学能力比赛方案 | generate/竞赛/excellent | 精品标准 |
| T-09 | 撰写教改课题申报书框架 | generate/教研/normal | 申报书结构 |
| T-10 | 审核16份教案并输出报告，评分≥95 | audit/教案/formal | 评分≥95、闭环报告 |

## 四、评价指标

| 指标 | 定义 | 计算方式 |
|---|---|---|
| 内容质量 | 输出与期望内容一致性 | 期望字段命中率 + 规则校验分 |
| 结构完整 | TaskSpec 必需字段齐全 | intent/domains/quality/constraints/deliverables/confidence 全有 |
| 任务符合度 | intent 与 domains 匹配率 | 精确匹配比例 |
| 成本 | 单次调用 token 估算 | 输入+输出 token 估计 × 单价 |
| 响应时间 | 端到端延迟 | 平均/95分位 latency ms |

汇总规则：内容质量60% + 结构完整20% + 任务符合度20%；成本与响应时间作为约束指标，不进入质量总分但必须记录。

## 五、与未来 DeepSeek 闭环的关系

1. 先用同一评测集跑“规则基线”；
2. 接入 DeepSeek 后跑“LLM增强”与“混合”；
3. 对比指标：LLM 必须优于或等于规则基线，且成本/延迟在预算内，才允许上线；
4. 不满足则保持规则路径，避免“为接入而接入”；
5. evaluation/reports 作为模型升级与供应商切换的回归依据。

## 六、实施范围

本阶段只输出设计，不写代码。经人工确认后，下一步（阶段5.1）将新增：

- prompts/manifest.yaml、prompts/translator/system.md、user.json；
- evaluation/cases/translator_cases.json、metrics.py、run_evaluation.py；
- 运行“规则基线评测”并输出第一份评测报告。

本设计文件未创建或修改任何代码。
