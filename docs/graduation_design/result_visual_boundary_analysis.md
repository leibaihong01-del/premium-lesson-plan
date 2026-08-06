# Result 视觉边界分析

时间：2026-08-06
性质：只读分析，不修改代码

## 一、当前生产链

```text
黄金模板
    ↓
TemplateInstanceBuilder（复制 + 字段替换）
    ↓
ContentAdapter（内容迁移 + 样式继承后处理）
    ↓
Visual Baseline 检查
    ↓
输出
```

## 二、样式控制位置

| 位置 | 当前行为 |
|---|---|
| 黄金模板 styles.xml | 定义全部样式（Heading/正文内容/表注/参考文献） |
| TemplateInstanceBuilder | 文件级复制，保留样式、分节、表格样式 |
| ContentAdapter | 插入内容元素；显式重赋 run 字体字号加粗；保留 AI 段落格式 |
| 后处理 | 清除 run rPr 后显式设置 黑体/宋体/Times + 字号 + 首行缩进 |

## 三、ContentAdapter 越权点

1. 显式设置 run 字体、字号、加粗（视觉重建）；
2. 保留 AI 初稿段落格式（行距、段前段后、首行缩进等 pPr）；
3. 内容表格表头显式宋体 12 加粗（来源格式残留）。

## 四、推荐修正方案

生产链调整为：

```text
黄金模板
    ↓
TemplateInstanceBuilder
    ↓
模板实例
    ↓
ContentAdapter（只迁移内容）
    ↓
Visual Baseline 检查
    ↓
输出
```

ContentAdapter 边界：

- 只负责选择内容元素与章节槽位；
- 清除来源 rPr / pPr 格式；
- 禁止设置 font / size / bold / color / line / indent；
- 所有视觉属性由模板样式继承。

## 五、约束

- 不新建模板；
- 不放弃 v0.2；
- 不新增视觉规则；
- 不修改黄金模板；
- 不修改已验证基线。

## ??证据（来自只读对比）

- A（v0.2基准）：标题 / 正文 / 参考文献运行属性全部继承模板（无显式字体 / 字号 / 行距）；
- B（邱志豪）：标题显式黑体16/15pt加粗；正文 firstLineChars 200/480；行距 300 atLeast；参考文献 12pt + 悬挂420；
- 结论：B的显式格式与A的模板继承格式存在层级差异，即ContentAdapter越权点。
