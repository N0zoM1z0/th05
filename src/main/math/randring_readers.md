# Byte-ring random WORD readers

Two complete three-entry families share the real byte ring DS3526..3626
and adjacent WORD cursor DS3626..3628. Instance1 is MAIN C700..C73E, 62 bytes;
instance2 is 1529C..152D9, 61 bytes. Both have 59 instruction bytes. The first
two entry alignments are relative13 and35; instance1 additionally ends with
alignment at61. All five NOPs compare normally with zero credit. The zero at
152D9 and the following vector procedure remain outside both contributions.
Neither family has a table, DATA/BSS or MZ fixup.

The entries return a raw WORD, a WORD masked by the caller's argument, or an
unsigned remainder. They load two overlapping bytes at the full WORD cursor
and increment only its low byte, after the load. At index255, the high sample
byte is the adjacent cursor's old low byte; there is no added boundary check
or circular two-byte read. Modulo by zero retains its original divide error.
The ring contents and cursor initialization remain foreign; the already
accepted C++ fill routine is unchanged.

The near no-argument entry returns in AX. The AND/MOD entries are near Pascal,
consume a full WORD argument with RET2, and address SS:entry-SP+2 through BX
after its ring-index lifetime ends. All preserve BP/SI/DI/DS/ES and IF/DF;
BX and arithmetic flags are scratch, and MOD also changes DX. This leaf
register/stack protocol and the identical copies in main_01/main_03 support
independent handwritten-ASM inference. The candidate macro is ReC98 b6ba5b0a
th04/math/randring.inc; its modern filename alone is not the language proof.
Historical source/assembler identity and exhaustive vendor ancestry remain
unknown. No failed C++ trial is used to infer ASM ownership.

The maintained family macro derives argument displacement and cleanup from
the WORD/near interface and factors the shared sample/advance operation. The
binders contain only native frames and foreign labels, no initialized ring,
cursor, instructions or stack. No opcode byte or target data is emitted.

An independent ordinary C++ raw-reader candidate remains unaccepted and outside
live manifests. Its natural local emits21 bytes; a register local emits15 with
an extra DX-to-AX transfer; a prefix-increment form emits19. The compact
15-byte postincrement source is retained. Their first size gates reject them,
so no second producer, negative or behavior model is run for those failures.
See private `unit-replays/main-randring-next-{a,b,c}` under `.analysis/`.

Both families pass two fresh deterministic producers, valid complete ordinary
OMF/CODE/LEDATA contributions, native publics/CS/DGROUP, every raw byte and
empty original fixup streams. Each normal shared-cursor negative increments
its high byte instead of the low byte and is rejected with unchanged extent
and fixup order. Normalized objects, MAPs and complete MZ outputs agree between
producers; only dependency timestamps are normalized. Explicit adoption adds
118 ASM instruction bytes, with five compared alignment bytes credited zero.
Existing accepted source and tool execution proofs are reused after identity
checks; no whole replay, extra negative or CPU model was run.

| Instance | Receipt under `.analysis/` | SHA-256 |
| --- | --- | --- |
| 1 | `asm-replays/main-randring-1-a/receipt.json` | `a340f3eba11bb951ae6ae3132cdf6344bcc0d6d69bb745876d23afa128500fc0` |
| 2 | `asm-replays/main-randring-2-a/receipt.json` | `af781fdf17fc79c4e949b8158d183ef39d069faf6836833c6e3dc298686f298a` |

Native proofs under `.analysis/`:
`randring-1-native-review.json` (`4e57c957eda40336b9527f1d15ac3836c697fedac43794778872575b847fcca3`).
`randring-2-native-review.json` (`28749f1e4a39f49292c69fd3003422b3f9e62f7cbd2f926e4983d09129eb3b22`).
