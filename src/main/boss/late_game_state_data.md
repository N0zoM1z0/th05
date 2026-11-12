# MAIN three original late-game public state objects, not a zero buffer

The original MAIN near DATA between Shinki's one-byte float-direction
latch and the separately corrected Stage Clear counters is not an
opaque 9-byte zero array. Three distinct native C/C++ consumers
identify **three meaningful initialized C state objects** with their
true DGROUP offsets and types:

| Decoded physical interval | DGROUP address | Original C public and purpose | Bytes |
| --- | --- | --- | ---: |
| `[2242C,2242D)` | `209D:1A5C` | `bullet_zap_drop_point_items`, actual 1-byte bool governing bullet-zap point-item drops | 1 |
| `[2242E,22430)` | `209D:1A5E` | `hud_hp_bar_value_prev`, signed 16-bit previous HUD HP bar value | 2 |
| `[22430,22431)` | `209D:1A60` | `midboss_defeat_angle`, 8-bit rotating defeat effect angle | 1 |

The **1619-byte five-function** original `bullet_update()` native
binding independently exposes the first address. Its actual bullet-zap
loop checks the flag and the quarter-period index before converting
bullets to point items; the EX-Alice Boss phase source also sets and
clears it around its late fight. This one-byte state has no invented
static C++ bool object in the original runtime.

The accepted **88-byte `hud_hp_update_and_render()`** and the original
midboss life-cycle both read and write the signed two-byte
`hud_hp_bar_value_prev`, smoothing the displayed HP bar toward its
current scaled value. The separately accepted complete **170-byte
`midboss_defeat_render()`** spins the one-byte
`midboss_defeat_angle` by its native angular step, drawing the
original 16-part radial defeat effect. These objects do not share a
C source type or a runtime storage aggregate.

Each natural C initializer exports the actual original near public
using an asserted native **1-, 2-, or 1-byte** type and an ordinary
zero initializer. Each isolated binder preserves only the authentic
MAIN CODE group frames and the external DGROUP prefix, supplying no
candidate bytes, instructions, switch tables or spoofed fixups.
The original zero-filled alignment cells `[2242B,2242C)`,
`[2242D,2242E)` and `[22431,22432)` remain **unowned**.
The following independently accepted two-byte Stage Clear previous
Miss/Bomb counters start at `[22432,22434)`, not at the unrelated
large-explosion frame at `[222B4,222B6)`.

All three initialized-DATA owners independently passed **two pinned
Borland C/TLINK producers**, complete byte equality, OMF/LEDATA/MAP
contribution equality, the original empty ordered MZ relocation
stream and **their own compiled initializer mutation** zero→one:

- `.analysis/unit-replays/gpt-web-main-bullet-zap-native-data-a/receipt.json`
- `.analysis/unit-replays/gpt-web-main-hud-hp-bar-native-data-a/receipt.json`
- `.analysis/unit-replays/gpt-web-main-midboss-defeat-angle-native-data-a/receipt.json`

These are four *new* source-owned initialized DATA bytes. Source-current
C/C++ consumers, including the complete EX-Alice Boss, are validated
separately before any cross-source ABI claim. No whole-game cold replay
or new CODE credit was involved.
