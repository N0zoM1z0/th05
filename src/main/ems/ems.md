# TH05 EMS initialization/cache candidate

Natural source follows ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05/ems.cpp` → `th04/main/ems.cpp` and`ems.hpp`. This is one TU in the original four-function order. It reuses the canonical complete128-byte resident type and declares the complete16-byte CDG file/slot structure, including dimensions, bottom offset, dword width, image count, plane layout and both real segment pointers. Every field offset is checked; no shortened record or fake pointer ABI is introduced.

The original contribution is independently decoded at `[0xB826,0xBAD2)`,684 bytes. Calibration683 was routing only and has a different start/parity. No instruction body or padding byte is supplied manually:

| Complete function | Original start | Extent |
|---|---:|---:|
| `ems_allocate_and_preload_eyecatch` | `0xB826` |155 |
| `bomb_bg_load__ems_preload_playchar_cdgs` | `0xB8C1` |267 |
| `ems_preload_boss_faceset(const char far*)` | `0xB9CC` |154 |
| `eyecatch_animate` | `0xBA66` |108 |

There are675 instruction bytes in218 decoded instructions, one compiler-zero alignment byte at`0xB9C3` (relative413), and an8-byte compiler switch table at`0xB9C4` (relative414). Its four real destinations`B922/B92A/B932/B93A` select the four external character faceset names. The CS-relative dispatch uses offset`0x0BB4`; every direct branch and every table target was independently checked to land on an original instruction start. There are24 original MZ fixups, retained in original order in the private review. Full raw comparison must retain the zero and table bytes.

The second and third functions preserve the actual unbounded resource walk: start at CDG slot2/8 and EMS byte offset100000/200000, capture the first slot's unsigned16 bitplane size once, copy alpha then four color planes, advance the unsigned32 offset, free the slot and continue until its alpha segment is null. They do not clamp the iteration count. Four-plane multiplication occurs in unsigned16 before conversion to the long EMS API parameter, as in the original; it is not silently widened. The boss function's `ENTER4` matches its real32-bit local offset, not a fabricated extra variable.

The last function loads color data for slot31 from EMS, or loads the original external eyecatch filename from disk. Slot31 bitplane size is DS`0x325C`; its color segment handle is DS`0x326A`. It sets PaletteTone0, calls palette_show, blits at `(80,112)`, frees the slot and fades in at speed1. The master APIs retain their actual long offset/size and segment-allocation conventions. No carry-flag contract is inferred.

True MAIN01 frame is`0xAE1`, unit offset`0x0A16`; DGROUP is`0x209D`. The master helpers are frame0. CDG helpers are true frame`14AB`, at offsets`01C0/0668/0726/072C/0788`. The binder preserves those addresses with labels/ORG only, no helper implementations, stack or resource values. Every ORG is below65536.

All state and resource bytes remain foreign: resident pointer DS`41FC`; stage/rank/playchar`576E/576F/5773`; EMS handle`5774`; complete CDG slots begin`306C`; eyename/bbname far pointers`009C/00A6`; palette tone`03DA`; EMS name`0229`; faceset names`023A/0243/024C/0255`. The actual original external EMS name is `KAIKIEMS`, despite the reference GAME5 macro saying `GENSOEMS`. Keeping `_EMS_NAME` external preserves original behavior without importing that reference-version difference as new data. This owner defines zero initialized DATA or BSS and contains no image/script/opaque array payloads.

Private evidence: `.analysis/ems-boundary-review.json`. Entry and negative proposal: `.analysis/ems-candidate.json`. The natural negative rejects EMS capacity exactly equal to EMSSIZE by changing `<` to`<=`, without a fake ABI or byte mutation. Both long source names are truncated in the actual calibration MAP; the private review records observed names rather than inventing aliases. Prefer whole684; any later complete scopes must use actual fresh MAP names and compiler-produced alignment. No compilation or exact acceptance has yet occurred.

The initial natural producer was683 bytes, missing the original switch table's
word-alignment zero. The ordinary `-a2` pragma is therefore explicit before
the switch owner, after all structure definitions. `main-ems-cache-b` then
reproduces every one of684 raw bytes in both independent builds and rejects
its real EMS-space mutation. Its whole ordered relocation list still differs;
that whole unit is unaccepted.

`main-ems-scopes-c` mechanically reviews three complete functions from those
same two intact producers and the same compiled mutation, with zero new compiler
invocations: allocation155, player preload267 and eyecatch108. Each individual
raw scope and original ordered fixup list passes. Together they credit529 CODE
bytes:521 instructions plus8 compiler switch-table bytes; the one compared
zero is excluded. The154-byte boss-face preload remains unaccepted because
its own ordered fixup list differs, despite identical raw code. No fixup sorting,
record splitting, masking, target bytes or handwritten padding is used.

A later independent `-y` line-information diagnostic leaves all684 raw bytes
equal but retains the same wrong ordered fixup stream. The boss scope's original
order is `[71,24,133,114]`; the diagnostic still emits `[133,114,71,24]`.
No maintained source, binder or accepted entry changed. Its sole first producer
is retained at `.analysis/native-producers/main-ems-lines-a/`; it is not an
acceptance receipt and grants no additional credit.

A later unmodified compiler `-S` output assembled by TASM32 also matches all
684 raw bytes, but emits all 24 MZ fixups in ascending order. It cannot recover
the native two descending runs. Its ordinary CODE LEDATA extents are 413 bytes
at0 and270 at414, separated by the original one-byte zero alignment; no record
or instruction was edited. The single diagnostic is retained at
`.analysis/native-producers/main-ems-via-asm-a/`, with no second producer,
negative or acceptance. This route need not be repeated unchanged.

## 2026-11-10 original lifecycle context and switch-table alignment review

The remaining complete `ems_preload_boss_faceset(const char far*)` at
`B9CC..BA66` is still raw-exact C++ with original 4-site relocation order
`[71,24,133,114]` unresolved in the native compiler contribution. A series of
first-producer diagnostics used only **actual adjacent original functions**:

- A same-TU DEMO94+114 followed by the original EMS684 bytes retains EMS raw
  equality but emits boss relocation order `[133,114,71,24]`.
- A single real MAIN01 CODE contribution with complete stage-session-free47,
  pause287, demo208 and EMS684 (**1226 bytes**) emits the original complete
  compiler switch-table alignment zero at `B9C3`, the table at `B9C4..B9CB`,
  and the boss function at **exactly B9CC**. All EMS684 bytes match, but the
  boss's literal relocation sequence is `[24,133,114,71]`. Original CODE OMF
  LEDATAs are represented by actual compiler chunks of 1022 and 204 bytes.
- Adding the real 174-byte `stage_runtime_init` before the full 1226-byte
  stage-release/pause/DEMO/EMS prefix makes a genuine **1400-byte** unified
  C++ source contribution starting at original even `B55A`. The compiler
  preserves the original Boss start **B9CC**, its full **154/154** raw bytes,
  the normal switch-table zero and DS209D, but the four ordered relocations
  become `[133,114,71,24]` (`gpt-web-ems-stage-session-demo-b`). Real empty
  compiler SEGDEFs and native external labels were bound at their original
  positions without introducing source-code holes or patching linked bytes.
- Omitting only the complete 47-byte preceding stage-release function yields
  a genuine pause287 + demo208 + EMS source contribution of **1178** bytes.
  Here both complete boss raw bytes and its **literal** `[71,24,133,114]`
  relocations match, but the boss begins at **B9CB**, not original B9CC:
  compiling from physical odd B637 shifts the code-segment-relative parity and
  omits the switch table's required compiler-generated zero. TCC emits chunks
  of 1024 and 154 bytes in this context. Its preceding table is therefore
  also one byte early; it cannot be an accepted complete-function source.

Eight additional real function-boundary CODESEG reselect trials left
the full even-start context raw-exact but ordered-inexact
(`gpt-web-ems-reselect-*-a`). Real same-segment CODESEG pragmas at the actual function boundary, `-y` line
information, `-a1/-a2/-a16`, ordinary optimization and register options, and
multiple source-equivalent pause/EMS rewrites were each compiled in bounded
first-producer trials. None recovers **both** original table alignment and
original OMF fixup record grouping. Original C++ declarations, pointers,
resource copies and call ABI are unchanged. We did not insert the missing byte,
shift scope coordinates, edit emitted OMF, normalize relocation lists or grant
154-byte credit. Future work needs a *genuine* compiler buffer-boundary context
that preserves the original full switch table and second/third FIXUPP runs.

Key private real producer roots: `.analysis/gpt-web-ems-unified-boss-a/`,
`.analysis/gpt-web-ems-pause-demo-boss-a/`,
`.analysis/gpt-web-ems-stage-session-demo-b/`,
`.analysis/gpt-web-ems-boundary-*-a/`, `.analysis/gpt-web-ems-align-*-a/`
and `.analysis/gpt-web-ems-natural-prefix-*-a/`. Original maintained EMS and
accepted neighboring DEMO/session sources were not changed, so no accepted
unit required cold replay.

## 2026-11-11: complete 154-byte Boss faceset loader now accepted

The last unaccepted EMS function, `ems_preload_boss_faceset(const char far*)`,
now passes **full original-function** exactness at MAIN `[B9CC,BA66)`:
**154/154 bytes**, native literal ordered MZ relocation sequence
`[71,24,133,114]`, exact two independent native Borland/TLINK producers and
a rejected compiled source mutation of the genuine `CDG_FACESET_BOSS` load
slot. No original byte, uninitialized link padding, OMF record, code patch or
artificial initialized DATA is inserted, and no fixups are sorted.

The key was restoring the actual compiler's source CODE contribution and true
foreign physical link frames *together*. The maintained
`ems_boss_full_context.cpp` compiles the complete real original-order 1,826
bytes of MAIN entry, gameplay loop, new-game initialization and stage-session
initialization, then the following real 1,400 bytes of stage-runtime setup,
release, pause, DEMO and four EMS functions. The context includes genuine
source bodies and complete headers with duplicate pragma/declaration
conflicts resolved in the context copies; no fabricated source CODE is
provided. The full 3,226-byte prefix determines the natural Turbo C++ FIXUPP
record partitions; the four-site Boss sequence now appears exactly in its
original `[71,24,133,114]` order. All real gameplay and EMS behavior and the
unbounded CDG slot walk remain unchanged.

The binder `ems_boss_full_context_bindings.asm` uses *source-free* before/
after compiler linkage with only externally established native public labels
and real address placement. In the first long-context trial, the compiler
produced a **zero-byte SHARED SEGDEF** grouped into MAIN01. Merging the
actual foreign `SHARED` providers into that same SEGDEF accidentally placed
14 bytes of alignment between CODE groups: CS14AB far calls instead pointed
to CS0AE1, and all DGROUP operands shifted by `+0E`. Keeping the foreign
source-free providers in a distinct `EMS_SHARED_PROVIDER` SEGDEF produces the
physical original MAIN01 `0AE1`, ungrouped SHARED `14AB`, MAIN03 `1527`,
and DGROUP `209D`, without emitting a single foreign instruction or data byte.
The resulting Boss 154-byte machine code *and* 4-site FIXUPP stream are both
precisely original. The initial isolated 154-byte trial had raw bytes exact
but the wrong fixup order `[133,114,71,24]` and remains diagnostic history.

Only this **one complete 154-byte function** is newly credited as compiler
C++ CODE from the joined source. The other three EMS functions were already
separately accepted at 155, 267 and 108 original bytes; their own accepted
sources and snapshots have not changed and are not duplicated. The 267-byte
player-preload includes one original zero-alignment byte which remains
uncredited and 8 genuine compiler switch-table bytes. The 3,226-byte
context proves natural source/binding provenance for this Boss function; **it
is not claimed as a newly accepted whole-3,226-byte executable unit or a
whole-EMS-TU OMF ordering certificate.** Historical original TU identity is
not established. This extends the full four-function EMS coverage while
respecting the complete-function acceptance contract.

Focused acceptance receipt:
`.analysis/unit-replays/gpt-web-main-ems-boss-154-full-context-20261111/receipt.json`.
The earlier unsuccessful first-producer contexts, link MAP diagnostics and
source snapshots remain in `.analysis/gpt-web-ems-*` for future audit.
