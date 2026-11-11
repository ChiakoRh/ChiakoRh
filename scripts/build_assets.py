"""Builds the static profile SVGs: hero, buttons, section headings, toolbox, footer.

Adapted from yappologistic's build_assets.py with ChiakoRh content, dark only.
Run after editing: python scripts/build_assets.py   (needs fonttools, brotli, pillow)
The live cards (projects, stats) are built daily by scripts/generate-cards.py.
"""
from __future__ import annotations

from common import OUT, THEMES, esc, measure, style, svg, words, write
from dither import dither, radial, smoothstep

W = 880
AVATAR = OUT / ("avatar.jpg" if (OUT / "avatar.jpg").exists() else "avatar.jfif")


# ------------------------------------------------------------------------ hero

def hero(t: str) -> str:
    c = THEMES[t]
    H = 380
    x0 = 48
    badge = ["ChiakoRh", "open source"]
    l1, l2 = "Small tools for", "the terminal."
    lede = ["Developer · gamer.",
            "VPN tooling and dashboard frontends."]
    cmd = "gh repo list ChiakoRh --source"

    size, track = 46, -46 * 0.034
    w1, _ = words(l1, x0 - 2, 146, size, c["fg"], track, 0.15)
    w2, _ = words(l2, x0 - 2, 196, size, c["fg"], track, 0.15 + 3 * 0.07)

    # badge pill (CUI .hero-badge)
    b0 = measure("sans", badge[0], 12.5)
    bw = 25 + b0 + 18 + measure("sans", badge[1], 12.5) + 13
    badge_svg = (
        f'<g class="rise">'
        f'<rect x="{x0}" y="50" width="{bw:.1f}" height="28" rx="14" fill="{c["bg"]}" fill-opacity=".82" stroke="{c["border"]}"/>'
        f'<circle cx="{x0 + 14}" cy="64" r="3.2" fill="{c["red"]}"/>'
        f'<text x="{x0 + 25}" y="68.5" class="s" font-size="12.5" fill="{c["text2"]}">{esc(badge[0])}</text>'
        f'<circle cx="{x0 + 25 + b0 + 9:.1f}" cy="64" r="1.5" fill="{c["text2"]}" opacity=".6"/>'
        f'<text x="{x0 + 25 + b0 + 18:.1f}" y="68.5" class="s" font-size="12.5" fill="{c["text2"]}">{esc(badge[1])}</text>'
        f'</g>')

    lede_svg = "".join(
        f'<text x="{x0}" y="{240 + i * 23}" class="s rise" style="animation-delay:{0.36 + i * 0.06:.2f}s" '
        f'font-size="15.5" fill="{c["text2"]}">{esc(s)}</text>' for i, s in enumerate(lede))

    # command pill (CUI .hero-cmd) with a copy icon
    cw = 14 + measure("mono", "$ " + cmd, 12.5) + 12 + 30
    cy = 292
    ix = x0 + cw - 32
    cmd_svg = (
        f'<g class="rise" style="animation-delay:.5s">'
        f'<rect x="{x0}" y="{cy}" width="{cw:.1f}" height="36" rx="18" fill="{c["bg"]}" fill-opacity=".78" stroke="{c["border"]}"/>'
        f'<text x="{x0 + 14}" y="{cy + 22.5}" class="m" font-size="12.5" fill="{c["text3"]}">$ <tspan fill="{c["text2"]}">{esc(cmd)}</tspan></text>'
        f'<rect x="{ix + 4:.1f}" y="{cy + 14}" width="9" height="10" rx="2" fill="none" stroke="{c["text3"]}" stroke-width="1.2"/>'
        f'<path d="M{ix + 7:.1f} {cy + 12.5}v-.5a1.5 1.5 0 0 1 1.5-1.5h5.5a1.5 1.5 0 0 1 1.5 1.5v6a1.5 1.5 0 0 1-1.5 1.5h-.5" '
        f'fill="none" stroke="{c["text3"]}" stroke-width="1.2"/>'
        f'</g>')

    # dithered avatar, dissolving to the left like the CUI hero art
    ds = 420
    dx, dy = W - ds + 40, -20

    def weight(x, y):
        return smoothstep(dx + 10, dx + 190, x) * (1 - smoothstep(H - 40, H + 10, y) * 0.6)

    dots = dither(AVATAR, c, dx, dy, ds, 3, 2, weight)

    used = {"display": l1 + l2, "sans": "".join(badge) + "".join(lede), "mono": "$ " + cmd}
    body = f"""<defs>{style(used)}
<clipPath id="f"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#f)">
<rect width="{W}" height="{H}" fill="{c['bg']}"/>
<g class="fadein" style="animation-delay:.1s">{dots}</g>
{badge_svg}
{w1}{w2}
{lede_svg}
{cmd_svg}
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" fill="none" stroke="{c['border']}"/>"""
    return svg(W, H, f"{l1} {l2} {' '.join(lede)}", body)


# --------------------------------------------------------------------- buttons

ARROW = "M0 0h9M5 -4l4 4l-4 4"
PLANE = "M1 8.2L14 2l-3.8 12-2.9-4.3z"


