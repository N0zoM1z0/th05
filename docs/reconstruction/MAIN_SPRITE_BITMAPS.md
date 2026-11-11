# TH05 MAIN preshifted sprite resources

Four complete sprite tables in the original MAIN decoded MZ are now
**source-reproduced from the independent TH02/TH04 BMP image files**,
for 2,752 newly classified resource bytes. The real ReC98
`bmp2arr` C producer was built twice (`-O0` and `-O2`), with identical
byte-for-byte generated ASM sources in both builds and against the
preserved **native TASM translation unit's exact included files**.

| Complete table | Original MAIN range | Bytes | Source bitmap |
| --- | --- | ---: | --- |
| `sPOINTNUMS` | `2121A..2181A` | 1,536 | `th04/sprites/pointnum.bmp`, inner preshift |
| `sPELLET` | `2181A..2189A` | 128 | `th02/sprites/pellet.bmp`, outer preshift |
| `sPELLET_BOTTOM` | `2189A..218DA` | 64 | `th04/sprites/pelletbt.bmp`, outer preshift |
| `sSPARKS` | `21E7A..2227A` | 1,024 | `th02/sprites/sparks.bmp`, outer preshift |

The generator outputs the preserved original-language `db` binary pixel
literals (8-pixel-wide, monochrome rows), not CPU instructions. Every
complete table has the exact unique position above in the **original**
MAIN image, empty original MZ relocation list, and no overlap with
previously accepted source or native library ownership.

**The original linker arranged the tables differently from the
calibration.** The native-calibration positions, checked separately
against its actual TASM input files, are pointnum `21764`, pellet
`212A2`, pellet-bottom `21322` and sparks `21362`. Applying a single
global DGROUP offset instead would misidentify the original pixels.
No unknown bytes between the source tables are adopted.

[Native two-producer reviewer](../../scripts/review_main_sprites.py),
[source/BMP/hash evidence](../../config/main_sprite_resources.json) and
[explicit resource-only decision](../../config/reviewed_main_sprite_resources.json)
make the 2,752-byte extent reproducible:

```sh
python3 scripts/review_main_sprites.py --check
python3 scripts/review_main_sprites.py --structural-check
python3 scripts/ownership.py --check
```

Native `--check` requires the ignored ReC98 BMP files, its original
C generator source, the saved historical MAIN calibration and the
candidate-local-attested original MZ. The public structure check uses
only committed evidence; it does not assert bytes without access to
the original sources. These are classified as
`reviewed-embedded-sprite-bitmap`, with **zero CPU instructions and
zero game-authored C++ credit**. Sprite source provenance is not
equivalent to original compiler-generated game code acceptance.
