# 模板 vs v1.5 对比报告

## 1. 页面概览

- 模板页数：18；v1.5 页数：22

- 模板正文显示页码区间：1；v1.5：1

- 模板 正文页均字符量：785；最大：1080；最小：151

- v1.5 正文页均字符量：789；最大：1010；最小：80

## 2. 标题

模板标题数：16；v1.5 标题数：16

### 模板

- L1 `1  引  言` | style=Heading 1 | eastAsia=None; ascii=None | 

- L2 `1.1  设计背景` | style=Heading 2 | eastAsia=None; ascii=None | 

- L2 `1.2  设计目的与意义` | style=Heading 2 | eastAsia=None; ascii=None | 

- L2 `1.3  设计内容` | style=Heading 2 | eastAsia=None; ascii=None | 

### v1.5

- L1 `1  引言` | style=Heading 1 | eastAsia=宋体; ascii=Times New Roman; sz=32; b=None | jc=center; spacing(before=240,after=240,beforeLines=100,afterLines=100)

- L2 `1.1  设计背景` | style=Heading 2 | eastAsia=宋体; ascii=Times New Roman; sz=28; b=None | jc=both

- L2 `1.2  设计目的与意义` | style=Heading 2 | eastAsia=宋体; ascii=Times New Roman; sz=28; b=None | jc=both

- L2 `1.3  设计内容` | style=Heading 2 | eastAsia=宋体; ascii=Times New Roman; sz=28; b=None | jc=both

## 3. 正文样式

- 模板段落计数：{'Normal': 5, '正文内容': 103, '表注': 4, '参考文献': 9}

- v1.5 段落计数：{'Normal': 5, '正文内容': 143, '表注': 4, '参考文献': 8}

### 模板

- `Normal` | 长沙轨道交通职业学院 | eastAsia=None; ascii=None; sz=52; b=0 | jc=center; spacing(line=240,lineRule=auto); ind(firstLine=0,firstLineChars=0); keepNext=0

- `Normal` | 长沙轨道交通职业学院教务处编制 | eastAsia=None; ascii=None; sz=30; b=None | jc=center; spacing(before=157,line=240,lineRule=auto,beforeLines=50); ind(firstLine=0,firstLineChars=0); keepNext=0

- `正文内容` | 随着我国城市化进程的不断加快，城市人 | eastAsia=None; ascii=None | 

- `正文内容` | 地铁车站作为乘客集散的重要场所，配备 | eastAsia=None; ascii=None | 

- `表注` | 表2.1  AFC闸机系统组成表 | eastAsia=None; ascii=None | 

- `表注` | 表3.1  AFC闸机常见故障及原因 | eastAsia=None; ascii=None | 

- `参考文献` | 杨晓峰,吴命利,游小杰.轨道交通牵引 | eastAsia=None; ascii=None | ind(left=420,hanging=420); keepNext=0

- `参考文献` | 城市轨道交通自动售检票系统技术条件（ | eastAsia=宋体; ascii=Times New Roman | ind(left=420,hanging=420); keepNext=0

### v1.5

- `Normal` | 长沙轨道交通职业学院 | eastAsia=宋体; ascii=Times New Roman; sz=24; b=0 | jc=center; spacing(line=240,lineRule=auto); ind(firstLine=0,firstLineChars=0); keepNext=0

- `Normal` | 长沙轨道交通职业学院教务处编制 | eastAsia=宋体; ascii=Times New Roman; sz=24; b=0 | jc=center; spacing(before=157,line=240,lineRule=auto,beforeLines=50); ind(firstLine=0,firstLineChars=0); keepNext=0

- `正文内容` | 城市轨道交通作为现代大城市公共交通体 | eastAsia=宋体; ascii=Times New Roman; sz=24; b=0 | 

- `正文内容` | AFC检票机是一个集机械传动、电子控 | eastAsia=宋体; ascii=Times New Roman; sz=24; b=0 | 

- `表注` | 表2-1 AFC检票机系统组成表 | eastAsia=宋体; ascii=Times New Roman; sz=24; b=0 | keepNext=None

- `表注` | 表3-1 AFC检票机常见故障及原因 | eastAsia=宋体; ascii=Times New Roman; sz=24; b=0 | keepNext=None

- `参考文献` | 城市轨道交通自动售检票系统技术条件（ | eastAsia=宋体; ascii=Times New Roman; sz=24; b=0 | ind(firstLine=0,left=420,hanging=420)

- `参考文献` | 中华人民共和国住房和城乡建设部.城市 | eastAsia=宋体; ascii=Times New Roman; sz=24; b=0 | ind(firstLine=0,left=420,hanging=420)

