# DOS position independence

Position independence (PI) means that every memory reference in the source is
symbolic, so code and data can be added, removed or resized without breaking
the game. ReC98 counts the hexadecimal operands left in its ASM dumps that fall
inside an executable's data range; structure resizing is out of scope. ReC98
reached 100% PI for TH05's `OP.EXE`, `MAIN.EXE` and `MAINE.EXE` in September
2020 (`cbf14ebb`, "Final false positives in TH05's MAIN.EXE"). That result
covers the pinned ReC98 tree, not our maintained source, so this audit checks
the TH05 DOS product we build (`scripts/build.py`: ReC98 `b6ba5b0a` with the 50
maintained translation units of `config/maintained_sources.toml` overlaid) and
the maintained source itself. The method follows TH04's
`TH04_DOS_POSITION_INDEPENDENCE.md`.

## Shifted relinks

`scripts/audit_dos_pi.py` relinks the product objects unchanged; the control
reproduces each EXE and MAP byte for byte. It then inserts a padding
contribution after the first definition of every public CODE segment and every
DGROUP DATA/BSS segment and relinks. Three layouts insert 16/32/48, 32/16/64
and 3/7/11 bytes of CODE/DATA/BSS; the last one also breaks word and paragraph
alignment. In each layout every original contribution keeps its size and the
checker maps the following back to their MAP owners:

| Executable | Contributions moved (CODE/DATA/BSS) | MZ relocations | Far CALL/JMP targets | Far data pointers | Switch tables (entries) |
| --- | ---: | ---: | ---: | ---: | ---: |
| MAIN | 162 / 26 / 7 | 1,001 | 819 | 19 | 60 (519) |
| OP | 112 / 35 / 13 | 952 | 526 | 279 | 17 (162) |
| MAINE | 105 / 27 / 12 | 667 | 436 | 84 | 16 (151) |

All relocation sites keep their order within their owners. Every far
transfer, every far pointer in initialized data (offset word plus relocated
segment) and every case of a `cmp`/`jmp word ptr cs:[bx+table]` switch still
reaches the same owner-relative target. The table length comes from the bound
compare; master.lib's `_BGM_MGET` compares a byte offset, so its 13-entry table
is bounded by `18h/2+1`.

Capstone 5.0.6 then screens direct 16-bit CS/DS displacements, restarting the
decode at every MAP public. Of 7,113 (MAIN), 1,403 (OP) and 1,754 (MAINE)
displacements that name a mapped owner, 6,961, 1,172 and 1,531 move with it. A
displacement whose owner moved but whose value did not follow is listed in
`direct-offset-review.json` (18, 97 and 95); a candidate inside a checked
switch table is dropped. All listed candidates were reviewed:

- **Hardware and foreign segments.** master.lib `GET_MACHINE_AT` reads the BIOS
  work area (`[04D0h]`, `[01F4h]`); `GRAPH_PI_LOAD_PACK` addresses fields
  `[4000h..4113h]` of its PI work buffer through a DS that points at the buffer
  segment. These values are correctly constant.
- **Misdecoded data.** Borland CL.LIB `new`, `xmsg`, `xalloc`, `strings` and
  `ctor2/3` embed exception and relocation tables in CODE; master.lib `PFEND`
  embeds a dispatch table. The "operands" are table bytes.
- **Switch tables before a function.** The bytes before `zunsoft_animate()`
  (OP) and before a `cutscene.cpp` function (MAINE) are near-offset tables of
  the preceding switch; each word follows its code.

No game code in the three executables references DGROUP or CODE through a
literal address.

## Maintained source

A screen of `src/` for numeric memory operands (`[1234h]`, `ds:[...]`),
integer-to-pointer casts, `MK_FP` with literals, `__emit__` and inline `asm`
found only PC-98 hardware and DOS interfaces: BIOS key groups at `052Ah`, VRAM
segments `A800h..E000h`, GRCG/EGC ports, the ROM board ID at `es:[2]`, the PSP
environment word `es:[2Ch]`, the IVT in `KAJA_ISR`, and the self-modifying
`mov di, 1234h` placeholder in `bgimage_rect.asm`.

One real case was fixed: the ZUN outer launcher read its own COMCSTM header as
`ds:[103h]`, `ds:[105h]` and `ds:[107h]`. The three fields now carry labels
(`header_usage_ptr`, `header_usage_size`, `header_inner_size`); the
`zun-outer` replay still reproduces every byte (receipt
`.analysis/zun-outer/pi-labels-a/receipt.json`).

## Every accepted unit, at object level

The product links only 50 maintained translation units, so
`scripts/audit_unit_pi.py` checks all 548 C/C++ units and 87 ASM families from
their retained producers instead. For each one it rebuilds the compiled OMF
segment and the bytes covered by FIXUPP records, decodes the unit's own extent,
and lists:

