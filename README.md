# CourseAgent 课程文档智能体

产品级文档生产智能体框架：规划 → 生成 → 检测 → 修复 → 打包 → 复盘 → 记忆。

## 结构

```text
CourseAgent/
├── main.py                  # 总控制器
├── agents/                  # Planner / Writer / Reviewer / Learner
├── modules/                 # 模板解析、文档生成、格式/内容检测、打包
├── config/agent_rules.yaml  # 工作规则（最低分95、权重、修复循环）
├── memory/                  # 成功/失败/规则更新/改进建议记忆
├── input/                   # 原始教案 + 模板 + fills.json
├── output/                  # 01_最终文件/02_检测报告/03_过程记录/04_Agent成长记录
└── reports/                 # plan/template_structure/quality_report/reflection
```

## 运行

评审已生成文件：

```bash
python main.py --template 模板.docx --existing 教案.docx --project 课程A --title "城市轨道交通概论课程教案"
```

按 fills.json 生成并评审：

```bash
python main.py --template 模板.docx --fills input/fills.json --project 课程A --kind lesson --title "城市轨道交通概论课程教案"
```

实训教案加 `--kind practice`（自动启用反思区跨页保护）。

## 质量闭环

综合质量 = 模板符合度30% + 内容完整度25% + 教学专业度25% + 格式规范度20%。
低于95分自动进入修复循环（最多3次），达标才打包输出。

## 运行时优化（低算力）

- 模板结构缓存：`reports/template_structure.json`。
- 评分结果缓存：`reports/review_cache.json`，按“文件哈希+模板哈希”复用；文件未变化且上次 PASS 直接跳过检测。
- 修复动作记忆：`memory/repair_actions.json` 记录已用修复动作及次数。
- 批量复用：`batch_score.py` 二次运行直接命中缓存（16份文件约0.5秒完成）。

## 自主迭代

`agents/learner.py` 每次运行写入 success/failure/improvements/rule_update；同一改进建议出现 ≥2 次自动沉淀为规则，形成“执行→检测→修复→学习→规则更新”闭环。

## 自适应算力调度

- `agents/router_agent.py`：路由Agent，先查决策缓存，再按复杂度分档。
- `modules/fast_classifier.py`：零/低Token规则判断（文件、表格、页数、质量关键词）。
- `modules/escalation.py`：渐进升级（同类失败≥2次升档，连续5次达标尝试降档）。
- `memory/task_patterns.json`：任务指纹 → 历史决策缓存，相似任务直接复用。
- 低/中/高对应修复循环 1/2/3 轮；`--profile auto` 自动判断，也可 `--profile low|medium|high` 强制指定。
- `agents/light_judge.py`：置信度不足时的第二层轻量判断。
- `modules/visual_checker.py`：高算力档 PDF 视觉检查（页数、空白尾页、越界、底部空白），`--profile high --pdf xxx.pdf` 启用。

## 核心底座（优秀高职教师智能体）

- `core/orchestrator.py`：总控状态机（TRANSLATED→…→DONE）与最小文档闭环。
- `core/translator.py`：需求转译，自然语言 → TaskSpec（意图/领域/质量/约束/置信度）。
- `core/memory.py`：统一记忆系统（任务/决策/规则/成败/用户偏好/问题方案）。
- `core/evolution.py`：自我进化（问题分类、方案、可控升级 L1/L2/L3、成长评分）。
- `core/problem_solver.py`：问题解决Agent（候选方案、择优、验证计划）。
- `core/intent_alignment.py`：满意度预测（文字要求+隐含目标+优秀教师标准）。
- `core/knowledge_update.py`：知识更新Agent（来源登记、导入、影响分析、规则建议）。
- `core/excellence_engine.py`：精品课程五维诊断（教学逻辑/内容体系/职业特色/创新设计/评价体系）。
- `batch_excellence.py`：16份教案五维诊断与《精品提升建议报告》。
- `capabilities/`：Phase 4 教师能力模块（competition/research/achievements），样例见 `output/Phase4样例/`。
- `core/user_model.py`：用户理解模型，从任务与反馈沉淀偏好。
- `tools/agent_selfcheck.py`：Agent自检，输出 `output/Agent成长报告.md`（能力状态、记忆统计、成长评分）。
- `tools/upgrade_review.py`：L2/L3升级审核，输出 `output/升级审核报告.md`。
- `tools/upgrade_verify.py`：L2规则按知识更新证据自动验证，输出 `output/升级验证报告.md`。
- `tools/upgrade_approve.py`：L3升级人工审批（list/approve/reject），输出 `output/升级审批记录.md`。
- `tools/knowledge_monitor.py`：知识来源联网监测，网络不可用时自动降级离线导入，输出 `output/知识监测状态报告.md`。
- `tools/user_profile_report.py`：用户画像报告，输出 `output/用户画像报告.md`。
- `core/skill.py`：Skill六件套抽象（执行/评价/反思/优化/经验/进化）与注册表；`tools/skill_demo.py` 冒烟示例。
- `core/skill_factory.py` + `tools/skill_audit.py`：默认注册教学资源/文件/分析/竞赛/科研/成果/知识7个Skill并审计。
- 说明：Skill注册表是应用内能力清单（Python字典 + memory JSON），与Windows系统注册表无关，不会读写注册表。
- Orchestrator 支持 `run_capability`，统一调度竞赛/教研/成果生成并纳入满意度预测与记忆。
- 设计文档见 `docs/`：01 现状分析与复用评估、02 系统架构设计V1.0、03 开发路线图V1.0。
