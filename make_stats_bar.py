#!/usr/bin/env python3
"""Generate an animated stats/social bar SVG that goes between the
two main panels and the heatmap."""

import pathlib

SVG_W, SVG_H = 860, 56
BG = "#0d1117"
GREEN = "#39d353"
DIM = "#8b949e"
CYAN = "#58a6ff"
PURPLE = "#bc8cff"
BORDER = "#30363d"
FONT = "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace"

STATS = [
    ("🧬", "Drug Discovery", GREEN),
    ("🕶️", "Smart Glasses", CYAN),
    ("📚", "RAG Systems", PURPLE),
    ("🌍", "Darija NLP", "#e3b341"),
    ("🇲🇦", "Made in Morocco", "#ff6b6b"),
]


def build_svg():
    lines = []
    lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {SVG_W} {SVG_H}" width="{SVG_W}" height="{SVG_H}">'
    )
    lines.append("<style>")
    lines.append(f"""
        .bg {{ fill: {BG}; }}
        text {{ font-family: {FONT}; }}
        @keyframes fadeUp {{
            from {{ opacity: 0; transform: translateY(8px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes shimmer {{
            0%, 100% {{ opacity: 0.7; }}
            50% {{ opacity: 1; }}
        }}
    """)
    lines.append("</style>")

    lines.append(f'<rect class="bg" width="{SVG_W}" height="{SVG_H}" rx="6"/>')

    # Decorative top/bottom lines
    lines.append(f'<line x1="20" y1="1" x2="{SVG_W - 20}" y2="1" stroke="{BORDER}" stroke-width="0.5"/>')
    lines.append(f'<line x1="20" y1="{SVG_H - 1}" x2="{SVG_W - 20}" y2="{SVG_H - 1}" stroke="{BORDER}" stroke-width="0.5"/>')

    # Stats items evenly spaced
    n = len(STATS)
    spacing = SVG_W // n
    for i, (emoji, label, color) in enumerate(STATS):
        cx = spacing * i + spacing // 2
        delay = 0.1 * i
        lines.append(
            f'<g opacity="0" style="animation: fadeUp 0.4s ease {delay:.2f}s forwards, '
            f'shimmer 3s ease-in-out {delay + 0.5:.1f}s infinite;">'
        )
        lines.append(f'<text x="{cx}" y="24" text-anchor="middle" font-size="16">{emoji}</text>')
        lines.append(f'<text x="{cx}" y="42" text-anchor="middle" fill="{color}" '
                     f'font-size="10" opacity="0.85">{label}</text>')
        lines.append("</g>")

    lines.append("</svg>")
    return "\n".join(lines)


if __name__ == "__main__":
    out = pathlib.Path(__file__).resolve().parent.parent / "data" / "stats_bar.svg"
    out.write_text(build_svg())
    print(f"✓ Wrote {out}")
