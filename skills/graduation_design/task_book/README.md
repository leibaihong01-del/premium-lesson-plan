# GraduationDesign TaskBook Skill v1.0

毕业设计任务书专家能力包，用于基于学校模板生成学生任务书。

## 内容

- SKILL.md：能力入口与使用说明
- version.json：版本信息
- workflow.md：经验复用与学习模式工作流
- rules/：模板 schema、生成规则、内容规则、命名规则、审核规则
- cases/validation_summary.json：脱敏验证摘要
- references.md：工作区可执行模块与经验库引用

## 使用方式

工作区运行入口：

```powershell
python "00_系统配置\模块\v03\run_taskbook_case.py"
```

参数：GRAD_STUDENT / GRAD_DIRECTION / GRAD_SEQ（默认 01）

## 版本管理

- 正式版本：v1.0-taskbook-baseline
- 版本说明：graduation_design_taskbook_v1.0.md

## 隐私约定

本仓库不包含学生隐私数据、完整成果文件、API 密钥。学生数据仅保存在本地工作区，禁止提交。
