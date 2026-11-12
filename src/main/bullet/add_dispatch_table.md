# MAIN three-mode enemy bullet creation callback dispatch

Decoded original MAIN `[2191C,21922)` is one complete six-byte natural
C++ initializer containing three 16-bit *near function pointers* in
main_03. The real original enemy bullet scripting dispatcher at
`_reference/ReC98/th05_main.asm` uses `off_2129C[bx]` to choose
its near callback after setting up and tuning `bullet_template`.
The original source declaration lists the functions in exactly this
order: `_bullets_add_regular`, `_bullets_add_regular_fixedspeed`, and
`_bullets_add_special`. Each has an independently confirmed original
near CODE public at main_03 offsets 1F94, 1FC6 and 1FA8, respectively.
These are callable executable addresses, not literal data constants or
art assets.

The maintained source declares the three real `extern "C"` near
functions and initializes the typed near-callback array from their
**source-level symbols**. The original two-byte near pointer ABI and
all six initializer bytes are compiler/linker generated; no target
pointer value, code body or relocation is embedded. The binder defines
only the three outside CODE publics and the genuine original MAIN
segment frames, plus the DATA prefix at DGROUP `209D:0F4C`. The
preceding two unknown bytes `[2191A,2191C)` and following two unknown
bytes `[21922,21924)` are outside the claim. The already accepted
`ST00.STD` string starts at `21924`.

Both independent Borland C++ producers in
`.analysis/unit-replays/gpt-web-main-bullet-mode-dispatch-a/receipt.json`
match all six original bytes, the complete OMF LEDATA/SEGDEF and MAP
contribution and the original empty ordered MZ fixup stream. A real
compiled control replacing the *middle fixed-speed callback* with
ordinary spawning changes the DATA value and is rejected. The
historical variable name and source TU grouping are not inferred;
this unit proves the complete typed initializer contribution in its
original linker context, not whole-executable function connectivity.
