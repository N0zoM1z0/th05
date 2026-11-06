# Dialog exit background restoration

The complete MAIN function `[14007,14081)` is 122 compared bytes: 113
instructions, eight compiler switch-table bytes and one uncredited zero.
It restores the player bomb background from EMS offset 34000 or selects the
appropriate one of four external character filenames. The complete existing
EMS/CDG types, word-sized plane multiplication and unchecked allocation remain
unchanged. There is no owned DATA/BSS or instruction NOP.

`exit.cpp` preserves the maintained `tail.cpp` function body literally in an
independent compiler contribution, as already done for dialog animation.
With the existing late `-a2`, this naturally emits the original switch-table
alignment: the zero at relative 113 and table at 114. The old combined tail
emitted 121 bytes because its preceding functions changed the compiler's
alignment phase. No filler, target byte, table initializer, assembly body or
output patch is supplied. The eight table bytes come from the semantic switch.

The real near CODE frame is `0AE1`/`main_01`, DS `209D`. Allocation and EMS
read retain the MASTER far Pascal APIs; disk loading retains shared frame
`14AB:0668`. Empty demo segments remain in their actual group context. Every
binder hole lies outside the complete source contribution.

`main-dialog-exit-a` passes two deterministic producers, valid OMF, all 122
raw bytes and original ordered fixups `[108,50,23]`. The shared compiled
Reimu image-index mutation is rejected. Receipt:
`.analysis/unit-replays/main-dialog-exit-a/receipt.json`, SHA-256
`e03acb44c4d7ba10fdea9f72bb75711e02502046e981019bdf39fbec248638e9`.
Native review: `.analysis/dialog-exit-boundary-review.json`.
Only 121 bytes receive authored credit; the zero is compared normally.
