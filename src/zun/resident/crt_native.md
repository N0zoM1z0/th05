# Exact original Borland C0T startup inside ZUN `-S`

The original Turbo C++ 4.02 tiny-model C0T startup is now independently
relinked and compared in the original `-S` COM context. The complete COM
runtime `0100..0367` CODE range is **615/615 exact bytes**; its separate
`1650..16BE` initialized CRT DATA range is **110/110 exact bytes**.
Two distinct positive native TASM32/TLINK builds and an authentic
`_INIT_`-layout mutation confirm the result.

The actual original vendor object is pinned at the installed toolchain path
`.analysis/toolchain/installed/tc40j/LIB/C0T.OBJ` (SHA-256
`27169f062a9b77bf4accfb9550ca4ccbf0fd710d4b1232768630d53bb6305f7c`).
It contains these actual OMF contributions:

| C0T.OBJ original OMF CODE/DATA record | COM runtime interval | Source-written bytes |
| --- | --- | ---: |
| `_TEXT` LEDATA, offset `0100`, size `0263` | `0100..0363` | 611 |
| **Unwritten** `_TEXT` runtime segment scratch | `0363..0365` | **0** (2 unknown bytes) |
| `_TEXT` LEDATA, offset `0365`, size `0002` | `0365..0367` | 2 |
| `_DATA` LEDATA, size `006E` | `1650..16BE` | 110 |
| **Total original source-written material** | **Discontiguous CODE and DATA** | **723** |

The original startup accesses the two uninitialized CODE bytes through
`CS:[0363]` during process initialization. These two zero bytes are compared
but deliberately **remain `unknown`** in the ownership map; they are neither
supplied by original OMF LEDATA nor counted as original instructions. The
final two-byte `_TEXT` record is a compiler model word, not automatically
defined as a CPU instruction. The **110 DATA bytes are vendor initializer
bytes**, not authored C++ and not BSS.

## Exact native placement without copying foreign code

The maintained [symbol-only TASM binder](../../../probes/units/zun_crt_layout_bindings.asm)
reserves the actual linked layout: the resident configuration function
`0367..04A9` (already separately accepted as **322 bytes of C++**), all
foreign Master/RTL code through `1642`, the CRT DATA starting at `1650`,
true end of ordinary `_DATA` at `1A94`, the **18-byte `_INIT_` segment** at
`1A94..1AA6`, and **84 bytes of BSS** at `1AA6..1AFA`. Those foreign
regions are ORG/symbol reservations only. The binder emits **no LEDATA,
LIDATA, COMDAT, initialized game data, or copied program bytes**.

The native replay reuses the two actual independent, already accepted
`zcfg.obj` producers and the pinned unmodified `C0T.OBJ`; it **does not
recompile configuration or `main()`**. In both builds, the original C0T
source-owned CODE and DATA and the complete neighboring configuration
function match naturally. In the compiled source negative, changing the
foreign `_INIT_` table from 18 to 16 bytes changes the real original
startup's addresses and DATA pointers but leaves the accepted C++ function
and two writable CS bytes untouched. That negative fails exact comparison,
as required.

Focused receipt:
`.analysis/zun-crt/gpt-web-crt-b/receipt.json`.
Accepted record:
[`config/zun_crt_acceptance.json`](../../../config/zun_crt_acceptance.json).
The explicitly reviewed adoption:
[`config/reviewed_zun_crt.json`](../../../config/reviewed_zun_crt.json).

The three adopted physical ZUN.COM ranges are:

- `[0AE4,0D47)` — 611 source-written vendor CODE-segment bytes
- `[0D49,0D4B)` — two source-written vendor model bytes in CODE
- `[2034,20A2)` — 110 source-written vendor initialized DATA bytes

Physical `[0D47,0D49)` remains unknown. These claims do not overlap the
accepted 322-byte configuration C++ function at `[0D4B,0E8D)` nor the
separate 320-byte semantic C++ DATA at `[20A2,21E2)`.

Source-current checking is lightweight; the native replay is explicitly
limited to C0T plus the frozen configuration object context:

```sh
python3 scripts/replay_zun_crt.py --check
python3 scripts/replay_zun_crt.py --output .analysis/zun-crt/NEW
python3 scripts/replay_zun_crt.py --accept .analysis/zun-crt/NEW/receipt.json
```

This is original **Borland runtime vendor code and DATA** with **zero new
game-authored credit**. It does not accept the 269-byte ZUN C++ `main()` or
assert a complete 6,564-byte `-S` child.
