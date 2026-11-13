# EX-Alice four complete bouncing/fixed/speedup/sweeping laser patterns

The real **645-byte** MAIN contribution contains four independent native
near C++ attack functions: bouncing ring 104 bytes, fixed laser fan 237,
speedup aimed spread 110, and sweeping lasers 194. The maintained
`laser_attack_rules.hpp` now names their original clocks, counts,
geometry, sound and state transitions. All values remain compile-time
source expressions. No new Laser24 allocation, Boss scratch byte,
resource asset, alternate branch, or private optimizer barrier is used.

**Bouncing rings:** the original first event at phase frame 64
initializes an eight-shot ring. Every sixteen frames the same
bounce-left/right/top bullet group fires, at speed two pixels/frame;
on each 128-frame boundary the count increases by one until the
original strict limit fourteen. The bullet template still uses a
single collision bounce and increments its 8-bit angle by two.

**Fixed laser fan:** one pair starts during each sixteen-frame cycle,
first at frame remainder zero and then at remainder eight, with
opposite signed ±0x30 aiming offsets, color three, width eight,
47-frame grow age and 80-frame shrink age. The first-half event also
fires a 32-pellet ring at speed four. Only phases earlier than frame
144 create new fixed lasers. The remaining real animation cycles
through sixteen existing slots (`slot & 0x0F`), turning each waiting
beam one angular unit either clockwise or counterclockwise. At phase
frame 208 it resets the slot index and returns true.

**Speedup aimed spreads:** every second frame the special bullet
speedup group emits a seven-shot spread with step nine and a two-unit
acceleration. Random horizontal jitter spans 48 pixels, biased left
24; the original random flystep begins from `phase_frame - 100` and
the attack finishes at frame 128.

**Sweeping lasers:** at frame 64 the real two-state scratch byte arms
color-two, six-pixel beams at shootout speed 5.5 with a 30-frame grow
age. Every fourth frame it turns the laser template by ±8 toward
angles zero and 128, spawning one real shootout laser on each step.
After frame 256 it also moves the Boss on a 64-frame cycle, and after
frame 512 fires 32-shot aimed rings every sixteen frames. The source
retains the real live `ExAliceBossScratch::pattern_byte15.sweeping_laser_direction`
view of `boss_statebyte[15]`; it never introduces a synthetic direction flag
or replacement laser table.

The focused receipt
`.analysis/unit-replays/gpt-web-exalice-laser-roles-a/receipt.json`
recompiled the complete four-function cohort in two independent pinned
Borland native rounds. All 645 original CODE bytes, actual OMF/MAP
boundaries and the original ordered MZ fixup stream are unchanged.
The source-level fixed-laser grow-age mutation **47→48** was compiled
and rejected. All source bytes were already accepted, so this change
improves gameplay meaning without duplicate CODE credit. No full-game
cold replay was performed.
