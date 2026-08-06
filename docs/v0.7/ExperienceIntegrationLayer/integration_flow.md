# Experience Integration Layer 调用流程图

版本：0.7-eil-flow-v1

## 一、总体流程

```mermaid
graph TD
  A[输入: 学生信息/模板/任务上下文] --> B[Template Understanding]
  B --> C[ExperienceLoader]
  C --> D[Applicable Experience Set]
  D --> E[Generation 复用旧生成器]
  E --> F[Quality Sense]
  F --> G{有偏差?}
  G -- 是 --> H[Revision Planner]
  H --> I[局部修正]
  I --> F
  G -- 否 --> J[Final Validation]
  J --> K[Output Naming Sense]
  K --> L[experience_trace.json / generation_trace.json]
  L --> M[Experience Usage Audit]
```

## 二、Result Agent 调用流程

```text
学生成果初稿
 ↓
Result TKM（结构理解）
 ↓
Result Quality Memory + Golden Case（规划约束）
 ↓
result_reference_builder（复用，不修改）
 ↓
内容层检查 + 格式层检查 + 引用层检查（Reference Quality Sense）
 ↓
Revision Planner（最小局部修正）
 ↓
Final Validation + Output Naming Sense
 ↓
双 Trace + Usage Audit
```

## 三、模板驱动型文档调用流程（成绩评定表/答辩记录表）

```text
模板 + 学生信息
 ↓
TKM 解析（表格/字段/区域）
 ↓
Quality Memory 加载
 ↓
模板填充（run级，样式继承）
 ↓
Table Structure / Region / Character Style Sense
 ↓
Revision Planner
 ↓
Validation + Output Naming Sense
 ↓
双 Trace + Usage Audit
```

## 四、文档包级调用流程

```mermaid
graph TD
  A[Student Profile] --> B[Document Package Manager]
  B --> C[01 任务书 Skill]
  B --> D[02 成果 Skill]
  B --> E[03 成绩评定表 Skill]
  B --> F[04 答辩记录表 Skill]
  C --> G[单文件 Validation]
  D --> G
  E --> G
  F --> G
  G --> H[Document Consistency Sense]
  H --> I[Template Compliance Sense]
  I --> J[Diff Engine]
  J --> K[Package Validator]
  K --> L[document_package_validation_report.json]
```