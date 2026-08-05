# Riemann Zeta Zero-Finding Suite

This repository contains a **modular Python toolkit** for studying the Riemann–Zeta function on the critical line and testing candidate zero certificates. It combines complete available Hardy-`Z` evaluations, an explicitly labelled leading Riemann–Siegel main-sum approximation, interval-style diagnostics, adaptive scanning techniques, and prime-sieving experiments. The current interval paths are numerical enclosures unless an independently validated outward-rounded Arb path is selected; this README keeps that distinction explicit.

## Motivation and Background

The non-trivial zeros of the Riemann–Zeta function play a central role in analytic number theory. Hardy's `Z`-function `Z(t)` evaluates zeta(1/2 + i*t) up to a phase so that zeros of `Z(t)` correspond to zeros on the critical line. Our suite uses exact mpmath zeta evaluation at small heights and the complete available `mpmath.siegelz` evaluation at larger heights. The leading Riemann–Siegel main sum remains available under the explicit `Z_rs_main_sum` helper for exploratory scans. Interval modules return numerical enclosures and diagnostic derivative bounds; they must not be called mathematical proof certificates unless their outward-rounding assumptions and remainder bounds have been independently validated.

### Core Concepts

- **Adaptive scanning of Hardy's `Z`-function.**  `zeta_zero_finder.py` scans a height interval `[T1, T2]` with a step proportional to the local wavelength (Delta t ~= 2*pi / log(t/(2*pi))) so sign changes aren't skipped. Found brackets are refined by bisection, optional secant, and (optionally) Chebyshev interpolation.

- **Candidate certification with interval diagnostics.**  `run_block.py` uses interval-style evaluations of `Z(t)` to test sign changes and local uniqueness. JSON records preserve brackets, derivative margins and method metadata; they are numerical candidate certificates unless validated outward-rounded Arb, complete remainder bounds and an independent counting argument are all present.

- **Turing checks as a consistency diagnostic.**  After each block, the number of detected zeros is compared with the Riemann–von–Mangoldt prediction. Mismatches should trigger rescans (finer step, higher precision, Gram fallback); they are not silently converted into a pass.

- **Prime-counting via the explicit formula.**  Using certified zeros, `sieve_from_zeros_psi_rigorous.py` estimates psi(x+h) - psi(x) with smoothing kernels and a tail bound; if needed it runs a segmented sieve to produce rigorous bounds for pi(x).

---

# Quick Start (from a cloned repo)

This project includes simple launcher scripts so you can run the suite without learning all internal Python entrypoints first.

* **Linux / macOS:** `./suite_menu.sh` (Bash)
* **Windows:** `rieman-zeta-zero.bat` (calls `rieman-zeta-zero.ps1`)

Both launchers ask only for:

* **Hours** (how long to run the batch; minimum `0.1`)
* **SIEVE_MAX** (upper bound for prime sieving; e.g. `100000` for 1e5)
* **DPS** (decimal precision for math; e.g. `80`)

They then run three steps in order:

1. compute zeros for about the requested time,
2. do a Turing consistency check,
3. run a rigorous sieve using the zeros just computed.

---

## Prerequisites

* **Python 3.10+** on PATH
  (Windows users: the scripts try `py -3`, then `python3`, then `python`.)
* Project dependencies (from the repo root):

  ```bash
  pip install -r requirements.txt
  export LC_ALL=C
  export LANG=C
  ```
* Bash (Linux/macOS) or PowerShell (Windows).
  The Windows `.bat` file launches PowerShell with a relaxed execution policy just for this run.

> **License notice (ACSL 1.4):** The launcher prints the Anti-Capitalist Software License header on start. By using these scripts you agree to the terms. See `LICENSE` for the full text.

---

## Linux / macOS

1. Open a terminal and `cd` into the repo folder.
2. Make the script executable (first time only):

   ```bash
   chmod +x suite_menu.sh
   ```
3. Run it:

   ```bash
   ./suite_menu.sh
   ```
4. You’ll be asked:

   * `Hours (>= 0.1) [default 0.1]:`
   * `SIEVE_MAX (>= 10) [default 1000000]:`
   * `DPS (>= 1) [default 80]:`

The script creates a timestamped working directory like `temp_YYYYMMDD_HHMMSS` in the current folder, with subfolders:

