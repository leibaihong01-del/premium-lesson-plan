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