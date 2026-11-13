# ZUN `-S` resident initialized DATA ownership (2026-11-13)

The file-backed COM interval `[0x17FE, 0x1A6A)` is 620 bytes. The accepted
review now accounts for **610 original vendor DATA bytes**: 492 bytes from six
complete Borland `CT.LIB` DATA LEDATAs and 118 bytes from four complete Master
0.23 OMF DATA members. Ten bytes remain unknown in six short gaps.

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

## Master 0.23 OMF DATA members

The pinned original `_reference/ReC98/bin/masters.lib` archive (SHA-256
`6be41dbcfcf4504977165ccc44443525a29a01f85a1580e6ad0c620bf802faf6`, 640
members) supplies four complete OMF DATA segments in the resident interval:

| Member | COM DATA start | Bytes | OMF relationship |
| --- | ---: | ---: | --- |
| `version` | `17FE` | 93 | `_Master_Version` public at offset 20 |
| `grp` | `185C` | 11 | imports `_Master_Version` |
| `resdata` | `1868` | 10 | `pal98 grb` resource name |
| `fil` | `1872` | 4 | original file state |
| **Total** | | **118** | |

All four are checked against their complete original OMF members: SEGDEF,
GRPDEF, LEDATA, PUBDEF, EXTDEF and FIXUPP metadata, plus exact target bytes.
Each DATA segment is a complete offset-zero LEDATA with no relocations. The
`grp`/`version` public-symbol relationship is independently checked. The
93-byte `version` LEDATA is also byte-identical to the NUL-terminated
`MASTERS.LIB Version 0.23 ... All rights reserved.` archive-header string at
file offset `0x79`; this is a cross-check of the same 93 bytes, not an
additional ownership claim.

## Remaining gaps in the 620-byte interval

| COM interval | Bytes |
|---|---:|
| `[0x185B, 0x185C)` | 1 |
| `[0x1867, 0x1868)` | 1 |
| `[0x1876, 0x1878)` | 2 |
| `[0x1897, 0x1898)` | 1 |
| `[0x1A0A, 0x1A0C)` | 2 |
| `[0x1A67, 0x1A6A)` | 3 |
| **Total** | **10** |

The separate 52-byte tail `[0x1A70, 0x1AA4)` is handled by the CT.LIB
initialized/uninitialized DATA review. It is not included in the 610-byte total
above. No BSS outside the bounded file-backed OMF DATA segment, inferred
zero-fill, or duplicate `rand` pattern is credited.

Focused reproduction:

```sh
python3 scripts/review_zun_resident_data.py --check
```

Acceptance evidence is in `config/zun_resident_data_acceptance.json`, generated
from `config/zun_resident_data.toml`. No compiler replay or full cold replay is
required.
