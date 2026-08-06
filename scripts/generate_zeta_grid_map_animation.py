#!/usr/bin/env python3
"""
Animated high-resolution complex-grid map under the analytically continued
Riemann zeta function.

Unlike a finite term-orbit diagram, this program maps horizontal and vertical
lines from the complex s-plane through

    w = zeta(s)

and animates luminous highlight bands along the mapped curves.

Dependencies
------------
    pip install numpy matplotlib mpmath pillow

Example
-------
    python generate_zeta_grid_map_animation.py \
        --output zeta_grid_map.gif \
        --width 1600 \
        --height 900 \
        --frames 96 \
        --fps 24 \
        --samples 520 \
        --sigma-lines 39 \
        --t-lines 37

For a faster test render:
    python generate_zeta_grid_map_animation.py \
        --output preview.gif \
        --width 960 \
        --height 540 \
        --frames 36 \
        --fps 18 \
        --samples 240 \
        --sigma-lines 23 \
        --t-lines 21 \
        --precision 20
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np
from matplotlib import patheffects
from matplotlib.animation import FuncAnimation, PillowWriter


BACKGROUND = "#01060b"
GRID_MAJOR = "#17485e"
GRID_MINOR = "#0c2b39"
AXIS_COLOR = "#a7b6c4"
TEXT_COLOR = "#f7f8fb"


@dataclass
class CurveSegment:
    values: np.ndarray
    color: tuple[float, float, float]
    width: float
    alpha: float
    phase: float
    family: str


@dataclass
class Geometry:
    segments: list[CurveSegment]
    xlim: tuple[float, float]
    ylim: tuple[float, float]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Animate an s-plane grid mapped by the Riemann zeta function."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/visualizations/zeta_grid_map.gif"),
    )
    parser.add_argument("--width", type=int, default=1600)
    parser.add_argument("--height", type=int, default=900)
    parser.add_argument("--dpi", type=int, default=120)
    parser.add_argument("--frames", type=int, default=96)
    parser.add_argument("--fps", type=int, default=24)

    # Source s-plane domain.
    parser.add_argument("--sigma-min", type=float, default=-6.2)
    parser.add_argument("--sigma-max", type=float, default=6.2)
    parser.add_argument("--t-min", type=float, default=-3.4)
    parser.add_argument("--t-max", type=float, default=3.4)
    parser.add_argument("--sigma-lines", type=int, default=45)
    parser.add_argument("--t-lines", type=int, default=41)
    parser.add_argument("--samples", type=int, default=460)

    # Output w-plane viewport. 14.4 / 8.1 = 16 / 9.
    parser.add_argument("--x-min", type=float, default=-7.2)
    parser.add_argument("--x-max", type=float, default=7.2)
    parser.add_argument("--y-min", type=float, default=-4.05)
    parser.add_argument("--y-max", type=float, default=4.05)

    parser.add_argument("--precision", type=int, default=24)
    parser.add_argument("--line-width", type=float, default=0.74)
    parser.add_argument("--glow-width", type=float, default=2.7)
    parser.add_argument("--highlight-count", type=int, default=28)
    parser.add_argument("--highlight-length", type=float, default=0.12)
    parser.add_argument("--title", default="Riemann zeta function")

    # Optional geometry cache. The cache is invalidated automatically when the
    # source domain, density or viewport changes.
    parser.add_argument(
        "--cache",
        type=Path,
        default=Path("artifacts/visualizations/zeta_grid_geometry_cache.npz"),
    )
    parser.add_argument("--no-cache", action="store_true")
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if args.width <= 0 or args.height <= 0 or args.dpi <= 0:
        raise SystemExit("width, height and dpi must be positive")
    if args.frames < 2 or args.fps <= 0:
        raise SystemExit("frames must be >= 2 and fps must be positive")
    if args.samples < 120:
        raise SystemExit("samples must be >= 120")
    if args.sigma_lines < 3 or args.t_lines < 3:
        raise SystemExit("sigma-lines and t-lines must be >= 3")
    if args.precision < 15:
        raise SystemExit("precision must be >= 15")
    image_ratio = args.width / args.height
    viewport_ratio = (args.x_max - args.x_min) / (args.y_max - args.y_min)
    if abs(image_ratio - viewport_ratio) > 1e-9:
        raise SystemExit(
            "The w-plane viewport must have the same aspect ratio as the image. "
            f"image={image_ratio:.9f}, viewport={viewport_ratio:.9f}"
        )


def zeta_complex(sigma: float, t: float) -> complex:
    """Evaluate the analytically continued zeta function away from its pole."""
    if abs(sigma - 1.0) < 1e-11 and abs(t) < 1e-11:
        return complex(np.nan, np.nan)
    try:
        value = mp.zeta(mp.mpc(sigma, t))
        return complex(float(mp.re(value)), float(mp.im(value)))
    except (ValueError, ZeroDivisionError, OverflowError):
        return complex(np.nan, np.nan)


def map_curve(sigmas: Iterable[float], ts: Iterable[float]) -> np.ndarray:
    return np.asarray(
        [
            zeta_complex(float(sigma), float(t))
            for sigma, t in zip(sigmas, ts)
        ],
        dtype=np.complex128,
    )


def split_curve(
    curve: np.ndarray,
    *,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
) -> list[np.ndarray]:
    """
    Split at the pole, non-finite samples, far excursions and large jumps.

    Without this step, plotting software joins disconnected branches by long
    straight chords across the entire image.
    """
    xmin, xmax = xlim
    ymin, ymax = ylim
    xspan = xmax - xmin
    yspan = ymax - ymin

    finite = np.isfinite(curve.real) & np.isfinite(curve.imag)
    bounded = (
        (curve.real > xmin - 0.30 * xspan)
        & (curve.real < xmax + 0.30 * xspan)
        & (curve.imag > ymin - 0.30 * yspan)
        & (curve.imag < ymax + 0.30 * yspan)
    )
    valid = finite & bounded

    if len(curve) > 1:
        dx = np.diff(curve.real) / xspan
        dy = np.diff(curve.imag) / yspan
        jump = np.zeros(len(curve), dtype=bool)
        jump[1:] = np.hypot(dx, dy) > 0.08
        valid &= ~jump

    segments: list[np.ndarray] = []
    start: int | None = None

    for index, is_valid in enumerate(valid):
        if is_valid and start is None:
            start = index
        elif not is_valid and start is not None:
            if index - start >= 3:
                segments.append(curve[start:index])
            start = None

    if start is not None and len(curve) - start >= 3:
        segments.append(curve[start:])

    return segments


def hex_rgb(value: str) -> np.ndarray:
    value = value.lstrip("#")
    return np.array(
        [int(value[index : index + 2], 16) for index in (0, 2, 4)],
        dtype=float,
    ) / 255.0


def blend(
    first: str,
    second: str,
    amount: float,
) -> tuple[float, float, float]:
    mixed = (1.0 - amount) * hex_rgb(first) + amount * hex_rgb(second)
    return tuple(float(component) for component in mixed)


def cache_signature(args: argparse.Namespace) -> str:
    data = {
        "sigma_min": args.sigma_min,
        "sigma_max": args.sigma_max,
        "t_min": args.t_min,
        "t_max": args.t_max,
        "sigma_lines": args.sigma_lines,
        "t_lines": args.t_lines,
        "samples": args.samples,
        "x_min": args.x_min,
        "x_max": args.x_max,
        "y_min": args.y_min,
        "y_max": args.y_max,
        "precision": args.precision,
    }
    return json.dumps(data, sort_keys=True)


def save_geometry_cache(
    path: Path,
    geometry: Geometry,
    signature: str,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    arrays: dict[str, np.ndarray] = {
        "signature": np.asarray([signature]),
        "count": np.asarray([len(geometry.segments)], dtype=int),
        "xlim": np.asarray(geometry.xlim, dtype=float),
        "ylim": np.asarray(geometry.ylim, dtype=float),
    }

    for index, segment in enumerate(geometry.segments):
        arrays[f"values_{index}"] = segment.values
        arrays[f"color_{index}"] = np.asarray(segment.color, dtype=float)
        arrays[f"meta_{index}"] = np.asarray(
            [segment.width, segment.alpha, segment.phase],
            dtype=float,
        )
        arrays[f"family_{index}"] = np.asarray([segment.family])

    np.savez_compressed(path, **arrays)


def load_geometry_cache(
    path: Path,
    signature: str,
) -> Geometry | None:
    if not path.exists():
        return None

    try:
        with np.load(path, allow_pickle=False) as data:
            stored_signature = str(data["signature"][0])
            if stored_signature != signature:
                return None

            count = int(data["count"][0])
            xlim = tuple(float(v) for v in data["xlim"])
            ylim = tuple(float(v) for v in data["ylim"])
            segments: list[CurveSegment] = []

            for index in range(count):
                values = np.asarray(data[f"values_{index}"], dtype=np.complex128)
                color = tuple(float(v) for v in data[f"color_{index}"])
                width, alpha, phase = (
                    float(v) for v in data[f"meta_{index}"]
                )
                family = str(data[f"family_{index}"][0])
                segments.append(
                    CurveSegment(
                        values=values,
                        color=color,
                        width=width,
                        alpha=alpha,
                        phase=phase,
                        family=family,
                    )
                )

            return Geometry(segments=segments, xlim=xlim, ylim=ylim)
    except (OSError, KeyError, ValueError):
        return None


def build_geometry(args: argparse.Namespace) -> Geometry:
    xlim = (args.x_min, args.x_max)
    ylim = (args.y_min, args.y_max)
    segments: list[CurveSegment] = []

    sigma_samples = np.linspace(
        args.sigma_min,
        args.sigma_max,
        args.samples,
    )
    t_values = np.linspace(args.t_min, args.t_max, args.t_lines)

    print(f"Computing {len(t_values)} horizontal source-grid curves...")
    for index, t_value in enumerate(t_values):
        curve = map_curve(
            sigma_samples,
            np.full_like(sigma_samples, t_value),
        )
        normalized = index / max(1, len(t_values) - 1)

        if t_value < -1e-12:
            color = blend("#97cad1", "#aaa4f5", normalized)
        elif t_value > 1e-12:
            color = blend("#eff05c", "#f3a0b7", normalized)
        else:
            color = (0.98, 0.93, 0.36)

        major = abs(t_value - round(t_value)) < 0.04
        for segment_index, values in enumerate(
            split_curve(curve, xlim=xlim, ylim=ylim)
        ):
            segments.append(
                CurveSegment(
                    values=values,
                    color=color,
                    width=args.line_width * (1.35 if major else 0.82),
                    alpha=0.86 if major else 0.48,
                    phase=2.0 * math.pi * (
                        normalized + 0.071 * segment_index
                    ),
                    family="horizontal",
                )
            )

    t_samples = np.linspace(args.t_min, args.t_max, args.samples)
    sigma_values = np.linspace(
        args.sigma_min,
        args.sigma_max,
        args.sigma_lines,
    )

    print(f"Computing {len(sigma_values)} vertical source-grid curves...")
    for index, sigma_value in enumerate(sigma_values):
        curve = map_curve(
            np.full_like(t_samples, sigma_value),
            t_samples,
        )
        normalized = index / max(1, len(sigma_values) - 1)
        color = blend("#9ed8d1", "#a49cf0", normalized)
        major = abs(sigma_value - round(sigma_value)) < 0.04

        for segment_index, values in enumerate(
            split_curve(curve, xlim=xlim, ylim=ylim)
        ):
            segments.append(
                CurveSegment(
                    values=values,
                    color=color,
                    width=args.line_width * (1.25 if major else 0.76),
                    alpha=0.70 if major else 0.38,
                    phase=2.0 * math.pi * (
                        normalized + 0.093 * segment_index + 0.25
                    ),
                    family="vertical",
                )
            )

    return Geometry(segments=segments, xlim=xlim, ylim=ylim)


def configure_axes(
    fig: plt.Figure,
    ax: plt.Axes,
    args: argparse.Namespace,
) -> None:
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)
    ax.set_xlim(args.x_min, args.x_max)
    ax.set_ylim(args.y_min, args.y_max)
    ax.set_aspect("equal", adjustable="box")

    major_x = np.arange(
        math.ceil(args.x_min),
        math.floor(args.x_max) + 1,
        1,
    )
    major_y = np.arange(
        math.ceil(args.y_min),
        math.floor(args.y_max) + 1,
        1,
    )
    minor_x = np.arange(
        math.ceil(args.x_min * 2) / 2,
        args.x_max + 0.25,
        0.5,
    )
    minor_y = np.arange(
        math.ceil(args.y_min * 2) / 2,
        args.y_max + 0.25,
        0.5,
    )

    ax.set_xticks(major_x)
    ax.set_yticks(major_y)
    ax.set_xticks(minor_x, minor=True)
    ax.set_yticks(minor_y, minor=True)

    ax.grid(
        which="minor",
        color=GRID_MINOR,
        linewidth=0.50,
        alpha=0.70,
    )
    ax.grid(
        which="major",
        color=GRID_MAJOR,
        linewidth=1.05,
        alpha=0.90,
    )
    ax.axhline(
        0,
        color=AXIS_COLOR,
        linewidth=1.15,
        alpha=0.92,
        zorder=8,
    )
    ax.axvline(
        0,
        color=AXIS_COLOR,
        linewidth=1.15,
        alpha=0.92,
        zorder=8,
    )

    tick_scale = args.width / 1600
    ax.tick_params(
        which="both",
        colors="#edf3f8",
        labelsize=10.5 * tick_scale,
        length=0,
        pad=7,
    )

    labels = []
    for value in major_y:
        rounded = int(round(value))
        if rounded == 0:
            labels.append("0")
        elif rounded == 1:
            labels.append(r"$i$")
        elif rounded == -1:
            labels.append(r"$-i$")
        else:
            labels.append(rf"${rounded}i$")
    ax.set_yticklabels(labels)

    for spine in ax.spines.values():
        spine.set_visible(False)


def longest_segments(
    geometry: Geometry,
    count: int,
) -> list[CurveSegment]:
    candidates = [
        segment
        for segment in geometry.segments
        if len(segment.values) >= 12
    ]
    candidates.sort(key=lambda segment: len(segment.values), reverse=True)

    if len(candidates) <= count:
        return candidates

    # Spread selections through the sorted list so the highlights are not all
    # concentrated in only one geometric region.
    indices = np.linspace(0, len(candidates) - 1, count, dtype=int)
    return [candidates[int(index)] for index in indices]


def main() -> None:
    args = parse_args()
    validate_args(args)
    mp.mp.dps = args.precision

    signature = cache_signature(args)
    geometry = None

    if not args.no_cache:
        geometry = load_geometry_cache(args.cache, signature)
        if geometry is not None:
            print(f"Loaded geometry cache: {args.cache}")

    if geometry is None:
        geometry = build_geometry(args)
        if not args.no_cache:
            save_geometry_cache(args.cache, geometry, signature)
            print(f"Saved geometry cache: {args.cache}")

    figsize = (args.width / args.dpi, args.height / args.dpi)
    fig = plt.figure(figsize=figsize, dpi=args.dpi, facecolor=BACKGROUND)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], facecolor=BACKGROUND)
    configure_axes(fig, ax, args)

    base_artists = []
    for segment in geometry.segments:
        glow, = ax.plot(
            segment.values.real,
            segment.values.imag,
            color=segment.color,
            linewidth=args.glow_width * segment.width,
            alpha=0.050,
            antialiased=True,
            solid_capstyle="round",
            solid_joinstyle="round",
            zorder=3.0 if segment.family == "vertical" else 4.0,
        )
        line, = ax.plot(
            segment.values.real,
            segment.values.imag,
            color=segment.color,
            linewidth=segment.width,
            alpha=segment.alpha,
            antialiased=True,
            solid_capstyle="round",
            solid_joinstyle="round",
            zorder=3.1 if segment.family == "vertical" else 4.1,
        )
        base_artists.append((segment, glow, line))

    selected = longest_segments(geometry, args.highlight_count)
    highlights = []
    particles = []

    for index, segment in enumerate(selected):
        highlight, = ax.plot(
            [],
            [],
            color=(1.0, 1.0, 1.0),
            linewidth=max(1.25, segment.width * 2.15),
            alpha=0.82,
            solid_capstyle="round",
            solid_joinstyle="round",
            zorder=12,
        )
        particle, = ax.plot(
            [],
            [],
            marker="o",
            linestyle="None",
            color=segment.color,
            markeredgecolor="white",
            markeredgewidth=0.45,
            markersize=3.6 + 0.18 * (index % 5),
            alpha=0.95,
            zorder=13,
        )
        highlights.append((segment, highlight, index))
        particles.append((segment, particle, index))

    title_scale = args.width / 1600
    title = ax.text(
        0.016,
        0.968,
        args.title,
        transform=ax.transAxes,
        va="top",
        ha="left",
        color=TEXT_COLOR,
        fontsize=35 * title_scale,
        family="serif",
        zorder=20,
    )
    title.set_path_effects(
        [
            patheffects.withStroke(
                linewidth=3.0,
                foreground=BACKGROUND,
                alpha=0.96,
            )
        ]
    )

    formula = ax.text(
        0.105,
        0.855,
        r"$\zeta(s)=\sum_{n=1}^{\infty}\frac{1}{n^s}$",
        transform=ax.transAxes,
        va="top",
        ha="left",
        color=TEXT_COLOR,
        fontsize=31 * title_scale,
        family="serif",
        zorder=20,
    )
    formula.set_path_effects(
        [
            patheffects.withStroke(
                linewidth=3.0,
                foreground=BACKGROUND,
                alpha=0.96,
            )
        ]
    )

    subtitle = ax.text(
        0.984,
        0.024,
        "complex s-plane grid mapped by the analytically continued ζ(s)",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        color="#cbd5df",
        fontsize=8.5 * title_scale,
        alpha=0.84,
        zorder=20,
    )

    progress_text = ax.text(
        0.018,
        0.024,
        "",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        color="#d7e6ef",
        fontsize=8.5 * title_scale,
        alpha=0.84,
        zorder=20,
    )

    highlight_fraction = max(
        0.025,
        min(0.30, float(args.highlight_length)),
    )

    def update(frame_index: int):
        phase = frame_index / args.frames
        theta = 2.0 * math.pi * phase

        # A restrained breathing effect keeps the full geometry alive without
        # redrawing the expensive zeta map.
        for index, (segment, glow, line) in enumerate(base_artists):
            pulse = 0.5 + 0.5 * math.sin(
                theta + segment.phase + 0.13 * index
            )
            glow.set_alpha(0.028 + 0.055 * pulse)
            line.set_alpha(
                max(0.12, min(0.96, segment.alpha * (0.83 + 0.23 * pulse)))
            )

        for segment, highlight, index in highlights:
            values = segment.values
            length = len(values)
            center = (
                phase * (1.0 + 0.035 * index)
                + index / max(1, len(highlights))
            ) % 1.0
            half_window = max(2, int(0.5 * highlight_fraction * length))
            center_index = int(center * (length - 1))
            start = max(0, center_index - half_window)
            stop = min(length, center_index + half_window + 1)
            local = values[start:stop]

            if len(local) >= 2:
                highlight.set_data(local.real, local.imag)
                highlight.set_color(segment.color)
                highlight.set_alpha(
                    0.46 + 0.45 * (
                        0.5 + 0.5 * math.sin(theta * 2.0 + index)
                    )
                )
            else:
                highlight.set_data([], [])

        for segment, particle, index in particles:
            values = segment.values
            position = (
                phase * (1.0 + 0.041 * index)
                + 0.173 * index
            ) % 1.0
            point_index = min(
                len(values) - 1,
                int(position * len(values)),
            )
            value = values[point_index]
            particle.set_data([value.real], [value.imag])
            particle.set_alpha(
                0.58 + 0.40 * (
                    0.5 + 0.5 * math.sin(theta * 3.0 + 0.7 * index)
                )
            )

        progress_text.set_text(
            "ζ-grid flow  ·  "
            f"frame {frame_index + 1}/{args.frames}  ·  "
            f"{args.sigma_lines + args.t_lines} source-grid lines"
        )

        return [
            *(artist for _, glow, line in base_artists for artist in (glow, line)),
            *(highlight for _, highlight, _ in highlights),
            *(particle for _, particle, _ in particles),
            title,
            formula,
            subtitle,
            progress_text,
        ]

    animation = FuncAnimation(
        fig,
        update,
        frames=args.frames,
        interval=1000 / args.fps,
        blit=False,
        repeat=True,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    animation.save(
        args.output,
        writer=PillowWriter(fps=args.fps),
        dpi=args.dpi,
        savefig_kwargs={
            "facecolor": BACKGROUND,
            "edgecolor": "none",
        },
    )
    plt.close(fig)
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
