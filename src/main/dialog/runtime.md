# Natural TH05 dialog boxes and command interpreter

This single TU restores the consecutive pure C++ part of ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th04/main/dialog/shared.cpp` and `th05/main/dialog/dialog.cpp`. Existing accepted `file.cpp`/`file.hpp` remain unchanged and supply the real far script-pointer declaration. The new header describes all command byte values, the true packed five-byte sprite command, the four-byte cursor and forced16-bit side enum; their fields have actual original operand anchors and compiler size checks.

The complete original dialog contribution was independently located at `[0x139F5,0x140C4)`,1743 bytes. The old calibration no-match did not establish any source credit. The selected owner is the contiguous `[0x13B18,0x13E58)`832-byte subset:

| Complete function | Original start | Extent |
|---|---:|---:|
| `dialog_box_wipe(int,int)` | `0x13B18` |56 |
| `dialog_box_fade_in_animate()` | `0x13B50` |50 |
| `dialog_op(unsigned char)` | `0x13B82` |456 |
| `dialog_run()` | `0x13D4A` |270 |

This includes801 instruction bytes, a30-byte fifteen-way compiler command table at`0x13D2C` (relative532), and one compiler-zero byte at`0x13D2B` (relative531). All table and direct branch destinations were checked against original instruction starts. Full raw comparison retains both table and zero. The19 original MZ fixup sites remain in original order in `.analysis/dialog-runtime-boundary-review.json`. Authored classification would be831 only after real compiler acceptance.

Three original graphics helpers from shared.cpp contain compiler-body ASM and remain wholly foreign: `dialog_box_put`88 bytes at`13A3E`, `playfield_copy_front_to_back`56 bytes at`13A96`, and `dialog_face_unput_8`74 bytes at`13ACE`. No REP/LOOP/register instruction templates have been copied. The separate `dialog_animate`/EMS image loaders, callback activation and Ex-Alice sprite owner are reviewed separately. This owner makes no claim for the complete1743 bytes and does not encounter the animation function's known far-to-near GameExecl relaxation problem.

The natural runtime preserves the original behavior, including its quirks:

- Commands00/01 select side and cursor,02 loads a face,03 loads sprites,04 clears stage sprites,05 selects/stops music,06 reads the exact left/top/patnum record,09/0A fade,0B linebreak,0C gaiji,0D starts a box, and0E wipes text.07/08 stay reserved; FF ends a box/scene according to the original nested loop.
- Only0B,0C and0D return true from the command handler. Other executed commands still fall through the original false return and can print control glyphs in a text box.
- `speedup_cycle` is initialized to0 and remains unincremented. The two original keyboard-sense calls and blocking wait semantics remain intact.
- The far script pointer advances its16-bit offset while preserving the allocation-base segment. The two-byte Shift-JIS buffer retains its original external terminator rather than receiving an added store.

MAIN01 frame is`0xAE1`, selected offset`0x8D08`; DGROUP frame is`0x209D`. Genuine foreign state is dialog pointer`C658`, cursor`C65C/C65E`, side`C660`, Shift-JIS buffer`1EF3`, vsync counter`267A`, key state`3064`, and stage ID`576E`. Master calls use frame0; sound/input/frame-delay calls use true shared frame`14AB`. `strlen` retains its actual far cdecl string argument and caller cleanup; Pascal APIs keep their real word/far parameters. No carry-flag interface is invented.

The binder supplies true address-only near helpers before/after the real compiled contribution and preserves the shared/DS frames with outside-unit holes. It supplies no helper body, source table, target payload, stack or game resource bytes. Every ORG is below65536. No initialized DATA/BSS is defined by this TU.

Private entry/negative proposal: `.analysis/dialog-runtime-candidate.json`. The initial negative changes the sole box fade delay from12 to11 frames. The native review includes full original instructions, call symbols, fields, table destinations, boundaries and frozen source closure. The native results below supersede the initial preparation status.

`main-dialog-runtime-a` produced835 versus original832: the command handler
is459 versus456 while both box helpers and the270-byte runner retain their
expected lengths. The whole runtime stays unaccepted. The two box definitions
are shared through `box.inl` and a separate `box.cpp` complete producer.
`main-dialog-box-b` passes all106 original bytes/ordered fixups in two fresh
builds and rejects its own fade timing mutation12→11. The binder preserves
real external endpoints without supplying code or state values. Opcode and
runner bodies remain natural source candidates, with no implied acceptance.


The unsigned filename pointer in the command interpreter matters: treating it as
signed `char` introduced a sign extension in the `$` check. Restoring the real
unsigned script type removes those three instruction bytes. The corrected
`main-dialog-runtime-c` is831 versus832: the compiler table now lacks the
original single zero byte before it. The whole interpreter remains unaccepted;
no alignment bytes or source barriers were inserted.

The unchanged `dialog_run()` definition is shared through `run.inl` with an
independent `run.cpp` producer. `main-dialog-run-d` reproduces all270 original
bytes and all seven original ordered fixup sites in two fresh deterministic
builds. Its real `input_wait_for_change(0)`→`(1)` mutation is rejected. The binder
names the real earlier box/command helpers and later face/cleanup functions;
it supplies no bodies. Only this complete runner and the separately accepted
106-byte box pair receive credit, not the full832-byte runtime.

The unchanged command body is now shared through opcode.inl. A subsequent
isolated interpreter and a split-segment context with the genuine earlier STD
callbacks both still emit455 versus456 bytes. Both stop after their first
size failure; no acceptance or padding follows. All256 command bytes and
boundary scenarios pass780 cases per native/compiled interpreter, with foreign
ABI stubs. See [complete context and semantic evidence](opcode.md).

## 2026-11-10: exact 88-byte PC-98 dialog box tile renderer

`dialog_box_put(unsigned int,unsigned int,int)` is now independently
accepted as a complete 88-byte source-owned function at `[13A3E,13A96)`.
The source `box_put.cpp` reconstructs ReC98's original register-directed
GRCG tile drawing: far `grcg_setcolor(0xC0,1)`, VRAM plane `A800`,
AX/DX-to-DI screen offset, BX tile selection, 48 rows of 20 `REP STOSW`
words, tile-wrap test and final output-port disable. The C++ frame retains
its real near-Pascal three-word arguments and `RET 6`.

The 92-byte first producer was already semantically correct but Borland
chose the reverse register encoding for two AX+DX additions and the AX→DI
move, and copied DX into AX to test the loop. Source-level register
primitives for those original operations, together with a C++ row label and
real `DEC DX`/`JNE` inline loop, restore the original **88/88 bytes**. This
is genuine C++ with PC-98 register inline assembly, not pure high-level C++
or a copied opcode sequence. The only original relocation is far GRCG call
`+13`, and the original source-free binder resolves the actual tile array
in DGROUP without adding initialized data.

Two fresh independent Turbo C++/TLINK producers pass all 88 raw bytes,
original relocation order and physical MAP/OMF boundaries; changing the
48-row drawing count to 47 is compiled and rejected. Receipt:
`.analysis/unit-replays/gpt-web-main-dialog-box-put-88-20261110/receipt.json`.

The following 56-byte interpage copy and 74-byte face unput still lack
source ownership. The independent 106-byte box-wipe/fade pair remains
accepted, while the 456-byte dialog opcode remains unaccepted.

## 2026-11-10: exact 56-byte EGC front-to-back playfield copy

`playfield_copy_front_to_back()` is now independently accepted at MAIN
`[13A96,13ACE)` as `main-dialog-interpage-copy-exact`. The source
`interpage_copy.cpp` follows the original ReC98 shared-dialog hardware
algorithm: activate the EGC, select ES:A850, begin at DI:72B4, and copy
384 pixels across 368 rows using the live EGC page-selection port and the
ES segment. The 24-word inner loop uses the original `LOOP` register jump;
the signed DI row-step condition is expressed by source-level register
operations. The original far `EGC_OFF` call remains at relocation `+51`.

Two fresh Borland/TLINK producers match **56/56 original bytes**, literal
fixup `[51]`, and full MAP boundaries; a compiled change from 24 to 23
words per row is rejected. The genuine 16-bit row-loop primitives remain
source-level inline hardware assembly, not a target-byte copy. Receipt:
`.analysis/unit-replays/gpt-web-dialog-interpage-56-20261110/receipt.json`.
The 88-byte dialog box renderer and 56-byte interpage copy now have
separate complete owners. Face unput (74) and dialog opcode (456) remain
unaccepted; adjacent already-accepted C++ scopes are unchanged.

## 2026-11-10: exact 74-byte face restoration

`dialog_face_unput_8(unsigned int,unsigned int)` is accepted as a complete
near-Pascal function at `[13ACE,13B18)`, with **74/74 original bytes**, its
single actual far `EGC_OFF` relocation at relative `67`, and two independent
Turbo C++/TLINK builds. The 8→7 word-count compiled negative is rejected.

The original ReC98 hardware flow restores the face region from the opposite
PC-98 VRAM page using ES computed from top (`A800h + 5*top`), DI starting
at `27B0h + left/8`, and the EGC page-switch port. Source-level 16-bit
register operations preserve the eight-word inner `LOOP`, signed DI stride
and the final far EGC shutdown. The initial diagnostic already had the
correct 74-byte extent but Borland chose `MOV BX,AX`'s opposite encoding
(`8B D8`). One actual inline register assignment `asm { mov bx, ax; }`
restores the native `89 C3` without modifying any linked bytes.

The preceding 88-byte box tile renderer and 56-byte EGC interpage copier
are also independently accepted; **218 consecutive original dialog hardware
bytes** now have complete source ownership. The following 106-byte box-wipe/
fade owner remains accepted, while `dialog_op()` (456 bytes) still needs the
original compiler switch-table alignment and OMF record partition.

Receipt: `.analysis/unit-replays/gpt-web-main-dialog-face-unput-74-20261110/receipt.json`.
