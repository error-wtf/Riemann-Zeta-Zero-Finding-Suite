#!/usr/bin/env python3
"""Render a complete two-sided finite term-map animation.

Every displayed circle is sampled over 0..2*pi and is therefore a closed
curve; the chosen radii are fitted inside the declared viewport.  This is a
finite explanatory map of n**(-s), not the infinite zeta function itself.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, default=Path("artifacts/periodicity/zeta_full_curve.gif"))
    p.add_argument("--frames", type=int, default=36)
    p.add_argument("--terms", type=int, default=12)
    args = p.parse_args()
    radii = np.array([0.32, 0.48, 0.72, 1.0, 1.35, 1.8, 2.35, 3.0, 3.8, 4.7, 5.7, 6.55])
    terms = np.arange(2, min(args.terms, 12) + 1, dtype=float)
    phase = np.linspace(0.0, 2.0 * math.pi, 720)
    colors = ["#f5df4d", "#e7a1b4", "#a9c3c8", "#b8b1f0", "#8de0d0"]
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=100)
    fig.patch.set_facecolor("#02070d")
    ax.set_facecolor("#02070d")
    ax.set_xlim(-7.2, 7.2)
    ax.set_ylim(-7.2, 7.2)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks(np.arange(-7, 8, 1))
    ax.set_yticks(np.arange(-7, 8, 1))
    ax.grid(color="#12435a", linewidth=.9, alpha=.8)
    ax.axhline(0, color="#a9b9c8", linewidth=1.1)
    ax.axvline(0, color="#a9b9c8", linewidth=1.1)
    ax.tick_params(colors="#f8fafc", labelsize=12)
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.set_xlabel("Re", color="#f8fafc", fontsize=14)
    ax.set_ylabel("Im", color="#f8fafc", fontsize=14)
    fig.text(.035, .93, "Riemann zeta function", color="white", fontsize=30, family="serif")
    fig.text(.06, .83, r"$\zeta(s)=\sum_{n=1}^{\infty}n^{-s}$", color="white", fontsize=28, family="serif")
    fig.text(.70, .93, r"$s=\sigma+i t$", color="#dbeafe", fontsize=20, family="serif")
    rings = []
    markers = []
    for i, n in enumerate(terms):
        col = colors[i % len(colors)]
        for j, radius in enumerate(radii):
            ring_col = colors[(i + j) % len(colors)]
            (line,) = ax.plot(radius * np.cos(phase), radius * np.sin(phase), color=ring_col, alpha=.70, linewidth=1.0)
            rings.append(line)
        (marker,) = ax.plot([], [], "o", color=col, markersize=3.5, alpha=.95)
        markers.append((marker, radii[-1], n))
    label = ax.text(.02, .04, "", transform=ax.transAxes, color="#f8fafc", fontsize=12)

    def update(i: int):
        shift = (i / max(1, args.frames - 1) - .5) * 2.4
        for marker, radius, n in markers:
            angle=-(shift+0.08*n)*math.log(n)
            marker.set_data([radius*math.cos(angle)],[radius*math.sin(angle)])
        label.set_text(f"complete closed term curves · finite n=2..{int(terms[-1])} · full two-sided viewport · no rays · phase={shift:+.2f}")
        return [*rings, *(m[0] for m in markers), label]

    animation = FuncAnimation(fig, update, frames=args.frames, interval=80, blit=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    animation.save(args.output, writer=PillowWriter(fps=12), dpi=100)
    plt.close(fig)


if __name__ == "__main__":
    main()
