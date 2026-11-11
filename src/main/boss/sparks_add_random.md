# Complete source-backed random Spark spawner

The original `sparks_add_random()` at MAIN `[16E86,16EE8)` is a full 98-byte
near-callee/far-Pascal-entry spark state machine. The pinned original
`_reference/ReC98/th04/main/spark_a.asm` retains its complete semantic
algorithm and 16-bit register/stack contract. The maintained `sparks_add_random.asm`
uses named Spark sizes and fields and only external original-game symbols.

It checks both 16-bit unsigned center coordinates before preserving SI/DI;
then visits exactly `count` ring slots even when occupied. A free slot becomes
alive and receives the original center and velocity produced from the existing
near Pascal RNG `(mask 31)` and vector helper. All 64 sixteen-byte slots share
one mutable 1024-byte ring cursor, wrapped at exactly 1024. No new zero-count
guard, output normalization, memory allocation or foreign helper body is added.
The original function returns `RETF 8`, with the two 16-bit center words,
radius and count on the true four-word far-Pascal stack.

## 2026-11-11: accepted 98-byte complete original-register ASM

`SPARKS_ADD_RANDOM` is independently accepted as the full unpadded original
`[16E86,16EE8)` code scope, **98/98 raw instruction bytes**, with both
independent TASM32/TLINK producers and the original empty ordered relocation
stream byte-exact. The compiled negative changes the original random radial
speed-span mask from 31 to 30, changing real code bytes and being rejected.
The independent native review decodes all 36 original instructions, preserving
original far `RETF 8`, initial bounds exits, original live/free flag values
and all instruction/stack boundaries. No raw target opcodes are supplied as
ASM source, no artificial jump padding or unowned entity storage is generated.

The source-free `sparks_add_random_bindings.asm` anchors the true `main_03`
CS at 1527, DATA at 209D, ring cursor DS41DC, ring records DS5AEA, RNG
callback at load `152AA` and near vector service `152DA`. The source
`src/main/boss/sparks_add_random.asm` and semantic field/type declarations
remain separate from the previously accepted near-Pascal 106-byte
`sparks_add_circle.asm` so the existing accepted input snapshots do not drift.

Receipt: `.analysis/gpt-web-main-sparks-random-98-asm-b/receipt.json`.
This adds **98 reviewed ASM instruction bytes** and does not duplicate the
neighboring 105 authored bytes + one uncredited NOP in the radial spark
routine at `[16EE8,16F52)`. Together they represent 203 consecutive authored
bytes from two real functions and one compared but uncredited EVEN NOP.
Historical original source authorship remains uncertain beyond the preserved
register-level ReC98 reconstruction and native code evidence.
