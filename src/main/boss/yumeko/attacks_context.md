# Yumeko original compiler source context

This translation unit includes the real maintained sword renderer, allocator,
updater and seven adjacent attack routines in native definition order. Its
`TH05_YUMEKO_COMBINED_CONTEXT` define only suppresses repeated `-zC/-zP`
**translation-unit** pragmas. Normal standalone compilations still receive
their historical flags and canonical function bodies. The renderer is compiled
in main_01 and the remaining functions in main_03 with their natural near,
far and Pascal interfaces preserved. The updater now uses the ordinary `-O`
profile with two narrowly scoped inline-ASM control-flow islands; the following
`#pragma option -O` keeps the same normal jump optimization for later attacks.

The retained true symbol-only binder contributes no instruction or initialized
storage: it anchors all foreign providers and code frames, and its sole code
tail begins after the entire real main_03 compiler contribution at `1F59C`.
Actual MAP confirms the main01 66-byte renderer at `143E0`, main03 CODE from
`1ED41` through `1F59C` (2139 bytes), and DS frame `209D`.

The complete current 2,139-byte MAIN03 emitter is now raw-exact, including
its 283-byte `swords_update` slice and all 25 original ordered MZ fixups. The
updater uses C++ with two narrow inline-ASM control-flow islands to retain the
original short clip and collision joins. Two fresh native diagnostic producers
reproduce the complete contribution byte-for-byte. The 283 bytes remain owned
and credited **only** by the accepted `main-yumeko-swords-update-asm` family;
this overlapping hybrid context does not create a second C++ CODE claim.
The 354-byte aimed-swords and 428-byte laser/swords functions remain separate
accepted complete functions, and the four unchanged prior source bodies retain
their focused replay receipts. The existing 782 authored C++ byte credit is
unchanged.

The first successful single-producer mixed-cohort diagnostic is
`.analysis/gpt-web-yumeko-ten-function-context-a/`; the canonical
source-inclusion diagnostic is `...-b/`. Both normal positives and own
compiled negatives are frozen for the accepted units under the
`gpt-web-main-yumeko-{aimed,laser}-context-20261110` receipt roots. This is
actual compiler buffering evidence, not a claimed original historical
translation-unit boundary.
