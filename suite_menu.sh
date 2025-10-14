#!/usr/bin/env bash
set -euo pipefail
command -v python3 >/dev/null || { echo "python3 missing"; exit 127; }

# Optional debug: VERBOSE=1 rieman-zeta-zero
: "${VERBOSE:=0}"
if [[ "$VERBOSE" == "1" ]]; then set -x; fi

# Installpfad (per ENV übersteuerbar)
SCRIPTDIR="${RZS_SCRIPTDIR:-/usr/lib/rieman-zeta-suite}"
export PYTHONPATH="$SCRIPTDIR:${PYTHONPATH:-}"

# Arbeitskontext: temp_<UTC-Timestamp> direkt im aktuellen Verzeichnis
TS="$(date -u +%Y%m%d_%H%M%S)"
WORKDIR="$PWD/temp_${TS}"
LOGDIR="$WORKDIR/logs"
RUNROOT="$WORKDIR/runs"
BATCH_DIR="$RUNROOT/batch"
SIEVE_DIR="$RUNROOT/sieve"
mkdir -p "$LOGDIR" "$BATCH_DIR" "$SIEVE_DIR"

# Sauber abbrechen (alle Kinder beenden)
trap 'echo; echo "INT received, stopping…"; pkill -P "$$" || true; exit 130' INT

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

# Live-Runner mit sauberem Exit-Code (auch mit tee)
run_live() {
  local LOG="$1"; shift
  if command -v stdbuf >/dev/null 2>&1; then
    PYTHONUNBUFFERED=1 stdbuf -oL -eL "$@" 2>&1 | tee "$LOG"
  else
    PYTHONUNBUFFERED=1 "$@" 2>&1 | tee "$LOG"
  fi
  return "${PIPESTATUS[0]}"
}

# Python-Datei bevorzugen, sonst Modul als Fallback
# -> gibt ein **Array** zurück (über nameref)
make_cmd() { # <name der Ziel-Array-Var> <file.py> [module.fallback] [args...]
  local __out="$1"; shift
  local file="$1"; shift
  local mod="${1:-}"; [[ -n "$mod" ]] && shift || true
  local -a base
  if [[ -f "$SCRIPTDIR/$file" ]]; then
    base=(python3 -u "$SCRIPTDIR/$file")
  elif [[ -n "$mod" ]]; then
    base=(python3 -u -m "$mod")
  else
    echo "FATAL: $SCRIPTDIR/$file not found and no module fallback given." >&2
    exit 127
  fi
  local -n ref="$__out"
  ref=("${base[@]}" "$@")
}

