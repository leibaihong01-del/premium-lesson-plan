# CourseAgent V1.1 DeepSeek + MiMo 双模型接入实施方案

日期：2026-08-02
基线：v1.0-baseline
模式：只读架构设计，未修改任何代码
业务定位：面向职业教育教师的智能助手（精品课程建设 + 毕业设计辅助），不是通用大模型平台。

## 0. 设计原则

1. 保持 v1.0 稳定：Rule Workflow 仍是主链路；
2. 小步修改：新增优先、默认关闭、逐阶段验证；
3. 不推倒重构，不接入 GLM，不设计无关平台能力；
4. DeepSeek 负责文字推理与教学设计，MiMo 负责视觉感知；
5. 所有模型输出必须经过 Evaluation，异常必须回退规则。

## 1. 当前架构适配分析

### 可复用能力

- models/base.py：统一 ModelAdapter 接口；
- models/registry.py：模型注册表；
- models/deepseek.py：DeepSeek Adapter（retry/timeout/cost/fallback 已加固，默认 disabled）；
- router/decision.py：rule / llm / hybrid 决策与 fallback；
- core/translator.py：规则 parse + enrich_spec_with_llm + translate_with_enhancement（默认关闭）；
- agents/preflight.py：需求预审（未接线）；
- prompts/：manifest + translator prompt 资产；
- evaluation/：案例、指标、runner、报告；
- modules/visual_checker.py：规则型 PDF 几何检测（pdfplumber + pypdfium2），无语义视觉理解；
- capabilities/：模板型能力生成。

### 现状缺口

- DeepSeek / Router / Preflight 均未接入 Orchestrator 主流程；
- MiMo Adapter 与视觉评测不存在；
- 内容生成仍是模板规则，未接入模型增强；
- 毕业设计类业务能力尚未进入 capabilities。

### 适配结论

V1.1 采用“增强节点 + 可选路径”方式接入，不改动 v1.0 默认行为。

## 2. DeepSeek 接入位置

DeepSeek 作为文字推理核心模型，接入以下节点：

| 节点 | 职责 | 接入方式 |
|---|---|---|
| Preflight | 需求理解、需求复述、信息完整性 | agents/preflight.py 可选启用 |
| Translator 增强 | TaskSpec 细化 | core/translator.translate_with_enhancement（enabled 时） |
| 内容生成 | 课程标准、教学进度、教案、PPT设计文案、毕业设计文档 | capabilities 生成路径可选 LLM 增强 |
| 质量判断辅助 | 教学设计合理性、内容完整度 | 仅作为 Evaluation 辅助，不由模型自评 |

接入约束：

- 规则 parse 先生成 TaskSpec；
- Router 判断是否启用 DeepSeek；
- LLM 输出必须过 evaluation gate；
- 任何异常回退规则 spec。

## 3. MiMo 视觉模块设计

### 3.1 新增 models/mimo.py

- MimoAdapter extends ModelAdapter；
- 实现 vision(image, prompt) 与 analyze_media(path, prompt)；
- 配置默认 disabled：enabled=false、base_url、api_key_env=MIMO_API_KEY、timeout、max_retries、价格参数；
- 成本统计与 DeepSeek 一致（calls / tokens / cost / failures）。

### 3.2 视觉能力范围

- 图片理解：教材图片、案例图、实训场景图；
- PPT 页面分析：版式、文字溢出、图表清晰度、页面一致性；
- PDF 视觉信息：封面、图表、公式、截图质量（补充 visual_checker 的几何检测）；
- 精品课程案例分析：从案例截图提取教学设计要素。

### 3.3 接入位置

- modules/visual_checker.py 增加可选视觉语义节点（保留现有几何检测）；
- 新增 modules/vision_analyzer.py 作为统一视觉分析入口（可选）；
- capabilities 或 orchestrator 的视觉任务走 MiMo 路径，默认关闭。

### 3.4 输出规范

统一输出结构化 JSON：

```json
{
  "ok": true,
  "issues": [],
  "visual_analysis": [],
  "confidence": 0.0,
  "model": "mimo"
}
```

## 4. Router 决策策略

### 4.1 保留现有 decide()

router/decision.py 的 decide() 继续兼容，新增 V1.1 决策函数：

- decide_v1_1(spec, modality, providers, compute_level)；
- modality：text / vision；
- 文本任务：rule / deepseek / hybrid；
- 视觉任务：rule（几何检测）/ mimo / hybrid（mimo + 规则校验）。

### 4.2 决策依据

- intent、domains、quality、compute_hint；
- modality（是否需要视觉）；
- enabled providers；
- 配置开关 translator.llm_enhance_enabled 与 vision.enabled。

### 4.3 默认策略

- 规则通过且置信度足够 → 规则；
- 规则不通过且模型可用 → 模型增强；
- 模型不可用 → 回退规则；
- 默认关闭模型路径。

## 5. Orchestrator 最小改造方案

### 5.1 不变部分

- run_document / run_capability 默认行为保持不变；
- 状态机、打包、复盘、记忆沉淀保持不变。

### 5.2 可选新增

