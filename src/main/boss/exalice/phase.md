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

## Bomb immunity and phase-reset contract (2026-11-12)

The original EX-Alice far hit-gate and near-Pascal phase-helper now share
`bomb_phase_protocol.hpp` with the full 18-state Boss controller. The
bomb collision gate refreshes the existing byte to **39** whenever
bombing is active; actual damage checks are delegated to the original
`boss_hittest_shots()` only when that byte is zero, otherwise the full
`int far` return is zero. The controller decrements the same physical
byte at the beginning of each update. No new protection timer or scratch
byte is introduced.

`exalice_phase_next()` keeps its original per-phase rule: optional
explosion and item-dropping bullet zap on an untimed transition,
followed by the timeout latch, phase increment, real phase-frame zero,
reposition mode, zero prior-pattern counter, and copying the previous
HP boundary before installing the next. The zero values are now
separately named for the timer, frame, and prior pattern count. This is
physical state recovery, not a substitute helper or a claimed new phase.

The paired focused replay at
`.analysis/unit-replays/gpt-web-exalice-bomb-phase-protocol-a/receipt.json`
passes two independent native Borland builds with complete **111/111**
original prefix bytes (33-byte far gate plus 78-byte phase helper),
full OMF/MAP boundaries, exact empty original MZ fixups, and the
compiled source mutation of immunity 39→40 rejected. The adjacent real
1,060-byte Boss controller is also exact under its separate accepted
scope. None of these previously accepted CODE bytes is counted twice.
