# 阶段总结与 Skill 沉淀报告

日期：2026-08-02
基线：v1.0-baseline（Git 标签已建立）

## 一、本次成果

- MiMo Vision 真实 API 接入成功（OpenAI Compatible /chat/completions）；
- 图片文字识别验证成功（OCR 结构化 JSON）；
- 《城市轨道交通概论》第2课按 39x6 模板格式重新产出，v2 文件完成，质量 PASS 100；
- run_agent.py 文件输入/输出式工作系统框架建立；
- JSON 编码治理完成（UTF-8 无 BOM + utf-8-sig 加载层）；
- 23 个测试全部通过，v1.0-baseline 冻结。

## 二、不足与教训

1. format/content checker 硬编码 39x6 实训模板，跨模板会 IndexError；
2. --profile auto 缺陷导致 KeyError，迫使强制 high，浪费算力；
3. MiMo 端点不是 /vision/analyze，需按 /chat/completions 适配；
4. 模型返回 Markdown 包裹 JSON，需要提取解析；
5. JSON BOM 会导致 json.load 失败；
6. 阶段边界曾被提前越过，已沉淀为 E-016 阶段边界保护规则。

## 三、亮点

- review_cache 命中：文档评审 0.48 秒完成，零重复检测；
- 自适应路由修复：auto 按复杂度选档，默认不再强制 high；
- 真实视觉链路：图片 → MiMo → Schema → Context → Consistency 全通；
- 全量测试 23/23，3.49 秒完成。

## 四、Token 优化措施

- profile auto 自适应计算档位；
- review_cache 缓存复用；
- run_agent 默认 auto；
- 编码统一 utf-8-sig，避免 BOM 报错重试；
- 每任务结束清理无用文件，避免无关数据进入上下文。

## 五、Skill 沉淀

- 新增 skills/agent_evolution/SKILL.md：自主进化闭环；
- memory/system/lessons_learned.json：追加 6 条经验；
- memory/improvements.json：追加 4 条改进建议；
- 规则沉淀沿用 memory/system/rules.json 与 E-016 阶段边界保护。

## 六、清理清单

- 已清理：__pycache__、.pytest_cache、无用临时中间产物；
- 保留：CourseAgent 项目、config、Memory、Skill、MigrationLogs、验收报告、关键备份。

## 七、性能数据

| 项目 | 指标 |
|---|---|
| 全量测试 | 23/23 通过，3.49s |
| 文档评审（缓存命中） | 0.48s，PASS 100 |
| MiMo OCR 单图 | 约 5.7s，ok=true |
| 第2课 v2 产出 | 39x6，55716 字节 |

## 八、下一阶段

- 主线：Agent Workspace 系统（放文件 → 运行 → 取结果）；
- 业务：毕业设计辅助（任务书、答辩记录表、指导记录、成果文档规范化）；
- 约束：不扩展 Vision 开发，保持 v1.0 稳定，逐步沉淀经验。