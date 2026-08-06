"""Generate an explanatory GIF of Dirichlet frequencies log(n).

Prime bars are highlighted because log(n) is an integer combination of the
prime frequencies log(p). The image is a visual research aid, not a proof.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def is_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, int(math.sqrt(n)) + 1))


def build_animation(output: Path, maximum: int, frames: int) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    numbers = list(range(2, maximum + 1))
    frequencies = [math.log(n) for n in numbers]
    periods = [2 * math.pi / f for f in frequencies]
    fig, (ax_freq, ax_period) = plt.subplots(2, 1, figsize=(8, 5), dpi=110)
    fig.patch.set_facecolor("#07111f")
    for ax in (ax_freq, ax_period):
        ax.set_facecolor("#07111f")
        ax.tick_params(colors="#b8cad7")
        ax.grid(color="#24425a", alpha=0.55)
    ax_freq.set_ylabel("log(n)", color="#d8e6f0")
    ax_period.set_ylabel("2π / log(n)", color="#d8e6f0")
    ax_period.set_xlabel("n", color="#d8e6f0")
    ax_freq.set_xlim(1, maximum + 1)
    ax_period.set_xlim(1, maximum + 1)
    ax_freq.set_ylim(0, max(frequencies) * 1.15)
    ax_period.set_ylim(0, max(periods) * 1.15)
    title = fig.suptitle("Dirichlet frequencies and individual periods", color="white")
    bars_f = ax_freq.bar(numbers, frequencies, color="#4ea8de")
    bars_p = ax_period.bar(numbers, periods, color="#b8860b")
    for n, bf, bp in zip(numbers, bars_f, bars_p):
        if is_prime(n):
            bf.set_color("#f28f3b")
            bp.set_color("#f28f3b")

    def update(frame: int):
        scale = 0.92 + 0.08 * math.sin(2 * math.pi * frame / frames)
        for n, bf, bp in zip(numbers, bars_f, bars_p):
            prime = is_prime(n)
            bf.set_alpha(scale if prime else 0.55)
            bp.set_alpha(scale if prime else 0.55)
        title.set_text(f"Dirichlet frequencies: prime bars highlighted · frame {frame + 1}/{frames}")
        return (*bars_f, *bars_p, title)

    animation = FuncAnimation(fig, update, frames=frames, interval=90, blit=True)
    animation.save(output, writer=PillowWriter(fps=11), dpi=110)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("artifacts/periodicity/prime_frequency_spectrum.gif"))
    parser.add_argument("--maximum", type=int, default=32)
    parser.add_argument("--frames", type=int, default=24)
    args = parser.parse_args()
    if args.maximum < 3 or args.frames < 2:
        raise SystemExit("maximum must be >= 3 and frames >= 2")
    build_animation(args.output, args.maximum, args.frames)
    print(args.output)


if __name__ == "__main__":
    main()
