# Registration insertion and rendering: exact C++

Two complete adjacent source contexts recover five functions from decoded MAINE:

| Function | Native extent | Instructions | Compiler table | Uncredited zero |
| --- | --- | ---: | ---: | ---: |
| `score_insert` | `B730..B899` (361) | 361 | 0 | 0 |
| `registration_score_put` | `B899..B9C1` (296) | 288 | 8 | 0 |
| `registration_stage_put` | `B9C1..BA84` (195) | 186 | 8 | 1 |
| `reg_name_put` | `BA84..BBEF` (363) | 354 | 8 | 1 |
| `registration_place_put` | `BBEF..BCD3` (228) | 219 | 8 | 1 |

The 551 instructions, returns, direct branches and all sixteen switch-table
destinations are reviewed against the pinned decoded original. CS is A54 /
GROUP_01 and DS 1011. There is no instruction NOP, initialized DATA or BSS.
Complete compared size is 1443; new authored CODE is 1440 = 1408 instructions
+ 32 compiler-table bytes. All three alignment zeros compare normally.

Maintained TH04 insertion, score/stage, row and name-cursor sources provide
structure and API evidence; TH05 native instructions establish every difference.
Insertion preserves equal-score ordering, FF rejection, the eight editable name
bytes and untouched ninth terminator, numeric-to-gaiji conversion and the Extra
rank's stage-marker branch. Rendering preserves the four-character panel layout,
signed leading-score division/remainder, editing-place colors, skipped current
name row, glyph cursor, GRCG borders and final hardware disable. Invalid selector
paths retain uninitialized coordinates; no defensive initialization is added.

Insertion is no-argument near C++; score/row take two Pascal words, stage takes
three words, and name takes a word place plus byte character/cursor in three
Pascal word slots. Full score/resident types and the byte character domain are
imported unchanged. Master graphics retain CS 0000; background restore retains
ungrouped E80:04E4. First declarations keep each real contribution together.

`values.cpp` compiles the genuine consecutive insertion/score/stage bodies.
`display.cpp` compiles the genuine consecutive name/row bodies through one
declaration header. Each body lives once in its `.inl`. Ordinary word alignment
after the canonical types naturally restores the switch-table zeros. Standalone
score and row diagnostics instead emit 297/227 versus native 296/228. An initial
combined display header retained separate first-declaration segments; the common
header fixes that real producer context. Stage's original stack layout requires
the int y declaration before the byte color. No filler, opcode transcription,
compiler-register algorithm, output edit or relocation normalization is used.

Both fresh direct TCC/OMF/MAP/TLINK producers match full bytes and original order:
values `[835,817,629,592,556]`; display
`[574,551,340,322,304,286,269,235,224,185,163,135]`.
The shared score-loop six-to-five negative is rejected. Receipt:
`.analysis/unit-replays/maine-registration-values-display-a/receipt.json`, SHA-256
`2e4fcca99d55de228471d16e6edcda9768397bfa55ecaf5379f38a7c51bcc312`.
Native/source/ABI review: `.analysis/registration-values-display-native-review.json`,
SHA-256 `b08e1ef3a830d18bc9e2ea8239a41fa1a07a140717c9b7a863675bd1caadbe09`.

All older accepted records and dependencies remain unchanged; no old owner is
replayed. No producer tool, behavior model, packed-file or whole-program claim
changes. Target provenance remains candidate-local-attested. These neighbors do
not resolve the [menu's original relocation context](menu.md).
