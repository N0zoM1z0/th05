# Exact TH05 OP high-score encoding

`scoredat_encode()` is a complete 100-byte near-Pascal C++ function at
decoded OP `[C87E,C8E2)`, immediately before the independently accepted
high-score viewer. It first sums the 92-byte `scoredat_t` payload into the
original word checksum at DS `5062`, then calls the authentic Master `irand`
provider twice to generate key bytes at `5060` and `5061`. It encodes the
payload backwards from byte 95 to byte 4, using an 8-bit feedback value
rotated right by three bits and XORed with the second key. The real 96-byte
score-section type in `src/op/hiscore/view.hpp` is reused unchanged.

The maintainable algorithm follows pinned ReC98
`th04/formats/scoredat/encode.cpp` and the original byte-feedback semantics.
Turbo C++ must operate directly on the indexed score bytes rather than using
a separate local pointer: a local pointer introduces six bytes of stack
frame and extra loads. The semantic `ROR BYTE PTR feedback,3` keeps the
actual 8-bit rotation; an unqualified register-memory rotation compiled as
a 16-bit operation and changed one native opcode.

This particular function requires the original **direct TCC `-c`** producer,
not the TCC `-S`/TASM32 recipe used for several 386-heavy neighbors. Both
produce identical 100 instruction bytes, but the latter orders the two
relocations as `[35,43]`. The true direct object and TLINK naturally emit
the exact original **`[43,35]`** sequence; no relocation normalization or
binary patching is used.

Focused receipt:
`.analysis/unit-replays/gpt-web-op-score-encode-exact-a/receipt.json`.
Two independent native Borland/TLINK producers match all 100 original bytes,
the literal ordered far `irand` fixups, real CODE/DGROUP context, and complete
OMF/MAP ownership. The compiled source mutation changes feedback rotation
from three to two bits and is rejected. The following viewer and its score
BSS/data pools keep their separate accepted ownership.
