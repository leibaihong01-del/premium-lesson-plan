# Experience Usage Audit（经验真实性审计）

版本：0.7-eil-audit-v1
状态：设计稿

## 一、审计目标

确认每条经验：

1. 是否存在；
2. 是否被加载；
3. 是否被使用；
4. 是否影响结果。

## 二、审计规则

- 生成报告中的经验声明必须能在 experience_trace.json 找到；
- experience_loaded 为空或与声明不一致时，审计判为 fail；
- 审计 fail 的成果不得进入交付目录；
- Trace 必须由代码写入，不允许手工声明。

## 三、输出

`experience_usage_report.md`

示例：

```markdown
# Experience Usage Report

| 经验 | 来源文件 | 存在 | 加载 | 使用 | 影响 |
|---|---|---|---|---|---|
| reference_format_001 | result/memory/reference_quality_experience.json | 是 | 是 | 是 | 参考文献悬挂缩进检查 |
| result_quality_memory | result_quality_memory.json | 是 | 是 | 是 | 章节规划约束 |

结论：全部真实调用，无伪调用。
```