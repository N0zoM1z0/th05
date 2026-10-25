# Natural TH05 item candidates

These algorithms reuse maintained TH04 `src/main/item/items_update.cpp`,
`splashes.inl`, and `invalidate.cpp`. ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47` provides format/layout and disassembly
corroboration through `th04/main/item/item.hpp`, `splash.hpp`, `miss_add.asm`,
and the supplied TH05 MAIN listing. Its reconstruction and acceptance do not
transfer. Original locations below were reviewed from our pinned executable;
they are MZ load-image offsets, not the reference listing's old addresses.

| Natural owner | Complete original range | Functions | Bytes |
| --- | --- | ---: | ---: |
| `spawn.cpp` | `1CC2B..1CDAC` | items_add165 + items_miss_add220 | 385 |
| `splash.cpp` | `1637C..163FE` | add72 + update58 | 130 |
| `invalidate.cpp` | `C1AC..C1F7` | items_invalidate | 75 |

Total590 instruction bytes, with no owned tables, padding, initialized DATA,
or BSS. All original ordered MZ fixup lists are empty. These are source
candidates; actual producer sizes/raw bytes/fixups and a compiled negative must
pass before acceptance. The next NOP at C1F7 is excluded from invalidation.

`item_t` is the complete20-byte record, with the unused byte, Motion12, byte type,
unknown byte, word patnum, and genuine word pulled-to-player boolean.
`item_splash_t` is the complete10-byte record, including its real time byte,
center, current radius and previous radius. Existing canonical entity flags,
item enum, Subpixel, SPPoint and Motion are reused unchanged. The active pool
has40 items and eight splashes. Reference BSS additionally names one unused
splash record and four unused item records; these are not invented padding
fields or extra active entries, and receive no source-owned storage credit.

TH05 behavior differs from the donor:

- During bomb attraction, byte item types power/point/dream and automatic-drop
  request FF become power. FE (IT_NONE) remains distinct; the unsigned byte
  comparison is deliberate.
- Death drops read the real standalone lives byte at DS:4AD4 rather than the
  TH04 resident structure. Both RNG slot draws are retained: the unused second
  draw still advances shared random state until distinct from the first.
- Spawn visits40 entries, but the original TH05 invalidation function still
  visits32. That actual historical behavior is kept explicitly rather than
  silently replacing it with the pool bound.

The drop pattern, sprite numbers and miss velocities are external semantic
arrays:64 bytes, seven words, and3x2x5 Subpixels respectively. The velocity table
has Y before X. No table values or asset bytes are imported into this source.
Global field operands and callback frames are in the private boundary packet.

Splash addition advances its byte ring index even when its chosen entry is
busy. Radius starts at32 subpixels, grows by32, and marks removal at512; the
following update clears a removed entry. Original splash initialization
`16362..1637C` remains foreign. The reference's REP STOSW/pseudoregister body is
not copied into authored C++; a natural memset producer needs separate evidence.
Hardware rendering and the larger collection/update routines are also outside
this packet.

Invalidation uses the existing `&tiles_invalidate_around` through the genuine
four-byte near Pascal aggregate ABI view already proved for enemy invalidation.
The original entry reads x at SP+2 and y at SP+4, returning RET4. This explicit
legacy DOS ABI adaptation copies canonical points, introduces no new symbol or
address, and does not assert ISO-portable calls through different function
types. It has no relation to the separately parked CF-returning script helper.

Suggested aliases are `th05/it_spawn.cpp`, `th05/it_spl_u.cpp`, and
`th05/it_inval.cpp`; GAME5/BINARY M, normal pinned large-model flags. Spawn and
splash use main_03 with BP enabled; invalidation uses main_01 and `-k-`.
Near helper declarations and even empty foreign segment contexts retain the
real frame. All binders contain only symbols/ORG space, with no bodies, values,
manual call sequences, or artificial stack. They establish bounded oracle
contexts, not whole-game layout acceptance.

Private proposals are `.analysis/item-natural-suggested.toml`,
`.analysis/item-natural-boundary-review.json`, and
`.analysis/item-natural-bindings/`. Controls change initial item upward speed,
splash radial growth, and the invalidation visit bound. None uses unused field
changes as its only behavioral negative.

`main-item-spawn-b`, `main-item-splashes-a` and
`main-items-invalidate-a` now independently pass two fresh producers, full
raw bytes, original ordered fixups and their compiled gameplay mutations. All
590 instruction bytes /five complete functions are accepted. The first spawn
producer was393 versus385: ordinary signed integer `%2` compiled to IDIV.
The actual byte-counter parity check is expressed as `item_drop_cycle &1`,
matching the independently observed TEST without changing gameplay. The
remaining `%64` division and both meaningful RNG draws are preserved.

## Complete rendering acceptance

The separate [item and splash renderers](render.md) now add202 instruction bytes
in two complete functions. They reuse the canonical20-byte item and10-byte splash
records and real graphics APIs. Old spawn/update/invalidation inputs remain
unchanged. Splash initialization and the parked item collection/update functions
receive no credit through this renderer acceptance.
