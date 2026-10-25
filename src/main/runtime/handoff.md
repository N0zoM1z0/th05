# Score publication and process handoff

This natural C++ producer owns the actual consecutive MAIN functions
`game_state_save_score` at `[0xCEA0,0xCEC2)` (34 bytes) and `GameExecl` at
`[0xCEC2,0xCF61)` (159 bytes). Coordinates are offsets in the unrelocated
MZ program image of locally attested MAIN, SHA-256
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
Their frame is `0AE1`, group `main_01`. All193 bytes are instructions; no
padding, CODE-data table, initialized DATA or BSS belongs to this owner.
The original zero alignment byte immediately afterward is outside the extent.
Both complete return boundaries and every direct local branch were checked.
The seven original MZ fixups, in existing order, are relative offsets
`184,168,163,158,153,133,54`.

The maintained TH04 reconstruction's `src/main/core/gameover.cpp` and
`gameexecl.cpp` supply natural semantic donors. Pinned ReC98 `b6ba5b0a`'s
`th05_main.asm` supplies additional names and behavior evidence. Actual TH05
operands, full boundaries, frame types and relocation order were reviewed
independently. Donor exactness does not transfer.

The small helper copies all eight score digits into the complete canonical
resident score field, then invokes the actual near `score_reset`. This reset
is a real TH05 difference from the donor helper. The far handoff calls it,
releases the EMS handle when present, and publishes the seven unsigned-word
run counters and two unsigned-dword frame counters at the actual resident
offsets44 through64. The unchanged accepted128-byte `resident_t` is reused
in full; individual written field offsets are asserted. Graze is not added
as a new write because no such store belongs to this original function.

Cleanup follows the original TH05 order: BB text, CDGs, boss BB, dialog,
character BB, STD, map, sprite storage, graphics visibility, text and the
shared process services. TH04's gaiji-restore call is absent. All real near
and far interfaces are retained. The long max-point counter keeps its
semantic source name; the binder uses the actual Borland-truncated external
spelling `_total_max_valued_point_items_col`.

`GameExecl` retains its genuine far Pascal interface, one four-byte far string
argument, int result, and RETF4. It calls TC4's actual16-bit process API:
`execl(char far *,char far *,...)`, declared by pinned `PROCESS.H`. Two
ordinary legacy qualifier casts satisfy that historical mutable-string API
without altering either pointer. In large model the pinned `_NULL.H` defines
NULL as0L; `sizeof(NULL)==4` is asserted, preserving the real four-byte
variadic sentinel and twelve-byte total C argument frame. DOS replaces the
process on success; the returned int describes failure.

All original far calls here target either the actual library frame0 or
shared frame `14AB`. There is no same-CS far-call relaxation, physical
register interface, Motion-return adaptation, flag protocol, call emission,
artificial function, inside-owner gap or samecodeseg hint. This provider does
not claim to repair the separate old callers' linker-context mismatches.
The reviewed accepted target extents do not overlap these193 bytes.

Private integration inputs are `.analysis/main-handoff-unit-proposal.json`,
`.analysis/main-handoff-bindings.asm`, and
`.analysis/main-handoff-boundary-review.json`. The outside-only binder
supplies real foreign symbols and no implementations, assets or artificial
stack. The owner-level negative substitutes the killed counter for the
gone counter in the resident publication, changing actual end statistics
when enemies leave without being killed. It is not a separate negative for
the score helper. Accepted focused replay `main-process-handoff-a` proves the complete193
bytes and both functions from two fresh deterministic producers, all seven
original ordered relocations, and valid OMF. The compiled gone-to-killed
statistics mutation changes output and is rejected. This is one negative
for the complete193-byte owner; it is not independent negative coverage
for the34-byte score-save helper. The receipt is
`.analysis/unit-replays/main-process-handoff-a/receipt.json`. Source, header
and binder remain frozen.
