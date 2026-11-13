# Generic Boss — complete shared hit, phase and defeat behavior

The original shared Boss implementation is fully covered by three complete
CODE scopes and one initialized-DATA scope:

| Accepted scope | Original range | Extent | Authored content |
| --- | --- | ---: | ---: |
| Six generic Boss helpers | `1FA51..1FBB1` | 352 bytes | 352 CODE bytes, 6 functions |
| Item-drop table | DS `1FBE..1FC8` | 10 bytes | 10 initialized DATA bytes |
| `boss_defeat_update(unsigned int)` | `1FBB1..1FD4F` | 414 bytes | 414 CODE bytes, 1 function |
| `boss_hittest_player()` | `1FD4F..1FD7A` | 43 bytes | 43 CODE bytes, 1 function |

The complete original CODE extent is `[1FA51,1FD7A)`, **809 bytes** across
eight functions. The six helpers and the 10-byte table are accepted separately
from the complete defeat and collision functions. No padding or target-byte
copy is credited.

## Six helper functions

| Function | Bytes | Behavior |
| --- | ---: | --- |
| `boss_hittest_shots_damage()` | 63 | Temporarily enables Boss shot collision, plays the hit sound, restores the flag and checks player contact |
| `midboss_hittest_shots_damage()` | 64 | Sets the Midboss hitbox, plays the hit sound and restores the collision flag |
| `boss_hittest_shots()` | 42 | Applies per-frame damage and tests the phase HP gate |
| `boss_hittest_shots_invincible()` | 18 | Performs the hit test without applying returned damage |
| `boss_items_drop()` | 85 | Selects five power or point drops and places them in the original Boss-sized region |
| `boss_phase_next()` | 80 | Runs the optional small explosion/drop path, advances phase, resets mode/pattern count and transfers HP |

The item-drop table contains the original five-entry power and point rows.
Its 10 signed-byte enum values are initialized DATA, not code or opaque assets.
The phase transition preserves the original timeout condition: bullets and
items are cleared/dropped only for a non-`ET_NONE` transition that did not
already time out.

## Defeat choreography

`boss_defeat_update()` is the complete 414-byte far-reaching shared state
machine used by the stage Boss controllers. The small defeat phase triggers
sound 13 and the original circle/vertical bursts at their frame gates. The big
explosion starts the defeat animation and player invincibility; shake runs only
while `phase_frame < 12`, alternating ±4 pixels on the original two- and
four-frame clocks. Slowdown is 2, the kill sprite advances every eight frames,
and the final palette tone is 60. The dialog, Extra Stage and final-stage
all-clear reward paths remain distinct. The fade stores the stage score,
leaves the overlay and fades the song with parameter 10; the next-stage handoff
waits one frame.

The pinned TH05 target does not contain the reference-only
`score_delta_commit()` call. The accepted source follows the actual original
fadeout branch. Its source-level `optimization_barrier()` is the genuine
pinned-reference empty inline call at the Extra Stage all-clear path; it keeps
the two original all-clear call sites distinct without emitting instructions.

The big explosion is always circular. The former
`boss_defeat_explode_big(type, bonus_units)` macro accepted an unused `type`
argument, even though its body always called `boss_explode_big_circle()`. The
shared API now says what it does:

```cpp
boss_defeat_explode_big_circle(bonus_units);
```

The macro still gates bullet-zap activation and score bonus on the existing
`boss.phase_state.defeat_bonus`, advances phase, installs the kill sprite and
resets the phase clock. It adds no runtime function or state.

## Player collision leaf

`boss_hittest_player()` is the complete original 43-byte near function. Its
rectangle test observes the actual DOS `_AX` (X) and `_DX` (Y) pseudoregisters
in the original argument order. The Boss dimensions are each 64 pixels, so
the original half-radii are 32 pixels. The player-hit flag is written only on
positive overlap. The canonical body is shared through
`collision_body.inl`; it contains ordinary source expressions and real
register intrinsics, not emitted instruction text.

## Focused evidence

The 2026-11-13 shared-header API clarification recompiled the generic helpers,
10-byte DATA table, full 414-byte defeat function, 43-byte collision leaf and
all accepted consumers of `generic.hpp`. **18 complete CODE/DATA owners**
passed two native Borland/TLINK producers with original raw bytes and ordered
fixups; each selected batch's compiled negative was rejected. Receipts:

- `.analysis/unit-replays/gpt-web-generic-boss-circle-data-20261113/receipt.json`
- `.analysis/unit-replays/gpt-web-generic-boss-circle-extra-data-20261113/receipt.json`
- `.analysis/unit-replays/gpt-web-generic-boss-circle-code-20261113/receipt.json`

This is a source/API clarification only: the original 809 CODE bytes and
10 DATA bytes retain their existing owners and receive no duplicate credit.
