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
