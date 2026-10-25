# Resident configuration initialization

`config.cpp` reconstructs the complete 322-byte `cfg_init` function in ZUN's
embedded `-S` program. It is ordinary compiler-generated C++, with no inline
assembly, instruction transcription, artificial optimization barriers, copied
target bytes or credited scaffold bytes.

## Scope and native ABI

The candidate-local-attested original is the Japanese ZUN.COM pinned in
`config/targets.toml`. Its SHA-256 is
`5044ae03f7c0333f37d88ef34e244502f90d7314287f6f387c07569e4e0b120e`.
The launcher parser independently bounds the complete `-S` child at outer file
`0AE4..2488`, 6,564 bytes. Only outer `0D4B..0E8D` is accepted here, with SHA-256
`4e0f4242fda6b3d76d1be1988637f7807f5e186c50f8797001f30cd31f09e444`.
The corresponding native COM addresses are `0367..04A9`:
`child IP = outer file offset - 0AE4 + 0100`.

The native function begins with its complete 20-byte local frame and ends with
a near return at `04A8`. The following function begins at `04A9` and receives
no credit. A complete instruction walk finds **zero instruction NOPs**, zero
linker relaxation/alignment bytes and zero compiler CODE-table bytes inside
this function. No instruction, branch target, relocation word or semantic
object is split at either boundary. Both target and candidate loader-relocation
lists are empty: the child is a raw COM, not a decoded MZ image.

The function uses near cdecl linkage: one 16-bit `resident_t __seg *` argument
at BP+4, caller cleanup, status returned in AL. It expands that segment-only
pointer to a far pointer with offset zero. The canonical resident is 128 bytes;
options are six signed chars, the disk configuration is ten bytes, and the
resident segment field is two bytes. The existing shared definitions are
reused unchanged. The local six-byte options copy uses Borland's actual
`N_SCOPY@` EXTDEF. The compiler emits `_TEXT` length 322 with BYTE alignment,
empty WORD-aligned `_DATA`/`_BSS`, and DGROUP containing those two data segments.
There is exactly one initialized CODE record, covering the complete function.

The first declarations preserve the native near Pascal file interfaces:

| Provider | Child COM address | Callee cleanup |
| --- | ---: | ---: |
| FILE_READ | 0698 | 6 bytes |
| FILE_CLOSE | 07B8 | 0 bytes |
| FILE_ROPEN | 07C6 | 2 bytes |
| FILE_WRITE | 07FC | 6 bytes |
| FILE_CREATE | 08A2 | 2 bytes |
| FILE_SEEK | 08DE | 6 bytes |
| FILE_APPEND | 0920 | 2 bytes |
| N_SCOPY@ | 0B66 | 8 bytes |

The shared semantic globals are bound at their native addresses: debug byte
`16BE`, six-byte default options `16BF`, and filename `16C5`. Their contents are
not supplied by the binding scaffold and receive no DATA credit.

## Source and producer context

The natural source reference is ReC98 commit `b6ba5b0a`, `th05/res_kso.cpp`;
its acceptance does not transfer. Native review and the actual TH05 producer
establish this unit independently. The historical build uses tiny model and
an explicit source `#pragma option -2` before all C/C++ tokens, overriding the
command-line `-3`. The replay invokes the pinned Borland C++ 4.02 with
`-c -I. -O -b- -3 -Z -d -DGAME=5 -mt th05/zcfg.cpp`, without a BINARY macro.

The original signed checksum, all range tests, ignored read/write results and
failure paths are preserved. In particular, a missing file leaves the checksum
local uninitialized; recreating an invalid existing file retains that file's
checksum. A failed resident-segment write returns without closing the file.
These original defects are not repaired in an exact reconstruction.

The real pinned `C0T.OBJ` is linked first, then the compiler object and the
symbol-only binding object, using TLINK `-t`. Startup SHA-256 is
`27169f062a9b77bf4accfb9550ca4ccbf0fd710d4b1232768630d53bb6305f7c`.
It supplies genuine COM entry/MODEND, the CODE prefix through `0367`, the
110-byte DATA prefix at `1650`, and the real segment/group declarations.
The scaffold reserves foreign extents and binds symbols; it supplies no
instructions, stack contents or semantic initializers. Every ORG is below
64 KiB. The real DATA base is `1650`, not the startup field address `16A0`.
No startup, foreign library, reserved gap or paragraph alignment byte is
counted as authored source.

`lib/tiny_com.py` validates the retained original container/member and actual
CRT identity, linker order and DGROUP layout. MAP addresses are runtime COM
addresses; the comparator subtracts the PSP bias once to obtain candidate file
offsets (`0367` becomes `0267`). It compares all 322 actual output bytes with
the original outer file bytes. No header, prefix, normalization or masking is
applied to either byte range. Existing MZ/DIET loader and oracle modules retain
their previous exact source identities; other artifacts delegate to them.

## Acceptance and retained attempts

Only `.analysis/unit-replays/zun-cfg-322-b/receipt.json` is imported. It contains
two fresh isolated compiler/assembler/linker producers, valid OMF records,
identical dependency-timestamp-normalized objects, identical complete linked
COM files, and complete raw-byte/ordered-relocation agreement. The complete
comparison COM hash is
`2089d7b257a7e0334960a33073782e68c37929bbae3b4da7e60a10055a943288`;
this sparse comparison build is not a runnable reconstruction of the child.

The unit's own compiled negative changes the life upper bound from 6 to 5.
Its complete contribution remains 322 bytes and differs only at relative
byte 205. The comparator rejects it. Its SHA-256 is
`b47d3e8684117149f9ee54976034cd13fd867b08a4b726193c626618f8d2fe94`.
Six public tests cover container/member identity, scope escape, invalid COM
receipts, MAP/file coordinates, startup/link/group/format errors, and tiny
compiler context. Existing accepted objects and unchanged tool execution
probes were reused after dependency identity checks.

Earlier private experiments remain diagnostic only. A first MZ link exposed
an invalid SS:SP/minimum-allocation combination; a startup-free COM link had
no valid initialized entry. Relinking the retained first C++ object with the
real C0T made the 322 bytes exact. The first generic replay (`-a`) then stopped
after one producer because a provisional validator expected an entry-point
MAP row; TLINK omits that row for `-t`. The corrected validator uses the pinned
real C0T MODEND and actual `-t` link response. No fake instruction, fabricated
stack, synthetic MZ header or patched linker output was introduced. All these
failed/intermediate artifacts remain private and are not accepted producers.

Independent native ABI and CRT reports are retained in
`.analysis/zun-resident-review/native-abi.json` and `c0t-context.json`.
Final independent gate review is retained at
`.analysis/zun-resident-review/gate-review.json`, SHA-256
`b95ec4edc9bed9c4acbfc6abfc0fc01f95ca35f30171cc784879ff9e5dd63c88`.
The saved producer import, all 303 public tests, full CI and native ownership
readback pass. All four incremental replay plans are empty after acceptance.

The adjacent 269-byte `main`, all remaining child functions and all other
unreviewed ZUN bytes remain unaccepted. This unit adds exactly one function
and 322 C++ instruction bytes, with zero DATA, ASM or padding credit. It
makes no whole-child, whole-COM, pristine-target or global-percentage claim.
