# MAINE semantic verdict UI DATA

Two new independent ordinary C++ DATA owners define readable Japanese labels,
messages and filenames already referenced by the accepted verdict routines.
They preserve the exact existing `const shiftjis_t near[]` and
`const char near[]` interfaces. The shared new header repeats those declarations
without modifying accepted headers or changing any element/pointer type. It
contains no storage definitions. All source text is UTF-8 and both entries
require the existing explicit CP932 staging pipeline.

| Accepted owner | Original DS range | Original decoded load range | Objects | Bytes |
|---|---|---|---:|---:|
| Metric/heading labels | 1620..16BC | 11730..117CC | 13 | 156 |
| Score messages/resources/stage headings | 16C2..173A | 117D2..1184A | 12 | 120 |

The first owner contains the bonus percent sign, screen heading and metric
category labels. The second contains the score unit, comment/picture filenames,
unrated and slowdown messages, and complete stage/final-score headings. These
are addressable semantic text objects, not bitmap/font/image data or opaque
numeric arrays. Every NUL terminator belongs to its complete source string.
All25 objects have independently decoded original pointer pushes in the real
verdict routines. Their CP932 literal sequences reproduce the original276
bytes; neither extent contains MZ relocation words, padding or a table.

## Const identity and conservative scope

An earlier uncompiled294-byte monolithic text hypothesis contained physically
distinct but identical const initializers. Retained compiler evidence elsewhere
shows that such objects can pool, so that hypothesis was not compiled or
accepted. Its source, binder, proposal and native review remain private under
`.analysis/verdict-ui-monolithic-uncompiled/`; its public CPP/binder were removed.

The two selected producers each contain no identical whole-object initializer.
They are useful semantic object groups, not claims about historical TH05
translation units. No artificial struct, alignment flag, dummy initializer,
manual byte payload or within-owner hole is introduced. Actual compiler DATA
size/coverage still must be checked; source spelling alone does not guarantee
that a compiler will preserve the required physical objects.

The four formatting punctuation objects at DS1614..1620 (12 bytes) and the two
physically distinct `回` counter-unit objects at16BC..16C2 (6 bytes) are outside
both owners. They remain unknown/uncredited. The rank glyph table, formatter
state, staff state and staff filenames are also outside these owners. There is
no overlap with the separate all-cast DATA ranges10930..109FA or10B16..115F9.
No ownership inventory or denominator classification was changed here.

Both symbol-only binders reproduce the original MAINE DS1011 and outside code
frames, ending their foreign DATA prefix at the real first object. All source
objects then belong to the actual compiler's one complete DATA contribution.
The binders supply no string values, relocations, helper instructions, inside
padding or stack. No CODE or BSS ownership is requested.

## Exact acceptance

Both owners passed independent normal strict DATA replays. Each has two fresh
positive producers, one complete MAP DATA contribution and one gapless compiler
SEGDEF/LEDATA extent. Every byte matches the pinned decoded target, with an empty
ordered relocation stream. Both compiler objects are deterministic after only
dependency timestamp normalization. Neither source owns CODE, BSS or padding.

Receipts under `.analysis/unit-replays/`:

- `maine-verdict-metric-ui-data-a/receipt.json`: 156 bytes, 13 objects.
- `maine-verdict-score-ui-data-a/receipt.json`: 120 bytes, 12 objects.

Each replay reused the unchanged installed toolchain proof and compiled its own
DATA negative. The strict imports re-read both actual MZ/MAP/OMF producers and
canonical UTF-8/actual CP932 input identities. Existing accepted verdict sources
and all ten current verdict function records were unchanged and not replayed.
The 276 DATA bytes are accepted in `config/accepted_units.maine.json`; this does
not establish packed-executable equality or the global authored denominator.

The metric negative changes the readable label `気合い` to `気合え`; the score
negative changes the real comment filename `_ude.txt` to `_udf.txt`. Each is a
unique same-width literal mutation in its own canonical UTF-8 source, applied
before CP932 staging. None of the selected CP932 strings contains a5C trailer
byte; no escape workaround or compiler option was added.

Private `.analysis/maine-verdict-metric-ui-data-boundary-review.json` and
`.analysis/maine-verdict-score-ui-data-boundary-review.json` pin every complete
object, actual native reference, accepted interface identity and source input.
The corresponding `*-proposal.toml` files preserve the pre-build proposals; the
live manifest and ledger now register the independently verified owners.
