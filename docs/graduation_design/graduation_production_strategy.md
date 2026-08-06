# 毕业设计四件套固定生产策略

时间：2026-08-06
状态：已固定（唯一生产方式）

## 一、总原则

- 模板为唯一版式来源；
- 学生信息、课题、初稿资料可来自学生；
- 其余一切（样式、表格、目录、页眉页脚、分节）只能来自模板；
- 每个文档使用各自已验证的生产方式，不使用统一生成链替代。

## 二、01 任务书

唯一生产方式：

- 入口：`v03/run_taskbook_case.py`（taskbook_generator）
- 版式修正：设计目标 / 设计任务保留两行空行
- Layout Compliance：2 页（第 1 页设计目标+设计任务，第 2 页设计进程+预期成果）
- 依据：`task_book/rules/layout_compliance.md`、CP-2026-08-06-003

## 三、02 成果

唯一生产方式：v1.3 模板样式法

- TemplateInstanceBuilder（黄金模板复制 + 字段替换）
- ContentAdapter（只迁移内容，清除来源 rPr/pPr）
- 表格样式：Table Grid（网格表 1）；表格内容：表格内容样式（五号居中）
- 表注与表格首行同页（keepNext）
- 参考文献：自动编号 + 悬挂缩进 0.74cm
- 目录：单一 TOC 域；PDF 经 Word 更新目录导出（不保存文档，保留模板样式）
- 依据：`result/rules/result_production_strategy_v1.3.md`、CP-2026-08-06-005/006

## 四、03 成绩评定表

唯一生产方式：EvaluationSkillRunner（v1.0）

## 五、04 答辩记录表

唯一生产方式：DefenseSkillRunner + DEFENSE_LAYOUT_NORMALIZE=1（v0.9-candidate-production）

## 六、验收

- 跨文件一致性：姓名、学号、课题、指导教师一致；
- 命名：01/02/03/04 + 学生 + 类型 + 课题；
- PDF 预览齐全；
- 人工验收顺序：PDF 快速扫描 → DOCX 细查 → 报告定位。
