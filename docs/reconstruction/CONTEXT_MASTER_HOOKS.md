# OP/MAINE: original Master-derived display and archive hooks

Ten complete procedures and two additional source-written parts of each
original `PFEND` routine are independently verified against actual native
TASM objects: **2,436 previously unknown CODE bytes**, 1,218 in each decoded
executable. The complete `PFEND` function spans 408 bytes per target, but
only 406 bytes per target are physically emitted by source LEDATA. The
remaining two bytes per target are runtime-writable and stay unknown. The
full `PFOPEN` (296 bytes per target) and `PFSTART` (160 bytes per target)
use TH05's original GAME=5 optimized archive-header path.

| Complete source procedure | OP decoded extent | MAINE decoded extent | Bytes per target |
| --- | --- | --- | ---: |
| `BGM_STOP_SOUND` | `3590..35B0` | `3758..3778` | 32 |
| `GRAPH_GAIJI_PUTS` | `3674..371E` | `383C..38E6` | 170 |
| `GRAPH_GAIJI_PUTC` | `371E..37B8` | `38E6..3980` | 154 |
| `PFSTART` | `37B8..3858` | `3980..3A20` | 160 |
| `PFOPEN` | `39F0..3B18` | `3BB8..3CE0` | 296 |
| `PFEND` source head | `3858..38F4` | `3A20..3ABC` | 156 |
| `PFEND` runtime slot (*unknown*) | `38F4..38F6` | `3ABC..3ABE` | 0 credited (2 physical) |
| `PFEND` source tail | `38F6..39F0` | `3ABE..3BB8` | 250 |

The original Master 0.23 author archive independently identifies the source
ancestry: `B_SP_SND.ASM`, `GRPGPUTS.ASM`, `GRPGJPUT.ASM`, `PFINT21.ASM` and
`PFOPEN.ASM`. The sound routine's authored instruction source is equivalent
under the real TASM `NOPCALL` expansion. The text functions **are not claimed
to be verbatim**: the GAME≥4 port changes the original gaiji-coordinate
`ADC` to `ADD`. The archive functions are even more substantially adapted:
GAME=5 uses a preloaded archive header and 32-bit offsets. Their source and
foreign interface change is recorded explicitly, not normalized away. All
five complete functions and PFEND's source-written ranges remain
Master-derived third-party code, **zero new game-authored C++ or ASM credit**.

The independently retained `th05_op.asm` and `th05_maine_master.asm` TASM
objects are actual compiler/assembler producers. Their `_TEXT` LEDATA covers
every credited byte exactly once; the actual OMF FIXUPP actions are resolved
using the original `_TEXT`, DGROUP and `_BSS` MAP context. The complete raw
bytes match *both* calibration and original decoded OP/MAINE images, preserving
the original ordered MZ relocation stream. The ten original complete-function scopes have 36 total OMF fixup actions;
the two `PFEND` procedures add 84 more across their four source-written
intervals, for 120 actions in all. Each `PFEND` source head has one original
segment relocation at relative +75; the real ordered MZ relocation sites are
compared, not sorted or masked. Each adopted byte interval is unique in its
decoded original artifact. Nothing is inferred from adjacent matches or
stripped from the comparison.

The neighboring `GRAPH_PACK_PUT_8_NOCLIP` has unresolved original author
provenance; its raw match alone does not establish this Master source lane.
The full `PFEND` procedures have separately proven native PUBLIC start/end
boundaries (`3858..39F0` OP, `3A20..3BB8` MAINE). Their exact ordinary CODE
LEDATA covers relative `[0,156)` and `[158,408)` once each, but **does not
write `[156,158)`**. Those two bytes are zero in both original and calibration,
and have no source LEDATA. They remain unowned, not classified as instructions,
not padded, and not filled in by comparing adjacent bytes. The 406 written
bytes per function are adopted under two explicitly separate source roles.
The neighboring `GRAPH_PACK_PUT_8_NOCLIP` is now separately classified as
[Master/ZUN-derived CODE](CONTEXT_GRAPH_PACK_NOCLIP.md), with an exact source
transformation from the original upstream Master procedure. Its two independent
196-byte scopes are not included or double-counted in this hook proof.

