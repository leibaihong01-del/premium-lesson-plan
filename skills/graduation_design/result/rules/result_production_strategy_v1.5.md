# Result 毕业设计成果唯一输出方式 v1.5

## 1. 定位

自 2026-08-06 起，毕业设计成果仅使用本方式输出，为唯一生产路径。

## 2. 唯一生产入口

`CourseAgent/tools/result_v1.4_pipeline.py`

调用参数：

```text
python result_v1.4_pipeline.py <学生信息.json> <方向> <输出.docx> <黄金模板.docx> [<输出.pdf>]
```

## 3. 生产流程

```text
StudentProfile
    ↓
TemplateInstanceBuilder（黄金模板实例化，只替换学生字段）
    ↓
ContentAdapter（只迁移文本/语义，不携带来源格式）
    ↓
DocumentFinalizer（标题/正文/表格/表注/参考文献/目录）
    ↓
TOC Cache（自动目录 + 缓存页码）
    ↓
Document Quality Engine（四维检查）
    ↓
DOCX 正式输出 + PDF 预览 + 质量报告
```

## 4. 强制规则

- 黄金模板是唯一视觉来源；
- 封面只替换姓名、学号、班级、题目、指导教师等字段，其余格式不动；
- 第二页承诺书保持模板原样；
- 目录为 Word 自动目录（sdt + Table of Contents），打开无需手动刷新，可自动更新；
- 标题纯样式继承，一级/二级标题不写直接字体，避免目录更新污染；
- 正文标点全角化，参考文献保持半角；
- 中文标点（含引号）Run 的 ascii/hAnsi/eastAsia 均设宋体并加 hint=eastAsia；
- 正文表格使用模板样式，单元格黑色单线、无底色、内容自适应列宽；
- 表注为表X.Y，样式表注，宋体/TNR 五号，keepNext；
- 虚构站点/线路名清洗为“某轨道交通线路”表述，封面校名保留；
- 专科毕业设计学术词黑名单：本文/本研究/本课题/本论文/实验结果表明/研究对象/笔者/该研究/课题研究；
- 生成后必须通过质量引擎：sections=4、footer_page_parity=true、toc_cache 完整。

## 5. 输出物

1. DOCX 正式成果；
2. PDF 内部预览（放 _过程记录）；
3. result_*_production_report.json 质量报告。

## 6. 版本与依据

- 依据：王欢 v1.5 人工确认；
- 保留历史：v1.4、v0.2、黄金模板均不覆盖。
