# MAIN Game Over / Continue gaiji text bank

The complete original MAIN `[21E1A,21E40)` region is now **38 bytes**
of source-level semantic initialized DATA. It contains five individually
sized gaiji string records in original order: GAME OVER (10 bytes),
CONTINUE? (11), YES (4), NO (3) and CREDIT (7), followed by a three-byte
two-space erase caption. The game UI's glyph selectors are not screen
pixels; `HG_BOLD_*` refers to the canonical bold gaiji alphabet defined
in the already accepted `overlay_data.h`. The question symbol is the
original special gaiji selector 8, **not** the ASCII question mark.
Both doubled NUL terminators after the first two words are preserved
because the original source has them.

The original table is shown in
`_reference/ReC98/th04/gaiji/gameover[data].asm`, included by
`_reference/ReC98/th05_main.asm`, with the following `asc_226B3`
blank-caption record. The accepted `src/main/runtime/gameover.cpp`
consumes the five named semantic phrases in the original continue menu.
The C owner now emits **six independently addressable, mutable C objects**
with the original real public names `gGAMEOVER`, `gCONTINUE_QUESTION`,
`gYES`, `gNO`, `gCREDIT`, and `gameover_erase_in`. These match the accepted
Game Over renderer's exact source-level external symbol dependencies; the
renderer may use a read-only `const char` view while the historical glyph
storage itself is writable. The individual publics are located by the
native linker at DS `144A`, `1454`, `145F`, `1463`, `1466`, and `146D`,
respectively. This removes the earlier unlinked aggregate placeholder.
The second three-byte blank caption and MAINE score-path filename are
separately accepted at `[21E40,21E49)`.

The outside-only binder preserves MAIN01/MAIN03 and shared segment
frames and places the C contribution at DS `209D:144A`. It supplies no
initialized glyphs or original executable code. Both native Borland C
producers in the bounded receipt
`.analysis/unit-replays/gpt-web-main-gameover-gaiji-a/receipt.json`
match all 38 original bytes and full OMF/MAP DATA boundaries, with an
empty ordered MZ fixup list. A compiled mutation changing the CREDIT
word's D glyph to E is rejected. No unrelated or full-program replay
was executed.

## Compiler-generated public order after canonical C declarations (2026-11-12)

A first attempt defined the five text arrays as `const`. Borland emitted
the **writable** blank string at the beginning of `_DATA`, moving the
five const arrays to later addresses; the 38-byte raw comparison failed.
The corrected natural C declarations use `char near` for all six objects,
which makes Borland emit the exact original record order and all six
independent public symbols without a packed struct, copied bytes or linker
padding. Both original DATA bytes and complete MAP/OMF boundaries match.
The mutation of the CREDIT glyph is still compiled and rejected.
The focused receipt is
`.analysis/unit-replays/gpt-web-gameover-canonical-publics-c/receipt.json`;
no other accepted unit was rerun for this source-only physical ABI change.


The direct C definitions also have the same byte-element type as the
C++ game-over consumer's `char near[]` declarations. The independent
complete **869-byte** Game Over control and Continue menu remain
raw/ordered-fixup exact with these canonical symbols and the compiled
credits-count mutation rejected; receipt:
`.analysis/unit-replays/gpt-web-gameover-canonical-consumer-a/receipt.json`.
