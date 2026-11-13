# ZUN `-S` resident initialized DATA ownership (2026-11-13)

The file-backed COM interval `[0x17FE, 0x1A6A)` is 620 bytes. Two
independent original vendor sources now account for **585 bytes** within it:
492 bytes from six complete Borland `CT.LIB` DATA LEDATAs and a 93-byte
Master 0.23 library-header string. The remaining 35 bytes in this interval
are four deliberate holes and remain unknown.

## Borland CT.LIB DATA segments

| Member | COM DATA start | Bytes | 16-bit OMF fixups |
| --- | ---: | ---: | ---: |
| `_abort` | `1878` | 31 | 0 |
| `atexit` | `1898` | 2 | 0 |
| `exit` | `189A` | 6 | 3 |
| `files` | `18A0` | 320 | 5 |
| `files2` | `19E0` | 42 | 0 |
| `ioerror` | `1A0C` | 91 | 0 |
| **Total** | | **492** | **8** |

Every segment is taken from its complete original CT.LIB OMF member. The
review checks the pinned library/tree identity, SEGDEF size/class/name,
DGROUP membership, ordered LEDATA/PUBDEF/EXTDEF/FIXUPP records and exact
original public boundaries. `_abort`, `atexit`, `files2` and `ioerror` DATA
match verbatim. The `files` segment's five two-byte fixups resolve to its own
DGROUP `_DATA` base `0x18A0` plus addends `0x00, 0x10, 0x20, 0x30, 0x40`.
The three `exit` DATA fixups resolve to the original `exit` CODE base `0x0A32`.
The 476 non-relocation bytes compare verbatim; the complete 492-byte DATA
image compares exactly after applying the eight original OMF relocations.
Both a plain DATA mutation and a relocated-pointer mutation are rejected.

The `atexit` member's separate 64-byte `__atexittbl` BSS segment is not
file-backed and is not claimed. A four-byte `rand` DATA pattern also appears
inside the `files` target interval; it is not separately claimed because an
independent resident placement/ownership boundary has not been established.

## Master 0.23 header string

The first **93 bytes** at COM `[0x17FE, 0x185B)` exactly match the
NUL-terminated `MASTERS.LIB Version 0.23 ... All rights reserved.` header
string at byte offset `0x79` in the pinned original `_reference/ReC98/bin/masters.lib`
(SHA-256 `6be41dbcfcf4504977165ccc44443525a29a01f85a1580e6ad0c620bf802faf6`).
The complete 93-byte source and target slices are identical. The following
29 bytes `[0x185B, 0x1878)` do not match this header slice and remain unknown.
The Master header is vendor initialized DATA with zero authored-code credit.

## Remaining gaps in the 620-byte interval

| COM interval | Bytes |
| --- | ---: |
| `[0x185B, 0x1878)` | 29 |
| `[0x1897, 0x1898)` | 1 |
| `[0x1A0A, 0x1A0C)` | 2 |
| `[0x1A67, 0x1A6A)` | 3 |
| **Total** | **35** |

The separate 52-byte tail `[0x1A70, 0x1AA4)` still needs its own DATA/INITDATA
segment review. The 93-byte Master string and six CT.LIB DATA extents are the
only claims made by this review; no inferred zero-fill, alignment, or BSS is
credited.

Focused reproduction:

```sh
python3 scripts/review_zun_resident_data.py --check
```

Acceptance evidence is in `config/zun_resident_data_acceptance.json`, generated
from `config/zun_resident_data.toml`. No compiler replay or full cold replay is
required.
