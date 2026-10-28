# Aimed-sword and laser/sword recovery

Two complete MAIN bodies now reproduce all original instruction bytes:
aimed swords `[1F088,1F1EA)`354 and laser/swords `[1F3F0,1F59C)`428.
Their109/132 native instructions, branches and final near returns are reviewed;
there are no instruction NOPs, tables or padding. **Neither is accepted**:
original relocation order differs from each standalone compiler result.

| Scope | Original relocation offsets | Standalone compiler |
| --- | --- | --- |
| Aimed swords354 | 71,329,309,203 | 329,309,203,71 |
| Laser/swords428 | 232,72,402,382 | 402,382,232,72 |

The aimed body is canonical in `aimed_swords.inl`, included by its independent
wrapper and the existing unaccepted combined family. The local word-value aim
adapter removes the old three-byte Subpixel temporary. Native171CC reads X/Y
as words at BP+8/+6, angle as a byte at BP+4, and returns RET6. Both canonical
Subpixels are two bytes; their original declaration and full types are unchanged.
The function-pointer view forwards the same values to the same real symbol.
It introduces no helper implementation or physical-register arithmetic.

The new laser/sword body retains the full Laser24, Sword26, Boss24 and template
records. Its setup, paired aimed volleys, random laser origins, two random
swords and HP-triggered rank transition are semantic C++. The final rank vector
is40/48/52/48. An initial argument-order mistake and a declaration-order trial
remain failed diagnostics; only the corrected body has428-byte raw equality.
An initial link failure from an empty main_01 segment beyond64K was corrected
by placing that real empty segment at its actual group context.

Standalone raw matches: `.analysis/native-producers/main-yumeko-aimed-swords-a`
and `main-yumeko-laser-swords-d`. Each is one diagnostic producer, not an exact
receipt; no unnecessary second producer/control was run for known order failures.

A genuine original-order prefix of allocator121, updater280 and three-pattern
family435 emits LEDATA `[0,1021)`/`[1021,1190)` and restores the aimed function's
original relocation stream. However, the updater is three bytes short of283,
so aimed entry is1F085 instead of1F088 and relative calls differ. The first
prototype also keeps its definition in B5_UPDATE_TEXT; a later selector does
not move it to the requested segment. This context attempt failed its requested
scope gate and is preserved privately, with no imported scope or filler bytes.

The next task is the genuine updater/source-context gap, not relocation sorting.
All782 raw-matching bytes remain unknown in authored-exact progress. Joint
review `.analysis/yumeko-later-root-review.json`, SHA-256
`1099a5063c7943fba749a258d3e449b1fdf1c75c916d329b5ef33cdbda94001c`.
