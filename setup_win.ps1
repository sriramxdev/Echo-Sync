<#
.SYNOPSIS
    Echo-Sync Automated Onboarding Script for Windows 11.
.DESCRIPTION
    1. Verifies Git installation.
    2. Installs Pixi package manager (if not present) and updates session PATH.
    3. Clones the Echo-Sync repository directly from GitHub.
    4. Runs `pixi install` to create the isolated environment.
    5. Runs unit tests to verify baseline integrity.
    6. Checks out the assigned Linear feature branch.
#>

[CmdletBinding()]
param (
    [string]$IssueTag = ""
)

$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "   Echo-Sync Team Onboarding Setup      " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# ---------------------------------------------------------------------------
# 1. Verify Git
# ---------------------------------------------------------------------------
Write-Host "`n[1/6] Checking Git..." -ForegroundColor Yellow
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Git is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Git for Windows from https://git-scm.com/ and re-run this script."
    exit 1
}
Write-Host "  -> Git detected: $(git --version)" -ForegroundColor Green

# ---------------------------------------------------------------------------
# 2. Check & Install Pixi
# ---------------------------------------------------------------------------
Write-Host "`n[2/6] Checking Pixi Package Manager..." -ForegroundColor Yellow

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
    Write-Host "  -> Pixi not found. Downloading & installing Pixi..." -ForegroundColor Magenta
    powershell -ExecutionPolicy Bypass -Command "irm -useb https://pixi.sh/install.ps1 | iex"
    Update-PixiPath
    $PixiCmd = Get-Command pixi -ErrorAction SilentlyContinue
    
    if (-not $PixiCmd) {
        Write-Host "[ERROR] Pixi installed but not found in PATH." -ForegroundColor Red
        Write-Host "Please restart PowerShell and re-run this script."
        exit 1
    }
}
Write-Host "  -> Pixi detected: $(pixi --version)" -ForegroundColor Green

# ---------------------------------------------------------------------------
# 3. Clone Repository
# ---------------------------------------------------------------------------
Write-Host "`n[3/6] Setting up repository..." -ForegroundColor Yellow
$RepoUrl = "https://github.com/sriramxdev/Echo-Sync.git"
$RepoDir = "Echo-Sync"

# If already inside the repo folder, skip cloning
if (Test-Path "pixi.toml") {
    Write-Host "  -> Already inside Echo-Sync repository." -ForegroundColor Green
} else {
    if (Test-Path $RepoDir) {
        Write-Host "  -> Found existing '$RepoDir' directory. Navigating inside..." -ForegroundColor Gray
        Set-Location $RepoDir
    } else {
        Write-Host "  -> Cloning repository from $RepoUrl..." -ForegroundColor Gray
        git clone $RepoUrl
        Set-Location $RepoDir
    }
}

# ---------------------------------------------------------------------------
# 4. Install Isolated Pixi Environment
# ---------------------------------------------------------------------------
Write-Host "`n[4/6] Resolving and installing dependencies via Pixi..." -ForegroundColor Yellow
pixi install
Write-Host "  -> Environment locked and ready." -ForegroundColor Green

# ---------------------------------------------------------------------------
# 5. Run Verification Tests
# ---------------------------------------------------------------------------
Write-Host "`n[5/6] Verifying schema and validation tests..." -ForegroundColor Yellow
pixi run python -m unittest discover -s tests -p "*test*.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "[WARNING] Unit tests flagged an issue. Check output above." -ForegroundColor Red
} else {
    Write-Host "  -> All schema tests passed successfully!" -ForegroundColor Green
}

# ---------------------------------------------------------------------------
# 6. Branch Configuration
# ---------------------------------------------------------------------------
Write-Host "`n[6/6] Branch Setup..." -ForegroundColor Yellow
if (-not $IssueTag) {
    $IssueTag = Read-Host "Enter your assigned Linear Issue tag (e.g. ECHO-12 or press Enter to stay on main)"
}

if ($IssueTag.Trim() -ne "") {
    # Sanitize tag format: e.g. ECHO-12 -> feat/ECHO-12
    $BranchName = if ($IssueTag -like "feat/*") { $IssueTag } else { "feat/$IssueTag" }
    
    Write-Host "  -> Syncing main branch..." -ForegroundColor Gray
    git checkout main
    git pull origin main
    
    Write-Host "  -> Switching to branch '$BranchName'..." -ForegroundColor Magenta
    git checkout -B $BranchName
    Write-Host "  -> Active branch: $BranchName" -ForegroundColor Green
} else {
    Write-Host "  -> Retaining current branch." -ForegroundColor Gray
}

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host "   Setup Complete! Happy Coding.                        " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Next steps:"
Write-Host "  - Open in VS Code:        code ."
Write-Host "  - Run scripts with env:   pixi run python <script.py>"
Write-Host "  - Open interactive shell: pixi shell"
