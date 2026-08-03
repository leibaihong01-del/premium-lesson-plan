# content_check（成果内容合规执行层）

- 规则来源：`../school_rules/content_rules.json`
- 不维护独立违禁词库
- 区域控制：封面/承诺页/参考文献 ignore；摘要/正文/总结/附录 check
- 三级判断：forbidden（明确违规）、warning（疑似）、allowed（参考文献允许）
- 输出：位置 / 区域 / 级别 / 原文 / 是否违规 / 建议 / 学校规则依据
