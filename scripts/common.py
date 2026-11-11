"""Shared pieces for the profile SVGs — yappologistic's common.py, dark-only.

The look follows the CUI docs site: neutral greys, Geist at weight 500 with
tight tracking, words that blur in, pill controls, quiet bordered surfaces and
a dithered image behind the hero. The only colour comes from the avatar:
camellia red and gold, used sparingly.
"""
from __future__ import annotations

import base64
import io
from functools import lru_cache
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
OUT = ROOT / "assets"

THEMES = {
    "dark": {
        "bg": "#121212", "surface": "#181818", "muted": "#1f1f1f", "bezel": "#1c1c1c",
        "fg": "#f2f2f2", "text2": "#b4b4b4", "text3": "#8c8c8c",
        "border": "#2b2b2b", "subtle": "#222222", "strong": "#676767",
        "red": "#e0525b", "gold": "#e8c46a",
        "dots": ["#f2f2f2", "#b4b4b4", "#7a7a7a", "#4a4a4a"],
        "dot_red": ["#e0525b", "#9c2b34"], "dot_gold": "#e8c46a",
    },
}

FONT_FILES = {
    "display": "Geist-Medium.woff2",
    "sans": "Geist-Regular.woff2",
    "mono": "GeistMono-Regular.woff2",
}

# CUI: --ease: cubic-bezier(0.22, 1, 0.36, 1)
EASE = "cubic-bezier(.22,1,.36,1)"

BASE_CSS = f"""
.d{{font-family:'GDisplay',Geist,Inter,system-ui,sans-serif;font-weight:500;}}
.s{{font-family:'GSans',Geist,Inter,system-ui,sans-serif;}}
.m{{font-family:'GMono','Geist Mono',ui-monospace,monospace;}}
.rise{{animation:rise 720ms {EASE} both;}}
@keyframes rise{{0%{{opacity:0;transform:translateY(14px);}}}}
.word{{animation:word 900ms {EASE} both;}}
@keyframes word{{0%{{opacity:0;transform:translateY(.32em);filter:blur(10px);}}}}
.fadein{{animation:fadein 1100ms {EASE} both;}}
@keyframes fadein{{0%{{opacity:0;}}}}
.grow{{transform-box:fill-box;transform-origin:left;animation:grow 1200ms {EASE} both;}}
@keyframes grow{{0%{{transform:scaleX(0);}}}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important;}}}}
"""


@lru_cache(maxsize=None)
def _font(key: str) -> TTFont:
    return TTFont(FONTS / FONT_FILES[key])


def measure(key: str, text: str, size: float, tracking: float = 0.0) -> float:
    f = _font(key)
    cmap, hmtx, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    w = sum(hmtx[cmap.get(ord(ch), cmap[ord("?")])][0] for ch in text) * size / upm
    return w + tracking * len(text)


def wrap(key: str, text: str, size: float, width: float) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if measure(key, trial, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


FAMILY = {"display": "GDisplay", "sans": "GSans", "mono": "GMono"}


def font_faces(used: dict[str, str]) -> str:
    """@font-face rules, each font subset to only the characters used."""
    rules = []
    for key, text in used.items():
        if not text:
            continue
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga", "calt"]
        opts.name_IDs = []
        opts.notdef_outline = False
        font = TTFont(FONTS / FONT_FILES[key])
        sub = subset.Subsetter(options=opts)
        sub.populate(text="".join(sorted(set(text + " "))))
        sub.subset(font)
        buf = io.BytesIO()
        font.flavor = "woff2"
        font.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        rules.append(f"@font-face{{font-family:'{FAMILY[key]}';src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
    return "\n".join(rules)


def style(used: dict[str, str], extra: str = "") -> str:
    return f"<style>\n{font_faces(used)}\n{BASE_CSS}\n{extra}\n</style>"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def svg(w: float, h: float, label: str, body: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" '
            f'role="img" aria-label="{esc(label)}">\n{body}\n</svg>\n')


def words(text: str, x: float, y: float, size: float, fill: str, tracking: float,
          delay0: float = 0.0, step: float = 0.07, cls: str = "d") -> tuple[str, float]:
    """Each word as its own <text> so it can blur in on its own, like CUI's hero."""
    out, cx = [], x
    space = measure("display", " ", size) * 1.0
    for i, w in enumerate(text.split(" ")):
        out.append(f'<text x="{cx:.1f}" y="{y:.1f}" class="{cls} word" style="animation-delay:{delay0 + i * step:.2f}s" '
                   f'font-size="{size}" letter-spacing="{tracking:.2f}" fill="{fill}">{esc(w)}</text>')
        cx += measure("display", w, size, tracking) + space
    return "".join(out), cx


def write(name: str, content: str, out: Path = OUT) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / name).write_text(content, encoding="utf-8")
