# 答辩记录表差异化控制设计（v0.1）

## 1. 目标

支持不同专业、不同方向的毕业设计答辩记录生成；保留专业共性，降低同方向学生之间的模板化表达；所有改写必须来源于学生已有材料，不虚构技术内容。

## 2. 三级画像数据模型

### 2.1 Professional Profile（专业画像）

```json
{
  "professional": "城市轨道交通机电技术",
  "knowledge_points": ["车站机电设备", "检修规范", "安全用电"],
  "common_terms": ["检修", "故障", "方案", "设备"],
  "answer_norms": ["结论明确", "步骤可执行", "突出安全"]
}
```

作用：保留专业共性表达基线。

### 2.2 Direction Profile（方向画像）

```json
{
  "direction": "电梯系统",
  "professional": "城市轨道交通机电技术",
  "knowledge_points": ["曳引系统", "门系统", "安全保护装置"],
  "keywords": ["电梯", "曳引机", "门锁", "限速器"],
  "expression_dimensions": [
    "开头强调车站客流与设备使用强度",
    "按结构-原理-故障-方案顺序",
    "按故障-排查-检修-验证顺序"
  ]
}
```

作用：定义同方向可变化表达维度，方向列表可扩展，不固定 8 个。

### 2.3 Student Project Profile（学生项目画像）

```json
{
  "student": "邱志豪",
  "professional": "城市轨道交通机电技术",
  "direction": "电梯系统",
  "topic": "太平街口站电梯常见故障分析与检修方案设计",
  "station": "太平街口站",
  "facts": ["电梯系统组成", "曳引系统检修", "门系统检修", "安全保护"],
  "source": {
    "taskbook": "任务书文本",
    "result": "成果文本摘要",
    "draft": "答辩记录初稿"
  },
  "features": ["故障分类", "检修周期", "安全措施"]
}
```

作用：差异化只依据该学生真实材料，禁止虚构。

## 3. Skill 接口

```text
build_professional_profile(professional) -> Professional Profile
build_direction_profile(professional, direction) -> Direction Profile
build_student_project_profile(student_info, materials) -> Student Project Profile
generate_answer(student_project_profile) -> 答辩答案草稿
analyze_similarity(direction, answer_texts) -> 相似度指标
rewrite_batch(student_project_profiles) -> 安全重写结果
```

实现位置：`CourseAgent/core/defense_differentiation.py`

## 4. 生成流程

```text
学生材料（任务书/成果/答辩初稿）
    ↓
专业画像 + 方向画像
    ↓
生成答辩记录
    ↓
同方向批量相似度检测（首句/高频句式/关键词）
    ↓
高度相似 → 基于学生真实材料安全重写
    ↓
输出差异化答辩记录
```

## 5. 安全约束

- 只重排/重述已有句子与真实事实；
- 不新增设备、数据、故障等未出现的技术内容；
- 专业共性与方向知识不得被删除。

## 6. 验证计划

选择“电梯系统”方向：

1. 提取 3 名学生答辩初稿；
2. 构建三级画像；
3. 相似度检测；
4. 安全重写；
5. 输出验证报告。

## v2 更新（2026-08-06）

- Student Anchor Extractor：从真实材料提取课题/对象/站点/设备/重点/任务关键词；
- 禁止简单句序调整，必须优先使用学生独有信息作开头；
- 结构固定：学生实例特征 → 专业共性描述 → 设计完成内容；
- 相似度重点：首句重复、句式模板重复、表达结构重复；关键词降权且保留专业共性；
- 落地：DefenseSkillRunner 支持 answer_text 注入，批量生成直接改写 DOCX。