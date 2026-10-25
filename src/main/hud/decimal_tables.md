# Decimal-place factor DATA

This owner defines two complete adjacent mathematical tables at MAIN load
`21DD6..21DFC`, in DS209D at1406..142C. Seven unsigned DWORD factors descend
from10^6 to10^0 (28 bytes); five unsigned word factors descend from10^4 to10^0
(10 bytes). There are no padding bytes or original segment relocations.
They are semantic divisors, not digit bitmaps, gaiji payloads or encoded assets.
Historical source translation-unit and const qualification are unknown.

Actual HUD instructions select DS1406 or its third DWORD at140E, divide by
DWORD factors at158F0 and advance the pointer by4 at158FE. The five-digit and
seven-digit entries share that loop. Actual point-popup instructions select
DS1422 at1587C, divide by words at15886, and advance by2 at15895. The score-delta
converter independently selects the same word bank atD564 and uses word DIV
atD56E. Both word consumers perform four divisions and use the last remainder
as the units digit. Their bounded original instruction views establish the
widths, table indices and decimal semantics independently of reference labels.

Pinned ReC98's `th02/main/hud/score_put[data].asm`,
`th03/main/5_powers_of_10[data].asm`, `th05/main/hud/number_p.asm`,
`th05/main/pointnum/digits.asm` and `th04/main/scoreupd.asm` corroborate the
algorithms and names. No target byte string or assembly instruction body is
used as maintained source. The compiler generates both ordinary numeric arrays
from decimal initializers. Existing formatter interfaces/sources are unchanged.

Private native review is `.analysis/hud-decimal-tables-boundary-review.json`.
Receipt `.analysis/unit-replays/main-hud-decimal-tables-data-a/receipt.json`
passes two fresh deterministic producers, the full38-byte real compiler
DATA contribution with gapless LEDATA coverage, all raw bytes and empty ordered
fixups. Its own compiled negative changes the million-place divisor from
1000000 to1000001 and is rejected. The unchanged installed-tool proof is reused.
Credit is38 initialized DATA bytes, with zero CODE, BSS or padding ownership.
The symbol-only binder supplies only foreign frame/prefix extents; the gaiji
row beginning at142C and all surrounding objects remain outside this owner.
