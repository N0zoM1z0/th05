# TH05 common player shot control candidate

This owner follows natural ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05/p_common.cpp`. It reuses the existing canonical `reimu.hpp` Shot/entity enum, near-pointer API, SPPoint return type, random-range inline implementation and genuine SC bitflags. Shared headers are unchanged. The source retains the reference `-a2` pragma after its include and introduces no instruction bodies, barriers or extra variants.

The old183-byte calibration no-match was not used as a boundary proof. Independently following the accepted character owners' calls identifies original `shot_cycle_init` at load`0xE644`; its two direct callers immediately precede Reimu's original first owner at`0xE6FB`:

| Complete function | Original start | Size | Extent detail |
|---|---:|---:|---|
| `shot_cycle_init()` | `0xE644` | 114 | 81 instruction bytes, one zero alignment byte,32-byte switch table |
| `shot_l0()` | `0xE6B6` | 27 | Complete instructions |
| `shot_l1()` | `0xE6D1` | 42 | Complete instructions |

The complete TU is `[0xE644,0xE6FB)`,183 bytes:150 instructions bytes,32 compiler switch-table bytes and1 explicitly classified zero padding byte. The dispatch at`0xE65D` is `jmp word ptr cs:[bx+0x3886]`, indexes shot times3 through18, and reaches16 real near targets in the same function. The table is `[0xE696,0xE6B6)`; all entries were checked against original instruction starts. Padding at`0xE695` is compiler zero, not NOP. It remains in raw comparison. Authored-code classification would therefore be182 and instruction classification150 only after strict producer acceptance.

There is one original ordered MZ fixup, relative51 (`0xE677`), for the sound call at true frame`14AB:0232`. Original MAIN01 frame is`0xAE1`, unit offset`0x3834`; DGROUP frame is`0x209D`. Actual near helpers are `randring1_next16_and` at`0xC70E`, `shots_add` at`0xE38C` and `shot_velocity_set` at`0xE3C4`. `shot_velocity_set` receives the actual canonical near SPPoint pointer and returns the real SPPoint ABI, including the original helper's access back into its containing Shot.

Globals are foreign: unsigned-byte `shot_time` at DS`0x36F2`, near `shot_ptr` at`0x4200`, char `shot_last_id` at`0x4202`, and64 canonical18-byte Shot records beginning`0xBA8E`. No initialized DATA or BSS is defined here.

`player_common_bindings.asm` supplies only genuine helper/global labels and outside-unit ORG context. The true shared sound frame splits the CODE gaps; every ORG value was checked below65536, with no stack or payload bytes. It does not materialize the switch table or padding: those must come from the C++ compiler.

Private review: `.analysis/player-common-boundary-review.json`. Proposed entry and one meaningful source negative: `.analysis/player-common-candidate.json`. The negative removes the once-per-cycle SC_1X bit only from the unique shot-time18 initializer. This preparation ran no compiler and makes no exact/acceptance claim.

`main-player-shot-common-a` passes two independent fresh producers, all183
raw bytes and the original ordered fixup. Its compiled18-frame shot-cycle
mutation is rejected. The one zero padding byte is compared and excluded;
32 compiler-generated switch-table bytes remain separate from150 instruction
bytes. No DATA/BSS or foreign helper body is credited.
