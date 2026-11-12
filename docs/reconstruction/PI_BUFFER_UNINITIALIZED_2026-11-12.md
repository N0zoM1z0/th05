# TH05 eight-slot PI image buffers: verified unwritten game storage

The 32 original bytes at OP `[FA64,FA84)` and MAINE `[1080E,1082E)` are
the actual eight four-byte far pointers in `_pi_buffers`. The retained
ReC98 reconstruction explicitly says `public _pi_buffers` followed by
`_pi_buffers dd 8 dup(?)` in `th05/formats/pi_buffers[bss].asm`.
Existing accepted PI loader/free/drawing functions independently access all
eight genuine 32-bit far-pointer slots. The original linked MAP publics
anchor the same complete ranges:

| Program | Original 32-byte reserved extent | Actual calibration MAP public |
| --- | --- | --- |
| OP | `FA64..FA84` | `0EFE:0A84` |
| MAINE | `1080E..1082E` | `1010:06FE` |

The original source named `[bss]` is included by the game's TASM DATA
module, not necessarily a separate physical `_BSS` segment. In both actual
object files, the previous initialized `_DATA` LEDATA ends exactly at the
public's offset and the next initialized LEDATA begins exactly **32 bytes
later**. No LEDATA or LIDATA initializes any byte in the reserve. Both
calibration and original decoded MZ payloads materialize those bytes as
zeros, without ordered loader relocations.

`python3 scripts/review_pi_buffer_reservations.py --check` verifies the
candidate-native source, both independent TASM objects, public addresses,
actual unwritten OMF extents, target bytes and original target identities.
The resulting `reviewed-uninitialized-game-storage` ownership is a separate
**zero-credit lane**. It classifies **64 source-backed reserve bytes** but
adds **no authored C/C++ initialized DATA, CODE, instruction or compiler
acceptance**, and does not assert that the original MZ contains the same
uninitialized bytes as authored source. This also does not turn arbitrary
neighboring zero-filled regions into accepted storage. The original
source's pristine historical provenance is not independently proven; it
is supported by the pinned candidate-local ReC98 source and native code.
