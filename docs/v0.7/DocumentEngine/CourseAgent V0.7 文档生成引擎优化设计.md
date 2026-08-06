# CourseAgent V0.7 文档生成引擎优化设计

版本：0.7-engine-v1
状态：设计稿（未编码）
来源：汪子涵独立验证暴露的问题 + 历史案例问题沉淀
原则：不修改 V0.4/V0.6 生产链路；新增能力默认关闭；经验不自动固化；人工确认是经验进入长期知识库的唯一入口。

## 一、背景

成绩评定表与答辩记录表 Skill 封装后，使用汪子涵作为独立新案例进行迁移验证时，暴露了三类系统性问题：

1. 运行环境不固定：`fitz` 缺失、`pdfplumber` 可用、部分 PDF 提取为空，导致每次任务依赖临时补装或组件降级。
2. 内容填充方式错误：跨 run 合并替换导致学生姓名继承标签 run 的加粗样式，生成结果出现字符级样式偏差。
3. 质量检查依赖单一解析器：缺少某个 PDF 组件时，Region Integrity 无法取得标记数据，检查结果不可信。

这三类问题说明：当前仍处于“任务驱动型”运行方式，需要升级为“系统运行环境 + 文档生成引擎”。

## 二、总体架构

```text
Template Parser
      ↓
Document Intermediate Representation
      ↓
Content Filling Engine
      ↓
Style Controller
      ↓
Layout Planner
      ↓
Quality Sense
      ↓
Output Manager
```

各层职责：

| 层 | 职责 | 典型输出 |
|---|---|---|
| Template Parser | 解析段落、表格、单元格、样式、run 结构、命名结构 | TKM / 区域锚点 / run 边界 |
| Content Filling Engine | 在模板副本上做 run 级内容替换，不重建段落 | 填充后的 DOCX |
| Style Controller | 记录并校验填充区域的字符样式继承 | Style Profile / 偏差记录 |
| Layout Planner | 维护页面语义不变量与区域完整性 | Page Layout Invariant / 空间规划 |
| Quality Sense | 对结构、区域、字符、视觉执行可计算检查 | Quality Sense 报告 |
| Output Manager | 继承模板命名规则，管理版本目录与交付命名 | 正式文件 + 命名检查结果 |

## 三、Runtime 环境固定

### 3.1 运行环境清单

新增 `runtime_dependencies.yaml` 作为运行时依赖的规范来源，并同步维护 `requirements.txt`。

依赖分组：

- document_parser：python-docx、pdfplumber、pypdf、pypdfium2
- analysis：lxml、pillow
- validation：openpyxl
- rendering：Word COM（Windows）
- config：pyyaml

### 3.2 environment_checker

每次启动或进入文档任务前执行：

1. 检查依赖是否已安装；
2. 检查版本是否满足要求；
3. 执行最小调用验证（如 `import docx`、打开一个 PDF、获取页数）；
4. 输出 Runtime Health Report。

状态定义：

- ready：全部必需依赖可用；
- degraded：必需依赖可用，可选依赖缺失或调用异常；
- missing：必需依赖缺失，禁止直接生成，先进入环境初始化。

规则：

- 任务执行中不得临时安装依赖；
- 缺失依赖由环境初始化阶段统一处理；
- 可选依赖不可用时，Quality Sense 输出 `unknown/degraded`，不得判定为通过或失败。

### 3.3 Runtime Health Report

报告包含：

- 环境名称与版本；
- 各依赖的安装状态、版本、调用结果；
- 解析器降级情况；
- 结论：ready / degraded / missing；
- 缺失依赖清单与初始化动作。

## 四、Content Filling Engine（run 级替换机制）

### 4.1 问题根因

Word 中一个段落由多个 run 组成，例如：

```text
run1: 学生姓名（加粗）
run2: ：
run3: 杨振海（普通）
```

若直接执行 `paragraph.text = paragraph.text.replace(...)`，Word/python-docx 会重新组合 run，导致：

```text
学生姓名：汪子涵（加粗）
```

即填充内容继承了标签 run 的样式，而不是模板中填写区域自身的样式。

### 4.2 填充规则

