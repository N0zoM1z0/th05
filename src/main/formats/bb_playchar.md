# Player bomb-background bitmap ownership

Two complete C++ functions reproduce MAIN `[10432,1045B)`: loader18 bytes and
release23 bytes, 41 instruction bytes in total. The original trailing NOP at
`1045B` is outside both functions and receives no credit. Ordered fixups are
`[32]`, the genuine MASTER HMEM_FREE call. There is no compiler table or owned
BSS.

The loader deliberately adds the character index to the existing filename
digit, including on repeated calls. It does not reset the digit or add error
handling. Explicit character conversion keeps the actual byte addition and
recovers the original memory ADD; the initial mixed signed/unsigned-char
expression emitted three additional bytes. The complete existing BB API uses
a far filename, near Pascal call and word-sized allocated-segment handle.
Release keeps its original nonzero test, far free and handle reset.
Documented `-k-` supplies the original frameless compiler context.

The same owner defines the whole seven-byte initialized DATA contribution at
MAIN `[222AC,222B3)`, DS `[18DC,18E3)`: mutable `bb_playchar_fn = "BB0.BB"`.
It is a semantic filename, not bitmap content. The following alignment byte
remains outside the compiler contribution and receives no credit. Full CODE
frame is `0AE1`/`main_01`, DS `209D`; external loader is `0AE1:4B20`, free is
`0000:291E`. Symbol-only bindings supply no bodies or initialized values.

`main-bb-playchar-a` passes two deterministic producers, valid OMF, complete
raw CODE/DATA and original ordered fixups. Separate compiled controls mutate
the filename character position in CODE and the initialized digit in DATA;
both are rejected. Receipt:
`.analysis/unit-replays/main-bb-playchar-a/receipt.json`, SHA-256
`56b3a3765908a185dd28692c31f8fa94769669dc8de42f5190837620399bc878`.
Native boundary/data review: `.analysis/bb-playchar-boundary-review.json`.
Pinned ReC98 `b6ba5b0a` and TH04 supply semantic references, not acceptance or
proof of historical source spelling.
