# Shinki B/C spinline motion: exact 19-function background family

The full original-order `background.cpp` reproduces the **3,254-byte / 19
function** MAIN Boss-background contribution including two already separately
accepted callbacks. Both the falling-particle type B and rising-particle
type C use the same genuine line-set motion protocol:

- Shift each line's history forward and integrate the current central Y
  position from that set's own vertical velocity
- Apply that type's distinct vertical acceleration or deceleration, without
  sharing or reordering the actual velocity condition
- Advance the common center-X/angle spiral, increment the line-set index,
  advance the pointer, and reverse the lateral delta for the next set

The maintained source now names the shared prepare/advance operations, but
keeps the two unique velocity conditions and separate top/bottom formation
logic. It introduces no new compiled helper, state, delay or synthetic byte.

Because `background.cpp` is one real original-order compiler family,
**all 17 affected accepted units** were recompiled under the focused
incremental dependency plan, not just the two edited B/C callbacks. All 17
passed *both* independent Borland/TLINK producers, the full raw target
comparison, original MAP/OMF identity, ordered loader relocations and a
compiled semantic negative. Existing independently accepted particle and
hexagram renderers are not counted again. Focused evidence:
`.analysis/unit-replays/gpt-web-shinki-spinline-bc-complete-family-a/receipt.json`.

This improves the natural source of a major Boss graphics family; it adds no
duplicate authored CODE credit and did not run a full cold replay.
