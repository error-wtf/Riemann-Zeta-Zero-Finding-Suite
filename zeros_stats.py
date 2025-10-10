#!/usr/bin/env python3
# zeros_stats.py
import math, csv, argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def dedup_sorted(arr, tol=1e-6):
    out=[arr[0]]
    for x in arr[1:]:
        if abs(x-out[-1])>tol: out.append(x)
    return np.array(out)

def mean_spacing_factor(gamma):
    # local mean spacing ≈ (2π)/log(gamma)  -> normalization factor is its reciprocal:
    return math.log(gamma/(2*math.pi))/(2*math.pi)

def wigner_surmise_pdf(s):
    # GUE nearest-neighbour "Wigner surmise"
    return (32/(math.pi**2))*(s**2)*np.exp(-4*(s**2)/math.pi)

def pair_correlation(svals, umax=5.0, nbins=1000):
    # very simple estimator: histogram of all |k-j| spacings normalized
    # (for small samples this is noisy; good for a first look)
    # Build all differences up to umax
    diffs=[]
    for i in range(len(svals)):
        acc=0.0
        for j in range(i+1, len(svals)):
            acc += svals[j]
            if acc>umax: break
            diffs.append(acc)
    if not diffs: return None, None
    diffs=np.array(diffs)
    bins=np.linspace(0,umax,nbins+1)
    H, edges=np.histogram(diffs, bins=bins, density=True)
    centers=0.5*(edges[:-1]+edges[1:])
    return centers, H

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="zeros_block.csv")
    ap.add_argument("--outdir", default="stats_out")
    ap.add_argument("--plot", action="store_true")
    ap.add_argument("--paircorr", action="store_true")
    args = ap.parse_args()

    outdir=Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.csv)
    if "t_zero" not in df.columns:
        df.columns=["t_zero"]+[f"c{i}" for i in range(1,len(df.columns))]
    gammas = np.sort(pd.to_numeric(df["t_zero"], errors="coerce").dropna().to_numpy())
    gammas = dedup_sorted(gammas, tol=1e-6)

    # normalized gaps
    gaps = np.diff(gammas)
    norms = np.array([mean_spacing_factor(g) for g in gammas[:-1]])
    s = gaps * norms
    pd.DataFrame({"gamma_i":gammas[:-1], "gap":gaps, "s_norm":s}).to_csv(outdir/"gaps_normalized.csv", index=False)

    print(f"zeros: {len(gammas)}  mean(s)~{np.mean(s):.4f}  var(s)~{np.var(s):.4f}")

    if args.plot:
        # histogram vs Wigner surmise
        plt.figure(figsize=(7,5))
        bins = np.linspace(0,4,60)
        plt.hist(s, bins=bins, density=True, alpha=0.5, label="data")
        xx=np.linspace(0,4,600)
        plt.plot(xx, wigner_surmise_pdf(xx), label="GUE Wigner", linewidth=2)
        plt.xlabel("normalized spacing s")
        plt.ylabel("density")
        plt.title("Nearest-neighbour spacing (normalized)")
        plt.legend(); plt.tight_layout()
        plt.savefig(outdir/"hist_vs_GUE.png", dpi=140)

    if args.paircorr:
        u, R = pair_correlation(s, umax=5.0, nbins=250)
        if u is not None:
            plt.figure(figsize=(7,5))
            plt.plot(u, R, label="empirical")
            # Montgomery prediction: 1 - (sin(pi u)/(pi u))^2  (rough overlay)
            uu=np.linspace(0.01,5.0,800)
            pred = 1.0 - (np.sin(math.pi*uu)/(math.pi*uu))**2
            plt.plot(uu, pred, linestyle="--", label="1 - (sin πu / πu)^2")
            plt.xlabel("u"); plt.ylabel("R2(u)")
            plt.title("Pair correlation (rough estimator)")
            plt.legend(); plt.tight_layout()
            plt.savefig(outdir/"paircorr.png", dpi=140)

if __name__=="__main__":
    main()