```
temp_YYYYMMDD_HHMMSS/
  ├─ logs/
  └─ runs/
      ├─ batch/   # zeros, master_zeros.csv
      └─ sieve/   # primes, bounds, windows, residues, gaps
```

---

## Windows

1. Open the repo folder in Explorer.
2. Double-click **`rieman-zeta-zero.bat`**.
   (It starts `rieman-zeta-zero.ps1` and prints the same ACSL header and prompts.)
3. Answer the three prompts. That’s it.

The working directory `temp_YYYYMMDD_HHMMSS` is created next to the scripts, with the same `logs/` and `runs/` layout as on Linux.

---

## What happens under the hood

* **Batch (zeros):**
  Runs `batch_until_deadline.py` with your `Hours` value (e.g., `0.1` → ~0.1 hours).
  Output: `runs/batch/master_zeros.csv` and per-block files.

* **Turing check:**
  Validates zeros over a small, safe interval (e.g., `T ∈ [0.1, 4]`) with conservative defaults.
  If the direct CSV mode complains, the launcher automatically falls back to `--zeros-root`.

* **Rigorous sieve:**
  Calls `sieve_from_zeros_psi_rigorous.py` from `x = 2` up to your `SIEVE_MAX`, using:

  * `--kernel fejer`
  * `--rigorous dusart`
  * `--rigorous-tail on --tail-C 50`
  * `--wheel 210`
    Outputs go to `runs/sieve/` (primes list, bounds, windows, residues, gaps).

All console output is also written to `logs/` (one file per step).

---

## Important runtime note (blocks)

The batch runs in **blocks**. It will **always finish the current block** before stopping, even if the requested time has elapsed. That means:

* `Hours = 0.1` (≈6 minutes) may actually take **~10–20 minutes** depending on CPU speed and where the block ends.
* This is expected and avoids truncated, low-quality outputs.

---

## Example session (shortened)

```
$ ./suite_menu.sh
============================================================
Anti-Capitalist Software License (ACSL), Version 1.4
... (license text) ...
============================================================
Hours (>= 0.1) [default 0.1]: 1
SIEVE_MAX (>= 10) [default 100000]: 100000
DPS (>= 1) [default 80]: 80

=== [00:01:07 UTC] 1/3 Batch run --tstart 10 --hours 1 --dps 80 ===
[batch] start t=10.000000, run for ~1.0h ...
[block 1] [10.000, 31.830] ...
[done] master_zeros.csv contains N zeros: runs/batch/master_zeros.csv

=== [..] 2/3 Turing (CSV) ... ===
[turing] Interval [0.100000, 4.000000] ...

=== [..] 3/3 Sieve [2, 100000] kernel=fejer rigor=dusart ===
[out] wrote primes: runs/sieve/primes_2_100000.txt
... Done. Logs: logs/
```

---

## Troubleshooting

* **`Python not found`**
  Install Python 3.10+ and make sure `python`/`python3` (Linux/macOS) or `py -3` (Windows) is on PATH.

* **`master_zeros.csv not found` after batch**
  The batch finished too quickly or didn’t complete a block. Increase `Hours` and try again.

* **Turing complains that `--zeros-root` is required**
  The launcher already retries in a fallback mode. Check `logs/turing_*.log` for details.

* **Sieve outputs are empty/small for tiny SIEVE_MAX**
  That’s normal for very small ranges. Increase `SIEVE_MAX` for more meaningful results.

* **Interrupting runs**
  Avoid `Ctrl+C` during a block; you might get partial results. If you must stop, rerun later with a larger `Hours`.

---

## Reproducibility & Logs

Each run writes a dated working directory:

* All step logs: `logs/`
* Batch zeros: `runs/batch/`
* Sieve artifacts: `runs/sieve/`

Keep these folders if you want to compare results or resume work later.

---

## Installation

Requirements: **Python 3.10+**, mpmath, numpy.

```bash
python3 -m venv venv
source venv/bin/activate
pip install mpmath numpy
```

Clone or extract this repository and run the scripts from the project root. No compilation is required.

## Module Overview

Each script supports `-h/--help` for details.

### `common.py`

Core math utilities:

* `theta(t)` — Riemann's theta function.
* `Z(t)` — complete available Hardy's Z evaluation (exact zeta below a switch, `mpmath.siegelz` above).
* `Z_exact(t)`, `Z_rs(t)`, `Z_rs_main_sum(t)` — exact, complete Siegel, and explicitly approximate leading-sum paths.