def button(t: str, label: str, primary: bool, icon: str | None) -> str:
    c = THEMES[t]
    h, pad, fs = 40, 17, 14
    tw = measure("display", label, fs)
    w = pad * 2 + tw + (18 if icon else 0)
    bg = c["fg"] if primary else c["surface"]
    fg = c["bg"] if primary else c["fg"]
    stroke = c["fg"] if primary else c["border"]
    ic = ""
    if icon == "arrow":
        ic = (f'<path transform="translate({pad + tw + 9:.1f} {h / 2})" d="{ARROW}" fill="none" stroke="{fg}" '
              f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
    elif icon == "plane":
        ic = (f'<path transform="translate({pad + tw + 8:.1f} {h / 2 - 6})" d="{PLANE}" fill="none" stroke="{c["red"]}" '
              f'stroke-width="1.4" stroke-linejoin="round"/>')
    body = f"""<defs>{style({'display': label})}</defs>
<rect x=".5" y=".5" width="{w - 1:.1f}" height="{h - 1}" rx="10" fill="{bg}" stroke="{stroke}"/>
<text x="{pad}" y="{h / 2 + 5}" class="d" font-size="{fs}" fill="{fg}">{esc(label)}</text>{ic}"""
    return svg(round(w, 1), h, label, body)


# --------------------------------------------------------------------- headings

HEADINGS = [
    ("featured", "Featured projects", "The picks people actually use."),
    ("more", "More from the workshop", "Utilities, mods and experiments."),
    ("toolbox", "Toolbox", "What these are built with."),
    ("activity", "Activity", "Refreshed every day by a GitHub Action."),
]


def heading(t: str, title: str, lede: str) -> str:
    c = THEMES[t]
    H = 96
    size, track = 30, -30 * 0.03
    tw = measure("display", title, size, track)
    ws, _ = words(title, (W - tw) / 2, 46, size, c["fg"], track)
    body = f"""<defs>{style({'display': title, 'sans': lede})}</defs>
{ws}
<text x="{W / 2}" y="78" text-anchor="middle" class="s rise" style="animation-delay:.2s" font-size="15" fill="{c['text2']}">{esc(lede)}</text>"""
    return svg(W, H, f"{title}. {lede}", body)


# ---------------------------------------------------------------------- toolbox

TOOLBOX = [
    ["Python", "Go", "JavaScript", "HTML", "CSS3"],
    ["Git", "VS Code", "PowerShell", "Windows Terminal"],
    ["V2Ray · Xray", "Cloudflare Workers", "Minecraft", "Mindustry"],
]


def toolbox(t: str) -> str:
    c = THEMES[t]
    ph, gap, rg, fs = 34, 6, 10, 13.5
    H = len(TOOLBOX) * (ph + rg) - rg + 4
    out, n = [], 0
    for r, row in enumerate(TOOLBOX):
        widths = [measure("display", s, fs) + 30 for s in row]
        total = sum(widths) + gap * (len(row) - 1)
        x = (W - total) / 2
        y = 2 + r * (ph + rg)
        for s, pw in zip(row, widths):
            out.append(
                f'<g class="rise" style="animation-delay:{n * 0.03:.2f}s">'
                f'<rect x="{x:.1f}" y="{y}" width="{pw:.1f}" height="{ph}" rx="{ph / 2}" fill="{c["surface"]}" stroke="{c["border"]}"/>'
                f'<text x="{x + pw / 2:.1f}" y="{y + ph / 2 + 4.7:.1f}" text-anchor="middle" class="d" font-size="{fs}" '
                f'fill="{c["text2"]}">{esc(s)}</text></g>')
            x += pw + gap
            n += 1
    body = f"<defs>{style({'display': ''.join(''.join(r) for r in TOOLBOX)})}</defs>\n" + "".join(out)
    return svg(W, H, "Toolbox: " + ", ".join(s for r in TOOLBOX for s in r), body)


# ----------------------------------------------------------------------- footer

def footer(t: str) -> str:
    c = THEMES[t]
    H = 260
    title = "Thanks for stopping by."
    # the face from the avatar, dithered, behind the text (CUI .home-cta)
    ds = 320
    dx, dy = W / 2 - ds / 2, H / 2 - ds / 2 - 6
    dots = dither(AVATAR, c, dx, dy, ds, 3, 2, radial(W / 2, H / 2 - 6, 60, 150),
                  crop=(0.30, 0.16, 0.68, 0.54))
    size, track = 28, -28 * 0.03
    tw = measure("display", title, size, track)
    ws, _ = words(title, (W - tw) / 2, H / 2 + 4, size, c["fg"], track, 0.2)
    body = f"""<defs>{style({'display': title})}
<radialGradient id="clear"><stop offset=".3" stop-color="{c['bg']}" stop-opacity=".94"/><stop offset="1" stop-color="{c['bg']}" stop-opacity="0"/></radialGradient>
<clipPath id="f"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs>
<g clip-path="url(#f)">
<rect width="{W}" height="{H}" fill="{c['bg']}"/>
<g class="fadein" opacity=".62">{dots}</g>
<ellipse cx="{W / 2}" cy="{H / 2 - 6}" rx="240" ry="52" fill="url(#clear)"/>
{ws}
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" fill="none" stroke="{c['border']}"/>"""
    return svg(W, H, title, body)


def main() -> None:
    t = "dark"
    write("hero.svg", hero(t))
    write("btn-projects.svg", button(t, "Browse projects", True, "arrow"))
    write("btn-telegram.svg", button(t, "Telegram", False, "plane"))
    for slug, title, lede in HEADINGS:
        write(f"h-{slug}.svg", heading(t, title, lede))
    write("toolbox.svg", toolbox(t))
    write("footer.svg", footer(t))
    print("built static assets")


if __name__ == "__main__":
    main()
