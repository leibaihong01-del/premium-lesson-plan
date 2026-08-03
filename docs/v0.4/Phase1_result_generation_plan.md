# Phase 1 成果生成改造实施方案（v0.4.1：Template Instance Pipeline）

状态：设计冻结（未编码）
日期：2026-08-03

## 1. Phase 1 目标

只改毕业设计成果生成链路；不涉及任务书、指导记录、答辩表、成绩表。

原因：成果文件是最大污染源。

## 2. 当前链路（v0.3）

```text
学生成果初稿
  ↓ normalize_draft（run 原位修改）
  ↓ deepcopy 段落/表格/参考文献
  ↓ _replace_text
  ↓ 格式补丁
  ↓ 输出 docx
```

问题：内容与格式混合，原 Word 属性进入生成结果。

## 3. Phase 1 新链路（v0.4.1）

```text
模板文件.docx
  ↓ Template Skeleton Layer（保留骨架/固定页/域/表格）
学生成果初稿 -> Content Clean Layer -> Document IR
  ↓ Region Fill Layer（区域映射填充）
  ↓ Style Apply Layer（模板规则）
  ↓ WPS Processor
  ↓ Document Diff
  ↓ 成果文件
```

## 4. 模块边界

- clean：docx → Document IR；禁止输出 font/style/xml。
- profile：学校模板 → template_profile.json。
- region/style：按 template_region_map 填充内容；格式唯一来自模板；禁止 deepcopy。
- diff：模板 vs 输出，输出差异报告。

## 5. v0.3 迁移策略

- 不删除 legacy：保留 result_reference_builder.py、result_generator.py。
- 新增 v04/result_pipeline/，配置开关：

```yaml
word_engine:
  version: v03   # 默认 v03；测试时切 v04
```

## 6. 开发顺序

1. Document IR 成果映射（确认全结构可表达）
2. Template Profile 解析成果模板（标题/正文/表格/参考文献/页码）
3. Rebuild 最小闭环（生成 1 份成果）
4. Diff 检测
5. 扩大测试：5 人 → 20 人 → 107 人

## 7. 验收标准

- 格式：无初稿字体残留、无颜色残留、无底纹残留、参考文献统一。
- 结构：一级/二级标题正确、标题空格规则正确、表格一致。
- 自动化：Diff 报告生成、WPS 目录流程正常。

## 8. 回滚方案

失败立即切回 `word_engine.version: v03`；保留 v0.4 代码、Schema 与测试数据。

## 9. 禁止事项

- 禁止 deepcopy/run 迁移/XML 复制；
- 禁止以学生初稿格式为格式来源；
- 禁止 Python 手工生成目录缓存。
