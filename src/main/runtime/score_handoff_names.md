# Score-path MAINE child filename and preceding blank field

Decoded MAIN `[21E40,21E49)` is nine bytes of original near-DATA:
the three-byte second blank-caption string `"  "` and the six-byte
third, independent `"maine"` child-program filename. The original
`th05_main.asm` labels these as `asc_226B6` and `aMaine_1` and
shows `aMaine_1` passed to the real `GameExecl()` handoff after setting
the resident `ES_SCORE` end-sequence flag. The earlier `end_game()` and
`end_extra()` paths each have their own separate mutable `maine` name,
already owned by the adjacent independent 12-byte C DATA reconstruction.

The source groups the original adjacent allocations in a byte-only
`ScoreHandoffNames` struct to preserve the three-byte blank caption and
natural odd offset of the six-byte filename. This is a source-level
physical grouping, **not** a claim that the original compiler declared
that struct type. Its field offsets and nine-byte size are asserted.
Both strings remain writable; there are no fake word-padding bytes.
The neighboring preceding blank caption and following unknown zero/
score data remain outside this claim.

The bounded native replay at
`.analysis/unit-replays/gpt-web-main-score-handoff-a/receipt.json`
passes two independent Borland C producers, complete 9-byte
initialized-DATA OMF/MAP contribution, full original raw equality and
empty ordered MZ fixups. A compiled `maine`→`mainf` mutation of the
score child path is rejected. No gameplay function, foreign DATA, or
whole-executable cold replay is included.
