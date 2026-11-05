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


def token_blocks(css):
    """Base tokens from .muse-theme, plus each layer merged over the base."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    blocks = re.findall(r'([^{}]+)\{([^{}]*--muse-[^{}]*)\}', css)
    base, layers = {}, {}
    for selector, body in blocks:
        tokens = dict(re.findall(r'--muse-([\w-]+)\s*:\s*(#[0-9A-Fa-f]{6})\s*;', body))
        name = selector.strip().split()[-1] if selector.strip() != '.muse-theme' else 'app'
        if name == 'app':
            base.update(tokens)
        elif tokens:
            layers[name] = tokens
    result = {'app layer (default)': base}
    for name, tokens in layers.items():
        result[f'{name.lstrip(".")}'] = {**base, **tokens}
    return result


PAIRS = [(fg, bg, 4.5) for fg in ('text', 'muted') for bg in ('bg', 'surface', 'soft')]
PAIRS += [('primary', 'bg', 4.5), ('primary', 'surface', 4.5), ('primary', 'soft', 4.5),
          ('on-primary', 'primary', 4.5), ('on-primary', 'primary-hover', 4.5),
          ('primary', 'primary-soft', 4.5),
          ('success', 'success-soft', 4.5), ('danger', 'danger-soft', 4.5),
          ('control-border', 'surface', 3), ('control-border', 'bg', 3),
          ('control-border', 'soft', 3)]


def main():
    css_path = (Path(sys.argv[1]) if len(sys.argv) > 1
                else Path(__file__).resolve().parents[1] / 'assets' / 'muse.css')
    css = css_path.read_text(encoding='utf-8')
    failed = False
    for layer, tokens in token_blocks(css).items():
        print(f'== {layer}')
        for foreground, background, required in PAIRS:
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
