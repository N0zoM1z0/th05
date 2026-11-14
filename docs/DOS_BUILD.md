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
`config/maintained_sources.toml` overlaid. Outputs and `build.json` (sizes,
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
`MIKO.CFG`/`GENSOU.SCR`. Only one Borland/Wine build may run at a time.

## Verified routes (2026-11-14)

With the same timed inputs, original and rebuilt products both reach the title,
character select, the Stage 1 card, Stage 1 combat and the Stage 1 boss, then
a bomb and the Game Over/Continue screen. Scores differ only through input
timing. Evidence: `.analysis/runtime/play-{original,rebuilt}-b/`.

## Next

Only 4 maintained sources are overlaid so far. The remaining work is to replace
ReC98 translation units and undecompiled ASM with TH05's own exact sources
until the product links from maintained source alone, as TH04's does.
