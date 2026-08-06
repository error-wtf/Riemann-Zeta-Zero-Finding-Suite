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
    trajectory_tau = np.linspace(args.t0 - args.sweep / 2, args.t0 + args.sweep / 2, 240)
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
    trajectory = np.array([
        np.sum(terms ** (-args.sigma) * np.exp(-1j * t * np.log(terms)))
        for t in trajectory_tau
    ])

    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=100)
    fig.patch.set_facecolor("#02070d")
    ax.set_facecolor("#02070d")
    ax.set_xlim(-7.2, 7.2)
    ax.set_ylim(-3.8, 3.8)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks(np.arange(-7, 8, 1))
    ax.set_yticks(np.arange(-3, 4, 1))
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
    ray_lines = []
    ray_meta = []
    # Complete mapped term geometry: sigma-lines become circles and t-lines
    # become rays under n**(-s)=exp(-s log n), exactly the structure shown in
    # the reference animation.  Keep the display finite and explicitly label
    # it as a term map, not as the analytic continuation of zeta.
    sigma_grid = np.linspace(-1.25, 1.0, 18)
    t_grid = np.linspace(-4.0, 4.0, 21)
    radial = np.linspace(0.02, 7.2, 220)
    display_terms = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    for n in display_terms:
        color = palette[n % len(palette)]
        for sigma in sigma_grid:
            radius = n ** (-sigma)
            (line,) = ax.plot(radius * np.cos(phase), radius * np.sin(phase), color=color, alpha=0.42 if n < 12 else 0.28, linewidth=0.9)
            orbit_lines.append(line)
        for tv in t_grid:
            angle = -tv * math.log(n)
            (line,) = ax.plot(radial * np.cos(angle), radial * np.sin(angle), color=color, alpha=0.34, linewidth=0.8)
            orbit_lines.append(line)
            ray_lines.append(line)
            ray_meta.append((n, tv))
    (path,) = ax.plot([], [], color="#f8a4c2", linewidth=2.2)
    (vector,) = ax.plot([], [], color="#37bdf8", linewidth=2.2)
    point, = ax.plot([], [], "o", color="#ffd84d", markersize=7)
    phase_points = [ax.plot([], [], "o", color=palette[i % len(palette)], markersize=3)[0] for i in range(min(args.terms, 12))]
    frame_text = ax.text(0.02, 0.04, "", transform=ax.transAxes, color="#f8fafc", fontsize=12)
    legend_text = ax.text(0.69, 0.83, "term orbits\npartial-sum path\ncurrent vector", transform=ax.transAxes, color="#dbeafe", fontsize=12, linespacing=1.7)

    def update(i: int):
        t = tau[i]
        current = trajectory[int(i * (len(trajectory) - 1) / max(1, args.frames - 1))]
        previous = partial[-2, i]
        path.set_data(trajectory.real, trajectory.imag)
        vector.set_data([previous.real, current.real], [previous.imag, current.imag])
        point.set_data([current.real], [current.imag])
        # Move the complete t-grid smoothly; sigma circles remain fixed.
        for line, (n, tv) in zip(ray_lines, ray_meta):
            angle = -(tv + (t - args.t0) * 0.35) * math.log(n)
            line.set_data(radial * np.cos(angle), radial * np.sin(angle))
        for n, marker in enumerate(phase_points, start=1):
            value = n ** (-args.sigma) * np.exp(-1j * t * math.log(n))
            marker.set_data([value.real], [value.imag])
        frame_text.set_text(f"finite terms N={args.terms}   σ={args.sigma:.2f}   t={t:.2f}   |S_N|={abs(current):.4f}   smooth precomputed trajectory")
        return [*orbit_lines, path, vector, point, *phase_points, frame_text]

    animation = FuncAnimation(fig, update, frames=args.frames, interval=70, blit=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    animation.save(args.output, writer=PillowWriter(fps=14), dpi=100)
    plt.close(fig)


if __name__ == "__main__":
    main()
