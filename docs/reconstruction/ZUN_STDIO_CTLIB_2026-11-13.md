# ZUN `-S` resident stdio/path CT.LIB partition (2026-11-13)

The original `-S` COM runtime interval `[0x0F13, 0x1650)` is 1,853 bytes.
Ten complete original Borland Turbo C++ 4.0 `CT.LIB` members now account for
**1,837 source-written CODE bytes** in that interval. Their original OMF
`_TEXT` segments and complete LEDATA/FIXUPP records are checked against the
pinned library and target:

| Member | COM CODE LEDATA | Bytes | 16-bit fixups |
| --- | ---: | ---: | ---: |
| `_pathops` | `0F13..0FD8` | 197 | 6 |
| `fflush` | `0FD8..1069` | 145 | 2 |
| `flushall` | `1069..10AB` | 66 | 3 |
| `fseek` | `10AB..1251` | 422 | 6 |
| `setvbuf` | `1251..1336` | 229 | 11 |
| `strlen` | `1336..1352` | 28 | 0 |
| `write` | `1352..1477` | 293 | 9 |
| `writea` | `1477..14CC` | 85 | 3 |
| `xfflush` | `14CC..1501` | 53 | 2 |
| `setargv` | `1503..1642` | 319 | 26 |
| **Total** | | **1,837** | **68** |

For each member the verifier pins the full OMF program-record hash, complete
segment/group definitions, ordered PUBDEF/EXTDEF tables, LEDATA extents and
ordered FIXUPP sites. All 68 two-byte relocations are resolved to original
public definitions. The external closure covers 22 symbols across the same
CT.LIB, the previously verified early-runtime/nearheap modules, and the
original `C0T.OBJ`. All **1,701 non-relocation bytes** match verbatim; the
complete 1,837-byte LEDATA image matches after applying OMF relocation. Both
a non-relocation instruction mutation and a resolved relocation mutation are
rejected by the same verifier.

The first nine CODE LEDATAs tile `[0x0F13, 0x1501)`. The `setargv` member has
a 321-byte `_TEXT` SEGDEF but its CODE LEDATA begins at segment offset `+2`,
so its 319 source-written bytes occupy `[0x1503, 0x1642)`. The two leading
bytes `[0x1501, 0x1503)` have no LEDATA, and the 14-byte gap
`[0x1642, 0x1650)` precedes the original C0T `_DATA`; neither is assumed to
be alignment or executable code. Both remain unclassified.

The relocation closure also gives exact address anchors into the still-open
resident DATA region: `_pathops` segment 2 at `0x1A70`, `setvbuf` segment 2 at
`0x1A80`, and `setargv` segment 2 at `0x1A86`. The `setargv` DATA publics
`__argc` and `__argv` are at offsets 0 and 2. Other referenced symbols
resolve to `__streams=0x18A0`, `__nfile=0x19E0`, `__openfd=0x19E2`,
`__exitbuf=0x189A`, and the original C0T configuration fields. These are
address/identity anchors only: this CODE review does not claim DATA, INITDATA
or BSS bytes.

The result is original Borland vendor CODE with zero authored TH05 credit.
It closes 1,837 bytes of the previously unknown 1,853-byte interval, leaving
only the two segment/file gaps above. The separate 620-byte DATA region and
52-byte DATA/INITDATA tail remain open.

Focused reproduction:

```sh
python3 scripts/review_zun_stdio_ctlib.py --check
```

Acceptance evidence is in `config/zun_stdio_ctlib_acceptance.json`, generated
from `config/zun_stdio_ctlib.toml`. No full cold replay is required.
