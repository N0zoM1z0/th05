# Yuki's opening solo attack family: common pursuit and completion

All three first solo-Yuki callbacks share a real pattern-completion
protocol: reset the phase clock, return to reposition mode and report
completion to the Boss controller. They also share the same conditional
random-pursuit window after the second pattern, with a distinct 32-frame
movement offset for the third (random-ring) attack. These are now expressed
in the canonical `yuki_patterns_initial.inl` as `YUKI_INITIAL_FINISH()` and
`YUKI_INITIAL_PURSUIT(offset)`. All individual shooting angles, rank-dependent
spread counts, RNG calls and timing conditions retain their original order.

The complete three-function **509-byte** original code contribution was
recompiled by two genuine Borland/TLINK producers. Both passed all raw
bytes, original ordered MZ relocations `[450,309,137]` and the existing
compiled ring-speed negative, recorded at
`.analysis/unit-replays/gpt-web-yuki-solo-first-reposition-pursuit-20261112-a/receipt.json`.
This is a source-quality improvement to already accepted Boss CODE, with
no duplicate authored-byte credit or full cold replay.
