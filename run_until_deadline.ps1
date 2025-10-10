param(
  [double]$TStart       = 10.0,
  [double]$Hours        = 12.0,
  [string]$OutRoot      = "big_run_final",
  [int]   $Dps          = 60,
  [Nullable[double]]$Rho = $null,
  [double]$MinBlock     = 5.0,
  [double]$MaxBlock     = 50.0,
  [double]$Mult         = 8.0,
  [string]$Python       = "python",
  [string]$LogDir       = ".\logs",
  [switch]$AutoRestart,
  [int]$RestartDelaySec = 5
)

function F([double]$x) {
  $ci = [System.Globalization.CultureInfo]::InvariantCulture
  return $x.ToString("G", $ci)
}

function Build-Args([double]$hoursRemaining) {
  $args = @(
    "batch_until_deadline.py",
    "--tstart",    (F $TStart),
    "--hours",     (F $hoursRemaining),
    "--outroot",   $OutRoot,
    "--dps",       $Dps,
    "--min_block", (F $MinBlock),
    "--max_block", (F $MaxBlock),
    "--mult",      (F $Mult)
  )
  if ($null -ne $Rho) { $args += @("--rho", (F $Rho)) }
  ,$args
}

$ErrorActionPreference = "Stop"

Write-Host "[ps1] Working dir: $((Get-Location).Path)"
Write-Host ("[ps1] Params  TStart={0}  Hours={1}  OutRoot={2}  Dps={3}  MinBlock={4}  MaxBlock={5}  Mult={6}  Rho={7}" -f `
  (F $TStart), (F $Hours), $OutRoot, $Dps, (F $MinBlock), (F $MaxBlock), (F $Mult), ($(if ($null -ne $Rho) { F $Rho } else { "null" })))

if (-not (Test-Path -LiteralPath $LogDir)) {
  New-Item -ItemType Directory -Path $LogDir | Out-Null
}
$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = Join-Path $LogDir "run_$ts.log"
Start-Transcript -Path $logFile -Append | Out-Null

$start    = Get-Date
$deadline = $start.AddHours($Hours)
Write-Host "[ps1] Starting batch_until_deadline.py ..."
Write-Host ("[ps1] batch window: {0}  ->  {1}  (total: {2} h)" -f `
  $start.ToString("s"), $deadline.ToString("s"), (('{0:N2}' -f $Hours)))

while ($true) {
  $remaining = ($deadline - (Get-Date)).TotalHours
  if ($remaining -le 0) {
    Write-Host "[ps1] Deadline reached. Exiting." -ForegroundColor Green
    break
  }
  $remainingCapped = [Math]::Max($remaining, 0.05)
  $argv = Build-Args -hoursRemaining $remainingCapped

  Write-Host "[ps1] CMD: $Python $($argv -join ' ')"
  Write-Host ("[ps1] Run for ~{0} h (remaining ~{1} h)" -f (('{0:N2}' -f $remainingCapped)), (('{0:N2}' -f $remaining)))

  & $Python $argv
  $code = $LASTEXITCODE

  if ($code -eq 0) {
    Write-Host "[ps1] Python exited with code 0." -ForegroundColor Green
  } else {
    Write-Host "[ps1] Python exited with code $code" -ForegroundColor Yellow
    if (-not $AutoRestart) {
      Write-Host "[ps1] AutoRestart=OFF -> Abbruch." -ForegroundColor Red
      Stop-Transcript | Out-Null
      exit $code
    }
    Write-Host "[ps1] AutoRestart=ON -> wait $RestartDelaySec s and restart…" -ForegroundColor Yellow
    Start-Sleep -Seconds $RestartDelaySec
  }
}

Stop-Transcript | Out-Null
Write-Host "[ps1] Done. Logs: $logFile"
