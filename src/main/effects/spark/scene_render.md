# Spark display: native per-record graphics renderer

The complete MAIN `_sparks_render` is located at `[E0D2,E10E)` and occupies
**60 compared bytes**: 59 original real instruction bytes and one trailing
uncredited `EVEN` alignment NOP. The original near RET and all native call
sites are covered; there is no initialized DATA, switch table or relocation.

The maintained `scene_render.asm` reconstructs the full active 64-spark loop,
not just the graphics worker. It selects the native grcg color 12, sets the
real ES:A800 blue-VRAM destination, skips non-alive 16-byte records, prepares
Y through the native screen-scroll conversion, computes left pixel X from
subpixels, forwards age in CL and calls the already accepted near `@spark_render`
worker. It preserves SI/DI and the native signed Y/render-input arithmetic.
The original PC-98 hardware/service interfaces and relative calls use the
actual frame AE1, DS209D and existing providers at C204, DF28 and E020.

The reconstruction is grounded in the actual TH05 original disassembly and
retained ReC98 `th04/main/sparks.asm`. It is reviewed native assembly
ownership, not a claim to historical compiler source or a copied target byte
array. The complete raw graphics/particle buffers and provider function bodies
remain foreign. Named physical geometry, age/flag state and 16-byte record
size come from existing canonical `update_types.inc` and `lifecycle.hpp`.

Focused receipt `.analysis/gpt-web-spark-scene-render-asm-a/receipt.json` verifies
two independently assembled/linked complete **60/60 byte** positives, native
ordered zero fixups, real map/source LEDATA/publics and true DS/CS frames. Its
own semantic negative changes the GRCG color from12 to13 and is rejected.
The trailing one-byte alignment is compared but earns no authored credit.
Exactly **59 reviewed ASM instructions bytes** are newly accepted. Previously
accepted spark motion update and the actual 102-byte `@spark_render` worker
were unchanged and were not cold-replayed.
