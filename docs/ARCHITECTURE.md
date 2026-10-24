# Architecture

TH05 is a real-mode, segmented 16-bit PC-98 game using the Borland/TASM/TLINK
tool family. `OP.EXE` owns menus and setup, `MAIN.EXE` gameplay, `MAINE.EXE`
endings, and `ZUN.COM` launch/resident services. These responsibilities are
candidate source-level descriptions pending bounded target review.

Unlike TH04's MZ-named ZUN.COM, this TH05 target is a plain COM program.
Do not reuse a loader merely because filenames match across games.

| Artifact | Stored format | Decoded/container bytes | Relocations |
| --- | --- | ---: | ---: |
| MAIN | ordinary MZ | 145,958 | 998 |
| OP | DIET MZ | 77,798 | 952 |
| MAINE | DIET MZ | 77,396 | 667 |
| ZUN | plain COM container | 18,116 | 0 |

OP/MAINE sizes come from each original decoder's terminal ES:DI. Replaying at
load segments 1000 and 3333 yields identical complete decoded images after
undoing the observed relocation additions. This proves an analysis view;
neither decoded originals nor their packing stubs acquire authored progress.

Targets, decoded images, compiler output, and database exports are private.
Public configuration pins their identities and documents replay steps.
Authored progress belongs to reviewed, non-overlapping target extents backed
by maintained source and cold replay; upstream source coverage is a separate
diagnostic. Complete executables require their own packing/layout comparison.
