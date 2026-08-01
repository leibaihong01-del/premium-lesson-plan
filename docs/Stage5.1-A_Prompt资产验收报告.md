# Stage5.1-A Prompt 资产验收报告

日期：2026-08-02    阶段：5.1-A（仅建立Prompt资产目录）    状态：验收通过，等待人工确认

## 一、新增文件

| 文件 | 职责 |
|---|---|
| prompts/manifest.yaml | Prompt 资产清单：id、版本、用途、路径、兼容模型、变更日志 |
| prompts/translator/system.md | 需求转译系统 Prompt：角色、输出JSON契约、约束 |
| prompts/translator/user_template.json | 用户 Prompt 模板：占位符与输出Schema |

另按本次新增架构原则，在 AGENTS.md 追加“任务生命周期数据治理原则”。

## 二、文件职责

- manifest.yaml：Prompt 注册与版本入口，供后续接入时按 id 加载；
- system.md：约束模型行为，保证输出契约稳定；
- user_template.json：格式化用户需求与画像，作为可复用模板。

## 三、版本管理方式

- 每个 prompt 独立版本号（当前 v1.0）；
- 变更必须升版本并在 manifest 的 change_log 记录原因；
- 后续 evaluation 报告按 prompt 版本归档，保证可回归。

## 四、后续接入方式

- 阶段5.1-B：建立 evaluation 评测集与指标；
- 阶段5.2：跑“规则基线”评测；
- 阶段5.3：接入 DeepSeek，用同一 Prompt 版本与评测集对比；
- 指标达标且成本受控才允许上线，否则保持规则路径。

## 五、测试结果（结构检查）

| 检查项 | 结果 |
|---|---|
| manifest.yaml 含 id/path/version | PASS |
| translator/system.md 路径存在 | PASS |
| translator/user_template.json 路径存在 | PASS |
| user_template.json 可解析且占位符完整 | PASS |
| system.md 非空 | PASS |
| 合计 | 5/5 PASS |

说明：当前运行环境缺少 pyyaml，manifest.yaml 采用无依赖结构检查（正则校验 id/path/version），后续在可用环境中补充 YAML 完整解析验证。

## 六、结论

阶段5.1-A 完成：Prompt 资产目录已建立，未接入模型、未修改 translator/orchestrator、未改动现有 Workflow、未创建 evaluation 代码。
