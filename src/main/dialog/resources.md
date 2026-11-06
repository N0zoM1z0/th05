# Dialog initialized resources

Two complete semantic C DATA contributions reproduce137 original MAIN bytes:

| Owner | MAIN load range | DS range | Bytes | Ordered segment fixups |
| --- | --- | --- | ---: | --- |
| Resource bank | `[228B8,2293D)` | `[1EE8,1F6D)` | 133 | empty |
| Initial script pointer | `[2289C,228A0)` | `[1ECC,1ED0)` | 4 | `[2]` |

The bank contains the signed-byte dialog sequence ID,15 actual filenames or
basenames, and the three-byte Kanji scratch string initialized to two spaces.
It preserves the mixed-case mutable faceset templates, four character-specific
bomb backgrounds, extra-stage sprite/music/replay resources and return binary.
The complete C-compatible record has17 named fields; its size and important
field offsets are checked at compilation. Every byte has a reviewed semantic
field. It embeds no dialog script, bitmap or opaque target-derived array.

The real mutable `char far *dialog_fn` initially points to the bank's script
filename at `209D:1EE9`. This is a normal C address initializer and real linker
relocation, not a copied segment/offset pair. Existing validated dialog-file,
animation and face-loading consumers establish the field addresses and uses.
Pinned ReC98 `b6ba5b0a`, TH04's shared dialog conventions and the original TH05
image supply supplemental evidence; reference acceptance does not transfer.

Each unit covers its whole actual compiler `_DATA` contribution in DS209D.
There is no owned CODE, BSS or padding. The original24-byte BOX_TILES pattern
between pointer and bank remains foreign, as does the alignment byte after the
bank at DS1F6D. Context binders supply only segment extents and external labels.
These remain bounded DATA results, with whole-executable linkage unclaimed.

Both replays pass two deterministic producers, valid OMF, complete raw bytes
and original relocation order. Each rejects its own compiled DATA mutation:
the bank changes the extra boss music basename; the pointer chooses the boss
faceset filename instead of the script. No unchanged function is recompiled.

- Bank receipt: `.analysis/unit-replays/main-dialog-resource-bank-a/receipt.json`,
  SHA-256 `715b8eab639c7fe7f9d21b3076c820a1fe218cb1ff747a52110cf4bfd12a7cad`.
- Pointer receipt: `.analysis/unit-replays/main-dialog-resource-pointer-a/receipt.json`,
  SHA-256 `a9a407bd625e965609ba51ea2414a89baa3ce5aaa0f9af8aef084793c068f190`.

Complete field/extent/ABI review: `.analysis/dialog-resource-data-review.json`.
