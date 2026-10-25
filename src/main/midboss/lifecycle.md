# Complete midboss defeat update in its local source family

The new `lifecycle.cpp` preserves six complete natural TH05 functions in
native order: reset35, activation50, HP interpolation88, midboss bonus106,
boss bonus112 and defeat65. The existing maintained TH04 `midboss.cpp` has
this same coherent family order. Pinned ReC98 `th04/main/midboss/defeat.cpp`
explicitly states that its manual call should become the ordinary typed
`midboss_reset()` when the provider shares the translation unit. That
source evidence supports this context independently of the desired size.
All six TH05 bodies are literal copies of maintained state/HP/default bodies;
the GAME5 phase, shake and activation differences are preserved.

Only complete `midboss_defeat_update()` at MAIN `[0x1C628,0x1C669)`,65 bytes,
is newly accepted. It is near cdecl, ends in RET at `0x1C668`, and contains
no instruction NOPs, tables, padding, MZ fixups or owned DATA/BSS. Its raw
SHA-256 is
`202aef40873c342dea624fd5cc27fe33f452cedb69549640acb04c8017ece5b1`.
The four-byte call at `0x1C663` is genuine compiler-generated PUSH CS/CALL
near, reaching the real far-cdecl `midboss_reset()` at `0x1C4A1` with RETF.
No samecodeseg directive, assembly body, opcode template, padding or byte
normalization supplies it. The previous external call's66-byte function
and extra loader fixup remain failed artifacts.

The complete source family `[0x1C4A1,0x1C669)` is456 bytes,164 decoded
instructions, with no NOPs/tables. Both new producers also match its entire
raw SHA-256 `8a62d53b77fb570e1a19c3852c4ae22e5e793e8dd728c7b33ac044b1f7f391a0`
and original ordered fixups `[165,19]`. This is additional context evidence,
not391 new credited bytes. Four older accepted rows cover that391-byte
prefix and remain unchanged, including their source/header/object identities.

`lifecycle.hpp` reuses canonical complete22-byte midboss,24-byte Boss and
callback types. Own functions and RNG first declarations use the real
main_03 frame1527; null/invalidate callbacks and far HP output retain the
actual main_01 frameAE1. The compiler definitions form one real public CODE
contribution. Symbol-only bindings provide actual outside endpoints and
DGROUP209D, with no initialized values, helper body, stack, entry or gap
inside the compiler contribution. All individual ORGs are below64KiB.

Only `.analysis/unit-replays/main-midboss-lifecycle-local-a/receipt.json`,
SHA-256 `965831477802a74492291d00df9f015b8475aba9e2fbd8744d7a5ccc8ef03d27`,
supplies acceptance. Two fresh deterministic producers, actual OMF/MAP and
full raw/ordered-fixup comparison pass. The function's own compiled negative
changes the explosion activation test from phase frame1 to2, changing when
shake and inactive state are published. The complete65-byte output changes
and is rejected. Installed tool execution probes and unrelated accepted
objects are reused; no whole-cohort rebuild or whole-executable claim occurs.
