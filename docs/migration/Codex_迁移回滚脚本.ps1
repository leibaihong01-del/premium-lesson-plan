#requires -RunAsAdministrator
<#
Codex migration rollback script: remove junctions, restore .bak, clear env vars.
No data is deleted. Quit Codex/CCSwitch first.
#>
$ErrorActionPreference = "Stop"

function Confirm-Step {
    param([string]$Message)
    $r = Read-Host ($Message + " (type YES to continue)")
    if ($r -ne "YES") { throw "User cancelled" }
}

$links = @(
    "C:\Users\leibaihong\.codex",
    "C:\Users\leibaihong\.cache\codex-runtimes",
    "C:\Users\leibaihong\AppData\Roaming\Codex",
    "C:\Users\leibaihong\AppData\Local\Codex",
    "C:\Users\leibaihong\AppData\Local\com.ccswitch.desktop",
    "C:\Users\leibaihong\AppData\Roaming\com.ccswitch.desktop"
)

Confirm-Step "Rollback removes junctions and restores .bak. Continue?"
foreach ($link in $links) {
    if (Test-Path -LiteralPath $link) {
        $item = Get-Item -LiteralPath $link -Force
        if ($item.LinkType -eq "Junction") {
            Remove-Item -LiteralPath $link -Force
            Write-Host ("Removed junction: " + $link)
        }
    }
    $bak = $link + ".bak"
    if (Test-Path -LiteralPath $bak) {
        $newName = Split-Path $link -Leaf
        Rename-Item -LiteralPath $bak -NewName $newName
        Write-Host ("Restored: " + $bak + " -> " + $link)
    }
}
foreach ($k in @("TEMP","TMP","NPM_CONFIG_CACHE","PIP_CACHE_DIR","CODEX_HOME")) {
    [Environment]::SetEnvironmentVariable($k, $null, "User")
    Write-Host ("Cleared user env: " + $k)
}
Write-Host "Rollback done. D: data kept, nothing deleted."
