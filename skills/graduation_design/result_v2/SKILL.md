# Result Skill v2

版本：2.0
状态：正式（最佳已验证生产策略）
类型：Content-driven Document（模板保真重构）

## 一、Skill 定义

负责毕业设计成果的生成、经验加载、质量检查与输出。
本 Skill 是 Result Production Strategy 的正式封装，不再按版本号选择旧入口。

## 二、输入规范

- StudentProfile（学生姓名/学号/专业/班级/指导教师/课题）
- 学生成果初稿（成果初稿.docx）
- 成果记录表（成果记录表.docx，封面字段来源）
- 杨振海毕业设计成果模板（02 ...docx）

## 三、调用流程

StudentProfile
↓
ResultSkillRunner
↓
result_reference_builder（模板保真重构）
↓
封面字段移植（成果记录表 → 模板封面）
↓
字体规范（正文12pt宋体/Times New Roman，Heading1 16pt黑体，Heading2 15pt黑体）
↓
ResultExperienceConsumer
↓
ResultQualityPipeline
↓
输出 DOCX/PDF

## 四、使用经验

- Result TKM
- Golden Case Experience（王欢成果）
- Reference Quality Sense
- Document Quality Sense
- 成果规则集（排版/目录/表格/内容/学院）

## 五、质量检查

- Content Quality Sense：身份/课题/任务匹配/禁用表达
- Structure Quality Sense：目录/标题/图表/参考文献/表格
- Layout Quality Sense：页数/空白页/正文字号/分节
- Reference Quality Sense：数量/编号/污染字符/悬挂缩进
- Academic Requirement Compliance Sense：学院要求

## 六、输出规范

- DOCX：02 学生姓名 毕业设计成果 课题名称.docx
- PDF：_过程记录/02 学生姓名 毕业设计成果 课题名称.pdf
- 过程文件：experience_trace_result.json、generation_trace_result.json、result_quality_report.json