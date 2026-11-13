# Mai/Yuki shared and solo Boss scratch lifetimes

The paired fight and both survivor controllers reinterpret the same original
16-byte `boss_statebyte` array. `MaiYukiPatternScratch`, `MaiSoloScratch` and
`YukiSoloScratch` are three views of that storage; none allocates independent
state. Compile-time size and offset assertions keep every view tied to the
original byte coordinates.

## Paired ring state at offsets 12..15

The late paired `mai_pattern_reversing_rings()` and
`yuki_pattern_reversing_rings()` callbacks use the final four bytes as two
character-specific angle/step pairs:

| Offset | Paired-fight role | Initialization and use |
| ---: | --- | --- |
| 12 | Mai reversing-ring step | `MYR_RING_MAI_STEP`; added to Mai's angle, then negated at the turn boundary |
| 13 | Yuki reversing-ring step | `MYR_RING_YUKI_STEP`; added to Yuki's angle, then negated at its turn boundary |
| 14 | Yuki reversing-ring angle | initialized to `MYR_RING_YUKI_ANGLE`, then advanced with the Yuki step and original random jitter |
| 15 | Mai reversing-ring angle | initialized to `MYR_RING_MAI_ANGLE`, advanced by the Mai step, then adjusted by the original random turn jitter |

The two callbacks retain their original independent clocks and turn gates.
No new shared angle counter or phase-transition reset is introduced.

## Sequential roles of byte 10 in Mai's solo fight

`MaiSoloPatternByte10` is the actual one-byte union at physical offset 10.
Its two roles do not overlap in time:

| Lifetime | Member | Owner and behavior |
| --- | --- | --- |
| Laser cycle (phase 5) | `laser_patterns_seen` | Reset to zero when the radial laser array is created; selects `mai_solo_laser_patterns[count % 3]` at each 256-frame cycle boundary, then increments |
| Final revenge snow (phase 9) | `revenge_snow_angle` | The final-approach transition overwrites byte 10 with the initial snow angle; `mai_solo_revenge_snow()` advances it by the signed step in byte 11 and resets it at the turn boundary |

The phase-8 final approach is the lifetime boundary: it initializes the
revenge-snow angle and step after the phase-5 laser counter is no longer used.
No explicit clearing or second counter is introduced. The union preserves the
same byte 10 and the existing step at byte 11; `MaiSoloScratch` remains exactly
16 bytes, with all following fields at offsets 12..15 unchanged.

The laser-cycle callback now reads and increments
`mai_solo_scratch.pattern_byte10.laser_patterns_seen`, while the final-approach
initializer and revenge-snow callback use
`mai_solo_scratch.pattern_byte10.revenge_snow_angle`. This removes the lone raw
`boss_statebyte[10]` alias from the Mai solo laser implementation and records
the real cross-phase lifetime.

The focused ten-unit replay includes the complete **1,018-byte** paired Boss
controller, **786-byte** Mai solo controller, **461-byte** laser cycle and
**615-byte** advanced pattern, plus the six affected neighboring pattern and
Yuki owners. Two native Borland/TLINK producers preserve all original raw
bytes and ordered fixups; the compiled negative is rejected. Receipt:
`.analysis/unit-replays/gpt-web-mai-solo-byte10-lifetime-20261113b/receipt.json`.
No duplicate CODE ownership is added.

## Sequential roles of byte 15

`MaiYukiPatternByte15` names five mutually exclusive uses of the same final
Boss scratch byte:

- `mai_paired_sweeping_pellet_angle`: the paired opening's Mai pellet sweep,
  initialized to unsigned `-0x10` at frame 48 and advanced by five per volley.
- `mai_solo_turning_stack_angle`: Mai's solo turning stacks, initialized to
  `0x60` and advanced by nine on each volley.
- `mai_solo_laser_direction`: Mai's solo laser cycle, initialized to one and
  negated at its original frame-180 direction change. The separate pattern
  count remains at byte 10.
- `mai_shared_reversing_ring_angle`: Mai's paired reversing-ring angle at
  offset 15, paired with its step at offset 12.
- `yuki_solo_snow_angle`: Yuki's final solo snow-cross angle, initialized by
  the final-approach transition and consumed by the existing snow pattern.

The remaining Yuki snow state is still distinct: snow step is byte 13 and
snow-angle step is byte 14. Mai's byte-10 laser counter/revenge angle share
their own one-byte union, the revenge-snow step remains byte 11, and the
laser-bounce angle remains byte 13. The overlay does not conflate these other
physical members or imply that a value survives an attack that explicitly
reinitializes it.

The source views now use named union members for all byte-15 accesses and
named fields for the paired angle/step pair at offsets 12..14. The original
arithmetic, initializers, branch clocks, and write order are unchanged. The
focused `gpt-web-mai-yuki-scratch-byte15-final-20261113` replay passed ten
complete affected units in two deterministic Borland/TLINK producers,
including the 1,018-byte shared Boss controller and both complete solo
controllers. All original raw bytes and ordered fixups match; the existing
compiled negative is rejected. No previously accepted CODE extent is credited
again. See the replay receipt in the ignored `.analysis/unit-replays` store.
