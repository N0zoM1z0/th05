# Mima bomb draw and retained full context

Accepted complete scope `mima_bomb_draw` contributes205 instruction bytes.
Its maintained natural C++ producer contains the actual consecutive MAIN functions
`mima_bomb_draw` at `[0x1010D,0x101DA)` (205 bytes) and `bomb_mima` at
`[0x101DA,0x1027B)` (161 bytes). Coordinates are offsets in the unrelocated
MZ program image of locally attested MAIN, SHA-256
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
Both functions use frame `0AE1`, group `main_01`, and end with their actual
near RET. All366 bytes are instructions; no padding or CODE-data table is
present. Every local branch destination is an original instruction start.

The actual original fourteen MZ relocations, in original order, are at
owner-relative offsets
`260,232,178,142,128,115,101,83,69,56,42,29,15,340`.
A strict replay must reproduce that order naturally. No relocation list is
sorted or patched. Earlier standalone control evidence has raw-equal161-byte
payloads but a different relocation order: original `55,27,135`, candidate
`135,55,27`. That failed parent remains unaccepted and preserved.

The new draw source places the existing control source directly afterward,
using the real adjacent function definitions. Its only edit to the control
file is a combined-mode guard around the initial segment pragma. From the
first include onward, the saved standalone source and current source are
byte-identical; removing the two added guard lines restores the complete
saved file. The standalone producer still sees the same initial pragma.
There are no artificial helper functions, inside-owner gaps, filler or
ordering variants. Both fresh full366-byte producers match raw bytes, but the final control
relocation remains first in the candidate instead of last in the original.
The full cohort and control161 remain unaccepted, with zero credit for the
control body; no order is normalized or patched.

Draw blits the existing background CDG, invokes the real foreign custom VRAM
backdrop helper at `0x1052C`, and draws the original eight vertical border
segments using the master.lib far-Pascal API. The first four use color7 at
x209/238; the second four use color6 at x208/239, with top/bottom ranges
16..63 and336..383. Color changes through `grcg_setcolor_direct_raw` use
AH only because AH is that actual hardware API's input, already documented
by the unchanged accepted overlay interface. No compiler arithmetic is
translated into pseudo-register operations.

The unchanged accepted181-byte `mima_circles_update_and_render` callback at
`0x10058` remains foreign. Its full canonical header retains the480-byte
bomb union, eight complete ten-byte Mima circle records and genuine player
motion ABI. This owner duplicates no record layout and does not re-credit
that callback. The outer circle uses signed word radius `224-bomb_frame`,
checks positivity, and passes a word radius to the real master circle API.
GRCG is disabled with the ordinary DOS `outportb(0x7C,0)` intrinsic, then
palette tone becomes `100+bomb_frame` and its dirty flag is set.

Hardware prototypes follow the actual canonical interfaces:
`grcg_setcolor(int,vc2)` with unsigned-word `vc2`, three signed-word vertical
line coordinates, and signed center/unsigned-word radius for `grcg_circle`.
The foreign backdrop's custom VRAM implementation is not copied or
credited. The control body preserves its real active background slot at
DS:`3508`, separately from the callback template at DS:`350A`.

ReC98 `b6ba5b0a`'s `th05_main.asm` lines2074-2186 supplies semantic and
disassembly evidence; actual original boundaries, operands, calls and
relocation order were reviewed independently. The reconstructed source
contains no instruction transcription, asset array, emitted byte, flag
barrier or invented ABI.

Private integration inputs are `.analysis/mima-bomb-full-unit-proposal.json`,
`.analysis/mima-bomb-full-bindings.asm`, and
`.analysis/mima-bomb-full-boundary-review.json`. The symbol-only binder
supplies foreign entry/state addresses, no helper bodies or resource values.
The owner-level negative changes the outer-circle radius constant224 to223.
The draw205 complete-function scope is accepted by
`.analysis/unit-replays/main-mima-bomb-draw-a/receipt.json`. It reuses the two
retained fresh producers from the preserved failed whole-cohort parent,
with zero additional compiler invocations. The scoped real payloads match
the original raw205 bytes and ordered eleven fixups, and the retained
compiled radius224-to223 mutation is rejected in that same scope. Actual
target/source identities, retained MZ payloads and ordered fixups, and the
parent receipt hash were independently rechecked before this note.

The complete-function boundary is the real next function `bomb_mima()` at
`0x101DA`; no interior successful fragment is substituted. The failed
whole366 parent stays preserved and no acceptance transfers to control161.
This packet owns no initialized DATA or BSS.
