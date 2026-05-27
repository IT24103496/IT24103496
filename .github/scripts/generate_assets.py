#!/usr/bin/env python3
"""Generate original, lightweight SVG visuals for Dasun's GitHub profile."""
from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"
CONFIG = ROOT / "profile.config.json"


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def wrapper(width: int, height: int, body: str) -> str:
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img">
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop stop-color="#040B15"/><stop offset="0.52" stop-color="#071C28"/><stop offset="1" stop-color="#111534"/>
    </linearGradient>
    <linearGradient id="signal" x1="0" x2="1"><stop stop-color="#18E0D0"/><stop offset="1" stop-color="#6366F1"/></linearGradient>
    <linearGradient id="safe" x1="0" x2="1"><stop stop-color="#18E0D0"/><stop offset="1" stop-color="#A3E635"/></linearGradient>
    <filter id="blur"><feGaussianBlur stdDeviation="28"/></filter>
    <filter id="soft"><feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#18E0D0" flood-opacity=".15"/></filter>
    <pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse"><path d="M34 0H0V34" fill="none" stroke="#102A38" stroke-width="1"/></pattern>
  </defs>
  <rect width="100%" height="100%" rx="24" fill="url(#bg)"/>
  <rect width="100%" height="100%" rx="24" fill="url(#grid)" opacity=".48"/>
  <circle cx="170" cy="44" r="108" fill="#18E0D0" opacity=".13" filter="url(#blur)"/>
  <circle cx="1055" cy="288" r="150" fill="#6366F1" opacity=".14" filter="url(#blur)"/>
{body}
</svg>\n'''


def hero(config: dict[str, Any]) -> str:
    name = esc(config["display_name"])
    headline = esc(config["headline"])
    tagline = esc(config["tagline"])
    specialties = esc(config.get("specialties", ""))
    return wrapper(1200, 360, f'''
  <text x="58" y="67" fill="#18E0D0" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="700" letter-spacing="2">NETWORKS / SECURITY / SOFTWARE</text>
  <text x="58" y="132" fill="#F8FAFC" font-family="Inter, Segoe UI, Arial" font-size="54" font-weight="800">{name}</text>
  <text x="60" y="173" fill="#DCE7F6" font-family="Inter, Segoe UI, Arial" font-size="19" font-weight="600">{headline}</text>
  <text x="60" y="204" fill="#DCE7F6" font-family="Inter, Segoe UI, Arial" font-size="18" font-weight="600">{specialties}</text>
  <text x="60" y="238" fill="#94A3B8" font-family="Inter, Segoe UI, Arial" font-size="15">{tagline}</text>
  <rect x="58" y="274" width="194" height="38" rx="19" fill="#06242A" stroke="#18E0D0" stroke-opacity=".5"/>
  <text x="78" y="298" fill="#C9FFFB" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="700">JAVA · SPRING</text>
  <rect x="264" y="274" width="212" height="38" rx="19" fill="#151738" stroke="#6366F1" stroke-opacity=".62"/>
  <text x="285" y="298" fill="#E0E7FF" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="700">SECURE SYSTEMS</text>

  <rect x="792" y="42" width="346" height="272" rx="24" fill="#06121D" stroke="#173446" filter="url(#soft)"/>
  <text x="820" y="78" fill="#94A3B8" font-family="JetBrains Mono, Consolas, monospace" font-size="11">SECURE SERVICE TOPOLOGY</text>
  <rect x="826" y="112" width="76" height="48" rx="12" fill="#07242A" stroke="#18E0D0" stroke-opacity=".72"/>
  <text x="844" y="141" fill="#C9FFFB" font-family="JetBrains Mono, monospace" font-size="10">CLIENT</text>
  <path d="M904 136H938" stroke="url(#signal)" stroke-width="3"/><circle cx="921" cy="136" r="4" fill="#18E0D0"/>
  <rect x="940" y="102" width="82" height="68" rx="13" fill="#12163A" stroke="#6366F1" stroke-opacity=".75"/>
  <path d="M981 114L1004 124V141C1004 153 994 160 981 165C968 160 958 153 958 141V124Z" fill="none" stroke="#A3E635" stroke-width="2"/>
  <text x="957" y="188" fill="#C7D2FE" font-family="JetBrains Mono, monospace" font-size="9">SECURITY</text>
  <path d="M1024 136H1050" stroke="url(#safe)" stroke-width="3"/>
  <rect x="1052" y="112" width="58" height="48" rx="12" fill="#08241B" stroke="#A3E635" stroke-opacity=".62"/>
  <text x="1063" y="141" fill="#ECFCCB" font-family="JetBrains Mono, monospace" font-size="9">API</text>
  <path d="M874 218H1080" stroke="#102B3D" stroke-width="2" stroke-dasharray="5 7"/>
  <circle cx="875" cy="218" r="7" fill="#18E0D0"/><circle cx="978" cy="218" r="7" fill="#6366F1"/><circle cx="1080" cy="218" r="7" fill="#A3E635"/>
  <text x="826" y="259" fill="#94A3B8" font-family="JetBrains Mono, Consolas, monospace" font-size="10">VALIDATE  →  ROUTE  →  SERVE</text>
  <rect x="826" y="277" width="284" height="9" rx="5" fill="#0D2632"/>
  <rect x="826" y="277" width="238" height="9" rx="5" fill="url(#safe)" opacity=".84"/>
