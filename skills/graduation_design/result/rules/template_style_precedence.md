# Template Style Precedence Rule

## 1. 规则目的

解决 Result 成果生成过程中，AI 初稿字符级 Run 格式污染黄金模板样式的问题。

背景：

- v1.2 版本发现 Heading 标题被 Arial 8/10pt 覆盖；
- 正文存在微软雅黑 16pt 等来源格式残留；
- 参考文献出现 Segoe UI 等非模板字体。

根因：

ContentAdapter 迁移内容时同时迁移了源文档格式。

---

## 2. 核心原则

必须遵循：

```text
模板样式 > Skill规则 > 内容来源样式
```

定义：

- 内容来源：只提供语义内容；
- 黄金模板：提供全部视觉属性。

---

## 3. 内容迁移边界

允许迁移：

- 文本内容；
- 章节关系；
- 语义结构。

禁止迁移：

- font；
- size；
- bold；
- italic；
- underline；
- color；
- 字符 Run 属性；
- 段落格式；
- 原始样式引用。

---

## 4. 区域规则

### 标题

Heading1 / Heading2 / Heading3 必须继承模板样式。

### 正文

Normal 必须继承模板正文样式。

### 表格

保持模板表格 DNA，只替换内容。

### 参考文献

统一：

- 模板字体；
- 模板字号；
- 悬挂缩进 0.74cm。

---

## 5. 验证规则

生成成果后必须检查：

Template Compliance：

- 标题样式；
- 正文样式；
- 表格样式；
- 参考文献格式。

Style Integrity：

- Run 级字体污染；
- 非模板字体；
- 样式覆盖。

---

## 6. 适用范围

适用于：

```text
skills/graduation_design/result
```

不影响：

- TaskBook Skill；
- Evaluation Skill；
- Defense Skill。
