# MAIN filename data

These C files reproduce initialized filename data in MAIN's data segment. Each
groups neighboring strings into one struct only so that the compiler emits
them contiguously and in the original order; the game addresses every string
on its own, and the original source probably declared them separately.

| File | Contents | DS offset |
| --- | --- | --- |
| `startup_resource_links.c` | far pointers to `"ST00"` and `"BB0.CDG"` (`bbname`) | `00A2` |
| `resource_bank.c` | archive, sound and launcher names, `"ST00"`, then 34 palette/font/face/stage filenames | `00B2` |
| `pause_spaces.c` | three 4-space strings that erase the pause menu | `020D` |
| `session_files.c` | `DEMO0.REC`, `op`, `KAIKIEMS`, `BB0.CDG`, `KAO0.cd2` to `KAO3.cd2` | `021C` |

## Findings

- **Duplicate strings are separate objects.** Stage 6 (Extra) has its own
  copies of `BSS4.CD2` and `st04.bft`. As separate `const` arrays, the
  compiler merged each pair into one object (304 instead of 322 bytes).
  Struct members keep them apart.
- **Even start address.** The 34 stage/session filenames start at the odd
  offset `00CB`, which a word-aligned data segment cannot start at. Including
  the four preceding strings (archive name to `"ST00"`) moves the start to
  the even `00B2`.
- **C, not C++.** Turbo C++ rejects `const` array members in an aggregate
  that has no constructor, so these files are compiled as C.
- **Writable strings.** The stage setup code patches the last two characters
  of `"ST00"` before loading the stage BGM, and
  `bomb_bg_load__ems_preload_playchar_cdgs()` writes the player digit into
  `"BB0.CDG"` through `bbname`. Both are therefore non-`const`.
- The EMS handle name is `KAIKIEMS` in this executable, although ReC98's
  TH05 macro says `GENSOEMS`.
