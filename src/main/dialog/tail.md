# Natural TH05 dialog animation, face cache and exit

One C++ TU restores the last four functions of ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05/main/dialog/dialog.cpp`. It reuses the complete accepted EMS/CDG16 and resident headers plus the real replay-buffer types from demo.hpp. It does not include runtime.hpp/file.hpp, avoiding the independent byte/enum declarations of the global player character. No accepted header is modified.

Original complete boundaries were independently decoded:

| Function | Original load start | Extent | Real ABI |
|---|---:|---:|---|
| `dialog_animate()` | `13E58` |183 | far cdecl, RETF |
| `dialog_face_load_unput_put_free_8` | `13F0F` |248 | near Pascal, three words, RET6 |
| `dialog_exit()` | `14007` |122 | near cdecl |
| `main_pat_exalice_override_and_super_clean_stage` | `14081` |67 | near cdecl |

The original range `[13E58,140C4)` totals620 bytes. Its four-word character-selection switch table is `[14079,14081)`, tail-relative545, preceded by the compiler-zero byte at relative544. The original GameExecl relaxed call also has a NOP padding byte at`13ED0`, relative120. Full raw comparison retains both padding bytes; potential authored classification is618 code,610 instruction and8 compiler-table bytes. There are27 original ordered MZ fixups. Every direct branch and table destination was checked against an actual original instruction start.

The source keeps the real semantics:

- Extra replay pre-boss handling loads the Ex-Alice sprites/music and the second40000-byte replay chunk, resets the actual frame index and advances the signed-byte sequence ID. Its post-boss path frees the real segment handle, fades, then calls the real far GameExecl API.
- Ordinary animation removes the bomb background, prepares the overlay/palette/page, fades boxes, copies the playfield through the genuine foreign graphics helper, runs dialog, restores the bomb background and switches access page back. The two VRAM page writes use ordinary `outportb(0xA6,page)` intrinsics; no register loop or manually emitted instruction is present.
- Face loading uses the complete CDG16 fields at slot2: bitplane size DS`308C`, alpha segment`3098`, color segment`309A`. The original16-bit product `face_id * size *5` is preserved before adding to the32-bit EMS offset. Allocation, alpha/color transfers, the unused final offset update, disk fallback, one-frame delay, genuine unblit and optional put/free remain in their original order.
- Exit restores CDG slot0 from EMS offset34000 or selects one of four external bomb background filenames. The late sprite owner frees the real `[36,320)` pattern range, reloads Ex-Alice data, converts tiny patterns`36..171` and selects the real character-specific bomb shape.

All filenames and data remain external symbols, including the mutable faceset templates. This owner defines no initialized DATA or BSS and includes no resource, script, image or opaque byte-array payload. The master declarations preserve real return types, including `int super_entry_bfnt` and `int super_convert_tiny`.

The first new declarations restore DIALOG_TAIL_TEXT after demo.hpp's genuine code-context directives. The binder retains those empty context names, binds the real earlier GameExecl far public at load`CEC2` in the same combined CODE context, and supplies only labels/ORG ranges. The actual callee returns `RETF4` at`CF5E`; no false near declaration or handwritten call is used. Whether TLINK performs the original relaxation is an actual-producer question. The original exit table is at an odd offset relative to this new TU, so compiler padding may also differ. The packet neither injects padding nor promises620 before a real build.

MAIN01 is frame`0AE1`, selected offset`9048`; DGROUP is`209D`. Master calls use frame0 and CDG/sound/frame-delay calls use real shared frame`14AB`. Every binder ORG value is below65536; no `.stack`, helper body or target value is supplied.

Private evidence: `.analysis/dialog-tail-boundary-review.json`. Entry/control/SHA proposal: `.analysis/dialog-tail-candidate.json`. The default negative changes the actual demo-return fade speed from8 to7; additional per-function negatives are listed only as future scope options. No compiler or heavy analysis was run for this preparation, and no exact acceptance is claimed.

## Actual producer result

The first real producer `main-dialog-tail-b` emitted619 bytes. Native complete-function review found the face loader248 bytes and Ex-Alice override67 bytes both raw and original ordered-fixup exact. Two fresh scoped producers and their compiled controls subsequently passed and those315 bytes were accepted in `main-dialog-tail-scopes-c`; this does not accept the complete tail.

`dialog_exit` is121 rather than122: its113 instruction bytes are identical except the genuine switch-table base operand at function-relative71, the eight table bytes are identical, and the original intervening zero is absent. The later Ex-Alice body therefore starts at actual`14080`, one byte before its original`14081`, while its complete relative bytes/fixups remain exact. `dialog_animate` stays183 bytes but fails raw and ordered fixups. Its only raw differences are tail-relative22 (its near call reaches the actual Ex-Alice address`14080`) and120..124 (actual `9A B2 20 E1 0A`, a genuine far call to`0AE1:20B2`, versus original relaxed `90 0E E8 ED 8F`). The far call also adds an MZ fixup at relative123. No other animation bytes differ. No source variant or padding/opcode template was introduced to fix either parked function.

## Later complete animation acceptance

The separate literal-body `animate.cpp` now accepts all183 animation bytes
with182 authored instructions and one checked relaxation NOP. It preserves
the real far Pascal GameExecl API and states its independently proven same-CS
context, while binding later foreign helpers to their actual native addresses.
See [complete dialog animation](animate.md). The original315 accepted bytes,
source/header and old mixed results above remain unchanged; the122-byte exit
switch owner is still unaccepted and receives no transferred credit.
