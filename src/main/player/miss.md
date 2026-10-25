# Player miss-state lifecycle

This natural C++ candidate recovers the complete original near function at
MAIN load `CB0A..CC3D`, 307 bytes. Maintained TH04
`src/main/player/update.cpp` supplies the semantic donor; ReC98's TH05
`sub_12017` corroborates TH05-specific behavior. The actual pinned original
determines the full function boundary, types, calls and operands. No compiler
acceptance transfers from the donor; the focused result is recorded below.

Every byte decodes through the final RET. The next separate player-update
function begins immediately at `CC3D`. There are no CODE tables, undecoded
gaps, source-owned initialized DATA or BSS. The original ordered relocation
list is `[94, 51]`. Native NOPs at offsets 84, 110, 159, 271 and 287 belong
to genuine same-CS far-call relaxation sequences and receive no authored
credit; all 307 bytes must still pass ordinary raw comparison. A future
complete match could credit 302 authored instruction bytes.

The helper decrements the death-animation clock, creates miss items and
reduces shot power by one quarter capped at 16. TH05 clamps performance to
38 before its real decrement-by-four interface. During the animation, dream
values above two decay by two during the Boss HP-fill phase or odd stage
frames; values at or below two become one. It updates the dream display,
expanding explosion radius and wrapped byte angle. The final four frames
flash the palette. Respawning restores position and upward velocity, consumes
a remaining life and resets bombs from the resident credit setting; otherwise
it calls the actual game-over runner and stores its byte quit result.

This uses the complete canonical `PlayfieldMotion`12, Boss24 and resident128.
The canonical byte `quit_t` enum is repeated identically without importing
startup's unrelated declaration segments. All other state is foreign. Dream
and angle changes use ordinary typed unsigned-byte arithmetic; no physical
register template, shortened object, fake callback, barrier or instruction
body is introduced. The TH04 donor's explicit `_AL` lifetime is not copied.

The symbol-only binder preserves actual CS `0AE1`, shared `14AB`, main_03
`1527`, and DS `209D`. Five true far providers retain their signatures and
explicit same-code-segment context; miss-item generation remains a real
cross-CS far call. All holes lie outside the whole compiler contribution;
there are no foreign instructions, literal values or artificial stack.

Private `.analysis/player-miss-boundary-review.json` records all instructions,
NOPs, original ordered fixups, globals, full source closure and helper ABIs.
`.analysis/player-miss-candidate.json` proposes one whole contribution and
a unique compiled negative lowering the real power-loss cap from 16 to 15.
Two fresh focused producers and that independent negative remain necessary.
The larger separate player-update function and previously parked movement,
invalidation and shot-update candidates are outside this packet.

Focused receipt `main-player-miss-a/receipt.json` passes both fresh producers
for all 307 bytes and the original ordered fixups `[94, 51]`. Its independently
compiled power-loss cap mutation from 16 to 15 is rejected. The root imported
one complete function and 302 authored instruction bytes, excluding all five
checked native NOPs. CPP, header and binder are now frozen accepted inputs.
