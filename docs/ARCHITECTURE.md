# Architecture

TH05 is a real-mode, segmented 16-bit PC-98 game using the Borland/TASM/TLINK
tool family. `OP.EXE` owns menus and setup, `MAIN.EXE` gameplay, `MAINE.EXE`
endings, and `ZUN.COM` launch/resident services. These responsibilities are
candidate source-level descriptions pending bounded target review.

Unlike TH04's MZ-named ZUN.COM, this TH05 target is a plain COM program.
Do not reuse a loader merely because filenames match across games.

Targets, decoded images, compiler output, and database exports are private.
Public configuration pins their identities and documents replay steps.
Authored progress belongs to reviewed, non-overlapping target extents backed
by maintained source and cold replay; upstream source coverage is a separate
diagnostic. Complete executables require their own packing/layout comparison.
