# 课程文档智能体生产规范 V1.0（Smart Course Document Agent）

## 一、多智能体分工

- Planner：任务分析、步骤、风险、检测标准；
- Executor：模板解析、内容重构、文档生成；
- Reviewer：教学质量与文档质量量化评分；
- Learner：失败总结、规则更新、经验沉淀。

## 二、质量评分

综合质量 = 模板符合度30% + 内容完整度25% + 教学专业度25% + 格式规范度20%；≥95 输出最终版本，否则进入修复循环（最多3次）。

## 三、自动循环

generate → check → score ≥95 ? break : analyze_error + repair。

## 四、企业级输出

01_最终文件 / 02_检测报告 / 03_过程记录 / 04_Agent成长记录。

## 五、思考外显与学习

工作日志、决策日志、反思日志；Agent_Memory（success/failure/rules/optimization），任务完成后更新并下次自动调用。

## 六、可执行项目

`课程材料优化/CourseAgent`：main.py、agents/、modules/、config/agent_rules.yaml、memory/、input/output/reports。
