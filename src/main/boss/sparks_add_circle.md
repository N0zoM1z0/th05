# Source-backed radial spark-circle generator

The real near-Pascal `sparks_add_circle` function at MAIN
`[16EE8,16F52)` handles 64 circular Spark records of 16 bytes each. Its
native source logic survives in ReC98 `th04/main/spark_a.asm`: reject centers
outside the unsigned playfield bounds, then generate a radial array of spark
velocity vectors while advancing the actual 1024-byte circular offset.

Unlike a C++ translation that would add register/stack moves, the maintained
`src/main/boss/sparks_add_circle.asm` expresses the genuine original 16-bit
register flow. The original near `VECTOR2_NEAR` and all DS state are external;
this source owns no spark pixels, image data or derived sprite tables.

The function's near Pascal arguments are the original center coordinates,
radius and count; the count is on `[BP+4]`. Every live empty slot receives the
center and a vector velocity calculated from its angular slot. Used slots are
skipped, but the circular slot pointer still advances, wrapping after 64.
The function has a 105-byte instruction body followed by one real `EVEN` NOP,
which is checked but never credited. Original behavior includes no zero-count
guard or added entity validation.

The native source is `SPARK_A_TEXT/main_03`, original `CS=1527`, and original
DS=209D; the source-free binder places the true foreign `VECTOR2_NEAR` helper
at `152DA`, the 16-bit spark ring cursor at DS41DC and the 64-slot Spark
array at DS5AEA. No foreign function or initialized state is supplied. The
arguments `count/radius/Y/X` use the real near-Pascal stack offsets; the
routine's short bounds branch skips the SI/DI saves, as in the original
source. It is accepted as a fully reviewed source-backed register-ASM
algorithm, not as a conjectured Turbo C++ compiler output.

Two independent TASM32/TLINK producers match all **106/106 original bytes**
(including the uncredited trailing EVEN NOP at +105), the unchanged empty
native relocation list and all MAP/public boundaries. The semantic negative
changes the real Spark alive flag value 1 to 2 and fails comparison. Receipt:
`.analysis/gpt-web-main-sparks-circle-106-asm-a/receipt.json`.

This adds **105 reviewed ASM instruction bytes**, not 106, and does not
re-credit the independently accepted 22-byte `player_sparks_circle()` far
wrapper at `[176B8,176CE)`, which directly invokes this unchanged helper.
