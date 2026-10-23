#!/usr/bin/env python3
"""Generate a stunning animated ASCII terminal SVG with typing effect,
scan lines, glowing cursor, and shimmer animations."""

import pathlib

SVG_W, SVG_H = 420, 460
BG = "#0d1117"
GREEN = "#39d353"
BRIGHT_GREEN = "#69f0a0"
DIM = "#8b949e"
CYAN = "#58a6ff"
PURPLE = "#bc8cff"
BORDER = "#30363d"
FONT = "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace"

ASCII_ART = [
    "  ███╗   ███╗",
    "  ████╗ ████║",
    "  ██╔████╔██║  ╔══════════════════╗",
    "  ██║╚██╔╝██║  ║  M E R I E M     ║",
    "  ██║ ╚═╝ ██║  ╚══════════════════╝",
    "  ╚═╝     ╚═╝",
]

TERMINAL_LINES = [
    # (text, color, is_command, delay_start)
    ("┌─ meriem@github ─────────────────┐", BORDER, False, 0),
    ("│", BORDER, False, 0),
    ("│  $ whoami", GREEN, True, 0.4),
    ("│  ► Meriem Lmoubariki", CYAN, False, 0.9),
    ("│  ► AI / ML Researcher", PURPLE, False, 1.1),
    ("│  ► CS Senior @ AUI  🇲🇦", DIM, False, 1.3),
    ("│", BORDER, False, 0),
    ("│  $ cat research.log", GREEN, True, 1.8),
    ("│  ╠═ Drug Discovery ML Pipeline", DIM, False, 2.2),
    ("│  ╠═ AI Smart Glasses (CV+NLP)", DIM, False, 2.4),
    ("│  ╠═ RAG Calculus Assistant", DIM, False, 2.6),
    ("│  ╚═ NLP for Darija", DIM, False, 2.8),
    ("│", BORDER, False, 0),
    ("│  $ echo $MOTTO", GREEN, True, 3.2),
    ('│  "First-gen from SE Morocco,', DIM, False, 3.6),
    ('│   building AI for impact"', DIM, False, 3.8),
    ("│", BORDER, False, 0),
    ("└──────────────────────────────────┘", BORDER, False, 0),
]


