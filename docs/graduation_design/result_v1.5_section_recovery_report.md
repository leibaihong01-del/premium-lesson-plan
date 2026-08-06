# Result v1.5 Section Skeleton Recovery 验证报告

## 1. 阶段定位

- 阶段：Result v1.4 收口 -> Section Skeleton Recovery 实现
- 目标：恢复黄金模板 4 分节骨架，正文页码独立从 1 起排
- 范围：只改模板实例生成层，不修改黄金模板、不改变生产策略

## 2. 根因确认

`rebuild_toc` 删除“目录标题 -> 第 1 章标题”区间全部节点时，删除了携带 S3 `sectPr` 的分节段落，导致目录 Section 与正文 Section 合并，v1.4 只剩 3 个 Section。

另外 `ensure_page_fields` 会给模板本身无 PAGE 域的 footer1/footer4 追加 PAGE，导致封面和目录页出现页码，与模板视觉不一致。

## 3. 代码修改

1. `CourseAgent/tools/result_v1.4_pipeline.py`
   - `rebuild_toc`：删除旧目录结果时保留含 `w:sectPr` 的段落；
   - `ensure_page_fields(doc, golden=None)`：只对黄金模板自身含 PAGE 域的 footer 补齐；
   - `finalize(out_docx, golden=None)`，main 传入 golden。
2. `CourseAgent/core/result_document_quality_engine.py`
   - `word_structure_quality` 增加 golden 对照；
   - sections 检查改为 `== 4`；
   - 新增 footer_page_parity：footer 页码域与模板逐项一致。

## 4. 验证结果

- Section 数量：模板 4，v1.5 4；
- Section 边界：
  - S1 封面：HDR first/default/even，FTR first/default/even；
  - S2 真实性承诺：HDR default，footer 链接继承；
  - S3 目录：HDR default，FTR default，`pgNumType fmt=decimal`；
  - S4 正文：HDR default，FTR default，`pgNumType fmt=decimal start=1`；
- Footer PAGE 布局：footer1=0，footer2=1，footer3=0，footer4=0，footer5=2，与模板一致；
- 质量引擎：四维 pass，sections=4，footer_page_parity=true；
- PDF 22 页：封面、承诺页、目录页无页码；目录显示三级条目与页码；正文从 1 起排。

## 5. 输出文件

- DOCX：`毕业设计智能制作工作区/06_输出成果/01_AFC自动售检票系统/王欢_成果v1.5分节恢复/02 王欢 毕业设计成果 解放西路站AFC检票机故障排查方案设计.docx`
- PDF：`王欢_成果v1.5分节恢复/_过程记录/02 王欢 毕业设计成果 解放西路站AFC检票机故障排查方案设计.pdf`
- 质量报告：`result_v1.5_production_report.json`

## 6. 遗留与下一步

- TOC Cache 按计划暂缓：Word/WPS 打开时依赖 `updateFields` 自动刷新，本次 PDF 渲染已由 Word 刷新目录；
- 下一步：TOC Cache 修复 -> 最终质量验收 -> 人工确认后冻结 v1.5。