1. 生成前先解析 run 结构，记录每个可替换区域的 run 边界与样式；
2. 只修改包含待替换 token 的 run.text；
3. 不合并 run、不重建段落、不新增 run；
4. 保留 bold、italic、underline、font、size、color、style；
5. 若 token 跨 run，按 run 边界拆分替换，或要求模板使用独立占位 run（如 `{{姓名}}`）；
6. 只有确认目标段落为纯正文且无样式差异时，才允许整段替换，并在报告中记录 warning；
7. 填充后必须执行 Character Style Sense，验证填充内容样式与模板一致。

### 4.3 模板占位建议

新模板或模板升级时，字段值区域应尽量使用独立 run 占位，例如：

```text
学生姓名：{{姓名}}
```

模板解析阶段同时记录占位 run 的索引与样式属性，生成阶段只替换占位 run.text。

## 五、Style Controller（样式继承机制）

- 填充内容应继承模板对应区域字符样式，不得因数据替换改变原有样式；
- 禁止写死“姓名不能加粗”等单案例规则；
- 正确经验：字段样式继承模板，偏差按 `character_style_deviation` 诊断；
- 样式检查维度：bold、italic、underline、font name、eastAsia font、size、color、styleId；
- 发现偏差时先做最小修正（恢复模板 run 属性），不重建段落。

## 六、Layout Planner（页面语义布局）

- 维护 Page Semantic Layout Invariant；
- 相关语义单元保持同页：设计目标+设计任务、预期成果+设计进程+签字区域等；
- 区域完整性：签字区域、成绩汇总、答辩结论、记录人/日期不得拆分；
- 布局规律从黄金案例提炼为可迁移质量经验，不复制单案例固定坐标。

## 七、Quality Sense 检查链

检查项：

1. Template Consistency Sense：表格数量、行列、合并、页面、区域标记与模板一致；
2. Table Structure Sense：表格结构未被破坏；
3. Region Integrity Sense：签字、评价、成绩汇总、答辩结论等区域完整；
4. Character Style Sense：字符级样式继承；
5. Visual Balance：页数与关键区域位置接近模板。

检查原则：

- 全部基于结构化数据，不使用模型凭视觉经验判断；
- 组件不可用时输出 `unknown/degraded`，并说明缺失组件；
- 差异 ≠ 错误：模板结构属性被破坏才判定 fail；
- 单案例规则不得直接进入长期知识。

## 八、Output Manager（输出命名管理）

- 文件命名继承模板命名规则：`[序号 ]学生姓名 文档类型关键词 选题名称.docx`；
- 命名在生成阶段执行，不做交付后整理；
- 版本目录区分：AI生成版 / 人工修订版 / 最终交付；
- 命名检查项：包含学生姓名、包含文档类型、与模板命名结构一致、不含 final/test/output/AI测试 等临时名称；
- 输出登记：生成文件路径、版本、检查结果写入输出登记表。

## 九、问题归类表

| 问题 | 生成环节 | 解决方案 | 来源 |
|---|---|---|---|
| 姓名加粗 | Content Filling Layer | run 级替换，不合并 run | 王欢/邱志豪/汪子涵 |
| fitz 缺失、PDF 提取为空 | Runtime Environment Layer | 固定依赖清单 + environment_checker | 汪子涵验证 |
| Region Integrity 误报 | Quality Sense Layer | 多解析器降级 + degraded 状态 | 汪子涵验证 |
| 输出命名临时化 | Output Manager | 模板命名继承 + 生成期命名检查 | 历史交付 |
| 设计进程跨页 | Layout Planning Layer | Page Semantic Layout Invariant | 邱志豪任务书 |

## 十、落地路线

1. V0.7.1：固化运行环境（runtime_dependencies.yaml、requirements.txt、environment_checker 设计）；
2. V0.7.2：实现 Template Filling Engine 与 Style Controller；
3. V0.7.3：Quality Sense 多解析器降级与 degraded 状态；
4. V0.7.4：Output Manager 命名管理接入；
5. 完成后继续汪子涵独立验证，并回归王欢、邱志豪案例。

## 十一、边界

- 不修改 V0.4/V0.6 生产链路；
- 新增能力默认关闭；
- 不自动固化经验；
- 不删除历史验证案例；
- 不临时安装缺失依赖。