# Extra-stage curved-bullet BB tile filename

MAIN decoded `[21E6B,21E73)` contains the complete original eight-byte
mutable resource filename `LS00.BB` with a natural trailing NUL.
`th05/formats/bb_cheeto[data].asm` contains the literal `aLs00_bb`,
and the actual independently accepted `bb_cheeto_load()` uses the same
resource to load Extra-stage curved-bullet tile graphics. This semantic
C file owns the **filename**, not any content or picture bytes from
`LS00.BB`.

`bb_cheeto_fn[8]` uses the natural writable near-C array ABI already
declared by the accepted loader's `bb_cheeto.hpp`. The compiler owns all
8 bytes and an external-only linker binder supplies the original
main_01/main_03 frames and DS `209D:169B` prefix, without any game data
inside the candidate. The original following zero word and any
neighboring tables remain unowned. This is also not a claim that the
original producer grouped the preceding five meaningful bytes into
this eight-byte filename contribution.

The focused native replay at
`.analysis/unit-replays/gpt-web-main-cheeto-filename-a/receipt.json`
passes two independent real Borland C producers, complete 8-byte
OMF/MAP initialized-DATA boundaries, full original raw-byte equality,
and exact original empty ordered MZ relocations. A compiled
`LS00.BB`→`LS01.BB` mutation is rejected. Only this new owner was
replayed; no global cold replay was performed.
