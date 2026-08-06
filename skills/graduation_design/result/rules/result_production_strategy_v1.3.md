# Result 毕业成果唯一生产策略 v1.3

状态：唯一毕业成果输出方式

## 一、生产链

```text
StudentProfile
    ↓
TemplateInstanceBuilder（黄金模板复制 + 字段替换）
    ↓
ContentAdapter（只迁移内容，清除来源 rPr/pPr，保留 pStyle）
    ↓
DocumentFinalizer（Word 更新 TOC/PAGE 域）
    ↓
RegressionValidator（三 DNA 对比杨/王 v0.2 基准）
    ↓
Output
    ↓
Memory
```

## 二、视觉 DNA 规则（对齐杨/王）

1. 标题：序号后两个空格 + 文字；一级两字标题中间两个空格（如 `1  引  言`）；
2. 正文/表格：清除来源 run 格式，继承模板样式；
3. 参考文献：自动编号（numId=1，lvlText=[%1]）+ 悬挂缩进 420/420（0.74cm）；
4. 目录：Word 更新 TOC/页码，最终化。

## 三、编号定义

参考文献编号定义从黄金模板复制 `numbering.xml`（numId=1，lvlText=[%1]）。

## 四、验证

回归验证以三项 DNA 为准：

- Structural DNA；
- Visual DNA；
- Delivery DNA。

页数仅记录，不作为通过依据。

## 五、版本追踪

每次生产记录：

- Skill 版本；
- Runner 入口；
- 模板版本；
- Baseline 版本；
- 规则文件；
- 生成时间。

## 六、约束

- 不修改黄金模板；
- 不删除 v0.2 基准；
- 不新增其他成果生产路径。

## ??表格规则（小修正）

- 内容表格统一边框与单元格边距?
- 表格内容：五号?10.5pt?Times New Roman / 宋体?水平居中 + 垂直居中?
- 表注与表格首行同页?keepNext??
- 目录：单一TOC域?不重复?

## ??表格整体规则（对齐杨/王）

- 宽度：4998 pct?
- 布局：autofit?
- 缩进：0 dxa?
- 边框：单元格四边单线4?
- 表头：加粗?
