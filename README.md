# Perfect Riemann Zero Runner (rigorous + hourly QC)

**Workflow**
1) Finder (Terminal 1): adaptive Schrittweite (`rho`), Hybrid-Zertifizierung.
2) Merge (stündlich) + Turing-Wächter (Terminal 2).
3) Bei Block-Mismatch → Auto-Rescan nur des Blocks (engerer Step, dps↑, arb-Fallback).

**Finder (Beispiel)**
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run_until_deadline.ps1 `
  -TStart 8 -Hours 48 -OutRoot "runs/big_run_48h_final" `
  -Dps 120 -MinBlock 2 -MaxBlock 12 -Mult 4 -Rho 0.6 -AutoRestart
```
**Watcher**
```
python all_in_one_runner.py --merge-roots runs/big_run_48h_final \
  --out-merged runs/merged_runs --minutes 60 --T0 0.1 --T1 2000 \
  --bins 80 --steps 20000 --noS
```

Block-QC

consistency.match muss True sein.

params loggt dps, rho, scan_step_max etc.

Zertifikat hat meta.certifier_used ∈ {mp, arb}.

Tipps

Wenn einzelne Bins im globalen Turing ±1 zeigen, aber --no-S OK ist → Unwrap-Kante, kein Loch.

Härten: scan_step_max → 0.005, dps +8..+16, certifier="arb" für gezielte Rescans.

```
---

## 4) Zur Sicherheit nochmal die vier Hauptdateien (frische Links)
- `run_block.py` – [öffnen](sandbox:/mnt/data/run_block.py)  :contentReference[oaicite:0]{index=0}  
- `run_certified_all.py` – [öffnen](sandbox:/mnt/data/run_certified_all.py)  :contentReference[oaicite:1]{index=1}  
- `batch_until_deadline.py` – [öffnen](sandbox:/mnt/data/batch_until_deadline.py)  :contentReference[oaicite:2]{index=2}  
- `run_until_deadline.ps1` – [öffnen](sandbox:/mnt/data/run_until_deadline.ps1)

> Falls du magst, kann ich dir **alle** sechs Dateien auch als **PowerShell-Installer** (ein einziges `.ps1`, das die Files lokal schreibt) bereitstellen – das umgeht jegliche Link-Probleme komplett.

Sag Bescheid, wenn irgendeiner der Links spinnt; dann droppe ich die Inhalte direkt nochmal hier im Chat. 💪
::contentReference[oaicite:3]{index=3}
```

