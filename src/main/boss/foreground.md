# Sara and Louise foreground rendering

Natural C++ candidates for the complete adjacent MAIN functions at
`140C4..14163` (Sara, 159 bytes) and `14163..141D7` (Louise, 116 bytes).
Their combined extent is 275 bytes, with 112 instructions, no padding,
compiler tables or initialized DATA. The original ordered MZ relocation list
is **[147,129,44,263,245,202]**. The first combined producer was inexact.
Louise subsequently passed as an independent complete owner; Sara remains
unaccepted.

The source uses the frozen complete 24-byte Boss from `movement.hpp`, including
its full motion, sprite, phase and damage fields. Only the original frame
bytes at DS `5768` and `5769` are external. The shared Boss remains at DS
`5ABA`, and the binder reserves its complete foreign extent through `5AD2`.
No accepted header or other foreground owner is changed.

Both callbacks convert the real Q12.4 center to pixel coordinates. The
playfield-left 32 and half sprite width 32 cancel; the top offset is
playfield-top 16 minus half sprite height 32. Phase 254 selects the large
explosion sprite. Sara's moving sprite bases 184 and 186 use the eight-frame
counter divided by four; stationary base 180 uses the sixteen-frame counter
divided by four. Other Sara sprites remain unoffset. Louise uses the
sixteen-frame animation for every normal base sprite.

A zero damage flag uses `super_put`. Damage uses the genuine five-argument
`super_put_1plane(left,top,pattern,pattern_plane,put_plane)` with pattern plane
zero and the real `FFC0` plane/mode mask. The far Pascal library APIs retain
their original frame-zero entries (`2048`, `33F0`, `2ADA`) and real stack
arguments. There are no fake short signatures or register templates.
Both sprite paths then call the real small and big explosion updaters at
`1060E` and `106D8`, near within frame `AE1`. The source expresses ordinary
sprite animation and API selection; no graphics kernel is transcribed.

The symbol-only binder anchors real external CODE symbols and DS globals.
Its origin holes occur outside the entire compiled contribution, with no
instructions, owned bytes, stack allocation or initialized DATA supplied.
The proposed DOS8.3 module is `th05/boss_fg.cpp`, contribution `BOSS_FG_TEXT`
in `main_01`.

Private `.analysis/sara-louise-foreground-boundary-review.json` pins native
bounds, target/extent hashes, every call, original ordered fixups, interfaces
and source closure. `.analysis/sara-louise-foreground-candidate.json` proposes
a complete contribution and optional complete function scopes. The primary
staged negative changes Sara's left-motion selector to the stationary selector,
which changes actual animation behavior. A separate Louise-only frame-rate
mutation is provided for independently selected complete scopes.
Actual compiler extent, two fresh deterministic producers, full raw/fixup
comparison and a compiled negative remain required before acceptance.

## First producer and independent Louise owner

The retained first producer `main-sara-louise-foreground-a` generated 277
bytes: Sara 161 and Louise 116. Sara retained 63 instructions but stored the
left coordinate on the stack while holding the top in DI. The original uses
the opposite allocation. Stack PUSH paths added two bytes; no physical register
hint or further source variant is proposed.

Louise retained all 49 instruction/register forms and its original ordered
fixups `[104,86,43]`. The combined artifact still fails raw comparison:
Sara's two extra bytes move Louise from `14163` to `14165`, change relative
calls, and shift the foreign DATA placement. Symbolic-address diagnosis of
Louise does not count as an exact match.

`louise_foreground.cpp` now supplies a standalone complete owner using the
unchanged `louise_foreground.inl`. The original combined `foreground.cpp`
includes that same guarded definition, avoiding duplicate maintained bodies.
The entire function definition is verbatim identical to the retained actual
producer's source (definition SHA256
`09409d4af56fa1bd267e913e3dd6cbc9746829d8708f18cb30cba6c3f59b4193`).
The original header is unchanged.

The independent binder anchors the whole source contribution at `14163` and
its tail at `141D7`; it does not move unaccepted Sara code, insert inside gaps,
or supply any function bytes. Private `louise-foreground-candidate.json`,
`louise-foreground-boundary-review.json` and
`louise-foreground-source-equivalence.json` under `.analysis/` specify the
whole 116-byte proposal, body equivalence and real interfaces. Its own staged
negative changes the divisor of Louise's frame animation from four to five
inside the shared implementation.

`main-louise-foreground-a/receipt.json` subsequently passed both fresh complete
116-byte producers, full raw bytes and original ordered fixups `[104,86,43]`.
The independently compiled animation-divisor mutation was rejected. The root
imported `main-louise-foreground` as one complete function and 116 authored
CODE bytes, with no padding or tables. Its CPP, shared implementation, header
and binder are now frozen accepted dependencies. This acceptance does not
transfer to Sara or the failed combined producer.

## Complete Sara foreground accepted

The new ordinary declaration order is `left, top, patnum`, matching the
unchanged coordinate-then-sprite computations. The previous order was
`top, patnum, left`. These are uninitialized ordinary signed int declarations;
their types, names, all calculations, evaluation order and calls are unchanged.
No `register`, physical-register reference, alias, compiler option, barrier or
padding is introduced. Borland now naturally retains left in DI and top in
the genuine stack local, matching all159 native bytes and ordered fixups
`[147,129,44]`. Literal historical declaration spelling remains unproved.

The complete definition is shared in sara/foreground.inl by the standalone
sara/foreground.cpp and the combined foreground.cpp. The existing accepted
Louise source, header, control and objects are unchanged. The first direct-source
replay passed; after canonical factoring, `main-sara-foreground-order-b`
supplies a normal replay with two fresh producers of the actual maintained
source closure. Its own phase-equality inversion changes only byte31 from75
to74, retaining full extent and fixup order, and is rejected.

The native procedure and both final source producers each pass1,744 modeled
rendering cases. Graphics and explosion functions are explicit ABI stubs;
arguments, ordering, full24-byte Boss records, canaries, stack and preserved
registers are checked. This does not execute hardware, raster assets, the
explosion pools or the complete game. An initial model used the wrong damage
offset16; its first native case failed. Canonical offset18 corrected the model
without changing game source or producer output; the failed model/log remain.

Receipt `.analysis/unit-replays/main-sara-foreground-order-b/receipt.json`, SHA-256
`ff85f75656a7c9ef8a4eb3a62197a587ae1b54139b513f90776b3ac69e1fe0b7`.
Joint native/source/actual-producer review `.analysis/foreground-order-root-review.json`,
SHA-256 `0d0eb838524f6b4d046a84d4acb135b4f422c1aeb50e60032ec7ae60c39ee8a6`.
The earlier161-byte failure stays archived. Only this complete159-byte function
gets new acceptance; the newly shared combined TU has not been replayed or
accepted as a whole. No DATA, padding, ASM or whole-EXE credit is added.
