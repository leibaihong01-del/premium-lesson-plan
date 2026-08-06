---
name: graduation-package
description: 毕业设计四件套唯一生产 Skill：任务书、成果（Result v1.5）、成绩评定表、答辩记录表端到端生成与跨文件校验。
---
# Graduation Package Skill

毕业设计四件套统一生产 Skill：任务书、成果、成绩评定表、答辩记录表端到端生成。

## 1. 定位

本 Skill 负责把一个学生的四件套完整产出，使用已经人工确认的唯一生产路径，不做实验性生成。

## 2. 输入

- 学生数据源：`毕业设计智能制作工作区/03_需要修改文件/毕业设计名单.xlsx`（权威名单，字段以名单为准）；
- 学生资料目录：`03_需要修改文件整理/<方向>/<学生名>/`（任务书.docx、成果初稿.docx、成绩评定表.docx、答辩记录表.docx、学生信息.json）；
- 黄金模板目录：`02_模板文件/`（01/02/04/05 杨振海模板）。

## 3. 调用链

```text
毕业设计名单.xlsx
    ↓
StudentProfile（姓名/学号/班级/指导教师/题目/方向）
    ↓
01 TaskBook：v03/run_taskbook_case.py → 2页校验 → 空行压缩
    ↓
02 Result：tools/result_v1.4_pipeline.py（v1.5 唯一输出方式）
    ↓
03 Evaluation：EvaluationSkillRunner（v1.0）
    ↓
04 Defense：DefenseSkillRunner + DEFENSE_LAYOUT_NORMALIZE=1（v0.9）
    ↓
跨文件一致性校验（姓名/学号/班级/指导教师/题目）
    ↓
README + 验证报告 + 成果包
```

## 4. 已知问题与修复（必须执行）

1. Result 封面字段替换必须覆盖姓名、学号、班级、指导教师、题目、站点；
   - 修复：`v03/result_reference_builder.py` 的 `_identity_pairs` 已包含班级与指导教师；
   - 漏掉班级会保留模板的“24级机电技术1班”。
2. TaskBook 必须 2 页：
   - 设计目标/设计任务各留 2 行空行（多余空行删除）；
   - 相关行 trHeight 设为 auto；
   - 渲染校验页数，超出继续压缩。
3. WPS/Word 占用输出文件会导致 WinError 32：
   - 生成前关闭打开中的 DOCX/PDF；
   - 文件被占用时改用新版本目录。
4. 学生信息必须与毕业设计名单一致，不得只信任学生信息.json。
5. 跨文件一致性校验必须包含班级，不能只查姓名/学号/题目/指导教师。

## 5. 验收

- 四个 DOCX 存在且命名规范；
- 四个 PDF 渲染成功；
- 五个字段四文件一致；
- Result 质量引擎 pass（sections=4、footer_page_parity=true、toc_cache 完整）；
- TaskBook PDF = 2 页；
- 成果包 README 可点击索引。

## 6. 输出

```text
06_输出成果/<方向>/<学生名>_毕业设计完整成果包/
    01/02/03/04 *.docx
    README.md
    _过程记录/*.pdf + 校验报告
```
