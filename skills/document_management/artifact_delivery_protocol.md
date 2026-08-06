# Agent 文件产物回传规范（Artifact Delivery Protocol）

版本：1.2
性质：交付层规范。不修改业务生成逻辑、Skill逻辑、模板、文档内容。

## 一、文件分类

1. Artifact 文件（需要人工查看）：docx?pdf?xlsx?pptx?图片?markdown报告?json分析结果?
2. 日志文件：不主动展示?

## 二、人工验收交付优先级

毕业设计文档类输出（TaskBook?Result?Evaluation?Defense）生成完成后：

- Level 1 主要验收文件：DOCX（检查模板一致性）?PDF（检查排版效果）?
- Level 2 分析资料：md?json?report?
- Level 3 过程日志：不主动展示?

## 三、交付顺序

固定顺序：1. Word?2. PDF?3. 报告?4. 数据?
禁止把json?markdown?日志放在主要交付列表之前?

## 四、交付格式

```text
?主要验收文件?
- xxx.docx，用途：人工检查Word模板一致性
- xxx.pdf，用途：检查最终排版效果

?分析与记录?
- report.md
- data.json
```

## 五、环境限制

如果当前执行环境不支持文件挂载：

- 明确说明：“当前环境仅生成本地文件，无法转换为聊天附件”?
- 然后提供：文件路径、用途、打开方式?

## 六、适用范围

以下目录生成的人工验收文件，默认按本协议交付：

- `experiments/`
- `graduation_document_ai_lab/`
- `06_输出成果`

## 七、交付层实现

- 协议文档：`CourseAgent/skills/document_management/artifact_delivery_protocol.md`
- 工具：`CourseAgent/tools/artifact_delivery.py`
- 输出：`delivery/delivery_manifest.json`
- 状态：`chat_attachment` / `local_artifact`

## 八、内容优化类实验交付规则

凡涉及：

- 回答优化?
- 文本优化?
- 内容重写?
- 语义调整?

必须生成实际目标文档。

毕业设计文档类实验必须输出：

- ?主要验收文件?优化版 DOCX?优化版 PDF?
- ?分析记录?优化前后对比报告?修改说明?

交付顺序：1. Word→2. PDF→3. 对比报告→4. JSON/日志?

禁止：仅输出markdown对比报告而不生成实际目标文档?
## 九、禁止修改

- 业务生成逻辑?
- Skill逻辑?
- 模板?
- 文档内容?
