TH05 OP title candidate
=======================

Natural-source provenance: nmlgc/ReC98 at
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05/op_title.cpp`
including the genuine TH05 `th05/op/title.cpp`. This is not the different
TH04 title animation. The shared sprite-loading inline is from
`th04/sprites/op_cdg.hpp`, and file/API declarations from the corresponding
TH05 PI, CDG, master.lib, and PC-98 headers. Canonical menu/resident/CDG enums
and the accepted graphics primitive declarations are reused read-only.

The original decoded OP contribution has three complete functions:

| Function | Load interval | Size |
|---|---|---:|
| main_cdg_load | BC0F..BC83 | 116 |
| main_cdg_free | BC83..BC8D | 10 |
| op_animate | BC8D..BE79 | 492 |

The whole `[0xBC0F,0xBE79)` extent is 618 instruction bytes and 39 original
segment relocations, without switch tables or alignment padding. The three
terminal returns and all nine direct branch destinations were checked
against original instruction boundaries. Real near-code frame is `0xA39`,
group offset `0x187F`; owner segment is `OP_TITLE_TEXT` in `op_01`.
The wrapper module remains `th05/op_title.cpp`, with GAME5/BINARYO and the
usual optimized Borland large-model OP flags. Only the initial owner option
pragma is used, before all includes; the canonical header's first declarations
and the definitions therefore share the same segment context.

The natural local anonymous page structure is retained: one byte each for
shown and accessed pages, plus the inlined `wait_and_flip()` method. The method
uses the actual `frame_delay()` API and compiler-supported `outportb()`
hardware port intrinsics, with no assembly transcription, emits, placeholders,
or register barriers. Size assertions check the two-byte state and byte
members. The real full CDG enum and four unsigned PI masks are preserved.
The animation loads eight roll images, alternates pages, releases those slots,
conditionally starts the menu song, and runs the original masked fade timing.

Initialized DATA is exactly the 154-byte ASCII filename pool at DS
`[0x0F34,0x0FCE)`, with 19 meaningful terminated names and no relocations.
Each source filename was independently checked at its original immediate
pointer destination. The preceding byte at DS `0x0F33` is outside this owner.
There is no BSS contribution. `_PaletteTone` at DS `0x054E` and the canonical
far `_resident` pointer at DS `0x2DEC` remain foreign objects. All image,
sprite, and audio contents remain external resources; no asset bytes are
imported. The new source and all used strings are ASCII-compatible UTF-8.

CDG load/free and master.lib graphics/sound calls are external C far-Pascal.
PI drawing/loading/free functions and `frame_delay` retain their genuine
C++ far-Pascal signatures and exact Borland symbols. Their original call
frames are `0` or `0xD30`; no dummy bodies are supplied.

Private integration packet: `.analysis/op-title-boundary-review.json` and
`.analysis/op_title_bindings.asm`. The context is address-only and supplies no
source-owned DATA/BSS, instructions, or `.stack`. A natural negative control
changes `frame_delay(16)` to `frame_delay(15)` in `op_animate`, altering the
real pre-fade pause without an ABI/layout change.

No compilation or reconstruction acceptance is performed by this packet.
Cached calibration locations are routing evidence; two fresh focused builds,
full raw bytes, ordered fixups, OMF integrity, and compiled negative rejection
are still required for exact acceptance. DATA observation remains separate
from code credit and standalone executable reconstruction.
