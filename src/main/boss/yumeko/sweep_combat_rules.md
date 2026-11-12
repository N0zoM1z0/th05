# Yumeko sword-border sweep and original complete 884-byte Boss controller

The original **321-byte** near-C++ `yumeko_pattern_sword_sweep()` is one
complete physical sword and accelerating-volley attack, not part of the
still-unaccepted 283-byte natural sword updater. Its actual live
`sword_template`, 26-byte sword pool, `boss_statebyte[13..15]`, and
`boss2.pos.cur.y` position are unchanged. The new
`sweep_combat_rules.hpp` names its original source-level gameplay
clocks and projectile geometry without allocating any replacement
state, code-generation barriers or static asset arrays.

On charge frames before **32**, the attack gathers colored circles
7/6 with a 16-frame lead and initializes its projectile templates at
frame **16**. The blue directional bullet pattern 52 fires five shots
with difficulty-dependent angle spacing **24/16/12/10**; its speed is
**128 subpixels**. The sword itself twirls for **32 frames**, flies at
64 subpixels, and uses original vertical gaps **40/30/24/16 pixels**
according to the difficulty. After charging, the real Sword26 spawn
alternates between the two existing playfield edges at X=16 and
X=`PLAYFIELD_W-16`, at an **eight-frame** cadence, advancing the live
Y coordinate by its 8-bit spacing shifted four Q12.4 bits. Once that
position reaches **376 pixels**, it restarts the actual random Y
origin and switches to the second part of the attack.

During the second half, the source emits regular bullets **every four
frames**, increasing template speed by eight subpixels per volley. At
speed above **96 subpixels**, the existing bullet speed resets to eight,
SE15 plays, and the shared sweep-round byte increments. After its
original five-round limit the method resets the sweep count and
returns without adding an extra volley. All near callback order and
byte-aliased signed arithmetic remain original.

The complete **884-byte far-Pascal `yumeko_update()`** keeps the
physical HP ladder and phase-state machine intact. Its initial HP is
8300, and its final circular-ring special bullets still have a real
two-turn maximum and alternating parity bit. The shared rule header
therefore links the sword sweep's exact phase behavior with the
unchanged complete Boss renderer, sword update call site and
original compiler-generated 22-byte phase switch table. The checked
alignment zero is never counted as authored CODE.

Both affected complete native original scopes were compiled twice
with the pinned Borland C++ toolchain. All **321+884 CODE extent bytes**,
actual OMF/MAP bounds and ordered MZ fixups match the original, and
both meaningful compiled negatives are rejected: the sweep volley
recycle threshold 96→112 subpixels and the final special bullet
turn count 2→3. Focused successful proof:
`.analysis/unit-replays/gpt-web-yumeko-sweep-and-884-boss-b/receipt.json`.

The first attempted text transformation halted **before writing** its
source changes because the old compound gather expression required
one ordered replacement. Its baseline-only compiler pass is not
claimed as proof. The `-b` receipt above compiles the actual changed
sources and rejects both controls. No already accepted CODE bytes
are double-counted; no complete MAIN cold replay ran.
