# DefenseRecordGenerationSkill

版本：v0.9-candidate-production
状态：Candidate Production（候选生产版）
类型：模板保持 + 区域填充

## 输入
- 学生信息
- 课题信息
- 答辩信息

## 调用
- Defense Record TKM
- Defense Record Quality Memory

## 输出
- 答辩记录表 DOCX/PDF
- 验收报告

## 流程
1. 模板保持
2. 区域填充
3. 字符样式检查
4. 页面检查
5. 输出验收报告

## 当前版本

- 状态：Candidate Production
- 版本：v0.9-candidate-production
- 基线目录：`versions/v0.9-candidate-production/`

已通过：

- 模板骨架验证
- 版式 DNA 固化
- 单页输出
- 字体规则保护
- 内容针对性优化
- 内容压缩适配
- DOCX/PDF 交付验证

## 版本约束

后续修改必须创建新版本，保留 v0.9 基线，并执行回归测试。

## 答辩差异化控制（v0.10）

- 批量同方向生成时执行相似度检测与安全重写；
- 画像：专业画像 + 方向画像 + 学生项目画像；
- 数据：skills/graduation_design/defense_record/rules/direction_profiles.json；
- 实现：CourseAgent/core/defense_differentiation.py；
- 规则：不虚构内容，改写必须来源于学生已有材料。