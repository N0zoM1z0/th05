# Original Master ATAN8: MAINE's complete 256-byte native lookup

The original MAINE `[101CC,102CC)` is the complete 256-byte
`AtanTable8` source from Master 0.23's archived `ATAN8.ASM`.
The original author gives sixteen complete sixteen-byte rows, providing
the monotonic mapping from an 8-bit slope to an eighth-circle angle.
The retained TASM source `libs/master.lib/atan8[data].asm` emits those same
256 values. The original CAL MAP public anchors `_AtanTable8` and
`AtanTable8` to `1010:00BC`, and the real `mainem.obj` DATA LEDATA
begins at local zero with all 256 exact source values.

The raw bytes in the original MZ and the actual retained calibration MZ
match the complete source and have **no loader relocations**. Unlike the
previously accepted independent MAIN table, MAINE's copy was still unknown
and is credited separately as **256 bytes of foreign initialized DATA**,
not original C++ code or a second MAIN owner.

The physical boundary matters: MAINE `[101CB,101CC)` is one still-unknown
preceding byte, and `[102CC,102DA)` contains **eight zero bytes followed by the six-byte** `BFNT 1Ah 00h`
font-header prefix. The native TASM ATAN LEDATA contributes two of the
trailing zeros; the remaining values belong to separate following context. These are not part of the author's 256-value table
and remain unknown; a separate CLIP initialized-DATA owner begins at
`102DA`. These fourteen bytes remain outside the 256-byte ATAN owner; no
additional resource or initialized-byte credit is inferred.

Focused original-source, real MAP/OMF and original-target verification:
`python3 scripts/review_maine_atan8_initial.py --check`.
Evidence: `config/reviewed_maine_atan8_initial.json`.
This review runs no full cold replay and grants zero game-authored C/C++ credit.
