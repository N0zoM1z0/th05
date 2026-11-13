# Yumeko sword-border sweep and original complete 884-byte Boss controller

The original **321-byte** near-C++ `yumeko_pattern_sword_sweep()` is one
complete physical sword and accelerating-volley attack, not part of the separately
owned 283-byte sword updater. That updater's maintained fully natural C++
source now matches exactly in two original-order context producers; its bytes
remain credited only to the reviewed-ASM owner. The sweep's actual live
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


## 2026-11-14: sweep cycles carry side, speed and aim state

The sweep's `round` byte at Boss scratch offset 13 is a cycle selector, not a
one-shot completion flag. Charge frame 16 initializes `round=0`, `side=0`,
the rank spacing, the random starting Y, and bullet speed 128. The sword half
fires every eight frames, toggles the side by `0x80` after each sword, and
adds the selected spacing to Y before testing the 376-pixel boundary. For the
original random Y range 0..31, one sword sweep emits 9/10 swords on Easy,
12/13 on Normal, 15/16 on Hard, and 22/23/24 on Lunatic. The final side is the
initial side XOR the parity of that count; the next cycle does not reset it.

The first aimed-bullet half begins after the sword sweep sets `round=1`.
Bullets fire every four frames. The speed test is strictly `>96`; when true,
speed resets to 8, SE15 plays, and `round` increments. The next bullet then
adds 8, so each full burst emits speeds **16, 24, ..., 104** (12 bullets).
The first cycle starts from charge speed128, so its first bullet performs a
reset and starts the first burst immediately. Four 12-bullet bursts are emitted
(48 bullets total); the fifth reset advances `round` to 6, resets it to zero,
plays SE15, and returns before aiming or firing an extra bullet. That terminal
reset leaves speed at 8 and leaves the last aimed angle untouched.

A later cycle starts with `round=0` but deliberately retains speed8 and the
previous bullet angle. Its sword half again carries the current side and chooses
a new random Y. After that sweep, the first 12-bullet burst advances speed from
8 to 16..104 without a new sound or aim calculation. Four subsequent reset
boundaries produce four more bursts, then the terminal boundary returns: a
steady-state cycle therefore emits **60 bullets**, has five SE15 events (four
before bullet-producing burst starts plus the terminal no-shot event), and
retargets only at those four reset boundaries. The fifth reset still plays
SE15 before returning without a bullet or aim update. No per-cycle reset of side,
speed or angle exists in the original leaf.

`tests/test_yumeko_sweep_cycles.py` models the rank-dependent sword counts,
side parity, first-cycle 48-shot sequence, later-cycle 60-shot sequence, and
the terminal no-shot reset/aim carry. The maintained source change is only a
comment clarifying this existing behavior.
