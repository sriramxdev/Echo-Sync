<#
.SYNOPSIS
    Echo-Sync Phase 0 Environment Setup for Windows 11.
.DESCRIPTION
    Installs Pixi, clones the repository, runs pixi install --locked,
    and executes the required Phase 0 verification command.
#>

$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "   Echo-Sync Phase 0: Environment Setup  " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# 1. Verify Git
Write-Host "`n[1/4] Checking Git..." -ForegroundColor Yellow
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Git is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Install Git for Windows from https://git-scm.com/ and re-run."
    exit 1
}
Write-Host "  -> Git detected: $(git --version)" -ForegroundColor Green

# 2. Install Pixi (if not present)
Write-Host "`n[2/4] Checking Pixi..." -ForegroundColor Yellow

function Update-PixiPath {
    $PixiCandidates = @(
        "$env:USERPROFILE\.pixi\bin",
        "$env:LocalAppData\pixi\bin"
    )
    foreach ($Path in $PixiCandidates) {
        if (Test-Path $Path) {
            if ($env:PATH -notlike "*$Path*") {
                $env:PATH = "$Path;$env:PATH"
            }
        }
    }
}

Update-PixiPath
$PixiCmd = Get-Command pixi -ErrorAction SilentlyContinue

if (-not $PixiCmd) {
    Write-Host "  -> Pixi not found. Installing..." -ForegroundColor Magenta
    powershell -ExecutionPolicy Bypass -Command "irm -useb https://pixi.sh/install.ps1 | iex"
    Update-PixiPath
    $PixiCmd = Get-Command pixi -ErrorAction SilentlyContinue
    
    if (-not $PixiCmd) {
        Write-Host "[ERROR] Pixi installed but not found in PATH. Please restart PowerShell and re-run." -ForegroundColor Red
        exit 1
    }
}
Write-Host "  -> Pixi detected: $(pixi --version)" -ForegroundColor Green

# 3. Clone Repository
Write-Host "`n[3/4] Cloning repository..." -ForegroundColor Yellow
$RepoUrl = "https://github.com/sriramxdev/Echo-Sync.git"
$RepoDir = "Echo-Sync"

if (Test-Path "pixi.toml") {
    Write-Host "  -> Already inside Echo-Sync repository directory." -ForegroundColor Green
} else {
    if (Test-Path $RepoDir) {
        Write-Host "  -> Found existing '$RepoDir' directory. Navigating inside..." -ForegroundColor Gray
        Set-Location $RepoDir
    } else {
        Write-Host "  -> Cloning from $RepoUrl..." -ForegroundColor Gray
        git clone $RepoUrl
        Set-Location $RepoDir
    }
}

# 4. Initialize Local Dependencies
Write-Host "`n[4/4] Running: pixi install --locked..." -ForegroundColor Yellow
pixi install --locked
Write-Host "  -> Pixi dependencies locked and installed." -ForegroundColor Green

# Verification Step
Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host " Running Phase 0 Verification...        " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

pixi run python -c "import sys, platform; print('--- VERIFIED ---'); print('OS:', platform.system(), platform.release()); print('Python:', sys.version.split()[0]); print('Status: READY')"
