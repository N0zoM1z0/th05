# Bullet and Gather dirty-tile invalidation: complete native ASM

The original TH05 MAIN function `bullets_and_gather_invalidate()` occupies
`[E40E,E4B6)`, exactly 168 instruction bytes with one near RET, no native
NOPs, switch table, initialized DATA/BSS or MZ relocation word. Its callers
use near cdecl `void()`; the routine preserves SI/DI and deliberately changes
the shared dirty-tile rectangle at DS `3502`.

The procedure first processes 180 eight-pixel pellets from the authentic
32-byte `bullet_t` records at DS `5F2A`, except during zap or bullet clearing.
Then it examines up to 220 16-pixel bullets, expanding the dirty rectangle
for bullet spawn states greater than `BSF_GRAZED`. When the first loop is
skipped, the original count deliberately expands to 400 so both bullet
classes are covered; no extra reset or invalid-input behavior is introduced.
Finally it walks all sixteen 38-byte `gather_t` records at DS `9BFA`, using
the actual radius field at offset 14 to set equal dirty width/height and
invalidating the previous center at offset 6. The routine calls the existing
near-Pascal four-byte tile invalidator at MAIN `BAD2`, with no fabricated
function body, resource payload or extra stack.

The full register-driven semantics have a maintained, explicit ASM donor in
pinned ReC98 `th04/main/bullets_gather_inv.asm` with its real GAME5 branch.
The canonical record sizes and flags are corroborated by the independently
accepted local `bullet/update.hpp`, `bullet/spawn_types.inc` and
`gather/gather.hpp`. The maintained source names the actual record offsets,
state machine, and box dimensions; it does not copy native opcode data.
The original assembly classification follows this retained family and the
actual 386 register/string/call instruction structure, not the candidate
filename alone. Literal ZUN source and assembler identity are unproved.

## Accepted original-register source

The focused receipt
`.analysis/asm-replays/gpt-web-bullets-gather-invalidate-a/receipt.json`
passes two independent genuine TASM32/TLINK builds and comparison of all
168 original bytes, the empty native ordered relocation list, the real
`main_01` CODE group/`209D` DGROUP frames, source-owned OMF LEDATA and
actual MAP boundaries. The semantic negative decreases the first pellet
count from 180 to 179 and is assembled and rejected. The native boundary
and source-origin proof is
`.analysis/gpt-web-bullets-gather-invalidate-native-review.json`.

Explicit adoption adds exactly **168 reviewed original-ASM instruction bytes**,
zero padding, and no DATA, BSS, C++ source credit or other function bytes.
Previously accepted bullet/gather/tile owners and inputs remain unchanged.
