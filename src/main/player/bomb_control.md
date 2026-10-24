# Complete bomb control callbacks

Three independent natural C++ callbacks pass the complete strict oracle:

| Callback | Complete load extent | Instruction bytes | Original ordered fixups |
| --- | --- | ---: | --- |
| Marisa | `[FFB7,10058)` | 161 | `[135,55,27]` |
| Reimu | `[FD6B,FE2C)` | 193 | `[166,86,49]` |
| Yuuka | `[10371,10432)` | 193 | `[166,86,49]` |

Receipts are `main-marisa-bomb-control-a`, `main-reimu-bomb-control-b` and
`main-yuuka-bomb-control-b` under `.analysis/unit-replays/`. Each has two fresh
positive producers and its own compiled final-tone mutation, 100 to 101, which
is rejected. No padding, tables or DATA receive credit through these owners.

The callbacks implement the original frame phases: tile-mask entrance where
applicable, effect drawing, dream decay, stage-dependent scroll restoration,
background callback restoration, tone fade, and bomb completion. Reimu and
Yuuka share the natural maintained lifecycle in `long_bomb_control.inl`, with
real character-specific frame constants supplied by their C++ wrappers. Yuuka
restores the hardware scroll on frame 161; Reimu does so on frame 130. The
shared mask-color byte is the actual object at DS:4444. Active background
rendering and its stored callback remain distinct words at DS:3508 and DS:350A.
Near Pascal callbacks, master.lib far Pascal services, full existing HUD state,
and real foreign effect functions retain their actual interfaces. Bindings
supply addresses only, with all holes outside the complete compiled owners.

The neighboring Mima control candidate has raw-exact 161 bytes in
`main-mima-bomb-control-a`, but its original ordered fixups are `[55,27,135]`
while the standalone producer emits `[135,55,27]`. It remains unaccepted with
zero credit. Relocations are never sorted or normalized. Its full adjacent
natural drawing/control context is a separate candidate requiring new evidence.

Pinned ReC98's `th05_main.asm` corroborates the algorithms. Complete native
original decodes and the actual fresh producers establish boundaries, bindings
and equality independently. Whole-program placement and packing remain open.

The complete Marisa drawing prelude `[FF7B,FFB7)` is separately accepted as
`main-marisa-bomb-draw-b`: 60 instruction bytes, original ordered fixup `[14]`,
two fresh producers and its own initial-tone mutation 196 to 195. Its beam
dispatch writes the canonical unsigned `shot_time` byte to the real blocked
sentinel `FFh`; the backdrop kernel stays a foreign near interface.
