# Music Room piano

The piano code lives in OP's `SHARED` segment (CS `0D30`, DS `0EFE`) at
`D894..DB3C`. It follows ReC98's `th05/op/piano_c.cpp` and `piano_a.asm`.

| Range | Function | Source |
| --- | --- | --- |
| `D894..D96E` | `piano_setup_and_put_initial()` | `setup_exact.cpp` |
| `D96E..D9E2` | `piano_render()` | `render_exact.cpp` |
| `D9E2..DA12` | `piano_fm_part_put_raw` | `fm.asm` |
| `DA12..DA30` | `piano_current_note_from()` | `note_register.cpp` |
| `DA30..DB01` | blank keys, pressed key, dispatch and key positions | `keys.asm` |
| `DB01..DB0D` | pressed-key top masks (12 bytes of data) | `pressed_top.asm` |
| `DB0D..DB21` | label glyph blit | `label.asm` |
| `DB21..DB3B` | direct GRCG color helper | unknown |

## Calling conventions

The assembly helpers take their parameters in registers:

- `piano_fm_part_put_raw`: ES:DI = VRAM position of the part's keyboard,
  SI = FM part number, DS:BX = address of the part's near pointer, FS = the
  game's data segment. It calls `piano_current_note_from()` with DS still set
  to PMD's work area, then switches to FS for game state.
- `piano_part_keys_put_raw` preserves DI and SI; `piano_pressed_key_put`
  preserves BX and DI.
- The keyboard and label code use string instructions and rely on the caller's
  DF = 0; there is no CLD.
- The direct color helper always ends with STI, so drawing paths return with
  interrupts enabled.

`piano_notes_cur` (DS `382A`) and `piano_notes_prev` (`3832`) are eight bytes
each: five FM notes and three unused bytes.

## Build notes

- `render_exact.cpp` needs `tcc -S` and TASM32, because only that path emits
  the 386 `POP FS`. `setup_exact.cpp` and `note_register.cpp` are compiled
  directly with `tcc -c`.
- Both C++ units call near helpers that sit in a separate segment in the link
  scaffold. The scaffold groups them with the C++ code so that TLINK resolves
  the near calls; at runtime everything is in CS `0D30`.
- `label.asm` starts at the odd address `DB0D`, so it must be assembled with
  BYTE alignment. With WORD alignment it moved to `DB0E`.
- The key position table in `keys.asm` is computed from the piano geometry
  (left = 384, key width = 4, sharps halfway between white keys).
  `replay_asm_family.py` checks it with its `piano-key-horizontal-positions`
  model. One of its bytes is 90h; it is data, not a NOP.
- The pressed-key masks in `pressed_top.asm` are derived from three key
  shapes, shifted into bit 5. They have their own acceptance file,
  `config/piano_pressed_top_acceptance.json`.

## Open questions

- `DB21..DB3B`: its 20-byte core matches master.lib's `GRCG_SETCOLOR`
  (`GC_SETCO.ASM`), but the interrupt handling and calling convention differ.
  It is unclear whether it is a modified library function or ZUN's code.
- The byte at `DB3B` has no known owner.
- The pixel data of the black keys (DS `09EE`), the label font (DS `0A0A`) and
  the CODE sprite bank (CS `0801`) are game resources and are not part of
  these sources.
