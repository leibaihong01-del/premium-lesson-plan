# 邱志豪四件套生产问题总结与优化报告

## 1. 背景

使用毕业设计四件套唯一生产路径生成邱志豪完整成果包：

- 01 毕业设计任务书；
- 02 毕业设计成果（Result v1.5 唯一输出方式）；
- 03 毕业设计成绩评定表；
- 04 毕业设计答辩记录表。

## 2. 生产过程中发现的问题

### 问题 1：Result 封面班级字段替换失败

- 现象：成果封面仍为模板“24级机电技术1班”，应为邱志豪“24级机电技术2班”。
- 根因：`result_reference_builder._identity_pairs` 只替换姓名、学号、题目、站点，未替换班级与指导教师。
- 修复：补充 `24级机电技术1班 → 班级`、`瞿曌 → 指导教师` 替换对。

### 问题 2：任务书 3 页，超出 Layout Compliance

- 现象：任务书 PDF 3 页，标准为 2 页。
- 根因：设计目标/设计任务单元格各留 3 行空行，且行高过大，预期成果内容溢出到第 3 页。
- 修复：多余空行删除至 2 行，相关行 trHeight 设为 auto，重新渲染后 2 页。

### 问题 3：WPS 占用文件导致生成失败

- 现象：生成时 WinError 32（另一个程序正在使用此文件）。
- 根因：WPS 打开着输出 DOCX。
- 修复：生成前关闭 WPS/Word 预览；被占用时改用新版本目录。

### 问题 4：学生信息权威来源

- 现象：成果封面班级来自模板默认值，未与权威名单核对。
- 要求：学生信息以 `毕业设计名单.xlsx` 为准，跨文件校验必须包含班级。

### 问题 5：跨文件一致性校验不完整

- 现象：原校验只查姓名/学号/题目/指导教师，漏查班级。
- 修复：四文件五字段（姓名/学号/班级/指导教师/题目）全部校验。

## 3. 验证结果

- 四文件五字段全部一致；
- Result 质量引擎 pass：sections=4、footer_page_parity=true、toc_cache=16；
- TaskBook PDF = 2 页；
- 四个 PDF 渲染成功。

## 4. 经验沉淀

新增 `skills/graduation_design/graduation_package`：

- SKILL.md；
- workflow.yaml；
- rules/production_rules.md；
- memory/package_production_memory.json；
- CHANGELOG.md。
