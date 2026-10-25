# Monochrome 16x16 ring blit: assembly review

This owner is the complete MAIN C21E..C322 graphics kernel: 260 compared bytes,
with 254 instruction bytes and six checked alignment NOPs. Its actual CS is
0AE1, with entry offset 140E. The next complete pellet renderer begins at C322.
There are no embedded tables or original MZ relocations in this scope. No
pattern pixels, segment handles, DATA, BSS or foreign callee bodies are owned.

The maintained semantic assembly factors the three row operations and the
shared video-ring driver into macros. Geometry is 16x16 pixels, 80 bytes per
row and 400 rows. It selects one external pattern segment, reads 16 two-byte
rows, rotates unaligned rows across three destination bytes, and skips blank
writes. An odd destination uses a leading byte and aligned word; an even one
uses an aligned word and trailing byte. Rows crossing the bottom wrap once
by subtracting the complete plane size. There is no clipping, argument
validation, top normalization or extra graphics-state setup.

The actual hybrid interface takes top in AX, left in CX and one Pascal stack
word for the pattern number. It returns with RET2 and preserves DS/SI/DI/BP/ES.
Callers provide the pattern table's DATA segment, video ES, the intended GRCG
mode/color and clear DF. Working AX/BX/CX/DX and arithmetic flags are clobbered;
IF and DF are not changed. Near calls in the accepted boss/background and
stage-two owners independently corroborate this interface. Negative or already
out-of-range top coordinates are not made safe by this routine.

Native origin review supports genuine handwritten assembly through the full
hybrid interface, BX stack capture before saving registers, CH/CL counter and
rotation packing, BL/BH pixel carry and the three specialized string/VRAM loops.
This is distinct from the compiler-generated callers. Candidate ReC98
b6ba5b0a source/history describes a modern reconstruction; historical original
source text, original assembler identity and absence of vendor ancestry are
not proved. A bounded primary Master archive search found no whole routine;
its older sprite routines share techniques while differing in format,
interface, color/header handling and dynamic geometry. No vendor exclusion
extends beyond that search.

All instruction NOPs at relative offsets 95, 133, 157, 181, 221 and 259 align
row-loop or following procedure boundaries. The source uses EVEN for all six;
they compare normally with zero authored credit. There are no hardware-delay
NOPs, inserted instruction bytes or runtime placeholders.

Exact replay and explicit ownership adoption are separate gates. C/C++
acceptance, packed/whole executable equality and the global authored denominator
are not established by this review.

## Actual replay

Two independent positive producers match all 260 raw bytes and the empty ordered
fixup stream, with deterministic normalized OMF objects, MAP and MZ outputs.
The own negative changes the pixel-alignment mask from 7 to 6; it preserves
the complete extent, public boundaries, frames and fixup stream, changes byte
38 and is rejected. The binder supplies no initialized bytes, entry or stack.

The first normal invocation built and linked its source successfully, then
stopped because the native review omitted its DATA-frame metadata. That
original failed invocation remains archived. The continuation adds only
`ds_base = 209D0` to the review and retains the just-built first producer after
checking every source/verifier/tool identity and saved file. It compiles only
the second producer and negative. No source, ABI, binding, flag or assembler
output changes. The unchanged standard receipt validator rechecks both actual
positive producers and the negative; the receipt records this lineage.
Previously accepted units and the unchanged successful tool execution probe
are reused after their identity checks.

Receipt: `.analysis/asm-replays/main-super-roll-16x16-b/receipt.json`, SHA-256
`0e535f70fbf47975f6685b1cf998a8a2a96166338f8bb260b42180e6e05cedae`.
Independent native/source origin review:
`.analysis/super-roll-16x16-independent-origin-source-review.json`, SHA-256
`a65e511bac136f0743837232a5babe046d7182cc85b7dd7a253f77e7b56b8e4e`.

A separate native-only check compares 256 valid-input cases to an independent
MSB-first per-pixel model: all shifts and byte parities, top rows 0/384/385/399,
blank/full/alternating/generated patterns, blank-write omission and preserved
ABI state. It proves those cases, not unrestricted argument safety. Report:
`.analysis/super-roll-16x16-native-semantic-check.json`, SHA-256
`8e3628eae187f3553b3ad671b3a5e972c6552ac6108947d70e3d84d9d773ed9e`.

Independent actual-producer and continuation review:
`.analysis/super-roll-16x16-actual-continuation-independent-review.json`, SHA-256
`efc3b5b9c25326fb87209ea01284260cbd6e395f15398732418cac630c0a8e15`.
The explicit decision in `config/reviewed_asm_families.json` adopts only this
complete scope: 254 ASM instruction bytes and six uncredited alignment bytes.
