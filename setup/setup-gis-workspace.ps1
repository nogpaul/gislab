$ErrorActionPreference="Stop"
Write-Host "Using PowerShell $($PSVersionTable.PSVersion)"

# Workspace skeleton
$root="C:\GISLab"
$dirs="bin","setup","data","notebooks","src","web","db","docs","envs"
New-Item -Path $root -ItemType Directory -Force | Out-Null
$dirs | % { New-Item -Path "$root\$_" -ItemType Directory -Force | Out-Null }
[Environment]::SetEnvironmentVariable('GISLAB_HOME',$root,'User')
if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { throw "winget not found (install App Installer from Microsoft Store)" }

function Install($Id,$Name,$Scope="user"){
  $o = winget list --id $Id -e 2>$null
  if($LASTEXITCODE -eq 0 -and $o -match [regex]::Escape($Id)){ Write-Host "✔ $Name already installed"; return }
  Write-Host "→ Installing $Name ..."
  winget install --id $Id -e --source winget --scope $Scope --accept-package-agreements --accept-source-agreements
  if($LASTEXITCODE -ne 0){ throw "Install failed: $Id" }
}

$pkgs = @(
  @{ Id="Git.Git";                    Scope="user"    ; Name="Git" },
  @{ Id="GitHub.cli";                 Scope="machine" ; Name="GitHub CLI" },  # <-- changed to machine
  @{ Id="Microsoft.VisualStudioCode"; Scope="user"    ; Name="VS Code" },
  @{ Id="Python.Python.3.11";         Scope="user"    ; Name="Python 3.11" },
  @{ Id="OSGeo.QGIS";                 Scope="machine" ; Name="QGIS" },
  @{ Id="PostgreSQL.PostgreSQL.16";   Scope="machine" ; Name="PostgreSQL 16" }
)


$venv="C:\GISLab\envs\gis311"
if(!(Test-Path $venv)){
  $py = (Get-Command py -ErrorAction SilentlyContinue)
  $cmd = if($py){"py -3.11"}else{"python"}
  Write-Host "→ Creating venv at $venv ..."
  & $env:ComSpec /c "$cmd -m venv `"$venv`""
}

& "$venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip setuptools wheel

git config --global init.defaultBranch main
git config --global core.longpaths true
git config --global pull.rebase false
git config --global core.autocrlf true
git config --global core.editor "code --wait"

Write-Host "✅ Day 1 complete. Core tools installed, venv ready at $venv."
