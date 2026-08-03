# 双版本交付机制（Dual Version Delivery）

毕业设计类 Skill 默认机制。

## 目录结构

```text
V0.3_<学生><文档类型>验证/
├── AI版本/
│   ├── 01 学生姓名 文档类型_AI生成版.docx
│   └── version.json
└── 人工版本/
    ├── 01 学生姓名 文档类型_人工修订版.docx
    └── version.json
```

## 元数据

AI版本 version.json：

```json
{
  "skill": "result",
  "generation_version": "v0.1",
  "document_type": "graduation_design_result",
  "origin": "ai_generated",
  "review_status": "pending"
}
```

人工版本 version.json：

```json
{
  "skill": "result",
  "generation_version": "v0.1",
  "document_type": "graduation_design_result",
  "origin": "human_reviewed",
  "review_status": "completed"
}
```

## 原则

- AI 版本是原始样本，保存 AI 思考轨迹，禁止被人工修改覆盖；
- 人工直接在人工版本上修改；
- 差异分析基于 AI 版本 vs 人工版本；
- 该机制适用于任务书、成果、开题报告、答辩、成绩评定等所有毕业设计类 Skill。
