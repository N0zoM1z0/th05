# Whole CDG bank release: exact native-assembly reconstruction

MAIN `CDG_FREE_ALL` occupies the complete `[1526E,1527C)` fourteen-byte
shared-code contribution. It releases the game's 64 CDG resource slots from
slot 63 down to 0 and returns FAR Pascal. The actual `CDG_FREE` service is the
same-CS FAR Pascal provider at `14AB:0788`: saving CS and making a relative
near transfer retains the provider's far return frame and one-word Pascal
cleanup. SI is preserved. No storage, table, or alignment byte belongs to this
routine.

The reference implementation `_reference/ReC98/th04/formats/cdg_load.asm`
independently supplies the original descending release-loop algorithm, and
the target's nine complete instructions confirm its assembler-style control
flow. This is a reviewed native-ASM reconstruction, **not** recovered
historical source or C++ compilation credit. A first natural C++ attempt emitted
23 instead of 14 bytes due to BP framing, an extra loop-entry jump, an OR test
and linker's length-preserving same-CS far-call relaxation. That failed source
and binder were removed after recording the result; their first compiler
artifacts remain in `.analysis/gpt-web-cdg-free-all-baseline-c/`.

The maintained semantic ASM source `cdg_free_all.asm` uses the 64-slot count
from the canonical `src/main/ems/ems.hpp`. TASM initially paragraph-aligned
its source `SHARED` contribution two bytes past the actual `14AB:07BE` entry.
Changing **only the source SEGDEF alignment** to BYTE preserves the native
start without injecting a gap or modifying any emitted instruction. The
separate symbol-only binder preserves the true `CDG_FREE` address and DGROUP
`209D` frame. Both independent TASM32/TLINK producers then match all **14/14
raw bytes**, the empty original ordered relocation stream, source CODE extent,
MAP start/end and OMF object identity. The semantic negative decreases the
last slot from 63 to 62; it retains the same function length but fails the
original comparison. Receipt:
`.analysis/gpt-web-main-cdg-free-all-asm-b/receipt.json`.

The original native-review digest, full instruction/return closure and target
SHA are pinned in `config/asm_families.toml`. The accepted local ASM ledger and
explicit reviewed ownership record grant 14 reviewed ASM instruction bytes,
not C/C++ authored bytes or graphics asset data. No adjacent 54-byte
`CDG_FREE` provider, packed file or whole executable is accepted by this unit.
