#!/usr/bin/env python3
"""Render a reproducible animated projection of the first prime phases."""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("artifacts/periodicity/prime_phase_torus.gif"))
    parser.add_argument("--frames", type=int, default=96)
    parser.add_argument("--maximum", type=int, default=13)
    args = parser.parse_args()
    if args.frames < 2 or args.maximum < 3:
        raise SystemExit("frames >= 2 and maximum >= 3 are required")
    primes = [2, 3, 5]
    times = [i * 0.11 for i in range(args.frames)]
    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=110)
    fig.patch.set_facecolor("#08111f")
    ax.set_facecolor("#08111f")
    ax.set_xlim(-math.pi, math.pi)
    ax.set_ylim(-math.pi, math.pi)
    ax.set_xlabel("phase of log 2", color="#cbd5e1")
    ax.set_ylabel("phase of log 3", color="#cbd5e1")
    ax.tick_params(colors="#94a3b8")
    ax.grid(alpha=.18, color="#94a3b8")
    (trace,) = ax.plot([], [], color="#f59e0b", linewidth=1.6, alpha=.65)
    (point,) = ax.plot([], [], "o", color="#38bdf8", markersize=7)
    (jump_from,) = ax.plot([], [], "o", markerfacecolor="none", markeredgecolor="#fb7185", markersize=12)
    (jump_to,) = ax.plot([], [], "o", markerfacecolor="none", markeredgecolor="#fb7185", markersize=12)
    label = ax.text(.03, .94, "", transform=ax.transAxes, color="#f8fafc")
    ax.set_title("Prime phase torus projection: (t log 2, t log 3) mod 2π", color="#f8fafc")

    def wrap(v: float) -> float:
        return (v + math.pi) % (2 * math.pi) - math.pi

    def update(i: int):
        t = times[i]
        xs = [wrap(times[j] * math.log(primes[0])) for j in range(i + 1)]
        ys = [wrap(times[j] * math.log(primes[1])) for j in range(i + 1)]
        segmented_x: list[float] = []
        segmented_y: list[float] = []
        last_jump: tuple[float, float, float, float, int] | None = None
        for j, (x_value, y_value) in enumerate(zip(xs, ys)):
            if j and (
                abs(x_value - xs[j - 1]) > math.pi
                or abs(y_value - ys[j - 1]) > math.pi
            ):
                segmented_x.append(math.nan)
                segmented_y.append(math.nan)
                last_jump = (xs[j - 1], ys[j - 1], x_value, y_value, j)
            segmented_x.append(x_value)
            segmented_y.append(y_value)
        trace.set_data(segmented_x, segmented_y)
        point.set_data([xs[-1]], [ys[-1]])
        if last_jump is not None and i - last_jump[4] < 5:
            jump_from.set_data([last_jump[0]], [last_jump[1]])
            jump_to.set_data([last_jump[2]], [last_jump[3]])
        else:
            jump_from.set_data([], [])
            jump_to.set_data([], [])
        score = max(abs(complex(math.cos(t * math.log(p)), math.sin(t * math.log(p))) - 1) for p in primes)
        jump_label = "   torus wrap jump" if last_jump is not None and i == last_jump[4] else ""
        label.set_text(f"t={t:.2f}   return score (2,3,5)={score:.3f}{jump_label}")
        return trace, point, jump_from, jump_to, label

    animation = FuncAnimation(fig, update, frames=args.frames, interval=45, blit=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    animation.save(args.output, writer=PillowWriter(fps=20))
    plt.close(fig)


if __name__ == "__main__":
    main()
