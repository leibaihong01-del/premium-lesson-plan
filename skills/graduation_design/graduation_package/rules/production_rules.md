# Graduation Package 生产规则

## 1. 数据规则

- 学生信息以毕业设计名单.xlsx 为准；
- 学生信息.json 仅作参考，冲突时以名单为准并提示人工确认；
- 每个学生独立成果目录，禁止混放。

## 2. 四产物唯一入口

- 01 任务书：`v03/run_taskbook_case.py`；
- 02 成果：`tools/result_v1.4_pipeline.py`（v1.5 唯一）；
- 03 成绩评定表：`EvaluationSkillRunner`；
- 04 答辩记录表：`DefenseSkillRunner + DEFENSE_LAYOUT_NORMALIZE=1`。

## 3. 必须修复点

### Result 封面字段

`_identity_pairs` 必须包含：

- 杨振海 → 姓名；
- 202421044622 → 学号；
- 24级机电技术1班 → 班级；
- 瞿曌 → 指导教师；
- 黄兴南路站AFC闸机设备检修方案设计 → 题目；
- 黄兴南路站 → 课题站点。

### TaskBook 2 页

- 设计目标、设计任务各保留 2 行空行；
- 超出页数时删除多余空行并把行高设为 auto；
- 渲染 PDF 校验总页数 = 2。

### 文件占用

- 生成前确认 WPS/Word 未打开目标文件；
- 若 WinError 32，关闭预览后重试，或改用新版本目录。

## 4. 验收规则

- 四个文件命名符合 `[编号] 姓名 文档类型 题目.docx`；
- 姓名/学号/班级/指导教师/题目四文件一致；
- Result 质量引擎 pass；
- TaskBook PDF 2 页；
- 成果包含 README 索引。
