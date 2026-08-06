# 毕业设计 Agent 现状报告

日期：2026-08-05
范围：CourseAgent 中与毕业设计相关的 Skill、Prompt、模板、生成脚本、测试案例

## 一、四类文件是否支持生成

| 文档 | 支持 | 状态 |
|---|---|---|
| 毕业设计任务书 | 是 | 已回归 PASS |
| 毕业设计成果 | 是 | 可生成，质量仍受内容深度限制 |
| 毕业设计成绩评定表 | 是 | 已回归 PASS |
| 毕业设计答辩记录表 | 是 | 已回归 PASS |

## 二、各文件生成入口

| 文档 | 生成入口 | 生成方式 |
|---|---|---|
| 任务书 | v03/run_taskbook_case.py + taskbook_generator | 模板母版复制 + 内容迁移 + 内部审核 |
| 成果 | result_reference_builder + ResultSkillRunner / result_v2 | 模板保真重构 + 封面字段移植 + 字体规范 + 参考文献经验 |
| 成绩评定表 | EvaluationSkillRunner（graduation_skill_runners.py） | 模板复制 + run级字段替换 |
| 答辩记录表 | DefenseSkillRunner（graduation_skill_runners.py） | 模板复制 + 字段替换 + 学生答辩内容迁移 |

## 三、模板使用情况

| 文档 | 模板 |
|---|---|
| 任务书 | 01 杨振海 毕业设计任务书 黄兴南路站AFC闸机设备检修方案设计.docx |
| 成果 | 02 杨振海 毕业设计成果 黄兴南路站AFC闸机设备检修方案设计.docx |
| 成绩评定表 | 04 杨振海 毕业设计成绩评定表 ...docx |
| 答辩记录表 | 05 杨振海 毕业设计答辩记录表 ...docx |

模板位置：毕业设计智能制作工作区/02_模板文件/

## 四、Prompt 使用情况

当前 CourseAgent Prompt 资产：

- prompts/manifest.yaml
- prompts/translator/system.md
- prompts/translator/user_template.json

现状：

- 毕业设计生成主要依赖脚本规则与模板，不依赖统一生成 Prompt；
- 尚无按文档类型区分的 TaskBook/Result/Evaluation/Defense Prompt；
- Prompt 与生成入口未形成强绑定。

## 五、批量支持

- 当前为单案例脚本/入口，不支持真正批量生产；
- 已有 DocumentPackageManager / StudentProfile 可支持逐学生组装；
- 未实现批量调度、批量排队、批量异常恢复。

## 六、质量检查

| 文档 | 检查 |
|---|---|
| 任务书 | v03 internal_audit：结构/内容/命名/页数 |
| 成果 | ResultQualityPipeline：Content/Structure/Layout/Reference/ARKM Sense |
| 成绩评定表 | Table/Region/Character Style/Template Compliance |
| 答辩记录表 | Table/Region/Character Style/Template Compliance |
| 全包 | DocumentPackageValidator：一致性/模板/PDF/命名/Trace |

## 七、经验沉淀

- Experience Registry 已建立（data/experience_registry.json）；
- 已固化：任务书 TKM/Quality Memory、成绩评定表 Quality Memory、答辩记录表 Quality Memory、Reference Quality Experience、Document DNA candidate；
- 缺失：Result Quality Memory、ARKM；
- 经验调用受 `experience_integration_enabled=false` 控制，默认不进入生产。

## 八、与 CourseAgent Skill 架构的差距

1. Skill 文档存在，但执行入口与 Skill 定义未完全绑定；
2. 四个文档类型没有统一可安装的 Skill 包结构（SKILL.md/manifest/输入输出规范/校验）；
3. Prompt 未按 Skill 拆分；
4. 无批量调度层；
5. Result 内容生成能力缺失，经验无法真正提升正文深度；
6. 经验候选多、验证与人工确认流程未闭环；
7. 当前以“脚本 + Runner”为主，尚未达到“Skill 驱动生产”的架构标准。

## 九、结论

- 四类文件均已具备真实生成能力；
- 任务书、成绩评定表、答辩记录表具备封装条件；
- 成果可封装但内容深度仍不足；
- 下一步优先补：Skill 包结构、Prompt 绑定、批量调度、Result 内容规划。