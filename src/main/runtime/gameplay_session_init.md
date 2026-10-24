# New-game session initialization

This natural C++ owner reconstructs the complete original MAIN function at
`[0xB063,0xB237)`, named `gameplay_session_init` by its maintained TH04
donor. It initializes a new game's resident statistics, character dispatch,
score, lives, bombs, movement speeds, difficulty and performance limits.
It is distinct from the stage-session initializer beginning at `0xB237`.
Coordinates are offsets in the MZ program image of locally attested MAIN,
SHA-256 `c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
The actual frame is `0AE1`, group `main_01`.

The complete extent is 468 bytes:450 instruction bytes through the near RET
at `0xB224`, followed by two semantic compiler switch tables. The rank table
occupies relative `[450,460)` and the character table `[460,468)`. Every table
entry and direct branch destination was checked against original instruction
starts. There are no padding bytes or original MZ fixups. The tables must be
generated from the ordinary source switches; no table values are supplied by
source or scaffold.

The donor is the sibling TH04 reconstruction's
`src/main/core/gameplay_session_init.cpp`; ReC98 `b6ba5b0a`'s `th05_main.asm`
provides additional semantic evidence. Original TH05 operands, complete
return/table boundaries and behavior were independently reviewed. Donor
acceptance does not transfer to this source.

The unchanged complete128-byte `resident_t` supplies the actual fields.
TH05 copies its character index directly and publishes credit bombs/lives
in the real runtime byte globals. It sets initial power and dream to1.
The four characters use Q12.4 speed pairs56/40,64/48,72/52 and56/40,
respectively, and genuine near-Pascal bomb callbacks. The selected shot row
comes from the existing4-by10 table of near C++ shot functions. Its complete
80-byte declaration and20-byte row preserve the real index calculation;
the foreign table contents are not copied or credited.

Demos1 through4 start at performance40/Lunatic, later demos at32/Extra,
with turbo enabled. Ordinary Extra stage uses32/Extra/turbo; other games
read the resident difficulty and turbo settings. Difficulty selects TH05's
actual full-dream item value, graze value, minimum/maximum performance and
one of the frozen accepted bullet-tuning functions. Hard and Lunatic reset
initial performance to44 and48. TH04's separate regular/special bullet-adder
callback assignments are absent here.

There are only three direct calls: near Pascal `bb_txt_load` at `0xE4B6`,
near C++ `score_reset` at `0xCFC6`, and near C++ `hiscore_load` at `0xC9A4`.
The bomb callbacks belong to main_01; the tuning callbacks retain their
real main_03 first-declaration context. Word movement lengths and score
values, byte difficulty/performance fields and both callback-pointer widths
are declared and checked. The source uses no hardware operation, far-call
relaxation, Motion return adaptation, register template, inline assembly,
source padding or inactive optimization expression.

Private integration inputs are
`.analysis/gameplay-session-init-unit-proposal.json`,
`.analysis/gameplay-session-init-bindings.asm`, and
`.analysis/gameplay-session-init-boundary-review.json`.
The outside-only binder defines symbols rather than implementations or data
values, and allocates no stack. The proposed negative changes initial dream
from1 to2, affecting actual game state. No initialized DATA or BSS belongs to this code owner.

Accepted focused replay `main-gameplay-session-init-a` proves all468 bytes
from two fresh deterministic producers, including both generated switch
tables and the original empty ordered relocation list. The compiled
initial-dream mutation from1 to2 changes output and is rejected. The receipt
is `.analysis/unit-replays/main-gameplay-session-init-a/receipt.json`. This
is owner-level negative coverage, not independent controls for each switch
branch. Accepted source and binder remain frozen.
