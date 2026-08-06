# Experience Integration Layer 模块结构设计

版本：0.7-eil-module-v1
状态：设计稿

## 一、新增模块

```text
CourseAgent/
├── core/
│   ├── experience_loader.py          # P1 经验加载
│   ├── experience_registry.py        # 经验注册表
│   ├── experience_trace.py           # experience_trace 写入
│   ├── generation_trace.py           # generation_trace 写入
│   ├── student_profile.py            # 学生主数据唯一数据源
│   ├── document_package_manager.py   # 学生档案包管理
│   ├── diff_engine.py                # 模板原文件 vs 生成文件对比
│   └── package_validator.py          # 包级交付验收
├── skills/
│   ├── task_book_skill/              # P3
│   ├── result_skill/                 # P2 Result Agent
│   ├── evaluation_form_skill/        # P4
│   └── defense_record_skill/         # P4 合并为 Graduation Administrative Document Skill
├── quality/
│   ├── document_quality_sense.py
│   ├── reference_quality_sense.py
│   ├── character_style_sense.py
│   ├── page_semantic_sense.py
│   ├── document_consistency_sense.py
│   └── template_compliance_sense.py
├── revision/
│   └── revision_planner.py
└── config/
    └── experience_integration.yaml   # experience_integration_enabled=false
```

## 二、各模块职责

### core/experience_loader.py
- 输入：document_type、template、task_context
- 输出：Applicable Experience Set
- 职责：按文档类型从经验注册表加载 TKM、Quality Memory、Validated Experience

### core/experience_registry.py
- 登记全部已验证经验
- 记录：id、名称、来源文件、状态、适用范围、判断依据、解决策略

### core/experience_trace.py / generation_trace.py
- 自动记录经验调用与生成过程
- 禁止人工手写“已使用”声明

### skills/*/runner.py
- 每个文档类型一个执行入口
- 内部复用旧生成器，不修改旧代码

### quality/*.py
- 各 Sense 执行器，全部基于结构化数据
- 组件不可用时输出 degraded/unknown，不误判通过/失败

### revision/revision_planner.py
- 根据 Quality Sense 输出生成最小修正计划
- 只做局部修正，不重建文档

## 三、默认关闭

- 配置：`experience_integration_enabled=false`
- 关闭时：所有 Runner 不接管，旧流程原样运行
- 开启时：仅影响新增 Runner，不影响旧入口