- Orchestrator 构造函数增加可选参数 router=None、adapters=None、evaluation_gate=None；
- translate() 增加可选模型路径：当 translator.llm_enhance_enabled=true 且 provider enabled 时调用 translate_with_enhancement；
- run_capability 增加可选 LLM 生成路径：规则模板生成失败或配置启用时调用 DeepSeek，输出经 evaluation gate 后落盘；
- 新增 run_visual(capability, context) 可选入口（或由 modules/vision_analyzer 提供），默认不接管主流程。

改造量：仅新增分支，不修改既有默认路径。

## 6. Workflow 接入方案

```text
用户输入
  ↓
Preflight（可选）
  ↓
Translator（规则，可选 DeepSeek 增强）
  ↓
TaskSpec
  ↓
Router（文本/视觉决策）
  ↓
执行：规则生成 / DeepSeek 生成 / MiMo 视觉分析
  ↓
Evaluation gate
  ↓
通过 → 打包 + Memory 沉淀
  ↓
失败 → 修复或回退规则
```

- 主链路仍是规则；
- 模型能力以旁路节点形式接入；
- 每个节点有独立开关与回退。

## 7. 配置管理方案

### config/models.yaml

- deepseek：保留现有字段；
- 新增 mimo：enabled=false、model、base_url、api_key_env=MIMO_API_KEY、timeout、max_retries、retry_delay、价格参数；
- 默认 provider 为空；
- 不保存任何 API Key。

### config/agent_rules.yaml

- translator.llm_enhance_enabled=false；
- 新增 vision.enabled=false；
- 新增 business.capabilities 路由表（课程标准/教学进度/教案/PPT/毕业设计任务书/答辩记录表/指导记录/成果文档）。

### 环境变量

- DEEPSEEK_API_KEY；
- MIMO_API_KEY；
- 密钥只允许环境变量读取。

## 8. Prompt 管理方案

### prompts/manifest.yaml 版本化登记

新增业务 Prompt：

| Prompt ID | 用途 | 模型 |
|---|---|---|
| translator.system | 需求转译 | deepseek |
| curriculum.standard | 课程标准生成 | deepseek |
| progress.plan | 教学进度计划 | deepseek |
| lesson.plan | 教案生成 | deepseek |
| ppt.design | 教学PPT设计支持 | deepseek |
| graduation.task | 毕业设计任务书 | deepseek |
| defense.record | 答辩记录表 | deepseek |
| guidance.record | 指导记录 | deepseek |
| doc.normalize | 成果文档规范化 | deepseek |
| vision.image | 图片理解 | mimo |
| vision.ppt | PPT页面分析 | mimo |
| vision.pdf | PDF视觉信息 | mimo |

管理规则：

- 每个 Prompt 独立 version；
- 变更必须升版本并写 change_log；
- manifest 记录 model_compat 与 purpose；
- 新增 prompt 不修改已有 prompt 内容。

## 9. Evaluation 测试方案

### 9.1 文本评测

- 现有案例：translator_cases.json（10）+ translator_external_v1.0.json（10）；
- 新增业务案例：课程标准、教学进度、教案、PPT 设计、毕业设计任务书、答辩记录表、指导记录、成果文档；
- 对比：rule vs deepseek vs hybrid；
- 指标：structure / content / task_match / cost / latency；
- 禁止 LLM 自评。

### 9.2 视觉评测

- 新增 evaluation/cases/vision_cases.json：图片 / PPT页面 / PDF 样例；
- 指标：要素识别、版式问题检出、输出结构完整、成本；
- 对比：MiMo vs 规则几何检测（visual_checker）。

### 9.3 回归

- 现有 10 个测试全部通过；
- 新增 tests/test_mimo.py、tests/test_router_v1_1.py、tests/test_vision_gate.py；
- v1.0-baseline 不退化。

## 10. 回滚方案

1. 配置回滚：llm_enhance_enabled=false、vision.enabled=false，立即恢复纯规则；
2. Git 回滚：git checkout v1.0-baseline；
3. 文件回滚：新增优先，不修改既有默认路径；
4. 每次小步独立 commit，可单独回滚；
5. 模型不可用时不阻塞主链路。

## 11. 建议实施阶段

| 阶段 | 内容 | 产出 |
|---|---|---|
| V1.1-A | MiMo Adapter + config + registry | models/mimo.py、配置、测试 |
| V1.1-B | Router v1.1 决策 | decide_v1_1、路由测试 |
| V1.1-C | Translator/内容生成增强接线（默认关） | Orchestrator 可选分支、evaluation gate |
| V1.1-D | 视觉节点 + vision prompts | vision_analyzer、visual_checker 可选增强、prompts |
| V1.1-E | 精品课程 + 毕业设计业务能力试点 | 业务案例集、评测报告 |
| V1.1-F | 全量回归 + 人工验收 | 报告、标签 |

## 12. 范围边界

- 不接入 GLM；
- 不建设通用大模型平台；
- 不重构 Orchestrator；
- 不默认启用任何模型；
- 不在本阶段实现完整多模态训练或本地模型服务。

本方案为只读设计输出，等待人工确认后再进入代码实现。