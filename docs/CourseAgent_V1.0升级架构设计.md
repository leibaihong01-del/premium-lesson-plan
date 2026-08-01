# CourseAgent V1.0 升级架构设计（LLM Enhanced Agent）

版本：V1.0（设计评审稿）    日期：2026-08-01
状态：设计评审阶段，等待人工确认后进入实施
依据：AGENTS.md 第一性原理审查原则；《07_Agent架构现状评估报告.md》

## 固定工作流

阶段0 AGENTS约束 → 阶段1 架构评估 → 阶段2 设计方案（不写代码）→ 阶段3 人工确认 → 阶段4 小步实施 → 阶段5 自动测试 → 阶段6 经验沉淀。

## 第一性原理预审结论

1. 是否必须用LLM解决：否。仅“语义理解、复杂判断、方案生成”存在真实缺口；格式、流程、校验由规则继续负责。
2. 哪些能力交给模型：需求理解（语义层）、任务规划建议、内容生成（受模板约束）、开放问题判断、知识影响判断（可选）、反思总结（可选）。
3. 哪些保持规则：文件解析/生成、格式/结构/分页/颜色检测、时间链与完整性校验、算力路由（规则优先）、Skill调度、打包、审批状态机、成本统计。
4. 是否存在过度设计：vision()、embed() 在V1.0无真实业务需求，仅设计为预留接口，不在本版本实现。
5. 是否影响现有稳定流程：阶段1“只新增不修改”，LLM默认关闭（fallback规则），通过配置开关控制，保证现有Workflow不受影响。

---

# 一、当前架构复盘

## 1. 当前架构图

```text
用户/CLI
  ↓
Agent Controller（main.py / Orchestrator）
  ↓
Workflow：转译 → 规划 → 执行 → 检测 → 修复 → 打包 → 学习
  ↓
Agents（planner/writer/reviewer/learner/router/light_judge）
  ↓
Modules（模板解析/文档生成/格式与内容检测/打包/缓存/视觉）
  ↑
Memory（JSON） / Knowledge（接口） / Skills（注册表） / Tools（脚本）
```

## 2. 当前模块职责

| 模块 | 职责 | 现状 |
|---|---|---|
| agents/ | 规划、生成、审核、学习、路由、轻量判断 | 规则脚本 |
| core/ | 总控、转译、记忆、进化、满意度预测、问题解决、Skill | 规则脚本 |
| modules/ | 模板解析、文档生成、检测、打包、缓存、视觉检查 | 规则工具 |
| capabilities/ | 竞赛、科研、成果生成 | 规则生成器 |
| tools/ | 自检、审核、审批、监测、画像 | 规则工具 |
| memory/ | 成功/失败/规则/改进/任务指纹/知识更新 | JSON存储 |

## 3. 已有能力

- Workflow闭环可运行；
- 四维质量评分与修复循环；
- 自适应算力路由与决策缓存；
- Skill六件套与7个能力单元注册；
- 可控升级三级（L1自动/L2验证/L3审批）；
- 知识联网监测（正文级候选提取）；
- 用户模型、成长报告、输出归档。

## 4. 当前限制

- 需求转译为关键词规则，无语义理解；
- 内容生成为模板/规则，无模型调用；
- Memory为JSON线性读写，无语义检索；
- 任务状态在内存，中断不可恢复；
- 无统一评测集与回归测试；
- 视觉检查为程序化像素/文本，非视觉理解。

## 5. 保留与新增边界

| 类别 | 模块 |
|---|---|
| 保留不动 | modules/、capabilities/、agents/reviewer、agents/learner、tools/ 现有工具、memory 现有结构 |
| 保留但预留开关 | core/translator、core/excellence_engine、core/knowledge_update（后续可选接入LLM增强） |
| 新增 | models/、router/、prompts/、evaluation/、state/、config 模型配置 |

---

# 二、CourseAgent V1.0 目标架构设计

## 1. 目标架构图

```text
用户层（CLI / 自然语言）
  ↓
Agent Controller（总控/状态机）
  ↓
Workflow Layer（转译→规划→执行→检测→修复→打包→学习）
  ↓
LLM Router（任务分类→模型选择→降级策略）
  ↓
Model Adapter（统一接口：generate/analyze/vision/embed/health_check）
  ↓
模型层：DeepSeek（当前） / GLM（未来） / MiMo（未来）

支撑层：Memory / Knowledge / Skills / Tools / Evaluation / state
```

## 2. 各层职责

| 层 | 职责 |
|---|---|
| 用户层 | 接收自然语言与文件 |
| Agent Controller | 总控状态机、任务生命周期、断点恢复 |
| Workflow Layer | 固定流程编排，规则优先 |
| LLM Router | 按任务类型与复杂度选择模型或规则 |
| Model Adapter | 屏蔽模型差异，统一接口 |
| Memory | 结构化+语义检索（演进目标） |
| Knowledge | 知识更新、影响判断、候选确认 |
| Skills | 六件套能力单元 |
| Tools | 文件、检测、打包、自检 |
| Evaluation | 测试案例、指标、回归 |

---

# 三、LLM 适配层设计（重点）

## 1. 目录结构

```text
models/
├── base.py          # ModelAdapter 抽象接口
├── deepseek.py      # DeepSeek 实现
├── glm.py           # GLM 实现（预留）
├── mimo.py          # MiMo 实现（预留）
└── registry.py      # 模型注册与配置
```

## 2. 统一接口（设计）

