# Experience Integration Layer 接口设计

版本：0.7-eil-interface-v1
状态：设计稿

## 一、ExperienceLoader

```python
class ExperienceLoader:
    def __init__(self, registry_path: str, enabled: bool = False): ...

    def load(
        self,
        document_type: str,
        template: str,
        task_context: dict
    ) -> ApplicableExperienceSet: ...
```

Applicable Experience Set：

```json
{
  "document_type": "result",
  "template_source": "02 杨振海 毕业设计成果 ...docx",
  "experiences": [
    {
      "id": "validated_reference_format_001",
      "name": "参考文献悬挂缩进视觉层级保持",
      "source_file": "result/memory/reference_quality_experience.json",
      "status": "long_term_knowledge",
      "role": "quality",
      "judgment": "续行未与正文起始位置形成统一视觉层级",
      "strategy": "依据模板样式调整悬挂缩进",
      "applicable_scope": ["毕业设计成果", "参考文献区域"]
    }
  ]
}
```

## 二、Skill Runner 统一接口

```python
class BaseSkillRunner:
    def run(self, student_info, template, task_context) -> RunResult: ...
```

RunResult 必须包含：

- document_type
- skill
- template_source
- experience_trace
- generation_trace
- quality_checks
- revision_actions
- final_validation

## 三、Quality Sense 统一接口

```python
class BaseSense:
    def check(self, docx_path, pdf_path, knowledge) -> SenseResult: ...
```

SenseResult：

- pass / fail / degraded / unknown
- evidence（结构化数据）
- suggestion

## 四、Revision Planner 接口

```python
class RevisionPlanner:
    def plan(self, sense_results, experience_set) -> RevisionPlan: ...
```

RevisionPlan：

- actions（最小局部修正）
- reason（依据哪条经验）
- impact

## 五、Trace 写入接口

```python
def write_experience_trace(path, entries): ...
def write_generation_trace(path, payload): ...
```

Trace 由代码在对应节点自动写入，不允许生成器自行声明“已使用”。

## 六、文档包级接口

### StudentProfile

```json
{
  "student_name": "",
  "student_id": "",
  "major": "",
  "class": "",
  "advisor": "",
  "topic": ""
}
```

所有文档生成器只能从该对象读取身份字段。

### DocumentPackageManager

```python
class DocumentPackageManager:
    def create_package(self, profile: dict) -> Package: ...
    def register_document(self, doc_type: str, path: str) -> None: ...
    def validate(self) -> PackageValidationReport: ...
```

### DocumentConsistencySense

```python
class DocumentConsistencySense:
    def check(self, documents: dict, profile: dict) -> SenseResult: ...
```

### TemplateComplianceSense

```python
class TemplateComplianceSense:
    def check(self, generated_path: str, expected_template: str) -> SenseResult: ...
```

### DiffEngine

```python
class DiffEngine:
    def compare(self, template_path: str, generated_path: str) -> TemplateDiffReport: ...
```

### PackageValidator

```python
class PackageValidator:
    def validate(self, package: Package) -> PackageValidationReport: ...
```

输出：document_package_validation_report.json