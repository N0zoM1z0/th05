# Generic player/boss collision candidate

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
