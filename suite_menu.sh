#!/usr/bin/env bash
set -Eeuo pipefail

# ------------------------------------------------------------
# Riemann Zeta Zero Finding Suite – simple orchestrator (Linux)
# Uses ONLY master_zeros.csv for Turing & Sieve
# ------------------------------------------------------------

# Resolve paths
SCRIPT_PATH="$(readlink -f "$0" || true)"
ROOT_DIR="$(dirname "${SCRIPT_PATH:-$PWD}")"

# Work directories (timestamped under CWD so it works anywhere)
STAMP="$(date -u +%Y%m%d_%H%M%S)"
WORKDIR="${WORKDIR:-$PWD/temp_${STAMP}}"
LOGDIR="$WORKDIR/logs"
RUNROOT="$WORKDIR/runs"
mkdir -p "$LOGDIR" "$RUNROOT"

echo "DEBUG: WORKDIR=$WORKDIR"
echo "DEBUG: LOGDIR=$LOGDIR"
echo "DEBUG: RUNROOT=$RUNROOT"

cat <<'LICENSE_NOTICE'
============================================================
Riemann Zeta Zero Finding Suite — proprietary source code
Copyright © 2026 Carmen Wrede and Lino Casu

No copying, modification, redistribution, sublicensing, or commercial use is
granted by this launcher. See LICENSE-CODE.md. The manuscript and non-executable
documentation have separate terms in LICENSE-DOCUMENTATION.
============================================================
LICENSE_NOTICE

# -------------------------
# Input (hours, sieve_max, dps)
# -------------------------
read -rp "Hours (>= 0.1) [default 0.1]: " HOURS_IN || true
HOURS="$(printf '%s' "${HOURS_IN:-0.1}" | tr ',' '.' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
if python3 - <<'PY' "$HOURS"; then :; else echo "Invalid hours"; exit 1; fi
import sys
try:
    h=float(sys.argv[1]); assert h>=0.1
    print("DEBUG: CLEAN_HOURS=",h)
except Exception:
    sys.exit(1)
PY

read -rp "SIEVE_MAX (>= 10) [default 100]: " SIEVE_IN || true
SIEVE_MAX="${SIEVE_IN:-100}"
if ! python3 - <<'PY' "$SIEVE_MAX"; then echo "Invalid SIEVE_MAX"; exit 1; fi
import sys
try:
    n=int(sys.argv[1]); assert n>=10
except Exception:
    sys.exit(1)
PY

read -rp "DPS (>= 1) [default 80]: " DPS_IN || true
DPS="${DPS_IN:-80}"
if ! python3 - <<'PY' "$DPS"; then echo "Invalid DPS"; exit 1; fi
import sys
try:
    n=int(sys.argv[1]); assert n>=1
except Exception:
    sys.exit(1)
PY

# -------------------------
# 1) Batch – produce master_zeros.csv
# -------------------------
echo
echo "=== [$(date -u +%H:%M:%S) UTC] 1/3 Batch run --tstart 10 --hours $HOURS --dps $DPS ==="
mkdir -p "$RUNROOT/batch"
BATCH_LOG="$LOGDIR/batch_${STAMP}.log"
BATCH_CMD=( python3 -u /usr/lib/rieman-zeta-suite/batch_until_deadline.py
  --tstart 10
  --hours "$HOURS"
  --outroot "$RUNROOT/batch"
  --dps "$DPS"
)
echo "DEBUG: Executing batch command: ${BATCH_CMD[*]}"
# run & tee
if ! "${BATCH_CMD[@]}" 2>&1 | tee "$BATCH_LOG"; then
  echo "!! Batch failed (exit=$?). See: $BATCH_LOG"
  exit 2
fi

MASTER_CSV="$RUNROOT/batch/master_zeros.csv"
if [[ ! -s "$MASTER_CSV" ]]; then
  echo "!! master_zeros.csv not found or empty: $MASTER_CSV"
  exit 3
fi

# -------------------------
# 2) Turing – FORCE using master_zeros.csv
# -------------------------
echo
echo "=== [$(date -u +%H:%M:%S) UTC] 2/3 Turing (CSV) --T0 0.1 --T1 4.0 --bins 10 --steps 20000 --mp-dps $DPS ==="
TURING_LOG="$LOGDIR/turing_${STAMP}.log"
TURING_CSV="$LOGDIR/turing_${STAMP}.csv"
TURING_CMD=( python3 -u /usr/lib/rieman-zeta-suite/turing_check.py
  --zeros-root "$RUNROOT/batch"    # required by script
  --csv "$MASTER_CSV"              # << use EXACTLY the master_zeros.csv
  --T0 0.1 --T1 4.0
  --bins 10 --steps 20000
  --mp-dps "$DPS"
)
echo "DEBUG: Executing Turing CSV command: ${TURING_CMD[*]}"
# run & tee
if ! "${TURING_CMD[@]}" 2>&1 | tee "$TURING_LOG"; then
  echo "!! Turing (CSV) failed; see $TURING_LOG"
  # continue anyway; sieve can still run with master CSV
fi

# -------------------------
# 3) Sieve – ONLY master_zeros.csv
#    Create isolated folder so scanning sees only that file
# -------------------------
echo
echo "=== [$(date -u +%H:%M:%S) UTC] 3/3 Sieve [2, $SIEVE_MAX]  kernel=fejer rigor=dusart ==="

# Make outputs + isolated zeros-root
ONLY_ZR="$RUNROOT/batch_master_only"
rm -rf "$ONLY_ZR"
mkdir -p "$ONLY_ZR"
cp -f "$MASTER_CSV" "$ONLY_ZR/master_zeros.csv"

mkdir -p "$RUNROOT/sieve"

SIEVE_LOG="$LOGDIR/sieve_${STAMP}.log"
SIEVE_CMD=( python3 -u /usr/lib/rieman-zeta-suite/sieve_from_zeros_psi_rigorous.py
  --zeros-root "$ONLY_ZR"                 # << points to folder with ONLY master_zeros.csv
  --x-start 2 --x-end "$SIEVE_MAX"
  --kernel fejer
  --rigorous dusart
  --rigorous-tail on --tail-C 50
  --wheel 210
  --out-primes       "$RUNROOT/sieve/primes_2_${SIEVE_MAX}.txt"
  --out-bounds       "$RUNROOT/sieve/bounds_2_${SIEVE_MAX}.csv"
  --out-windows      "$RUNROOT/sieve/windows_2_${SIEVE_MAX}.csv"
  --out-residues     "$RUNROOT/sieve/residues_2_${SIEVE_MAX}.csv"
  --out-residues-win "$RUNROOT/sieve/residues_win_2_${SIEVE_MAX}.csv"
  --out-zeroqc       "$RUNROOT/sieve/zeroqc_2_${SIEVE_MAX}.csv"
  --out-gaps         "$RUNROOT/sieve/gaps_2_${SIEVE_MAX}.csv"
)
echo "DEBUG: Executing Sieve command: ${SIEVE_CMD[*]}"
if ! "${SIEVE_CMD[@]}" 2>&1 | tee -a "$SIEVE_LOG"; then
  echo "!! Sieve failed. See $SIEVE_LOG"
fi

echo
echo "FINISHED. Workdir: $WORKDIR"
echo "Logs:    $LOGDIR"
