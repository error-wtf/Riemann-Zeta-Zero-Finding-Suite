#!/usr/bin/env python3
"""Render a high-quality, finite complex-plane zeta term/orbit animation.

This is an explanatory visual: for fixed sigma, each term n**(-s) with
s=sigma+i*t traces a circle of radius n**(-sigma) as t varies.  The
partial-sum path is shown separately.  No convergence claim is made for
sigma <= 1.
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("artifacts/periodicity/zeta_complex_plane.gif"))
    parser.add_argument("--frames", type=int, default=72)
    parser.add_argument("--terms", type=int, default=36)
    parser.add_argument("--sigma", type=float, default=0.5)
    parser.add_argument("--t0", type=float, default=14.1)
    parser.add_argument("--sweep", type=float, default=8.0)
    args = parser.parse_args()
    if args.frames < 2 or args.terms < 2 or args.sigma <= 0:
        raise SystemExit("frames >= 2, terms >= 2 and sigma > 0 are required")

    tau = np.linspace(args.t0 - args.sweep / 2, args.t0 + args.sweep / 2, args.frames)
    phase = np.linspace(-math.pi, math.pi, 360)
    terms = np.arange(1, args.terms + 1, dtype=float)
    radii = terms ** (-args.sigma)
    palette = ["#f5df4d", "#e7a1b4", "#a9c3c8", "#b8b1f0", "#8de0d0"]

    # Precompute all finite geometry before constructing the animation.
    orbits = np.array([r * np.exp(-1j * phase * math.log(n)) for n, r in zip(terms, radii)])
    partial = np.array([
        [np.sum(terms[:k] ** (-args.sigma) * np.exp(-1j * t * np.log(terms[:k]))) for t in tau]
        for k in range(1, args.terms + 1)
    ])

    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=100)
    fig.patch.set_facecolor("#02070d")
    ax.set_facecolor("#02070d")
    ax.set_xlim(-2.25, 2.25)
    ax.set_ylim(-1.55, 1.55)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks(np.arange(-2, 2.1, 0.5))
    ax.set_yticks(np.arange(-1.5, 1.6, 0.5))
    ax.grid(color="#12435a", linewidth=0.9, alpha=0.75)
    ax.axhline(0, color="#a9b9c8", linewidth=1.1)
    ax.axvline(0, color="#a9b9c8", linewidth=1.1)
    ax.tick_params(colors="#dbeafe", labelsize=12)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xlabel("Re", color="#e5e7eb", fontsize=14)
    ax.set_ylabel("Im", color="#e5e7eb", fontsize=14)
    fig.text(0.04, 0.92, "Riemann zeta function", color="white", fontsize=29, family="serif")
    fig.text(0.05, 0.83, r"$\zeta(s)=\sum_{n=1}^{\infty} n^{-s}$", color="white", fontsize=27, family="serif")
    fig.text(0.69, 0.92, r"$s=\sigma+i t$", color="#dbeafe", fontsize=20, family="serif")

    orbit_lines = []
    for i in range(args.terms):
        (line,) = ax.plot(orbits[i].real, orbits[i].imag, color=palette[i % len(palette)], alpha=0.20 if i > 4 else 0.42, linewidth=0.75)
        orbit_lines.append(line)
    (path,) = ax.plot([], [], color="#f8a4c2", linewidth=2.2)
    (vector,) = ax.plot([], [], color="#37bdf8", linewidth=2.2)
    point, = ax.plot([], [], "o", color="#ffd84d", markersize=7)
    phase_points = [ax.plot([], [], "o", color=palette[i % len(palette)], markersize=3)[0] for i in range(min(args.terms, 12))]
    frame_text = ax.text(0.02, 0.04, "", transform=ax.transAxes, color="#f8fafc", fontsize=12)
    legend_text = ax.text(0.69, 0.83, "term orbits\npartial-sum path\ncurrent vector", transform=ax.transAxes, color="#dbeafe", fontsize=12, linespacing=1.7)

    def update(i: int):
        t = tau[i]
        current = partial[-1, i]
        previous = partial[-2, i]
        path.set_data(partial[:, i].real, partial[:, i].imag)
        vector.set_data([previous.real, current.real], [previous.imag, current.imag])
        point.set_data([current.real], [current.imag])
        for n, marker in enumerate(phase_points, start=1):
            value = n ** (-args.sigma) * np.exp(-1j * t * math.log(n))
            marker.set_data([value.real], [value.imag])
        frame_text.set_text(f"finite terms N={args.terms}   σ={args.sigma:.2f}   t={t:.2f}   |S_N|={abs(current):.4f}")
        return [*orbit_lines, path, vector, point, *phase_points, frame_text]

    animation = FuncAnimation(fig, update, frames=args.frames, interval=70, blit=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    animation.save(args.output, writer=PillowWriter(fps=14), dpi=100)
    plt.close(fig)


if __name__ == "__main__":
    main()
