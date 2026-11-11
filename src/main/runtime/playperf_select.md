# MAIN performance clamp and parameter selectors: reviewed original ASM

The original `MAIN.EXE` `[CF7A,CFC6)` forms a complete, contiguous
76-byte original-register assembly family. The four externally callable
entrypoints are `PLAYPERF_RAISE` at `CF7A` (25 instructions bytes),
`PLAYPERF_LOWER` at `CF94` (24 instruction bytes),
`select_for_playchar(int,int,int,int)` at `CFAC` (5 bytes), and
`SELECT_FOR_RANK` at `CFB2` (20 bytes). The two selectors deliberately
share the tail beginning at `CFB5`, so their compiled contributions cannot
be treated as independent ordinary C++ functions. Original NOPs at `CF93`
and `CFB1` align the next entry; both are compared but excluded from authored
credit. The preceding unowned byte and the next accepted score reset are
outside this family.

The far-Pascal performance helpers read their byte argument at `SS:[SP+4]`
through BX and clamp an unsigned addition against the real maximum at DS
`5771`, or a subtraction under the original signed `JGE` condition against
the real minimum at DS `5772`. The live performance byte is DS `5770`.
`select_for_playchar` uses DS `5773`, `SELECT_FOR_RANK` DS `576F`; both
select one of four word arguments by doubling the byte selector and
indexing the far-Pascal frame through `SS:SP+10`. The family has no
relocations, source-owned DATA/BSS, hidden callbacks or target-byte arrays.

The maintained semantic ASM source follows separately maintained source
families in pinned ReC98: `th04/main/playperf.asm`,
`th04/main/select_for_rank.asm` and `th05/main/select_for_playchar.asm`.
Its real control flow and ABI were independently checked against the locally
attested MAIN disassembly, not inferred from names alone. `EVEN` preserves
actual source alignment, rather than inserting speculative padding; the
reviewed ownership is original assembly, not authored C++.

## Complete native acceptance

The focused native replay
`.analysis/asm-replays/gpt-web-playperf-select-a/receipt.json` passed two
independent genuine TASM32/TLINK producers, the complete 76-byte target
extent, the empty original ordered MZ relocation list, real MAP entry
addresses and valid fully covered OMF LEDATA. Its own source-level mutation
changes the shared selector argument displacement from 10 to 12 and is
assembled and rejected. The preserved independent original instruction and
boundary proof is `.analysis/gpt-web-playperf-select-native-review.json`.

The explicit original-ASM adoption credits **74 instruction bytes** in this
MAIN family. Both original `EVEN` NOPs compare exactly but earn no authored
credit. The independent compiler-generated C/C++ counters and accepted
neighbors are unchanged. The reviewed semantics and source ancestry support
an original-assembly classification, not a claim that the maintained spelling
or assembler is historically identical to ZUN's.