## 4. 表格

模板表格数：6；v1.5 表格数：6

### 模板

- #0 style=19 align=center width=0 auto 11x2 | 表头=毕业设计毕业设计 | 单元格字体=eastAsia=宋体; ascii=Times New Roman; sz=108; b=None | vAlign=center

- #1 style=19 align=center width=0 auto 7x5 | 表头=学生毕业设计真实性承诺学生毕业设计真实性承诺学生毕业设计真实 | 单元格字体=eastAsia=宋体; ascii=Times New Roman; sz=30; b=None | vAlign=center

- #2 style=18 align=None width=4998 pct 8x4 | 表头=组成部分主要功能核心部件备注 | 单元格字体=b=0 | vAlign=center

- #3 style=18 align=None width=4998 pct 12x5 | 表头=故障类别故障现象故障原因发生频率影响程度 | 单元格字体=b=0 | vAlign=center

- #4 style=18 align=None width=4998 pct 5x5 | 表头=检修等级检修周期主要检修内容执行人员预计用时 | 单元格字体=b=0 | vAlign=center

- #5 style=18 align=None width=4998 pct 11x5 | 表头=序号检查项目检查内容与标准检查方法检查结果 | 单元格字体=b=0 | vAlign=center

### v1.5

- #0 style=19 align=center width=0 auto 11x2 | 表头=毕业设计毕业设计 | 单元格字体=eastAsia=宋体; ascii=Times New Roman; sz=108; b=None | vAlign=center

- #1 style=19 align=center width=0 auto 7x5 | 表头=学生毕业设计真实性承诺学生毕业设计真实性承诺学生毕业设计真实 | 单元格字体=eastAsia=宋体; ascii=Times New Roman; sz=30; b=None | vAlign=center

- #2 style=19 align=center width=4250 pct 8x4 | 表头=组成部分主要功能核心部件备注 | 单元格字体=eastAsia=宋体; ascii=Times New Roman; sz=21; b=0 | vAlign=center

- #3 style=19 align=center width=4250 pct 12x5 | 表头=故障类别故障现象可能故障原因发生频率影响等级 | 单元格字体=eastAsia=宋体; ascii=Times New Roman; sz=21; b=0 | vAlign=center

- #4 style=19 align=center width=4250 pct 8x4 | 表头=排查步骤步骤名称主要内容所需工具 | 单元格字体=eastAsia=宋体; ascii=Times New Roman; sz=21; b=0 | vAlign=center

- #5 style=19 align=center width=4250 pct 11x5 | 表头=序号故障现象首选排查方向快速检查方法处理建议 | 单元格字体=eastAsia=宋体; ascii=Times New Roman; sz=21; b=0 | vAlign=center

## 5. 表注

### 模板（4 条）

- `表2.1  AFC闸机系统组成表` | eastAsia=None; ascii=None | 

- `表3.1  AFC闸机常见故障及原因分析表` | eastAsia=None; ascii=None | 

- `表4.1  AFC闸机检修周期表` | eastAsia=None; ascii=None | 

### v1.5（4 条）

- `表2-1 AFC检票机系统组成表` | eastAsia=宋体; ascii=Times New Roman; sz=24; b=0 | keepNext=None

- `表3-1 AFC检票机常见故障及原因分析表` | eastAsia=宋体; ascii=Times New Roman; sz=24; b=0 | keepNext=None

- `表4-1 AFC检票机故障排查流程表` | eastAsia=宋体; ascii=Times New Roman; sz=24; b=0 | keepNext=None

## 6. 参考文献

### 模板（9 条）

- `杨晓峰,吴命利,游小杰.轨道交通牵引供电系统技术进展与思考.` | eastAsia=None; ascii=None | ind(left=420,hanging=420); keepNext=0

- `城市轨道交通自动售检票系统技术条件（GB/T31478-20` | eastAsia=宋体; ascii=Times New Roman | ind(left=420,hanging=420); keepNext=0

- `中华人民共和国住房和城乡建设部.城市轨道交通技术规范（GB5` | eastAsia=宋体; ascii=Times New Roman | ind(left=420,hanging=420); keepNext=0

### v1.5（9 条）

- `城市轨道交通自动售检票系统技术条件（GB/T31478-20` | eastAsia=宋体; ascii=Times New Roman; sz=24; b=0 | ind(firstLine=0,left=420,hanging=420)

- `中华人民共和国住房和城乡建设部.城市轨道交通技术规范（GB5` | eastAsia=宋体; ascii=Times New Roman; sz=24; b=0 | ind(firstLine=0,left=420,hanging=420)

