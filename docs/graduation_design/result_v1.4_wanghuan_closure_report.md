# 王欢成果 v1.4 生成闭环报告

时间：2026-08-06
性质：模板 → 生成 → Diff → Quality Engine → 修复 → 最终 docx

## 一、生成链

- 入口：`tools/result_v1.4_pipeline.py`
- 生成：黄金模板 → TemplateInstanceBuilder → ContentAdapter → Finalizer → Quality Engine
- 修复：Run 级字体拆分、标点、页码域、settings updateFields

## 二、规则落地

1. 标点：正文英文引号转中文全角；标题编号、步骤编号、参考文献编号与科研半角格式保持原样；
2. Run 级字体：中文宋体小四，英文数字 Times New Roman 小四，混合 Run 自动拆分；
3. 标题：H1 微软雅黑三号加粗居中、段前段后 1 行；H2 宋体四号加粗两端对齐；H3 宋体小四加粗；
4. 表格：Table Grid + 表格内容样式，85% 宽、页面居中、单元格水平垂直居中、内容感知列宽；
5. 表注：模板“表注”样式 + keepNext；
6. 参考文献：模板自动编号（[%1]）、悬挂缩进 0.74cm、宋体/Times 小四；
7. 目录：单一 TOC 域、settings updateFields、Word 刷新导出。

## 三、Diff 与修复

- Diff 发现：页码域缺失（模板 16 / 生成 3）；
- 修复：各分节页脚补 PAGE 域（现 4）；
- Diff 发现：正文混合 Run 字体不拆分；已修复；
- Diff 发现：目录未最终化；已通过 Word 刷新。

## 四、Quality Engine

| 维度 | 结果 |
|---|---|
| Format Quality | 通过 |
| Content Quality | 通过（无事实风险、无科研论文表达） |
| Template Inheritance Quality | 通过（styles/numbering/settings、样式 19/33、6 表） |
| Word Structure Quality | 通过（单一 TOC、页码域、6 表） |

## 五、输出

- DOCX：王欢_成果v1.4闭环/02 王欢 毕业设计成果 解放西路站AFC检票机故障排查方案设计.docx
- PDF：22 页（目录已更新）

## 六、残余问题

- 分节 3（黄金模板 4），已记录待修；
- DOCX 目录域未缓存，打开时 WPS/Word 会按 updateFields 自动刷新。
