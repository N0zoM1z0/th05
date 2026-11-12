# Original Master BGM track/effect state: 198 unwritten bytes in each EXE

The archived Master author `B_DATA.ASM` declares `timerorg dd ?`, three
`SPART <>` music channels, and 16 `SESOUND <>` effect slots. `BGM.INC`
defines the exact structure widths (22 bytes per music part and eight per
effect), so their full storage is **4 + 3×22 + 16×8 = 198 bytes**.
All structure fields are declared with `?`, not authored zero values.

| Original EXE | Source-backed full 198-byte reserve | First MAP public |
| --- | --- | --- |
| MAIN | `23960..23A26` | `209E:2FA2` |
| OP | `12744..1280A` | `0EFE:3764` |
| MAINE | `127F0..128B6` | `1010:26E0` |

The actual original-compiler TASM `_BSS` PUBDEFs bind `timerorg`,
`part`/`_bgm_part` and `esound`/`_bgm_esound` to the correct offsets.
The complete `_BSS` segments have **no LEDATA or LIDATA writes**, and the
original MZ target views contain exactly 198 materialized zero bytes per
program without loader relocations. The retained TASM source agrees with
the original Master author archive.

`python3 scripts/review_master_bgm_track_bss.py --check` verifies the
archived source layout, native source, actual segment/PUBDEF, MAP,
original payload and source-unwritten semantics. This adopts **594 bytes
of third-party uninitialized storage**, with **zero original initialized
DATA, C/C++ CODE or instruction credit**. The adjacent single-byte MIDI
flag, its alignment and later game structures remain separately unknown or
independently owned.
