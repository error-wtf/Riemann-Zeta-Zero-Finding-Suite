# Requires: Windows PowerShell 5+ or PowerShell 7+, Python 3.x on PATH
# Runs from the folder where this script and the Python files live.

$ErrorActionPreference = "Stop"

function Get-Python {
    if (Get-Command py -ErrorAction SilentlyContinue)       { return @("py", "-3") }
    elseif (Get-Command python3 -ErrorAction SilentlyContinue) { return @("python3") }
    elseif (Get-Command python -ErrorAction SilentlyContinue)  { return @("python") }
    else { throw "Python 3.x not found on PATH. Install Python 3 and try again." }
}

function Read-Number($Prompt, $Default, $Min, $IsInteger=$false) {
    while ($true) {
        $raw = Read-Host $Prompt
        if ([string]::IsNullOrWhiteSpace($raw)) { $raw = $Default }
        $raw = $raw.Trim().Replace(',', '.')  # de/locale → dot

        if ($IsInteger) {
            [int]$n = 0
            if ([int]::TryParse($raw, [ref]$n) -and $n -ge $Min) { return $n }
        } else {
            [double]$x = 0
            if ([double]::TryParse($raw, [ref]$x) -and $x -ge $Min) { return $x }
        }
        Write-Host "Invalid input. Must be >= $Min." -ForegroundColor Yellow
    }
}

# --- Layout detection (program directory) ---
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# --- Work dirs (temp_YYYYMMDD_HHMMSS) ---
$TS = (Get-Date).ToUniversalTime().ToString("yyyyMMdd_HHmmss")
$WorkDir = Join-Path $ScriptDir "temp_$TS"
$LogDir  = Join-Path $WorkDir "logs"
$RunRoot = Join-Path $WorkDir "runs"
New-Item -Force -ItemType Directory -Path $WorkDir, $LogDir, (Join-Path $RunRoot "batch"), (Join-Path $RunRoot "sieve") | Out-Null

# --- Header ---
Write-Host "DEBUG: WORKDIR=$WorkDir"
Write-Host "DEBUG: LOGDIR=$LogDir"
Write-Host "DEBUG: RUNROOT=$RunRoot"
"============================================================"
"Anti-Capitalist Software License (ACSL), Version 1.4"
"Copyright (c) 2025 Lino Casu and Carmen Wrede"
""
"You may use, modify, and distribute this software, but not"
"for the purpose of generating profit, advertising, or in"
"service of capitalist enterprise. You may not use it on"
"behalf of organizations or individuals who fund, support, or"
"perform exploitation, oppression, surveillance, policing,"
"incarceration, or warfare. Distributions must keep this"
"license and attribution intact and apply the same license to"
"derivative works. (Full text in LICENSE)"
"============================================================"

# --- Inputs (only these three) ---
$Hours    = Read-Number "Hours (>= 0.1) [default 0.1]"  "0.1"  0.1  $false
$SieveMax = Read-Number "SIEVE_MAX (>= 10) [default 100]" "100" 10   $true
$Dps      = Read-Number "DPS (>= 1) [default 80]"         "80"  1    $true

# --- Resolve Python ---
$pySpec = Get-Python
$pyExe  = $pySpec[0]
$pyArgs = @()
if ($pySpec.Count -gt 1) { $pyArgs += $pySpec[1] }

# --- Files ---
$BatchPy  = Join-Path $ScriptDir "batch_until_deadline.py"
$TuringPy = Join-Path $ScriptDir "turing_check.py"
$SievePy  = Join-Path $ScriptDir "sieve_from_zeros_psi_rigorous.py"

if (!(Test-Path $BatchPy) -or !(Test-Path $TuringPy) -or !(Test-Path $SievePy)) {
    throw "Missing required Python files in $ScriptDir (batch_until_deadline.py, turing_check.py, sieve_from_zeros_psi_rigorous.py)"
}

# --- Logs ---
$batchLog  = Join-Path $LogDir "batch_$TS.log"
$turingLog = Join-Path $LogDir "turing_$TS.log"
$sieveLog  = Join-Path $LogDir "sieve_$TS.log"

# --- Step 1: Batch until deadline ---
$utcNow = (Get-Date).ToUniversalTime().ToString("HH:mm:ss 'UTC'")
Write-Host ""
Write-Host "=== [$utcNow] 1/3 Batch run --tstart 10 --hours $Hours --dps $Dps ===" -ForegroundColor Cyan

