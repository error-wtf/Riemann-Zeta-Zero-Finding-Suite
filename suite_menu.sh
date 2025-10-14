#!/usr/bin/env bash
set -euo pipefail

# Optional debug: VERBOSE=1 rieman-zeta-zero
: "${VERBOSE:=0}"
if [[ "$VERBOSE" == "1" ]]; then set -x; fi

# Script location (install path); override via RZS_SCRIPTDIR if nötig
SCRIPTDIR="${RZS_SCRIPTDIR:-/usr/lib/rieman-zeta-suite}"

# Arbeitskontext: immer relativ zum aktuellen Verzeichnis
TS="$(date -u +%Y%m%d_%H%M%S)"
WORKDIR="$PWD/temp_${TS}"
LOGDIR="$WORKDIR/logs"
RUNROOT="$WORKDIR/runs"
BATCH_DIR="$RUNROOT/batch"
SIEVE_DIR="$RUNROOT/sieve"
mkdir -p "$LOGDIR" "$BATCH_DIR" "$SIEVE_DIR"

echo "DEBUG: WORKDIR=$WORKDIR"
echo "DEBUG: LOGDIR=$LOGDIR"
echo "DEBUG: RUNROOT=$RUNROOT"

header() {
cat <<'ACSL'
============================================================
Anti-Capitalist Software License (ACSL), Version 1.4
Copyright (c) 2025 Lino Casu and Carmen Wrede

You may use, modify, and distribute this software, but not
for the purpose of generating profit, advertising, or in
service of capitalist enterprise. You may not use it on
behalf of organizations or individuals who fund, support, or
perform exploitation, oppression, surveillance, policing,
incarceration, or warfare. Distributions must keep this
license and attribution intact and apply the same license to
derivative works. (Full text in LICENSE)
============================================================
ACSL
}
step()    { printf "\n=== [%s UTC] %s ===\n" "$(date -u +%H:%M:%S)" "$*"; }
done_in() { local s=$1; printf "✓ done in %02d:%02d:%02d\n" $((s/3600)) $(((s%3600)/60)) $((s%60)); }
run_live(){ local LOG="$1"; shift; PYTHONUNBUFFERED=1 stdbuf -oL -eL "$@" 2>&1 | tee "$LOG"; return "${PIPESTATUS[0]}"; }

# Python-Datei bevorzugen, ansonsten Modulpfad (falls du mal als -m laufen willst)
cmd_py(){ # $1=file.py  $2=module.fallback
  local file="$1" mod="${2:-}"
  if [[ -f "$SCRIPTDIR/$file" ]]; then printf "python3 -u %q/%s" "$SCRIPTDIR" "$file"
elif [[ -n "$mod" ]]; then printf "python3 -u -m %s" "$mod"
else printf "python3 -u %q/%s" "$SCRIPTDIR" "$file"; fi
}

# ── Banner ──────────────────────────────────────────────────────────────────────
header

# ── Eingaben ───────────────────────────────────────────────────────────────────
read -rp "Hours (>= 0.1) [default 0.1]: " HOURS_RAW
HOURS_RAW="${HOURS_RAW:-0.1}"
CLEAN_HOURS="$(echo "$HOURS_RAW" | tr ',' '.' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
echo "DEBUG: CLEAN_HOURS=$CLEAN_HOURS"
python3 - "$CLEAN_HOURS" <<'PY' || { echo "Hours must be numeric and >= 0.1"; exit 2; }
import sys
try:
    h=float(sys.argv[1]); assert h>=0.1
except Exception: raise SystemExit(1)
PY
HOURS="$CLEAN_HOURS"

read -rp "SIEVE_MAX (>= 10) [default 100]: " SIEVE_MAX_RAW
SIEVE_MAX_RAW="${SIEVE_MAX_RAW:-100}"
CLEAN_SIEVE_MAX="$(echo "$SIEVE_MAX_RAW" | tr -d '[:space:]')"
python3 - "$CLEAN_SIEVE_MAX" <<'PY' || { echo "SIEVE_MAX must be integer and >= 10"; exit 3; }
import sys
try:
    v=int(sys.argv[1]); assert v>=10
except Exception: raise SystemExit(1)
PY
SIEVE_MAX="$CLEAN_SIEVE_MAX"

read -rp "DPS (>= 1) [default 1]: " DPS_RAW
DPS_RAW="${DPS_RAW:-1}"
CLEAN_DPS="$(echo "$DPS_RAW" | tr -d '[:space:]')"
python3 - "$CLEAN_DPS" <<'PY' || { echo "DPS must be integer and >= 1"; exit 4; }
import sys
try:
    v=int(sys.argv[1]); assert v>=1
except Exception: raise SystemExit(1)
PY
DPS="$CLEAN_DPS"

# ── 1) Batch bis Deadline ──────────────────────────────────────────────────────
BATCH_LOG="$LOGDIR/batch_${TS}.log"
step "1/3 Batch run --tstart 10 --hours $HOURS --dps $DPS"
start=$(date +%s)
PYTHON_CMD=$(printf "%s --tstart 10 --hours %s --outroot %q --dps %s"   "$(cmd_py batch_until_deadline.py rieman_zeta_suite.batch_until_deadline)"   "$HOURS" "$BATCH_DIR" "$DPS")
echo "DEBUG: Executing batch command: $PYTHON_CMD"
run_live "$BATCH_LOG" $PYTHON_CMD
dur=$(( $(date +%s) - start )); done_in "$dur"

