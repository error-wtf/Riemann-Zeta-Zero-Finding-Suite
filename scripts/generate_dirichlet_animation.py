"""Generate a finite Dirichlet partial-sum animation.

The animation is explanatory only.  It visualises
S_k(s) = sum_{n <= k} n**(-s) for a finite N and never claims convergence
outside the domain where the Dirichlet series is known to converge.
"""

from __future__ import annotations

import argparse
import cmath
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def partial_sums(sigma: float, t: float, terms: int) -> list[complex]:
    total = 0j
    values: list[complex] = []
    for n in range(1, terms + 1):
        total += cmath.exp(-(sigma + 1j * t) * cmath.log(n))
        values.append(total)
    return values


def build_animation(output: Path, sigma: float, t: float, terms: int, frames: int) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    trajectories = [partial_sums(sigma, t, terms) for _ in range(frames)]
    # Slowly vary t so the same finite Dirichlet geometry visibly evolves.
    for frame in range(frames):
        trajectories[frame] = partial_sums(sigma, t + 0.08 * frame, terms)
    radius = max(1.0, max(abs(point) for path in trajectories for point in path))

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=110)
    fig.patch.set_facecolor("#07111f")
    ax.set_facecolor("#07111f")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-radius * 1.08, radius * 1.08)
    ax.set_ylim(-radius * 1.08, radius * 1.08)
    ax.grid(color="#24425a", alpha=0.55)
    ax.axhline(0, color="#8aa4b8", lw=0.7)
    ax.axvline(0, color="#8aa4b8", lw=0.7)
    ax.set_xlabel("Re S_k(s)", color="#d8e6f0")
    ax.set_ylabel("Im S_k(s)", color="#d8e6f0")
    ax.tick_params(colors="#b8cad7")
    title = ax.set_title("Dirichlet partial sums: zeta(s) = sum n^{-s}", color="white")
    path_line, = ax.plot([], [], color="#e9c46a", lw=1.8)
    vector_line, = ax.plot([], [], color="#4ea8de", lw=2.0)
    point, = ax.plot([], [], "o", color="#f28f3b", ms=6)
    text = ax.text(0.02, 0.96, "", transform=ax.transAxes, color="#d8e6f0", va="top")

    def update(frame: int):
        values = trajectories[frame]
        xs = [z.real for z in values]
        ys = [z.imag for z in values]
        path_line.set_data(xs, ys)
        k = min(terms, max(1, 1 + frame * terms // frames))
        current = values[k - 1]
        previous = values[k - 2] if k > 1 else 0j
        vector_line.set_data([previous.real, current.real], [previous.imag, current.imag])
        point.set_data([current.real], [current.imag])
        text.set_text(f"sigma={sigma:.2f}, t={t + 0.08 * frame:.2f}, k={k}/{terms}")
        return path_line, vector_line, point, text, title

    animation = FuncAnimation(fig, update, frames=frames, interval=90, blit=True)
    animation.save(output, writer=PillowWriter(fps=11), dpi=110)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("artifacts/periodicity/dirichlet_partial_sums.gif"))
    parser.add_argument("--sigma", type=float, default=1.2)
    parser.add_argument("--t", type=float, default=14.1)
    parser.add_argument("--terms", type=int, default=120)
    parser.add_argument("--frames", type=int, default=36)
    args = parser.parse_args()
    if args.sigma <= 1 or args.terms < 2 or args.frames < 2:
        raise SystemExit("use sigma > 1, terms >= 2 and frames >= 2 for the convergent Dirichlet-series illustration")
    build_animation(args.output, args.sigma, args.t, args.terms, args.frames)
    print(args.output)


if __name__ == "__main__":
    main()
