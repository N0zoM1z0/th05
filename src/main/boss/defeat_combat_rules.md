# Exact generic Boss defeat/clear and near player-collision protocol

TH05's complete native source-owned **414-byte**
`boss_defeat_update(unsigned int)` and **43-byte** `boss_hittest_player()`
are independently accepted physical functions, not tentative stubs. The
former is the game-wide end-of-Boss state machine used by multiple
complete Alice, Shinki, Mai/Yuki, Louise and Yumeko Boss controllers.
The latter is the genuine player/Boss rectangle collision leaf that
observes physical `AX` (X) and `DX` (Y) pseudo-registers. Their source
now shares compile-time-only `defeat_combat_rules.hpp` for the remaining
original physical timing and contact geometry; no new BSS, DATA or
helper body has been introduced.

**Defeat choreography.** The first small explosion uses sound 13 and
advances to the original vertical burst and big-explosion thresholds
already named in `generic.hpp`. After the big explosion, screen shake
runs only through frame 11 (the original `frame < 12`): X alternates
±4 pixels with frame modulo 2, and Y stays negative for mod-4 residues
0/1 before alternating positive. The original slowdown factor is 2,
and the defeated Boss sprite advances once every eight frames. The
post-defeat code retains the original darkening tone 60 and both
separate all-clear reward paths. The final fade uses the real song-fade
parameter 10; the next stage handoff pauses for exactly one frame.
The player's invincibility, homing clear, resident score write and
stage-selection branches are left untouched. The large explosion is always
the fixed circular Boss explosion: `boss_defeat_explode_big_circle(bonus_units)`
has no explosion-type input because the original transition never selected
another shape. It still gates the bullet-zap activation and score award from the same
one-byte `boss.phase_state.defeat_bonus` lifetime.

**Collision geometry.** The original DOS-style leaf subtracts the player
coordinates in `_AX`/`_DX` before calling
`overlap_wh_inplace_fast(_DX, _AX, ...)` in that *actual* register order.
Each original Boss dimension is 64 pixels, hence each tested physical
half-radius is 32 pixels. The two radius names preserve their
respectively original BOSS_H and BOSS_W expressions; the implementation
intentionally does not swap pseudo-register arguments or introduce a
normal C++ temporary (known to change Borland's 43-byte register
allocation). The real `player_is_hit` lvalue remains written only on
positive overlap.

The original `optimization_barrier()` source spelling in the accepted
414-byte function is **unchanged**; the pinned ReC98 source has that
specific genuine inline invocation, and its compiler-generated source
layout is required to keep the two real all-clear calls separate.
No new optimizer barrier, instruction text, linker filler, game asset or
extra control-flow branch was inserted by this semantic edit.

The two edited canonical source files are
`src/main/boss/generic.cpp` and its shared original near-collision
body `src/main/boss/collision_body.inl`. A bounded native replay of
**every affected accepted unit** — 352-byte generic functions,
10-byte item-drop initialized DATA, 414-byte defeat controller and
43-byte collision function — matches two pinned Borland producers,
original complete OMF/MAP boundaries, literal ordered MZ fixups and
the existing meaningful compiled negatives:
`.analysis/unit-replays/gpt-web-generic-boss-defeat-and-collision-a/receipt.json`.
These bytes were already accepted and are not credited again. No full
MAIN or foreign-library replay was run.


## 2026-11-13: make the fixed circular explosion API honest

The original `boss_defeat_explode_big(type, bonus_units)` macro accepted a
`type` argument but never read it; its only body operation was
`boss_explode_big_circle()`. The generic Boss controller now calls
`boss_defeat_explode_big_circle(bonus_units)`, with the dead type parameter
removed. This does not add a runtime helper or alter the 414-byte callback.
The actual callback and all 17 additional shared-header code/data consumers
were recompiled in two focused native rounds. All 18 complete owners preserve
original raw bytes and ordered fixups; the compiled negative controls are
rejected. Receipts are recorded in `src/main/boss/generic.md`.
