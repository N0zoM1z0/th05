# Stage/session resource filename DATA

The proposed owner is the complete contiguous bank of 34 readable ASCII
filenames at original MAIN `[20A9B,20BDD)`, 322 bytes, or DS
`209D:00CB..020D`. It names the palette, character/bomb fonts, boss facesets,
stage fonts and stage MPN files. Referenced file contents remain foreign;
no images, fonts, maps or other asset payload are reproduced here.

All 34 existing `SESSION_*` symbol names and near-array types match the frozen
stage-session header. Each original filename has a natural NUL terminator.
Native decoding of the original stage-session callback independently finds
one actual filename PUSH operand for every object start. Candidate source
and CP932 reference literals agree with the original data. The reference is
semantic text evidence, and actual operand addresses are independently checked.

The maintained 803-byte stage-session callback remains unaccepted because
its saved compiler output was 802 bytes. That failed candidate supplies no
acceptance to this independent DATA owner. The reference checks here use
the original 772-byte instruction body, excluding its following zero/table
layout. No callback CODE is claimed by this packet.

Stage six genuinely uses distinct copies of `BSS4.CD2` and `st04.bft`.
Both named objects and original identities remain separate despite identical
contents. The source neither pools them nor redirects one to the other.
No pointer bank, BSS or mutable runtime state is defined. There are zero
padding bytes and zero original MZ relocations across this 322-byte extent.

The symbol-only binder places the empty compiler CODE segment in its actual
`main_01` context, retains the original overall MAIN code/DS frame layout,
and reserves a DATA prefix ending at `00CB`. The compiler must emit the whole
322-byte `_DATA` contribution with complete gapless LEDATA and a complete
MAP extent. The binder contains no filename payload, internal hole, stack
or dummy instructions.

The own semantic negative changes the actual Extra-stage map filename from
`st06.mpn` to `st07.mpn`, preserving its encoded length. Two fresh builds,
full raw comparison, the empty original ordered-fixup stream, full producer
identity/OMF/MAP/dependency checks and this compiled mutation remain required.
The first `main-stage-resource-filenames-a` compiler producer failed before
linking: its real `_DATA` SEGDEF contains 304 fully covered bytes. PUBDEFs
prove that the compiler pooled both nine-byte duplicate filename arrays:
the repeated `BSS4.CD2` aliases the first at contribution offset 250, and
repeated `st04.bft` aliases the first at 259. Original objects have distinct
addresses. Separately, original DS `00CB` is odd, so a standalone word-aligned
DATA contribution cannot begin there. No second producer, link, negative or
success receipt was produced. All 322 bytes remain unaccepted.

Private review/proposal files are
`.analysis/stage-resource-files-boundary-review.json` and
`.analysis/stage-resource-files-unit-proposal.json`. Run
`python3 .analysis/stage-resource-files-review.py` to repeat the bounded native
checks, including all 34 original operand sites, readable object boundaries,
reference lines and source identities.

The failed standalone C++ source/header and its unused binder are archived
verbatim in private `.analysis/failed-semantic-banks/files/`, preserving
original paths and whole-file hashes in the parent manifest. The original
compiler workspace and input snapshots remain intact; native replay reads
those consumed canonical inputs. The accepted complete C field-bank model
is documented in `resource_bank.md`.
