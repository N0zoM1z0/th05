# Staff-roll image reveal: two original writable blank eraser strings

The decoded MAINE interval `[1185C,11862)` is one complete six-byte
initialized-DATA contribution: two independent `char near[3]` strings
containing two ASCII spaces and a natural NUL terminator. They are the
original `unk_1184C` and `unk_1184F` text-erasure resources in the
ReC98 `th05_maine.asm` reference, each consumed by a **different**
original staff image reveal routine.

The accepted `staff_image_update_a()` passes the first text pointer to
`text_putsa()` with black reverse attributes while preparing the A-side
CDG image; the paired `staff_image_update_b()` passes the second string
at the same text-cell erasure step for the B-side reveal. Both routines
have independently accepted complete 376-byte near-Pascal function
bodies. The source therefore exports their actual writable C publics
`staff_image_cover_a` and `staff_image_cover_b`, instead of pooling two
visually identical strings or copying character-pixel assets.

The real original DATA location is DS `10110:174C`. The outside-only
binder preserves group_01 `A540`, SHARED `E800`, and only the preceding
DATA prefix. The source contributes exactly six ordinary initialized
bytes with no extra alignment. The preceding **18 unknown zero bytes**
remain unowned; the immediately following `staff` and `stf*.cdg`
filename bank has its own accepted source contribution.

The scoped receipt
`.analysis/unit-replays/gpt-web-maine-staff-cover-strings-a/receipt.json`
passes two independent Borland C compiler producers, full six-byte raw,
OMF LEDATA/SEGDEF and MAP equality, the original empty ordered MZ
fixups, and rejection of the compiled second-string mutation from
`"  "` to `" X"`. This is a source-level text object, not inferred
original compiler packing or a whole-program acceptance.

## Native C/C++ public-symbol consumer closure (2026-11-12)

Both standalone source interfaces now declare their owned C arrays under
explicit C linkage: `extern "C" char staff_image_cover_a[3]` in
`image_phase.hpp` and `staff_image_cover_b[3]` in `reveal_b.hpp`.
This resolves a source-origin cross-translation-unit ABI edge rather
than replacing the already exact text, creating a fake provider or
modifying linker operands. The actual `text_putsa()` calls in both
376-byte image reveal functions still reference the original source
addresses and remain exact. The shared header touches thirteen
accepted Staff functions (clip, wipe, both reveals, lifecycle and
particle functions, bitmap helpers, and the full staff controller).
Every affected accepted unit was selectively recompiled twice by
Borland/TLINK and checked against complete raw code, original MAP
bounds and ordered relocations. All thirteen exact comparisons pass,
with the existing compiled semantic negative rejected:
`.analysis/unit-replays/gpt-web-maine-staff-eraser-abi-a/receipt.json`.
No previously accepted CODE or six-byte DATA is counted twice.

## Targeted reviewed-ASM dependency refresh (2026-11-12)

The Staff image header is also a pinned *semantic review input* for five
separately accepted low-level CDG drawing ASM families. Changing the
header invalidated their old review-input fingerprints, although the
full Staff C++ cohort had passed. Rather than suppressing those checks
or reverting the correct C ABI, all five families were independently
rebuilt under the reviewed-ASM lane with their original native boundary
proofs, **two complete TASM/TLINK producers per family**, ordered fixups,
and their own compiled ASM negative:

- `main-cdg-alpha` and `op-cdg-alpha` (148 bytes each)
- `main-cdg-opaque`, `op-cdg-opaque`, `maine-cdg-opaque` (102 bytes each)

The receipts are saved respectively under `.analysis/unit-replays/`
with names `gpt-web-staff-abi-asm-{main-alpha,op-alpha,main-opaque,
op-opaque,maine-opaque}-a/receipt.json`. Their accepted records and
explicit review-adoption fingerprints were refreshed atomically without
changing any native CODE or source-note provenance. This is **not**
new C++ source credit; these are the same five separately reviewed ASM
functions with source-current dependency evidence. The 13 accepted
Staff C++ functions also retain the scoped proof cited above. No whole
cold replay was executed.
