---
name: agent_evolution
description: 自主进化Skill：每次任务结束后总结不足与亮点、沉淀经验规则、清理无用文件、优化token与性能，形成执行→检测→总结→沉淀→优化闭环。
---

# Agent Evolution Skill

## 闭环

1. 任务执行；
2. 结果检测；
3. 错误发现与原因分析；
4. 经验沉淀（lessons_learned / improvements）；
5. 规则与 Skill 更新；
6. 无用文件清理；
7. Token 与性能优化；
8. 下次任务应用。

## 每任务结束清单

- 总结不足与亮点；
- 记录经验到 memory/system/lessons_learned.json；
- 记录改进建议到 memory/improvements.json；
- 更新或新增 Skill；
- 清理 __pycache__、临时文件、无用中间产物；
- 记录性能与 token 指标。