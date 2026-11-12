# MAINE cutscene

Natural source: pinned nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05/cutscene.cpp`,
`th03/cutscene/cutscene.cpp`, `th03/formats/script.hpp`, `planar.h`,
`th01/hardware/egcstart.cpp` and the original graphics/sound interfaces.
The owner specializes the actual TH05 branches and reuses the accepted
`resident.hpp` / `shared/abi.hpp` declarations without modifying them.

The source retains script loading, numeric/filename parsing, the full semantic
opcode switch, color-name mapping, two-page text/picture crossfades, Return-key
animation, input sensing and sound commands. It contains no ASM, emitted
instructions, fake zero objects, barriers or precomputed instruction tables.
Canonical files are UTF-8 and can use `source_encoding = "cp932"`. This TU has
no initialized DATA or Japanese string literals: its Japanese text comes from
the external loaded cutscene script. No script text or asset bytes are copied
into maintained source.

## Original decoded extent

Packed MAINE SHA-256:
`8308c416e756a07766f9f66dbf5575fa12c09189059226931a9562e7272b6997`.
Retained decoded payload SHA-256:
`4c5d12f7cfdcf45665c923c46203fc03ab56cd467513e3d19305b914e4e5bf2e`.
The complete reviewed contribution is **`[A695,B1B5)`**, **2848 bytes**.
These are decoded load-module offsets, not packed EXE file offsets.

| Complete function | Decoded span | Bytes |
| --- | --- | ---: |
| `cutscene_script_load(const char far*)` | `A695..A6D1` | 60 |
| `egc_start_copy()` | `A6D1..A705` | 52 |
| `pic_put_both_masked(int,int,int,int)` | `A705..A738` | 51 |
| `script_param_read_number_first(int far&)` | `A738..A7FE` | 198 |
| `script_param_read_number_second(int far&)` | `A7FE..A826` | 40 |
| `cursor_advance_and_animate()` | `A826..A866` | 64 |
| `box_1_to_0_masked(box_mask_t)` | `A866..A8EC` | 134 |
| `box_1_to_0_animate()` | `A8EC..A92B` | 63 |
| `box_wait_animate(int)` | `A92B..A9C3` | 152 |
| `script_op(unsigned char)` | `A9C3..AFD6` | 1555 |
| `cutscene_animate()` | `AFD6..B1B5` | 479 |

The original decodes as 940 instructions / **2768 instruction bytes** plus
**80 compiler sparse-switch bytes**, with **zero padding**. `script_op` ends
with 16 key words and 16 target words at `[AF96,AFD6)` (unit offset `901`, size
`40` hexadecimal); `cutscene_animate` ends with four keys/four targets at
`[B1A5,B1B5)` (offset `B10`, size `10`). Every table target and all local jump
targets are observed instruction starts. Tables remain part of full raw
comparison. There are 64 ordered original MZ segment fixups, each on a far-call
segment word; they must not be masked or reordered.

Private `.analysis/cutscene-boundary-review.json` records all original spans,
call sites, table keys/targets, fixups, globals and pointer immediates. Candidate
symbols only route the original review; no source-current exactness is claimed.

## ABI and context

Wrapper `th05/cutscene.cpp` includes `src/maine/cutscene/cutscene.cpp`.
The actual reference build rule uses `GAME=5`, `BINARY='E'` and standard
`-O -b- -3 -Z -d -ml`; the owner retains `-a2` at the original point.
The initial compiler segment is `CUTSCENE_TEXT`, group `group_01`, frame
**`0A54`** / base **`A540`**, contribution group offset **`0155`**. It contains
`cutscene_script_load` (60 bytes) and the inexact `egc_start_copy` (51 compiled
bytes, original 52). A distinct `CUTSCENE_AFTER_TEXT` holds the remaining nine
whole functions, expected 2736 bytes at original load `A705`.

The scaffold's independent `CUTSCENE_AFTER_TEXT` prefix is one uncredited ORG
byte at load `[A704,A705)`, after EGC's actual compiler RET. This byte is inside
the entire original EGC range, which remains unaccepted. It is outside every
compiler-owned function and never part of any accepted function extent. The
compiler contributes 2847 CODE bytes; the overall layout spans 2848 including
that hole. `CUTSCENE_TEXT` ends at `A704`, `CUTSCENE_AFTER_TEXT` starts at `A705`
and ends at `B1B5`; function comparisons must stop at each real contribution
end and must not extend EGC through the hole. Original DGROUP is
**`1011`**. All near calls are internal to this owner. The 37 distinct external
functions are genuinely far, including libc classification and file routines.

Original shared helpers use **`0E80`**, not calibration frame `0E7F`; their
original offsets are also **`0A` smaller** than calibration offsets. For example,
`pi_put_quarter_masked_8` is `0E80:066E`, frame delay `0E80:0A88`, and the EGC
rectangle copy `0E80:0C02`. Both frame and offset are taken from original call
operands. The symbol-only `probes/units/maine_cutscene_bindings.asm` supplies
only real external labels and holes outside complete compiler contributions.
It has no `.stack` directive and no helper bodies. A diagnostic may set its
`CUTSCENE_FIRST_SIZE` / `CUTSCENE_AFTER_SIZE` from the actual compiler OMF
before assembling the foreign tail. The current expected sizes are 111 and
2736. Together with the one uncredited inter-contribution byte they keep the
foreign tail at the original `B1B5`; no bytes are inserted inside functions.

The numeric parser's references retain the real large-model `int far&` ABI
(original `RET 4`); the box-mask enum retains its word domain (`RET 2`). The
VRAM pointer is the real four-byte `VRAM_PLANE_B`, not a replacement constant
segment. Screen points have both signed words, Shift-JIS characters retain
both bytes and the word view, the color map has all eight colors and all
8x3 two-byte keys, and masks have their actual four word rows.

## Owned runtime state and limits

This TU's initialized DATA contribution is zero. Its BSS candidate occupies
DGROUP **`[2E88,4F0E)`**, **8326 / `2086` hexadecimal bytes**: the complete
8192-byte script buffer, near script cursor, real unused TH05 far backup
pointer, flags, eight-entry color map, screen cursor, interval/color state and
numeric default. The original decoded file ends at `12E54`; this entire BSS
range begins at load `12F98`, beyond stored payload bytes. Its touched offsets
and final word are independently corroborated by operands; this is layout
information, not a stored-byte equality or authored-data acceptance claim.

The reference's unreferenced 60-byte `unused` state and one named `padding`
byte are retained as reference-correlated candidate declarations. Their exact
source type/ownership is **unresolved**; surrounding accessed positions alone
do not prove those declarations. They receive no reconstructed-byte credit.
The scaffold must not define any owner state a second time.

The reference's `outport2` instruction macro is replaced by the genuine
DX:AX word-OUT register protocol (`cutscene_egc_write`) in EGC initialization
and constant mask setup. The first two single-producer diagnostics showed
that all mask-helper bytes match after this natural register binding. The
EGC address-register zero still compiles as `XOR AX,AX` versus original
`MOV AX,0`, making that helper one byte shorter. No artificial zero object,
ASM or extra work is added to force this encoding, and the complete original
52-byte helper remains unaccepted. The first diagnostic also established that
`script_op`'s apparent extra byte was only table alignment after the preceding
shift: its 1491-byte instruction body was already byte-identical. Restored
placement must be checked again; no exactness is presumed. The BGM macro is specialized to
this cutscene's true stop-before-load path, removing an unreachable artificial
barrier without changing any reachable stop/load/play behavior.

## Single-producer scope review and planned replay

The initial single-producer cutscene diagnostic used one actual compiler invocation.
Its real MAP contributions are `CUTSCENE_TEXT` at `[A695,A704)` (111 bytes)
and `CUTSCENE_AFTER_TEXT` at `[A705,B1B5)` (2736 bytes). Nine complete functions
pass both full raw bytes and original ordered MZ fixups in this diagnostic:
script load, masked picture put, both numeric parsers, cursor advance, box
mask, box animation, box wait, and `cutscene_animate`. Their combined extent is
**1241 bytes**, comprising **1225 instruction bytes** and the complete **16-byte
compiler switch table** at the end of `cutscene_animate` (function offset 463).
No padding or inter-contribution hole belongs to these scopes.

`config/exact_units.maine.toml` registers those nine complete functions for a
focused two-cold-producer replay of this single shared translation unit. Each
scope uses its actual next public function as the end boundary; the final
`cutscene_animate` ends at the real contribution end. The scope before
`script_op` still ends at that unaccepted function's start, never skips it.
The configured natural negative control changes the unique
`((frame / 8) % RETURN_KEY_CELS)` to `((frame / 4) % RETURN_KEY_CELS)` in
`box_wait_animate`, changing the visible Return-key animation period. Only the
staged negative source receives this mutation. Its rejection must be measured
by that future replay; it is not inferred from the positive diagnostic.

The complete original 52-byte EGC helper remains unregistered because its
natural compiler output is 51 bytes. `script_op` now has all 1555 raw bytes
identical, including its full 64-byte sparse-switch table, but its ordered
fixup sequence differs after the contribution split. It remains unregistered.
Neither relocation order nor tables are masked, sorted or waived. The overall
2848-byte span remains declined because it contains EGC and its uncredited
hole. The single diagnostic grants no reconstruction acceptance, full
executable placement or packed-file reconstruction claim; the nine registered
scopes still require both fresh producers and a compiled rejected control.

## Accepted focused replay

`maine-cutscene-a` independently compiled the nine selected complete functions
in two fresh workspaces, then compiled the animation-period negative. All
1,241 bytes and original ordered fixups pass in both producers; the negative
changes the accepted box-wait function and is rejected. The 16-byte final
compiler switch table counts separately from 1,225 instruction bytes. The
EGC helper, dispatcher, inter-contribution hole and BSS receive no credit.

## Later complete EGC setup recovery

The older 51-byte EGC compiler diagnostic above is retained as evidence of
an inexact *combined* candidate. A separate maintained C++ hardware-register
owner now matches the entire 52-byte `A6D1..A705` routine; see
[exact EGC setup](egc_setup_exact.md). The original nine accepted functions
and their source inputs are unchanged. The 1,555-byte `script_op()` still has
unmatched original relocation ordering and earns no code credit.

## Complete original CODE segment and dispatcher acceptance

The remaining 1,555-byte `script_op(unsigned char)` now passes exact native
comparison, including the full 64-byte sparse-switch table and **42 original
ordered MZ relocation sites**. The original compiler contribution was not two
CODE segments: all eleven MAINE cutscene functions occupy **one 2,848-byte
`CUTSCENE_TEXT` segment** at decoded `A695..B1B5` in `group_01`. Reconstructing
that context also reproduces all **2,848 native bytes** and the original
**64-site relocation sequence**, with natural OMF LEDATA chunks of
1,024/1,024/800 bytes. Previously splitting out EGC caused a different
compiler buffer boundary and therefore a different relocation order, even
though the interpreter instructions themselves already matched.

The maintained one-segment wrapper `cutscene_joined.cpp` includes the same
canonical gameplay source. Two small compile-time choices preserve the old
nine-function split context: joined mode selects `CUTSCENE_TEXT` instead of
`CUTSCENE_AFTER_TEXT` and expresses the original EGC zero-word write through
semantic `MOV AX,0`. The color-map default (white, 15) is a genuine gameplay
constant and provides the new interpreter's compiled negative. No translated
opcodes, patched OMF, relocation sorting, foreign function bodies or copied
script strings are introduced.

Strict source-backed receipts:

- New `script_op` full function: `.analysis/unit-replays/gpt-web-maine-cutscene-script-op-unified-a/receipt.json`
- All nine existing split-context functions, revalidated after the common
  source change: `.analysis/unit-replays/gpt-web-maine-cutscene-split-after-join-a/receipt.json`

The independently accepted 52-byte EGC setup remains a distinct owner. The
three accepted scopes together cover all 2,848 original bytes: 1,241 from
nine functions, 52 from EGC, and 1,555 from the dispatcher. Existing original
16-byte `cutscene_animate` and 64-byte `script_op` CODE tables are included
in their complete function extents, never double-counted.

## Explicit TH05 cutscene command vocabulary and exact compiler tables

The complete **1,555-byte `script_op()` cutscene VM** now uses named constants
for all sixteen original ASCII script command bytes. They represent newline,
new text box, text color/color-map registration, text font weight, white fade
or wait, text-speed/page selection, palette tone, black fade/song fade,
shake or gaiji output, Return-key wait, page clear, image resource handling,
image quarter, BGM control, sound effect and script termination. Their original
values (`'n'`, `'s'`, `'c'`, `'b'`, `'w'`, `'v'`, `'t'`, `'f'`, `'g'`, `'k'`, `'@'`,
`'p'`, `'='`, `'m'`, `'e'`, `'$'`) remain untouched. Secondary arguments such
as `wi`/`wo`, `fm`, `vp`, `p=`, `p-` and color-map assignment are intentionally
handled within their existing command branches, not invented new opcodes.

The 16 sparse-switch keys are still compiled naturally by Borland into the
original 64-byte key/target switch table and retain their original jump and
relocation sites. All ten complete source owners affected through the shared
`cutscene.cpp` translation unit were replayed together (the VM plus script
loading, parser, cursor, masked rendering, box animation, waiting and the
479-byte cutscene animation controller). Their **2,796 total bounded bytes**
match both independent real Borland/TLINK producers and the original ordered
MZ relocations. The compiled change to the default text color was rejected as
a semantic negative. The focused receipt is
`.analysis/unit-replays/gpt-web-maine-cutscene-semantic-opcodes-20261111/receipt.json`.
No new original target code ownership, BSS or Japanese script assets are
claimed by this semantic source improvement. This was not a whole-MAINE replay.

## Original script subcommand and page protocol (2026-11-12)

The entire 1,555-byte `script_op()` interpreter and the adjacent
479-byte `cutscene_animate()` now use a maintained
[`subcommands.hpp`](subcommands.hpp) vocabulary for the **existing**
script-control bytes. This recovers the semantic difference between a
white fade (`wi`/`wo`), the `wm` music-measure wait, `wk` key marker,
black fade versus `fm` music fade, `vp` display-page selection,
`c=` glyph color mapping, `p=` palette-and-draw, `p@` draw with the current
palette, `p-` release, `pp` palette-only and `p,` filename loading.
The `=` quarter-image transition, `\` script-command escape and `@`
inline gaiji prefix are also distinct original parsing contexts; the
last one has separate sweat, heart, question and exclamation glyph forms.
Equal ASCII values are named differently where they mean different things.

The controller also names the real front (0) and background (1) page
arguments used by picture and text rendering. Its source still performs
the same graphics operations in the same order and retains every original
format quirk, unchecked script read, stack ABI and `goto colmap_add` path.
The default 64-frame wait, normal palette tone 100, music-fade default 1
and quarter-transition frame delay 1 are explicit protocol defaults.
These are genuine compile-time constants, not state variables or
optimizer barriers. No script asset data, undocumented opcode, resource
copy or instruction bytes are introduced.

The affected shared source is used by nine accepted cutscene functions
and by the **real single-segment 1,555-byte script interpreter** owner.
Every one was replayed in a bounded batch, using the original group_01
and SHARED frames and original relocation order, with two native compiler
producers and the preexisting compiled controls. The focused receipt at
`.analysis/unit-replays/gpt-web-maine-cutscene-subcommand-semantics-b/receipt.json`
reports all ten units exactly matched; in particular `script_op()`
reproduces its full 64-byte sparse switch table and 42 original ordered
relocations. The 479-byte scene animator's original 16-byte compiler
table also remains identical. This is semantic improvement to previously
owned CODE, not a duplicate 2,796-byte credit or a full MAINE replay.

## Original writable Shift-JIS byte-pair provider and consumer (2026-11-12)

The interpreter's existing `ShiftJISKanji` two-byte reference now
refers through a header-level `extern "C"` to the independently accepted
MAINE `_CUTSCENE_KANJI` C initializer at `[1086A,1086D)`. The original
script still writes two Shift-JIS glyph bytes in place, using the third
source-owned byte as the original NUL terminator. This removes a
function-local symbol declaration while keeping all source-visible
script behaviour, memory writes and the original parser's return ABI.

The shared-header closure was revalidated on **ten complete native
C++ cutscene units**, including the full 1,555-byte script opcode
interpreter and its 479-byte scene animation owner, at
`.analysis/unit-replays/gpt-web-maine-kanji-consumer-cpp-a/receipt.json`.
The six related source-reviewed EGC/PI ASM families were also
recompiled under their separate native-reviewed ASM lane; details
and receipts appear in `kanji_buffer.md`. No new CODE bytes were
counted and no full cold replay was executed.
