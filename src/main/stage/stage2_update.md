# Stage-two update and packed-return ABI

This standalone natural owner targets the complete original `stage2_update`
at `[0x118EC,0x11B79)`,653 instruction bytes, frame `0AE1`, group `main_01`.
Coordinates are MZ program-image offsets in locally attested MAIN, SHA-256
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
The original near RET is at `0x11B78`; every direct branch lands on an
original instruction start. There are no tables or padding. The three
original MZ fixups are at relative offsets `441,426,225`, in that order.
This owner defines no initialized DATA or BSS.

The source keeps the full transition, tile-ring, particle spawn/render and
palette-pulse algorithm. Only consumption of the real Motion return changes.
The complete canonical `PlayfieldMotion` still returns `PlayfieldPoint`;
no type, Motion method prototype, record field, calling convention or flag
is changed. One independent header linkage correction marks the existing
scroll conversion as `extern "C"`, matching the accepted overlay/render5
interfaces. Its int return, signed-word argument, Pascal near frame and
RET2 are unchanged. No earlier declaration inherited that C linkage in
this header include chain; the new binder uses the real C external name. The complete26-byte particle/custom record,12-byte Motion,
48-byte palette and1600-byte tile ring retain the complete layouts declared
by `background2.hpp`.

Actual original `update_seg1` at `[0xBE1A,0xBE3A)` and `update_seg3` at
`[0x1527C,0x1529C)` are the same32 bytes. They read one near-this stack
word, copy previous/current coordinates in the true Motion record and
return new X in AX and new Y in DX, then RET2. There is no hidden result
buffer or CF result protocol. Retained typed-result producers independently
show the compiler copying DX and AX directly into the real point local;
they do not reinterpret the result as a far pointer. Pinned ReC98
`th04/main/playfld.hpp` explicitly documents that some callers access the
returned coordinates through AX(X) and DX(Y).

The former named point was used only by four signed clipping comparisons.
The new source calls the same real method, then immediately reads its four
actual return-word uses through genuine DOS intrinsics and explicit signed
`subpixel_t` casts. Bounds remain x/y<=-128, x>=6272 and y>=6016. The code
neither assigns nor performs arithmetic on AX/DX. It adds no helper or
scalar/void return declaration. This is a limited external ABI unpacking
boundary, classified `compiler-generated-cxx-dos-intrinsics`; it is not a
translation of the compiler's algorithm into physical-register operations.

The result lifetime ends after clipping. The clipped path calls the real
foreign initializer only afterward. The surviving path subsequently sets
ES for actual VRAM drawing, overwriting AX after the result is dead, and
reads positions from the real Motion.cur fields. Its existing AX/CX/ES raw
graphics transport is unchanged. No return value is borrowed across the
initializer, graphics calls or ordinary arithmetic.

`stage2_update.cpp` is the single canonical complete function body, with a
guard around its initial compiler selector. The old unaccepted
`background2.cpp` now includes this body; its initializer prefix remains
byte-identical. The standalone owner compiles no initializer body or parent
contribution. The initializer at `0x11700` stays a genuine foreign near
Pascal reference API with RET2, whose raw external name was taken from the
retained actual compiler PUBDEF. No fake body, interior fill or padding
is supplied. The old natural initializer is still unaccepted and is not
claimed to match its original492-byte function.

Private integration inputs are `.analysis/stage2-update-abi-unit-proposal.json`,
`.analysis/stage2-update-abi-bindings.asm`, and
`.analysis/stage2-update-abi-boundary-review.json`. The reusable native ABI
review is `.analysis/motion-return-abi-review.json`. The negative lowers the
palette pulse peak from `0x3F` to `0x3E`, changing actual displayed colors.
The prior typed-local producer emitted664 bytes; that archived mismatch is
not accepted or normalized. Accepted focused replay `main-stage2-update-abi-a` proves two fresh
deterministic producers, all653 raw instruction bytes, the original three
ordered fixups `441,426,225`, and valid OMF. The compiled palette-peak
mutation `0x3F` to `0x3E` is rejected for this complete owner. Its receipt is
`.analysis/unit-replays/main-stage2-update-abi-a/receipt.json`. This acceptance
proves this genuine return-boundary bridge for the actual compiler context;
it does not accept the uncompiled initializer or other consumers. Source,
header and binder remain frozen.
No shot-update source was changed by this work.