```python
class ModelAdapter:
    def generate(self, prompt, system=None, **kwargs) -> str: ...
    def analyze(self, prompt, context=None, **kwargs) -> dict: ...
    def vision(self, image, prompt, **kwargs) -> str: ...   # V1.0 预留
    def embed(self, texts, **kwargs) -> list: ...           # V1.0 预留
    def health_check(self) -> dict: ...                     # 连通性/延迟/配额
```

约束：核心Agent只依赖 `ModelAdapter` 抽象，不依赖具体模型类。

## 3. 接入方式

- DeepSeek：OpenAI兼容接口，配置 base_url、api_key、model；`health_check` 验证连通。
- GLM：实现同一接口，配置智谱API参数即可，不改核心逻辑。
- MiMo：按供应商接口实现 adapter；通过 `registry` 注册，Router按配置选择。

## 4. 配置

模型配置写入 `config/models.yaml`（本阶段不创建代码，仅设计）：provider、model、base_url、api_key_env、enabled、fallback。

---

# 四、模型调用策略设计

| 任务 | 策略 | 理由 |
|---|---|---|
| 需求理解 | LLM语义增强 + 规则兜底 | 规则无法覆盖复杂自然语言 |
| 任务规划 | LLM建议 + 规则约束 | 保持流程边界 |
| 内容生成 | LLM生成 + 模板/规则校验 | 质量底线不变 |
| 质量判断 | 规则为主（四维评分） | 可复现、低成本 |
| 视觉分析 | 程序化检查（V1.0）；vision预留 | 当前无真实视觉需求 |
| 文件处理 | 规则 | 稳定、可测 |
| 知识更新 | 规则抓取 + LLM影响判断（可选） | 避免噪音 |

原则：LLM输出必须经过规则校验；校验不过则重试或回退规则结果。

---

# 五、任务状态持久化设计（state/）

## 1. 现状问题

Orchestrator 状态在内存，中断/重启后丢失，无法续跑与审计。

## 2. 设计

- 任务ID：uuid，贯穿全流程。
- 状态保存：`state/tasks/<task_id>.json`，记录 spec、state、steps、artifacts、trace、created/updated。
- 断点恢复：启动时按任务ID读取状态，从最后一个完成步骤续跑。
- 运行日志：`state/logs/<task_id>.log`，记录每步决策与结果。

本阶段仅设计方案，不实现。

---

# 六、Memory 升级方向

## 演进路线

```text
规则记录（现状：JSON线性）
  ↓
结构化Memory（索引+类型化字段，先建表与检索）
  ↓
语义检索Memory（embed + 向量库，预留）
```

原则：先结构化，后语义化；不一次性引入向量库，避免过度设计。

---

# 七、评测体系设计（evaluation/）

## 结构

```text
evaluation/
├── cases/        # 测试案例：id、输入、期望输出
├── metrics.py    # 评价指标计算
└── regression.py # 回归测试入口
```

## 指标

- LLM调用成功率；
- 输出质量（结构完整、内容一致、评分≥95）；
- 任务完成率；
- 成本统计（token/请求数）；
- 异常恢复（失败→重试→降级）。

## 回归基线

现有16份教案、课件样例、题库样例作为回归基线，模型升级后必须复测通过。

---

# 八、改造实施路线

| 阶段 | 目标 | 新增文件 | 修改范围 | 风险 | 验证方式 |
|---|---|---|---|---|---|
| 0 架构确认 | 本设计评审通过 | 无 | 无 | 低 | 人工确认 |
| 1 LLM适配层 | 只新增不修改，默认关闭 | models/、config/models.yaml | 无核心改动 | 低 | health_check + 单元测试 |
| 2 DeepSeek接入 | 试点需求理解/内容生成 | models/deepseek.py | translator可选调用 | 中 | 评测用例+回归 |
| 3 Router增强 | 任务分类→模型/规则选择 | router/ | orchestrator调用点 | 中 | 路由准确率+fallback测试 |
| 4 Memory升级 | 结构化索引+状态持久化 | state/、memory索引 | memory读写层 | 中 | 断点恢复测试 |
| 5 GLM/MiMo扩展 | 多模型可切换 | models/glm.py、mimo.py | registry配置 | 低 | 多模型一致性测试 |

---

# 九、风险分析

1. LLM成本风险：设调用上限、缓存、低档模型兜底、成本统计。
2. 模型依赖风险：Adapter隔离+多供应商；单模型故障自动回退规则。
3. 输出不可控风险：LLM输出必须过规则校验，不达标重试/降级。
4. Memory污染风险：模型输出写入Memory前需校验与人工/规则确认。
5. 架构复杂化风险：新增模块职责单一，禁止跨层直连。
6. 对现有Workflow影响：阶段1默认关闭LLM，回归测试保障不回归。

---

# 十、最终建议

1. V1.0最小可行升级：阶段0确认 + 阶段1适配层 + 阶段2 DeepSeek试点（需求理解、内容生成）+ 基础状态持久化。
2. 暂缓：vision、embed/语义检索、GLM/MiMo实际接入、在线学习闭环。
3. 原因：低成本、低风险演进，先用真实任务验证LLM收益，再扩展能力。
4. 下一步开发顺序：人工确认本设计 → 阶段1（只新增）→ 阶段2试点 → 自动测试 → 经验沉淀。

---

本文件仅为设计，未创建或修改任何代码文件；等待人工确认后进入实施阶段。
