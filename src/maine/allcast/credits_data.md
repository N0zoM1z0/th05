This accepted initialized-DATA reconstruction owns the complete all-cast UI text
bank `[0x10B16, 0x115F9)`, DS:0A06..14E9: 47 distinct NUL-terminated arrays,
2787 bytes, no gaps, padding, or relocations. They are game headings, cast
names and roles, and credits. These are readable interface text, not glyphs,
fonts, images, or other opaque assets.

The source is UTF-8 and must use explicit CP932 staging. Each string's encoded
length, including its terminator, is checked separately. All 47 strings
round-trip to the original CP932 bytes; none contains a multibyte character
with trailing byte 0x5C. Original spacing, punctuation, romanization and
misspellings are retained. Repeated equal text is deliberately represented by
distinct externally named arrays, preserving each real object and address.
There is no pooled literal bank or enclosing synthetic original structure.

The original 47-entry `LINES` far pointer table references each object at its
start, in exactly the physical string order. The strings are passed through
the actual `const shiftjis_t far *` text API. The47 complete arrays are ordinary mutable unsigned-character objects in
writable DATA, with a const-pointee view at the text consumer. The historical
original source declarations and qualification are unknown. Pinned ReC98 revision
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05_maine.asm` lines 5986..6034,
corroborates the literal strings and adjoining objects as disassembly evidence.

The bank starts immediately after a complete `EXED15.pi` filename and ends
immediately before the separate `EXED` filename. Neither neighbor is owned.
The existing accepted 94 MAINE DATA bytes (entry43 and alphabet51) do not
overlap this bank. The native ownership inventory classifies this whole bank
as unknown before this proposal.

The outside-only binder places the original DGROUP frame at 1011h and the
source contribution at offset 0A06h. It supplies no string bytes or assets.
The proposed negative changes `Project of TOUHOU` to `Project of TOUHOX`.
The `maine-allcast-credits-data-b` replay passes two independent fresh
producers, all2787 raw bytes, complete compiler DATA coverage and the original
empty relocation stream. The own compiled negative changes TOUHOU toTOUHOX
and fails comparison. The ledger credits2787 initialized semantic DATA bytes;
no historical original-TU identity or independent whole-program linkage is
claimed.
Native object extents, references, hashes and encoding checks are retained in
`.analysis/allcast-ui-data-boundary-review.json`.

The first actual producer `maine-allcast-credits-data-a` stopped at its size
gate: Turbo C++4.02 coalesced equal const arrays into38 physical objects,
emitting2263 bytes instead of2787. All47 names were present, but nine repeated
objects shared addresses, removing524 bytes. There was no alignment gap or
encoding defect. Original distinct DATA object identities falsified the
initial assumption that external const definitions preserved them.

The corrected model removes only the unsupported definition/declaration const
qualification from these47 writable objects; the consumer pointer types,
contents, sizes, order, binder and compiler flags are unchanged. It uses no
enclosing synthetic structure, packed type, filler, literal-offset arithmetic
or pooling flag. The shared new header affects only this text producer and
the separate202-byte pointer/count producer, which is replayed with that
header as `maine-allcast-lines-data-b`. The first failed objects and pooling
proof remain private; no first-attempt acceptance is claimed.
