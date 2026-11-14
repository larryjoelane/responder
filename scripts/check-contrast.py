#!/usr/bin/env python3
"""Check theme color pairs against WCAG 2.2 AA.

Text and placeholders need 4.5:1. Large headings are checked at 3:1 and
also reported at 4.5:1. Borders, button fills against the page, and focus
colors need 3:1. Disabled controls are inactive UI, so 1.4.3 exempts them;
they are still reported.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEMES = ["green", "light", "dark"]


def lin(channel):
    channel = channel / 255
    if channel <= 0.04045:
        return channel / 12.92
    return ((channel + 0.055) / 1.055) ** 2.4


def lum(hex_color):
    hex_color = hex_color.lstrip("#")
    rgb = [lin(int(hex_color[i : i + 2], 16)) for i in (0, 2, 4)]
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def contrast(foreground, background):
    lighter = max(lum(foreground), lum(background))
    darker = min(lum(foreground), lum(background))
    return (lighter + 0.05) / (darker + 0.05)


def mix(foreground, background, amount):
    def channel(hex_color, index):
        return int(hex_color.lstrip("#")[index : index + 2], 16)

    out = ""
    for index in (0, 2, 4):
        value = round(channel(foreground, index) * amount + channel(background, index) * (1 - amount))
        out += f"{value:02x}"
    return "#" + out


def load(theme):
    text = (ROOT / "css" / "themes" / f"{theme}.css").read_text()
    return dict(re.findall(r"(--responder-color-[\w-]+):\s*(#[0-9a-fA-F]{6})", text))


def main():
    failures = 0
    for theme in THEMES:
        color = load(theme)
        bg = color["--responder-color-bg"]
        surface = color["--responder-color-surface"]
        text = color["--responder-color-text"]
        muted = color["--responder-color-muted"]
        heading = color["--responder-color-heading"]
        accent = color["--responder-color-accent"]
        hover = color["--responder-color-accent-hover"]
        active = color["--responder-color-accent-active"]
        ink = color["--responder-color-accent-contrast"]
        header = color["--responder-color-header-bg"]
        header_text = color["--responder-color-header-text"]
        header_hover = color["--responder-color-header-hover"]
        border = color["--responder-color-border"]
        focus = color["--responder-color-focus"]
        link = color["--responder-color-link"]
        code_bg = color["--responder-color-code-bg"]
        code_text = color["--responder-color-code-text"]
        warning = color["--responder-color-warning"]
        success = color["--responder-color-success"]
        danger = color["--responder-color-danger"]
        disabled_bg = color["--responder-color-disabled-bg"]
        disabled_text = color["--responder-color-disabled-text"]

        notice = mix(accent, surface, 0.10)
        warn_bg = mix(warning, surface, 0.14)
        ok_bg = mix(success, surface, 0.12)
        bad_bg = mix(danger, surface, 0.12)
        stripe = mix(accent, surface, 0.06)

        pairs = [
            ("text on page", text, bg, 4.5),
            ("text on surface", text, surface, 4.5),
            ("muted on page", muted, bg, 4.5),
            ("muted on surface", muted, surface, 4.5),
            ("heading on page", heading, bg, 4.5),
            ("heading on surface", heading, surface, 4.5),
            ("link on page", link, bg, 4.5),
            ("link on surface", link, surface, 4.5),
            ("link hover on page", hover, bg, 4.5),
            ("link hover on surface", hover, surface, 4.5),
            ("link active on page", active, bg, 4.5),
            ("link active on surface", active, surface, 4.5),
            ("button label", ink, accent, 4.5),
            ("button hover label", ink, hover, 4.5),
            ("button active label", ink, active, 4.5),
            ("button against page", accent, bg, 3.0),
            ("button against surface", accent, surface, 3.0),
            ("button hover against page", hover, bg, 3.0),
            ("quiet label on page", accent, bg, 4.5),
            ("quiet label on surface", accent, surface, 4.5),
            ("quiet hover on surface", hover, surface, 4.5),
            ("header text", header_text, header, 4.5),
            ("header hover", header_hover, header, 4.5),
            ("selected theme pill", header, header_hover, 4.5),
            ("focus on page", focus, bg, 3.0),
            ("focus on surface", focus, surface, 3.0),
            ("focus on header", header_hover, header, 3.0),
            ("border on page", border, bg, 3.0),
            ("border on surface", border, surface, 3.0),
            ("code", code_text, code_bg, 4.5),
            ("notice text", text, notice, 4.5),
            ("warning text", text, warn_bg, 4.5),
            ("success text", text, ok_bg, 4.5),
            ("danger text", text, bad_bg, 4.5),
            ("warning border", warning, warn_bg, 3.0),
            ("success border", success, ok_bg, 3.0),
            ("danger border", danger, bad_bg, 3.0),
            ("table text", text, stripe, 4.5),
            ("disabled label", disabled_text, disabled_bg, 4.5),
        ]
        print(f"\n{theme}")
        for label, foreground, background, minimum in pairs:
            ratio = contrast(foreground, background)
            status = "ok" if ratio + 1e-9 >= minimum else "FAIL"
            if status == "FAIL":
                failures += 1
            print(f"  {ratio:5.2f} {status:4} {minimum:.1f}  {label}  {foreground} on {background}")
    if failures:
        print(f"\n{failures} contrast failures")
        return 1
    print("\nAll required pairs pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
