# Original 108-byte HitShot creation

`hitshot_from(Shot near*)` at MAIN `[13617,13683)` invalidates the shot and
converts its position and braked velocity into one of 24 circular hit-animation
slots. The authentic 16-bit near-Pascal routine and record layout survive in
`_reference/ReC98/th05/main/player/hitshot_from.asm`.

The maintained register-level `hitshot_from.asm` uses a 14-byte HitShot,
next-free index at DS:C64A, hit-animation array at DS:BF56, and the genuine
Shot pointer from SS:BP+4. It marks the Shot removed, leaves occupied hit slots
unchanged, selects pattern 28 or 32 and copies 32-bit current/previous
positions. Signed 16-bit X and Y velocities are divided by six separately,
with an original `RET 2`. It creates no DATA or BSS and adds no guard or
modified behavior.

The original function has 108 instruction bytes and no relocation sites or
padding. The complete native review pins its 40 decoded instructions; the
source-free binder supplies only the true `main_01` CS `0AE1`, DGROUP DS
`209D` and original foreign storage. Both independent TASM32/TLINK producers
match all **108/108 bytes**, and changing the signed velocity divisor from
6 to 5 is compiled and rejected. No adjacent renderer or collision code is
recounted. Focused receipt:
`.analysis/gpt-web-hitshot-from-asm-a/receipt.json`.
