---
name: vision_quality_check
description: 基于视觉识别的模板结构检查生成结果一致性，输出结构化JSON，用于课程文档生成质量校验。
---

# Vision Quality Check Skill

## 能力

- 必需模板段落检查；
- 版式约束提示；
- 生成结果一致性评分。

## 输出

```json
{
  "ok": true,
  "issues": [],
  "score": 1.0,
  "skill": "vision_quality_check"
}
```