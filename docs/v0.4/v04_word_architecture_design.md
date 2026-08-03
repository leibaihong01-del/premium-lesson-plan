# v0.4 毕业设计 Word 生成架构设计方案

状态：设计稿（Phase 0 冻结，未编码）
日期：2026-08-03

## 1. 总体目标

v0.3：Word → 复制元素 → 修改格式 → 输出（格式污染不可控）。
v0.4：内容 → 结构化 → 模板规则 → 重新生成 → 验证（模板驱动确定性生成）。

## 2. 总体架构

```text
输入资料
  ↓
Word Clean Layer（文档清洗解析）
  ↓
Document IR（中间文档表示）
  ↓
Template Profile Layer（模板画像）
  ↓
Document Rebuild Layer（文档重建）
  ↓
WPS 处理（目录/域生命周期）
  ↓
Document Diff Layer（自动检测）
  ↓
输出成果
```

## 3. 模块边界

### 3.1 Word Clean Layer
- 输入：docx；输出：Document IR。
- 提取文本、标题层级、表格、图片、参考文献；删除字体、颜色、底纹、原样式、修订、批注。

### 3.2 Document IR
- 核心中间结构：document_type + metadata + blocks。
- 不保存 font/size/color/style/xml。

### 3.3 Template Profile Layer
- 输入：学校模板 docx；输出：template_profile.json。
- 包含 page、styles、heading_rules、table_rules、reference_rules、toc_rules。

### 3.4 Document Rebuild Layer
- 输入：Document IR + template_profile；输出：docx。
- 原则：每个 Paragraph/Run/Table 都是新建，禁止 copy/deepcopy/migration。

### 3.5 WPS Processor
- 负责目录生成与刷新、域更新；生成器不维护目录缓存。

### 3.6 Document Diff Layer
- 模板 vs 生成：页面、字体、字号、行距、缩进、标题编号与空格、表格边框/合并/宽度、参考文献、目录。
- 输出差异报告。

## 4. Schema 关系

Document IR（写什么）+ Template Profile（怎么显示）→ Document Builder → DOCX

## 5. 迁移策略

- Phase 0：冻结 v0.3 基线（v0.3-baseline），保证回滚。
- Phase 1：改造成果生成（result_reference_builder 替换为 IR + Rebuild）。
- Phase 2：迁移任务书（taskbook_generator，移除 migrate_cell）。
- Phase 3：统一答辩、指导记录、成绩表。

## 6. 开发步骤

1. Document IR Schema（document_ir.schema.json）
2. Template Profile Schema（template_profile.schema.json）
3. Clean Layer
4. Rebuild Layer
5. Diff Layer
6. 接入现有 Orchestrator（模式开关 v03/v04）

## 7. 测试方案

- 污染清除测试：红色字体/黄色底纹/微软雅黑/隐藏格式必须全部消失。
- 模板一致性测试：模板 宋体小四 → 生成 宋体小四。
- 结构测试：标题层级、表格数量、页数。
- 批量测试：107 人数据稳定性。

## 8. 回滚方案

- 新架构默认关闭；config 中 word_generation.mode = v03 / v04。
- 失败立即回退 v03 链路。

## 9. v0.4 验收标准

- 格式：字体 100% 来自模板；无颜色/底纹残留；参考文献统一。
- 结构：标题层级正确；空格规则正确；表格一致。
- 自动化：Diff 检测通过；WPS 目录正常。

## 10. 结论

v0.4 不是 Word 格式优化模块，而是 CourseAgent 文档生成基础设施，后续毕业设计、教案、课程标准、精品课程材料统一复用。

## 11. v0.4.1 架构修正

- 原 Document Rebuild Layer 调整为 Template Instance Pipeline；
- 新增 Template Skeleton Layer（保留模板资产）与 Region Fill Layer（区域填充）；
- 禁止“模板 -> JSON -> 新 Word”；详细见 v0.4.1_Word生成架构实施方案.md。
