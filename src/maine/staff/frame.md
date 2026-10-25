# Staff frame pump

Current canonical bodies and producer choices are documented in
[full.md](full.md). Earlier standalone diagnostics and controls below remain
historical evidence; they are not relabelled as fresh compilation.

This accepted owner is the complete near procedure at original decoded MAINE
`E34E..E3A4`: 86 bytes, 30 instructions, final near RET, no instruction NOPs,
padding or CODE data tables. Original ordered MZ fixup offsets are **[60, 46,
14]**. `maine-staff-frame-a` passes both fresh deterministic producers, all86 raw
bytes and the original ordered fixups. Its own compiled wait1-to-2 control is
rejected.

The candidate reference is `ReC98/th05_maine.asm` lines 5434–5465, named
`sub_E349`. Its old address is five bytes before the actual original function.
Native original operands independently identify the renderer at `DFF1`, also
five bytes after old `sub_DFEC`, while the particle updater remains at `D5E1`.
The local difference is not applied as a general address conversion. Full
instruction coverage, both internal branches, near return and all provider
addresses are recorded in the private native review.

The procedure updates particles, renders the scene, waits one frame, selects
the access page, flips the existing alternating page and displays it. A pending
text-clear request is serviced once and reset. It then increments the canonical
signed frame counter and queries the music measure. When the genuine music
query returns a negative value, signed frame division by 22 supplies the silent
fallback measure. No CF-return or aggregate-return helper is invented.

The header reuses unchanged `lifecycle.hpp` and its `staff_back_page` byte at
DS `1011:173A`, `staff_frame` word at `1011:50E2`, and true first declaration
of the near particle updater in `STAFF_LIFE_TEXT/group_01`. Shared phase APIs
use the agreed `staff_text_clear_requested` byte at `1746` and signed
`staff_bgm_measure` word at `50E0`; no same-address replacement globals or
storage definitions are introduced. `staff_scene_render()` declares the real
near scene provider at `DFF1` in `STAFF_DRAW_TEXT/group_01`; that foreign body
is not accepted by this candidate.

`frame_delay(int)` is far Pascal at `0E80:0A88`, with the actual original
`RETF 2` cleanup. `text_clear()` is C-linkage far Pascal at `0000:2298`,
ending in `RETF`. The signed-int, no-argument far cdecl music query is at
`0E80:0A42`. Its canonical accepted C++ owner exports the actual OMF symbol
`@snd_bgm_measure$qv`; the older reference ASM calls it `_snd_bgm_measure`.
The maintained declaration uses the canonical provider name and matching real
physical ABI. Original hardware access is expressed through Borland's genuine
`outportb()` intrinsics for ports `A6h` and `A4h`.

The binder provides only real foreign labels and origin holes outside the
complete 86-byte contribution. Each empty foreign source segment retains its
actual group context. No prior updater, renderer, foreign DATA or layout hole
receives authored credit. The proposed own negative changes the real frame
wait from one to two; raw bytes and original ordered fixups still require two
fresh deterministic producers. Private replayable native review and the
unit/control proposal are under `.analysis/maine-staff-frame/`.
