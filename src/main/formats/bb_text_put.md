# Bitmap text raw rendering: complete original-register ASM

The near fastcall `bb_txt_put_8_raw(unsigned int,unsigned int)` in TH05 MAIN
occupies `[E51A,E57C)`: 98 compared bytes, 96 original instructions and
two `EVEN` NOPs at relative offsets 39 and 97. The preceding `90` at
`E519` belongs to a different contribution and is excluded. There are no
native MZ relocation sites, compiler-generated switch tables, owned DATA or
BSS. This is a full register/stack ABI source owner, not a selected fragment
of the following MPN upload function.

The original procedure receives bitmap text coordinates in AX/DX and the
sprite index in CX. It converts 640-pixel PC-98 VRAM coordinates to ES:DI,
selects the 128-byte source cel through `SI`, and loads `DS` from the
foreign bitmap segment at original DS `19B0`. It copies exactly 32 raster
rows by DWORD, preserving blank rows and scrolling the destination by the
native 32,000-byte VRAM plane when rows cross the 400-line boundary. The
routine saves/restores the caller's original SI/DI/DS, preserving the
assumption that DF is clear rather than adding a new CLD.

The maintained source follows the explicit original-register ASM family
retained in pinned ReC98 `th04/formats/bb_txt_put.asm`, using named
screen/bitmap geometry and genuine `LODSD`/`STOSD`/`MOVSD` semantics. Native
instruction and public boundaries have been read independently against the
locally attested MAIN; original historical spelling and whole-executable
linkage remain unknown. The outside-only binder publishes no image bytes or
helper bodies.

## Exact adopted original-ASM result

`.analysis/asm-replays/gpt-web-main-bb-text-put-a/receipt.json` contains
two fresh deterministic TASM32/TLINK producers with complete **98/98 raw
byte equality**, empty ordered fixups and genuine MAP/OMF CODE and entry
boundaries. An independently assembled semantic negative changes the 32-row
no-roll copy to 31 rows and is rejected by the native oracle. Original
instruction/boundary evidence is stored at
`.analysis/gpt-web-bb-text-put-native-review.json`.

Explicit original-ASM adoption credits **96 instruction bytes**. Both actual
alignment NOPs are compared but uncredited. The following unaccepted MPN
upload, already accepted text resource lifecycle, and every older accepted
source dependency remain unchanged.
