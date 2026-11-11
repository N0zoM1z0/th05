# Master file, DOS and heap routines: exact original MAIN ownership

**28 complete source-backed Master 0.23 assembly procedures, 1,724 CODE bytes**
have been reconstructed from their original archive source, the actual
TASM-generated MAIN OMF, and authentic Borland linker contexts. The main
functions include **HMEM_ALLOC (240 B)**, **HMEM_FREE (168 B)**,
**FILE_READ (180 B)** and **FILE_FLUSH (108 B)**. The remaining 24
complete procedures cover DOS/file I/O, font and pattern readers,
the PF interface, SMEM, memory assignment, and SUPER_FREE.

The [bounded native verifier](../../scripts/review_master_io.py) uses
the genuine original Master archive as an independent source-identity
oracle. The maintained compiler input must match the original full
procedure bodies after whitespace/comments and ordinary local-label
scoping. The only additional structure spelling rule applies to
HMEM_ALLOC and HMEM_FREE: the port's named `memhead` fields refer to
the original zero-offset heap header fields (`ES:[0].nextseg`,
`ES:[0].using` and `ES:[0].mem_id`). The actual OMF and linked raw
comparison independently check every associated opcode and offset.

Each complete source LEDATA range is reconstructed with the real,
ordered OMF FIXUPP records. The actual calibration and original MAIN
payloads and original ordered MZ relocations must match without a byte
exception. The linker model is anchored independently by C0L startup:
`DGROUP=209E0h` in the calibration and `209D0h` in original MAIN,
with original initialized DATA/BSS offsets 18 bytes earlier.

Evidence and adoption are separate:

- [Original linked-source proof](../../config/master_io_ownership.json)
- [Explicit complete-function adoption](../../config/reviewed_master_io.json)

These 28 extents were previously all `unknown` in the MAIN ownership
map and have no overlap with earlier Master, CL.LIB or game-authored
owners. Targeted negative checks mutate a real OMF LEDATA byte or
an independently established DATA binding, both of which must break
full original-byte equality.

```sh
python3 scripts/review_master_io.py --check
python3 scripts/review_master_io.py --structural-check
python3 scripts/ownership.py --check
```

This is third-party source-backed Master assembly CODE, not new
game-authored C++ code. No foreign DATA/BSS or adjacent functions are
implicitly owned. Neither a cold replay nor a whole-game image build
was used.
