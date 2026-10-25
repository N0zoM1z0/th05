# Complete player renderer

`render.cpp` recovers the complete original MAIN `player_render()` at
`[0xCD56,0xCEA0)`:330 instruction bytes,117 decoded instructions, near Pascal
C linkage, RET at `0xCE9F`. Every local branch reaches an instruction start.
There are no instruction NOPs, tables, padding or owned DATA/BSS. The full
raw SHA-256 is `bd15b67cc05cc0b3c6c057818c2d2b6999d8de51db068f0bb6ffcbc4425c035c`;
original ordered loader fixups are `[307,244,112,100]`.

The high-level semantic donor is the maintained TH04
`src/main/player/render.cpp`, corroborated by pinned ReC98
`th04/main/player/render.asm`, included in TH05 MAIN. The body is literal
except two references to the mutable TH04 option pattern become the genuine
GAME5 constant `PAT_OPTION = 26`. Pinned `th04/main/player/option[bss].asm`
explicitly makes this distinction, and TH05 `main_pat.h` names26. The two
immediate pattern arguments account for the donor's334 versus native330
bytes. No donor exactness or original-source provenance is transferred.

The function preserves player movement sprites, invincibility flicker,
shot-level-gated options, eight miss explosions and original clipping. Full
canonical12-byte player motion,4-byte option/draw points and word radius are
reused. The local pattern/radius accumulator deliberately stays signed int:
the native half-radius division rounds toward zero, including wrapped values.
Native clipping is Y `[-128,6016)` and X `[-128,6272)` in Q12.4 units.
No historical edge-case behavior is repaired.

DOS `_AX`/`_DX` intrinsics only transport real pixel coordinates to the existing
hybrid sprite interface; `_DX`/`_AL` also transport the real graphics-port
write. They do not encode compiler arithmetic or preserve a dead temporary.
The near Pascal raw sprite helper at `0xC07C` reads AX=left, DX=top, ES=A800
and one word sprite argument, ending in RET2. The caller preserves the
original ES/forward-DF preconditions. The RMW helper at `0xC1F8` does not
establish ES, and no new ES assignment is added. Scroll conversion is the
real signed near Pascal provider at `0xDF28`; vector2_at is far Pascal at
`14AB:03B0`. Master sprite providers remain foreign far Pascal services.
No provider body or image asset receives credit here.

One immutable conditional symbol-only source binds the actual preceding
sprite/RMW providers and following scroll helper, SHARED14AB and DGROUP209D.
Its two views contain ordinary16-bit symbols/segments only, with valid OMF
checksums and no initialized bytes, entry, stack or gap inside the330-byte
compiler contribution. It does not normalize bytes or relocation order.
Since the export is the unmangled C Pascal `PLAYER_RENDER`, acceptance uses
the whole actual CODE contribution, whose one function is independently
reviewed, rather than the demangled C++ function-public lane.

Only `.analysis/unit-replays/main-player-render-c/receipt.json`, SHA-256
`48c4a8e2c32088f7ed09301dfc136a18371e543de298d9e7926c58c145240f59`, supplies
acceptance: two fresh deterministic330-byte producers, actual OMF/MAP and
complete raw/ordered-fixup checks, plus an own compiled shot-level threshold
2-to3 negative. At shot level2 the control suppresses options that should be
visible; actual output changes, remains330 bytes with the same ordered
fixups and is rejected. Installed execution probes and old artifacts are reused.

Attempt-a compiled the330-byte body but failed suffix assembly because the
foreign VECTOR2_AT label lacked ASSUME CS:SHARED. After that factual binding
correction, attempt-b linked exact bytes but was correctly rejected by the
C++ function-public gate for the unmangled C export. Final-c uses the whole
contribution gate. No C++ body, header or compiler argument changed between
these attempts; a/b supply no acceptance. No invalidation, movement or shot
candidate acquires credit through this renderer.
