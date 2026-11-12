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
The C owner groups their byte arrays in one `GameoverGaijiBank` struct,
with explicit member offsets; this expresses the exact physically
adjacent data, but is not a claim about the original source's type or
complete standalone linkage of the separate historical labels. The
second three-byte blank caption and MAINE score-path filename are
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
