# TH05 .TX2 dialog-file loader candidate

Natural source follows ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05/f_dialog.cpp` → `th05/formats/dialog.cpp` and its format header. The owner keeps the real ten-byte TX2 header, four playable characters plus the terminal file offset, and the large-model master.lib ABI. Allocation returns a segment handle; the far dialog pointer retains that segment for later freeing. No carry-flag convention is inferred or introduced.

The original target was decoded independently, after the calibration match supplied only routing:

| Complete function | Original start | Size |
|---|---:|---:|
| `dialog_load(const char far*)`, Pascal far | `0x1392B` | 144 |
| `dialog_load()`, near | `0x139BB` | 27 |
| `dialog_free()`, near | `0x139D6` | 31 |

The whole contribution is `[0x1392B,0x139F5)`,202 instruction bytes,70 instructions, no tables and no padding. Its eight original MZ fixup sites remain ordered as relative offsets `189,137,132,121,84,41,29,20`. The first function ends with `RETF4`, corroborating the real far filename argument; the other two end with near `RET`. The internal overload call is generated from a real same-TU far C++ declaration and definition.

MAIN01 frame is `0xAE1`, original DGROUP frame `0x209D`. True globals are `dialog_fn` at DS`0x1ECC`, stage ID at`0x576E`, player character at`0x5773`, and `dialog_p` at`0xC658`. They remain extern; this owner defines zero DATA/BSS bytes. The symbol-only binder anchors master.lib calls in frame0 and uses only external ORG gaps; there are no helper bodies, initializers, stack allocation, original target bytes or ABI shims.

The private `.analysis/dialog-file-boundary-review.json` records full original instruction/boundary/call/fixup/source evidence. `.analysis/demo-dialog-candidates.json` supplies the whole-TU registration proposal and a natural negative that changes the stage filename digit base from`'0'` to`'1'`. `main-dialog-file-a` now passes both independent complete raw/ordered
producers and rejects that compiled filename mutation. All202 instruction
bytes are accepted; no DATA or BSS is credited.
