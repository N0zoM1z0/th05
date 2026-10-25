# Verdict settings and rank labels

The complete DATA owner is MAINE load `116F2..11724`, 50 bytes, at original
DS `1011:15E2..1614`. It defines seven existing global objects in their real
types and order:

| Object | DS offset | Size | Meaning / initial value |
| --- | --- | ---: | --- |
| verdict_text_left | 15E2 | 2 | Left coordinate 336 |
| verdict_text_color | 15E4 | 2 | Text color selector 2 |
| verdict_comment_color | 15E6 | 2 | Comment color selector 6 |
| verdict_text_top | 15E8 | 2 | Top coordinate 48 |
| skill_subtract | 15EA | 1 | Subtraction mode initially false |
| verdict_rank_glyphs | 15EB | 40 | Five complete eight-byte glyph strings |
| graph_3_digit_put_as_fixed_2_digit | 1613 | 1 | Fixed-decimal mode initially false |

The array contains EASY, NORMAL, HARD, LUNATIC and EXTRA. Each has seven
visible cells, right justified with the actual EMPTY glyph, and its own NUL.
These are semantic character selectors, not font pixels or opaque payload.
GAME5's alphabet begins at AA and proceeds through Z; M precedes N. The older
TH02 bold-font names swap those two positions and are not blindly reused.
Original code derives the row from the actual rank or Extra-stage selection,
multiplies it by eight, and passes the row to the real gaiji-string renderer.

The DATA-only header preserves the exact canonical underlying types from
`format.hpp`, `display.hpp` and `main.hpp`: signed-word coordinates,
unsigned-word colors, the real unsigned-byte bool typedef and mutable
`char[5][8]`. It uses unchanged `resident.hpp` for that bool definition.
No accepted header, caller, array type, near/far API or source token is changed.
The original Borland 31-character formatter-symbol truncation is preserved
in the actual PUBDEF/MAP. No fake legacy aliases are needed for these globals.

All 50 bytes are initialized semantic state/text. There is no CODE, BSS,
table asset, padding or original ordered MZ fixup in this owner. The outside-only
binder supplies no initialized values or artificial stack. Its real frames are
GROUP_01 at A54, separate SHARED at E80 with no group, and DGROUP at 1011.
The new compiler's empty CODE segment belongs only to GROUP_01; DATA and BSS
retain their original word alignment. Every ORG remains below 64 KiB.

The first `maine-verdict-state-data-a` pair passed DATA bytes but exposed an
unwanted empty foreign SHARED SEGDEF inherited from the full logic header,
which grouped the binder's SHARED into GROUP_01. It is not imported. A new
DATA-only header removed those unused function selectors without changing
any canonical ABI or compiler option. Attempt b stopped at compilation because
TC4 requires the historical bool typedef; including its unchanged defining
header fixed that omission. Attempt c passed after that correction. The final
private glyph enum was then kept in the CPP so the new public header can coexist
with the canonical formatter's enum. These intermediate producers are retained;
none is relabeled as final source-current evidence.

Final strict evidence is
`.analysis/unit-replays/maine-verdict-state-data-d/receipt.json`: two fresh
deterministic complete compiler DATA producers, gapless SEGDEF/LEDATA coverage,
actual MAP/PUBDEF/frame checks, full raw bytes and empty literal ordered fixups.
Its own compiled negative changes the visible NORMAL label to MORMAL and is
rejected over the full 50 bytes. Installed execution probes and all unchanged
accepted objects are reused. No packed-executable or global-percentage claim
follows from this bounded DATA owner.

Independent source/native review is
`.analysis/verdict-data-source-native-review.json`, SHA-256
`492e3eb12cb77b94cf9bdec5c2590563bacb5390d01de3b719af7507ac60eb6d`.
Root independently reread both actual final MZ/MAP/public/frame outputs in
`.analysis/verdict-state-data/root-final-native-review.json`, SHA-256
`e93c89ac086564a47e5e705b64d7a5deb48ffc2733563face3392276e11ed50a`.
