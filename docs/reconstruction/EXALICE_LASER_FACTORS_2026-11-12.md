# EX-Alice complete laser attacks: two real source protocols

The complete four-function `main-exalice-laser-patterns` source contributes
645 original bytes. Its two fixed-laser fan launches now share
`EXALICE_FIXED_AIM_AND_SPAWN(aim_offset)` to compute the actual player
angle from the genuine laser origin and consume exactly one 16-bit laser
slot. The two real angles (right and converted left) remain distinct.

The sweeping-laser callback now names a shared `EXALICE_SWEEP_TURN` rule
for advancing one step, switching direction only at its original limit
and dispatching the real shootout. Forward and backward comparisons retain
their original unsigned-byte wrap and state transitions. The bouncing ring
and speedup fan callbacks were not changed.

Focused complete-unit replay:
`.analysis/unit-replays/gpt-web-exalice-laser-two-directions-20261112-a/receipt.json`.
Both genuine Borland/TLINK producers reproduced **645/645 bytes** and
original ordered MZ fixups `[422,98]`; the compiler negative that changes
laser growth age 47→48 was rejected. The accepted source owner has been
refreshed without assigning duplicate authored CODE credit. No full cold
replay or related nonaffected Boss controllers were rebuilt.
