# Shinki stage backdrop fill routines

MAIN `[C68A,C6E8)` contains three adjacent PC-98 GRCG drawing procedures.
`shinki_stage_backdrop_colorfill()` draws the two stage background strips with
ES:DI set to the upper and lower playfield origins. `boss_bg_fill_col_0()`
and `shinki_bg_type_d_colorfill()` switch the GRCG to tile-direct mode, clear
all four color planes through port 7E and call the real near
`grcg_fill_playfield_rows` helper from the original locations 72B4 and 4AB4.
The callbacks save DI and preserve interrupt flags around mode changes. They
leave the caller's tile color and EAX register protocol as observed, without
introducing clipping, initialized graphic data or an invented helper body.

The source reuses the actual PC-98 VRAM segment and GRCG port constants,
with symbolic code labels and no copied instruction bytes. The independent
native reference is `ReC98/th05_main.asm` for the three Shinki/Boss backdrop
procedures and `th04/hardware/grcg_fill_rows.asm` for their separately
accepted row painter at MAIN `10600`. The native control flow is
register-directed assembly; this is reviewed original-ASM reconstruction, not
C++ attribution or proof of identical historical source spelling.

The whole 94-byte scope includes 93 real instructions bytes and one original
`EVEN` NOP at `C6A3`, before the second procedure. The NOP is compared but
excluded from authored ASM credit. No MZ relocation, switch table or owned
DATA/BSS occurs in this family; original caller boundaries stay distinct.

## Exact acceptance

The focused receipt at
`.analysis/asm-replays/gpt-web-main-shinki-backdrop-fills-a/receipt.json`
validates two independent TASM32/TLINK producers, all 94 native bytes, the
original empty relocation stream and complete OMF/MAP ownership. A semantic
negative changes the second stage-strip left address by one byte and is
rejected without altering the comparison. The original instruction and
source-origin review is
`.analysis/gpt-web-shinki-backdrop-fills-native-review.json`.

This adoption adds **93 authored original-ASM bytes**. The checked `EVEN`
NOP remains uncredited; the previously accepted `10600` row worker and all
other Boss bodies are unchanged.
