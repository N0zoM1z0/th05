# CONTINUE score entry: exact C++

MAIN `C998..C9A3` is the complete 11-byte near C++ void/no-argument entry.
CS is `AE1` / `main_01`, DS `209D`. It reads the byte `turbo_mode` at DS
`5776` and calls the foreign insertion routine at `C8F0` only when nonzero.
The RET at `C9A2` completes the function; the following `C9A3` NOP is outside.
There is no padding, table, DATA, BSS or MZ fixup in this scope.

The natural condition follows maintained TH04's `main/score/ranking.cpp`,
with TH05's actual omission of the score-file load call. The canonical caller
already declares this near C++ interface. No file I/O, validation, defensive
condition or score-state mutation is added. Insertion and the accepted ASM
codec remain separate owners; their acceptance does not transfer.

Two fresh direct C++ producers match valid ordinary OMF, the complete MAP
contribution and all original raw bytes/empty fixups. The normal guard-inversion
compiled negative is rejected. No accepted dependency or build tool changed.

Receipt: `.analysis/unit-replays/main-score-continue-entry-b/receipt.json`,
SHA-256 `20345b78bff26f7fb51164d242ce76d43b390c35e9d5bd127f2c78ceacf0120e`.
Native/source/ABI review: `.analysis/score-continue-entry-native-review.json`,
SHA-256 `e8e58d723c7f709924594eb27b9eee9ca183f2d8811a384af6890dcc42ec4969`.
Target provenance is candidate-local-attested. New credit is one complete
function and 11 C++ instruction bytes, with no whole-game claim.
