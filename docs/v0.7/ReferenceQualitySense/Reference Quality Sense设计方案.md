# Reference Quality Sense（参考文献质量感知）设计方案

版本：0.7-rqs-draft
状态：设计稿，未编码
目标：让 Agent 学会判断参考文献是否符合毕业设计成果质量要求。
原则：禁止学习固定数值；禁止形成“必须使用某个缩进值”的死规则。

## 一、闭环

```
Reference Understanding
  ↓
Reference Diagnosis
  ↓
Reference Revision
  ↓
Reference Validation
```

## 二、区域解析

1. 文献数量：记录 reference_count，检查空编号、连续性、重复；
2. 文本内容：U+00A0、多余空格、隐藏字符、网页复制残留；
3. 网页污染：查看/全文/链接/访问/URL残留 → reference_content_pollution；
4. 根因：生成阶段内容清洗不足；
5. 修正：删除污染，保留作者/题名/来源/年份/卷期/页码/文献类型标识。

## 三、视觉结构检查

- 编号区域：对齐、层级一致、位置稳定；
- 悬挂缩进：第一行保留编号，续行向正文起始位置对齐；
- 异常：续行回到页边或超过正文位置 → reference_hanging_indent_deviation；
- 根因：参考文献段落样式异常。

## 四、参考基准选择

- 必须使用杨振海成果模板（source_verified=true）；
- 禁止使用未验证案例作为视觉标准；
- source_verified=false 的案例标记 invalid_evidence，不参与学习/规则/判断。

## 五、样式比较

- 段落样式：左缩进、悬挂缩进、首行缩进、段前、段后、行距；
- 字体样式：中文字体、英文字体、字号；
- 编号方式：自动编号 vs 文本编号，需与黄金模板一致；
- 视觉节奏：条目间距、页面密度、孤行。

## 六、诊断

Diagnosis Record 使用三级结构：

```
现象
  ↓
直接原因
  ↓
根本原因
```

problem_type：reference_layout。

## 七、修正策略优先级

1. 调用模板参考文献样式；
2. 调用 validated_experience；
3. 执行局部样式修复。

允许：修改段落样式、悬挂缩进、行距、清理异常字符。
禁止：修改文献内容、顺序、数量（除非明显错误）。

## 八、修正后验证

- 异常字符=0；
- 网页污染=0；
- 编号一致；
- 首行一致；
- 续行悬挂一致；
- 字体一致；
- 行距一致；
- 输出 Reference Quality Report。

## 九、经验沉淀

禁止记录“修改悬挂缩进为0.74cm”；

应记录：

- 问题：参考文献多行结构视觉失衡；
- 判断依据：续行未形成悬挂层级；
- 根因：模板样式未继承；
- 策略：调用黄金模板参考文献样式；
- 结果：视觉一致性恢复。

形成 Reference Quality Experience Candidate。