### `rigorous_Z.py`

Interval arithmetic:

* `eval_ZZp_interval(t, rad, dps)` returns interval enclosures for `Z(t)`, `Z'(t)` and a Lipschitz constant.
* `sign_from_interval(iv)` robustly decides the sign of `Z` on a small neighbourhood.

### `zeta_zero_finder.py`

Adaptive scanner (approximate by default, with rigorous options):

* **Scan** `[T1,T2]` with (Delta t proportional to 2*pi / log(t)).
* **Refine** by bisection, optional secant and optional Chebyshev interpolation.
* **Merge** only numerically identical estimates; close physical zeros are never
  removed by a mean-spacing heuristic. Certified interval overlap is the
  preferred deduplication mechanism.
* **Output** CSV (and optionally JSON per block).

**CLI options (selection)**:

```
--tmin, --tmax      start and end heights
--block             block size for batching write-out
--out               CSV file to append zeros
--dps               decimal precision (mpmath)
--bisect-steps      bisection iterations per bracket
--no-sec            disable secant refinement
--dedup             remove near duplicates
--fixed-step        override adaptive step with a constant step
--adapt-scale       scaling for adaptive step (Delta t ~= adapt_scale * 2*pi/log(t))
--json              also emit JSON certificates per block
--cheb              enable Chebyshev interpolation refinement
--cheb-k            number of Chebyshev nodes (degree = k-1)
```

**Example**:

```bash
python3 zeta_zero_finder.py \
  --tmin 10 --tmax 50 --dps 80 \
  --cheb --cheb-k 8 \
  --out zeros_10_50.csv
```

### `run_block.py`

**Candidate certification** on `[T1,T2]` using interval-style diagnostics and repeated halving to reduce missed sign changes. Formal certification requires independently validated outward rounding, complete approximation remainders and a counting theorem.

**Parameters** (programmatic use):

* `T1, T2` — block endpoints
* `scan_step` — fixed step (ignored if `adaptive=True`)
* `adaptive` — enable adaptive scanning
* `adapt_scale` — scale for adaptive step
* `min_step`, `max_step` — hard bounds for the step
* `eps` — target bracket width for certification
* `dps` — precision for interval calculations

**Example**:

```bash
python3 - <<'PY'
import run_block
print(run_block.run_block(20, 40, adaptive=True, adapt_scale=0.25, dps=60))
PY
```

The return object includes metadata (precision, step config) and a list of JSON-serializable **certificates** (interval, margins, uniqueness checks).

### `batch_until_deadline.py`

Run consecutive blocks until a time budget is consumed.

```
--tstart   starting height
--hours    wall-time budget in hours (float)
--outroot  output directory (CSV/JSON per block)
--dps      precision
--adapt-scale, --min-step, --max-step  as in run_block
```

**Example**:

```bash
python3 batch_until_deadline.py --tstart 10 --hours 3 --outroot run3h --dps 60
```

### `run_certified_all.py`

End-to-end wrapper: scanning -> certification -> Turing check across blocks; merges CSV/JSON and writes consolidated outputs.

### `zeros_by_scan.py`

Lightweight exploratory scanner (approximate). Supports adaptive step and **repeated halving** when no sign change is seen. Use for quick reconnaissance and then verify with `run_block.py`.

**Example (API)**:

```python
from zeros_by_scan import find_zeros_scan
zeros = find_zeros_scan(10.0, 60.0, adaptive=True, adapt_scale=0.25)
print(zeros)
```

### `zeros_by_gram.py`

Uses Gram points g_n (solutions of theta(g_n) = n*pi) to bracket zeros efficiently; refine by bisection.

### `turing_check.py` / `turin_watchdog.py`

* `turing_check.py`: Compare counted zeros with Riemann–von–Mangoldt expectation on bins; warn on discrepancies.
* `turin_watchdog.py`: Automate rescans on failing bins.

### `merge_zeros.py` / `count_certified.py`

* `merge_zeros.py`: merge overlapping CSV/JSON zero lists.
* `count_certified.py`: count certified zeros; optionally compare to theoretical counts.

### `sieve_from_zeros_psi_rigorous.py` / `explicit_tail.py`

