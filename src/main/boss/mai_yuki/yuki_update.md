# Complete Yuki solo update candidate

The complete C far Pascal callback `YUKI_UPDATE` covers original MAIN
`18A05..18D3F`,826 bytes. Its228 instructions occupy806 bytes and contain
two genuine RETF exits. The final20 bytes are the complete10-entry compiler
switch table, with no alignment byte. All table destinations and direct local
branches land on original instruction starts. Ordered fixups are `[256,140]`.

The state machine fills HP, reveals Yuki, initializes custom bullets, approaches
waypoints, cycles through real near callbacks, advances HP thresholds and
performs defeat cleanup. The default defeat path returns before custom-bullet
and HUD updates, preserving the second full return path. The phase counter's
byte promotion to signed16-bit modulo5 and the explicit minus8 byte state
initialization retain their actual widths and semantics.

The frozen `b4ball.hpp` provides the complete canonical custom26/B4Ball26 and
B4BallTemplate25 storage, including real unused fields and bool16 revenge.
The owner writes only the real origin and tiny-pattern-base216 template fields.
Both Boss records remain the complete24-byte canonical type; the second record
at DS5AD2 is used as the real waypoint storage. The complete canonical16-bit
explosion enum is reused without importing generic.hpp, whose broader constant
names conflict with the frozen Mai/Yuki macros. No accepted header is edited.

The existing two2-entry and one5-entry pattern-selector tables at DS1964,
1968 and196C are declared semantically without defining their pointer entries.
No initialized DATA, BSS, asset, instruction array or helper body is supplied.
The accepted shared callback pointer remains at DS4438.

Near game code uses frame1527. BG rendering, B4Ball rendering and the null
callback belong to main01/AE1; the growing circle is far Pascal AE1:347A.
Sound is far C Pascal14AB:0232. Custom-ball reset/update are the actual C near
Pascal entries at183D5 and18459. The update's original C Pascal linkage agrees
with the independent shared Mai/Yuki caller. DS is209D. The symbol-only binder
places all foreign segments in their actual groups, follows the full826-byte
contribution with an outside byte tail, and ends it at209D0. It defines no
instructions, initialized values, stack or hole within compiled functions.

ReC98 `th05_main.asm` lines14675..14976 supplies semantic evidence. The native
prologue and complete point-initialization sequence uniquely locate the actual
original callback. All228 complete instruction shapes then agree with cached
calibration at1B9F2, a local displacement of `-2FED`. Routing evidence and source
presence remain separate from source acceptance.

Private `.analysis/yuki-update-boundary-review.json` contains the whole-unit
proposal, complete table metadata and a unique staged negative changing
end-HP4600 to4500. Two fresh focused producers, full826-byte comparison,
original ordered fixups and compiled rejection remain required. This packet
was prepared with native/static tools only and executes no compiler.

`main-yuki-update-c` passes two fresh deterministic complete826-byte raw
comparisons and original ordered fixups[256,140]. The actual phase threshold
4600→4500 control is compiled and rejected for this whole callback. Authored
credit is826 bytes (806 instructions plus20 semantic switch-table bytes),
one complete function, with no padding, DATA or BSS. All table bytes and
both complete RETF paths remain in the verified extent.

Source integration now uses `boss_solo_pattern_current` for the genuine
DS4438 callback slot shared by both survivor states. This is distinct from
the shared-fight Yuki callback at4430 and the internal Mai void callback
at443A. Only this826-byte accepted owner required replay for that rename;
its final c receipt preserves the complete original raw bytes and fixups.
