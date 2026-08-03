# v0.3 Word生成架构审计报告

日期：2026-08-03
模式：READ ONLY（只读审计，未修改任何代码）

## 1. 审计背景

毕业设计 Word 批量生成出现：字体不一致、字号偏差、参考文献格式异常、标题间距不一致、目录非 WPS 自动生成、部分文字颜色/底纹残留。

本报告目标是定位根因，而不是增加格式规则。结论先行：根因是“Word 元素迁移式生成”，不是“缺少格式参数”。

## 2. 当前 Word 生成链路

```text
学生成果初稿.docx
   ↓ result_generator.generate / normalize_draft
初稿副本：run 原位修改 font/size/style（原 rPr 残留）
   ↓ result_reference_builder.reconstruct
模板母版复制（golden）
   ↓ 删除模板正文/参考文献，deepcopy 初稿段落/表格/参考文献元素插入
   ↓ _replace_text 原位替换字段
   ↓ _add_toc_field 手工插入 TOC 域
   ↓ result_revision.apply_to_file
Heading1 pageBreakBefore + Word COM 域更新
   ↓
输出 docx
```

| 阶段 | 模块 | 关键函数 | 输入 | 输出 | 是否保留原格式 |
|---|---|---|---|---|---|
| 内容预处理 | result_generator | normalize_draft / set_run_font | 初稿 | 初稿副本 | 是（run 原位修改，保留其他 rPr） |
| 模板重构 | result_reference_builder | reconstruct | 初稿副本 + 模板 | 生成 docx | 是（deepcopy 段落/表格/参考文献） |
| 域处理 | result_revision | apply_to_file | 生成 docx | 最终 docx | 部分（Word 重写） |
| 检测 | content_check/validator | analyze | 最终 docx | 报告 | 只读 |

## 3. 高危模块函数清单

| 序号 | 文件 | 函数 | 危险操作 | 对象类型 | 风险 |
|---|---|---|---|---|---|
| 1 | result_reference_builder.py | reconstruct | copy.deepcopy(el)（正文） | Paragraph/Table XML | 高 |
| 2 | result_reference_builder.py | reconstruct | copy.deepcopy(el)（参考文献） | Paragraph XML | 高 |
| 3 | result_reference_builder.py | _replace_text | run.text 原位替换 | Run | 中高 |
| 4 | result_generator.py | set_run_font | run.font.size/name 原位修改 | Run（保留 rPr 其他属性） | 高 |
| 5 | result_generator.py | normalize_draft | 原段落/原 run 上改格式 | Paragraph/Run | 高 |
| 6 | taskbook_generator.py | migrate_cell | deepcopy(paras[-1]._p) | Paragraph XML | 中 |
| 7 | taskbook_generator.py | set_para_text | 原 run 上改 text | Run | 中 |
| 8 | result_revision.py | apply_to_file | paragraph_format.page_break_before | Paragraph | 低（预期行为） |

详细说明：

1. `reconstruct`（result_reference_builder.py:185,242）：直接把初稿正文段落、表格、参考文献元素的 XML 复制进模板文档。原 `<w:rPr>`、`<w:pPr>`、单元格属性（颜色/底纹/字体/行距）一并带入。
2. `set_run_font`（result_generator.py:39-50）：只改写 font.size、bold、name，不清除原 run 的 color/highlight/shading/underline 等属性，形成字符级残留。
3. `normalize_draft`（result_generator.py:80）：在初稿副本的原段落结构上改格式，原段落属性与样式引用保留。
4. `_replace_text`（result_reference_builder.py:62）：对 run 文本原位替换，保留 run 全部字符属性。
5. `migrate_cell`（taskbook_generator.py:82）：deepcopy 模板段落 XML 克隆段落。

## 4. deepcopy/run/XML/style 风险分析

- deepcopy 段落/表格/参考文献：直接搬运 `<w:p>`、`<w:rPr>`、`<w:tblPr>`、单元格 `<w:tcPr>`，原文档格式进入生成结果。
- run 原位修改：只覆盖部分属性（font/size/bold/name），颜色、高亮、底纹、下划线、字符间距等残留。
- 样式继承：正文段落被重映射到“正文内容”样式，但 run 级旧属性仍存在；标题样式映射后，原段落行距/对齐等属性可能保留。
- 表格：整表 deepcopy，单元格宽度、边框、颜色来自初稿；模板边框仅在后置补丁阶段加入。
- 目录：TOC 域手工插入，未由 WPS 生成与更新，缓存条目不完整（仅一级标题），目录层级（1.1 等）缺失。

