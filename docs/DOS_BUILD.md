# DOS product build and play testing

The playable PC-98 product is separate from the exact per-unit replays. A
product build or run grants no exactness credit.

## Build

```sh
python3 scripts/build.py            # OP, MAIN, MAINE and ZUN, published together
python3 scripts/build.py --only main
```

Each product is a cold Borland 4.02/TASM build of the pinned ReC98 tree
(`b6ba5b0a`) with every maintained source listed in
`config/maintained_sources.toml` overlaid. Overlays use the exact-replay
wrapper form: unit pragmas, `GAME=5` (ReC98 shares some `th04` objects built
with `GAME=4`), then `#include` of the maintained source. Shift-JIS units are
re-encoded like the replays. A generated empty-SEGDEF anchor, linked after
`c0l.obj`, keeps our headers' declaration-context segments (e.g.
`SMALL_MAIN01_CONTEXT`) inside their group; otherwise TLINK stretches
`main_01` over the `main_03` segments. Outputs and `build.json` (sizes,
SHA-256, overlays, original equality) go to `.analysis/build/th05/`. ZUN.COM
goes through ReC98's `zungen`/`comcstm` pipeline and is byte-identical to the
original. OP and MAINE ship unpacked (the originals are DIET-packed).

## Play test

```sh
xvfb-run -a -s "-screen 0 1024x768x24" python3 scripts/play_dos.py \
  --products .analysis/build/th05 --output .analysis/runtime/NEW \
  --seconds 60 --event z@14 --event z@17 --frame title@13 --frame play@40
```

`--original` runs the unmodified game as the reference. The runner copies the
private multi-game HDI pinned in `config/runtime.toml` (its `KAIKI/`
executables equal the TH05 targets), installs the products, and boots
`GAME.BAT` through ZUN, OP, MAIN and MAINE. It runs DOSBox-X headless (PC-98,
24,000 cycles, Pentium normal core) and drives keys with xdotool
(`z@S`, `down:z@S`, `up:z@S`). It saves window PNGs and before/after
`MIKO.CFG`/`GENSOU.SCR`. `--install DOSNAME=PATH` copies a file into the
game directory first, for example a `GENSOU.SCR` with Extra unlocked. Only one
Borland/Wine build may run at a time.

## Verified routes (2026-11-14)

With the same timed inputs, original and rebuilt products both reach the title,
character select, the Stage 1 card, Stage 1 combat and the Stage 1 boss, then
a bomb and the Game Over/Continue screen. Scores differ only through input
timing. Evidence: `.analysis/runtime/play-{original,rebuilt}-b/`.

## Maintained-source coverage

MAIN overlays 34, OP 9 and MAINE 7 ReC98 translation units with TH05's exact
units. After the build, `scripts/integrate_product.py` (method in
`scripts/lib/product_integration.py`) also links the accepted units whose code
ReC98 still keeps in its IDA dumps `th05_main.asm` and `th05_maine.asm`:

1. Each unit module is compiled exactly as in its replay, into `obj/integ/`.
2. One relink with a public marker before every dump procedure and data label
   gives their addresses; bytes do not change.
3. A unit's code is located in that image by matching every byte outside its
   FIXUPP fields. The dump procedures that tile the match, and the tables and
   alignment between them, are cut and declared `extrn`.
4. The unit object gets alias PUBDEFs for the cut names. Its externs that ReC98
   names differently are renamed to the symbol the matched ReC98 code
   resolves at the same fixup; dump labels it needs become public.

Every TLINK warning or error stops the link. In the current build this
replaces 175 MAIN and 22 MAINE dump procedures (29,176 MAIN dump bytes) with
99 MAIN and 18 MAINE units; `integration.json` next to each build lists them
and the reasons the others stay out. The attract loop plays the same three
demos as the unintegrated build.

Still from ReC98: units inside ReC98 C++ translation units that are not
overlaid (their function would have to be cut from the C++ source), units built
through special pipelines (`compiler_pipeline`, generated sources,
before/after binders), units whose ReC98 code differs from the original bytes,
initialized DATA units, the reviewed ASM families, and all of OP's dump code.

## Position independence

`scripts/audit_dos_pi.py` relinks these products with moved CODE/DATA/BSS and
checks that every relocation, far call, far pointer, switch table and direct
displacement follows its owner. See
[DOS_POSITION_INDEPENDENCE.md](reconstruction/DOS_POSITION_INDEPENDENCE.md).