# Schön formatierte Vorschau einer Array-Commandline
preview_cmd() {
  local -a arr=( "$@" )
  local out=()
  for tok in "${arr[@]}"; do
    printf -v q %q "$tok"
    out+=( "$q" )
  done
  printf "%s\n" "${out[*]}"
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

read -rp "SIEVE_MAX (>= 10) [default 100000]: " SIEVE_MAX_RAW
SIEVE_MAX_RAW="${SIEVE_MAX_RAW:-100000}"
CLEAN_SIEVE_MAX="$(echo "$SIEVE_MAX_RAW" | tr -d '[:space:]')"
python3 - "$CLEAN_SIEVE_MAX" <<'PY' || { echo "SIEVE_MAX must be integer and >= 10"; exit 3; }
import sys
try:
    v=int(sys.argv[1]); assert v>=10
except Exception: raise SystemExit(1)
PY
SIEVE_MAX="$CLEAN_SIEVE_MAX"

read -rp "DPS (>= 1) [default 80]: " DPS_RAW
DPS_RAW="${DPS_RAW:-80}"
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
make_cmd batch_cmd batch_until_deadline.py rieman_zeta_suite.batch_until_deadline   --tstart 10 --hours "$HOURS" --outroot "$BATCH_DIR" --dps "$DPS"
echo "DEBUG: Executing batch command: $(preview_cmd "${batch_cmd[@]}")"
run_live "$BATCH_LOG" "${batch_cmd[@]}"
dur=$(( $(date +%s) - start )); done_in "$dur"

ZEROS_CSV="$BATCH_DIR/master_zeros.csv"
ZEROS_DIR="$BATCH_DIR"
if [[ ! -s "$ZEROS_CSV" ]]; then
  echo "!! No zeros found at $ZEROS_CSV"; exit 5
fi

# ── 2) Turing-Check (CSV + zeros-root, Fallback zeros-root) ────────────────────
: "${TURING_BINS:=10}"
: "${TURING_STEPS:=20000}"
: "${TURING_T0:=0.1}"
: "${TURING_T1:=4.0}"
: "${TURING_MPDPS:=80}"   # <— fehlt bisher
TURING_LOG="$LOGDIR/turing_${TS}.log"

step "2/3 Turing (CSV) --T0 $TURING_T0 --T1 $TURING_T1 --bins $TURING_BINS --steps $TURING_STEPS --mp-dps $TURING_MPDPS"
start=$(date +%s)
set +e
make_cmd turing_cmd turing_check.py rieman_zeta_suite.turing_check   --csv "$ZEROS_CSV" --zeros-root "$ZEROS_DIR"   --T0 "$TURING_T0" --T1 "$TURING_T1"   --bins "$TURING_BINS" --steps "$TURING_STEPS" --mp-dps "$TURING_MPDPS"
echo "DEBUG: Executing Turing CSV command: $(preview_cmd "${turing_cmd[@]}")"
run_live "$TURING_LOG" "${turing_cmd[@]}"
RC=$?
set -e
dur=$(( $(date +%s) - start )); done_in "$dur"

if (( RC != 0 )); then
  step "2/3 Turing (Fallback zeros-root) --T0 $TURING_T0 --T1 $TURING_T1"
  start=$(date +%s)
  make_cmd turing_fb_cmd turing_check.py rieman_zeta_suite.turing_check     --zeros-root "$ZEROS_DIR"     --T0 "$TURING_T0" --T1 "$TURING_T1"     --bins "$TURING_BINS" --steps "$TURING_STEPS" --mp-dps "$TURING_MPDPS"
  echo "DEBUG: Executing Turing Fallback command: $(preview_cmd "${turing_fb_cmd[@]}")"
  run_live "$TURING_LOG" "${turing_fb_cmd[@]}"
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
# optionale Flags nur setzen, wenn belegt
opt_flags=()
[[ -n "$SIEVE_H"      ]] && opt_flags+=( --H "$SIEVE_H" )
[[ -n "$SIEVE_TCUT"   ]] && opt_flags+=( --Tcut "$SIEVE_TCUT" )
[[ -n "$SIEVE_QMAX"   ]] && opt_flags+=( --qmax "$SIEVE_QMAX" )
[[ -n "$SIEVE_QWIN"   ]] && opt_flags+=( --qwin "$SIEVE_QWIN" )
[[ -n "$SIEVE_MAXWIN" ]] && opt_flags+=( --max-windows "$SIEVE_MAXWIN" )

make_cmd sieve_cmd sieve_from_zeros_psi_rigorous.py rieman_zeta_suite.sieve_from_zeros_psi_rigorous   --zeros-root "$ZEROS_DIR"   --x-start 2 --x-end "$SIEVE_MAX"   --kernel "$SIEVE_KERNEL"   --rigorous "$SIEVE_RIGOR"   --rigorous-tail "$SIEVE_RIGTAIL"   --tail-C "$SIEVE_TAILC"   --wheel "$SIEVE_WHEEL"   "${opt_flags[@]}"   --out-primes "$SIEVE_DIR/primes_2_${SIEVE_MAX}.txt"   --out-bounds "$SIEVE_DIR/bounds_2_${SIEVE_MAX}.csv"   --out-windows "$SIEVE_DIR/windows_2_${SIEVE_MAX}.csv"   --out-residues "$SIEVE_DIR/residues_2_${SIEVE_MAX}.csv"   --out-residues-win "$SIEVE_DIR/residues_win_2_${SIEVE_MAX}.csv"   --out-zeroqc "$SIEVE_DIR/zeroqc_2_${SIEVE_MAX}.csv"   --out-gaps "$SIEVE_DIR/gaps_2_${SIEVE_MAX}.csv"

echo "DEBUG: Executing Sieve command: $(preview_cmd "${sieve_cmd[@]}")"
run_live "$SIEVE_LOG" "${sieve_cmd[@]}"
dur=$(( $(date +%s) - start )); done_in "$dur"

echo ""
echo "FINISHED. Workdir: $WORKDIR"
echo "Logs: $LOGDIR"
