# Whole-map dirty fill: unaccepted C++ candidate

The native MAIN function `BD38..BD4E` is 22 instruction bytes, with no NOP,
table or fixup. It sets all 1600 bytes of the full 50x32 half-tile dirty map
at DS `4ADA` to one. The actual game bool is an unsigned byte. Native sets
ES from DS, writes 400 DWORDs and preserves DI, without adding CLD.

Maintained TH04 `main/tile/tile.cpp` and the pinned ReC98 tile source corroborate
the complete map and fill semantics. Their register-template/string-operation
body is not copied as C++ acceptance. The new candidate uses Borland's real
`__memset__` intrinsic from the pinned MEM.H, with the full unsigned-byte map.

The initial setup lacked TC4's separately declared boolean aliases and failed
at the frontend. Correcting the declaration to canonical `uint8_t` and the
true value 1 allows the first complete producer: 16 bytes, with 800 `REP STOSW`
stores and PUSH DS / POP ES instead of native 400 `REP STOSD` stores and
MOV AX,DS / MOV ES,AX. Neither implementation adds CLD. Raw equality fails;
there is no second positive, negative, padding addition, register kernel,
option sweep or ASM-origin inference. The source stays outside the live
manifest, with zero authored credit. The neighboring reset function and
its independent alignment NOP remain foreign.

Actual first producer:
`.analysis/native-producers/main-tile-invalidate-intrinsic-b/`.
Review: `.analysis/tile-invalidate-intrinsic-review.json`.
No existing accepted source/header or compiler tool changed or needed replay.
