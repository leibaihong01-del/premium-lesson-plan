# Generation Pipeline Audit Report（生成链路审计报告）

版本：0.7-audit-v1
日期：2026-08-04
对象：毕业设计完整成果包生成链路
结论：知识经验已固化，但当前生成入口未真正调用，`knowledge_isolated=true`。

## 一、当前实际生成入口

完整成果包实际走的是 V0.3 生成器 + V0.7 临时验证脚本，不是 V0.4/V0.6/V0.7 Skill 正式入口。

| 文档 | 实际执行路径 | 是否调用正式入口 |
|---|---|---|
| 01 任务书 | v03/run_taskbook_case.py → taskbook_generator → internal_audit | 是（V0.3 入口） |
| 02 成果 | v03/run_result_case.py → result_generator → result_audit；再由 run_v07_complete_package_*.py 合并黄金模板前页 | 否（未调用 result_reference_builder.py 正式入口） |
| 03 成绩评定表 | run_v07_*_evaluation_defense.py 模板填充 | 否（Skill 目录无可执行入口） |
| 04 答辩记录表 | run_v07_*_evaluation_defense.py 模板填充 | 否（Skill 目录无可执行入口） |

## 二、当前调用链

### 01 任务书

```text
run_taskbook_case.py
  → taskbook_generator.generate()
      - 复制 01 杨振海模板
      - 迁移学生任务书内容
  → internal_audit.auto_repair()
      - 结构/内容/命名检查，最多 3 轮自动修复
  → convert_to_pdf + probe_pdf（页数校验）
```

未调用：v06 cognitive_model_builder、generation_planner、gap_report_generator、diagnosis_engine、revision_planner。
v06 config.json `enabled=false`，页面语义布局经验未进入生成。

### 02 成果

```text
run_result_case.py
  → result_generator.generate()
      - 复制成果初稿
      - normalize_draft（标题/字体/正文标准化）
  → result_audit.auto_repair_result()
      - 结构/格式/命名/固定页缺口会审
  → run_v07_complete_package_*.py
      - build_result()：黄金模板前页 + 学生正文合并
      - 自写检查：table_stats / pdf_markers / cover_char_style_check
```

未调用：result_reference_builder.py、result/rules/template_schema.json、reference_quality_experience.json、result/memory/golden_cases/wanghuan.md、Document Quality Sense 执行器、Reference Quality Sense 执行器。

### 03 成绩评定表 / 04 答辩记录表

```text
run_v07_*_evaluation_defense.py
  → 复制 04/05 杨振海模板
  → run级字段替换 + 段落级内容替换
  → 自写检查：table_stats / pdf_markers / char_style_check
```

未调用：evaluation_form/defense_record Skill 下的任何可执行入口（目录中只有 SKILL.md、workflow.md、rules/quality_memory.yaml）。

## 三、经验接入状态（知识隔离判定）

| 能力 | 固化产物 | 位置 | 是否被生成链路调用 | 判定 |
|---|---|---|---|---|
| Result Template Knowledge Model | result/rules/template_schema.json 等规则 | CourseAgent/skills/graduation_design/result/rules | 否 | knowledge_isolated=true |
| Result Quality Memory | 未发现独立 quality_memory 文件；规则散落在 result/rules | result/rules | 否 | knowledge_isolated=true |
| Document Quality Sense | 设计文档与 schema | CourseAgent/docs/v0.6/DocumentQualitySense | 否（无执行器接入） | knowledge_isolated=true |
| Reference Quality Sense | 设计文档、schema、validated experience | docs/v0.7/ReferenceQualitySense；result/memory/reference_quality_experience.json | 否 | knowledge_isolated=true |
| Golden Case Experience | result/memory/golden_cases/wanghuan.md | result/memory | 否 | knowledge_isolated=true |
| 任务书页面语义布局经验 | v06 模块 + 经验固化报告 | 00_系统配置/模块/v06 | 否（enabled=false） | knowledge_isolated=true |
| 成绩评定表/答辩记录表 Skill | SKILL.md / workflow / quality_memory.yaml | skills/graduation_design/evaluation_form、defense_record | 否（仅文档骨架） | knowledge_isolated=true |

## 四、声明的经验使用与实际调用不一致

陈家宝完整成果包 `_过程记录/使用经验记录.json` 声明使用了 Result Quality Memory、Quality Memory Taskbook 等，但生成脚本未以编程方式读取这些文件。

- 声明：使用经验记录写入 experience_used_record.json
- 实际：脚本只输出知识清单，不加载、不解析、不按经验约束生成
- 结论：报告记录 ≠ 链路调用

## 五、经验注入点检查

期望链路与现状：

| 节点 | 任务书 | 成果 | 成绩评定表 | 答辩记录表 |
|---|---|---|---|---|
| Template Understanding | V0.3 硬编码模板 | V0.3 硬编码模板 | V0.7 脚本硬编码 | V0.7 脚本硬编码 |
| Generation Planning | 缺失（v06 未启用） | 缺失 | 缺失 | 缺失 |
| Content Generation | V0.3 迁移 | V0.3 标准化 | 字段替换 | 字段+段落替换 |
| Quality Sense | 自写基础检查 | 自写基础检查 | 自写基础检查 | 自写基础检查 |
| Revision Planner | 缺失 | 缺失 | 缺失 | 缺失 |
| Final Validation | V0.3 audit | V0.3 audit + 自写 | 自写 | 自写 |

经验注入点均未建立。

## 六、审计证据

- 00_系统配置/模块/v06/config.json：enabled=false
- 00_系统配置/模块/v06/README.md：默认关闭
- 00_系统配置/模块/v03/result_reference_builder.py：正式入口，未加载经验
- 00_系统配置/模块/v03/result_revision.py：仅章节分页与目录更新
- CourseAgent/skills/graduation_design/result/SKILL.md：声明 result_reference_builder.py 为正式入口
- CourseAgent/skills/graduation_design/result/memory/reference_quality_experience.json：long_term_knowledge，未被调用
- CourseAgent/skills/graduation_design/result/content_check/validator.py：仅加载 school_rules/expert_rules
- 毕业设计智能制作工作区/00_系统配置/模块/v06/run_v07_complete_package_chenjiabao.py：自写检查，未加载经验

## 七、结论

1. 经验已经固化，但生成链路没有接入，处于“经验孤岛”状态。
2. 当前入口应明确为 V0.7 Skill runner（默认关闭），内部复用 V0.3 生成器与 V0.6 规划器，但不修改旧生产链路。
3. 必须先建立经验加载层与注入点，再重新验证。