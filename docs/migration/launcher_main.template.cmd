@echo off
net session >nul 2>&1
if %errorlevel%==0 goto run
echo 检测到非管理员权限，正在请求提升...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
exit /b
:run
if not exist "D:\AI\Codex\MigrationLogs" mkdir "D:\AI\Codex\MigrationLogs"
set "LOG=D:\AI\Codex\MigrationLogs\launcher_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log"
echo ================================================
echo  Codex C盘迁移至D盘 一键启动
echo  日志: %LOG%
echo ================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Codex_C盘迁移至D盘执行脚本.ps1" > "%LOG%" 2>&1
echo.
echo 执行结束，退出码: %errorlevel%
echo.
echo ---- 日志尾部 ----
powershell -NoProfile -Command "Get-Content -LiteralPath '%LOG%' -Tail 20"
echo.
pause
