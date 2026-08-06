# Document Package Intelligence Layer 实施设计与编码

版本：0.7-dpil-v1
状态：P2 设计 + 编码
任务定位：不是管理文件夹，而是建立“一个学生毕业设计全生命周期档案对象”。

## 一、核心概念

Student Graduation Archive（学生毕业设计全生命周期档案）：

- 一个学生 = 一个档案对象；
- 档案对象承载完整生命周期：创建 → 规划 → 生成 → 验证 → 修正 → 交付 → 归档；
- 档案对象统一持有 Student Profile、四类文档、Trace、检查报告、验证报告；
- 目录只是档案对象的物理落盘位置，不是档案本身。

## 二、生命周期状态机

```text
created
  ↓
planning
  ↓
generating
  ↓
validating
  ↓
revision
  ↓
deliverable
  ↓
archived
```

每个状态变更写入 timeline：

```json
{
  "timestamp": "2026-08-04T...",
  "event": "register_document",
  "detail": "03 毕业设计成绩评定表"
}
```

## 三、档案对象模型

```json
{
  "archive_id": "dpil-20260804-chenjiabao",
  "student_profile": { ... },
  "direction": "电梯系统",
  "package_dir": "...",
  "lifecycle_status": "validating",
  "documents": [
    {
      "code": "01",
      "document_type": "毕业设计任务书",
      "filename": "01 陈家宝 毕业设计任务书 ....docx",
      "docx_path": "...",
      "pdf_path": "...",
      "template_source": "01 杨振海 毕业设计任务书 ....docx",
      "status": "generated",
      "generated_at": "..."
    }
  ],
  "timeline": [],
  "consistency_report": {},
  "template_report": {},
  "validation_report": {}
}
```

## 四、模块结构

```text
core/
├── student_profile.py                 # P1：学生主数据
├── experience_loader.py               # P1：经验加载
├── experience_trace.py                # P1：经验 Trace
├── generation_trace.py                # P1：生成 Trace
├── document_package.py                # P2：档案对象模型
├── document_package_manager.py        # P2：档案生命周期管理
├── document_consistency_sense.py      # P2：跨文档一致性
├── template_compliance_sense.py       # P2：模板符合性
└── package_validator.py               # P2：包级验收
```

## 五、接口设计

### DocumentPackageManager

```python
class DocumentPackageManager:
    def create_archive(self, profile, direction, base_dir) -> StudentGraduationArchive: ...
    def register_document(self, code, document_type, docx_path, pdf_path, template_source): ...
    def write_lifecycle_state(self): ...
    def validate(self) -> PackageValidationReport: ...
```

### DocumentConsistencySense

```python
class DocumentConsistencySense:
    def check(self, archive, profile) -> ConsistencyReport: ...
```

### TemplateComplianceSense

```python
class TemplateComplianceSense:
    def check(self, archive) -> TemplateComplianceReport: ...
```

### PackageValidator

```python
class PackageValidator:
    def validate(self, archive, trace_dir=None) -> PackageValidationReport: ...
```

## 六、数据流

```text
StudentProfile + 四类 DOCX/PDF
 ↓
DocumentPackageManager.create_archive
 ↓
register_document（写入 timeline）
 ↓
DocumentConsistencySense（身份/课题跨文档比对）
 ↓
TemplateComplianceSense（表格结构/固定区域）
 ↓
PackageValidator（齐全/命名/一致性/模板/PDF/经验Trace）
 ↓
document_package_validation_report.json
```

## 七、与 Experience Integration Layer 的关系

- ExperienceLoader 负责“生成前加载经验”；
- 档案对象负责“生成后持有证据”；
- 包级验收时把 P1 的 experience_trace 作为证据纳入 validation_report；
- 禁止无 Trace 的档案进入 deliverable。

## 八、验收标准

1. 一个学生只有一个档案对象；
2. 档案对象可回答：当前处于什么生命周期阶段、有哪些文档、用了什么经验、验证是否通过；
3. 跨文档身份/课题不一致必须被发现；
4. 模板结构被破坏必须被发现；
5. 验证报告由代码生成，不手工填写；
6. 默认关闭逻辑不受影响。