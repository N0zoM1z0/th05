# Random-ring fill

The complete MAIN function `[C6E8,C700)` is24 instruction bytes in nine
instructions, with one original ordered MZ fixup at7. Its final near RET is
at C6FF; there is no table, NOP or padding. The real frame is AE1, DS209D.
The accepted stage-runtime initializer already calls this same near entry.

Natural C++ follows the maintained TH04
`src/main/math/randring_fill.cpp` donor and independently reviewed TH05 code.
It fills all256 bytes in descending index order, then clears the complete
word cursor. The ring and cursor remain foreign at DS3526 and3626. Their
256/2-byte declarations define no new storage or initialized DATA.

The actual vendor interface is `int pascal far IRand(void)`, at0000:23C6,
as corroborated by pinned ReC98 b6ba5b0a's master.hpp and RANDOM.ASM. The byte
array assignment performs the original AL truncation; the donor's narrower
byte-return declaration is not inherited. The ordinary signed register local
becomes SI naturally and retains the original signed loop exit. No physical
register arithmetic, inline ASM, opcode emission or padding is used.

Focused replay `.analysis/unit-replays/main-randring-fill-exact-b/receipt.json`
passes two deterministic builds, valid OMF/MAP ownership, all24 raw bytes and
the original relocation order `[7]`. Its compiled cursor-reset0-to1 mutation
is rejected. The binder supplies only real foreign addresses and extents,
with each ORG below64 KiB. Unchanged accepted units and installed execution
proofs are reused after identity checks.

Receipt SHA-256:
`ce145eab85cab6687b0bc844a12478f8d8879569aa3bbbfb37f32cd2a6fdfc12`.
Native extent SHA-256:
`54e7237b3382200c40f0e89200792bd1803b4e1a0e9a136f8586f347f03d61c2`.
Independent boundaries, actual calls and state are retained in
`.analysis/randring-fill-boundary-review.json`.

The earlier broad prefix survey omitted this short routine for insufficient
fixed bytes. That routing omission supplied no ownership decision. This adds
one complete C++ function and24 authored CODE bytes, without accepting any
ring accessor, BSS, vendor provider or whole executable.