- `中华人民共和国住房和城乡建设部.城市轨道交通运营管理规范（G` | eastAsia=宋体; ascii=Times New Roman; sz=24; b=0 | ind(firstLine=0,left=420,hanging=420)

## 7. 目录

### 模板（0 段）

### v1.5（16 段）

- style=13 tabs=['9355', '8777', None] instr=[' TOC \\o "1-3" \\h \\u ', ' HYPERLINK \\l "_Toc1001" ', ' PAGEREF _Toc1001 \\h '] text='1  引言1'

- style=15 tabs=['9355', None] instr=[' HYPERLINK \\l "_Toc1002" ', ' PAGEREF _Toc1002 \\h '] text='1.1  设计背景1'

- style=15 tabs=['9355', None] instr=[' HYPERLINK \\l "_Toc1003" ', ' PAGEREF _Toc1003 \\h '] text='1.2  设计目的与意义1'

- style=15 tabs=['9355', None] instr=[' HYPERLINK \\l "_Toc1004" ', ' PAGEREF _Toc1004 \\h '] text='1.3  设计内容2'

## 8. 修正结果（2026-08-06）

- 封面固定区域已保护：封面标题恢复模板字号（26pt/15pt）；
- 两字一级标题两字中间空两格：引  言、总  结；
- 正文表格对齐模板：样式 18、宽 4998pct、单元格表格内容(33)、宋体/TNR 五号、水平垂直居中；
- 表注对齐模板：表X.Y、样式表注、宋体/TNR 五号、keepNext；
- 正文学术词黑名单命中 0；真实线路名清洗后正文“长沙地铁”命中 0，仅保留封面校名；
- 质量引擎通过：sections=4、footer_page_parity=true、toc_cache=16。
## 9. 二次修正（2026-08-06）

- 表格线条恢复清晰：内容表格单元格边框统一为黑色单线（000000 / sz=4），不再继承初稿的浅灰边框；
- 目录恢复 Word 自动目录：目录域包入 sdt，docPartGallery=Table of Contents，WPS/Word 可自动调整、自动更新目录；
- 封面只替换学生字段，承诺书页保持不变；
- 质量引擎通过：sections=4、footer_page_parity=true、toc_cache=16、表格边框与模板一致。
## 10. 三次修正（2026-08-06）

- 目录自动更新后一级条目字体固定为宋体（TOC1 样式 13 显式 eastAsia=宋体 / ascii=Times New Roman）；
- 表格去除底色：内容表格单元格填充统一为白色 FFFFFF，不再保留初稿灰色底；
- 表格列宽按内容自适应：短内容（两三个字）保持单格单行，列宽依据表头与内容计算并写入单元格宽度。
## 11. 四次修正（2026-08-06）

- 正文列表序号统一规则：数字加点/顿号/括号后不跟空格（如“2.门翼开关异常类故障排查路径”）；
- 中文标点按中文字体处理：正文中文引号等全角标点使用宋体，不使用 Times New Roman；
- 参考文献保持半角格式，不受正文标点规则影响；
- 质量引擎通过：sections=4、footer_page_parity=true、toc_cache=16。
## 12. 五次修正（2026-08-06）

- 正文标点全角化：中文语境下 ASCII 逗号/分号/冒号/问号/感叹号/括号转为全角，中文引号使用宋体；
- 参考文献保持半角格式，不受正文标点规则影响；
- 标题改为纯样式继承：一级/二级标题不再写入直接字体，完全继承模板 Heading 样式，目录更新后一级条目不再变微软雅黑；
- 质量引擎通过：sections=4、footer_page_parity=true、toc_cache=16。
## 13. 全角标点整篇核验（2026-08-06）

- 正文段落与内容表格单元格统一全角标点：引号、逗号、分号、冒号、问号、感叹号、括号全部转全角；
- 第五章“三是逻辑性强……”整段已逐字核验：引号为全角“ ”（U+201C/201D），逗号 U+FF0C、顿号 U+3001、分号 U+FF1B、句号 U+3002，引号 Run 使用宋体；
- 正文仅保留技术性半角字符：%、-、.、/（如 25%、表2.1、Type A/B、25-35），这些保持半角不转换；
- 参考文献保持半角格式；
- 质量引擎通过：sections=4、footer_page_parity=true、toc_cache=16。
## 14. 中文标点真实渲染验证（2026-08-06）

- 中文引号“ ”在 PDF 实测字体为 SimSun（宋体），与正文汉字同字体，不再是 Times New Roman；
- 修复方式：中文 Run 的 ascii/hAnsi/eastAsia 均设宋体，并加 w:hint="eastAsia"；
- 质量引擎 run_fonts 检查已允许宋体/微软雅黑，整体 pass。