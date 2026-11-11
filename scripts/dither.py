"""Ordered (Bayer) dithering of the avatar into square dots, like the CUI hero."""
from __future__ import annotations

import colorsys
import math
from typing import Callable

from PIL import Image, ImageEnhance

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def dither(img_path, theme: dict, x0: float, y0: float, size: float, cell: float,
           dot: float, weight: Callable[[float, float], float],
           crop: tuple[float, float, float, float] | None = None) -> str:
    img = Image.open(img_path).convert("RGB")
    if crop:
        w, h = img.size
        img = img.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    img = ImageEnhance.Contrast(img).enhance(1.25)
    n = int(size / cell)
    small = img.resize((n, n), Image.LANCZOS)
    px = small.load()

    groups: dict[str, list[str]] = {}
    for j in range(n):
        for i in range(n):
            r, g, b = (v / 255 for v in px[i, j])
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
            x, y = x0 + i * cell, y0 + j * cell
            wgt = weight(x + cell / 2, y + cell / 2)
            if wgt <= 0:
                continue
            is_red = s > 0.42 and v > 0.28 and (h < 0.05 or h > 0.93)
            is_gold = s > 0.38 and v > 0.45 and 0.07 < h < 0.18
            if is_red:
                density = min(1.0, 0.55 + v * 0.8)
                color = theme["dot_red"][0] if v > 0.38 else theme["dot_red"][1]
            elif is_gold:
                density = 0.95
                color = theme["dot_gold"]
            else:
                density = max(0.0, min(1.0, (lum - 0.06) / 0.78)) ** 0.95
                dots = theme["dots"]
                color = dots[0] if lum > 0.72 else dots[1] if lum > 0.5 else dots[2] if lum > 0.3 else dots[3]
            density *= wgt
            if density > (BAYER[j % 4][i % 4] + 0.5) / 16:
                groups.setdefault(color, []).append((round(x, 1), round(y, 1)))
    out = []
    for color, pts in groups.items():
        d, px_, py_ = [], None, None
        for x, y in pts:
            if px_ is None:
                d.append(f"M{x:g} {y:g}")
            else:
                d.append(f"m{x - px_:g} {y - py_:g}")
            d.append(f"h{dot:g}v{dot:g}h-{dot:g}z")
            px_, py_ = x, y
        out.append(f'<path fill="{color}" d="{"".join(d)}"/>')
    return "".join(out)


def smoothstep(a: float, b: float, x: float) -> float:
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


def radial(cx: float, cy: float, r0: float, r1: float) -> Callable[[float, float], float]:
    return lambda x, y: 1 - smoothstep(r0, r1, math.hypot(x - cx, y - cy))
