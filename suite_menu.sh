#!/usr/bin/env bash
set -euo pipefail

# Optionales Debug: VERBOSE=1 ./suite_menu.sh
: "${VERBOSE:=0}"
if [[ "$VERBOSE" == "1" ]]; then set -x; fi

# Use SCRIPTDIR from wrapper, fallback to current directory if not set (e.g., direct execution)
SCRIPTDIR="${RZS_SCRIPTDIR:-$(dirname "$(readlink -f "$0")")}"

BASE="$(pwd -P)"                  # spätere .deb: alles relativ zum Ausführungsort
TS="$(date -u +%Y%m%d_%H%M%S)"    # kompakter UTC-Stamp (nicht „laut“)
WORKDIR="$BASE/temp_${TS}"
LOGDIR="$WORKDIR/logs"
RUNROOT="$WORKDIR/runs"
{ set +x; } 2>/dev/null || true
mkdir -p "$LOGDIR" "$RUNROOT"
echo "DEBUG: WORKDIR=$WORKDIR"
echo "DEBUG: LOGDIR=$LOGDIR"
echo "DEBUG: RUNROOT=$RUNROOT"
if [[ "$VERBOSE" == "1" ]]; then set -x; fi

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
incarceraion, or warfare. Distributions must keep this
license and attribution intact and apply the same license to
derivative works. (Full text in LICENSE)
============================================================
ACSL
}
step() { printf "\n=== [%s UTC] %s ===\n" "$(date -u +%H:%M:%S)" "$*"; }
done_in() { local s=$1; printf "✓ done in %02d:%02d:%02d\n" $((s/3600)) $(((s%3600)/60)) $((s%60)); }
run_live() {
  # run_live "LOGFILE" cmd...
  local LOG="$1"; shift
  # Unbuffered Ausgabe (so siehst du live Output)
  PYTHONUNBUFFERED=1 stdbuf -oL -eL "$@" 2>&1 | tee "$LOG"
  return "${PIPESTATUS[0]}"
}
cmd_py() {
  # $1=datei.py , $2=modulpfad
  local file="$1" mod="$2"
  if [[ -f "$SCRIPTDIR/$file" ]]; then printf "python3 -u %q/%s" "$SCRIPTDIR" "$file"
  else printf "python3 -u -m %s" "$mod"; fi
}

header

# ── Eingaben ────────────────────────────────────────────────────────────────
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
    d=int(sys.argv[1]); assert d>=1
except Exception: raise SystemExit(1)
PY
DPS="$CLEAN_DPS"

# PYTHONPATH so setzen, dass lokale Module gefunden werden
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$SCRIPTDIR"

# ── 1) Batch bis Deadline (zeigt live Output) ───────────────────────────────
BATCH_TSTART="${BATCH_TSTART:-10}"
# BATCH_DPS="${BATCH_DPS:-80}" # This line is removed
BATCH_OUTROOT="$RUNROOT/batch"
BATCH_LOG="$LOGDIR/batch_${TS}.log"

step "1/3 Batch run --tstart $BATCH_TSTART --hours $HOURS --dps $DPS"
start=$(date +%s)
PYTHON_CMD=$(printf "%s --tstart %s --hours %s --outroot %q --dps %s"     "$(cmd_py batch_until_deadline.py zeta_prime_suite.batch_until_deadline)"     "$BATCH_TSTART" "$HOURS" "$BATCH_OUTROOT" "$DPS")
echo "DEBUG: Executing batch command: $PYTHON_CMD"
run_live "$BATCH_LOG" $PYTHON_CMD
rc=$?; dur=$(( $(date +%s) - start ))
done_in "$dur"
if (( rc != 0 )); then echo "(!) Batch exit code: $rc (weiter mit Turing/Sieve, Logs siehe $BATCH_LOG)"; fi

# ── master_zeros.csv suchen (ohne Merge) ────────────────────────────────────
find_master_csv() {
  local cand=""
  for name in master_zeros.csv master_zero.csv certified_zeros.csv zeros.csv; do
    if [[ -s "$SCRIPTDIR/$name" ]]; then echo "$SCRIPTDIR/$name"; return 0; fi
  done
  cand="$(find "$RUNROOT" -type f \( -name 'master_*.csv' -o -name 'zeros.csv' \) -not -path '*/merged/*' -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -n1 | awk '{print $2}')"
  [[ -n "$cand" && -s "$cand" ]] && { echo "$cand"; return 0; }
  return 1
}
ZEROS_CSV="$(find_master_csv || true)"
if [[ -z "${ZEROS_CSV:-}" ]]; then
  echo "!! Keine master_zeros.csv gefunden. Bitte in $SCRIPTDIR bereitstellen."
  echo "Abbruch."
  exit 6
fi
ZEROS_DIR="$(dirname "$ZEROS_CSV")"

# ── 2) Turing-Check (CSV-Modus; Fallback zeros-root). Live-Output ───────────
TURING_T0="${TURING_T0:-1}"
TURING_T1="${TURING_T1:-2}"
TURING_LOG="$LOGDIR/turing_${TS}.log"

