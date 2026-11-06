#!/usr/bin/env python3
"""Check the reference CSS: contrast pairs and the type ramp (stdlib only).

Contrast covers the token pairs the CSS actually uses, including the alpha
grays, which are composited over their background before measuring. The type
check guards the two rules that decay first: the px size/leading pairs of the
measured ramp, and the 400/500/600 weight range.

It does not check screenshots, focus placement, real rendered line breaks, or
the accessibility of a downstream application.
"""
from pathlib import Path
import re
import sys


def linear(value):
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def channels(color):
    """#RRGGBB -> (r, g, b, a) with each channel in 0..1; #RRGGBBAA keeps alpha."""
    body = color.lstrip('#')
    parts = [int(body[i:i + 2], 16) / 255 for i in range(0, len(body), 2)]
    return tuple(parts) if len(parts) == 4 else (*parts, 1.0)


def over(color, backdrop):
    """Composite a possibly translucent color over an opaque backdrop."""
    r, g, b, a = channels(color)
    br, bg_, bb, _ = channels(backdrop)
    return (r * a + br * (1 - a), g * a + bg_ * (1 - a), b * a + bb * (1 - a), 1.0)


def luminance(rgba):
    return sum(weight * linear(value)
               for weight, value in zip((0.2126, 0.7152, 0.0722), rgba[:3]))


def contrast(foreground, background):
    """Foreground may be translucent; the background must be opaque."""
    high, low = sorted((luminance(over(foreground, background)),
                        luminance(channels(background))), reverse=True)
    return (high + 0.05) / (low + 0.05)


def token_blocks(css):
    """Base tokens from .muse-theme, plus each layer merged over the base."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    blocks = re.findall(r'([^{}]+)\{([^{}]*--muse-[^{}]*)\}', css)
    base, layers = {}, {}
    for selector, body in blocks:
        tokens = dict(re.findall(r'--muse-([\w-]+)\s*:\s*(#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8}))\s*;', body))
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
PAIRS += [('text-tertiary', bg, 4.5) for bg in ('bg', 'surface', 'soft')]
PAIRS += [('primary', 'bg', 4.5), ('primary', 'surface', 4.5), ('primary', 'soft', 4.5),
          ('on-primary', 'primary', 4.5), ('on-primary', 'primary-hover', 4.5),
          ('primary', 'primary-soft', 4.5),
          ('success', 'success-soft', 4.5), ('danger', 'danger-soft', 4.5),
          ('control-border', 'surface', 3), ('control-border', 'bg', 3),
          ('control-border', 'soft', 3)]


# Sizes and leadings read from the CSS platform.muse.ai serves, 2026-11-06.
RAMP = {
    'caption-2': (11, 13), 'caption-1': (12, 16), 'footnote': (13, 18),
    'subheadline': (14, 20), 'subheadline-lg': (15, 20), 'body': (16, 22),
    'response': (16, 26), 'body-status': (17, 22), 'title-3': (18, 26),
    'title-2': (22, 28), 'title-1': (30, 34), 'lg-title-3': (34, 40),
    'lg-title-2': (40, 46), 'lg-title-1': (48, 52),
}
ALLOWED_WEIGHTS = {'400', '500', '600'}


def check_type(css):
    """The ramp pairs are intact and no rule asks for a weight outside 400-600."""
    failed = False
    declared = dict(re.findall(r'--muse-([\w-]+)\s*:\s*(\d+)px\s*;', css))
    for role, (size, leading) in RAMP.items():
        got = (declared.get(role), declared.get(f'{role}-lh'))
        want = (str(size), str(leading))
        ok = got == want
        failed |= not ok
        print(f'{"PASS" if ok else "FAIL"} ramp {role:15} {got[0]}/{got[1]}px '
              f'(expects {size}/{leading}px)')
    weights = sorted({w for w in re.findall(r'font-weight:\s*(\d+)', css)}
                     - ALLOWED_WEIGHTS)
    if weights:
        failed = True
        print(f'FAIL font-weight outside 400/500/600: {", ".join(weights)}')
    else:
        print('PASS font-weight literals stay within 400/500/600')
    return failed


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
    print('== type ramp')
    failed |= check_type(css)
    print('Tokens only; inspect the real interface separately.')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
