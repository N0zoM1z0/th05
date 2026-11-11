# Three original Master circle helpers: 223 complete source-written CODE bytes

Three separate near procedures in TH05 MAIN's original graphics module are
recovered from **the author's unchanged `GC_CIRCL.ASM`**, the retained TASM
OMF and original ordered linker fixups. They occupy parts of the old unknown
circle region; the previously accepted primary `GRCG_CIRCLEFILL`, main
`GRCG_CIRCLE`, and primary `GRCG_CIRCLE_X` are unchanged.

| Complete procedure | Original MAIN load extent | CODE bytes | OMF fixups |
| --- | --- | ---: | ---: |
| `GC_CIRCL_ALLIN` (original `ALLIN`) | `10A4..10AE` | 10 | 0 |
| `GC_CIRCL_PSET4Q` (original `PSET4Q`) | `1146..1148` | 2 | 0 |
| `GC_CIRCL_PSET4` (original `PSET4`) | `1148..121B` | 211 | 16 |

The namespaced `GC_CIRCL_` spelling in the pinned ReC98 assembler source is
an adaptation of the matching original procedure names, not different
instructions. Normalized source blocks match line-for-line, including actual
register operations, `ORG $-1` self-patched zoom operands, and the `RET`/`EVEN`
terminators. The complete procedure boundaries are present in the original
TASM listing; the two-byte `PSET4Q` is anchored by that listing and adjacent
`GRCG_CIRCLE` and `PSET4`, not by an implausible uniqueness claim for `C3 90`.

The retained compiler/assembler-produced OMF includes every LEDATA byte and
all 16 genuine `PSET4` offset16 fixups. Linking once with calibration frames
and once with the independently established original C0L/DGROUP layout
reconstructs **all 223 native bytes** without patching instruction bytes,
changing source operands or reordering relocation sites. Both the calibration
and native original MZ fixup streams are empty for these three scopes;
source and target extents agree exactly. `PSET4`'s full 211-byte occurrence
is also unique in the original MAIN image.

**The byte at `121B` is deliberately excluded.** It is after `PSET4`'s real
near `RET` and before the separate primary `GRCG_CIRCLE_X`. The retained
calibration has `90` from an `EVEN` directive there, but original MAIN has
`00`. It remains a one-byte *unknown* ownership interval. Neither the helper
proof nor the explicit adoption fills or normalizes it.

Executable native evidence and source pins are in
[`config/master_circle_helpers_ownership.json`](../../config/master_circle_helpers_ownership.json),
with a separate decision in
[`config/reviewed_master_circle_helpers.json`](../../config/reviewed_master_circle_helpers.json).
The bounded real check is `python3 scripts/review_master_circle_helpers.py
--check`; public CI uses only its `--structural-check` and normal ownership
checks, without the Japanese image or installed assembler. Existing accepted
C/C++ and ASM replay receipts are untouched. All 223 bytes are original
third-party Master CODE with **zero game-authored credit**. No global authored
percentage or whole-executable claim follows from this review.
