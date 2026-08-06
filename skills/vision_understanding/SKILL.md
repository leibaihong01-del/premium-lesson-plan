---
name: vision_understanding
description: 通过视觉模型（MiMo）分析图片、PPT页面截图、PDF页面视觉信息，输出结构化JSON，用于教材图片理解、PPT版式检查、毕业设计成果图检查。
---

# Vision Understanding Skill

## 能力

- 图片理解；
- PPT 页面分析；
- PDF 页面截图分析；
- 毕业设计成果图/表/公式检查。

## 输入

- path：图片或 PDF 路径；
- prompt：分析要求；
- provider：可选的 VisionProvider（默认 MiMo，未启用时返回结构化失败）。

## 输出

结构化 JSON：

```json
{
  "ok": true,
  "analysis": "...",
  "provider": "mimo",
  "prompt": "...",
  "skill": "vision_understanding"
}
```

## 调用

```bash
python skills/vision_understanding/skill.py 案例图.png --prompt "请分析该图片并输出结构化JSON"
python skills/vision_understanding/skill.py 课件.pdf --prompt "请分析第3页版式" --page 2
```