The source/linked evidence is
[`config/context_master_hooks.json`](../../config/context_master_hooks.json),
with explicit adoption in
[`config/reviewed_context_master_hooks.json`](../../config/reviewed_context_master_hooks.json).
Run `python3 scripts/review_context_master_hooks.py --check` for the focused
native original/OMF/relocation checks. Public CI runs only the structural
source-identity/ledger check. Bounded proof negatives reject missing/clipped functions, an invented
relocation, altered author provenance, modified runtime slot limits, and false
authored credit. No whole-game cold replay or accepted
unrelated C++ unit rebuilding was performed.

## Complete BFNT entry and header procedures in both front ends

Four further complete native Master procedures are now attributable in **each**
OP and MAINE executable, totaling **964 new source-written CODE bytes**:
`BFTENTRY_INVAL` (`0272..0286`, 20 bytes), `BFNT_ENTRY_PAT` (`0286..03B4`,
302 bytes), `BFNT_HEADER_READ` (`03B4..03F0`, 60 bytes), and
`BFNT_EXTEND_HEADER_ANALYSIS` (`03F0..0454`, 100 bytes).

The original Master `BFTENTRY.ASM` is independently correlated to the retained
TASM source by the two actual conditional-branch expansions and private-label
renames already reviewed for MAIN. The original `BFNTHDRR.ASM` and
`BFTHDRAN.ASM` blocks match their retained native sources exactly under
whitespace normalization. `BFTENTRY_INVAL` has no exported MAP public: its
20-byte extent ends precisely at the genuine `BFNT_ENTRY_PAT` public. Every
complete CODE extent, actual OMF fixup and ordered original MZ relocation
matches both original and calibration images. The preceding startup region
`0000..0272` stays outside these claims.

This review extends the existing focused Master-hook source proof and decision,
without introducing a separate verification framework. All eight original
functions remain third-party code, with no new game-authored credit.

## Original buffering, DOS and EGC helpers

A further twelve whole Master 0.23 functions per executable now have exact
source-backed ownership, totaling **908 newly attributed bytes** (454 each):
`BCLOSER` (24), `BFILL` (60), `BGETC` (48), `BSEEK` (66), `BSEEK_` (48),
`DOS_AXDX` (24), `DOS_READ` (26), `DOS_SEEK` (28), `DOS_SETVECT` (32),
`EGC_ON` (22), `EGC_OFF` (32), and `EGC_END` (44). The native OP/MAINE DOS
routine addresses differ after the front-end-specific file utilities; their
original positions, not assumed constant offsets, are in the evidence ledger.

All twelve complete original author ASM source blocks match the retained
actual native TASM bodies without semantic rewriting. Their whole CODE
intervals occur uniquely at the recorded original positions; both native
OMFs and original MZ images match. These 24 source scopes contain no OMF or
MZ relocations. They extend the existing bounded Master-hook review and earn
only vendor CODE ownership, not additional game-authored C++ credit.

## Early palette, file and packed-graphics functions

Another 34 complete Master 0.23 source procedures, occupying **1,736
previously unknown CODE bytes**, now match the original decoded OP and
MAINE images. This review covers sixteen functions in OP (776 bytes) and
eighteen in MAINE (960 bytes). The largest new functions are `BOPENR`
(84 bytes each), `FILE_APPEND` (84 bytes each), and MAINE's
`GRCG_CIRCLEFILL` (150 bytes). It also covers palette fades, buffered
reads, file creation/open/seek/existence, selected DOS services and the
original packed GRCG color setter.

