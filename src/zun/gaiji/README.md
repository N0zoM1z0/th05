# ZUN.COM `-G`: exact PC-98 custom-glyph installer

The ZUN.COM launcher embeds an independent `-G` gaiji installer as a plain
DOS COM member at original outer-file `[2488,4541)` (8,377 bytes) and COM
runtime `[0100,21B9)`. Its full original SHA-256 is
`b27d83dffa8d2bc9716a5e8cf135b95e181e67b1e34bb8cbbf28aa057153f6d8`;
its full MD5 is `7c8f4cab7f06b9a218e838d50bb4e314`.

The maintained semantic 8086 assembly is [install.asm](install.asm). It
initializes the PC-98 GAIJI CG-RAM ports `68h`, `A1h`, `A3h`, `A5h` and `A9h`,
then uploads 256 glyphs of 16 rows each to the hardware custom-glyph range
`5680h..577Fh`. Each glyph row is read by `LODSW`, split into two CG-RAM
plane accesses, and written with the original register and loop protocol.
The DOS print/exit services also retain the native Japanese result message
and version banner.

## Distinct byte provenance

| Complete COM byte range | Class | Bytes | Origin/credit |
| --- | --- | ---: | --- |
| `[0000,004B)` | CG-RAM installer instructions | **75** | Semantic register ASM, original source inferred |
| `[004B,004C)` | `_TEXT`/`_DATA` word alignment | **1** | Checked, zero instruction credit |
| `[004C,00B9)` | DOS banner and confirmation text | **109** | Initialized semantic text |
| `[00B9,20B9)` | 256 distinct glyph bitmaps | **8,192** | Separate, previously reviewed external font; **zero authored credit** |
| **Entire child** | **Original COM byte-for-byte** | **8,377** | No code/asset double counting |

The native font is not shipped or reproduced in the maintained assembler.
Instead the private native replay materializes a disposable
`gaiji_private_asset.inc` **only under ignored `.analysis/`**, by converting
the independently pinned `_reference/ReC98/th05/sprites/gaiji.bmp` using
`review_font_resource.bitmap_tiles()`. That resource model and its 8,192-byte
original target digest are already reviewed separately in
[`config/font_resource.json`](../../../config/font_resource.json) and
[`config/reviewed_font_resource.json`](../../../config/reviewed_font_resource.json).
No asset byte array, generated font file or sprite payload is introduced into
this repository's public source tree. The complete COM has 75 executable
instruction bytes, not 8,377.

The pinned ReC98 `th05_gjinit.asm` is an IDA-generated native reference.
The algorithm and CPU/port protocol independently support register-level ASM,
but neither historical source spelling nor global authorship percentage is
proven by the exact byte match. The currently accepted source and resource
owners remain separate from the open overall denominator.

## Focused native source verification

The targeted receipt
`.analysis/zun-gaiji/gpt-web-gaiji-a/receipt.json` contains two real,
independent TASM32/TLINK producers. Each outputs the complete 8,377-byte
COM with the original SHA-256, real `GAIJI_INSTALL_START` public at `0100`,
the actual mixed `_TEXT`/`_DATA` segments, and gapless OMF LEDATA. The source
negative shortens the glyph upload loop from sixteen rows to fifteen: both
outputs retain the original 109-byte messages and 8,192-byte external bitmap,
while only the instruction region differs and the strict oracle rejects it.

The explicitly scoped, zero-global-credit evidence is
[`config/zun_gaiji_acceptance.json`](../../../config/zun_gaiji_acceptance.json).
Its source-current lightweight check invokes **no compiler or game**:

```sh
python3 scripts/replay_zun_gaiji.py --check
```

To explicitly perform **only the -G member** native replay:

```sh
python3 scripts/replay_zun_gaiji.py --output .analysis/zun-gaiji/NEW
python3 scripts/replay_zun_gaiji.py --accept .analysis/zun-gaiji/NEW/receipt.json
```

The accepted `-I` 1,009-byte and `-M` 311-byte children use their own separate
source and evidence, and neither was recompiled for this focused work.
