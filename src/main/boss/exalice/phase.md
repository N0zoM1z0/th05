# EX-Alice shot gating and phase transition

Two complete functions fill original MAIN `1A1DB..1A24A`: the far-cdecl
shot wrapper (33 bytes, 14 instructions) and near-Pascal phase transition
(78 bytes, 25 instructions, RET4). All direct branches, complete returns,
global operands and the empty ordered MZ relocation stream were reviewed
natively. No tables, padding, initialized DATA or BSS are owned here.

Bombing refreshes 39 frames of boss immunity. Once immunity expires, the far
wrapper returns the real near collision helper's AL boolean widened to int;
otherwise it returns zero. Phase transition optionally explodes and enables
item-dropping bullet zap on an untimed completion, then advances the phase,
clears frame/mode/pattern count, clamps HP to the previous phase threshold
and installs the next threshold. These are genuine state changes and helper
calls, with no target instruction body supplied by the binding scaffold.

The canonical full Boss, explosion enum and zap union are unchanged. The
existing generic phase transition supplies a natural semantic comparison;
EX-Alice specifically enables bullet zap rather than the ordinary clear timer.
ReC98 `th05_main.asm` far shot wrapper and `th05/main/boss/bx.asm` corroborate
the behavior. The latter is reconstructed as natural C++, without carrying
its assembly instruction body into authored code.

Original near calls use frame1527; DS is209D. The binder anchors the actual
foreign explode, collision and item-drop APIs and the paragraph tail after
1A250. It emits no instructions, values, stack or hole in the 111-byte owner.
`main-exalice-phase-a` passes two fresh deterministic complete raw/ordered
positives. The real immunity39→40 source mutation is compiled and rejected.
Both functions and111 instruction bytes are accepted.
