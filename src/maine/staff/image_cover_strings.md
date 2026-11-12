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
