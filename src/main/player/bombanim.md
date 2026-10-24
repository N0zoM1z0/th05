# Reimu bomb star animation candidate

Natural source provenance is ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th05/main/player/bombanim.cpp`. Its old emitted call bytes are replaced by the
real typed `circles_add_growing` far Pascal call. No assembly, pseudoregister,
barrier, instruction array, or copied implementation bytes remain in this owner.

The complete original MAIN function is `[FB44,FD17)`, frame `AE1`, offset `4D34`,
467 bytes. Its next function starts at `FD17`; that real caller calls back to
`FB44` at `FD2A`. All local branches land at instruction boundaries. Five actual
ordered loader fixups belong to VECTOR2 and the four sprite calls. The original
NOP at `FD03` is the linker-shortened circle call's padding: compare all467
bytes, but credit at most466 instruction bytes. There are no switch tables.
No acceptance is claimed before the root worker's real producers and control.

The full external animation union is retained:48 ten-byte Reimu stars,
eight ten-byte Marisa lasers, eight ten-byte Mima circles, or one ten-byte
Yuuka heart. Every real scalar/unused field is declared; the union is480 bytes,
a trail is80 bytes, and star velocity/angle are at4/8. These declarations use
canonical Subpixel/SPPoint and the existing complete point_t. The separate
owner-named BombScreenPoint preserves the actual two signed word coordinates
without adding a competing global screen_point_t class. This owner defines no
DATA or BSS; the global union is external at DS:420E. Bomb frame and modulo-eight
stage frame are bytes at DS:4207 and DS:5768.

The original unrolled trail copies and pointer arithmetic are preserved,
including their initialization stride quirk and final next-head memory access.
Slow pixel conversion remains signed division by16; shifting a negative value
would change its rounding. Random position, speed and angle calculations retain
word RNG results and actual byte truncation, with meaningful range expressions.
The plane constant uses master.lib erase mode and inverted four-bit color mask.

Foreign interfaces are the actual near Pascal RNG functions at `C70E`/`C724`,
far Pascal VECTOR2 at `14AB:0008`, far Pascal SUPER_ROLL_PUT_1PLANE at `0000:2E1A`,
and far Pascal circles_add_growing at `AE1:347A` (`E28A`, observed RETF4).
VECTOR2 takes two real far word references plus word angle/length. Circle's
address is earlier than the owner and the ordinary prefix scaffold places its
true FAR public in the same original frame. Only the real compiler/linker may
produce the shortened call; no normalization or forced call sequence is used.

Suggested alias `th05/bombanim.cpp`, segment `BOMBANIM_TEXT`, group `main_01`,
GAME5/BINARY M, ordinary pinned large-model flags with BP enabled. A meaningful
negative changes bomb-frame cutoff112 to111. Private boundary metadata, ordinary
binders and suggested entries are in `.analysis/bombanim-midboss5-*`.

`main-reimu-bomb-stars-a` now passes two independent fresh producers, complete
raw-byte comparison, original ordered fixups, deterministic OMF and the
reviewed compiled gameplay mutation. Source state and foreign API bodies
remain uncredited.
