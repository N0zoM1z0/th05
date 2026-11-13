# ZUN resident ownership map — 2026-11-13

Scope: the `-S` COM child inside the pinned `ZUN.COM` container. COM addresses below are segment offsets; the corresponding child-file offset is `COM - 0x100`. The outer-container offset is `0x0AE4 + COM - 0x100`.

## Verified file-backed ownership

The live ownership overlay currently admits **8,185 bytes** of verified source ownership in this child. The vendor-library additions below carry zero authored-code credit.

- The original C0T startup object is pinned independently. Its `_TEXT` segment is 0x367 bytes, but the file-backed `LEDATA` starts at COM 0x0100; the two-byte hole at COM `[0x0363, 0x0365)` is not claimed as code. The original C0T `_DATA` extent is 110 bytes at COM `[0x1650, 0x16BE)`.
- The previously accepted `brk` and `nearheap` CT.LIB members remain independently verified at their recorded COM extents.
- The new early-runtime CT.LIB partition covers the complete COM interval `[0x09D6, 0x0C1D)` (583 bytes), outer-container file interval `[0x13BA, 0x1601)`. Nine complete original OMF CODE segments tile it without gaps or overlaps:

| CT.LIB member / public entry | COM start | CODE bytes |
|---|---:|---:|
| `_abort` / `__abort` | `09D6` | 21 |
| `atexit` / `_atexit` | `09EB` | 40 |
| `errormsg` / `___ErrorMessage` | `0A13` | 31 |
| `exit` / `_exit`, `__exit`, `__cexit`, `__c_exit` | `0A32` | 160 |
| `ioerror` / `__IOERROR`, `__DOSERROR` | `0AD2` | 82 |
| `isatty` / `_isatty` | `0B24` | 21 |
| `lseek` / `_lseek` | `0B39` | 45 |
| `n_scopy` / `N_SCOPY@` | `0B66` | 28 |
| `setupio` / `__setupio` | `0B82` | 155 |

For every one of these nine members, the reviewer checks the complete original OMF member, segment and group definitions, public boundaries, external-symbol order, LEDATA extents, and ordered FIXUPP records. The CODE bytes match exactly after applying the original 16-bit OMF relocations. Non-relocation bytes are byte-identical. Negative controls verify that both an instruction-byte mutation and a relocation-word mutation are rejected.

The early code's external references resolve to original public definitions, including C0T symbols (`__terminate`, `__cleanup`, `__checknull`, `__restorezero`, `_errno`) and CT.LIB symbols (`__streams`, `__nfile`, `__openfd`, `_setvbuf`, `_isatty`, `_strlen`, `__rtl_write`, `__sys_nerr`). This also gives useful address anchors into the still-unclassified data intervals; those anchors are not themselves a data-ownership claim.

- The stdio/path CT.LIB partition now covers **1,837 additional CODE bytes** in the COM interval `[0x0F13, 0x1642)`, with two deliberate holes. The first nine complete CODE segments tile `[0x0F13, 0x1501)`; the tenth member, `setargv`, has a 321-byte CODE SEGDEF but only 319 bytes of CODE LEDATA beginning at segment offset `+2`, so only `[0x1503, 0x1642)` is claimed. Its leading two bytes and the 14-byte trailing gap to C0T DATA remain unknown.

| CT.LIB member / public entry | COM CODE start | LEDATA bytes |
|---|---:|---:|
| `_pathops` / `___path_isdbcsleadbyte` | `0F13` | 197 |
| `fflush` / `_fflush` | `0FD8` | 145 |
| `flushall` / `_flushall` | `1069` | 66 |
| `fseek` / `_fseek`, `_ftell` | `10AB` | 422 |
| `setvbuf` / `_setvbuf` | `1251` | 229 |
| `strlen` / `_strlen` | `1336` | 28 |
| `write` / `___write` | `1352` | 293 |
| `writea` / `__rtl_write`, `__write` | `1477` | 85 |
| `xfflush` / `__xfflush` | `14CC` | 53 |
| `setargv` / `__setargv__` marker | `1503` | 319 |

