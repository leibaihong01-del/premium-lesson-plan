# Codex C盘迁移至D盘：第一阶段环境审计报告

日期：2026-08-02    阶段：Phase 1 全面扫描（只审计，未执行迁移）
目标目录：D:\AI\Codex（本阶段未创建）

## 一、扫描范围与方法

扫描位置：C:\Users\leibaihong\.codex、.cache、AppData\Local、AppData\Roaming、.config、Codex安装目录、CCSwitch相关目录。

说明：.config 目录因权限受限无法访问；部分目录为空或不存在。

## 二、审计结果

| 路径 | 类型 | 大小 | 可否迁移 | 建议 |
|---|---|---|---|---|
| C:\Users\leibaihong\AppData\Local\Temp | 临时目录 | 约2.18GB | ✅ 可迁移 | 迁移TEMP/TMP到 D:\AI\Codex\Temp 并建目录联接 |
| C:\Users\leibaihong\.cache\codex-runtimes | 运行时缓存 | 约1.08GB | ✅ 可迁移（需配置） | 迁移后更新工作区依赖路径/环境变量，或重建 |
| C:\Users\leibaihong\.codex\logs_2.sqlite | 会话日志库 | 约160MB | ✅ 可迁移 | 随 CODEX_HOME 迁移，需先退出Codex并备份 |
| C:\Users\leibaihong\.codex\.sandbox-bin | 沙箱工具 | 约366MB | ⚠️ 需验证 | 迁移后需重新校验沙箱权限 |
| C:\Users\leibaihong\.codex\visualizations | 可视化数据 | 约52MB | ✅ 可迁移 | 随 CODEX_HOME 迁移 |
| C:\Users\leibaihong\.codex\archived_sessions | 归档会话 | 约9MB | ✅ 可迁移 | 随 CODEX_HOME 迁移 |
| C:\Users\leibaihong\.codex\skills | Skills | 约1MB | ✅ 可迁移 | 迁移后 AGENTS/SKILL 路径需同步 |
| C:\Users\leibaihong\.codex\plugins | 插件 | 约6MB | ✅ 可迁移 | 随 CODEX_HOME 迁移 |
| C:\Users\leibaihong\.codex 其余（auth/config/sqlite/state等） | 配置与状态 | 数十MB | ⚠️ 需评估 | 部分文件（auth、global-state）建议保留或重映射，避免凭据失效 |
| C:\Users\leibaihong\AppData\Roaming\Codex | 应用数据 | 约107MB | ✅ 可迁移 | 应用数据目录迁移或联接 |
| C:\Users\leibaihong\AppData\Local\Codex | 本地应用数据 | 约36MB | ✅ 可迁移 | 迁移或联接 |
| C:\Program Files\WindowsApps\OpenAI.Codex* | 程序安装 | 系统管理 | ❌ 不迁移 | 由Windows/Store管理，禁止改动 |
| C:\Users\leibaihong\AppData\Local\com.ccswitch.desktop | CCSwitch数据 | 空/极小 | ✅ 可迁移 | 随用户数据迁移，需保持配置一致 |
| C:\Users\leibaihong\AppData\Roaming\com.ccswitch.desktop | CCSwitch数据 | 空/极小 | ✅ 可迁移 | 同上 |
| npm-cache / pip cache | 开发缓存 | 未发现/为空 | — | 后续按需配置缓存目录到D盘 |

## 三、结论

1. 主要可迁移空间：AppData\Local\Temp（约2.18GB）、.cache\codex-runtimes（约1.08GB）、.codex（约700MB）、Roaming/Local Codex（约143MB）。
2. 程序安装目录（WindowsApps）不可迁移；auth/全局状态等敏感文件迁移需谨慎。
3. 本阶段未创建 D:\AI\Codex，未执行任何迁移、删除或环境变量修改。

## 四、下一步（待确认）

Phase 2 迁移方案设计：备份策略、目录联接计划、环境变量（CODEX_HOME/TEMP/CACHE/WORKSPACE）、CCSwitch配置同步、验证清单。
