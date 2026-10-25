# EX-Alice firewave renderer candidate

The complete custom-bullet renderer occupies `[11B79,11CAD)` (308 bytes) in
near `main_01` frame `0AE1`. Native review decodes all 117 instructions,
validates the real return and all 17 direct branches, and finds no table or
padding. The already accepted EX-Alice foreground begins at `11CAD` and remains
outside this owner.

The source iterates the two real firewaves. Each live wave's bottom coordinate
determines its initial half-angle and 16-pixel-aligned band. Bands step upward
while their phase advances through the half-sine. The actual amplitude and
external sine table feed the genuine far Pascal polar API. Left and right waves
fill the appropriate VRAM byte columns, apply the real player collision tests,
and draw their 168/169 edge sprites. The complete renderer then calls the real
foreign cheeto renderer.

Player coordinates retain signed `/ 16` rounding. The vertical band test keeps
the original unsigned 16-bit difference, and left/right horizontal comparisons
remain asymmetric. No returned-point temporary or flag-returning custom ABI is
introduced. The player uses its canonical full motion structure.

The complete six-byte `firewave_t` is token-identical to the accepted natural
`firewaves.cpp` owner's definition: two bool bytes, signed bottom and amplitude.
That owner has no shared type header, so this header repeats the full identical
ODR definition without editing accepted source. Private evidence checks all
tokens and offsets. The two actual objects remain external at DS `4A90`;
player motion is at `36D2`, its hit byte at `36F3`, and the canonical external
sine table at `041C`. No table or asset values are copied into source.

The accepted explosion header supplies the actual tiny-sprite wrapper, with
AX=left and DX=top. Setting ES to VRAM segment `A800` immediately before that
foreign call is a real PC-98 rendering requirement, not a register-allocation
hint for ordinary C++ arithmetic. The far GRCG byte-box API, far polar API and
near cheeto consumer retain their real frames and cleanup. No assembler, emits,
instruction arrays, stand-in helper bodies or register forcing is present.

Original ordered fixups are `[211,144,82]`. Calibration supplies a unique full
instruction-body route only; acceptance must compare all raw bytes and this
original stream without sorting. The independent symbol-only binder places
actual foreign symbols and outside-only holes. Its fixed tail is valid only
after actual OMF confirms the complete 308-byte compiler contribution.

Private `.analysis/exalice-custom-render-boundary-review.json` records native
boundaries, branches, calls, full-type identity, hashes and ABI evidence.
`.analysis/exalice-custom-render-unit-proposal.json` proposes the whole owner
and a meaningful phase-step negative, 8 to 9.
`python3 .analysis/exalice-custom-render-review.py` repeats the bounded native
review. This source is uncompiled and unaccepted; a focused two-producer replay,
raw/original-ordered-fixup agreement, OMF/MAP/dependency gates and rejected own
control remain required.

The first focused replay `main-exalice-custom-render-a` passed two fresh
complete 308-byte producers, full raw bytes, the original ordered fixups
`[211,144,82]`, and the own phase-step 8-to-9 negative control. The root imported
the whole renderer. Its source, complete ABI header and independent binder are
now frozen accepted inputs.
