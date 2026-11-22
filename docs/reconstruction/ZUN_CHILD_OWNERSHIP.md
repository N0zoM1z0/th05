# ZUN `-S` child: vendor ownership

The `-S` resident installer is a tiny-model COM child inside `ZUN.COM`. Every
file-backed byte of it is classified in `resources/ownership.json`. Its only
game-authored parts are `main()`, `cfg_init()` and their 320-byte DATA
contribution ([initialize.md](../../src/zun/resident/initialize.md)). The rest
is the original Borland `C0T.OBJ`, members of Borland Turbo C++ 4.0 `CT.LIB`
and Master 0.23 DATA members, all with zero authored credit.

Addresses below are COM segment offsets. The child-file offset is `COM - 0x100`
and the outer `ZUN.COM` offset is `0x0AE4 + COM - 0x100`, the coordinate used
by `ownership.json` and `config/reviewed_gaps.json`.

## How the vendor bytes are verified

Each reviewer rebuilds its members from the original OMF records of the pinned
`CT.LIB` or `_reference/ReC98/bin/masters.lib` (SHA-256 `6be41dbc...`). It
checks SEGDEF/GRPDEF layout, ordered PUBDEF/EXTDEF, LEDATA extents and ordered
FIXUPP records. Then it applies the original relocations against independently
resolved public definitions and compares every target byte. Each reviewer
rejects a mutated plain byte and a mutated relocation word. No target bytes
are copied into a source object.

```sh
python3 scripts/review_zun_early_ctlib.py --check    # config/zun_early_ctlib.toml
python3 scripts/review_zun_stdio_ctlib.py --check    # config/zun_stdio_ctlib.toml
python3 scripts/review_zun_resident_data.py --check  # config/zun_resident_data.toml
python3 scripts/review_zun_ctlib_data.py --check     # config/zun_ctlib_data.toml
python3 scripts/review_zun_brk.py --check
python3 scripts/review_zun_nearheap.py --check
python3 scripts/review_zun_ownership.py --check
python3 scripts/ownership.py --check
```

These need the private targets and the pinned libraries. They are not part of
the public `ci.py` table.

## CODE

`C0T.OBJ` relinks exactly in the `-S` context (`replay_zun_crt.py`); its
`_TEXT` is 0x367 bytes with file-backed LEDATA from COM `0x0100`.

| Interval | Bytes | Contents | Fixups |
| --- | ---: | --- | ---: |
| `[09D6,0C1D)` | 583 | `_abort`, `atexit`, `errormsg`, `exit`, `ioerror`, `isatty`, `lseek`, `n_scopy`, `setupio` | 45 |
| `[0F13,1501)` | 1,518 | `_pathops`, `fflush`, `flushall`, `fseek`, `setvbuf`, `strlen`, `write`, `writea`, `xfflush` | 42 |
| `[1503,1642)` | 319 | `setargv` (321-byte SEGDEF, LEDATA from `+2`) | 26 |

`brk`/`sbrk` (from outer `0x1601`) and `nearheap` have their own reviewers.
The relocations resolve to C0T publics such as `__terminate`, `__cleanup`,
`__checknull`, `__restorezero` and `_errno`, and to CT.LIB publics such as
`__streams` (`18A0`), `__nfile` (`19E0`), `__openfd` (`19E2`) and
`__exitbuf` (`189A`).

## Initialized DATA

| Interval | Bytes | Members |
| --- | ---: | --- |
| `[17FE,1876)` | 118 | Master `version` (93; same bytes as the `masters.lib` header string at `0x79`), `grp` (11), `resdata` (10), `fil` (4) |
| `[1878,1A67)` | 492 | CT.LIB `_abort`, `atexit`, `exit` (3 fixups to its CODE base `0A32`), `files` (5 fixups to `18A0+0x00..0x40`), `files2`, `ioerror` |
| `[1A70,1AA4)` | 52 | `_pathops:2`, `setvbuf:2`, `sysnerr:2`, `setargv:2`, and INITDATA `setupio:4`, `_pathops:4`, `setargv:3` |

The last row has 42 initialized bytes. The other 10 are the unwritten suffix of
`setargv`'s 14-byte DATA SEGDEF, classified as uninitialized vendor storage.
The last two bytes of `setargv:3` INITDATA lie beyond the end of the COM file.
The three INITDATA bases come from their own relocation fields. The `_DATA`
bases come from the accepted CODE relocations. A four-byte `rand` pattern
inside `files` is not claimed separately. The 64-byte `__atexittbl` BSS at
`1ABA` is not file-backed.

## Small gaps

The nine short gaps that an earlier survey left open are all resolved in
`config/reviewed_gaps.json`. None of them earns credit.

| COM interval | Bytes | Classification |
| --- | ---: | --- |
| `[0363,0365)` | 2 | C0T's writable CS runtime slot, unwritten in the OMF |
| `[1501,1503)` | 2 | `setargv` CODE SEGDEF prefix without LEDATA |
| `[1642,1650)` | 14 | Paragraph alignment before DGROUP (C0T DATA at `1650`) |
| `[185B,185C)` | 1 | Word alignment |
| `[1867,1868)` | 1 | Word alignment |
| `[1876,1878)` | 2 | master.lib `fontopen` DATA: `file_sharingmode dw 0` (DOS_ROPEN reads `[1876]`) |
| `[1897,1898)` | 1 | Word alignment |
| `[1A0A,1A0C)` | 2 | CT.LIB `heaplen`: `__heaplen dw 0` (C0T adds `[1A0A]` to the stack size) |
| `[1A67,1A68)` | 1 | Word alignment |
| `[1A68,1A6A)` | 2 | CT.LIB `stklen`: `__stklen dw 1000h` (C0T clamps `[1A68]`) |

The `fontopen`, `heaplen` and `stklen` words show why zero runs must not be
filed as alignment without checking: each one turned up only through a search
of raw operand bytes for readers.
