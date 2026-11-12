# C0L.OBJ startup: source-backed foreign CODE in all three EXEs

The original MAIN, OP and MAINE load modules begin with the same Borland C++
4.02 large-model `C0L.OBJ` startup contribution, linked against each game's
actual DATA, initializer and BSS boundaries. The retained calibration MAPs
independently place its complete 625-byte `_TEXT` segment at `0000:0000`;
the installed pinned C0L object supplies **621 contiguous written CODE bytes**
ending in `RET` at offset `26C`. Its native source has 57 actual `_TEXT`
FIXUPP operands, and TLINK relaxes six original far-call sites to the
observed near-call form. The exact original ordered MZ segment relocations
for the written CODE prefix are `[1, 94, 165, 318]` in each executable.

The original source is verified from the actual pinned Borland object, not a
copy of the target machine-code bytes. The original/calibration models differ
only at its genuine OMF link sites:

| Program | DS frame in original | Original relative link changes | Verified written CODE |
| --- | --- | --- | ---: |
| MAIN | `209D` | DGROUP -1 paragraph; linked DATA markers -18 bytes; BSS end -20 | 621 |
| OP | `0EFE` | Same original/calibration frames and boundaries | 621 |
| MAINE | `1011` | DGROUP +1 paragraph; remaining frame-relative offsets unchanged | 621 |

`config/borland_c0_startup_ownership.json` records the real object identity,
calibration MAP/MZ identities, source fixups and full raw/ordered native
comparison in the three artifacts. The explicit decision in
`config/reviewed_borland_c0_startup.json` adopts **only `[0000,026D)`** in
each program as `verified-vendor-code`, a total of **1,863 foreign CODE
bytes**, with **zero game-authored C/C++ credit**. Run
`python3 scripts/review_borland_c0_startup.py --check` for a focused
object/link/native replay.

The source CODE segment actually has a five-byte unresolved tail: two
unwritten and runtime-writable CS bytes at `[026D,026F)`, two initialized
but non-instruction CS bytes at `[026F,0271)`, and an outside-segment
alignment byte at `[0271,0272)`. **All five remain unknown per EXE**; they
are not silently converted into instructions, BSS, authored initialized DATA
or checked padding. The next independently reviewed Master function begins
at `0272`.
