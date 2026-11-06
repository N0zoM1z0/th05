# Cheeto renderer

MAIN `[12F2B,12FF5)` is one complete 202-byte C++ function, with no table,
padding, relocations or owned DATA/BSS. The existing complete 26-byte head,
82-byte trail and custom pool types are reused. Rendering preserves all seven
trails, reverse traversal of nodes 15 through 1 in steps of two, clipping,
negative-Y wrapping, head rendering and the absence of stage scrolling.

The real CODE frame is `0AE1`/`main_01`, DS `209D`. AH supplies GRCG color and
ES selects VRAM. The external `cheeto_put(int,int,int)` retains its genuine
C fastcall AX/DX/BX interface and actual `@cheeto_put` symbol. Its body remains
external. The maintained source has no instruction emitter or assembly body.

The initial natural producer was 200 bytes: ENTER replaced the original
PUSH BP/MOV BP,SP/SUB SP sequence, and the two register locals were swapped.
The documented `-G` speed option restores the original prologue. An ordinary
register-qualified node index and ordinary trail pointer restore allocation;
no local is bound to a named machine register. The complete resulting 202 raw
bytes match, including both clipped drawing paths.

`main-cheetos-render-a` passes two deterministic producers and the original
empty relocation list. The shared compiled node-step mutation is rejected.
Receipt: `.analysis/unit-replays/main-cheetos-render-a/receipt.json`, SHA-256
`2fd25646e88e17441e691bacda9c96b39d50c27ff9b4ab4b1e0d70613b94ad46`.
Native boundary/ABI review: `.analysis/cheetos-render-boundary-review.json`.
Pinned ReC98 `b6ba5b0a` is supplemental semantic evidence; no reference
acceptance or instruction body is transferred.
