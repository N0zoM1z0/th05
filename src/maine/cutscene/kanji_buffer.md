# MAINE cutscene's writable two-byte Shift-JIS glyph buffer

The decoded MAINE interval `[1086A,1086D)` is exactly the original
three-byte `_CUTSCENE_KANJI` resource: a writable two-character buffer
initialized as `"  "` with a terminating NUL. The original
`_reference/ReC98/th03/cutscene/cutscene[data].asm` declares this
public symbol immediately after the five-stage `BOX_MASKS` coverage
bank. The separately accepted `script_op()` cutscene interpreter uses
the beginning of these bytes as a two-byte `ShiftJISKanji` field,
replacing its two characters when displaying inline script glyphs.
This is an actual dynamically updated text buffer, not a font image,
PI bitmap, copied target opcode or arbitrary anonymous zero state.

The natural C source exports `char near CUTSCENE_KANJI[3] = "  "` and
asserts its exact size. It owns no physical source beyond those three
bytes. The original `even` alignment zero at `[1086D,1086E)`, the
separate initialized `_page_shown` state at `[1086E,1086F)`, and its
following original alignment zero `[1086F,10870)` remain **unknown**;
none is charged to this compiler contribution. The next accepted
four-by-eight All Cast background pointer table begins at `10870`.

The source-free native binder preserves group_01 `A540`, SHARED
`E800`, and DGROUP `10110:075A` without copying or supplying any
candidate bytes. The scoped receipt
`.analysis/unit-replays/gpt-web-maine-cutscene-kanji-a/receipt.json`
passes two independent original Borland C producers, all three raw
bytes, complete OMF/LEDATA and MAP initialized-DATA scope, the empty
ordered original MZ fixups, and a rejected compiled mutation of the
second character to `X`. The source-level historical aggregate type
is not inferred merely from these three bytes; a separate future
consumer validation is appropriate before a full cross-TU claim.

## Canonical C public and original Shift-JIS consumer ABI (2026-11-12)

The independently exact C initializer now has a source-visible
C++ consumer with the same historical public identifier. The native
`cutscene.hpp` declares `extern "C" ShiftJISKanji near CUTSCENE_KANJI[]`
as a **two-byte glyph view** of the first two bytes in the already
accepted three-byte writable C allocation. The original
`cutscene_animate()` refers to `ShiftJISKanji& kanji = *CUTSCENE_KANJI`
without a new alias array, address literal, cast to a fabricated struct,
or copy. Its former function-local unqualified `extern` was eliminated.
This declares linkage of the actual C public, not that the original
Borland C source used the same aggregate type as the C++ consumer.

The shared cutscene header and interpreter source affect **ten accepted
MAINE native C++ scopes**. Their original whole-function bytes, 1555-byte
`script_op()` switch-table code, 479-byte `cutscene_animate()` body,
ordered MZ relocations and compiled meaningful semantic negative all
pass two Borland producer rounds in the focused receipt
`.analysis/unit-replays/gpt-web-maine-kanji-consumer-cpp-a/receipt.json`.

This source header is also pinned as a semantic review input for six
previously accepted original graphics ASM families: OP and MAINE EGC
rectangular copying, masked PI drawing, and palette/free PI drawing.
All **six** were individually replayed with their original native
boundary reviews, two pinned TASM/TLINK producers each and rejected
ASM semantic controls. Their actual producer records and explicit
adoption hashes were refreshed without changing a byte of those
hardware functions or their original reviewed ASM provenance. The six
receipts are in `.analysis/unit-replays/` under
`gpt-web-kanji-abi-asm-{op-egc,maine-egc,op-pimask,op-piplain,
maine-pimask,maine-piplain}-a/receipt.json`.

No additional initialized DATA or already-accepted CODE is credited
from this cross-translation-unit source link. No all-game cold replay
or unreviewed function adjustment is involved.
