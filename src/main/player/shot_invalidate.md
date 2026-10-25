# TH05 shot and hit-sprite invalidation

The independently decoded original complete function is MAIN load
`1337D..133DB`,94 bytes/33 instructions, with no NOPs, compiler tables or MZ
relocations. It is a no-argument near C++ routine and ends with a near RET.
The next actual function begins at133DB. No accepted extent overlaps it.

The semantic donor is maintained TH04 `src/main/player/shots.cpp`'s ordinary
shot invalidation loop; the original TH05 adds its separate24-entry hit-sprite
loop. This source reuses the complete canonical `Shot` (18 bytes),
`hitshot_t` (14 bytes), full12-byte Motion and four-byte point types from
`shot_runtime.hpp` and its canonical dependencies. It changes no shared header.
The two pools begin at DSBA8E/BF56; both previous-position fields are x+6,y+8.
All64 active shots and all24 nonzero-age hit sprites invalidate their complete
previous16×16-pixel rectangles. No geometry, flags or unused fields are dropped.

The existing canonical near Pascal `tiles_invalidate_around(y,x)` interface is
called directly. Its actual BAD2 entry reads x at SS:SP+2, y at+4 and has a
RET4 path atBAE8, matching the original two signed-subpixel-word calls. No new
function-pointer ABI, CF facade or structure-return adaptation is introduced.
The actual pixel-sized `tile_invalidate_box` remains its complete canonical
four-byte object at DS3502; both members are assigned separately.

The symbol-only binder reserves the true MAIN01 frameAE1, SHARED14AB and
DS209D. Foreign empty compiler segments retain their actual group names. It
supplies only one real helper label and three real data-object labels, with
all ORG extents outside the complete function. It supplies no instruction,
state value, stack, inside-function padding or target bytes.

The focused `main-shots-invalidate-a` replay passed two independent fresh
producers: all 94 bytes, complete OMF contribution, original placement and
empty ordered relocation stream match. Its own compiled negative changes
rectangle width16 to15 and fails the comparison. The ledger credits94 authored
instruction bytes and one complete function. The Shot pointer retains the
ordinary `register` declaration present in the maintained TH04 donor; the
separate hit-sprite pointer has no added allocation hint.

Private `.analysis/shots-invalidate-boundary-review.json` pins the original
instructions, complete ABI and target identities. The accepted receipt is
`.analysis/unit-replays/main-shots-invalidate-a/receipt.json`. This bounded
acceptance does not establish historical original source or whole-program
placement independently of the explicit foreign bindings.
