# OP/MAINE: original Master-derived display and archive hooks

Ten complete original CODE procedures are now independently verified from
maintained assembler source and the real pinned native TASM objects: **1,624
previously unknown bytes**, 812 in each decoded executable. The two biggest
whole functions, `PFOPEN` (296 bytes in each) and `PFSTART` (160 bytes in each),
use TH05's original GAME=5 optimized archive-header code path.

| Complete source procedure | OP decoded extent | MAINE decoded extent | Bytes per target |
| --- | --- | --- | ---: |
| `BGM_STOP_SOUND` | `3590..35B0` | `3758..3778` | 32 |
| `GRAPH_GAIJI_PUTS` | `3674..371E` | `383C..38E6` | 170 |
| `GRAPH_GAIJI_PUTC` | `371E..37B8` | `38E6..3980` | 154 |
| `PFSTART` | `37B8..3858` | `3980..3A20` | 160 |
| `PFOPEN` | `39F0..3B18` | `3BB8..3CE0` | 296 |

The original Master 0.23 author archive independently identifies the source
ancestry: `B_SP_SND.ASM`, `GRPGPUTS.ASM`, `GRPGJPUT.ASM`, `PFINT21.ASM` and
`PFOPEN.ASM`. The sound routine's authored instruction source is equivalent
under the real TASM `NOPCALL` expansion. The text functions **are not claimed
to be verbatim**: the GAME≥4 port changes the original gaiji-coordinate
`ADC` to `ADD`. The archive functions are even more substantially adapted:
GAME=5 uses a preloaded archive header and 32-bit offsets. Their source and
foreign interface change is recorded explicitly, not normalized away. All
five complete functions remain Master-derived third-party code, **zero new
game-authored C++ or ASM credit**.

The independently retained `th05_op.asm` and `th05_maine_master.asm` TASM
objects are actual compiler/assembler producers. Their `_TEXT` LEDATA covers
every credited byte exactly once; the actual OMF FIXUPP actions are resolved
using the original `_TEXT`, DGROUP and `_BSS` MAP context. The complete raw
bytes match *both* calibration and original decoded OP/MAINE images, preserving
the original ordered MZ relocation stream. These ten scopes have 36 total
original OMF offset16 actions, and no original MZ segment relocation sites.
Each complete target extent is unique in its own decoded artifact. Nothing is
inferred from adjacent matches or stripped from the comparison.

The neighboring `GRAPH_PACK_PUT_8_NOCLIP` has unresolved original author
provenance; its raw match alone does not establish this Master source lane.
Likewise `PFEND` contains actual missing CODE LEDATA/runtimely written state
and is not counted as one source-written procedure. Those spans remain unknown
until their source extent and individual runtime slots can be reviewed.

The source/linked evidence is
[`config/context_master_hooks.json`](../../config/context_master_hooks.json),
with explicit adoption in
[`config/reviewed_context_master_hooks.json`](../../config/reviewed_context_master_hooks.json).
Run `python3 scripts/review_context_master_hooks.py --check` for the focused
native original/OMF/relocation checks. Public CI runs only the structural
source-identity/ledger check. A bounded tool-negative review rejected a
missing function, a clipped function, an invented relocation, altered author
provenance and false authored credit. No whole-game cold replay or accepted
unrelated C++ unit rebuilding was performed.
