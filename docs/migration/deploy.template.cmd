@echo off
set "SCRIPT_DIR=%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$dir=$env:SCRIPT_DIR; $ws=New-Object -ComObject WScript.Shell; $desk=$ws.SpecialFolders('Desktop'); foreach($n in @('Codex迁移启动.cmd','Codex回滚启动.cmd')){ $src=Join-Path $dir $n; if(Test-Path -LiteralPath $src){ $lnk=$ws.CreateShortcut((Join-Path $desk ($n -replace '\.cmd$','.lnk'))); $lnk.TargetPath=$env:COMSPEC; $lnk.Arguments='/c ""'+$src+'""'; $lnk.WorkingDirectory=(Split-Path $src); $lnk.IconLocation='%SystemRoot%\System32\shell32.dll,13'; $lnk.Save(); Write-Host ('已创建快捷方式: '+$lnk.FullName) } else { Write-Host ('未找到: '+$src) } }"
pause
