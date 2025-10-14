#!/usr/bin/env bash
# suite_menu.sh — Riemann Zeta Suite launcher (batch → turing → sieve)
# Verbose, math-preserving, no timeouts, auto Turing parameters from CSV.
# License banner shown at start (ACSL 1.4).

set -euo pipefail

# -------------------- config / paths --------------------
SCRIPTDIR="${RZS_SCRIPTDIR:-/usr/lib/rieman-zeta-suite}"
PROGDIR="$SCRIPTDIR"
PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$PROGDIR"; export PYTHONPATH

# current working dir bleibt CWD des Users
TS="$(date -u +%Y%m%d_%H%M%S)"
WORKDIR="$PWD/temp_$TS"
LOGDIR="$WORKDIR/logs"
RUNROOT="$WORKDIR/runs"
mkdir -p "$LOGDIR" "$RUNROOT" "$RUNROOT/batch" "$RUNROOT/sieve"

echo "DEBUG: WORKDIR=$WORKDIR"
echo "DEBUG: LOGDIR=$LOGDIR"
echo "DEBUG: RUNROOT=$RUNROOT"

# -------------------- helpers --------------------
_utc(){ date -u +%H:%M:%S; }

cmd_py(){ # $1=file.py , $2=module.fallback
  local file="$1" mod="${2:-}"
  if [[ -f "$PROGDIR/$file" ]]; then
    printf "python3 -u %q/%s" "$PROGDIR" "$file"
  elif [[ -n "$mod" ]]; then
    printf "python3 -u -m %s" "$mod"
  else
    printf "python3 -u %q/%s" "$PROGDIR" "$file"
  fi
}

prompt_float(){
  local prompt="$1" def="$2" min="$3"
  local v; read -rp "$prompt (>= $min) [default $def]: " v || true
  v="${v//,/.}"; v="${v//[$'\r\t ']/}"
  [[ -z "${v:-}" ]] && v="$def"
  python3 - "$v" "$min" <<'PY' || { echo "Invalid number."; exit 2; }
import sys
v = sys.argv[1]
minv = float(sys.argv[2])
try:
    x = float(v)
    assert x >= minv
    print(x)
except Exception:
    sys.exit(1)
PY
}

prompt_int(){
  local prompt="$1" def="$2" min="$3"
  local v; read -rp "$prompt (>= $min) [default $def]: " v || true
  v="${v//[$'\r\t ']/}"
  [[ -z "${v:-}" ]] && v="$def"
  python3 - "$v" "$min" <<'PY' || { echo "Invalid integer."; exit 2; }
import sys
v = sys.argv[1]
minv = int(sys.argv[2])
try:
    x = int(v)
    assert x >= minv
    print(x)
except Exception:
    sys.exit(1)
PY
}

# -------------------- banner --------------------
cat <<'TXT'
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
TXT

# -------------------- inputs --------------------
HOURS="$(prompt_float 'Hours' '0.1' '0.1')"
echo "DEBUG: CLEAN_HOURS=$HOURS"
SIEVE_MAX="$(prompt_int 'SIEVE_MAX' '100' '10')"
DPS="$(prompt_int 'DPS' '80' '1')"

# -------------------- 1/3 batch --------------------
echo
echo "=== [$(_utc) UTC] 1/3 Batch run --tstart 10 --hours $HOURS --dps $DPS ==="
BATCH_CMD="$(cmd_py batch_until_deadline.py zeta_prime_suite.batch_until_deadline) --tstart 10 --hours "$HOURS" --outroot "$RUNROOT/batch" --dps "$DPS""
echo "DEBUG: Executing batch command: $BATCH_CMD"
$BATCH_CMD | tee "$LOGDIR/batch_${TS}.log"

CSV="$RUNROOT/batch/master_zeros.csv"
if [[ ! -s "$CSV" ]]; then
  echo "!! No master_zeros.csv produced. Exiting."
  exit 3
fi

# -------------------- 2/3 turing (auto T1/BINS aus CSV) --------------------
T0="0.1"
T1="$(awk -F, 'NR>1 {if ($1+0>m) m=$1+0} END {if (m>0) printf(\"%.6f\", m); else print \"2.000000\"}' "$CSV")"
BINS="$(awk -v t1="$T1" 'BEGIN{b=int(t1/7); if(b<10)b=10; if(b>200)b=200; print b}')"
STEPS=20000
MPDPS="$DPS"

echo
echo "=== [$(_utc) UTC] 2/3 Turing (CSV) --T0 $T0 --T1 $T1 --bins $BINS --steps $STEPS --mp-dps $MPDPS ==="
TUR_CMD="$(cmd_py turing_check.py zeta_prime_suite.turing_check) --csv "$CSV" --T0 "$T0" --T1 "$T1" --bins "$BINS" --steps "$STEPS" --mp-dps "$MPDPS""
echo "DEBUG: Executing Turing CSV command: $TUR_CMD"
if ! $TUR_CMD | tee "$LOGDIR/turing_${TS}.log"; then
  echo "!! Turing (CSV) failed; trying zeros-root fallback ..."
  ZROOT="$RUNROOT/batch"
  TUR_CMD2="$(cmd_py turing_check.py zeta_prime_suite.turing_check) --zeros-root "$ZROOT" --T0 "$T0" --T1 "$T1" --bins "$BINS" --steps "$STEPS" --mp-dps "$MPDPS""
  echo "DEBUG: Executing Turing fallback command: $TUR_CMD2"
  $TUR_CMD2 | tee -a "$LOGDIR/turing_${TS}.log" || echo "!! Turing fallback failed."
fi

# -------------------- 3/3 sieve --------------------
echo
echo "=== [$(_utc) UTC] 3/3 Sieve [2, $SIEVE_MAX]  kernel=fejer rigor=dusart ==="
mkdir -p "$RUNROOT/sieve"
SIEVE_CMD="$(cmd_py sieve_from_zeros_psi_rigorous.py zeta_prime_suite.sieve_from_zeros_psi_rigorous) \
  --zeros-root "$RUNROOT/batch" \
  --x-start 2 --x-end "$SIEVE_MAX" \
  --kernel fejer \
  --rigorous dusart \
  --rigorous-tail on --tail-C 50 \
  --wheel 210 \
  --out-primes "$RUNROOT/sieve/primes_2_${SIEVE_MAX}.txt" \
  --out-bounds "$RUNROOT/sieve/bounds_2_${SIEVE_MAX}.csv" \
  --out-windows "$RUNROOT/sieve/windows_2_${SIEVE_MAX}.csv" \
  --out-residues "$RUNROOT/sieve/residues_2_${SIEVE_MAX}.csv" \
  --out-residues-win "$RUNROOT/sieve/residues_win_2_${SIEVE_MAX}.csv" \
  --out-zeroqc "$RUNROOT/sieve/zeroqc_2_${SIEVE_MAX}.csv" \
  --out-gaps "$RUNROOT/sieve/gaps_2_${SIEVE_MAX}.csv""

echo "DEBUG: Executing Sieve command: $SIEVE_CMD"
$SIEVE_CMD | tee "$LOGDIR/sieve_${TS}.log" || {
  echo "!! Sieve failed."
}

echo
echo "FINISHED. Workdir: $WORKDIR"
echo "Logs: $LOGDIR"
