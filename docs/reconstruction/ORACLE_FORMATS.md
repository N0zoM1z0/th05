# Special replay formats

This is a tool index for occasional DATA, ASM and retained-producer work.
It adds no steps to ordinary C/C++ recovery; use only the relevant entry.
The [exact contract](../ORACLES.md) and [workflow](../RE_WORKFLOW.md) define the
normal process. Detailed receipt fields live in the corresponding scripts.

| Work | Tool / reference |
| --- | --- |
| New/affected C/C++ CODE or initialized DATA | `scripts/replay_units.py` |
| Merge one or several receipts atomically | `scripts/progress.py --accept PATH` (repeat for a batch) |
| Reuse whole initialized DATA from two saved CODE producers | `scripts/review_saved_data.py` |
| Project complete functions from a saved mixed-result receipt | `scripts/review_saved_scopes.py` |
| Optional additional compiled control for an existing owner | `scripts/supplement_negative.py` |
| Reviewed assembly families | `scripts/replay_asm_family.py` |
| Text renderer CODE / DATA | `scripts/replay_text_fx_render.py` / `scripts/replay_text_fx_data.py` |
| Original text-renderer ASM ownership | [Text FX review](TEXT_FX_ASM_OWNERSHIP.md) |
| Enemy VM ASM | `scripts/replay_enemy_vm.py`, [source notes](../../src/main/enemy/script.md) |
| ZUN memory child | `scripts/replay_zun_memory.py` |
| Vendor/library scopes | `scripts/review_vendor.py`, `scripts/review_master.py` and family-specific reviewers |
| Font bitmap resource classification | [Font resource](ZUN_FONT_RESOURCE.md) |

C/C++ manifests select an artifact and the real compiler binary context. OP and
MAINE receipts use the pinned decoded image and ordered relocation stream;
they do not rebuild the packed container. A genuine `bindings_after_compiler`
entry preserves the actual before/compiler/after object order.

Function scopes use actual MAP function publics. Initialized semantic DATA uses
one complete compiler DATA contribution and an explicit semantic role; C DATA
has a C source/wrapper. CODE tables, BSS and raster assets are separate.

CP932 inputs retain UTF8 maintained snapshots and record the transcoded compiler
bytes. Generated inputs name their generator and output. These identify actual
producer inputs; they are not separate behavior-test obligations.

Saved-producer lanes retain their original verdicts and input identities.
Subset import does not turn an aggregate failure into a success. Re-reading a
saved producer is not a fresh compilation. Import checks the actual saved
OMF/MAP/MZ and source closure through the relevant reader.

ASM ownership is a separate reviewed decision; exact assembly output alone
cannot relabel compiler-generated code or assets. Padding and runtime-patched
placeholders are compared with zero authored credit. Semantic dispatch/coordinate
tables remain distinct from instructions and resources.

Supplemental per-function negatives and CPU behavior models are optional
investigations. Do not add them just because an extra tool or format exists.
