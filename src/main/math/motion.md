# Bounded motion-method candidate: no acceptance

`motion_seg1.cpp` implements the existing canonical `PlayfieldMotion` method
without changing shared geometry or any accepted caller. It saves each old
coordinate, adds the corresponding velocity, and returns the new point.

The complete native methods occupy MAIN BE1A..BE3A and 1527C..1529C, each32
bytes with identical payloads. Both use a near Pascal interface: one 2-byte
near `this`, RET2, and a 4-byte point returned as AX=X and DX=Y. Neither has
instruction NOPs, embedded tables or MZ relocations. The existing accepted
player-position caller and the retained typed-return producers independently
support this interface. The real motion remains 12 bytes, with current,
previous and velocity points at offsets 0/4/8.

One natural seg1 candidate produced 42 bytes. Its actual complete OMF
contribution is valid, contains no fixups or NOPs, and returns the correct
point. The compiler preserves SI and a BP frame, updates the fields in memory,
then reloads the 4-byte result with EAX/SHLD. The native method instead carries
the new coordinates through AX/DX. This is a whole-contribution mismatch;
no bytes are normalized or accepted. The first extent gate stopped before a
second producer or compiled negative. Seg3 was not compiled.

No register template, return-type substitution, geometry edit, expression or
compiler-flag sweep follows. The modern ReC98 and maintained TH04 assembly
versions explain the algorithm and interface, but do not prove the original
implementation language. A failed C++ candidate does not establish handwritten
assembly ownership. Both native scopes remain unknown, with zero new authored
credit. The failed replay manifest stays private and outside incremental plans.

The installed toolchain identities were checked and its successful execution
probe was reused. No previously accepted unit was rebuilt. Private complete
first-producer review: `.analysis/motion-seg1-natural-first-review.json`, SHA-256
`f23bfd8df9240bb493aa16e51772f54b889ff45138c04d0ae45ac17736635f09`.
Independent ABI/origin routing: `.analysis/motion-seg1-routing-review.json`,
SHA-256 `a088615515765a2846e6e0c6f28e3bd02c7e3596d8a08355f59ab4ed69b63e74`.
Independent actual-producer review:
`.analysis/motion-seg1-natural-actual-independent-review.json`, SHA-256
`31c86894c99928662c45b6d7b7666b0aef72efb1d10abf1bcc15853a52a98d84`.