- any 16-bit direct memory displacement (no base or index register) whose
  field has no fixup, and
- any 16-bit immediate without a fixup whose value equals the offset of a
  DGROUP public in the producer MAP. The binders place every foreign symbol at
  its original address, so a literal pointer would match one.

Of 7,672 direct displacements, 32 have no fixup, and all of them address
PC-98 BIOS or interrupt-vector memory through ES: the key groups
`es:[052Ah..0533h]` in the three input-sense families, the INT 60h/61h vectors
`es:[0180h]`/`es:[0184h]` in the PMD/MMD resident checks, and the EGC BIOS byte
`es:[0495h]` in `egc-rect-setup`. No immediate matches a DGROUP public without
a fixup; 278 immediates in MAIN units that do match all carry one. Removing an
object's fixup coverage makes the check report the unit's DGROUP accesses.
DATA units are not decoded: a literal pointer in an initializer has no
recognizable shape, so those rely on the source screen.

## Layout adjacency

Two dependencies on variable order survive any fixup check:

- `HUD_SCORE_PUT` (`src/main/hud/score.asm`) prints `_hiscore` and then
  `_score` without resetting SI, so `_score` must directly precede `_hiscore`,
  exactly as in TH04.
- The random-ring readers read a word at `randring[randring_p]`; at index 255
  its high byte is the cursor's own low byte, so `randring_p` must directly
  follow the 256-byte ring.

Both pairs sit inside the `_BSS` contribution of ReC98's `th05_main.asm`, so
the relinks never split them (distance 8 and 256 in all four layouts). Treat
each pair as one layout owner when moving or redefining them. Adjacent fields
written together inside one structure (spread count and angle delta, bullet
template fields) are structure layout, which ReC98's PI criterion excludes.

## Runtime

Headless DOSBox-X (`scripts/play_dos.py`, 24,000 cycles, no input) booted the
baseline and the 3/7/11 and 32/16/64 products through `GAME.BAT` into the first
attract demo and saved a frame every 2 s from 26 to 48 s
(`.analysis/runtime/pi-demo-{baseline,shift-3-7-11,shift-32-16-64}/`). All
three play the same Lunatic demo with the same enemies, bombs and
points. Host-timed captures are not frame-aligned, so each capture was matched
to its nearest frame of the port's `--scene demo1` render. The matched frames
advance in lockstep: 3/7/11 stays 4 frames ahead of the baseline (271 vs 267
at 26 s, 1651 vs 1646 at 48 s) and 32/16/64 stays 39-40 frames behind, the
difference in boot time. Every capture differs from its port frame by about
100,000 pixels in all three runs, so this is a trajectory check, not a
pixel-exact one; TH04's memory observer has no TH05 counterpart yet.

## Limits

- The product links the 50 overlaid translation units plus, since the
  integration, 141 MAIN and 26 MAINE units in place of ReC98 code (see
  [DOS_BUILD.md](../DOS_BUILD.md)). The integrated build passes the same three
  relinks: MAIN 313 contributions, the 1,001/952/667 relocations, all far
  transfers, far pointers and switch tables, and no new literal candidates;
  its attract loop plays the same demos. The remaining units are covered by the
  object-level check, not by a relink or a runtime run.
- ZUN.COM is built by ReC98's `zungen`/`comcstm` pipeline and was not relinked.
  The ZUN resident ASM families (`file_family_native.asm`,
  `resdata_native.asm`) use `org` to place their bounded scope inside the `-S`
  child, like the per-unit binders; they cannot be linked standalone.
- Layout adjacency that code relies on without a literal address (TH04's
  `_score`/`_hiscore` pair) is not visible to the relink check. The padding
  goes after the first definition of each segment, so it separates neighbours
  only at that point; the demo run above is the only exercise of the rest.

## Replay

```sh
python3 scripts/build.py --output .analysis/build/pi-baseline
python3 scripts/audit_dos_pi.py --baseline .analysis/build/pi-baseline \
  --output .analysis/pi/shift-16-32-48
python3 scripts/audit_dos_pi.py --baseline .analysis/build/pi-baseline \
  --output .analysis/pi/shift-32-16-64 --padding 32 16 64
python3 scripts/audit_dos_pi.py --baseline .analysis/build/pi-baseline \
  --output .analysis/pi/shift-3-7-11 --padding 3 7 11
```

Each output directory holds the shifted products, `build.json`, and per
executable `receipt.json` and `direct-offset-review.json`.

```sh
python3 scripts/audit_unit_pi.py --output .analysis/pi/unit-literals.json
```
