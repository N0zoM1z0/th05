# Mai/Yuki initial charge and attack cohort

Original MAIN **17957..17B76**, **543 bytes / six complete functions**, directly
follows the accepted248-byte shared flight contribution. Native decoding covers
all543 bytes with183 instructions. Every direct branch lands on an instruction
start within its real function. No RET is followed by a compiler table, zero
or gap before the next function. Original ordered relative loader fixups are
**[525,433,324,233,51]**, the five genuine far sound calls.

| Complete function | Original interval | Bytes |
| --- | --- | ---: |
| Mai charge/current-pattern dispatch | 17957..179B4 | 93 |
| Yuki charge/current-pattern dispatch | 179B4..179EC | 56 |
| Mai random cross stacks | 179EC..17A52 | 102 |
| Mai aimed turning fan | 17A52..17AAC | 90 |
| Mai sweeping pellets | 17AAC..17B1A | 110 |
| Mai small-ball fan | 17B1A..17B76 | 92 |

ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47` retains these algorithms as
`mai_yuki_1A556`, `mai_yuki_1A5B3`, `sub_1A5EB`, `sub_1A651`, `sub_1A6AB`
and `sub_1A719` in `th05_main.asm`, immediately after the shared flight
interface. The source recovers ordinary charge, sprite and bullet behavior in
natural C++ with full canonical Boss24 objects for both characters,
BulletTemplate14 and gather14. The existing flight source/header and all shared
headers are unchanged. There is no ASM, opcode transcription, pseudo-register
loop, fake flags interface, opaque array, inert barrier or source/flag variant.

Mai charges before48 frames by setting the real gather center to her position,
calling the three-stack helper with frame-24 and colors9 then8, and selecting
sprite183. Frame32 plays SE8. Later frames invoke the actual current near
pattern and inspect completion truth inAL; incomplete patterns select184,
while completion resets the shared timer/mode and both sprites180. Yuki uses
her own full Boss position and callback with the same shared phase timer,
selects her charge/fire sprites, and deliberately does not reset the shared
state when her callback completes. The distinction is original behavior.

Random crosses fire every6 frames: cloud-forward/no-deceleration aimed stacks,
angle uniform-20..1F hex, cross patnum47, origin8 pixels above Mai, two layers
at delta0.375, and random speed1..2.9375. They tune, add normal bullets and
play SE3, returning true exactly at128 frames. The turning fan fires once at48:
16-way/delta8 blue V bullets, aimed decelerate-then-turn motion and speed3.75,
using the genuine special fixed-speed add path; completion is exactly96.
Sweeping pellets initialize the byte angle to-10 hex at48, emit every4 frames
with five-way/delta10 spreads and speed3.125, advance the angle5 each emission,
and use the real regular fixed-speed path until exact completion160. The final
fan fires every8 frames at angle40 hex, small-ball patnum46, eight-way/delta12
spread and speed4, completing at128. Each producer retains its actual tuning
call and sound behavior. The completion tests are exact equality, not invented
timeout inequalities.

The two original callbacks are genuine near no-argument CODE pointers at
DS442E/4430, with byte truth consumed inAL; the complete four real bool bodies
are recovered here as normal functions. Tuning is the separate real near
Pascal callback at DS41DE. Other foreign state is bullet_template577E(14),
boss5ABA(24), boss2/yuki5AD2(24), gather_template9EA6(14) and
boss_statebyteC682(16). No callback entries, initial state, assets or DATA/BSS
are defined. The stack/spread setters combine only the actual asserted
adjacent semantic fields, following the reference BulletTemplate interface.

Foreign near helpers retain frame1527: random AND152AA, gather1705D,
regular add17204, regular fixed-speed17236 and special fixed-speed17244.
Sound is genuine C Pascal far14AB:0232. Packed gather PUSH00090008 was checked
in Pascal left-to-right order: color9 then8. The symbol-only binder supplies
only these original addresses and outside-contribution ORG gaps. The complete
compiler source occupies its slot, followed by a separate paragraph context
at17B80 after original full end17B76 to anchor DS209D. There are no helper
bodies, initialized values, inside-function holes or `.stack`, and every ORG
is below64KiB.

`.analysis/mai-yuki-initial-patterns-boundary-review.json` pins original hashes,
full per-function branches/calls/returns and original ordered fixups.
`.analysis/mai-yuki-initial-patterns-candidate.json` proposes valid DOS8.3 module
`th05/my_init.cpp`, MAIN_035_TEXT/main_03 and a meaningful whole-cohort negative
changing the first stack from2 to3, plus six optional complete-function scopes
with independent natural controls. Native closure, classification and unique
mutation checks pass. Preparation ran no compiler or Wine; actual two-cold
raw/ordered verification and compiled-negative rejection remain required before
any authored acceptance.

`main-mai-yuki-initial-patterns-a` passes two fresh deterministic full543-byte
raw/ordered positives. The real first attack's stack count2→3 mutation is
compiled and rejected for this whole owner. All six complete functions and
543 instruction bytes are accepted, with no DATA, BSS, tables or padding.
