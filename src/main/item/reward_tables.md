# Item reward and sprite tables: candidate

The natural initialized DATA owner is `[0x227D4,0x22848)`, 116 bytes in
MAIN's MZ program image, or `209D:1E04..1E78`. It owns three complete arrays:

| Object | DS offset | Bytes | Meaning |
| --- | --- | --- | --- |
| `ITEM_PATNUM` | `1E04` | 14 | Sprite for each of the seven actual item types |
| `POWER_OVERFLOW_BONUS` | `1E12` | 86 | 43 reward levels, with level0 also used before full power |
| `DREAM_SCORE_PER_ITEMS` | `1E68` | 16 | Legacy eight-entry Dream reward schedule, in ten-point units |

The source uses enum-based sprite expressions and ordinary integer reward
initializers. It preserves the accepted declarations of the constant signed
sprite words and mutable signed overflow words. The Dream array's unsigned
word declaration follows the maintained TH04 collection donor; all original
entries are positive or zero, so the binary alone cannot distinguish signed
from unsigned. The full table remains present in TH05 even though the revised
TH05 collection algorithm does not perform this legacy lookup.

Candidate provenance is pinned ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th04/main/item/items[data].asm`, `th02/main/power_overflow[data].asm`, and
`th05/sprites/main_pat.h`. These are semantic DATA definitions, not executable
instruction transcriptions or opaque asset arrays. Maintained TH04
`src/main/item/items_update.cpp` corroborates the Dream declaration. Neither
reference acceptance nor TH04 layout is treated as TH05 exact evidence.

The three complete arrays and all values were independently checked against
the locally attested supplied MAIN, SHA-256
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
No MZ relocation falls inside the interval. There are no gaps, alignment bytes
or executable functions, and no configured unit overlaps this interval.
Adjacent play-performance bytes at `1E02..1E04` and mutable item state from
`1E78` are excluded; no initialized-zero/BSS placement assumption is needed.

The private outside-only binder supplies empty actual compiler segment
contexts, the original DATA base, and the foreign DATA prefix. It supplies no
owned values, function bodies, helper aliases or artificial stack. Existing
accepted headers remain unchanged. The compiler must still demonstrate the
three arrays' actual storage order and extent in MAP/OMF.

This packet is uncompiled and unaccepted. Native metadata and unit/control
proposal are `.analysis/item-reward-tables-boundary-review.json` and
`.analysis/item-reward-tables-unit-proposal.json`; the proposed negative
changes the overflow reward150 to151. Acceptance requires two fresh exact
producers, empty original ordered fixups, and the compiled negative. This is
116 candidate semantic DATA bytes and zero candidate CODE/functions.

Focused `main-item-reward-tables-data-a` now accepts the complete116-byte DATA
contribution from two fresh producers, empty ordered fixups and its own rejected
150-to151 reward mutation. All three complete arrays are generated from their
semantic declarations; there are no CODE/function/padding credits. Existing
canonical headers and code owners were neither changed nor replayed.