Prime-counting via the explicit formula for psi(x) using certified zeros; supports Fejer/Parzen smoothing and a configurable tail bound. Can trigger a segmented sieve (mod 210) when necessary. Results written to `prime_bounds.csv`.

## Workflows

### 1) Rigorous zero finding on a range

```bash
python3 run_certified_all.py \
  --tmin 10 --tmax 100 --block 10 \
  --dps 60 --adapt-scale 0.25 --min-step 0.002
```

* Writes block CSV/JSON with certificates.
* Performs Turing checks; if a mismatch occurs, re-scan that block with finer settings.

### 2) Manual Turing check on one CSV

```bash
python3 turing_check.py --csv runs/block_10_20/zeros.csv --t1 10 --t2 20
```

### 3) Prime bounds from certified zeros

```bash
python3 sieve_from_zeros_psi_rigorous.py \
  --lower 1000000000 --upper 1000000000+1000000 \
  --zeros runs/big_run/certified_zeros.csv \
  --kernel fejer
```

## Recent Improvements (what's new)

* **Repeated halving on scan** (in `run_block.py`, `zeta_zero_finder.py`, `zeros_by_scan.py`): if the full step shows no sign change, halve repeatedly until either a change is found or the step falls below about 1.5*min_step. This eliminates missed zeros in highly oscillatory regions.

* **Chebyshev refinement** (optional): after bisection (and optional secant), fit a Chebyshev polynomial on the bracket and take the closest root; improves accuracy with few evaluations.

* **Sharper Turing control**: bin-wise Riemann–von–Mangoldt comparisons; automatic rescan hooks for blocks with mismatches.

* **Logging & modularity**: consistent progress logs; results in CSV/JSON; components can be swapped (e.g., Arb-based certifier).

## Tips, Limits, Best Practices

* **Precision vs. speed**: increase `dps` and decrease `eps` for final certification runs; for exploration, keep `dps` around 60–80.

* **RS regime caution**: near the RS switch (e.g., t >= ~50) the main sum alone may give coarse brackets; prefer interval methods for certification.

* **Chebyshev stability**: use moderate `--cheb-k` (6–12). Validate with secant/Newton if the bracket is wide.

* **Reproducibility**: fix RNG seeds (if any) and record `dps`, step parameters, and certificate metadata.

## Quick Reference (common commands)

```bash
# Adaptive, approximate scan with Chebyshev refinement
python3 zeta_zero_finder.py --tmin 10 --tmax 60 --dps 80 --cheb --cheb-k 8 --out zeros_10_60.csv

# Rigorous certification on a single block
python3 - <<'PY'
import run_block
out = run_block.run_block(40, 60, adaptive=True, adapt_scale=0.25, min_step=0.002, dps=80)
print(out["certificates"])
PY

# Time-boxed batch run (e.g. 3 hours)
python3 batch_until_deadline.py --tstart 10 --hours 3 --outroot run3h --dps 60

# Merge and count
python3 merge_zeros.py --in runs/run3h --out merged/certified_zeros.csv
python3 count_certified.py --in merged/certified_zeros.csv
```

## Acknowledgements & References

* Classical references on Hardy's `Z`, Riemann–Siegel, Gram points, Turing checks, and explicit prime-counting formulas.
* Empirical reference lists of low-lying zeros (e.g., tables by Odlyzko) are useful for sanity checks in small intervals.
* The accompanying analysis PDFs in this repository describe design decisions, benchmarks, and further improvement ideas (e.g., Arb-based certifiers, FFT-accelerated evaluations, Gram-guided rescans).

---

## License

Anti-Capitalist Software License (ACSL) 1.4  
Copyright (c) 2025 Lino Casu and Carmen Wrede

Summary (non-binding, for convenience only):
- You may use, modify, and distribute this software, but **not** for the purpose of generating profit, advertising, or in service of capitalist enterprise.  
- You may **not** use it on behalf of organizations or individuals who fund, support, or perform exploitation, oppression, surveillance, policing, incarceration, or warfare.  
- Any distribution must keep this license and attribution intact and apply the same license to derivative works.  
- The full legal text is provided in the `LICENSE` file of this repository.

If the `LICENSE` file is not yet present, create a new file named `LICENSE` at the repository root and paste the complete text of ACSL v1.4 with the copyright line:

```
Anti-Capitalist Software License (ACSL), Version 1.4
Copyright (c) 2025 Lino Casu and Carmen Wrede
```

