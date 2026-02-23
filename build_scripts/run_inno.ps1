param(
    [string]$ISCCPath,
    [string]$IssFile = "installer\csv_merger_installer.iss"
)

function Find-ISCC {
    $candidates = @(
        "$env:ProgramFiles\Inno Setup 6\ISCC.exe",
        "$env:ProgramFiles(x86)\Inno Setup 6\ISCC.exe",
        "C:\Program Files\Inno Setup 6\ISCC.exe",
        "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    )
    foreach ($p in $candidates) {
        if (Test-Path $p) { return $p }
    }
    return $null
}

if (-not $ISCCPath) {
    $ISCCPath = Find-ISCC
}

if (-not $ISCCPath -or -not (Test-Path $ISCCPath)) {
    Write-Host "ISCC not found. Please provide the path to ISCC.exe when running this script, e.g.:" -ForegroundColor Yellow
    Write-Host ".\run_inno.ps1 -ISCCPath 'C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe'" -ForegroundColor Cyan
    exit 1
}

$fullIss = Join-Path (Get-Location) $IssFile
if (-not (Test-Path $fullIss)) {
    Write-Host "Installer script not found: $fullIss" -ForegroundColor Red
    exit 1
}

Write-Host "Running ISCC: $ISCCPath with $fullIss"
& $ISCCPath $fullIss
if ($LASTEXITCODE -ne 0) {
    Write-Host "ISCC failed with exit code $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "Installer compiled successfully." -ForegroundColor Green
