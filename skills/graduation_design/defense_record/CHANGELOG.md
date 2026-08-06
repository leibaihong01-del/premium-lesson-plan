# Defense Skill CHANGELOG

## v0.9-candidate-production (2026-08-05)

### Added

- Defense 模板骨架驱动（27 段结构）
- DNA 版式控制（行高 12547、行距 440/360/440、加粗规则）
- 回答针对性优化规则
- 内容压缩规则（单页容量适配）
- 单页输出规则
- DOCX/PDF 交付验证

### Status

Candidate Production

## v0.10-differentiation (2026-08-06)

### Added

- 答辩记录表同方向差异化控制（defense_differentiation.py）；
- 三级画像体系：Professional Profile / Direction Profile / Student Project Profile；
- 相似度检测：首句重复 / 高频句式 / 关键词重复率；
- 安全重写：仅重排已有材料，不虚构；
- 设计文档与电梯方向验证。
## v0.11 structured-rewrite (2026-08-06)

### Changed

- 新增 Student Anchor Extractor；
- 重写结构：学生实例特征 → 专业共性 → 设计完成内容；
- 相似度权重调整：首句 0.45 / 句式模板 0.40 / 关键词 0.15；
- DOCX 实际改写落地（DefenseSkillRunner answer_text 注入）。

### 验证

- 电梯方向 3 人：相似度 0.924 → 0.431；
- 首句重复 1.000 → 0.000；
- 关键词重复保留 0.875（专业共性）。
## v0.12 answer-only (2026-08-06)

### Changed

- 回退整单元格改写：仅修改两个“答：”段落；
- 新增 extract_defense_answers / apply_defense_answers；
- 模板 27 段结构与视觉保持不变；
- 电梯方向验证：答段落相似度 0.981 → 0.398。
## v0.13 light-rewrite (2026-08-06)

### Changed

- 答辩记录生成固定回 v0.9：DefenseSkillRunner + DEFENSE_LAYOUT_NORMALIZE=1；
- 差异化只对两个“答：”段落轻改写（学生实例开头 + 原答案保留）；
- 移除整单元格/重结构改写路径。
## v0.14 fixed-v0.9 (2026-08-06)

### Changed

- 答辩记录生成回退并固定：DefenseSkillRunner + DEFENSE_LAYOUT_NORMALIZE=1（v0.9）；
- 禁止修改已生成答辩记录 DOCX；
- 差异化模块仅保留只读相似度分析（analysis-only）。