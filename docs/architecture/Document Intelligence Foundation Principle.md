# Document Intelligence Foundation Principle（文档智能基础原则）

版本：1.0
状态：CourseAgent 底层架构原则
适用范围：所有文档生成、质量感知、经验沉淀能力。

## 1. 所有文档处理必须经过结构化理解层

CourseAgent 不直接依赖模型阅读原始 Word/PDF 文件进行判断。

所有文档进入系统后，必须经过：

```
原始文档
 ↓
Document Parser（Python解析层）
 ↓
Document Intermediate Representation（文档中间表示）
 ↓
Quality Sense / Knowledge Model
 ↓
Generation / Review / Revision
```

## 2. Python 文档解析层职责

负责提取客观事实。

### Word层

- 段落结构
- 表格结构
- 单元格关系
- 样式继承
- 字体
- 字号
- 行距
- 段距
- 缩进
- 分页信息
- 页眉页脚
- 编号格式

### PDF层

负责验证最终表现：

- 实际页数
- 内容位置
- 页面溢出
- 表格断裂
- 空白区域
- 视觉布局

## 3. 大模型职责边界

模型不负责“看一眼 Word，然后凭经验判断”。

模型负责基于结构化数据完成：

- 语义理解
- 原因分析
- 质量判断
- 策略生成
- 经验抽象

示例：

错误方式：给模型一个 Word，让它说参考文献有没有问题。

正确方式：

```json
{
  "reference_item": 3,
  "line_count": 2,
  "hanging_indent": 480,
  "template_standard": 420,
  "alignment_status": "failed"
}
```

模型判断：当前问题属于参考文献视觉一致性问题，建议调整悬挂缩进。

## 4. 所有 Quality Sense 必须建立在结构化数据之上

包括：

- Document Quality Sense
- Page Layout Quality Sense
- Reference Quality Sense
- Table Quality Sense
- Template Quality Sense
- Character Style Sense
- Output Naming Sense

以后新增成绩评定表、答辩记录表、指导记录表、课程标准、教案等，都走同一基础能力。

## 5. 经验系统只记录“判断逻辑”

不要沉淀：

- “王欢第一页这样”
- “参考文献改0.74厘米”

应沉淀：

- 为什么两个区域必须同页
- 多行参考文献需要保持首行与续行视觉层级一致，具体参数来自模板基准
## 6. 输出管理必须经过结构化命名与目录管理

- 文件命名继承模板规则，禁止模型自由命名；
- 学生成果按 专业方向/学生姓名_毕业设计材料 目录隔离；
- 编号代表文档类型，禁止按生成顺序随机编号；
- 所有输出经 Output Naming Sense 检查并输出 output_validation_report.json；
- StudentProjectRegistry 统一管理 专业→班级→学生→课题→材料集合，不写死方向数量。