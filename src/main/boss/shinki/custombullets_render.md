# Shinki custom bullet renderer

MAIN `[12FF5,13066)` is one complete 113-byte C++ function, with no table,
padding or owned DATA/BSS. It reuses the existing full Shinki/custom entity
types without changing shared headers. The 63 ball slots retain cloud-circle
rendering with signed radius division, solid tiny-32 rendering with only
negative-Y clipping, and the final Cheeto renderer call. Stage scrolling is
absent, as in the original.

Frame is `0AE1` in `main_01`, DS `209D`. AH supplies the genuine GRCG color;
ES selects VRAM and AX/DX supply the real raw sprite helper's coordinates.
The sole far fixup is the MASTER circle-fill call, at relative offset 61.
Empty foreign compiler segments stay in their real main_01/main_03 groups.

`main-shinki-custombullets-render-a` passes two deterministic producers,
complete raw bytes and ordered fixups `[61]`. The shared compiled cloud-color
mutation from 15 to 14 is rejected. Receipt:
`.analysis/unit-replays/main-shinki-custombullets-render-a/receipt.json`, SHA-256
`91db51f0e6e7becbf23cbcee8a77c9847ca8385881f8fb3d3c7f47a30cf6b931`.
Native boundary/ABI review:
`.analysis/shinki-custombullets-render-boundary-review.json`.

Pinned ReC98 `b6ba5b0a` supplies supplemental rendering evidence; acceptance
comes from the local TH05 target and compiler output. No reference instruction
body, target-byte table or hand assembly is maintained here.
