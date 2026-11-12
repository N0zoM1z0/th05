# MAINE All Cast background pointer and quarter index

The complete original MAINE DATA interval `[10870,10930)` now has a
**192-byte** natural C++ initializer owner. The first 128 bytes are the
real four-by-eight `BG_FN` far-pointer table; each of the four character
programs selects seven consecutive `EXEDnn.pi` resources and terminates
with a fully null eighth slot. The next 64 bytes are the original signed
16-bit `BG_QUARTER[4][8]` controls, which select the quarter-screen layout
for each background. Both arrays have their original mutable pointer and
word representations. The separately accepted all-cast controller in
`allcast.cpp` uses the exact `BG_FN` and `BG_QUARTER` symbol names.

All 28 non-null pointers are source-level references to entries in the
separately accepted, **280-byte** `allcast_background_filenames[4][7][10]`
bank. No numeric pointer offsets or segment words are embedded in source;
the native binder provides only the foreign array's true linker public at
DATA `1011:08EE`. In this isolated replay, the source-derived pointers
resolve against the original MAINE frame and genuine post-contribution
outside-DATA context. The four end-of-row null slots and all 32 quarter
values are genuine semantics, not compiler filler or artificially inserted
relocations. The preceding masked-image DATA and the next accepted All
Cast text pointer bank stay outside the complete scope.

The original eight-slot row order and quarter values are directly recorded
in `th05_maine.asm` under `_BG_FN` and `_BG_QUARTER`. Their source grouping
matches the 4×8 indexing in `allcast.cpp`, preserving each stage's displayed
image and current quarter. The full native replay at
`.analysis/unit-replays/gpt-web-maine-allcast-bg-index-a/receipt.json`
passed two independent Borland C++ producers, complete 192-byte OMF/MAP
DATA ownership, all original raw bytes and every original ordered segment
fixup. The compiled mutation of the first program's quarter selector from
three to two is rejected. The accepted filename producer remains unchanged
and requires no cold replay.

## Consolidated source identity after dirty-worktree reconciliation

A separate, uncommitted `background_schedule.cpp` proposal was present in
the live worktree after the 192-byte acceptance checkpoint. It declared
the exact same `BG_FN`/`BG_QUARTER` bytes and the same target interval, so
accepting it independently would have double-owned all 192 bytes. Rather
than leave or silently discard that work, its useful seven-filename row
macro was integrated into the canonical `background_index.cpp`, retaining
the original four-by-eight shape and every distinct 10-byte filename
reference. The source now explicitly captures the actual **C linkage** of
`allcast_background_filenames`, which is compiled by the separate C unit.

The duplicate untracked source, duplicate binder and extra manifest entry
were retired as one coherent reconciliation; no accepted owner or source
initializer was dropped. Focused replay
`.analysis/unit-replays/gpt-web-maine-allcast-index-dirty-merged-a/receipt.json`
recompiled the canonical owner twice, exactly reproduced the full 192
original bytes, all 28 ordered far-pointer fixups, the complete DATA
OMF/MAP contribution, and rejected its compiled quarter-change negative.
Only this affected accepted unit needed rebuilding.

## Canonical C/CPP filename linkage and 192-byte revalidation

The filename producer is real C, so `background_index.hpp` now declares
`allcast_background_filenames[4][7][10]` with explicit C linkage. The C++
index expresses each source-derived 10-byte string as the address of its
first character, retains the four separate seven-name programs, and uses
a single initializer macro so no repeated pointer is silently shortened.
The original mutable pointer array and signed quarter selectors remain
unchanged. This corrects the cross-translation-unit ABI rather than
adding a second owner for the same interval.

A duplicate proposal for `[10870,10930)` was rejected by the progress
ledger's interval-overlap check even though its independent 192-byte
compiler comparison was exact. The already accepted
`maine-allcast-background-pointer-index-data` owner was retained; no
second 192-byte acceptance is imported. The canonical source/ABI update
was rebuilt with the real Borland compiler twice in the same affected
unit, reproducing all 192 target bytes and the 28 original descending
segment fixups. The compiled quarter-selection mutation is rejected:
`.analysis/unit-replays/gpt-web-maine-bg-index-canonical-abi-a/receipt.json`.
