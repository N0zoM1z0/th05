#!/usr/bin/env python3
"""Generate mathematical Q8 angle inputs, without reading a game or oracle.

The C initializer specializes these inputs to the game's 192-subpixel shot
speed. This generator emits neither executable bytes nor the specialized
velocity table. Decimal sine and explicit nearest rounding avoid host libm.
"""
from __future__ import annotations

import argparse
from decimal import Decimal, ROUND_HALF_UP, localcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "src/main/player/shot_velocity_q8.inc"
PI = Decimal("3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986")


def sine_q8() -> list[int]:
    with localcontext() as context:
        context.prec = 80
        values = []
        for angle in range(256):
            if angle % 64 == 0:
                sine = (Decimal(0), Decimal(1), Decimal(0), Decimal(-1))[angle // 64]
            else:
                radians = 2 * PI * angle / 256
                if radians > PI:
                    radians -= 2 * PI
                term = sine = radians
                n = 1
                while abs(term) > Decimal("1e-74"):
                    term *= -(radians * radians) / ((2 * n) * (2 * n + 1))
                    sine += term
                    n += 1
            values.append(int((sine * 256).to_integral_value(rounding=ROUND_HALF_UP)))
        return values


def render() -> str:
    sine = sine_q8()
    lines = [
        "/* Mathematical Q8 cosine/sine samples; regenerated without target input. */",
        "/* Use generate_shot_velocity_table.py --check to verify this include. */",
    ]
    for angle in range(256):
        lines.append(
            f"VELOCITY_FROM_Q8({sine[(angle + 64) % 256]:4d}, {sine[angle]:4d}), /* angle {angle:3d} */"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = render()
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text() != content:
            parser.exit(1, f"outdated mathematical angle include: {OUTPUT}\n")
        print("PASS 256 mathematical Q8 angle samples; no target input")
    else:
        OUTPUT.write_text(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