$batchArgs = $pyArgs + @(
    "-u", $BatchPy,
    "--tstart", "10",
    "--hours",  "$Hours",
    "--outroot", (Join-Path $RunRoot "batch"),
    "--dps",    "$Dps"
)

try {
    & $pyExe @batchArgs 2>&1 | Tee-Object -FilePath $batchLog -Append
    $code = $LASTEXITCODE
    if ($code -ne 0) { throw "Batch exited with code $code" }
} catch {
    Write-Host "!! Batch failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "See: $batchLog"
    exit 2
}

# master_zeros.csv expected here
$BatchOut   = Join-Path $RunRoot "batch"
$MasterCsv  = Join-Path $BatchOut "master_zeros.csv"
if (!(Test-Path $MasterCsv)) {
    Write-Host "!! master_zeros.csv not found: $MasterCsv" -ForegroundColor Red
    Write-Host "Check batch logs: $batchLog"
    exit 3
}

# --- Step 2: Turing check (try CSV+zeros-root, fallback zeros-root only) ---
$utcNow = (Get-Date).ToUniversalTime().ToString("HH:mm:ss 'UTC'")
Write-Host ""
Write-Host "=== [$utcNow] 2/3 Turing check (CSV preferred; fallback zeros-root) ===" -ForegroundColor Cyan

# Conservative small window (works with very few zeros)
$T0 = 0.1
$T1 = 4.0
$Bins = 10
$Steps = 20000
$MpDps = $Dps

function Run-Turing($useCsv) {
    $args = $pyArgs + @("-u", $TuringPy, "--T0", "$T0", "--T1", ("{0:F6}" -f $T1), "--bins", "$Bins", "--steps", "$Steps", "--mp-dps", "$MpDps")
    if ($useCsv) { $args += @("--csv", $MasterCsv) }
    $args += @("--zeros-root", $BatchOut)

    & $pyExe @args 2>&1 | Tee-Object -FilePath $turingLog -Append
    return $LASTEXITCODE
}

$code = Run-Turing $true
if ($code -ne 0) {
    Write-Host "!! Turing (CSV) failed; trying zeros-root fallback ..." -ForegroundColor Yellow
    $code2 = Run-Turing $false
    if ($code2 -ne 0) {
        Write-Host "!! Turing failed (fallback): exit $code2" -ForegroundColor Red
        Write-Host "See: $turingLog"
        exit 4
    }
}

# --- Step 3: Rigorous sieve ---
$utcNow = (Get-Date).ToUniversalTime().ToString("HH:mm:ss 'UTC'")
Write-Host ""
Write-Host "=== [$utcNow] 3/3 Sieve [2, $SieveMax]  kernel=fejer rigor=dusart ===" -ForegroundColor Cyan

$sieveOutDir = Join-Path $RunRoot "sieve"
$null = New-Item -Force -ItemType Directory -Path $sieveOutDir

$sieveArgs = $pyArgs + @(
    "-u", $SievePy,
    "--zeros-root", $BatchOut,
    "--x-start", "2",
    "--x-end",   "$SieveMax",
    "--kernel",  "fejer",
    "--rigorous","dusart",
    "--rigorous-tail", "on",
    "--tail-C",  "50",
    "--wheel",   "210",
    "--out-primes",        (Join-Path $sieveOutDir ("primes_2_{0}.txt" -f $SieveMax)),
    "--out-bounds",        (Join-Path $sieveOutDir ("bounds_2_{0}.csv" -f $SieveMax)),
    "--out-windows",       (Join-Path $sieveOutDir ("windows_2_{0}.csv" -f $SieveMax)),
    "--out-residues",      (Join-Path $sieveOutDir ("residues_2_{0}.csv" -f $SieveMax)),
    "--out-residues-win",  (Join-Path $sieveOutDir ("residues_win_2_{0}.csv" -f $SieveMax)),
    "--out-zeroqc",        (Join-Path $sieveOutDir ("zeroqc_2_{0}.csv" -f $SieveMax)),
    "--out-gaps",          (Join-Path $sieveOutDir ("gaps_2_{0}.csv" -f $SieveMax))
)

try {
    & $pyExe @sieveArgs 2>&1 | Tee-Object -FilePath $sieveLog -Append
    $code = $LASTEXITCODE
    if ($code -ne 0) { throw "Sieve exited with code $code" }
} catch {
    Write-Host "!! Sieve failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "See: $sieveLog"
    exit 5
}

Write-Host ""
Write-Host "FINISHED. Workdir: $WorkDir"
Write-Host "Logs: $LogDir"
exit 0
