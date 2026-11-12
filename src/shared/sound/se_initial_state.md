# TH05 playback state: accepted initialized C++ DATA

The complete two-byte sound-effect playback state is recovered from the native
TH05 MAIN, OP and MAINE DATA segments. The original representation is an
unsigned effect ID initialized to `SE_NONE` (`FFh`), followed immediately by
an unsigned elapsed-frame counter initialized to zero. These are mutable C-linkage
objects, **not** extra priority-array entries, a one-time CODE instruction,
or BSS. The historical value and names also occur in pinned ReC98
`th02/snd/se_data.c`; the real TH05 play/update/reset code directly consumes
and modifies the two native byte addresses. The existing exact `se.hpp`
interface and accepted sound handlers are unchanged.

| Artifact | Native DS frame | `snd_se_playing` | `snd_se_frame` | Complete initialized DATA extent |
| --- | --- | --- | --- | --- |
| MAIN | `209D` | `0822` | `0823` | `211F2..211F4` |
| OP decoded | `0EFE` | `09E2` | `09E3` | `F9C2..F9C4` |
| MAINE decoded | `1011` | `06C0` | `06C1` | `107D0..107D2` |

The maintained source `se_initial_state.cpp` emits only a complete two-byte
Borland `_DATA` LEDATA; no compiler CODE, padding, artificial alignment or
foreign initialized bytes are included. Each native binder reserves only the
preexisting code frames and DATA prefix. OP also retains the already verified
Music Room foreign DATA end to satisfy the MZ minimum allocation, without
claiming or emitting any of that area. The original four-byte MAIN gap and
larger OP/MAINE gaps are **not** all claimed as sound state. The separate
[initial memory budget](../memory/mem_assign_initial.md) recovers the `4E20h`
word following MAIN state and the corresponding words in OP/MAINE; other
intervening bytes remain outside both DATA owners.

Each of the following receipts has two real original-compiler/TLINK producers,
complete byte and empty ordered MZ relocation equality, actual OMF/MAP
scope, and a meaningful compiled negative (`SE_NONE` becomes effect zero):

- `.analysis/unit-replays/gpt-web-main-se-initial-state-a/receipt.json`
- `.analysis/unit-replays/gpt-web-op-se-initial-state-a/receipt.json`
- `.analysis/unit-replays/gpt-web-maine-se-initial-state-a/receipt.json`

All three complete two-byte scopes are accepted independently, adding **six
source-authored initialized DATA bytes**, zero instructions. The original
translation-unit organization and whole-executable identities are not inferred
from separate exact producer contexts. No full cold replay was used.
