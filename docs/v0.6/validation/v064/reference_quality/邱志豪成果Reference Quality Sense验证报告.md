# 邱志豪成果 Reference Quality Sense 验证报告

## 一、发现的问题

- 参考文献 5 条存在 `查看` + U+00A0；
- 6 个参考文献段落存在段落级缩进覆盖；
- style36 缺少明确 spacing/rPr。

## 二、判断依据

- 杨振海模板：style36 spacing=440 exact、ind left=0/hanging=1040/200、rPr(TNR/宋体)；
- 当前：段落级 left/hanging=480，样式不完整。

## 三、根因分析

- 直接原因：段落级缩进覆盖模板样式，异常字符未清理；
- 根本原因：成果生成阶段缺少参考文献区域质量约束。

## 四、修改内容

- 删除 `查看/全文/链接` 与 U+00A0；
- 移除参考文献段落级 w:ind；
- style36 恢复模板样式（spacing/ind/rPr）。

## 五、修改前后对比

| 项 | 修正前 | 修正后 |
|---|---|---|
| 污染 | 10 | 0 |
| 段落级缩进 | 6 | 0 |
| style36 spacing/rPr | 缺失 | 存在 |
| PDF首行 x0 | - | 70.8（模板 70.8） |
| 续行悬挂偏移 | - | 0.0（模板 0.0） |
| 页数 | 16 | 16 |
| 表格 | 6 | 6 |

## 六、结论

- Reference Layout Integrity: Pass
- Document Quality Sense: Pass

## 七、经验处理

- 生成 Experience Candidate；
- 不自动升级；
- 等待人工查看成品后确认。