step "2/3 Turing (CSV) --T0 $TURING_T0 --T1 $TURING_T1"
start=$(date +%s)
set +e
PYTHON_CMD=$(printf "%s --csv %q --zeros-root %q --T0 %s --T1 %s"     "$(cmd_py turing_check.py zeta_prime_suite.turing_check)"     "$ZEROS_CSV" "$ZEROS_DIR" "$TURING_T0" "$TURING_T1")
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
  PYTHON_CMD=$(printf "%s --zeros-root %q --T0 %s --T1 %s --bins %s --steps %s --mp-dps %s"       "$(cmd_py turing_check.py zeta_prime_suite.turing_check)"       "$ZEROS_DIR" "$TURING_T0" "$TURING_T1" "$TURING_BINS" "$TURING_STEPS" "$TURING_MPDPS")
echo "DEBUG: Executing Turing Fallback command: $PYTHON_CMD"
  run_live "$TURING_LOG" $PYTHON_CMD
  dur=$(( $(date +%s) - start )); done_in "$dur"
fi

# ── 3) Rigorous Sieve (ein Schuss: [2, SIEVE_MAX]). Live-Output ─────────────
SIEVE_DIR="$RUNROOT/sieve"
SIEVE_LOG="$LOGDIR/sieve_${TS}.log"
{ set +x; } 2>/dev/null || true
mkdir -p "$SIEVE_DIR"
if [[ "$VERBOSE" == "1" ]]; then set -x; fi

SIEVE_KERNEL="${SIEVE_KERNEL:-fejer}"      # {none,fejer,parzen}
SIEVE_RIGOR="${SIEVE_RIGOR:-dusart}"       # {none,dusart,bertrand}
SIEVE_RIGTAIL="${SIEVE_RIGTAIL:-on}"       # {off,on}
SIEVE_TAILC="${SIEVE_TAILC:-50}"
SIEVE_WHEEL="${SIEVE_WHEEL:-210}"          # {1,6,30,210,2310,30030}
SIEVE_H="${SIEVE_H:-}"                     # optional
SIEVE_TCUT="${SIEVE_TCUT:-}"               # optional
SIEVE_QMAX="${SIEVE_QMAX:-}"               # optional
SIEVE_QWIN="${SIEVE_QWIN:-}"               # optional
SIEVE_MAXWIN="${SIEVE_MAXWIN:-}"           # optional

step "3/3 Sieve [2, $SIEVE_MAX]  kernel=$SIEVE_KERNEL rigor=$SIEVE_RIGOR"
start=$(date +%s)
PYTHON_CMD=$(printf "%s --zeros-root %q --x-start 2 --x-end %s --kernel %s --rigorous %s --rigorous-tail %s --tail-C %s --wheel %s %s %s %s %s %s           --out-primes %q --out-bounds %q --out-windows %q --out-residues %q --out-residues-win %q --out-zeroqc %q --out-gaps %q"     "$(cmd_py sieve_from_zeros_psi_rigorous.py zeta_prime_suite.sieve_from_zeros_psi_rigorous)"     "$ZEROS_DIR" "$SIEVE_MAX" "$SIEVE_KERNEL" "$SIEVE_RIGOR" "$SIEVE_RIGTAIL" "$SIEVE_TAILC" "$SIEVE_WHEEL"     "${SIEVE_H:+"--H $SIEVE_H"}" "${SIEVE_TCUT:+"--Tcut $SIEVE_TCUT"}" "${SIEVE_QMAX:+"--qmax $SIEVE_QMAX"}"     "${SIEVE_QWIN:+"--qwin $SIEVE_QWIN"}" "${SIEVE_MAXWIN:+"--max-windows $SIEVE_MAXWIN"}"     "$SIEVE_DIR/primes_2_${SIEVE_MAX}.txt"     "$SIEVE_DIR/bounds_2_${SIEVE_MAX}.csv"     "$SIEVE_DIR/windows_2_${SIEVE_MAX}.csv"     "$SIEVE_DIR/residues_2_${SIEVE_MAX}.csv"     "$SIEVE_DIR/residues_win_2_${SIEVE_MAX}.csv"     "$SIEVE_DIR/zeroqc_2_${SIEVE_MAX}.csv"     "$SIEVE_DIR/gaps_2_${SIEVE_MAX}.csv")
echo "DEBUG: Executing Sieve command: $PYTHON_CMD"
run_live "$SIEVE_LOG" $PYTHON_CMD
rc=$?; dur=$(( $(date +%s) - start ))
done_in "$dur"

# Optional: Primzahlen konsolidieren (falls später gefenstert)
if command -v awk >/dev/null 2>&1;
then
  cat "$SIEVE_DIR"/primes_*.txt 2>/dev/null | awk 'NF>0' | sort -n | uniq > "$SIEVE_DIR/primes_up_to_${SIEVE_MAX}.txt" || true
fi

printf "\nFINISHED. Workdir: %s\nLogs: %s\n" "$WORKDIR" "$LOGDIR"