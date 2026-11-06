# Sound extension and initial-mode resources

`load_resources.c` independently recovers three complete initialized C DATA
contributions,18 bytes each. There is no CODE, BSS, relocation or alignment
padding in these contributions. The six fields are the SE extension, FM26
extension, adjacent FM86/MIDI strings, and three initial mode/availability
bytes. No original neighboring word or buffer is included.

| Artifact | Complete load scope | DS:offset | Receipt under `.analysis/unit-replays/` |
| --- | --- | --- | --- |
| MAIN | `[211F6,21208)` | 209D:0826 | `main-sound-load-resources-exact-b/receipt.json` |
| OP | `[FA32,FA44)` | 0EFE:0A52 | `op-sound-load-resources-exact-b/receipt.json` |
| MAINE | `[107DC,107EE)` | 1011:06CC | `maine-sound-load-resources-exact/receipt.json` |

The first15 bytes are the original extension bank: `efc`, a four-byte `m`
field, then the adjacent `m2` and `mmd` strings. The C initializer expresses
the latter as the seven-byte string `"m2\0mmd"`; it is not a four-by-four
extension array. Its embedded terminator and all array-initialized zeros are
inside the real four-byte copy windows, not compiler-inserted padding.

At offsets15/16/17 the initial SE mode, BGM mode and MIDI-possible byte are
all disabled. The loader's unsupported mode3 still reads bank+12 as `md`,
with its fourth copied byte overlapping SE mode. Source retains this original
layout and behavior, without a new terminator, guard or fourth full field.
The field/size assertions check18 bytes and the three state offsets.

Semantic evidence is pinned ReC98 b6ba5b0a's `th05/snd/load[data].asm` and
`th04/snd/snd[data].asm`, the maintained TH04 sound state owner, and the
independently reviewed TH05 [loader](load.md) and [driver probes](resident.md).
TH04's different extension-pointer table is not imported. The original loader
uses the bank at DS0826/0A52/06CC and mode bytes15/16; resident detection and
mode selection independently establish byte17. All18 native bytes in each
target were checked before compiling. Their identical extent SHA-256 is
`f78e5f64269b01ac669d1011c2f659235551686350a32db5160d2ee513e66cae`.

Each focused DATA replay passes two deterministic C builds, valid OMF, whole
MAP/LEDATA ownership, all18 raw bytes and the empty original ordered fixup
stream. Its own compiled `efc`-to-`efs` mutation changes DATA and is rejected.
MAIN's initial scaffold exceeded the16-bit ORG limit and was split into legal
foreign segments before any successful producer. OP retains the actual foreign
Music Room DATA end at DS2817, as the already accepted priority-bank scaffold
does, so its validation MZ has a valid minimum allocation. No artificial stack,
owned payload or function body is supplied by a binder. Foreign prefixes and
tails receive no credit.

Receipt SHA-256, in table order:

* `afca925f2236346169b8063a8e53ee54f0e1402fc0f2567d7c1b2294fb460c4b`
* `ec9e1746f44ae925cab54c352778fd77e601163d7ae8796161e77c07a8dbb83c`
* `2201c494a9722c85ba382607ff000f6e809fe6e76380832b94c90148707f9432`

Native field routing is retained in `.analysis/sound-resource-bank-review.json`.
The new54 bytes receive initialized semantic C DATA credit, separately from the
loader's reviewed ASM and the probes' C++ CODE. No old source/header changed,
and no unchanged accepted unit was compiled. Literal historical source,
standalone linkage, packed files and whole-executable exactness remain unproved.
