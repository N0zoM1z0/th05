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

Three original graphics helpers from shared.cpp contain compiler-body ASM and remain wholly foreign: `dialog_box_put`88 bytes at`13A3E`, `playfield_copy_front_to_back`56 bytes at`13A96`, and `dialog_face_unput_8`74 bytes at`13ACE`. No REP/LOOP/register instruction templates have been copied. The separate `dialog_animate`/EMS image loaders, callback activation and Ex-Alice sprite owner also remain foreign. This owner makes no claim for the complete1743 bytes and does not encounter the animation function's known far-to-near GameExecl relaxation problem.

The natural runtime preserves the original behavior, including its quirks:

- Commands00/01 select side and cursor,02 loads a face,03 loads sprites,04 clears stage sprites,05 selects/stops music,06 reads the exact left/top/patnum record,09/0A fade,0B linebreak,0C gaiji,0D starts a box, and0E wipes text.07/08 stay reserved; FF ends a box/scene according to the original nested loop.
- Only0B,0C and0D return true from the command handler. Other executed commands still fall through the original false return and can print control glyphs in a text box.
- `speedup_cycle` is initialized to0 and remains unincremented. The two original keyboard-sense calls and blocking wait semantics remain intact.
- The far script pointer advances its16-bit offset while preserving the allocation-base segment. The two-byte Shift-JIS buffer retains its original external terminator rather than receiving an added store.

MAIN01 frame is`0xAE1`, selected offset`0x8D08`; DGROUP frame is`0x209D`. Genuine foreign state is dialog pointer`C658`, cursor`C65C/C65E`, side`C660`, Shift-JIS buffer`1EF3`, vsync counter`267A`, key state`3064`, and stage ID`576E`. Master calls use frame0; sound/input/frame-delay calls use true shared frame`14AB`. `strlen` retains its actual far cdecl string argument and caller cleanup; Pascal APIs keep their real word/far parameters. No carry-flag interface is invented.

The binder supplies true address-only near helpers before/after the real compiled contribution and preserves the shared/DS frames with outside-unit holes. It supplies no helper body, source table, target payload, stack or game resource bytes. Every ORG is below65536. No initialized DATA/BSS is defined by this TU.

Private entry/negative proposal: `.analysis/dialog-runtime-candidate.json`. The negative changes the sole box fade delay from12 to11 frames. The native review includes full original instructions, call symbols, fields, table destinations, boundaries and frozen source closure. This preparation has not run a compiler and does not claim exactness yet.

`main-dialog-runtime-a` produced835 versus original832: the command handler
is459 versus456 while both box helpers and the270-byte runner retain their
expected lengths. The whole runtime stays unaccepted. The two box definitions
are shared through `box.inl` and a separate `box.cpp` complete producer.
`main-dialog-box-b` passes all106 original bytes/ordered fixups in two fresh
builds and rejects its own fade timing mutation12→11. The binder preserves
real external endpoints without supplying code or state values. Opcode and
runner bodies remain natural source candidates, with no implied acceptance.
