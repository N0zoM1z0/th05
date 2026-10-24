# Stage-five midboss update candidate

The original stage-setup callback at load **1487A** identifies MAIN
**1527:1682**, load **168F2..16A30**, **318 bytes / one complete function**.
All 97 native instructions cover the whole extent, including both RETF paths.
All 13 direct local branches land on instruction starts. The final RETF is at
16A2F; the next byte at 16A30 begins the already maintained scroll conversion
function (`MOV BX,SP`). There is no compiler table or padding in this original
callback. ReC98's relocated assembly lists a zero after its own version, but
that zero cannot be transferred to the original target. The original ordered
relative MZ fixup list is **[275]**.

ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47` retains this algorithm as
`@midboss5_update$qv` in `th05_main.asm`. This owner recovers the phase and
pattern behavior in ordinary C++, reusing the full canonical 22-byte midboss,
14-byte BulletTemplate and 14-byte gather template. It neither implements the
foreign helpers nor transcribes their instructions. No registers, flags,
opcode emissions, opaque arrays, alignment directives or source variants are
used. The ordinary shared defeat label expresses an actual timeout/HP join.

Every frame publishes the current position to bullet and gather templates.
Phase 0 moves while invulnerable. At 192 frames it advances phase, resets the
timer/angle/orbit state and vertical velocity, sets pattern phase 1 with count
0, and selects the original blue-spread pattern. Phase 1 preserves previous
position and dispatches the real movement/pattern phase. Movement completion
resets the timer, increments the byte counter, selects the external pattern
by `patterns_done % 3`, and advances pattern phase. Reaching count 16 enters
defeat directly without HP rewards. Active pattern phase calls the original
pattern updater. Shot handling retains the genuine byte damage store before
signed HP subtraction. HP defeat enables bullet zap, grants 30 bonus units
and adds the real 1UP item. Both paths enter phase 254/sprite 4, zero the timer,
emit 48 sparks at 8 pixels and play SE 12. Default phases call the real defeat
updater and return after HP rendering; live phases publish the homing point.
Total HP is 1550.

The semantic pattern table is a genuine external array of three **near CODE
pointers** at DS:1490. Original entries point to 1527:157D/15C1/162A, load
167ED/16831/1689A. The current two-byte pointer is at DS:3788. The actual
pattern updater calls it without arguments and tests AL for completion. Pattern
bodies return truth values 0/1 in AX, whose AL is consumed; the declaration
preserves that observed truth contract, near-pointer width and calling frame.
These are ordinary function-pointer declarations, not copied table contents;
no table values or initialized DATA are emitted or credited here.

| Foreign interface | Original load destination |
| --- | --- |
| `PlayfieldMotion::update_seg3()` | 1527C |
| movement-completion helper, returns truth in AL | 16724 |
| pattern/animation updater | 16768 |
| initial blue-spread pattern | 167ED |
| circle sparks | 16EE8 |
| HP render / score bonus / defeat updater | 1C4F6 / 1C54E / 1C628 |
| item addition / shot damage | 1CC2B / 1FA90 |

All near interfaces retain frame 1527; sound is genuine C Pascal far at
14AB:0232. Pascal publics, including the full sparks symbol, use the actual
uppercase mangling. The address-only binder anchors SHARED and the main03
prefix, leaves the entire source slot to the compiler, then uses a separate
PARA context beginning at the original complete end 16A30. All later helpers
and DS209D retain their native addresses only if the real compiler contribution
fits that context. Every ORG is smaller than 64KiB. There are no helper bodies,
initialized values, `.stack` or holes inside the source contribution.

Foreign state is the pattern table DS1490 (6 bytes), current pointer3788 (2),
homing_target3F8A (4), bullet_zap3F96 (1), bullet_template577E (14),
midboss5AA4 (22), gather_template9EA6 (14), and boss_statebyteC682 (16).
The owner defines no DATA or BSS; completed-pattern count and pattern phase
remain bytes 13/14 of the full canonical Boss state array.

`.analysis/midboss-stage5-boundary-review.json` pins native target/extent hashes,
complete branch/call/return/global evidence and the external table's semantic
pointer destinations. `.analysis/midboss-stage5-candidate.json` proposes module
`th05/midbos5u.cpp`, MAIN_036_TEXT/main_03 and the meaningful compiled negative
changing the HP-defeat reward from 30 to 31 bonus units. Native source-closure,
unique-mutation and classification checks pass. Preparation ran no compiler or
Wine. Two actual cold producers, raw/ordered-fixup agreement and rejected
compiled negative are still required before authored credit.


## Producer integration observation

The first combined launch `main-midboss5-extra-a` exposed a wrapper naming
error in this packet: `midboss5u` is a nine-character DOS basename. TCC created
a short-name object while the driver expected the unsuffixed long object
name. Root corrected only the module alias to the genuine eight-character
`th05/midbos5u.cpp` and relaunched `main-midboss5-extra-b`. Maintained algorithm,
ABI header and symbol-only binder were unchanged. This integration failure
grants no exact evidence or authored credit.


## Accepted complete callback

`main-midboss5-extra-b/receipt.json` passes both independent fresh producers
for the complete 318-byte Stage5 callback. All original raw bytes and the
ordered loader fixup list[275] agree in both rounds. Its separately compiled
reward negative30→31 changes real code bytes and is rejected. The ledger
accepts `main-midboss-stage5-update`: one complete function,318 instruction
and authored-code bytes, zero compiler tables or padding, and no DATA/BSS
credit. The combined receipt's Extra owner is a distinct compilation group
with independent evidence. This Stage5 source/header/binder stayed unchanged
during both launches; only the documented DOS module alias was corrected.
