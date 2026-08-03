# Environment Preflight（环境预检）

版本：1.0
适用范围：所有依赖 Python 运行时的文档任务开始前。

## 一、检查项

- 当前 Python 解释器路径；
- 虚拟环境是否激活；
- 依赖是否完整（docx、fitz、pdfplumber 等）；
- 外部工具版本（Word/WPS、Poppler 等）。

## 二、自动处理

- 若发现依赖缺失或 Python 路径错误：
  自动切换项目 bundled runtime 或虚拟环境；
  无需等待用户确认。

## 三、报告

- 仅当无法自动修复时才报告并暂停。
