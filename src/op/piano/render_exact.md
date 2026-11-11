# Exact Music Room PMD piano render

`piano_render()` at decoded OP `[D96E,D9E2)` is a complete 116-byte far
C++ function. It restores the PMD part work area through `LDS BX` while
keeping the original DS in FS, sets GRCG RMW mode, draws the SSG/blank
keyboard, then renders all five FM parts and two SSG notes using the genuine
near piano helper functions. The updated note identifiers travel through
BX, SI and AL, with no reconstructed sprite/font data. The original DS/SI/DI
save/restore sequence and `RETF` are preserved.

The maintained C++ follows pinned ReC98 `th05/op/piano_c.cpp`. It uses the
real `PmdPart` type and 18-pixel-spaced piano geometry, plus Borland
register intrinsics for the original fastcall helpers. TCC `-S` produces the
actual 386 `POP FS` instruction for TASM32. The first part's `SI=0` is
expressed as semantic inline `MOV SI,0` because Turbo C++ otherwise chooses
the shorter `XOR SI,SI`, shifting every later call by one byte. No instruction
byte sequence is emitted or patched.

The isolated linker binder uses a proof-only same-CS group for the external
near helpers, as with the separately accepted [218-byte piano initializer]
(setup_exact.md). Both functions' actual segment addresses and the runtime
CS frame stay at `D300`; the binder defines only foreign symbols and DATA
positions, not provider instructions. The existing ASM keyboard, FM wrapper,
label and pressed-key functions retain their independent accepted ownership.

Focused receipt:
`.analysis/unit-replays/gpt-web-op-piano-render-116-a/receipt.json`.
Two independent TCC `-S`/TASM32/TLINK builds match all 116 native bytes,
the original empty ordered relocation stream, original MAP/OMF CODE scope,
and their source dependencies. The semantic negative changes piano highlight
color from 5 to 4 and is compiled and rejected. This adds one full C++
function without rebuilding or double-counting its previously accepted
providers.
