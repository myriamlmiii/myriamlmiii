#!/usr/bin/env python3
"""Generate a stunning neofetch info card with animated skill bars,
glowing accents, and smooth reveal animations."""

import pathlib

SVG_W, SVG_H = 440, 460
BG = "#0d1117"
GREEN = "#39d353"
BRIGHT_GREEN = "#69f0a0"
DIM = "#8b949e"
CYAN = "#58a6ff"
PURPLE = "#bc8cff"
WHITE = "#e6edf3"
YELLOW = "#e3b341"
ORANGE = "#f0883e"
BORDER = "#30363d"
FONT = "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace"

INFO_LINES = [
    ("meriem", "@github", CYAN, GREEN),
    ("─" * 28, "", DIM, None),
    ("OS", "Morocco Linux 🇲🇦", CYAN, WHITE),
    ("Host", "Al Akhawayn University", CYAN, WHITE),
    ("Kernel", "CS + AI & Big Data", CYAN, WHITE),
    ("Shell", "Python / PyTorch / React", CYAN, WHITE),
    ("WM", "VS Code + Jupyter", CYAN, WHITE),
    ("Uptime", "4 years of CS", CYAN, WHITE),
    ("Theme", "Dark + Green Terminal", CYAN, WHITE),
]

SKILLS = [
    ("Python", 95, GREEN),
    ("ML / DL", 88, CYAN),
    ("NLP", 80, PURPLE),
    ("React", 70, ORANGE),
    ("Cloud", 65, YELLOW),
]

COLOR_BLOCKS = ["#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff",
                "#bc8cff", "#f0883e", "#e3b341", "#e6edf3"]


def build_svg():
    lines = []
    lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {SVG_W} {SVG_H}" width="{SVG_W}" height="{SVG_H}">'
    )

    lines.append("<defs>")
    lines.append("""
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="2" result="blur"/>
            <feComposite in="SourceGraphic" in2="blur" operator="over"/>
        </filter>
        <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#39d353;stop-opacity:0.6"/>
            <stop offset="50%" style="stop-color:#58a6ff;stop-opacity:0.6"/>
            <stop offset="100%" style="stop-color:#bc8cff;stop-opacity:0.6"/>
        </linearGradient>
    """)
    # Skill bar gradients
    for name, _, color in SKILLS:
        slug = name.replace(" ", "").replace("/", "")
        lines.append(f"""
        <linearGradient id="bar{slug}" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:{color};stop-opacity:1"/>
            <stop offset="100%" style="stop-color:{color};stop-opacity:0.4"/>
        </linearGradient>
        """)
    lines.append("</defs>")

    lines.append("<style>")
    lines.append(f"""
        .bg {{ fill: {BG}; }}
        text {{ font-family: {FONT}; font-size: 12.5px; }}
        .small {{ font-size: 10px; }}

        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateX(-12px); }}
            to   {{ opacity: 1; transform: translateX(0); }}
        }}
        @keyframes popIn {{
            from {{ opacity: 0; transform: scale(0); }}
            to   {{ opacity: 1; transform: scale(1); }}
        }}
        @keyframes fillBar {{
            from {{ width: 0; }}
        }}
        @keyframes glowPulse {{
            0%, 100% {{ filter: none; opacity: 0.9; }}
            50% {{ filter: url(#glow); opacity: 1; }}
        }}
    """)
    lines.append("</style>")

    # Background + border
    lines.append(f'<rect class="bg" width="{SVG_W}" height="{SVG_H}" rx="10"/>')
    lines.append(f'<rect width="{SVG_W}" height="{SVG_H}" rx="10" fill="none" '
                 f'stroke="url(#borderGrad)" stroke-width="1.5"/>')

    # Title bar
    for i, color in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        lines.append(f'<circle cx="{20 + i * 22}" cy="18" r="6" fill="{color}" opacity="0.9"/>')
    lines.append(f'<text x="{SVG_W // 2}" y="21" text-anchor="middle" fill="{DIM}" font-size="11" '
                 f'opacity="0.7">neofetch</text>')

    # Info lines
    y = 48
    for idx, (label, value, lcolor, vcolor) in enumerate(INFO_LINES):
        delay = 0.08 * idx + 0.3

        g = f'<g opacity="0" style="animation: slideIn 0.4s ease {delay:.2f}s forwards;">'
        lines.append(g)

        if not value:  # separator
            escaped = label.replace("&", "&amp;")
            lines.append(f'<text x="20" y="{y}" fill="{lcolor}" opacity="0.5">{escaped}</text>')
        elif "@" in value:  # username line
            lines.append(f'<text x="20" y="{y}" fill="{lcolor}" font-weight="bold" '
                         f'font-size="14">{label}</text>')
            lines.append(f'<text x="{20 + len(label) * 8.5}" y="{y}" fill="{vcolor}" '
                         f'font-size="14">{value}</text>')
        else:
            lines.append(f'<text x="20" y="{y}" fill="{lcolor}" font-weight="bold">{label}:</text>')
            x_val = 20 + (len(label) + 2) * 7.8
            lines.append(f'<text x="{x_val}" y="{y}" fill="{vcolor}">{value}</text>')

        lines.append("</g>")
        y += 20

    # Skills section header
    y += 8
    delay_base = 1.2
    lines.append(f'<g opacity="0" style="animation: slideIn 0.4s ease {delay_base}s forwards;">')
    lines.append(f'<text x="20" y="{y}" fill="{PURPLE}" font-weight="bold" font-size="13">Skills</text>')
    lines.append("</g>")
    y += 6

    # Animated skill bars
    bar_w = SVG_W - 120
    for i, (name, pct, color) in enumerate(SKILLS):
        y += 20
        delay = delay_base + 0.2 + i * 0.15
        slug = name.replace(" ", "").replace("/", "")

        # Label
        lines.append(f'<g opacity="0" style="animation: slideIn 0.3s ease {delay:.2f}s forwards;">')
        lines.append(f'<text x="20" y="{y}" fill="{DIM}" class="small">{name}</text>')

        # Bar background
        bx = 90
        lines.append(f'<rect x="{bx}" y="{y - 9}" width="{bar_w}" height="10" rx="5" '
                     f'fill="{BORDER}" opacity="0.5"/>')

        # Filled bar with animation
        fill_w = int(bar_w * pct / 100)
        lines.append(f'<rect x="{bx}" y="{y - 9}" height="10" rx="5" '
                     f'fill="url(#bar{slug})" width="{fill_w}" '
                     f'style="animation: fillBar 0.8s ease {delay + 0.2:.2f}s backwards;"/>')

        # Percentage
        lines.append(f'<text x="{bx + bar_w + 8}" y="{y}" fill="{color}" class="small" '
                     f'font-weight="bold">{pct}%</text>')
        lines.append("</g>")

    # Color blocks
    y += 30
    for i, color in enumerate(COLOR_BLOCKS):
        delay = 2.0 + i * 0.06
        lines.append(
            f'<rect x="{20 + i * 30}" y="{y}" width="24" height="24" rx="4" fill="{color}" '
            f'opacity="0" style="animation: popIn 0.3s cubic-bezier(0.34,1.56,0.64,1) {delay:.2f}s forwards, '
            f'glowPulse 2s ease-in-out {delay + 0.3:.2f}s infinite;"/>'
        )

    lines.append("</svg>")
    return "\n".join(lines)


if __name__ == "__main__":
    out = pathlib.Path(__file__).resolve().parent.parent / "data" / "info_card.svg"
    out.write_text(build_svg())
    print(f"✓ Wrote {out}")
