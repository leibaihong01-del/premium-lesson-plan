# 邱志豪参考文献 Layout Integrity 修正验证报告

## 一、修正前差异

1. 段落级 left/hanging=480 覆盖模板样式；
2. 样式 36 缺少明确 spacing/rPr，依赖 Normal 继承。

## 二、修正动作

- 移除参考文献段落级 w:ind；
- 样式 36 更新为模板样式：spacing 440 exact + ind left=0/hanging=1040/200 + rPr(TNR/宋体)；
- 未修改文字、数量、编号内容。

## 三、修正后检测

- 段落级缩进：0
- style36 spacing：True
- style36 rPr：True
- PDF首行 x0：邱志豪=70.8，杨振海模板=70.8
- 页数：16

## 四、是否建议升级

- 建议：candidate → validated_experience（需人工确认）
- 本次不固化。
