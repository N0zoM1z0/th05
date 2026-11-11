# Exact native-register PlayfieldMotion updates

`PlayfieldMotion::update_seg1()` at MAIN `BE1A..BE3A` and
`PlayfieldMotion::update_seg3()` at `1527C..1529C` are now two complete
32-byte C++ units, using the original `main_01` and `main_03` CODE frames.
Each consumes a near-Pascal two-byte `this` pointer through `SS:[SP+2]`,
advances the signed 12-byte motion structure, copies current X/Y into the
previous X/Y fields, and returns updated X/Y in the real `AX`/`DX` register
pair. Both finish in `RET 2` and have no ordered MZ relocation sites.

The conventional [motion candidate](motion_seg1.cpp) returned `cur` through
Borland's structure-return lowering and emitted 42 bytes rather than 32.
The new register-aware C++ uses the genuine `peek(_SS, _BX + 2)` pointer
interface and typed near word writes. Its function signature keeps the actual
`PlayfieldPoint` return type; the compiler-observed AX/DX result is prepared
through intrinsic register bindings instead of an additional C++ return
expression, which would reload/repack the result and change the ABI. This is
compiler-specific source and is not portable standard-C++ return behavior.
The full 12-byte canonical geometry type and all accepted caller code remain
unchanged.

Focused receipt:
`.analysis/unit-replays/gpt-web-main-motion-register-both-a/receipt.json`.
Two independent Turbo C++/TLINK producers match both original 32-byte bodies
and the original empty fixup streams. The negative changes the Y-field step
from 2 bytes to 4 bytes in the maintained register source, and the full
compiled comparison rejects it. The real DATA/BSS payload remains foreign.
