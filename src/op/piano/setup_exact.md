# Exact OP piano setup and initial screen draw

The Music Room's `piano_setup_and_put_initial()` is now a complete, exact
218-byte far C++ function at decoded OP `[D894,D96E)`. The maintained C++
initializes the GRCG mode, draws six blank keyboard sections at their
18-pixel-spaced VRAM positions, then draws 18 individual `FM1`–`FM5` and
`SSG` label glyphs through the already accepted near piano helper entries.
Finally it calls PMD interrupt `60h` function `10h` to obtain the music
work-area segment pointer and stores its two native WORDs at DS `383A`.
The function preserves the original SI/DI save/restore behavior, `RETF`,
unchecked PMD call and original page/colour handling. No piano glyph assets,
label fonts, helper bodies or initialized DATA belong to this source.

The source uses the original semantic piano geometry and label IDs, with
constant expressions rather than 18 copied VRAM offset bytes. It follows
pinned ReC98 `th05/op/piano_c.cpp`. The actual Borland `-c` output matches
every native instruction. Isolated linking needs a *proof-local* group alias
for the adjacent helper symbols: these near providers occupy the same actual
CS `D300`, but are in a separate foreign-only segment in the binder. The
alias lets TLINK resolve their original near call displacements without
supplying instructions or altering target bytes. The source CODE and data
frames, PUBLIC addresses, and ordered MZ relocation stream are checked
against the decoded OP target; this is not a claim that the historical
linker's internal group names were identical.

Focused receipt:
`.analysis/unit-replays/gpt-web-op-piano-setup-218-a/receipt.json`.
Two independent real Borland/TLINK producers match all 218 original bytes,
complete OMF/MAP function coverage, and the native empty ordered relocation
stream. The negative changes the piano label highlight color from 5 to 4
and is compiled and rejected. Existing keyboard/label ASM and current-note
providers are foreign, with no duplicate acceptance.

The immediately following [116-byte piano renderer](render_exact.md) is now
also accepted as an independent exact C++ owner. Together the two adjacent
functions cover all `D894..D9E2` (334 bytes) without a gap or overlapping
piano ASM contributions.
