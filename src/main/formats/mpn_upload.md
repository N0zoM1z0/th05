# MAIN MPN two-page image upload: exact compiler-generated C++

`mpn_load(const char far *)` is the complete near-Pascal function at MAIN
`[E57C,E5C1)`: 69 instruction bytes, `RET 4`, and original ordered segment
relocations `[12,32,61]`. It loads the MPN bank through the real far Pascal
`mpn_load_inner`, draws four 16-pixel columns at X576..624 and 25 rows at
Y0..384 on each VRAM page, then frees the bank. The caller's parameter
remains a four-byte far pointer. The original return declaration is `int`,
but the body never assigns an AX result; this behavior is preserved.

The earlier high-level nested `for` loops compiled to 94 bytes, with a local
page/image frame, redundant entry checks, and `OUT DX,AL`. The current
`mpn_upload.cpp` retains the same algorithm as typed C++ and uses the real
Borland `_AL`, `_SI`, `_DI`, and `_BP` register interfaces. Two nested
`do-while` loops eliminate the original's nonexistent entry jumps. The only
inline assembly is the actual PC-98 page port, saving/restoring AX between
pages, and the flag-sensitive `DEC AL; JE page_begin` page-control pair.
No copied target bytes, filler function, added DATA/BSS, or repaired linked
output is involved.

A standalone Turbo C++ object now matches all 69 original bytes, but its
ordered MZ fixups are `[61,32,12]` rather than `[12,32,61]`. The existing
reconstruction toolchain's **unedited TCC `-S` output compiled by TASM32**
naturally produces both the exact bytes and the original ordered fixups.
This is a genuine Borland C++ source contribution, with only PC-98 register
hardware operations explicitly controlled, not an ASM origin claim. The
symbol-only binder preserves real `_TEXT` foreign helper positions and
MAIN01 `AE1` / DGROUP `209D` frames.

The focused exact receipt is
`.analysis/unit-replays/gpt-web-main-mpn-upload-exact-a/receipt.json`.
Two independent TCC/TASM32/TLINK producers match 69/69 raw bytes and the
literal ordered fixups; changing the vertical tile stride from 16 to 17 in
maintained C++ is compiled and rejected by the strict oracle. The native NOP
at `E5C1` is **outside** this function and earns no authored credit. Other
accepted MPN components (`mpn_free`, MPN drawing) and their inputs are unchanged.

The formerly unresolved `MPN_LOAD_INNER` (MAIN `41B2..420E`) now has its own
independently verified [92-byte reviewed ASM owner](mpn_loader.md). The game-
specific handwritten-ASM classification is inferred from the native DOS and
segment protocol, not claimed as recovered historical source. The earlier
origin challenge remains at `.analysis/mpn-load-inner-origin-challenge-review.json`.
Neither this 69-byte C++ wrapper nor the loader transfers source credit to the
other; both retain separate complete acceptance receipts.
