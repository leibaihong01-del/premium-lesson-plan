# Section Skeleton Recovery Plan

时间：2026-08-06
性质：只读分析 + 恢复方案设计（未修改代码/docx）

## 一、当前差异

| 项目 | 黄金模板 | 王欢 v1.4 |
|---|---|---|
| Section 数量 | 4 | 3 |
| 目录 Section 页码 | fmt decimal | 缺失（与正文合并） |
| 正文 Section 页码 | fmt decimal start=1 | 保留（start=1） |
| footer 关系 | S1: footer3/1/2；S3: footer4；S4: footer5 | S1 保留；S3 footer4 丢失；S4 footer5 保留 |
| PAGE 域 | 19 | 4 |
| settings updateFields | 无 | 有 |

## 二、合并点定位

模板：

```text
目录结束（目  录）
    ↓
S3 sectPr（fmt decimal + footer4）
    ↓
正文开始（1 引言）
```

生成版：

```text
目录结束（目  录）
    ↓
TOC 域（重建）
    ↓
正文直接开始（1 引言）
```

合并点：目录与正文之间的 Section Break 段落（携带 S3 sectPr）在 TOC 重建时被删除。

## 三、根因判断

分类：B（内容填充/TOC 重建删除 section break）+ C（段落重建导致 sectPr 丢失）。

具体：`rebuild_toc` 删除“目录标题”到“第 1 章标题”之间的全部子节点，其中包含模板的 S3 sectPr 段落，导致 S3 与 S4 合并。

## 四、恢复架构设计

推荐：Template Skeleton Layer

```text
Template Skeleton Layer
    ↓
保护：sectPr / header / footer / page numbering / TOC 位置 / section break
    ↓
Region Fill（仅替换内容）
    ↓
Content Replace
```

关键约束：

- 禁止重新创建 Section；
- TOC 重建时保留并重排 sectPr 段落（移到 TOC 域之后、正文之前）；
- 内容替换不得删除 headerReference / footerReference；
- 生成后骨架校验：Section 数量、边界、footer 映射、pgNumType。

## 五、恢复步骤（实现阶段执行）

1. 快照模板骨架：sectPr 段落位置、header/footer rId 映射、pgNumType；
2. 生成后 TOC 重建：保留“目录→正文”间的 sectPr 段落，仅在正文前重放；
3. 校验：S1/S2/S3/S4 边界与模板一致；
4. 校验 footer 映射：S1 footer3/1/2、S3 footer4、S4 footer5；
5. 校验 PAGE 域数量与页码连续性。

## 六、验收标准

- Section 数量 = 4；
- 目录 Section 与正文 Section 独立；
- footer 映射与模板一致；
- 正文页码 start=1；
- 无新创建 Section。

## 七、下一阶段

1. Section Skeleton Recovery 实现；
2. 重新生成王欢 v1.5；
3. TOC Cache；
4. 最终质量验收。

## 八、实施结果（2026-08-06）

已完成实现与验证：

- Section 数量 = 4，目录 Section 与正文 Section 已恢复独立；
- footer 映射与模板一致，页码域逐项一致（footer1=0、footer2=1、footer3=0、footer4=0、footer5=2）；
- 正文页码 start=1，PDF 渲染后封面/承诺页/目录页无页码；
- 验证报告：docs/graduation_design/result_v1.5_section_recovery_report.md；
- Checkpoint：CP-2026-08-06-008。

待办：TOC Cache（暂缓），人工确认后冻结 v1.5。