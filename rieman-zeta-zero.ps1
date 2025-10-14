# rieman-zeta-zero.ps1  (Windows PowerShell 5.1+ / PowerShell 7)
# Orchestrates:
#   1) batch_until_deadline.py
#   2) turing_check.py (zeros-root + CSV out)
#   3) sieve_from_zeros_psi_rigorous.py

Set-StrictMode -Version Latest

# ---------------- UTF-8 / Console & Python ----------------
try {
  # Für Windows PowerShell 5.1/WT/CMD: auf UTF-8 schalten
  $null = cmd /c chcp 65001
} catch {}
try {
  [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
  [Console]::InputEncoding  = [System.Text.UTF8Encoding]::new($false)
} catch {}

# Erzwinge UTF-8 für Python-StdIO (umgeht cp1252-Fehler bei '≈' etc.)
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUTF8       = '1'

# ---------------- Helpers ----------------
function TSUTC { ([DateTime]::UtcNow.ToString('HH:mm:ss')) }

function Ensure-Dir([string]$Path) {
  if (-not (Test-Path -LiteralPath $Path)) {
    New-Item -ItemType Directory -Path $Path -Force | Out-Null
  }
}

function Get-PyExe {
  $candidates = @()
  if ($env:PYTHON)       { $candidates += $env:PYTHON }
  if ($env:CONDA_PREFIX) { $candidates += (Join-Path $env:CONDA_PREFIX 'python.exe') }
  if ($env:VIRTUAL_ENV)  { $candidates += (Join-Path $env:VIRTUAL_ENV 'Scripts\python.exe') }
  $candidates += @('py.exe','python.exe','python3.exe','python')
  foreach ($c in $candidates) {
    $cmd = Get-Command $c -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.Source) { return $cmd.Source }
  }
  throw "No Python interpreter found. Install Python 3.10+ and ensure it's on PATH."
}

function Ask-Number([string]$prompt, [string]$default, [double]$min, [bool]$isInt=$false) {
  $ci = [System.Globalization.CultureInfo]::InvariantCulture
  while ($true) {
    $raw = Read-Host $prompt
    if ([string]::IsNullOrWhiteSpace($raw)) { $raw = $default }
    $raw = $raw.Trim().Replace(',', '.')
    if ($isInt) {
      [int]$val = 0
      if ([int]::TryParse($raw, [ref]$val) -and $val -ge $min) { return $val }
    } else {
      [double]$val = 0.0
      if ([double]::TryParse($raw, [System.Globalization.NumberStyles]::Float, $ci, [ref]$val) -and $val -ge $min) { return $val }
    }
    Write-Host "Invalid input. Must be ≥ $min." -ForegroundColor Yellow
  }
}

# Run native process; stream stdout/stderr live in Konsole + Log; gib Exitcode zurück
function Invoke-Native {
  param(
    [Parameter(Mandatory=$true)][string]$Exe,
    [Parameter(Mandatory=$true)][string[]]$Args,
    [Parameter(Mandatory=$true)][string]$LogPath
  )
  Write-Host ""
  Write-Host ">> $Exe $($Args -join ' ')" -ForegroundColor DarkGray

  $psi = New-Object System.Diagnostics.ProcessStartInfo
  $psi.FileName = $Exe
  $psi.Arguments = [string]::Join(' ', ($Args | ForEach-Object {
    if ($_ -match '\s|"') { '"' + ($_ -replace '"','\"') + '"' } else { $_ }
  }))
  $psi.RedirectStandardOutput = $true
  $psi.RedirectStandardError  = $true
  $psi.UseShellExecute = $false
  $psi.CreateNoWindow   = $true
  # UTF-8 sicherheitshalber auch auf Prozessebene:
  $psi.StandardOutputEncoding = [System.Text.UTF8Encoding]::new($false)
  $psi.StandardErrorEncoding  = [System.Text.UTF8Encoding]::new($false)

  $p = New-Object System.Diagnostics.Process
  $p.StartInfo = $psi

  [void]$p.Start()
  $out = $p.StandardOutput
  $err = $p.StandardError

  $logWriter = [System.IO.StreamWriter]::new($LogPath, $false, [System.Text.Encoding]::UTF8)

  while (-not $p.HasExited) {
    while (-not $out.EndOfStream) { $line = $out.ReadLine(); $logWriter.WriteLine($line); Write-Host $line }
    while (-not $err.EndOfStream) { $line = $err.ReadLine(); $logWriter.WriteLine($line); Write-Host $line }
    Start-Sleep -Milliseconds 30
  }
  while (-not $out.EndOfStream) { $line = $out.ReadLine(); $logWriter.WriteLine($line); Write-Host $line }
  while (-not $err.EndOfStream) { $line = $err.ReadLine(); $logWriter.WriteLine($line); Write-Host $line }

  $exit = $p.ExitCode
  $logWriter.Dispose()
  return $exit
}

