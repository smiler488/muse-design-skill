#!/usr/bin/env python3
"""Check the reference CSS: contrast pairs and the type ramp (stdlib only).

Contrast covers the token pairs the CSS actually uses, including the alpha
grays, which are composited over their background before measuring. The type
check guards the px size/leading pairs of the measured ramp and the 400/500/600
weight range. The accent check holds each hue to the one step that works both
as text on white and as a fill under white text, and keeps the two hues that
cannot carry text from being promoted. The motion check holds the duration
pairs to "out is never slower than in" and requires the intent-named curves.

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


# Accents: each hue's one usable step, and the ceiling it must clear on every
# background the page actually uses. Measured on platform.muse.ai, 2026-11-06.
ACCENT_BACKDROPS = ('#FFFFFF', '#FCFCFC', '#F3F4F5')
ACCENTS = {'blue': '#0064D4', 'indigo': '#4553E4', 'purple': '#8523C6',
           'red': '#C01F37', 'green': '#008200'}
# Deliberately NOT text colors: orange clears 4.5:1 on white but not on the
# soft panel, and yellow clears it nowhere. If a future edit promotes either
# into --muse-primary, this check fails on purpose.
NON_TEXT_MARKERS = {'marker-orange': '#C65323', 'marker-yellow': '#B07C00'}

DURATION_STEPS = ('xxs', 'xs', 's', 'm', 'l', 'xl')
REQUIRED_CURVES = ('move', 'passive', 'quick', 'enter', 'exit', 'fade')


def check_accents(css):
    """Every offered accent is legible as text and as a fill, both ways."""
    failed = False
    for name, value in ACCENTS.items():
        worst = min(contrast(value, bg) for bg in ACCENT_BACKDROPS)
        on_fill = contrast('#FFFFFF', value)
        ok = worst >= 4.5 and on_fill >= 4.5
        failed |= not ok
        print(f'{"PASS" if ok else "FAIL"} accent {name:8} {value} '
              f'worst-on-page {worst:.2f}:1, white-on-it {on_fill:.2f}:1 (requires 4.5:1)')
    for name, value in NON_TEXT_MARKERS.items():
        worst = min(contrast(value, bg) for bg in ACCENT_BACKDROPS)
        # These must stay below the bar; if one ever clears it the comment in
        # muse.css is wrong and the restriction should be revisited.
        ok = worst < 4.5 and f'--muse-{name}: {value}' in css
        failed |= not ok
        print(f'{"PASS" if ok else "FAIL"} marker {name:14} {value} '
              f'{worst:.2f}:1 — must stay a non-text marker')
    promoted = [n for n, v in NON_TEXT_MARKERS.items()
                if re.search(r'--muse-primary\s*:\s*' + v + r'\s*;', css, re.I)]
    if promoted:
        failed = True
        print(f'FAIL {", ".join(promoted)} is used as --muse-primary but cannot carry text')
    return failed


def check_motion(css):
    """Durations come in in/out pairs where out is never slower than in."""
    failed = False
    # Keep the FIRST declaration of each: the prefers-reduced-motion block
    # later in the file zeroes them all, and that override is not the scale.
    ms = {}
    for name, value in re.findall(r'--muse-duration-([\w-]+)\s*:\s*(\d+)ms\s*;', css):
        ms.setdefault(name, value)
    for step in DURATION_STEPS:
        a, b = ms.get(f'{step}-in'), ms.get(f'{step}-out')
        ok = a is not None and b is not None and int(b) <= int(a)
        failed |= not ok
        print(f'{"PASS" if ok else "FAIL"} duration {step:4} in {a}ms / out {b}ms '
              f'(out must not be slower)')
    missing = [c for c in REQUIRED_CURVES if f'--muse-ease-{c}:' not in css]
    if missing:
        failed = True
        print(f'FAIL missing intent curve(s): {", ".join(missing)}')
    else:
        print('PASS intent curves present: ' + ", ".join(REQUIRED_CURVES))
    fade = re.search(r'--muse-ease-fade\s*:\s*([^;]+);', css)
    fade_ok = bool(fade) and fade.group(1).strip() in ('linear', 'cubic-bezier(0, 0, 1, 1)')
    failed |= not fade_ok
    print(f'{"PASS" if fade_ok else "FAIL"} fade curve is linear '
          f'(opacity takes no easing)')
    # Light theme first, then the dark override; take each step's first
    # declaration so the dark block does not shadow the light one.
    levels = {}
    for step, value in re.findall(r'--muse-elevation-([123])\s*:\s*([^;]+);', css):
        levels.setdefault(step, value)
    tinted = (len(levels) == 3
              and all(v.count(',') >= 1 and '#111112' in v for v in levels.values()))
    failed |= not tinted
    print(f'{"PASS" if tinted else "FAIL"} 3 light elevation steps, two-layer, tinted #111112')
    return failed


DARK_SELECTORS = (
    r':root\[data-theme="dark"\] \.muse-theme,[^{]*\{([^{}]*)\}',
    r'\.muse-theme:root:not\(\[data-theme="light"\]\)\s*\{([^{}]*)\}',
)


def check_dark_parity(css):
    """The explicit and the system dark blocks declare the same tokens."""
    blocks = []
    for pattern in DARK_SELECTORS:
        found = re.search(pattern, css)
        if not found:
            print(f'FAIL dark block not found: {pattern[:40]}...')
            return True
        blocks.append(dict(re.findall(r'(--muse-[\w-]+)\s*:\s*([^;]+);', found.group(1))))
    explicit, system = ({k: v.strip() for k, v in b.items()} for b in blocks)
    same = explicit == system
    if same:
        print(f'PASS dark blocks identical ({len(explicit)} tokens declared twice)')
        return False
    for key in sorted(set(explicit) | set(system)):
        if explicit.get(key) != system.get(key):
            print(f'FAIL dark drift {key}: explicit={explicit.get(key)} system={system.get(key)}')
    return True


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
            backdrop = tokens[background]
            if len(backdrop.lstrip('#')) == 8:
                # A translucent panel is only ever seen over the page, so
                # measure the text against what the eye actually gets.
                page = tokens.get('bg', '#FFFFFF')
                r, g, b, _ = over(backdrop, page)
                backdrop = '#%02x%02x%02x' % (round(r * 255), round(g * 255), round(b * 255))
            ratio = contrast(tokens[foreground], backdrop)
            passed = ratio >= required
            failed |= not passed
            print(f'{"PASS" if passed else "FAIL"} {foreground:16} / {background:16} '
                  f'{ratio:.2f}:1 (requires {required}:1)')
    print('== type ramp')
    failed |= check_type(css)
    print('== dark theme')
    failed |= check_dark_parity(css)
    print('== accents')
    failed |= check_accents(css)
    print('== motion & elevation')
    failed |= check_motion(css)
    print('Tokens only; inspect the real interface separately.')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
