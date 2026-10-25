# Parked shot and hit-animation renderer

The maintained semantic-safe natural C++ candidate targets the complete
original MAIN function
`shots_render` at `[0x13573,0x13617)`,164 instruction bytes, frame `0AE1`,
group `main_01`. Coordinates are offsets in the unrelocated MZ program
image of locally attested MAIN, SHA-256
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
The near RET is at `0x13616`. Every direct branch targets an original
instruction start; no CODE table, padding or MZ relocation belongs to the
complete extent. This owner defines no initialized DATA or BSS.

The unchanged `shot_runtime.hpp` and `reimu.hpp` supply the complete18-byte
Shot,6-byte alive-cache entry and14-byte hit-animation record. The actual
alive cache is at DS:`C4C8`, its unsigned-word count at `C648`, and the24
hit-animation records start at `BF56`. Rendering uses cached positions,
skips the exact `(-999 * 16)` X sentinel, and reads the referenced Shot
only for its base sprite and age. Base plus age parity wraps within an
unsigned byte before becoming the sprite word. Hit-animation ages1 through12
are visible. Signed/unsigned loop comparisons preserve the two original
count domains. TH04's shot-laser path and its direct scan of all Shot records
are absent.

The graphics interface is genuine, as declared by ReC98
`th04/formats/super.h` and the unchanged accepted `explosion.hpp`:
`z_super_roll_put_tiny_16x16_raw` at `0xC07C` takes pixel-left in AX,
VRAM top in DX, an ES VRAM plane, and one Pascal stack word for the sprite.
The original helper reads SS:SP+2 and exits through RET2. Its coordinates
are transported by the existing DX/AX interface macro; ES is set to `A800`.
The vertical transform at `0xDF28` is the genuine near-Pascal word API with
RET2, and `grcg_setmode_rmw` at `0xC1F8` enables the hardware drawing mode.
An ordinary `outportb(0x7C,0)` disables it afterward.

All sprite arithmetic uses natural C++ and an ordinary word local holding
an explicitly byte-wrapped sprite value. The
TH04 donor's CH/CL/AL arithmetic and register-retention template are not
copied. Only actual AX/DX/ES graphics-argument transport remains; there is
no fake fastcall aggregate, function-pointer cast, Motion return, CF
protocol or custom instruction emission. Actual producer inspection must
check that ordinary sprite argument lowering preserves the real hybrid
interface. The first semantic-safe word-local producer was173 bytes rather than164;
its ordinary word spill and argument pushes account for the nine-byte
difference. It preserves the real AX/DX protocol by pushing the already
widened word directly from its local slot. That failed producer and source
snapshot remain retained at `main-shots-render-a`.

The one authorized byte-local trial at `main-shots-render-b` produced175
bytes and is abandoned. Actual native instructions prove a semantic API
failure at both calls: after AX=left is calculated, ordinary byte-to-int
argument promotion loads AL and clears AH before PUSH AX. The raw helper
therefore receives left=sprite; DX remains the correct scroll top and ES
the VRAM plane. The raw int/RET2 API and coordinate macro were unchanged.
Root restored the original safe int source exactly, SHA-256
`0c30efdc7934ff68ca81886f488d4ef4a36ecb1e6ab444d6871c57bfaa7b2f2d`.
No further type or physical-register variant, interface disguise, padding
or allocation hint is proposed. Neither candidate is exact or credited.


Semantic provenance is the maintained TH04 reconstruction's
`src/main/player/shots.cpp` renderer. Pinned ReC98 `b6ba5b0a`'s
`th05_main.asm` lines6608-6687 supplies additional TH05 behavior evidence.
Actual original records, calls, complete boundaries and branch destinations
were independently checked. Donor acceptance does not transfer.

Private integration inputs are `.analysis/shot-render-unit-proposal.json`,
`.analysis/shot-render-bindings.asm`, and
`.analysis/shot-render-boundary-review.json`. The outside-only binder supplies
real entry/state symbols and no instructions, resources, artificial stack
or owned padding. Both runs stopped after their first producer at the
boundary-size gate: neither reached a second producer or compiled negative.
The proposed parity-mask mutation1-to0 was not compiled and is not claimed
rejected. Full exact-acceptance requirements remain unmet. Detailed native
forensics are retained in `.analysis/shot-render-first-producer-review.json`
and `.analysis/shot-render-byte-protocol-review.json`.
