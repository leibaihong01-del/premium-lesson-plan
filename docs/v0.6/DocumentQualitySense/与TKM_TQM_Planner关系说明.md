# 与 TKM / TQM / Planner 关系说明

## 一、定位

- TKM：模板是什么；
- TQM：优秀作品有什么规律；
- Quality Sense：为什么优秀；
- Planner：怎么生成；
- Revision + Experience：怎么改进。

## 二、关系

```
TKM（模板约束）
   +
TQM（优秀规律）
   +
Quality Sense（优秀认知）
   ↓
Generation Planner
   ↓
Writer
   ↓
Reviewer（L1/L2/L3）
   ↓
Revision + Experience
```

## 三、数据流

- Quality Sense 读取 TKM/TQM 与生成结果；
- 输出 quality_level 与 deviation；
- Planner 参考 Quality Sense 语义规则；
- Reviewer 使用 Quality Sense 输出质量等级；
- Experience 沉淀需人工确认。

## 四、可迁移原则

王欢案例只提供“目标与任务关联、结果确认闭环”等语义规律，不写死为所有任务书第一/第二页固定内容。
