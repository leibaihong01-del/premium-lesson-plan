# Runtime Health Report

生成时间：{{timestamp}}
环境：{{environment_name}}
状态：{{status}}

| 依赖 | 导入名 | 必需 | 已安装 | 版本 | 最小调用 | 结果 |
|---|---|---|---|---|---|---|
| python-docx | docx | 是 | {{yes/no}} | {{version}} | {{ok/fail}} | {{ok/degraded/missing}} |
| pdfplumber | pdfplumber | 是 | {{yes/no}} | {{version}} | {{ok/fail}} | {{ok/degraded/missing}} |
| pypdf | pypdf | 是 | {{yes/no}} | {{version}} | {{ok/fail}} | {{ok/degraded/missing}} |
| pypdfium2 | pypdfium2 | 否 | {{yes/no}} | {{version}} | {{ok/fail}} | {{ok/degraded/missing}} |
| lxml | lxml | 是 | {{yes/no}} | {{version}} | {{ok/fail}} | {{ok/degraded/missing}} |
| pillow | PIL | 否 | {{yes/no}} | {{version}} | {{ok/fail}} | {{ok/degraded/missing}} |
| openpyxl | openpyxl | 否 | {{yes/no}} | {{version}} | {{ok/fail}} | {{ok/degraded/missing}} |
| Word COM | - | 是 | {{yes/no}} | {{version}} | {{ok/fail}} | {{ok/degraded/missing}} |

## 结论

- 状态：ready / degraded / missing
- 缺失必需依赖：{{list}}
- 降级项：{{list}}
- 初始化动作：{{none / install list / manual action}}