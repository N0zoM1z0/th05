# Complete typed miss-drop velocity table

This accepted owner defines the complete canonical
`const Subpixel ITEM_MISS_VELOCITIES[3][2][5]` at original MAIN
DS`209D:1E86..1EC2`, load offsets`22856..22892`:60 bytes,30 real signed-word
Subpixel cells. Field order is left/center/right; each field stores Y first and
X second for five item slots. It is gameplay motion data, not sprites, pixels,
opcodes, opaque bytes or a shortened structure view.

Original native consumers at1CD33/1CD46 multiply the selected field by20, then
add the spawned slot multiplied by2. The Y load uses DS1E86 and stores the
canonical item motion's velocityY at item+12; the X load uses DS1E90,10 bytes
later, and stores velocityX at item+10. The real three-way player-position
selection and five-slot bound corroborate the complete declared dimensions.
No MZ relocation intersects the60 bytes, and their complete sequence occurs
once in the pinned original image. No previously accepted extent overlapped it.

| Field | Y velocity, pixels/frame | X velocity, pixels/frame |
| --- | --- | --- |
| Left | -3,-3.5,-4,-4.5,-5 | 0,0.75,1.5,2.25,3 |
| Center | -3,-3.5,-4,-3.5,-3 | -1.5,-0.75,0,0.75,1.5 |
| Right | -3,-3.5,-4,-4.5,-5 | 0,-0.75,-1.5,-2.25,-3 |

The pinned ReC98 `th04/main/item/items[data].asm` supplies the same readable
physics schedule; every semantic initializer is independently compared with
this original TH05 target. Source expresses integer pixels/frame and fractional
subpixel steps at16 subpixels per pixel. Negative arithmetic uses multiplication
rather than left-shifting a negative C++ value. It supplies no target-byte array
or data copied by an assembly producer.

`miss_velocity_data.hpp` includes the unchanged complete item header, which in
turn uses the unchanged canonical `SubpixelBase<int,int>` class. That class has
one public scalar `v`, no base, no virtual members and no user-declared
constructor; its subtraction and conversion operators do not add data fields.
Each innermost brace initializes this actual aggregate. Array/axis/field size
assertions retain the real2/10/20/60-byte structure. No constructor, fake class,
scalar alias, alternate ABI field or canonical-header modification is added.

`main-item-miss-velocity-data-a` proves one complete60-byte initialized DATA
contribution with its matching PUBLIC identity and gapless OMF LEDATA, zero
dynamic-initialization CODE/BSS, two fresh deterministic raw comparisons and
the original empty ordered relocation stream. The own compiled3-to-4px X
velocity control is rejected. The real canonical aggregate initializes
statically; no type replacement or constructor instructions were needed.

The independent binder follows the already accepted item-DATA context. It
places even the empty foreign HUD_OVRL_TEXT at its true MAIN01 group, anchors
DS209D, and reserves only the prefix before the complete source-owned DATA.
It defines neither the owned table label nor values, internal gaps or `.stack`.
The preceding pull-to-player byte1E84 and outside alignment byte1E85 are not
owned. The extent stops at1EC2; following HUD/state bytes are not annexed.

One staged source negative changes only the left field's last X velocity from
3 pixels/frame to4. This is a unique initializer and affects word offset18 of
the table. The module alias `th05/itmissv.cpp` satisfies DOS8.3. The
proposal remains private in `.analysis/item-miss-velocity-data.proposal.toml`.

`ITEM_PATNUM` is already part of the accepted116-byte item-reward table owner;
`ENEMY_DROPS` already has its own accepted64-byte owner. Neither receives
duplicate credit here. The accepted spawn code and all canonical headers remain
unchanged. Private native references, dimension/stride proof, initializer
arithmetic, target hash and zero-overlap check are recorded in
`.analysis/item-miss-velocity-data-native-review.json`; the functional freeze is
`.analysis/item-miss-velocity-data-freeze.json`. Preparation ran no compiler; actual acceptance is established by the focused
producer receipt named above.
