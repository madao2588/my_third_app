param(
  [int]$BackendPort = 8000,
  [int]$FrontendPort = 8093
)

$ErrorActionPreference = "Stop"

function Get-ListeningPids([int]$Port) {
  $matches = netstat -ano -p tcp | Select-String "LISTENING\s+\d+$" | Select-String ":$Port\s"
  $pids = @()
  foreach ($line in $matches) {
    $parts = ($line.ToString().Trim() -split "\s+")
    if ($parts.Length -gt 0) {
      $portPid = $parts[-1]
      if ($portPid -match "^\d+$" -and $portPid -ne "0") {
        $pids += [int]$portPid
      }
    }
  }
  return $pids | Select-Object -Unique
}

function Stop-PortProcesses([int]$Port) {
  $pids = Get-ListeningPids -Port $Port
  foreach ($portPid in $pids) {
    try {
      taskkill /PID $portPid /F | Out-Null
      Write-Host "Stopped PID $portPid on port $Port"
    } catch {
      Write-Warning "Failed to stop PID $portPid on port ${Port}: $($_.Exception.Message)"
    }
  }
}

$crawlerRoot = Split-Path $PSScriptRoot -Parent
$workspaceRoot = Split-Path $crawlerRoot -Parent
$serverDir = Join-Path $crawlerRoot "server"
$frontendDir = Join-Path $crawlerRoot "frontend"
$venvPython = Join-Path $workspaceRoot ".venv\Scripts\python.exe"

if (!(Test-Path $venvPython)) {
  throw "Missing venv python: $venvPython"
}

if (!(Get-Command flutter -ErrorAction SilentlyContinue)) {
  throw "Flutter command not found in PATH"
}

Write-Host "Cleaning existing listeners..."
Stop-PortProcesses -Port $BackendPort
Stop-PortProcesses -Port $FrontendPort

Write-Host "Starting backend on http://127.0.0.1:$BackendPort ..."
$backendCommand = "Set-Location '$serverDir'; & '$venvPython' -m uvicorn main:app --host 127.0.0.1 --port $BackendPort"
$backendProc = Start-Process -FilePath "powershell" -ArgumentList @("-NoExit", "-Command", $backendCommand) -WindowStyle Minimized -PassThru

Write-Host "Starting frontend on http://127.0.0.1:$FrontendPort ..."
$frontendCommand = "Set-Location '$frontendDir'; flutter run -d web-server --web-port $FrontendPort"
$frontendProc = Start-Process -FilePath "powershell" -ArgumentList @("-NoExit", "-Command", $frontendCommand) -WindowStyle Minimized -PassThru

Write-Host ""
Write-Host "Backend PID:  $($backendProc.Id)"
Write-Host "Frontend PID: $($frontendProc.Id)"
Write-Host "Backend URL:  http://127.0.0.1:$BackendPort"
Write-Host "Frontend URL: http://127.0.0.1:$FrontendPort"
