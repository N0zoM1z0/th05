# Generic player/boss collision: exact original-register C++

## 2026-11-10 accepted original-register complete collision

The complete original `[1FD4F,1FD7A)` **43-byte** `boss_hittest_player()`
now passes the real compiler's original bytes and empty ordered relocation
stream twice, with its own compiled hit-result mutation rejected. The original
ReC98 `th04/main/boss/boss.cpp` gives **explicit `_AX`/`_DX` hardware register
lvalues**, not two ordinary local integer variables. Reintroducing these real
signed X/Y registers produces the native `MOV AX`/`MOV DX`, two `SUB`s and
inclusive `ADD/CMP/JA` overlap, with the same 43 raw bytes and BP frame.
The formerly natural 46-byte BX/DX versions were semantically close but
incorrect as source provenance. They remain retained as failed history above.

The canonical function body is now in `src/main/boss/collision_body.inl`,
used by both the standalone `collision.cpp` wrapper and the real original-order
`generic.cpp` unit. `#include <dos.h>` supplies `_AX`/`_DX`, and no inline
assembly, instruction bytes, inert hints, register compiler switches, DATA,
BSS or code padding is introduced. Original frame is `main_03`/CS `1527`,
with DGROUP DS `209D`, player X/Y from `36D2/36D4`, boss X/Y from
`5ABA/5ABC` and hit byte at `36F3`.

The new accepted `main-boss-player-collision` full function lies immediately
after the now-accepted 414-byte Boss defeat controller. Together with the
previous six-helper 352-byte CODE scope they now cover all three original
non-overlapping CODE contributions (352+414+43=**809 exact bytes**). The
combined image's raw CODE is byte-for-byte exact, while formal fixup evidence
is retained **per complete source segment/function**, not by sorting across
independent OMF segment contributions. The existing 10-byte item-drop DATA
owner stays exact and is not counted as new code.

Focused exact receipt:
`.analysis/unit-replays/gpt-web-main-boss-collision-43-and-neighbors-20261110/receipt.json`.
The newly selected collision and all three dependent accepted units were
built twice and compared for native complete raw/fixup identity with meaningful
compiled negative checks. **Only 43 newly accepted C++ instruction bytes** are
credited. Earlier experimental C++ collision results below are superseded.

---

Original MAIN `[1FD4F,1FD7A)` is43 bytes/15 instructions, no NOPs, tables,
padding or relocations. It uses the complete canonical Boss/player motion
objects, unsigned inclusive overlap after adding256, and the real hit byte.

The independent scalar `collision.cpp` preserves reads and calculations while
declaring Y before X. One actual diagnostic producer emits46 bytes, using
BX/DX instead of native AX/DX. An alternative fullSPPoint local emits59 and
spills its coordinates; that experiment remains in its private input snapshot.
Both fail the complete-size gate and receive zero credit. Neither has a second
producer or compiled negative. The original combined candidate is unchanged.

Evidence: `.analysis/native-producers/main-boss-collision-order-a` and
`main-boss-collision-point-a`; joint findings in
`.analysis/scalar-render-followups-root-review.json`. No physical register
hints, ABI changes, padding or byte normalization are used. Further work should
recover genuine source context rather than extend behavior tests.

## 2026-11-10 whole boss-player collision register-allocation trials

The original full collision callback `1FD4F..1FD7A` is 43 bytes with no
fixups. A standalone replay of the maintained natural expression remains 46
bytes: the compiler keeps X in BX and Y in DX, while the native code uses AX
and DX. The three one-byte deltas are the X load, X addition and X comparison.
Seventeen ordinary C++ variants tested declaration/initialization and
subtraction order, register hints, direct Boolean checks and reordered overlap
conditions. The closest 45-byte candidate computes fresh temporary AX values
with different dataflow; it is still not the native full 43-byte function.
Actual single-producer snapshots are under
`.analysis/gpt-web-boss-collision-*-a/`. These trials are not exact acceptance;
no artificial register-body transcript, linker adjustment or partial byte
claim was introduced. The original `collision.cpp` and accepted six-function
generic Boss helper owner remain unchanged.
