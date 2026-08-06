# Experience Integration Layer 迁移方案、风险与验收

版本：0.7-eil-migration-v1
状态：设计稿

## 一、迁移方案

1. 新增 `config/experience_integration.yaml`，`experience_integration_enabled=false`。
2. 新增 P1 ExperienceLoader 与 Trace 模块，不改旧入口。
3. P2 新增 Result Skill Runner：内部调用 result_reference_builder.py，外部注入经验。
4. P3 新增 TaskBook Skill Runner：加载页面语义经验并校验。
5. P4 新增 Graduation Administrative Document Skill：统一成绩评定表与答辩记录表。
6. 每个阶段用已验证案例回归，通过后保持开关关闭，等待人工启用。

## 二、回退方案

- 关闭开关后，所有 Runner 不接管，旧入口原样运行；
- 旧脚本不删除、不修改；
- 若新链路异常，删除 Runner 调度即可恢复。

## 三、风险分析

| 风险 | 等级 | 对策 |
|---|---|---|
| 伪调用 | 高 | Trace 由代码写入 + Usage Audit 门禁 |
| 经验过拟合 | 高 | 注册表只收多案例验证经验 |
| 误改正文 | 中 | Revision 只做最小局部修正 |
| Word 目录更新失败 | 中 | finalization 失败降级为人工会审 |
| 开关误开 | 中 | 默认 false + 版本登记 |
| 旧链路被污染 | 高 | Runner 只读调用旧生成器，不写旧模块 |
| 跨文档身份/课题不一致 | 高 | Student Profile 唯一数据源 + Document Consistency Sense |
| 模板版本混用 | 高 | Template Compliance Sense 登记模板版本与来源 |
| 包内文件缺失 | 中 | Package Validator 检查齐全性与命名 |

## 四、验收标准

1. 经验真实调用：experience_trace.json 与代码调用路径一致。
2. 生成稳定：同一输入两次生成差异可控。
3. 可追溯：能回答“为什么这样生成、用了什么经验”。
4. 可回退：关闭开关恢复旧流程。
5. 无破坏：V0.3/V0.4/V0.6 脚本零修改。
6. 成果问题收敛：参考文献、固定页、字符样式、页面语义不再复现历史问题。
7. 包级一致：四个文档姓名、学号、专业、班级、指导教师、课题名称全部一致。
8. 包级可交付：Package Validator 通过，document_package_validation_report.json 为 pass。

## 五、阶段验收

### P1
- 任意生成任务可输出真实 experience_trace.json；
- 审计可区分“已加载/未加载/声明未加载”。

### P2
- Result Agent 五项经验全部真实加载；
- 引用层检查命中经验文件；
- 无伪调用。

### P3
- 任务书生成后自动校验页面语义不变量；
- 跨页进入 Revision，而不是直接通过。

### P4
- 成绩评定表/答辩记录表共用同一 Runner；
- 经验域保持隔离，不合并 Quality Memory。