#requires -RunAsAdministrator
<#
Codex C: to D: migration script (generated only, not executed).
Features: preflight, disk usage estimate, CCSwitch protection, pre-migration report,
double YES confirmation, .bak rename, rollback support. Delete operations disabled.
Usage:
  1. Open PowerShell as Administrator.
  2. Quit Codex and CCSwitch.
  3. Run: powershell -ExecutionPolicy Bypass -File "this script.ps1"
#>

param(
    [string]$TargetRoot = "D:\AI\Codex",
    [switch]$SetCodexHome
)

$ErrorActionPreference = "Stop"
$LogRoot = Join-Path $TargetRoot "MigrationLogs"
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$LogFile = Join-Path $LogRoot ("migration_" + $Timestamp + ".log")
New-Item -ItemType Directory -Force -Path $LogRoot | Out-Null

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $line = "{0} [{1}] {2}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Level, $Message
    Add-Content -LiteralPath $LogFile -Value $line -Encoding UTF8
    Write-Host $line
}

function Confirm-Step {
    param([string]$Message)
    $r = Read-Host ($Message + " (type YES to continue)")
    if ($r -ne "YES") { throw "User cancelled: $Message" }
}

function Test-Admin {
    $id = [Security.Principal.WindowsIdentity]::GetCurrent()
    return (New-Object Security.Principal.WindowsPrincipal($id)).IsInRole(
        [Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Test-CodexRunning {
    return [bool](Get-Process -ErrorAction SilentlyContinue |
        Where-Object { $_.ProcessName -match 'codex|ccswitch' })
}

function Get-FolderSize {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    try {
        return (Get-ChildItem -LiteralPath $Path -Recurse -Force -File -ErrorAction SilentlyContinue |
            Measure-Object Length -Sum).Sum
    } catch { return $null }
}

function Get-FileCount {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return 0 }
    try {
        return (Get-ChildItem -LiteralPath $Path -Recurse -Force -File -ErrorAction SilentlyContinue).Count
    } catch { return 0 }
}

function Copy-WithInheritance {
    param([string]$Src, [string]$Dst)
    New-Item -ItemType Directory -Force -Path (Split-Path $Dst -Parent) | Out-Null
    Copy-Item -LiteralPath $Src -Destination $Dst -Recurse -Force
    Write-Log ("Copied: " + $Src + " -> " + $Dst)
}

function New-Junction {
    param([string]$Link, [string]$Target)
    if (Test-Path -LiteralPath $Link) {
        throw "Junction target already exists: $Link"
    }
    New-Item -ItemType Junction -Path $Link -Target $Target | Out-Null
    Write-Log ("Junction created: " + $Link + " -> " + $Target)
}

$Map = @()
$Map += @{ C = "C:\Users\leibaihong\.codex"; D = (Join-Path $TargetRoot "UserData\codex-home") }
$Map += @{ C = "C:\Users\leibaihong\.cache\codex-runtimes"; D = (Join-Path $TargetRoot "Cache\codex-runtimes") }
$Map += @{ C = "C:\Users\leibaihong\AppData\Roaming\Codex"; D = (Join-Path $TargetRoot "UserData\RoamingCodex") }
$Map += @{ C = "C:\Users\leibaihong\AppData\Local\Codex"; D = (Join-Path $TargetRoot "UserData\LocalCodex") }
$Map += @{ C = "C:\Users\leibaihong\AppData\Local\com.ccswitch.desktop"; D = (Join-Path $TargetRoot "Core\ccswitch-local") }
$Map += @{ C = "C:\Users\leibaihong\AppData\Roaming\com.ccswitch.desktop"; D = (Join-Path $TargetRoot "Core\ccswitch-roaming") }

$Sensitive = @(
    "C:\Users\leibaihong\.codex\auth.json",
    "C:\Users\leibaihong\.codex\.codex-global-state.json",
    "C:\Users\leibaihong\.codex\config.toml",
    "C:\Users\leibaihong\.codex\logs_2.sqlite",
    "C:\Users\leibaihong\.codex\state_5.sqlite"
)

function Find-CCSwitchDirs {
    $found = @()
    $candidates = @(
        "C:\Users\leibaihong\AppData\Local\Programs\CCSwitch",
        "C:\Users\leibaihong\AppData\Local\com.ccswitch.desktop",
        "C:\Users\leibaihong\AppData\Roaming\com.ccswitch.desktop",
        "C:\Program Files\CCSwitch",
        "C:\Program Files (x86)\CCSwitch"
    )
    foreach ($c in $candidates) {
        if (Test-Path -LiteralPath $c) { $found += $c }
    }
    $cmd = Get-Command ccswitch -ErrorAction SilentlyContinue
    if ($cmd) { $found += $cmd.Source }
    return ($found | Select-Object -Unique)
}

function Step-Preflight {
    Write-Log "==== Preflight ===="
    if (-not (Test-Admin)) { throw "Must run as Administrator" }
    if (Test-CodexRunning) { throw "Codex/CCSwitch is running. Quit first." }
    $who = whoami
    Write-Log ("Current user: " + $who)
    if ($who -notmatch "leibaihong") { Write-Log "Warning: user is not leibaihong, verify paths" "WARN" }
    foreach ($m in $Map) {
        Write-Log ("C path: " + $m.C + " exists=" + (Test-Path -LiteralPath $m.C) +
                   " size=" + (Get-FolderSize $m.C) + " files=" + (Get-FileCount $m.C))
    }
    $cc = Find-CCSwitchDirs
    foreach ($c in $cc) { Write-Log ("CCSwitch found: " + $c) }
    if ($cc.Count -eq 0) { Write-Log "CCSwitch dirs not detected" "WARN" }
}

function Step-Estimate {
    Write-Log "==== Disk usage estimate ===="
    $total = 0
    foreach ($m in $Map) {
        $sz = Get-FolderSize $m.C
        if ($sz) { $total += $sz }
    }
    $totalGB = [math]::Round($total / 1GB, 2)
    $d = Get-PSDrive D -ErrorAction SilentlyContinue
    if (-not $d) { throw "D: drive not readable. Abort." }
    $freeGB = [math]::Round($d.Free / 1GB, 2)
    $needGB = [math]::Round($totalGB + 0.5, 2)
    Write-Log ("Total size to migrate GB: " + $totalGB)
    Write-Log ("D free GB: " + $freeGB + " needed GB: " + $needGB)
    if ($freeGB -lt $needGB) {
        throw ("Not enough free space on D:. Need " + $needGB + " GB, have " + $freeGB + " GB. Abort.")
    }
    Step-Report -TotalBytes $total -FreeGB $freeGB
}

function Step-Report {
    param([long]$TotalBytes, [double]$FreeGB)
    $report = Join-Path $LogRoot "Migration_Before_Report.md"
    $lines = @()
    $lines += "# Migration Before Report"
    $lines += ""
    $lines += ("Time: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
    $lines += ("User: " + (whoami))
    $lines += ("TargetRoot: " + $TargetRoot)
    $lines += ("Total size bytes: " + $TotalBytes)
    $lines += ("Total size GB: " + [math]::Round($TotalBytes / 1GB, 2))
    $lines += ("D free GB: " + $FreeGB)
    $lines += ""
    $lines += "## Path mapping"
    $lines += ""
    $lines += "| C path | D target | files | size bytes |"
    $lines += "|---|---|---|---|"
    foreach ($m in $Map) {
        $sz = Get-FolderSize $m.C
        if (-not $sz) { $sz = 0 }
        $lines += ("| " + $m.C + " | " + $m.D + " | " + (Get-FileCount $m.C) + " | " + $sz + " |")
    }
    $lines += ""
    $lines += "## Environment variables (current user)"
    $lines += ""
    $lines += "| Name | Current value |"
    $lines += "|---|---|"
    foreach ($k in @("TEMP","TMP","NPM_CONFIG_CACHE","PIP_CACHE_DIR","CODEX_HOME")) {
        $v = [Environment]::GetEnvironmentVariable($k, "User")
        $lines += ("| " + $k + " | " + $v + " |")
    }
    $lines += ""
    $lines += "## CCSwitch detection"
    $lines += ""
    foreach ($c in (Find-CCSwitchDirs)) { $lines += ("- " + $c) }
    $lines | Set-Content -LiteralPath $report -Encoding UTF8
    Write-Log ("Report written: " + $report)
}

function Step-Backup {
    $bak = Join-Path $TargetRoot ("Backup\" + $Timestamp)
    New-Item -ItemType Directory -Force -Path $bak | Out-Null
    foreach ($f in $Sensitive) {
        if (Test-Path -LiteralPath $f) {
            $dst = Join-Path $bak (Split-Path $f -Leaf)
            Copy-Item -LiteralPath $f -Destination $dst -Force
            Write-Log ("Backed up: " + $f + " -> " + $dst)
        }
    }
    Write-Log ("Backup dir: " + $bak)
}

function Step-CCSwitchBackup {
    $ccbak = Join-Path $TargetRoot ("Backup\" + $Timestamp + "\ccswitch")
    New-Item -ItemType Directory -Force -Path $ccbak | Out-Null
    $files = @()
    foreach ($c in (Find-CCSwitchDirs)) {
        if (Test-Path -LiteralPath $c -PathType Container) {
            $files += Get-ChildItem -LiteralPath $c -Recurse -Force -File -ErrorAction SilentlyContinue |
                Where-Object { $_.Extension -match '\.(json|toml|yaml|yml|env|conf|log)$' }
        }
    }
    foreach ($f in $files) {
        $rel = $f.FullName -replace '[:\\]', '_'
        Copy-Item -LiteralPath $f.FullName -Destination (Join-Path $ccbak $rel) -Force
    }
    Write-Log ("CCSwitch config backed up: " + $ccbak + " files=" + $files.Count)
}

function Step-CreateTree {
    $dirs = @("Core\config","Core\plugins","Core\extensions","UserData\sessions",
              "UserData\history","UserData\memory","UserData\logs","Cache","Workspace",
              "Skills","Temp","PythonEnv","NodeCache","Backup","MigrationLogs")
    foreach ($d in $dirs) {
        New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot $d) | Out-Null
    }
    Write-Log "Directory tree created"
}

function Step-CopyAndJunction {
    foreach ($m in $Map) {
        if (-not (Test-Path -LiteralPath $m.C)) {
            Write-Log ("Skip missing: " + $m.C) "WARN"
            continue
        }
        if (Test-Path -LiteralPath $m.D) {
            Write-Log ("Target exists, skip copy: " + $m.D) "WARN"
        } else {
            Copy-WithInheritance $m.C $m.D
        }
        $bak = $m.C + ".bak"
        if (-not (Test-Path -LiteralPath $bak)) {
            $newName = (Split-Path $m.C -Leaf) + ".bak"
            Rename-Item -LiteralPath $m.C -NewName $newName
            Write-Log ("Renamed: " + $m.C + " -> " + $bak)
        } else {
            Write-Log (".bak already exists, skip rename: " + $bak) "WARN"
        }
        New-Junction -Link $m.C -Target $m.D
    }
}

function Step-Env {
    $vars = @{
        "TEMP" = Join-Path $TargetRoot "Temp"
        "TMP"  = Join-Path $TargetRoot "Temp"
        "NPM_CONFIG_CACHE" = Join-Path $TargetRoot "NodeCache"
        "PIP_CACHE_DIR"    = Join-Path $TargetRoot "Cache\pip"
    }
    if ($SetCodexHome) { $vars["CODEX_HOME"] = Join-Path $TargetRoot "UserData\codex-home" }
    foreach ($k in $vars.Keys) {
        [Environment]::SetEnvironmentVariable($k, $vars[$k], "User")
        Write-Log ("User env set: " + $k + " = " + $vars[$k])
    }
}

function Step-Verify {
    Write-Log "==== Verification ===="
    foreach ($m in $Map) {
        if (-not (Test-Path -LiteralPath $m.C)) {
            Write-Log ("Verify fail, path missing: " + $m.C) "ERROR"
            continue
        }
        $item = Get-Item -LiteralPath $m.C -Force
        $isLink = ($item.LinkType -eq "Junction")
        Write-Log ("Verify: " + $m.C + " Junction=" + $isLink + " accessible=" + (Test-Path -LiteralPath $m.C))
        if (-not $isLink) { Write-Log ("Verify fail: " + $m.C) "ERROR" }
    }
}

try {
    Write-Log "==== Codex C: to D: migration started ===="
    Step-Preflight
    Step-Estimate
    Confirm-Step "Preflight and estimate done. Continue?"
    Step-Backup
    Step-CCSwitchBackup
    Step-CreateTree
    Confirm-Step "Backup and tree done. Continue with copy/rename?"
    Step-CopyAndJunction
    Step-Env
    Step-Verify
    Write-Log "==== Migration done ===="
    Write-Log ("Log: " + $LogFile)
    Write-Log "Note: delete .bak directories manually after verification."
}
catch {
    Write-Log ("Migration failed: " + $_.Exception.Message) "ERROR"
    Write-Log "See rollback script Codex_迁移回滚脚本.ps1"
    exit 1
}
