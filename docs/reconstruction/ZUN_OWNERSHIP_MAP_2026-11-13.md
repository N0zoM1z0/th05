# ZUN resident ownership map — 2026-11-13

Scope: the `-S` COM child inside the pinned `ZUN.COM` container. COM addresses below are segment offsets; the corresponding child-file offset is `COM - 0x100`. The outer-container offset is `0x0AE4 + COM - 0x100`.

## Verified file-backed ownership

The live ownership overlay currently admits **5,763 bytes** of verified source ownership in this child. The vendor-library additions below carry zero authored-code credit.

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

## Still unclassified

The original resident tail's previously reported 3,110 unknown file-backed bytes is now reduced by the verified 583-byte early-runtime partition to **2,527 bytes**:

| COM interval | Bytes | Current interpretation |
|---|---:|---|
| `[0x0363, 0x0365)` | 2 | Writable CS slot; identity and lifetime still open |
| `[0x0F13, 0x1650)` | 1,853 | Strong CT.LIB code candidates; complete member/fixup ownership not yet admitted |
| `[0x17FE, 0x1A6A)` | 620 | Mixed resident data candidates; exact segment/member partition still open |
| `[0x1A70, 0x1AA4)` | 52 | INIT/DATA tail candidates; exact segment/member partition still open |

The BSS range `[0x1AA6, 0x1AFA)` is zero-filled runtime storage, not file-backed bytes in the 2,527-byte count. The `atexit` OMF member's `__atexittbl` relocation resolves to COM 0x1ABA, inside that BSS range. Its 64-byte BSS extent is recorded as a symbol/segment anchor only; no BSS ownership claim is made by the early-code reviewer.

## Reproduction

- `python3 scripts/review_zun_early_ctlib.py --check`
- `python3 scripts/review_zun_ownership.py --check`
- `python3 scripts/ownership.py --check`

Do not use a full cold replay for this workstream. The next high-value target is the 1,853-byte interval `[0x0F13, 0x1650)`: validate complete OMF member boundaries and relocation semantics, then separately resolve the 620-byte data region and 52-byte INIT/DATA tail.
