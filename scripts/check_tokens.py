#!/usr/bin/env python3
"""Check contrast pairs actually used by the reference CSS (Python stdlib only).

This checks solid-color token pairs, not screenshots, transparency, font sizes,
focus placement, or the accessibility of a downstream application.
"""
from pathlib import Path
import re
import sys


def linear(channel):
    value = int(channel, 16) / 255
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def luminance(color):
    return sum(weight * linear(color[start:start + 2])
               for weight, start in zip((0.2126, 0.7152, 0.0722), (1, 3, 5)))


def contrast(a, b):
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def main():
    css_path = (Path(sys.argv[1]) if len(sys.argv) > 1
                else Path(__file__).resolve().parents[1] / 'assets' / 'muse.css')
    css = css_path.read_text(encoding='utf-8')
    tokens = dict(re.findall(r'--muse-([\w-]+)\s*:\s*(#[0-9A-Fa-f]{6})\s*;', css))
    pairs = [(fg, bg, 4.5) for fg in ('text', 'muted') for bg in ('bg', 'surface', 'soft')]
    pairs += [('primary', 'bg', 4.5), ('primary', 'surface', 4.5),
              ('on-primary', 'primary', 4.5), ('on-primary', 'primary-hover', 4.5),
              ('success', 'success-soft', 4.5), ('danger', 'danger-soft', 4.5),
              ('control-border', 'surface', 3), ('control-border', 'bg', 3),
              ('primary', 'soft', 3)]
    failed = False
    for foreground, background, required in pairs:
        if foreground not in tokens or background not in tokens:
            print(f'FAIL missing token: {foreground} / {background}')
            failed = True
            continue
        ratio = contrast(tokens[foreground], tokens[background])
        passed = ratio >= required
        failed |= not passed
        print(f'{"PASS" if passed else "FAIL"} {foreground:16} / {background:16} '
              f'{ratio:.2f}:1 (requires {required}:1)')
    print('Solid-color pairs only; inspect the real interface separately.')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