def build_svg():
    lines = []
    lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {SVG_W} {SVG_H}" width="{SVG_W}" height="{SVG_H}">'
    )

    # Definitions: glow filters, gradients
    lines.append("<defs>")
    # Green glow filter
    lines.append("""
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="2" result="blur"/>
            <feComposite in="SourceGraphic" in2="blur" operator="over"/>
        </filter>
        <filter id="strongGlow" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="4" result="blur"/>
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#39d353;stop-opacity:0.6"/>
            <stop offset="50%" style="stop-color:#58a6ff;stop-opacity:0.6"/>
            <stop offset="100%" style="stop-color:#bc8cff;stop-opacity:0.6"/>
        </linearGradient>
        <linearGradient id="shimmer" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#39d353;stop-opacity:0">
                <animate attributeName="offset" values="-0.5;1.5" dur="3s" repeatCount="indefinite"/>
            </stop>
            <stop offset="15%" style="stop-color:#69f0a0;stop-opacity:0.7">
                <animate attributeName="offset" values="-0.35;1.65" dur="3s" repeatCount="indefinite"/>
            </stop>
            <stop offset="30%" style="stop-color:#39d353;stop-opacity:0">
                <animate attributeName="offset" values="-0.2;1.8" dur="3s" repeatCount="indefinite"/>
            </stop>
        </linearGradient>
    """)
    lines.append("</defs>")

    # Styles
    lines.append("<style>")
    lines.append(f"""
        .bg {{ fill: {BG}; }}
        .ascii {{ fill: {GREEN}; font-family: {FONT}; font-size: 11px; filter: url(#glow); }}
        .cmd {{ fill: {GREEN}; font-family: {FONT}; font-size: 12.5px; font-weight: bold; }}
        .info {{ fill: {DIM}; font-family: {FONT}; font-size: 12.5px; }}
        .name {{ fill: {CYAN}; font-family: {FONT}; font-size: 12.5px; font-weight: bold; }}
        .role {{ fill: {PURPLE}; font-family: {FONT}; font-size: 12.5px; }}
        .border {{ fill: {BORDER}; font-family: {FONT}; font-size: 12.5px; }}

        @keyframes typeIn {{
            from {{ clip-path: inset(0 100% 0 0); opacity: 0.3; }}
            to   {{ clip-path: inset(0 0% 0 0); opacity: 1; }}
        }}
        @keyframes fadeSlide {{
            from {{ opacity: 0; transform: translateX(-8px); }}
            to   {{ opacity: 1; transform: translateX(0); }}
        }}
        @keyframes blink {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0; }}
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 0.4; }}
            50% {{ opacity: 0.15; }}
        }}
        @keyframes asciiGlow {{
            0%, 100% {{ filter: url(#glow); opacity: 0.9; }}
            50% {{ filter: url(#strongGlow); opacity: 1; }}
        }}
        .scanline {{
            animation: pulse 4s ease-in-out infinite;
        }}
        .cursor {{
            fill: {BRIGHT_GREEN};
            filter: url(#strongGlow);
            animation: blink 0.8s step-end infinite;
        }}
    """)
    lines.append("</style>")

    # Background with rounded corners + gradient border
    lines.append(f'<rect class="bg" width="{SVG_W}" height="{SVG_H}" rx="10"/>')
    lines.append(f'<rect width="{SVG_W}" height="{SVG_H}" rx="10" fill="none" '
                 f'stroke="url(#borderGrad)" stroke-width="1.5"/>')

    # Title bar
    for i, color in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        lines.append(f'<circle cx="{20 + i * 22}" cy="18" r="6" fill="{color}" opacity="0.9"/>')
    lines.append(f'<text x="{SVG_W // 2}" y="21" text-anchor="middle" fill="{DIM}" '
                 f'font-family="{FONT}" font-size="11" opacity="0.7">meriem@github — zsh</text>')

    # Scan lines overlay (subtle CRT effect)
    for sy in range(0, SVG_H, 4):
        lines.append(f'<rect x="0" y="{sy}" width="{SVG_W}" height="1" fill="#ffffff" '
                     f'opacity="0.015" class="scanline"/>')

    # ASCII art with glow animation
    y = 50
    for i, art_line in enumerate(ASCII_ART):
        escaped = art_line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        delay = 0.05 * i
        lines.append(
            f'<text class="ascii" x="16" y="{y}" '
            f'opacity="0" style="animation: fadeSlide 0.5s ease {delay:.2f}s forwards, '
            f'asciiGlow 3s ease-in-out {delay + 0.5:.2f}s infinite;">'
            f'{escaped}</text>'
        )
        y += 16

    # Shimmer line under ASCII art
    y += 4
    lines.append(f'<rect x="16" y="{y}" width="{SVG_W - 32}" height="1" fill="url(#shimmer)"/>')

    # Terminal content with typing animation
    y += 16
    for text, color, is_cmd, delay in TERMINAL_LINES:
        escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        if not text.strip() or text.strip() in ("│",):
            y += 6
            continue

        cls = "cmd" if is_cmd else ("name" if color == CYAN else
              "role" if color == PURPLE else
              "border" if color == BORDER else "info")

        anim = "typeIn" if is_cmd else "fadeSlide"
        dur = "0.6s" if is_cmd else "0.4s"

        lines.append(
            f'<text class="{cls}" x="16" y="{y}" '
            f'opacity="0" style="animation: {anim} {dur} ease {delay:.2f}s forwards;">'
            f'{escaped}</text>'
        )
        y += 18

    # Blinking cursor
    lines.append(
        f'<rect class="cursor" x="16" y="{y}" width="9" height="15" rx="1" '
        f'opacity="0" style="animation: fadeSlide 0.1s ease 4.2s forwards, '
        f'blink 0.8s step-end 4.3s infinite;"/>'
    )

    lines.append("</svg>")
    return "\n".join(lines)


if __name__ == "__main__":
    out = pathlib.Path(__file__).resolve().parent.parent / "data" / "ascii_intro.svg"
    out.write_text(build_svg())
    print(f"✓ Wrote {out}")