The verifier checks complete OMF segment/group layouts, PUBDEF/EXTDEF order, LEDATA and FIXUPP extents, all 68 two-byte CODE relocation fields, and each external address against the original public definition. The 1,837 source bytes match after applying those relocations; instruction and relocation mutations are rejected. Internal segment references also anchor `_pathops` DATA at `0x1A70`, `setvbuf` DATA at `0x1A80`, and `setargv` DATA at `0x1A86`. These are semantic address anchors only; no DATA or INITDATA bytes are claimed here. See [the stdio/path CT.LIB review](ZUN_STDIO_CTLIB_2026-11-13.md).

- The resident DATA review now admits **585 vendor initialized-data bytes**: six complete CT.LIB DATA segments (492 bytes) plus the exact 93-byte Master 0.23 library-header string at COM `0x17FE`. The CT.LIB `files` DATA pointers resolve to DGROUP `_DATA` base `0x18A0` plus five original addends; the `exit` DATA pointers resolve to its CODE base `0x0A32`. The other four CT.LIB segments match their original LEDATA verbatim. The Master string matches `masters.lib` offset `0x79` exactly. No BSS or duplicate `rand` pattern is claimed. See [the resident DATA review](ZUN_RESIDENT_DATA_2026-11-13.md).

| Vendor DATA member | COM start | Initialized bytes |
|---|---:|---:|
| Master 0.23 `masters.lib` header string | `17FE` | 93 |
| CT.LIB `_abort` | `1878` | 31 |
| CT.LIB `atexit` | `1898` | 2 |
| CT.LIB `exit` | `189A` | 6 |
| CT.LIB `files` | `18A0` | 320 |
| CT.LIB `files2` | `19E0` | 42 |
| CT.LIB `ioerror` | `1A0C` | 91 |
| **Total** | | **585** |

## Still unclassified

The original resident tail's previously reported 3,110 unknown file-backed bytes is now reduced by 583 early-runtime CODE bytes, 1,837 stdio/path CODE bytes and 585 resident DATA bytes to **105 bytes**:

| COM interval | Bytes | Current interpretation |
|---|---:|---|
| `[0x0363, 0x0365)` | 2 | Writable CS slot; identity and lifetime still open |
| `[0x1501, 0x1503)` | 2 | `setargv` CODE SEGDEF prefix has no LEDATA; not classified as alignment or code |
| `[0x1642, 0x1650)` | 14 | Gap after `setargv` CODE LEDATA and before C0T DATA; remains unknown |
| `[0x185B, 0x1878)` | 29 | Tail after the exact Master 0.23 header string; unknown |
| `[0x1897, 0x1898)` | 1 | Gap between `_abort` and `atexit` DATA |
| `[0x1A0A, 0x1A0C)` | 2 | Gap between `files2` and `ioerror` DATA |
| `[0x1A67, 0x1A6A)` | 3 | Gap after `ioerror` DATA |
| `[0x1A70, 0x1AA4)` | 52 | INIT/DATA tail candidates; exact segment/member partition still open |

The BSS range `[0x1AA6, 0x1AFA)` is zero-filled runtime storage, not file-backed bytes in the 105-byte count. The `atexit` OMF member's `__atexittbl` relocation resolves to COM 0x1ABA, inside that BSS range. Its 64-byte BSS extent is recorded as a symbol/segment anchor only; no BSS ownership claim is made by either CODE reviewer.

## Reproduction

- `python3 scripts/review_zun_early_ctlib.py --check`
- `python3 scripts/review_zun_stdio_ctlib.py --check`
- `python3 scripts/review_zun_resident_data.py --check`
- `python3 scripts/review_zun_ownership.py --check`
- `python3 scripts/ownership.py --check`

Do not use a full cold replay for this workstream. The next high-value target is the 52-byte INIT/DATA tail `[0x1A70, 0x1AA4)`. The 29-byte Master-header tail, three small DATA gaps, two code-segment holes and writable CS slot remain deliberately unknown until their identity and lifetime are proven.
