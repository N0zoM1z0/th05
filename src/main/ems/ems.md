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
