# MAIN stage-zero song and initial CG/BB far-pointer bank

The original MAIN `[20A72,20A7A)` contains two natural four-byte
source-initialized far pointers, with original ordered segment fixups
`[6,2]`: an originally anonymous pointer to the stage-zero `ST00`
song/stage basename, followed by the actual public `_bbname` to
`BB0.CDG`. Their genuine foreign resource providers are the independently
accepted `main_resource_files.stage_bgm_base` (field offset 20 in the
347-byte resource bank) and `main_session_files.bomb_background` (field
offset 22 in the 66-byte session bank). The C owner names
`stage_zero_song_name` and `bbname` and takes **source-level field
addresses**, not hardcoded near offsets or original pointer bytes.

`bbname` retains its real independently addressable C public symbol and
is used by the accepted EMS/resource loading code. The actual original
DS object is `209D:00A6` and the anonymous song pointer begins at
`209D:00A2`. The preceding unknown zero word `[20A70,20A72)` and the
other already accepted `eyename` pointer do not belong to this
compiler contribution. The compiler enforces both natural far-pointer
widths and the total eight-byte DATA scope. The binder defines only
the two outside provider publics, at their original downstream DGROUP
coordinates; it contributes no resource filename bytes, pointer words,
or fake relocation records.

The final focused receipt
`.analysis/unit-replays/gpt-web-main-startup-links-b/receipt.json`
passes two native Borland C producers, full raw/OMF/MAP DATA and literal
ordered MZ fixups. The compiled negative changes the source song field
to the genuine other file field `op_fn`, which produces a different
actual linked far address and is rejected. The source is linked only
as a bounded contribution; original whole-object TU identity is not
assumed. No full cold replay was run.

## Actual far-pointer mutability and consumer closure (2026-11-12)

The two source-initialized pointers are now both `char far *near` rather
than pointers to `const char`. In particular, the canonical public
`bbname` must point to writable `BB0.CDG` storage because the real
EMS playchar loader performs `bbname[2] = '0' + playchar` before loading
the background. The stage-zero `ST00` base remains writable in its
separately accepted resource bank as well. The corresponding
`MainSessionFiles.bomb_background` source field has been corrected to
`char[8]`, retaining its genuine offset and whole original initializer.

The new provider and 8-byte pointer owner both pass two independent
native Borland C rounds with full original raw bytes, unchanged ordered
MZ fixups `[6,2]`, and their own compiled semantic negatives:
`.analysis/unit-replays/gpt-web-session-bb-mutable-a/receipt.json`
and `.analysis/unit-replays/gpt-web-startup-links-mutable-a/receipt.json`.
The three actual dependent EMS CODE functions (155-byte allocation,
267-byte playchar preload and 108-byte eyecatch) were also selectively
recompiled twice with their original bytes, fixups and compiled control
rejected, receipt
`.analysis/unit-replays/gpt-web-ems-mutable-resource-consumers-a/receipt.json`.
No whole-program acceptance, new CODE credit or cold replay is implied.