ZEROS_CSV="$BATCH_DIR/master_zeros.csv"
ZEROS_DIR="$BATCH_DIR"
if [[ ! -s "$ZEROS_CSV" ]]; then
  echo "!! No zeros found at $ZEROS_CSV"; exit 5
fi

# ── 2) Turing-Check (CSV + zeros-root; Fallback zeros-root) ────────────────────
TURING_T0="${TURING_T0:-1}"
TURING_T1="${TURING_T1:-2}"
TURING_LOG="$LOGDIR/turing_${TS}.log"

step "2/3 Turing (CSV) --T0 $TURING_T0 --T1 $TURING_T1"
start=$(date +%s)
set +e
PYTHON_CMD=$(printf "%s --csv %q --zeros-root %q --T0 %s --T1 %s"   "$(cmd_py turing_check.py rieman_zeta_suite.turing_check)"   "$ZEROS_CSV" "$ZEROS_DIR" "$TURING_T0" "$TURING_T1")
echo "DEBUG: Executing Turing CSV command: $PYTHON_CMD"
run_live "$TURING_LOG" $PYTHON_CMD
RC=$?
set -e
dur=$(( $(date +%s) - start )); done_in "$dur"

if (( RC != 0 )); then
  TURING_BINS="${TURING_BINS:-80}"
  TURING_STEPS="${TURING_STEPS:-20000}"
  TURING_MPDPS="${TURING_MPDPS:-80}"
  step "2/3 Turing (Fallback zeros-root) --T0 $TURING_T0 --T1 $TURING_T1"
  start=$(date +%s)
  PYTHON_CMD=$(printf "%s --zeros-root %q --T0 %s --T1 %s --bins %s --steps %s --mp-dps %s"     "$(cmd_py turing_check.py rieman_zeta_suite.turing_check)"     "$ZEROS_DIR" "$TURING_T0" "$TURING_T1" "$TURING_BINS" "$TURING_STEPS" "$TURING_MPDPS")
  echo "DEBUG: Executing Turing Fallback command: $PYTHON_CMD"
  run_live "$TURING_LOG" $PYTHON_CMD
  dur=$(( $(date +%s) - start )); done_in "$dur"
fi

# ── 3) Rigorous Sieve [2, SIEVE_MAX] ───────────────────────────────────────────
SIEVE_LOG="$LOGDIR/sieve_${TS}.log"
SIEVE_KERNEL="${SIEVE_KERNEL:-fejer}"    # {none,fejer,parzen}
SIEVE_RIGOR="${SIEVE_RIGOR:-dusart}"     # {none,dusart,bertrand}
SIEVE_RIGTAIL="${SIEVE_RIGTAIL:-on}"     # {off,on}
SIEVE_TAILC="${SIEVE_TAILC:-50}"
SIEVE_WHEEL="${SIEVE_WHEEL:-210}"        # {1,6,30,210,2310,30030}
SIEVE_H="${SIEVE_H:-}"                   # optional
SIEVE_TCUT="${SIEVE_TCUT:-}"             # optional
SIEVE_QMAX="${SIEVE_QMAX:-}"             # optional
SIEVE_QWIN="${SIEVE_QWIN:-}"             # optional
SIEVE_MAXWIN="${SIEVE_MAXWIN:-}"         # optional

step "3/3 Sieve [2, $SIEVE_MAX]  kernel=$SIEVE_KERNEL rigor=$SIEVE_RIGOR"
start=$(date +%s)
PYTHON_CMD=$(printf "%s --zeros-root %q --x-start 2 --x-end %s --kernel %s --rigorous %s --rigorous-tail %s --tail-C %s --wheel %s %s %s %s %s %s --out-primes %q --out-bounds %q --out-windows %q --out-residues %q --out-residues-win %q --out-zeroqc %q --out-gaps %q"   "$(cmd_py sieve_from_zeros_psi_rigorous.py rieman_zeta_suite.sieve_from_zeros_psi_rigorous)"   "$ZEROS_DIR" "$SIEVE_MAX" "$SIEVE_KERNEL" "$SIEVE_RIGOR" "$SIEVE_RIGTAIL" "$SIEVE_TAILC" "$SIEVE_WHEEL"   "${SIEVE_H:+"--H $SIEVE_H"}" "${SIEVE_TCUT:+"--Tcut $SIEVE_TCUT"}" "${SIEVE_QMAX:+"--qmax $SIEVE_QMAX"}"   "${SIEVE_QWIN:+"--qwin $SIEVE_QWIN"}" "${SIEVE_MAXWIN:+"--max-windows $SIEVE_MAXWIN"}"   "$SIEVE_DIR/primes_2_${SIEVE_MAX}.txt"   "$SIEVE_DIR/bounds_2_${SIEVE_MAX}.csv"   "$SIEVE_DIR/windows_2_${SIEVE_MAX}.csv"   "$SIEVE_DIR/residues_2_${SIEVE_MAX}.csv"   "$SIEVE_DIR/residues_win_2_${SIEVE_MAX}.csv"   "$SIEVE_DIR/zeroqc_2_${SIEVE_MAX}.csv"   "$SIEVE_DIR/gaps_2_${SIEVE_MAX}.csv")
echo "DEBUG: Executing Sieve command: $PYTHON_CMD"
run_live "$SIEVE_LOG" $PYTHON_CMD
dur=$(( $(date +%s) - start )); done_in "$dur"

echo ""
echo "FINISHED. Workdir: $WORKDIR"
echo "Logs: $LOGDIR"