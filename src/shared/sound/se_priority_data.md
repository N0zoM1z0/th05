# Sound-effect arbitration DATA

`se_priority_data.cpp` defines the two complete 17-entry unsigned-byte tables
used by the shared sound controller. A sound-effect ID selects a replacement
priority and a playback lifetime in frames. The controller permits replacement
when the new priority is at least the current priority; after the frame limit
it releases the current effect. These are game policy tables, not sound-bank,
music, graphics, or opaque encoded asset data.

The existing `se.hpp` supplies the exact mutable C-linkage array interfaces.
It is unchanged. Pinned ReC98 `th04/snd/se_priority[data].asm` corroborates the
semantic values; its acceptance and historical source spelling are not assumed.
Native instructions in each pinned local artifact independently establish the
two byte-indexed reads for replacement and the byte-indexed frame-limit read.
All 34 bytes, including the zero-valued policies, are real table entries.

| Artifact | DS frame | Priorities | Frame limits | Complete load extent |
| --- | --- | --- | --- | --- |
| MAIN | 209D | 0800..0811 | 0811..0822 | 211D0..211F2 |
| OP decoded | 0EFE | 0980..0991 | 0991..09A2 | 0F960..0F982 |
| MAINE decoded | 1011 | 065E..066F | 066F..0680 | 1076E..10790 |

All extents are half-open. There are no padding bytes or original relocation
words. The adjacent playing/frame state and the 64-byte gaps after OP/MAINE's
tables are outside these owners. None of those bytes is initialized here.
The native DATA and its three consumer references per artifact are retained in
`.analysis/se-priority-data-boundary-review.json`.

Each artifact has its own symbol-only binder with the real code/DS frames and
outside DATA prefix. OP also reserves the independently accepted foreign Music
Room DATA end at DS2817 after the complete compiler contribution. Its first
attempt `op-se-priority-data-a` failed the MZ minimum-allocation check before
comparison; it is retained and receives no credit. The corrected outside-only
suffix supplies no values, source bytes or artificial stack. It preserves a
valid harness allocation without extending either owned array.

## Accepted evidence

Receipts under `.analysis/unit-replays/`:

- `main-se-priority-data-a/receipt.json`
- `op-se-priority-data-b/receipt.json`
- `maine-se-priority-data-a/receipt.json`

Each independently passes two fresh deterministic producers, one complete
34-byte compiler DATA SEGDEF/fully covered LEDATA contribution, actual MAP
boundaries, full raw comparison and the original empty ordered relocation
stream. Actual compiler arguments and consumed input identities are retained.
Each compiles its own negative, shortening effect7's lifetime from48 to47
frames; all three are rejected. The unchanged installed-tool proof is reused.
Total new credit is102 initialized semantic DATA bytes, with zero CODE/BSS or
padding credit. Existing sound CODE is still unaccepted. No shared accepted
header or source dependency was edited or replayed.

The source tables are a maintained semantic producer, not proof of historical
TH05 translation-unit boundaries. OP/MAINE acceptance refers to the pinned
decoded view and grants no packed-file or whole-executable acceptance.
