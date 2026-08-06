# ResultPipeline 拆分架构经验

时间：2026-08-05
性质：架构经验候选，不修改 Skill

## 背景

Result baseline 发现模板 DNA 被破坏，根因是模板实例化与学生内容迁移混在一个阶段，`_transplant_cover` 等步骤有机会覆盖模板封面。

## 结论

Result 以后应拆成两个阶段：

```text
ResultPipeline
├── 阶段 1：TemplateInstanceBuilder（黄金模板实例化）
└── 阶段 2：ContentAdapter（学生内容迁移）
```

## 正确方向

```text
杨振海成果.docx
        ↓
王欢成果实例.docx（模板 DNA 完整）
        ↓
填充正文
```

而不是：

```text
杨振海成果.docx + 王欢资料 + AI初稿
        ↓
重新拼 Word
```

## 约束

- 阶段 1 只做字段替换，不插入正文、不移植封面、不强制字体、不增分节；
- 阶段 2 只做内容迁移，必须保留阶段 1 的模板 DNA。
