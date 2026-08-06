# Template Style Precedence Rules（模板样式优先规则）

## 一、问题背景

Run 级格式污染导致模板样式失效：

- 标题被 AI 初稿 Arial 8/10pt 覆盖；
- 参考文献被 Segoe UI 7.5pt 覆盖；
- 正文存在源格式残留。

## 二、核心原则

```text
模板样式 > 内容来源样式
```

## 三、输入输出边界

输入资料：

- 仅提供文本内容；
- 仅提供语义结构。

黄金模板：

- 提供全部视觉属性（页面、样式、字体、标题层级、表格、参考文献）。

## 四、禁止迁移

从内容来源迁移时禁止携带：

- font；
- size；
- bold；
- italic；
- color；
- underline；
- paragraph formatting。

## 五、适用范围

- 标题；
- 正文；
- 表格；
- 参考文献。

## 六、执行方式

迁移文本后清除源 run 格式，由模板重新赋予：

- Heading 样式；
- Normal 样式；
- 表格样式；
- 参考文献格式。