function Tail-File([string]$Path, [int]$Lines=50) {
  if (Test-Path -LiteralPath $Path) {
    Write-Host "---- last $Lines lines of: $Path ----" -ForegroundColor DarkGray
    Get-Content -LiteralPath $Path -Tail $Lines | ForEach-Object { Write-Host $_ }
    Write-Host "-------------------------------------" -ForegroundColor DarkGray
  }
}

# ---------------- Paths ----------------
if ($MyInvocation.MyCommand.Path) {
  $ROOT = Split-Path -Path $MyInvocation.MyCommand.Path -Parent
} elseif ($PSCommandPath) {
  $ROOT = Split-Path -Path $PSCommandPath -Parent
} else {
  $ROOT = (Get-Location).Path
}
Set-Location -LiteralPath $ROOT

$BatchPy = Join-Path $ROOT 'batch_until_deadline.py'
$TuringPy = Join-Path $ROOT 'turing_check.py'
$SievePy  = Join-Path $ROOT 'sieve_from_zeros_psi_rigorous.py'
foreach ($p in @($BatchPy,$TuringPy,$SievePy)) {
  if (-not (Test-Path -LiteralPath $p)) { throw "Required Python script not found: $p" }
}

$Py = Get-PyExe

# Work dirs
$Stamp   = (Get-Date).ToString('yyyyMMdd_HHmmss')
$WORKDIR = Join-Path $ROOT "temp_$Stamp"
$LOGDIR  = Join-Path $WORKDIR 'logs'
$RUNROOT = Join-Path $WORKDIR 'runs'
$BATCH_OUT = Join-Path $RUNROOT 'batch'
$SIEVE_OUT = Join-Path $RUNROOT 'sieve'
Ensure-Dir $WORKDIR; Ensure-Dir $LOGDIR; Ensure-Dir $RUNROOT; Ensure-Dir $BATCH_OUT; Ensure-Dir $SIEVE_OUT

$BatchLog  = Join-Path $LOGDIR "batch_$Stamp.log"
$TuringLog = Join-Path $LOGDIR "turing_$Stamp.log"
$SieveLog  = Join-Path $LOGDIR "sieve_$Stamp.log"

# ---------------- Banner ----------------
Write-Host "DEBUG: WORKDIR=$WORKDIR"
Write-Host "DEBUG: LOGDIR=$LOGDIR"
Write-Host "DEBUG: RUNROOT=$RUNROOT"
Write-Host "============================================================"
Write-Host "Anti-Capitalist Software License (ACSL), Version 1.4"
Write-Host "Copyright (c) 2025 Lino Casu and Carmen Wrede"
Write-Host ""
Write-Host "You may use, modify, and distribute this software, but not"
Write-Host "for the purpose of generating profit, advertising, or in"
Write-Host "service of capitalist enterprise. You may not use it on"
Write-Host "behalf of organizations or individuals who fund, support, or"
Write-Host "perform exploitation, oppression, surveillance, policing,"
Write-Host "incarceration, or warfare. Distributions must keep this"
Write-Host "license and attribution intact and apply the same license to"
Write-Host "derivative works. (Full text in LICENSE)"
Write-Host "============================================================"

# ---------------- Inputs ----------------
$Hours = Ask-Number "Hours (>= 0.1) [default 0.1]:" "0.1" 0.1 $false
$MaxX  = Ask-Number "SIEVE_MAX (>= 10) [default 100]:" "100" 10 $true
$Dps   = Ask-Number "DPS (>= 1) [default 80]:" "80" 1 $true

# ---------------- 1) Batch ----------------
Write-Host ""
Write-Host "=== [$((TSUTC)) UTC] 1/3 Batch --tstart 10 --hours $Hours --dps $Dps ===" -ForegroundColor Cyan

