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
