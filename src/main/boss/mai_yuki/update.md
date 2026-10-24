# Mai/Yuki complete shared update

The accepted stage-setup callback at **14820** identifies MAIN
**1527:2D6B**, load **17FDB..183D5**, **1018 bytes / one complete far Pascal
function**. Native decoding covers282 instructions/993 bytes through the actual
RETF at183BB. It is followed by the original zero at183BC and two complete
compiler tables: six word values at183BD..183C9, then six word destinations at
183C9..183D5. Values are0/1/2/253/254/255. All56 direct branches and all six
table destinations land on real instruction starts. The next function begins
183D5. Original ordered relative MZ fixups are
**[942,931,915,898,874,723,312,171,123]**. Classification is1017 authored-code
bytes:993 instructions plus24 compiler-table bytes, excluding the one zero.

ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47` retains this state machine as
`@mai_yuki_update$qv` in `th05_main.asm`, lines13217..13590. The source includes
the frozen accepted flight and pattern interfaces with full canonical Boss24
objects, Laser24/32 slots, Cheeto/Custom layouts, gather, dialog and the actual
canonical HUD title-pointer surface.
All existing accepted sources and headers remain unchanged. No ASM, emitted
opcode, pseudo-register loop, fake flags API, opaque table, inert barrier or
source/flag variant is introduced. The complete canonical explosion enum and
zap union are declared independently because the generic header's BOSS_W
constant conflicts with the existing flight header's same-valued macro.

Homing selects the lower of the two actual Boss positions and the shared timer
advances. Phase0 initializes4500 HP per character, both zero HP boundaries,
gather geometry and the real212..227 tiny sprite conversions. Both characters
remain shot-invulnerable through128 frames, then SE13 and the genuine shared
background callback are selected. Phase1 waits64 frames, then initializes the
first accepted Mai/Yuki patterns and real custom-bullet renderer.

Phase2 alternates shared random flight and the two accepted charge/pattern
dispatchers. Cycles9/14 use the actual64-frame relative wait and clear/explosion
actions at16; other cycles use a16-frame relative wait. Completed flight selects
patterns from genuine external four-entry near-CODE arrays for the first,
laser and final pattern groups. Completing36 cycles skips rewards and selects
Mai's defeat. Combined HP below5500/2250 advances early groups to cycles9/14.
The real shared hit helper returns0/1/2 for neither/Mai/Yuki; a nonzero result
selects the defeated character and sets the actual reward flag. The shared
phase temporary carries either relative flight frame or this result in
mutually exclusive paths, matching its actual word lifetime in the function.
Any active first laser is stopped before the small-explosion phase.

At phase253/frame16 the chosen character emits the real vertical small
explosion. Frame32 performs its big circle, restores the other still sprite,
advances phase, applies the actual zap/reward state and SE12 and gives255
invincibility frames. Phase254 shakes at the real +/-4 values for12 frames,
selects full tile rendering and slowdown2, advances the chosen kill animation
every8 frames and reaches phase255 after64. Phase255 sets palette tone60 and,
on its first frame, loads the survivor's genuine dialog and BGM title. If Mai
was defeated it copies Yuki's current position into the shared primary object
and assigns the real Yuki update; otherwise it assigns Mai's update. Dialog,
BGM overlay, new foreground renderer, phase0 and7900 HP follow. Every path
updates the real Cheetos and renders combined HP against9000.

Five pattern tables remain ordinary external semantic arrays of four near
function pointers at DS18E6/18EE/18FE/1906/190E. Current pointers remain DS442E
and4430. Dialog filename/title resources remain external at1916/1920/193E/1948;
no pointer entries, Japanese payloads, strings, images, DATA or BSS are emitted.
HUD titles retain the canonical Shift-JIS byte type and actual far pointer.

The Yuki damage helper at177F0..1782C is genuine near Pascal with three signed
word parameters, RET6 and damage inAX. The shared selector at1782C..1785F is a
real no-argument near function returning codes0/1/2 inAL, verified from its
complete native body. Boss2 explosion helpers at1775D/177C7 retain their real
word-Pascal/near-cdecl interfaces. Existing shared flight at17937 and accepted
pattern bodies remain foreign; their byte ownership is not transferred.

True first declarations preserve all foreign frames. Runtime sprite conversion
is C Pascal far0000:35A2; sound is C Pascal far14AB:0232. Main01 callbacks use
AE1: shared background5D87, survivor foreground5B2F, tiles0DDC, Cheeto
render811B and BGM overlay732A. Dialog load/animate are genuinely far in main01
at8B1B/9048. The overlay symbol's actual32-character truncation is verified
from the accepted HUD OMF PUBDEF as
`@OVERLAY_BOSS_BGM_UPDATE_AND_REND$QV`. No invented linkage alias supplies a
body. The two survivor update pointers are true C Pascal far1527:3795/42BB,
load18A05/1952B, consistent with the independent Yuki owner. Call lowering and
far-pointer stores still require actual producer verification; preserving
truthful declarations alone is not a claim of exact compilation.

Other real globals are palette tone DS03DA, background callback350A,
shake351C/351E, invincibility36EE, homing3F8A, zap/clear3F96/3F97,
overlay4ABE, BGM title pointer4AD0, frame mod2/mod45766/5767,
slowdown576A, palette-changed576D, lasers578C, Boss objects5ABA/5AD2,
gather9EA6, update far pointerC672, foregroundC676 and custom rendererC678.
The symbol-only binder supplies original addresses and outside-contribution
holes only. Its actual foreign LASER_SC_TEXT merges in main03 after an
independent paragraph at183E0 following original full end183D5, anchoring
DS209D. Every ORG is below64KiB; no helper instruction, initialized value,
inside-function hole or `.stack` is supplied. Ordinary `-a2` appears only after
complete ABI declarations; it supplies no manual padding or table bytes.

`.analysis/mai-yuki-update-boundary-review.json` pins target/extent hashes,
complete native branches/calls/table/return/fixup evidence, real data roles and
actual foreign symbol spellings. `.analysis/mai-yuki-update-candidate.json`
proposes valid DOS8.3 module `th05/my_upd.cpp`, MAIN_035_TEXT/main_03 and the
meaningful HP-group threshold negative5500→5501. Native closure/classification
and unique-mutation checks pass. Preparation ran no compiler or Wine. Two
actual cold producers, complete raw/ordered proof and rejected compiled
negative remain required before authored acceptance.


## Initial integration correction

The first focused launch failed while compiling because including the broad
HUD overlay header also declared a second `to_sp(float)` implementation already
provided by the canonical movement header. Root removed only that broad include
from this new, unaccepted owner and retained the actually required canonical
`shiftjis_t = uint8_t` and external far `boss_bgm_title` pointer. Function first
declarations, the existing dialog API, object layouts and all accepted headers
were unchanged. `main-mai-yuki-update-b` is the subsequent real focused producer;
this integration correction supplies no exact or authored evidence by itself.

Saved native outcomes remain unaccepted. Producer a stopped at the frontend's
duplicate HUD/movement speed helper; only the needed canonical title-byte
FAR pointer surface is now declared locally. Producer b emitted1023 bytes: two
word shake branches each add3 instruction bytes, and the original zero is
absent. Natural conditional rvalues restore the original shared word-store
dataflow in c, but c still emits1017 rather than1018: the original zero before
the24-byte switch tables remains absent. The993-byte instruction region has
its original fixup stream and differs only at the table-base operand by1;
the24 table bytes themselves agree. The entire function, zero and tables
remain mandatory. No clipping, inserted byte, normalization or speculative
flag/context replay is used, and this owner is outside default selection.
