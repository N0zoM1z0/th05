# Score-path MAINE handoff and the Game Over erase text public

The decoded MAIN DATA interval `[21E40,21E49)` contains exactly nine
source-initialized bytes. Its first three are the *second* independently
writable two-space erase caption, and its next six are the third writable
MAINE child-executable filename. The original `th05_main.asm` labels
these as `asc_226B6` and `aMaine_1`, used by the real `GameExecl()`
score/end-sequence handoff. The earlier normal and Extra end paths each
have their own distinct six-byte MAINE name, independently accepted in
`end_binary_names.c`; these strings must not be merged or pointer-aliased.

The original source was first modeled with an anonymous byte-only
`ScoreHandoffNames` struct so the Borland compiler would produce the
complete 3+6 DATA contribution without inserting alignment or pooling
identical names. Now it uses *independent, named near C publics*:
`gameover_erase_out[3] = "  "` and `maine_binary[6] = "maine"`.
Both ordinary mutable arrays are naturally emitted in their original
order and exact physical positions, at DS `209D:1470` and
`209D:1473`; no linker alias, original-address literal, synthetic
padding or instruction byte is necessary. The accepted C++ Game Over
renderer reads the blank field when animating the exit text and passes
`maine_binary` to the real `GameExecl()` loader for the score ending.
The source-level declaration in `gameover.hpp` now matches the writable
C filename object.

Two independent Borland C producers in the scoped receipt
`.analysis/unit-replays/gpt-web-score-canonical-publics-a/receipt.json`
match the complete original nine bytes and one OMF/MAP DATA contribution,
with the original empty ordered MZ fixups. The compiled filename
mutation to `mainf` is rejected. The separately accepted full
**869-byte** Game Over/Continue CODE contribution was also recompiled
in the affected scope with the new canonical field declarations,
and all original raw bytes, fixups, checked NOPs and compiled semantic
negative remain exact:
`.analysis/unit-replays/gpt-web-gameover-score-handoff-consumer-a/receipt.json`.
No neighboring unknown state, other DATA or full executable is claimed.
