# MAIN high-score insertion: exact C++ register-context recovery

The full `hiscore_continue_enter_raw()` at MAIN `[C8F0,C998)` now has a
168-byte Borland C++ source match, with no MZ relocation sites, CODE tables,
padding or initialized DATA. It compares eight current-score digits against
the top-five gaiji BCD records, shifts lower records and names by one place,
then writes `CONTINUE`, converts eight digits to gaiji and saves the score
file through the real near routine at `C8B9`. The temporary insertion rank
and extra-stage remapping remain the original byte/word operations.

The maintainable source combines typed complete score records and Borland's
real `_AX`/`_BX`/`_CX`/`_DX`/`_SI`/`_DI` register interfaces with semantic
inline `IMUL`, `LOOP` and 386 `MOVSD` instructions for the actual overlapping
score/name copies. It provides no emitted opcode byte templates, copied
binary image, modified linker output or fabricated state. Its symbol-only
binder reserves the true original `main_01` CS `AE1`, DGROUP `209D`, existing
`hi`, score, stage and filename addresses, and the external save function.

## Compiler context and strict evidence

Turbo C++ 4.02's **direct** `-c` inline assembler rejects 386 `MOVSD` even
though `-S` emits the semantic assembly instruction. Assembling that genuine,
unaltered compiler output using TASM32 and linking with TLINK reproduces the
original 168 bytes. The distinction is material: previously attempted
`movsd`/`movs dword ptr` direct compile failed before any object was emitted.
The current source uses the existing `compiler_pipeline = "tcc-s-tasm32"`
replay without changing the tool or normal oracle comparison.

Receipt:
`.analysis/unit-replays/gpt-web-main-score-continue-raw-exact-s-a/receipt.json`.
Two independent fresh original-toolchain producers match all 168 raw bytes,
the original empty ordered fixup list, complete native MAP/OMF boundaries
and staged C++ dependency identity. The negative changes the initial score
rank from `SCOREDAT_PLACES - 1` to `SCOREDAT_PLACES - 2`; it compiles but is
rejected on the full function. Neighboring score loaders/callers remain
separately accepted without any duplicate credit. No full cold replay ran.
