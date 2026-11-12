# MAINE Staff roll's six independent source-initialized state groups

The original decoded MAINE near DATA interval `[1184A,1185C)` contains
**six separately addressable, source-meaningful C state contributions**
that together account for 15 of its 18 bytes. The remaining **three
single-byte original alignment gaps are not credited**. The actual
native compiler/ASM public map is in
`probes/units/maine_staff_complete_context_bindings.asm`, which was
established independently of these new C initializer declarations.
The state groups are used by the existing source-defined 13-function
Staff ending, including its complete original controller, the two
376-byte CDG image reveal routines, the orbital particle/rain routines
and the frame-advance source.

| Decoded interval | Original DGROUP | Natural C public purpose | Source bytes |
| --- | --- | --- | ---: |
| `1184A..1184B` | `173A` | `staff_back_page`, one-byte frame/page selection | 1 |
| `1184C..11850` | `173C` | `staff_spark_cursor` and `staff_orb_opening_frame`, signed 16-bit clocks | 4 |
| `11850..11851` | `1740` | `staff_camera_accel_phase`, one-byte acceleration phase | 1 |
| `11852..11856` | `1742` | `staff_rain_cursor` and `staff_rain_frame`, signed 16-bit rain clocks | 4 |
| `11856..11857` | `1746` | `staff_text_clear_requested`, one-byte text erase request | 1 |
| `11858..1185C` | `1748` | `staff_image_phase_a` and `staff_image_phase_b`, distinct 16-bit CDG reveal phases | 4 |

The original interposed bytes `[1184B,1184C)`, `[11851,11852)` and
`[11857,11858)` are explicit uncredited alignment in the historical
DATA layout, not a new C struct or extra runtime flag. The following
six-byte `staff_image_cover_a/b` text strings at `[1185C,11862)` are
already owned by a different complete original C DATA contribution and
are not repeated. The source also never merges these small variables
with the independently accepted CP932 staff filename bank or unrelated
ZUN initialization data.

All six natural C initializers are complete contributions, using the
original real near C globals, native word/byte widths and zeros. Their
six external-only binders preserve MAINE `group_01` and SHARED CODE
frames and supply only the preceding original DATA prefix, without
bytes, candidate instructions, or manufactured relocation values.
Every one received **two independent pinned Borland C producers**,
full raw and OMF/LEDATA/MAP scope equality and the original empty
ordered MZ fixup stream. Each has its **own compiled zero-to-one DATA
mutation**, rejected by the original-byte oracle. Focused receipts:

- `.analysis/unit-replays/gpt-web-staff-back-page-a/receipt.json`
- `.analysis/unit-replays/gpt-web-staff-orb-opening-clocks-a/receipt.json`
- `.analysis/unit-replays/gpt-web-staff-camera-phase-a/receipt.json`
- `.analysis/unit-replays/gpt-web-staff-rain-clocks-a/receipt.json`
- `.analysis/unit-replays/gpt-web-staff-text-clear-a/receipt.json`
- `.analysis/unit-replays/gpt-web-staff-image-phase-a/receipt.json`

This adds **15** authored initialized MAINE DATA bytes, and no CODE
credit. The source-level C++ public consumers retain their original
accepted code; shared-header ABI integration, if pursued, requires a
separate complete affected-unit and reviewed-ASM dependency replay.
No full program or all-game cold replay was executed.
