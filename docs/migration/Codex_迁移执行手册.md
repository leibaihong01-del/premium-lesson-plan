# Codex C盘迁移至D盘：执行手册

日期：2026-08-02    状态：脚本已生成，未执行

## 一、前置条件

1. 真实Windows管理员用户；
2. 已退出 Codex 与 CCSwitch；
3. D盘可用空间 ≥ 5GB；
4. 已阅读并确认迁移方案。

## 二、执行步骤

1. 以管理员身份打开PowerShell；
2. 执行主脚本：
   `powershell -ExecutionPolicy Bypass -File Codex_C盘迁移至D盘执行脚本.ps1`
3. 按提示两次输入 `YES` 确认；
4. 等待脚本完成并查看日志 `D:\AI\Codex\MigrationLogs`；
5. 重启Codex/CCSwitch验证。

脚本新增：

1. 迁移前磁盘占用预估：统计全部待迁移目录大小与文件数，检查D盘空间，不足自动终止；
2. CCSwitch保护：自动检测CCSwitch目录并备份配置/API配置/模型路由配置；
3. 迁移前报告：生成 `Migration_Before_Report.md`（用户、路径映射、文件数、总大小、环境变量）。

## 三、迁移后验证

- Codex启动正常、CCSwitch正常、CourseAgent正常、AGENTS.md/skills正常读取；
- 新任务数据写入D盘；
- C盘对应目录为Junction，指向D盘。

## 四、回滚

如验证失败，退出应用后执行：
`powershell -ExecutionPolicy Bypass -File Codex_迁移回滚脚本.ps1`

## 五、删除.bak（人工执行）

确认运行正常一段时间后，由人工删除 `*.codex.bak` 等 `.bak` 目录，脚本不会自动删除。
