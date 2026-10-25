# HP bar drawer candidate

The complete original function is `[D28B,D323)`,152 instruction bytes in
MAIN's MZ program image. It is the actual far Pascal `hud_hp_put(int)`
drawer, distinct from the accepted main-03 HP animator. Its stack word is at
BP+6 and its return is RETF2. Three original ordered MZ fixups are `[145,126,78]`.
There are no NOPs, tables, DATA or BSS in this owner.

The maintained TH04 natural donor is `src/main/hud/hud.cpp`, with the same
initial `-G` option. The two full external aggregates are a nine-byte blank
string and five-byte color table; their fields are genuine complete byte
arrays. Ordinary const aggregate copies retain native local semantics:
blank at BP-0A and colors at BP-10. The data at DS13E2/13EB and five-byte
caption at13C4 remain foreign; no font/string bytes are copied into source.

The bar value remains a signed word and its color index ordinary signed
division by32. The true TH05 `hud_bar_put` at D474 is C near Pascal with three
word arguments. MASTER `gaiji_putsa` remains C far Pascal at0000:1DBE with
unsigned coordinates, a genuine far string pointer and unsigned attribute.
Automatic blank strings therefore use their real SS far addresses. Code
frame is AE1 and DS209D. No fabricated return convention or register bridge
is introduced, and accepted headers remain unchanged.

Original boundaries, full branches/calls and ordered fixups were independently
checked against locally attested MAIN, SHA-256
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`
`th04/main/hud/element_put.asm` is disassembly evidence only; its instruction
body is not transcribed. The source implements the maintained donor's C++
aggregate and conditional behavior.

The packet is uncompiled and unaccepted. Whole152 MAP/OMF extent, two fresh
raw/ordered comparisons and its own bar-row9-to10 negative are still required.
Private integration material is `.analysis/hud-draw-reset/`. The binder is
outside-only and supplies no owned instructions, values or artificial stack.
The adjacent full HUD initializer remains separate: its337 bytes include a
mandatory zero and eight table bytes plus internal relocation-order context,
so a blind standalone compile is not proposed.

## Accepted result

`main-hud-hp-draw-a` passes two fresh deterministic full152-byte comparisons,
the original ordered `[145,126,78]` fixups and OMF checks. Its own compiled
bar-row9-to10 control was rejected. This accepts this complete drawer alone;
the separate animator and full HUD initializer receive no transferred credit.
CPP, header and maintained binder are now frozen accepted dependencies.