结论：当前属于“直接迁移格式”（C 类），不是“完全重建格式”（A 类）。

## 5. 格式污染根因

1. 字体不一致：初稿 run 的 `<w:rPr>` 随 deepcopy 进入模板；set_run_font 只改部分属性。
2. 字号不一致：初稿 run 字号残留，样式继承与 run 显式字号混用。
3. 颜色/底纹残留：deepcopy 保留 `<w:color>/<w:shd>/<w:highlight>`。
4. 参考文献异常：参考文献段落 deepcopy 后只改样式名与去空格，未重建字符格式，中英文字体混用。
5. 标题空格不稳定：标题文本基于初稿段落迁移，编号与标题之间的空格未按模板规则重建（如“五  总结”）。
6. 目录非 WPS：目录域手工插入 + Word 更新，未走 WPS 自动目录流程，缓存不全。

## 6. 模板画像能力评估

| 能力 | 当前状态 | 覆盖 |
|---|---|---|
| 页面解析（尺寸/页边距/页眉页脚） | 部分支持（section_profile） | 约 70% |
| 字体解析（中/西文字体、字号、粗体、颜色） | 部分支持（run 级，缺样式定义级） | 约 40% |
| 段落解析（行距/对齐/缩进/段前段后） | 部分支持（paragraph_metrics） | 约 35% |
| 标题规则（编号+两空格、两字标题加空格） | 未结构化 | 约 40% |
| 表格规则（行列/合并/边框/样式） | 部分支持 | 约 50% |
| 参考文献规则（字体/格式） | 未形成规则 | 约 30% |
| 目录规则（WPS/TOC 域） | 仅检测存在，不生成 | 约 20% |

总体：不足。当前无法生成完整 `template_profile.json`（缺少样式定义级字体/字号、段落级行距缩进、标题编号规则、参考文献字体规则、WPS 目录规则）。

## 7. 当前架构问题

- 生成链路是“模板复制 + 内容元素迁移”，不是“内容解析 + 格式重建”；
- 内容与格式未分离：原 run/段落/表格属性进入生成结果；
- 模板解析停留在结构统计，未达到“模板画像”；
- 目录、页码等 Word/WPS 自动化依赖手工域补丁；
- 检测偏内容与结构计数，缺少逐 run 字符属性比对。

## 8. 四层升级方案（只设计，不实现）

Layer 1：Word Clean Layer
- 输入 Word → 只提取文本、层级、表格数据、参考文献；丢弃字体、颜色、底纹、高亮、下划线、样式、修订、批注、隐藏格式；输出结构化 JSON。

Layer 2：Template Profile Layer
- 解析模板为 `template_profile.json`：页面、字体（中/西文、字号、粗斜、颜色）、段落（行距/对齐/缩进/段前段后）、标题（编号+两空格、两字标题加空格）、表格（边框/样式/合并）、参考文献、目录（WPS/TOC 域）。

Layer 3：Document Rebuild Layer
- 禁止 deepcopy/run 迁移/XML 复制；按结构化内容新建 Paragraph/Run/Table，逐项应用模板规则；目录交由 WPS 生成。

Layer 4：Document Diff Layer
- 模板 vs 生成：页面、字体、字号、行距、缩进、标题编号与空格、表格边框/合并、参考文献字体、目录域与 WPS 规范性，输出全量差异报告。

## 9. 改造优先级建议

P0（必须）：停止 deepcopy 式 Word 元素生成；内容与格式分离（Word Clean + Rebuild）。
P1（重要）：建立模板画像 `template_profile.json`；目录改由 WPS 生成。
P2（增强）：Document Diff 自动检测 + 自动修复闭环；逐 run 字符属性比对。

## 10. 审计结论

- 是否存在 Word 元素直接复制：是（deepcopy 段落/表格/参考文献 XML）。
- 是否存在原格式继承：是（run 原位修改 + deepcopy 保留 rPr/pPr/tcPr）。
- 高危函数：8 处，最大风险模块为 `result_reference_builder.py`（reconstruct），其次 `result_generator.py`（set_run_font/normalize_draft）。
- 根因：不是格式参数缺失，而是“元素迁移式生成”。
- 建议：停止当前 deepcopy 式生成方式，升级为“结构化内容 + 模板重建”的 v0.4 架构。
