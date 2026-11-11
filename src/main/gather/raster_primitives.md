# Main 03 Gather raster and GRCG color primitives

The native MAIN interval `[15312,1538C)` contains three complete near
assembly interfaces. `GATHER_GRCG_COLOR_DIRECT` accepts an AH color nibble,
shifts four bits through carry and writes each resulting full tile byte to
GRCG port 7E while interrupts are disabled. `GATHER_GRCG_MODE_RMW` enables
the 0C0h read-modify-write mode at port 7C. The 90-byte fastcall
`gather_point_render(int left,int top)` uses AX/DX coordinates and the
foreign shifted-pellet mask bank at DS `0E4A`, choosing a byte or WORD copy
for eight raster rows and wrapping across the 400-line/32,000-byte VRAM
plane. It preserves SI/DI, relies on clear DF and a caller-selected ES
plane, and owns no bitmap values.

The high-level semantics and original-register source structure are retained
in pinned ReC98 `th04/hardware/grcg_modecol.asm` and
`th04/main/gather_point_render.asm`, with the native MAIN `main_03` code at
CS `1527` and DGROUP `209D`. The source uses named geometric constants and
symbolic branches. The preceding `15311` NOP and the accepted enemy-VM
interpreter that begins at `1538C` remain external. Inside the 122-byte
family, alignment NOPs at `15331` and `1536D` are compared but receive zero
authored credit. There are no module relocation sites or owned DATA/BSS.

## Accepted focused source

`.analysis/asm-replays/gpt-web-main-gather-raster-a/receipt.json`
records two fresh deterministic TASM32/TLINK producers, all 122 native
bytes, original public boundaries and empty relocation stream. The source
mutation that shortens the eight-raster-row renderer by one row is assembled
and rejected by the full native comparison. The original instruction record
is `.analysis/gpt-web-main-gather-raster-native-review.json`.

Explicit reviewed ASM credit is **120 instruction bytes**. Two `EVEN`
NOPs are verified but uncredited; no accepted enemy-VM or graphics provider
is recompiled or double counted.
