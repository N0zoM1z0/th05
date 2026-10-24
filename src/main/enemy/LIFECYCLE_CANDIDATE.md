# Enemy lifecycle candidate

This is maintained natural C++ adapted from the TH04 reconstruction's
`src/main/enemy/enemies_add.cpp`, `enemies_update.cpp`,
`enemies_invalidate.cpp`, and `src/main/stage/std_run.cpp`. Their exactness does
not transfer. TH05 behavior and operands were reviewed independently against
this repository's locally attested MAIN executable. ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47` supplies additional disassembly and
format evidence, not accepted compiler bodies. Its MAIN IDA input digest differs
from this supplied executable; original addresses below come from our artifact.

| Candidate | Original load-image range | Complete functions | CODE bytes |
| --- | --- | --- | ---: |
| `ENEMY_SPAWN_TEXT` / `main_03` | `16A7A..16BCF` | `enemies_add`, `std_run` | 341 |
| `ENEMY_UPDATE_TEXT` / `main_03` | `16BE7..16E27` | `enemies_update` | 576 |
| `ENEMY_INVALIDATE_TEXT` / `main_01` | `C180..C1AB` | `enemies_invalidate` | 43 |

These are source candidates; formal acceptance is recorded separately. All 960
bytes must be compared. Two original far-call relaxation NOPs at `16B7A` and
`16D13` receive no authored instruction credit, leaving at most 958 instruction
bytes. No code tables, initialized DATA, or BSS belong to these owners.

The canonical `enemy.hpp` retains every real field of the 64-byte TH05 enemy,
including its complete bullet template and unused tail. No accepted definition
is changed. TH05's STD spawn record is eight bytes: script index, unaligned
word x/y coordinates, item, subtype, and an unused byte. The source advances the
real far cursor's offset word, preserving its segment and wrap behavior. A
zero spawn count follows the actual byte do-while behavior. The stage VM is a
real far Pascal callback.

TH05 changes from the donor include its packed clipping byte, subtype,
Lunatic autofire initialization, seven sparks per kill, unsigned score widening,
IT_NONE guard, homing selection without TH04's player-height cap, and byte-based
stage-dependent dream recharge. Dream is the byte at DS:`36F6`; the nearby byte
at `36F5` is not substituted. Gone/killed counters are distinct word globals.

The foreign 24-byte template-copy helper at `16BCF..16BE7` remains outside all
owned scopes. Its actual argument is a near reference to a 14-byte template,
with Pascal `RET 2`, rather than a reference to the whole enemy. The original
script interpreter also remains external. Its caller at `1543B` calls a helper
at `1538C` and immediately branches on CF. That helper returns through CLC/STC;
it cannot truthfully become a conventional C++ boolean helper. No such helper
body or compiler instruction transcription is introduced here.

The update owner calls the genuine far Pascal sparks API. The stage runner
calls genuine far midboss activation. Their same-group far-call shortening is
left to the actual linker; no handwritten NOP, CALL body, `samecodeseg`, unused
expression, or optimization barrier is present. Motion retains its real
`PlayfieldPoint` return type. Invalidation uses an explicit legacy Borland function-pointer view of the
existing Pascal entry, passing the complete four-byte SPPoint. The real entry
reads x at SP+2 and returns RET4; both interfaces marshal that same frame. The
compiler naturally emits the observed PUSH dword and direct CALL. No shared
accepted header or symbol address changes. This is a Borland ABI adaptation,
not a claim of ISO-portable compatibility between distinct function types.

Configured producer aliases are `th05/en_life.cpp` and `th05/en_inv.cpp`,
GAME=5, BINARY=M, large model, normal `-O -3 -ml`, BP enabled for lifecycle and
`-k-` for invalidation. Owned and foreign first declarations carry explicit
segment/group contexts. Private boundary review and symbol-only binders are
under `.analysis/main-enemy-lifecycle-boundary-review.json` and
`.analysis/main-enemy-lifecycle-bindings/`. They contain no implementation
bytes or initialized data and allocate no artificial stack. They establish a
bounded original-address context, not a standalone game's global layout.

Meaningful negative controls change the spawn autofire interval 128 to 120,
the kill spark count 7 to 6, or invalidation width 32 to 40. Formal acceptance
requires the root worker's two fresh producers, complete raw bytes, ordered
fixups, and compiled negative control.

Private diagnostic `enemy-common-b` preserves an ordered prefix / spawn C++ /
foreign 24-byte ORG / update C++ / tail layout using one real SEGDEF. It still
retains the two far calls rather than shortening them; each complete lifecycle
owner differs at exactly five bytes and one relocation. These owners remain
unaccepted. The invalidation ABI diagnostic reproduces all 43 bytes and no
relocations; it still needs the normal two-positive/compiled-negative gate.

The allocator is also maintained as its own complete natural producer:
`spawn.cpp` includes the same `spawn.inl` body as the lifecycle candidate.
`main-enemy-allocation-a` proves all 252 original bytes at 16A7A..16B76 from two
fresh producers, with unchanged original fixups and a compiled 128-to-120
negative. This uses a complete actual contribution, not a fabricated demangled
C symbol or an interior function slice. The remaining 89-byte STD runner and
576-byte update stay unaccepted. `main-enemies-invalidate-c` separately proves
all 43 original invalidation bytes and its compiled box-width mutation.
