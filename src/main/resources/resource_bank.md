# Semantic runtime resource bank

This candidate groups 38 independently proved semantic character arrays at
original MAIN `[20A82,20BDD)`, 347 bytes, or DS `209D:00B2..020D`.
The first four objects are the real archive filename `怪綺談2.dat`, sound
basename `miko`, launcher name `op`, and mutable song basename `ST00`.
The following 34 fields are the actual palette/character/bomb/stage resource
filenames reviewed in `stage_files.md`. No file payload is reproduced.

The first archive field is const unsigned char, matching the accepted entry
API; launcher/sound names and the 34 resource names are const char arrays.
`ST00` is mutable char. Original DS `00A2` holds the real far pointer
`209D:00C6`; at `B506` the original stage callback loads it. At `B50A` and
`B514` it writes the song basename's final two characters, then passes that
same far name to `SND_LOAD` at `B520`. These five real basename bytes are
state, not filler. The other three prefix objects have individually decoded
PUSH references in the accepted MAIN entry.

Every one of the 38 fields has a size and `offsetof` assertion, and the whole
bank has a 347-byte size assertion. It is an ordinary mutable near aggregate
with actual const member types. Distinct original copies of `BSS4.CD2` and
`st04.bft` remain distinct semantic fields. No packing directive, compiler
flag experiment, arbitrary prefix, integer byte initializer or compensating
padding is used. The real 25-byte four-object prefix places the bank at its
actual even address `00B2`.

This addresses two proved failures of the earlier 322-byte standalone model:
the compiler pooled its two identical nine-byte const arrays, producing 304
bytes; and the requested `00CB` start was odd for word-aligned DATA. That
original failed source, compiler object, snapshots and pre-link outcome are
preserved. No second producer or negative was run for that failed model.
The new proposal uses genuine objects and identity rather than alignment
bytes or artificially unmerged names.

The bank is a reconstruction model of observed semantic objects, not a claim
that the historical source declared this struct. Its explicit source API is
`main_resource_files.<field>`. It does not automatically supply any old
global-array PUBDEF. Future callers must use real field expressions in their
demonstrated affected source closure. No accepted header or caller changes
are part of this DATA proposal.

The original C++ draft was not compiled. The smaller title-bank C++ producer
demonstrated that TCC rejects const character-array members without a
constructor. Rather than change member constness, add runtime construction
or alter compiler flags, the current `resource_bank.c` uses ordinary C static
aggregate initialization and the C-compatible `resource_bank_c.h` typedef
struct. All 38 types, offsets and the total size remain asserted. A
`__cplusplus` error and a `.c` wrapper require actual C mode with unchanged
compiler arguments and no `-P`. The strict `compiler-generated-c-semantic-data`
origin is restricted to initialized DATA with zero functions; no C++ or
compiler-generated instruction acceptance follows.

Maintained source remains UTF-8, with CP932 staging for the readable archive
name. The source defines no CODE, BSS, pointer table, assets or padding.
The outside-only binder supplies the real empty CODE group context and DATA
prefix `00B2`. Actual complete 347-byte compiler SEGDEF, gapless LEDATA,
complete MAP extent, two fresh raw-exact producers, original ordered fixups,
input/tool/dependency checks and the own `st06.mpn` to `st07.mpn` mutation
passed in the focused `main-resource-filename-bank-c-a` replay. Both fresh
actual `.c` compiler producers emitted all 347 bytes exactly, with the empty
original ordered relocation stream. The own map-filename mutation was compiled
and rejected. All 347 bytes were imported as authored C semantic DATA,
separately classified from C++ ownership. The semantic aggregate model is
accepted; no historical struct, old-PUBDEF alias or caller CODE acceptance is
claimed. Its 347 bytes and the title bank's 78 bytes were imported together,
retaining each independent producer and own control provenance.

Private `.analysis/main-resource-bank-boundary-review.json` and the adjacent
unit-proposal JSON record all 38 native fields, original references and
source identities. `.analysis/failed-semantic-text-data-review.json` preserves
the initial pooling/category-reorder findings. The earlier stage-session
803-byte C++ callback remains unaccepted; its original filename operands are
native observations, with no transferred CODE credit.

The current C boundary/proposal files are
`.analysis/main-resource-bank-c-boundary-review.json` and its adjacent
unit-proposal JSON. Original C++ drafts and the initial failed 322-byte
compiler output remain unchanged as evidence.

The uncompiled C++ draft source/header and failed standalone-array files were
subsequently archived verbatim under `.analysis/failed-semantic-banks/files/`.
The manifest preserves exact original paths, sizes and whole-file hashes.
Actual compiler workspaces and canonical input snapshots remain intact.
The accepted `.c`, C header and bank binder remain byte-for-byte frozen.
