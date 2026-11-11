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
