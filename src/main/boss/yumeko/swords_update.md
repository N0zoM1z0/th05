# Sword updater candidate

Original MAIN `[1EDBA,1EED5)` is283 bytes, with one far relocation at75 and
no NOPs, tables or padding. The old routing-table distance2504 crossed later
functions and was not a function boundary.

The new C++ covers bullet-clear transition, unsigned twirl countdown and index-dependent rotation,
angle-based sprite restoration, real Motion Point-return consumption, clipping,
player collision, velocity halving and sprite decay. Full canonical Sword26,
template25, custom pool and player types remain unchanged. Returned AX/DX are
read only within their actual Point ABI lifetime, before another foreign call.
No physical arithmetic kernel, target bytes or shortened record is used.

One normal-profile diagnostic emits280 bytes, with its far relocation still75.
The native clip has a two-byte local removal proxy absent from the result;
a second two-byte loop-tail jump is merged, while the player-Y calculation is
one byte longer. Together these explain the three-byte gap. The body remains
unaccepted and outside the live manifest. Diagnostic:
`.analysis/native-producers/main-yumeko-swords-update-a`.

Disabling jump optimization emits 285 and shifts the relocation to 76. Removing
the nested continue or using a decay `else` under that profile still emits 285.
Statement-scoped `-O-` pragmas leave 280 unchanged; a switch emits 286. A scalar
word-pair alias either fails the frontend or emits 320; it is not adopted.
All trials failed, and the ordinary 280-byte source is restored. Alternative
producers are archived; see [storage](../../../../docs/LOCAL_STORAGE.md).

Restoring this complete function is also important for the genuine compiler
context of the adjacent354/428-byte attacks; see
[attack recovery](laser_swords.md).
