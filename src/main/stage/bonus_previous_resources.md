# MAIN stage-clear No Miss/No Bomb previous-resource counters

The decoded original MAIN `[222B4,222B6)` is one complete two-byte C
initialized-DATA contribution. The native original assembly lists two
consecutive byte globals (`byte_22274` and `byte_22275`) following the
explosion state and an alignment byte; their use identifies them as the
*previous stage* Miss and Bomb counters. The real accepted
`stage_clear_bonus()` (561 bytes) and `stage_allclear_bonus()` (579 bytes)
each compare `resident->miss_count` against the first byte and
`resident->bombs_used` against the second, then store the current
resident counters for the next stage. A No Bomb reward is granted only
if the current Bomb count matches **and** there has also been No Miss.
These are actual mutable stage-scoring latches, not a CP932 title image,
static score bonus string, or BSS-only temporary.

The maintained C names `bonus_previous_miss_count` and
`bonus_previous_bomb_count` are those already used by the separately
accepted source of both complete bonus renderers. Their 1-byte widths
and native zero initializers exactly reproduce the original two-byte
run, without merging the preceding uncredited zero `[222B3,222B4)`
which is an original alignment byte, or the succeeding near-pointer
array starting at `[222B6,222C6)`.

The binder places the natural near-C data at DGROUP `209D:18E4`,
providing only the outside native MAIN CODE frames and preceding DATA
prefix—not the candidate bytes, source functions or any fixups. Two
independent pinned Borland C producer rounds match the original raw
bytes, OMF/LEDATA and MAP DATA scope, with the genuine empty ordered
MZ fixups. The actual compiled mutation changes only the previous
Bomb count from zero to one and is rejected:
`.analysis/unit-replays/gpt-web-stage-bonus-previous-counts-a/receipt.json`.

No CODE is recredited and no full MAIN cold replay is executed.
