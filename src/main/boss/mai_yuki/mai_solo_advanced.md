# Advanced Mai solo pattern candidates

Three complete callbacks cover original MAIN `190F7..1935E`,615 instruction
bytes and187 instructions. No compiler table, padding, initialized DATA or BSS
occurs. The original complete ordered relocation stream is `[567,295,120]`.

| Function | Original extent | Bytes | Ordered fixups |
|---|---|---:|---|
| `mai_solo_turning_fans` | `190F7..191A7` | 176 | `[120]` |
| `mai_solo_revenge_snow` | `191A7..19250` | 169 | `[119]` |
| `mai_solo_laser_bounce` | `19250..1935E` | 270 | `[222]` |

Turning fans alternate the real unsigned byte turn angle and gradually widen
it, with later movement between attacks. Revenge snow configures the complete
custom-ball template, emits rotating revenge balls and prepares the caller's
random bullet template before reversing its byte angle increment. Laser bounce
creates four fixed lasers around a random signed integer angular gap, then
emits mirrored bouncing stacks and prepares the caller's random bullets.
Template assignments whose emission occurs in the caller remain intact.

All callbacks use the actual near cdecl bool interface and full original return
paths. Frame arithmetic is signed16-bit; stored angles, state counters and
turn_by are unsigned bytes. Negative integral angle constants and negation
retain modulo256 behavior. The B4Ball revenge flag and HP remain real16-bit
fields. The third callback's ordinary signed16-bit local remains live across
four actual spawn calls and uses signed truncating division by2; no register
hints, hidden ABI or optimizer barriers are introduced.

The frozen Mai pattern, later-pattern, B4Ball and Laser headers supply complete
Boss24, BulletTemplate14, special unions, custom26/B4Ball26/template25 and
Laser24/32-slot types. All fields and enum values remain represented. Existing
headers and accepted source owners are unchanged. No target byte, instruction
array, asset payload, fake global or helper implementation is supplied.

Near code uses frame1527; sound is far C Pascal14AB:0232. The symbol-only binder
retains each foreign compiler segment in its real group. Its byte tail follows
the entire615-byte contribution at1935E, anchors the actual fixed-laser producer
at1A6EF and ends at209D0. It supplies no instructions, initialized values, stack
or inside-function holes.

ReC98 `th05_main.asm` lines15401..15637 supplies semantic evidence. A unique
native initialization sequence independently locates the original first entry,
rather than assuming the calibration label address. All three complete bodies,
returns, local branch destinations and ordered fixups were then checked against
pinned MAIN. Full instruction shapes agree with cached calibration at1C0E4,
1C194 and1C23D, a local displacement of `-2FED`. This is routing evidence,
not a source acceptance claim.

Private `.analysis/mai-solo-advanced-boundary-review.json` contains the whole
unit and three optional complete-function scopes. Scope entries and controls
are also in `.analysis/mai-solo-advanced-scopes.json`. The independent staged
negatives change fan speed3 to4, snow HP6 to5, or laser shrink age90 to91 in
their actual owner functions. Focused replay must check two fresh deterministic
producers, full raw bytes, original ordered fixups and compiled rejection.
No compiler was executed during preparation.

The initial frontend failed because the long common guard prefix suppressed
the required Mai-solo declarations. Short distinct guards resolve this real
header-composition issue without flags, ABI changes or instruction fillers.
The two accepted dependent owners were independently replayed and reaccepted.
`main-mai-solo-advanced-b` passes two fresh deterministic complete615-byte
raw/ordered producers and rejects its own real fan speed3→4 mutation. All
three complete functions and615 instruction bytes are accepted, without
DATA, BSS, padding or table credit.
