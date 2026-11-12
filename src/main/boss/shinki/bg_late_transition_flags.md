# MAIN Shinki C/D and EX-Alice hexagram: three real independent state bytes

The complete original MAIN `[22360,22363)` contains three adjacent
initialized near-C publics, each one byte wide and originally zero:
`shinki_bg_type_c_initialized` at `22360`,
`shinki_bg_type_d_initialized` at `22361`, and `hexagrams_flag` at
`22362`. The original `th05_main.asm` declares all three separately.
The C-stage initialization flag changes when B-type falling particles
are converted into upward motion, the D-stage flag changes after
smoke-particle setup, and EX-Alice uses its independent hexagram flag
as the three-state uninitialized/clockwise/counterclockwise selector.
These are source-level mutable gameplay state, not graphics bitmaps,
compiler switch tables, or arbitrary zero-filled storage.

A natural Borland C source defines all three **independently named
unsigned byte objects**, without inserting any compiler padding between
them, while asserting their individual and combined widths. Its
symbol-free binder preserves the actual MAIN code group frames and
only the original DGROUP prefix `209D:1990`. It contributes no candidate
bytes, original C++ machine instructions or fake relocation records.
No claim is made that the original program historically grouped the
three source declarations in a single translation unit; the bounded
native proof establishes the 3-byte initialized-DATA contribution and
its C public names. The following original alignment byte at `22363`
and the remaining unclassified bytes up to the next accepted table
remain UNKNOWN.

Two independent pinned Turbo/Borland C producers exactly reproduce the
whole three-byte initialized record, its original OMF/LEDATA/MAP extent,
raw bytes and empty ordered DOS MZ relocation sequence. A compiled
mutation changing **only** `hexagrams_flag` from zero to one is rejected.
Focused receipt:
`.analysis/unit-replays/gpt-web-shinki-bg-late-flags-a/receipt.json`.
The real accepted Shinki/EX-Alice background CODE was not modified by
this DATA contribution and is not recredited. Its C++ extern declarations
will receive separate source-current ABI validation.

## Real one-byte C++ enum consumer (2026-11-12)

The EX-Alice animator now obtains `_hexagrams_flag` through its
canonical global C-linkage declaration in `background_rules.h`, typed
as the original one-byte `hexagrams_flag_t` in C++ and as the true
unsigned-byte public in C. The local duplicated extern and enum were
replaced with the unchanged global enum definition, preserving the
original 0/1/2, `FLAG_COUNT`, and all source-level arithmetic.
The 220-byte hexagram animation, all 17 background CODE units and the
three-byte physical C DATA contribution pass source-current native
replay; see the ABI closure receipts in `background_rules.md`.
