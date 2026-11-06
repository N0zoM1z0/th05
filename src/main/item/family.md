# Exact item initialization and collection family

The complete natural C++ contribution MAIN `1CC0E..1D0AD` contains six
functions and 1,183 compared bytes: 1,168 instructions, 14 compiler switch-table
bytes and one uncredited zero. The whole source owns no initialized DATA or
BSS. CS is `1527`, group `main_03`; DS is `209D`.

| Complete function | Native start | Bytes | Coverage |
| --- | --- | ---: | --- |
| `items_init()` | 1CC0E | 29 | New |
| `items_add(int,int,item_type_t)` | 1CC2B | 165 | Preserved |
| `ITEMS_MISS_ADD` | 1CCD0 | 220 | Preserved |
| `item_extend_check()` | 1CDAC | 79 | Preserved |
| `item_collect(item_t near*)` | 1CDFB | 620 | New |
| `item_miss_penalty(item_t near*)` | 1D067 | 70 | Preserved |

The maintained TH04 `src/main/item/items_update.cpp` supplies the coherent
source-family model and its actual `#pragma option -a` after includes.
The accepted 20-byte item, 10-byte splash, full Motion and callback types stay
unchanged. First declarations place all six owned functions in one contribution.
Existing spawn/extend/collection bodies are included once, with only guarded
standalone selectors added to their original wrappers. Initialization adds
ordinary IRand masking, splash reset, attraction reset and the observed foreign
WORD reset. It uses the real full-word far Pascal random API, not a fake
byte-return declaration. The DS C650 WORD's semantic name follows TH04;
its storage receives no ownership credit.

The standalone collection had 619 compiled bytes against 620 and failed its
original internal relocation order. The genuine preceding 29+385+79 functions
and the donor's normal alignment context recover both gates: the compiler now
emits the zero at family+1098 (collection+605), followed by all seven generated
WORD targets at family+1099. The two real compiler record runs reproduce the
original 18-site order, including the transition near family+1024. No fabricated
prefix, padding directive, table payload, empty barrier or output edit is used.
This establishes reproducibility, not the literal historical TU or record cuts.

The source retains unchecked historical collection semantics: the big-power
lookup still precedes its clamp, stage point items increment as a byte, normal
and full-dream rewards differ, and score_delta receives the unsigned base
reward. Existing full records, global widths, near/far pointers and Pascal
cleanup remain intact. No extra validation or defensive branch is introduced.

`main-item-family-whole-e` passes two fresh deterministic compiler producers,
complete valid OMF/MAP, all 1,183 raw bytes and every original fixup in order.
The shared compiled full-dream reward 12800-to-12801 negative is rejected.
The real C/Pascal `ITEMS_MISS_ADD` public remains unmangled; the family is
accepted as one complete contribution, without an invented C++ alias.

Explicit adoption replaces the old `main-item-spawn`, `main-item-extends` and
`main-item-miss-penalty` records, preserving their 534 previously accepted bytes
and four functions. Only initialization 29 and collection 620 are new coverage:
**649 compared / 648 authored bytes**, two functions. Net new credit is 634
instructions plus 14 compiler-table bytes; the one zero earns none. Three old
units become one whole unit, so the bounded unit count decreases by two.
Every unrelated acceptance record remains identical. Installed probes and
unrelated objects are reused after dependency identity checks; no whole cold
replay, CPU model or new behavioral test runs.

Native/source/boundary review: `.analysis/item-family-native-source-review.json`,
SHA-256 `cb8a1ec5fb36507b0decae4bf5a56d90fd21a408d9e86b4018998140147ebdd3`.
Final receipt: `.analysis/unit-replays/main-item-family-whole-e/receipt.json`,
SHA-256 `ca9d5d23e55136223fc3137703464f213d85c5c67c9f50e625d7797e97d6a2c3`.
The explicit no-overlap migration is recorded in
`.analysis/item-family-acceptance-migration.json`. Earlier preparation,
whole-family diagnostic and function-scope registration failures add no credit.
