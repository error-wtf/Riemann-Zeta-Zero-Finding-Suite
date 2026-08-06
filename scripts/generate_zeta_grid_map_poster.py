#!/usr/bin/env python3
"""Render the complete analytic-continuation grid z -> zeta(z).

Unlike the finite Dirichlet-term animation, this maps a rectangular grid in
the s-plane through mpmath's analytically continued zeta function.  Curves
are split at the pole and at screen-space jumps, so no false chords are
drawn across the singularity.  The same renderer produces the poster and
the reference-style animated GIF.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patheffects
import mpmath as mp
import numpy as np
from PIL import Image

BG = "#01060b"
MAJOR = "#17485e"
MINOR = "#0c2b39"
AXIS = "#a7b6c4"
WHITE = "#f7f8fb"


def zeta(sigma: float, height: float) -> complex:
    if abs(sigma - 1.0) < 1e-10 and abs(height) < 1e-10:
        return complex(np.nan, np.nan)
    try:
        z = mp.zeta(mp.mpc(sigma, height))
        return complex(float(mp.re(z)), float(mp.im(z)))
    except (ValueError, ZeroDivisionError, OverflowError):
        return complex(np.nan, np.nan)


def split_curve(curve: np.ndarray, xlim: tuple[float, float], ylim: tuple[float, float]):
    xmin, xmax = xlim; ymin, ymax = ylim
    xspan = xmax - xmin; yspan = ymax - ymin
    good = np.isfinite(curve.real) & np.isfinite(curve.imag)
    good &= (curve.real > xmin - .35*xspan) & (curve.real < xmax + .35*xspan)
    good &= (curve.imag > ymin - .35*yspan) & (curve.imag < ymax + .35*yspan)
    if len(curve) > 1:
        jump = np.zeros(len(curve), dtype=bool)
        # Only sever the pole/true singular excursions.  A generous screen
        # jump threshold preserves the long, smooth arcs of the reference
        # map instead of turning them into a collection of short dashes.
        jump[1:] = np.hypot(np.diff(curve.real)/xspan, np.diff(curve.imag)/yspan) > .38
        good &= ~jump
    out = []; start = None
    for i, ok in enumerate(good):
        if ok and start is None: start = i
        if (not ok or i == len(good)-1) and start is not None:
            end = i + 1 if ok and i == len(good)-1 else i
            if end - start >= 3: out.append(curve[start:end])
            start = None
    return out


def blend(a: str, b: str, amount: float):
    def rgb(v):
        v = v.lstrip('#'); return np.array([int(v[i:i+2], 16) for i in (0, 2, 4)]) / 255
    return tuple((1-amount)*rgb(a) + amount*rgb(b))


def draw(ax, seg, color, width, alpha, zorder):
    ax.plot(seg.real, seg.imag, color=color, linewidth=width*3.0, alpha=.075,
            solid_capstyle="round", solid_joinstyle="round", zorder=zorder)
    ax.plot(seg.real, seg.imag, color=color, linewidth=width, alpha=alpha,
            solid_capstyle="round", solid_joinstyle="round", zorder=zorder+.1)


def render(output: Path, width=1920, height=1080, dpi=120, samples=360,
           sigma_min=-5.5, sigma_max=5.5, t_min=-3.5, t_max=3.5,
           sigma_lines=65, t_lines=61, precision=24, highlight=0.0):
    mp.mp.dps = precision
    fig = plt.figure(figsize=(width/dpi, height/dpi), dpi=dpi, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=BG)
    xlim=(-7.2, 7.2); ylim=(-4.05, 4.05)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal", adjustable="box")
    major_x=np.arange(-7,8,1); major_y=np.arange(-4,5,1)
    minor_x=np.arange(-7,7.51,.5); minor_y=np.arange(-4,4.51,.5)
    ax.set_xticks(major_x); ax.set_yticks(major_y)
    ax.set_xticks(minor_x, minor=True); ax.set_yticks(minor_y, minor=True)
    ax.grid(which="minor", color=MINOR, linewidth=.55, alpha=.68)
    ax.grid(which="major", color=MAJOR, linewidth=1.15, alpha=.88)
    ax.axhline(0, color=AXIS, linewidth=1.15, alpha=.9, zorder=8)
    ax.axvline(0, color=AXIS, linewidth=1.15, alpha=.9, zorder=8)
    ax.tick_params(which="both", colors="#e7edf4", labelsize=11, length=0, pad=7)
    ax.set_yticklabels(["0" if v==0 else (r"$i$" if v==1 else (r"$-i$" if v==-1 else rf"${int(v)}i$")) for v in major_y])
    for spine in ax.spines.values(): spine.set_visible(False)
    sig=np.linspace(sigma_min, sigma_max, samples)
    for idx, tv in enumerate(np.linspace(t_min, t_max, t_lines)):
        curve=np.asarray([zeta(float(s), float(tv)) for s in sig])
        frac=idx/max(1,t_lines-1); color=blend("#91b8ff","#b8b4ff",frac) if tv<0 else (blend("#f0df5a","#f3a5bb",frac) if tv>0 else (0.96,.94,.55))
        major=abs(tv-round(tv)) < .04
        for seg in split_curve(curve,xlim,ylim): draw(ax,seg,color,1.35 if major else .86,.86 if major else .56,4)
    heights=np.linspace(t_min,t_max,samples)
    for idx, sv in enumerate(np.linspace(sigma_min,sigma_max,sigma_lines)):
        curve=np.asarray([zeta(float(sv),float(t)) for t in heights])
        frac=idx/max(1,sigma_lines-1); color=blend("#9cd7d1","#aba5f5",frac)
        major=abs(sv-round(sv)) < .04
        for seg in split_curve(curve,xlim,ylim): draw(ax,seg,color,1.25 if major else .80,.72 if major else .43,3)
    # Animated marker: a source-plane horizontal line and its image point.
    image=zeta(0.0, highlight)
    if np.isfinite(image.real) and xlim[0] < image.real < xlim[1] and ylim[0] < image.imag < ylim[1]:
        ax.scatter([image.real],[image.imag],s=34,color="#ffd84d",edgecolors="#fff3a0",linewidths=.8,zorder=14)
        ax.annotate(rf"$\zeta({highlight:.2f}i)$",(image.real,image.imag),xytext=(9,9),textcoords="offset points",color=WHITE,fontsize=10,zorder=15)
    title=ax.text(.016,.968,"Riemann zeta function",transform=ax.transAxes,va="top",color=WHITE,fontsize=40,family="serif",zorder=20)
    title.set_path_effects([patheffects.withStroke(linewidth=3,foreground=BG,alpha=.92)])
    formula=ax.text(.105,.855,r"$\zeta(s)=\sum_{n=1}^{\infty}\frac{1}{n^s}$",transform=ax.transAxes,va="top",color=WHITE,fontsize=34,family="serif",zorder=20)
    formula.set_path_effects([patheffects.withStroke(linewidth=3,foreground=BG,alpha=.92)])
    ax.text(.982,.025,"analytic continuation: images of an s-plane grid under ζ(s)",transform=ax.transAxes,ha="right",va="bottom",color="#cbd5df",fontsize=9,alpha=.86,zorder=20)
    output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output,dpi=dpi,facecolor=fig.get_facecolor(),edgecolor="none",bbox_inches=None,pad_inches=0)
    plt.close(fig)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,default=Path("artifacts/periodicity/zeta_grid_map_poster.png"))
    p.add_argument("--width",type=int,default=1920); p.add_argument("--height",type=int,default=1080); p.add_argument("--dpi",type=int,default=120)
    p.add_argument("--samples",type=int,default=360); p.add_argument("--precision",type=int,default=24); p.add_argument("--highlight",type=float,default=0.0)
    a=p.parse_args(); render(a.output,a.width,a.height,a.dpi,a.samples,precision=a.precision,highlight=a.highlight); print(a.output)


if __name__ == "__main__": main()