''')


def systems_blueprint() -> str:
    cards = [
        ("01", "Observe", "Traffic &amp; requirements", "#18E0D0"),
        ("02", "Secure", "Boundaries &amp; controls", "#A3E635"),
        ("03", "Build", "Java services", "#6366F1"),
        ("04", "Operate", "Reliability loop", "#18E0D0"),
    ]
    body = [
        '  <text x="44" y="58" fill="#F8FAFC" font-family="Inter, Arial" font-size="27" font-weight="800">Secure Systems Blueprint</text>',
        '  <text x="44" y="87" fill="#94A3B8" font-family="Inter, Arial" font-size="14">A network-engineering inspired workflow for reliable software delivery</text>',
    ]
    x = 46
    for index, title, subtitle, color in cards:
        body.extend([
            f'  <rect x="{x}" y="130" width="238" height="132" rx="18" fill="#06131F" stroke="#173446" filter="url(#soft)"/>',
            f'  <text x="{x+22}" y="166" fill="{color}" font-family="JetBrains Mono, monospace" font-size="14" font-weight="700">{index}</text>',
            f'  <text x="{x+22}" y="202" fill="#F8FAFC" font-family="Inter, Arial" font-size="20" font-weight="700">{title}</text>',
            f'  <text x="{x+22}" y="231" fill="#94A3B8" font-family="Inter, Arial" font-size="13">{subtitle}</text>',
        ])
        if x < 800:
            body.extend([
                f'  <path d="M{x+244} 196H{x+268}" stroke="url(#signal)" stroke-width="3"/>',
                f'  <path d="M{x+261} 189L{x+270} 196L{x+261} 203" fill="none" stroke="#18E0D0" stroke-width="3"/>',
            ])
        x += 270
    return wrapper(1200, 310, "\n".join(body))


def automation_loop() -> str:
    nodes = [
        ("CONFIG", "profile.config.json"),
        ("BOT", "GitHub REST API"),
        ("SVG", "Local dashboard"),
        ("README", "Protected blocks"),
        ("VERIFY", "Tests + CodeQL"),
    ]
    body = [
        '  <text x="44" y="56" fill="#F8FAFC" font-family="Inter, Arial" font-size="27" font-weight="800">Automation Loop</text>',
        '  <text x="44" y="84" fill="#94A3B8" font-family="Inter, Arial" font-size="14">Deterministic profile updates: commits occur only when displayed content changes</text>',
    ]
    x = 44
    for index, (title, subtitle) in enumerate(nodes):
        body.extend([
            f'  <rect x="{x}" y="136" width="204" height="106" rx="18" fill="#06131F" stroke="#173446"/>',
            f'  <text x="{x+18}" y="174" fill="#18E0D0" font-family="JetBrains Mono, monospace" font-size="13" font-weight="700">{title}</text>',
            f'  <text x="{x+18}" y="208" fill="#CBD5E1" font-family="Inter, Arial" font-size="12">{subtitle}</text>',
        ])
        if index < len(nodes) - 1:
            body.append(f'  <path d="M{x+210} 188H{x+228}" stroke="url(#signal)" stroke-width="3"/>')
        x += 228
    body.extend([
        '  <path d="M1084 258C1084 291 72 291 72 258" fill="none" stroke="#243A4B" stroke-width="2" stroke-dasharray="7 7"/>',
        '  <text x="465" y="288" fill="#64748B" font-family="JetBrains Mono, monospace" font-size="12">SCHEDULED + MANUAL REFRESH</text>',
    ])
    return wrapper(1200, 320, "\n".join(body))


def main() -> int:
    config = load_config()
    ASSETS.mkdir(exist_ok=True)
    files = {
        "hero-banner.svg": hero(config),
        "systems-blueprint.svg": systems_blueprint(),
        "automation-loop.svg": automation_loop(),
    }
    for name, content in files.items():
        (ASSETS / name).write_text(content, encoding="utf-8")
        print(f"generated assets/{name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
