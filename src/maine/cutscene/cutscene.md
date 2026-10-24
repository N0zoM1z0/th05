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

The retained `.analysis/compiler-probes/maine-cutscene-d/receipt.json`, produced
by `.analysis/diagnose_cutscene_d.py`, contains one actual compiler invocation.
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
