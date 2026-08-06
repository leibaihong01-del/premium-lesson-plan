# 毕业设计任务书专家能力包 v1.1

名称：GraduationDesign TaskBook Skill v1.1
状态：正式生产（唯一生产路径 = taskbook_generator）

## 唯一生产路径

```text
taskbook_generator（v03/run_taskbook_case.py）
```

禁止以下组件参与生产：
- schema_v0.1_auto
- Document Understanding 实验
- 视觉解析模块

## 输入

- 学生信息（姓名/学号/班级/专业/指导教师）
- 毕业设计课题信息
- 黄金任务书模板（01 杨振海 毕业设计任务书）

## 输出

- 毕业设计任务书 DOCX
- 内部 PDF 渲染验证（不交付）

## 处理流程

模板加载 → 字段映射 → 内容生成 → 内容迁移 → 格式保护 → 内部审核 → 输出生成

## 能力清单

1. 模板解析：2 页 / 1 表（18 行 × 14 列）
2. 生成策略：模板母版复制 + 字段填充 + 学生真实内容迁移
3. 格式保持：内容区 12pt 宋体/Times New Roman；软换行拆段；Wingdings 勾选
4. 内容逻辑：虚拟地点不得作为真实资料来源
5. 命名继承：[序号 ]学生姓名 毕业设计任务书 选题名称.docx
6. 内部审核：内容 / 结构 / 格式 / 命名 / 页数

## 调用说明

```powershell
$env:GRAD_STUDENT='王欢'
$env:GRAD_DIRECTION='01_AFC自动售检票系统'
$env:GRAD_SEQ='01'
python 00_系统配置/模块/v03/run_taskbook_case.py
```

## 验收规则：TaskBook Layout Compliance

- 总页数：2 页?
- 第1页：设计目标、设计任务?
- 第2页：设计进程、预期成果?
- 禁止：模块拆散、表格跨页、内容溢出?
- 规则文件：`rules/layout_compliance.md`?

- 生产必须包含版式修正（设计目标/任务保留两行空行） + Layout Compliance（2页），唯一生产方式?