$batchArgs = @(
  "-X","utf8",               # <<<<<<<<<<  UTF-8 erzwingen
  "-u", $BatchPy,
  "--tstart", "10",
  "--hours",  "$Hours",
  "--outroot", $BATCH_OUT,
  "--dps",   "$Dps"
)
$code = Invoke-Native -Exe $Py -Args $batchArgs -LogPath $BatchLog
if ($code -ne 0) {
  Write-Host "!! Batch failed (exit=$code). See: $BatchLog" -ForegroundColor Red
  Tail-File $BatchLog 80
  Write-Host ""; Write-Host "FINISHED. Workdir: $WORKDIR"; Write-Host "Logs:    $LOGDIR"
  exit $code
}

$MasterCsv = Join-Path $BATCH_OUT 'master_zeros.csv'
if (-not (Test-Path -LiteralPath $MasterCsv)) {
  Write-Host "!! master_zeros.csv not found at: $MasterCsv" -ForegroundColor Red
  Tail-File $BatchLog 80
  Write-Host ""; Write-Host "FINISHED. Workdir: $WORKDIR"; Write-Host "Logs:    $LOGDIR"
  exit 3
}

# ---------------- 2) Turing ----------------
Write-Host ""
Write-Host "=== [$((TSUTC)) UTC] 2/3 Turing (zeros-root) --T0 0.1 --T1 4.0 --bins 10 --steps 20000 --mp-dps $Dps ===" -ForegroundColor Cyan
$turingCsvOut = Join-Path $LOGDIR "turing_$Stamp.csv"
$turingArgs = @(
  "-X","utf8",               # <<<<<<<<<<  UTF-8 erzwingen
  "-u", $TuringPy,
  "--zeros-root", $BATCH_OUT,
  "--T0", "0.1",
  "--T1", "4.0",
  "--bins", "10",
  "--steps", "20000",
  "--mp-dps", "$Dps",
  "--csv", $turingCsvOut
)
[void](Invoke-Native -Exe $Py -Args $turingArgs -LogPath $TuringLog)

# ---------------- 3) Sieve ----------------
Write-Host ""
Write-Host "=== [$((TSUTC)) UTC] 3/3 Sieve [2, $MaxX]  kernel=fejer rigor=dusart ===" -ForegroundColor Cyan
$outPrimes      = Join-Path $SIEVE_OUT ("primes_2_{0}.txt" -f $MaxX)
$outBounds      = Join-Path $SIEVE_OUT ("bounds_2_{0}.csv" -f $MaxX)
$outWindows     = Join-Path $SIEVE_OUT ("windows_2_{0}.csv" -f $MaxX)
$outResidues    = Join-Path $SIEVE_OUT ("residues_2_{0}.csv" -f $MaxX)
$outResiduesWin = Join-Path $SIEVE_OUT ("residues_win_2_{0}.csv" -f $MaxX)
$outZeroQC      = Join-Path $SIEVE_OUT ("zeroqc_2_{0}.csv" -f $MaxX)
$outGaps        = Join-Path $SIEVE_OUT ("gaps_2_{0}.csv" -f $MaxX)
foreach ($f in @($outPrimes,$outBounds,$outWindows,$outResidues,$outResiduesWin,$outZeroQC,$outGaps)) {
  Ensure-Dir (Split-Path -Path $f -Parent)
}

$sieveArgs = @(
  "-X","utf8",               # <<<<<<<<<<  UTF-8 erzwingen
  "-u", $SievePy,
  "--zeros-root", $BATCH_OUT,
  "--x-start", "2",
  "--x-end",   "$MaxX",
  "--kernel", "fejer",
  "--rigorous", "dusart",
  "--rigorous-tail", "on",
  "--tail-C", "50",
  "--wheel", "210",
  "--out-primes",       $outPrimes,
  "--out-bounds",       $outBounds,
  "--out-windows",      $outWindows,
  "--out-residues",     $outResidues,
  "--out-residues-win", $outResiduesWin,
  "--out-zeroqc",       $outZeroQC,
  "--out-gaps",         $outGaps
)
$code = Invoke-Native -Exe $Py -Args $sieveArgs -LogPath $SieveLog
if ($code -ne 0) {
  Write-Host "!! Sieve failed (exit=$code). See: $SieveLog" -ForegroundColor Red
  Tail-File $SieveLog 100
  Write-Host ""; Write-Host "FINISHED. Workdir: $WORKDIR"; Write-Host "Logs:    $LOGDIR"
  exit $code
}

# ---------------- Done ----------------
Write-Host ""
Write-Host "FINISHED. Workdir: $WORKDIR"
Write-Host "Logs:    $LOGDIR"
exit 0
