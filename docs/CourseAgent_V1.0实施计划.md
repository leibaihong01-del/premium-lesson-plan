# CourseAgent V1.0 实施计划

版本：V1.0（实施准备稿）    日期：2026-08-01
状态：等待人工确认；本文件只制定计划，不修改任何代码
依据：AGENTS.md；《CourseAgent_V1.0升级架构设计.md》

## 一、实施原则

1. 保留现有Workflow：既有流程与模块不重构、不推翻。
2. 新增优先：V1.0先“只新增、默认关闭”，避免影响现有路径。
3. 每步可回滚：每阶段有独立开关与回滚方案。
4. 每步必须测试：每个阶段完成即跑自动化测试，未通过不进入下一阶段。

## 二、阶段任务拆解

### 阶段0：架构确认

- 目标：设计文档与实施计划经人工确认。
- 涉及文件：docs/CourseAgent_V1.0升级架构设计.md、docs/CourseAgent_V1.0实施计划.md。
- 新增文件：无。
- 修改文件：无。
- 修改原因：无。
- 风险：低。
- 测试方案：人工评审确认单。
- 回滚方案：无需回滚。

### 阶段1：Model Adapter 基础层

- 目标：建立统一模型抽象层，默认关闭，不接入具体模型。
- 涉及文件：CourseAgent/models/、CourseAgent/config/models.yaml。
- 新增文件：models/base.py、models/registry.py、models/__init__.py、config/models.yaml、tests/test_model_adapter.py。
- 修改文件：无核心Workflow文件；仅新增入口（可选：在 README 增加说明）。
- 修改原因：无核心修改。
- 风险：低；依赖仅标准库与配置读取。
- 测试方案：单元测试（health_check 未配置返回 disabled；registry 注册/获取）。
- 回滚方案：删除 models/ 与 config/models.yaml 即可，现有流程不受影响。

### 阶段1.5：Task State 持久化

- 目标：任务ID、状态保存、断点恢复、运行日志。
- 涉及文件：CourseAgent/state/。
- 新增文件：state/store.py、state/__init__.py、tests/test_state.py。
- 修改文件：core/orchestrator.py（可选接入：默认不启用，配置开关）。
- 修改原因：为断点恢复与审计提供持久化底座。
- 风险：中；涉及Orchestrator可选接入点。
- 测试方案：创建任务→保存→读取→模拟断点续跑。
- 回滚方案：开关关闭后走原内存路径，删除 state 目录。

### 阶段2：DeepSeek 试点接入

- 目标：实现 DeepSeek Adapter，试点“需求理解增强”，默认关闭。
- 涉及文件：models/deepseek.py、config/models.yaml、core/translator.py（可选）。
- 新增文件：models/deepseek.py、tests/test_deepseek.py（mock模式）。
- 修改文件：core/translator.py 增加可选调用点（开关控制）。
- 修改原因：为语义需求理解提供试点。
- 风险：中；API密钥泄露、成本、输出不可控。
- 测试方案：mock模式单测；真实调用用最小请求+超时+回退规则。
- 回滚方案：关闭LLM开关，translator回到纯规则路径。

### 阶段3：Router 增强

- 目标：按任务类型/复杂度选择模型或规则，支持fallback。
- 涉及文件：router/。
- 新增文件：router/decision.py、router/__init__.py、tests/test_router.py。
- 修改文件：orchestrator/translator 调用点（可选）。
- 修改原因：把“模型/规则选择”集中管理。
- 风险：中；路由误判。
- 测试方案：构造简单/复杂/未知任务，验证路由与fallback。
- 回滚方案：路由开关关闭，直接走原规则路径。

### 阶段4：Memory 结构化

- 目标：在JSON之上增加索引与查询，保留现有存储。
- 涉及文件：memory/、core/memory.py。
- 新增文件：memory/index.py、tests/test_memory_index.py。
- 修改文件：core/memory.py（新增查询接口，向后兼容）。
- 修改原因：提升记忆检索效率，为语义检索预留。
- 风险：中；数据兼容。
- 测试方案：旧JSON可读，新索引可建可查，回归旧用例。
- 回滚方案：保留旧接口，索引目录可删除。

## 三、第一阶段详细实施方案（Model Adapter 基础层）

### 1. 目录结构

```text
CourseAgent/
├── models/
│   ├── __init__.py
│   ├── base.py          # ModelAdapter 抽象
│   └── registry.py      # 模型注册与获取
├── config/
│   └── models.yaml      # 模型配置（默认全部 disabled）
└── tests/
    └── test_model_adapter.py
```

### 2. 接口设计

```python
class ModelAdapter:
    def generate(self, prompt, system=None, **kwargs) -> str: ...
    def analyze(self, prompt, context=None, **kwargs) -> dict: ...
    def vision(self, image, prompt, **kwargs) -> str: ...   # 预留
    def embed(self, texts, **kwargs) -> list: ...           # 预留
    def health_check(self) -> dict: ...                     # enabled/status/latency

class ModelRegistry:
    def register(self, name, adapter): ...
    def get(self, name) -> ModelAdapter: ...
    def list(self) -> list: ...
```

约束：核心Agent只依赖 `ModelAdapter` 抽象与 `ModelRegistry`，不依赖具体模型。

### 3. 配置方式

`config/models.yaml` 设计：

```yaml
default_provider: ""
providers:
  deepseek:
    enabled: false
    model: deepseek-chat
    base_url: ""
    api_key_env: DEEPSEEK_API_KEY
    timeout: 30
```

密钥只从环境变量读取，不写入仓库。

### 4. 测试方式

- 未配置：health_check 返回 disabled，registry 可注册/获取。
- 配置后（mock）：generate 返回固定文本、analyze 返回结构化 dict。
- 回归：现有脚本（batch_score、selfcheck）运行结果不变。

## 四、实施前检查清单

- [ ] AGENTS.md 约束满足：先三审，小步实施，偏离即纠错。
- [ ] 不破坏现有流程：阶段1只新增，默认关闭。
- [ ] 不引入无必要依赖：阶段1仅标准库+pyyaml（已有）。
- [ ] 不泄露API密钥：密钥仅环境变量，config不写真实密钥，.gitignore覆盖。
- [ ] 有测试验证：每阶段配套tests与回归。

## 五、下一步

等待人工确认本实施计划后，从阶段1（Model Adapter基础层）开始，按“小步实施→自动测试→经验沉淀”推进。
