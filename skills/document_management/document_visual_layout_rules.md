# 文档视觉布局规则（Document Visual Layout Rules）

版本：1.0
适用范围：目录、表格、表注、标题等元素之间的视觉关系验收。

## 一、定位

不再只检查“格式是否正确”，而是检查“元素之间的视觉关系是否符合人工审稿标准”。

最终验收 = DOCX 结构检查 + PDF 视觉检查。

## 二、表格版式规则

### 1. 表格宽度

- 不固定某个列宽值；
- 表格总宽度优先适配页面有效宽度（版心宽度）；
- 避免表格过窄导致表头折行、内容挤压、空白区域过大；
- 原则：页面利用率优先，内容可读性优先。

### 2. 表注格式

- 正确格式：`表4.1  表名称`；
- 编号与名称之间使用两个空格；
- 编号格式保持 `X.X`（4.1、4.2、5.1）；
- 禁止 `表4-1  ××××`；
- 禁止 `表4.1 ××××`（单空格）。

### 3. 表注与表格绑定

- 表注、表格首行、表格内容属于一个视觉单元；
- 表注必须紧贴表格；
- 表注与表格之间不得出现空白段落；
- 不允许表注单独留在上一页；
- 不允许表注和对应表格分离。

### 4. 表与表之间间距

- 表注必须贴近对应表格；
- 表与表之间允许通过段落间距或空行形成视觉分隔；
- 空行的目的是让下一个表注靠近自己的表格，不是错误。

## 三、配置（草案）

```yaml
table_layout:
  width:
    adaptive_to_page: true
    prioritize_readability: true

  caption:
    format: "表X.X  表名称"
    separator_spaces: 2
    keep_with_table: true

  spacing:
    caption_to_table: 0
    between_tables:
      allow_visual_spacing: true
      avoid_caption_detachment: true

  header:
    short_title_single_line: true
    optimize_column_width_first: true
```

## 四、验收

- 表头单行、无拆行；
- 表注格式统一、与表格紧贴；
- 表格宽度适配页面、无溢出；
- 目录、表格、表注、标题的视觉关系符合人工审稿标准。