The original Master archive and actual retained TASM inputs are compared
**whole procedure by whole procedure**. Some procedures are text-identical.
The others have a narrowly reviewed source spelling: native `NOPCALL`
for a source-equivalent relocated call, explicit `word ptr` arguments,
`IF LDATA`-guarded far-pointer pushes, typed file-error and font-color
fields. Every such change is specified by a fixed original-source line and
checked at its expected occurrence count. The native body must match all
remaining original lines, and its actual OMF LEDATA, ordered FIXUPP actions,
full original target bytes and MZ relocations must agree. The original
Master `PALETTE_BLACK_IN`/`OUT` archive has two platform-specific definitions;
the reviewed PC-98 source is its first complete branch, rather than a blend
of both alternatives.

The existing proof at
[`config/context_master_hooks.json`](../../config/context_master_hooks.json)
and explicit adoption now cover these regions without a new oracle family.
All 1,736 bytes are third-party Master code, not new game-authored source.

## Packed-file I/O and random functions

OP and MAINE now also own nine complete original archive I/O functions each,
**398 bytes per executable / 796 bytes total**: `PFCLOSE` (26), `PFGETC`
(16), `PFGETC1` (78), `PFGETX0` (68), `PFGETX1` (14), `PFREAD` (46),
`PFREWIND` (60), `PFSEEK` (48), and `IRAND` (42). The native TASM OMF
contains full CODE LEDATA for every range. There are five actual offset
FIXUPP actions in the `IRAND` owner per executable; complete native and
original MZ bytes and ordered relocations agree.

All source bodies besides two are identical to the original Master author
archive under normalized whitespace. `PFCLOSE` adds an explicit `word ptr`
qualification to the original near stack argument. In TH05's `PFGETX1`, the
original Master `ROR AL,4` after the archive-key XOR has been **removed**.
This changes the nibble decoding operation; the native source is checked as a
specific GAME=5 adaptation, not described as an equivalent original function.
No other branch, call or instruction is removed in the accepted source
comparison. The 18 whole-function bounds, source/OMF fixup counts and original
image bytes are kept in the existing Master-hook evidence.

## Original OP residency-palette and large masked trapezoid functions

Four more **complete functions**, totaling **436 originally unknown CODE
bytes**, are now source-backed in OP: `RESPAL_EXIST` (`2ADC..2B18`, 60 B),
`RESPAL_CREATE` (`2B18..2B8E`, 118 B), `RESPAL_FREE` (`2B8E..2BAC`, 30 B),
and `draw_trapezoid` (`2BD6..2CBA`, **228 B**). The trapezoid rasterizer is
the original `KOIZOID.ASM` procedure, including the self-modifying drawing
registers and full horizontal clipping/masking; the native GAME>=3 branch
uses `trapezoid_hmask` in place of the original solid-plane word. The
reviewed source transformation permits only explicit private-field/label
renames and the actual `IF GAME GE 3` horizontal-mask branch. No opcode,
address, register or CODE bytes are copied from the target to source.

The three other procedures derive from the original `RSPEXIST.ASM` and
`RSPFREE.ASM`. `REP CMPSB` uses its equivalent native `REPE CMPSB` spelling
in the existence check, private labels have explicit namespace prefixes,
and CREATE/FREE contain the genuine native `IF GAME GE 2; NOP; ENDIF` around
the original call site. This NOP belongs to the **retained existing native
TASM source** and matches the target under the actual linker; it is neither
invented padding nor newly authored game logic. All source/procedure
comparisons are complete and every transformed original line is constrained.

The original complete bounds are supplied by MAP publics. The actual TASM
OMF records 2, 2, 2 and **26 ordered fixup actions** respectively; they and
all 436 native bytes match the original OP decoded MZ. These four scopes are
unique in the original target. The two neighboring GAME-specific joystick
functions `JS_START` (`2BAC..2BD6`, 42 B) and `JS_SENSE` (`2CBA..2CD0`,
22 B) **remain unknown**: their source differs more substantially from the
published original Master platform handlers. This review does not claim
either complete joystick function, any mutable DATA or new game-authored
C++/ASM credit. The shared evidence/decision now encompass **102 source
scopes / 7,276 third-party CODE bytes** in OP and MAINE combined.
