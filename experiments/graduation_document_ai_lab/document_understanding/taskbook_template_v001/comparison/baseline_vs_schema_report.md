# Baseline vs Schema Report

| 项目 | 旧策略 baseline | schema_v0.1 实验 |
|---|---|---|
| 页面 | 2 | 3 |
| 表格 | 1 | 1 |
| 行列 | [(18, 14)] | [(18, 14)] |
| 合并单元格 | 66 | 66 |
| 姓名 | True | True |
| 学号 | True | False |
| 课题 | True | True |
| 设计目标 | True | True |
| 设计任务 | True | True |
| 内容量 | 1255 | 1240 |

## 结论

- 旧策略保留完整格式保护与内容迁移，schema 实验仅做字段填充
- 差异集中在内容质量与格式保真，而非表格结构