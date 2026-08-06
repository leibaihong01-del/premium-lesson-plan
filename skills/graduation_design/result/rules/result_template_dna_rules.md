# Result 模板 DNA 保护规则

## 一、模板实例化优先原则

Result 生产必须遵循：

```text
黄金模板复制
    ↓
字段替换
    ↓
内容迁移
    ↓
格式检查
```

## 二、禁止

- 重新构造 Word 结构；
- 搬移封面段落；
- 修改目录结构；
- 修改 Heading 层级；
- 强制覆盖模板字体；
- 新增分节。

## 三、允许

- 学生信息替换；
- 正文内容填充；
- 内容质量优化。

## 四、阶段拆分

```text
ResultPipeline
├── TemplateInstanceBuilder：黄金模板实例化
└── ContentAdapter：学生内容迁移
```
