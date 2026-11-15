# Laser ray rendering and hit testing (assembly)

`laser_render_hit.asm` holds four procedures in MAIN main_01 (CS `0AE1`):

| Procedure | MAIN range | Interface |
| --- | --- | --- |
| Vector at center | `D5C2..D5FA` | center at SS:BP, length in BX, angle in CX, result at SS:DI |
| Line to pixels | `D5FA..D626` | point at SS:DI, endpoint at SS:BX, displacement at SS:BP+4 |
| `laser_render_ray()` | `D626..D6C6` | near Pascal, `const laser_coords_t near &`; returns AX |
| `laser_hittest()` | `D6C6..D71E` | near Pascal, `Laser near &`; RET 2 |

ReC98's `th05/main/bullet/laser_rh.cpp` documents the same algorithms. The
source exports the C++ names `@LASER_RENDER_RAY$QRX14LASER_COORDS_T` and
`@LASER_HITTEST$QR5LASER` so the C++ callers link against them.

## Behavior

- The vector helper sign-extends the length and each sine/cosine sample,
  multiplies in 32 bits and shifts right arithmetically by 8, then adds the
  center with 16-bit wraparound. AX returns Y. It saves only SI and clobbers
  EAX/EDX.
- The ray uses ENTER 32 / LEAVE and passes SS:DI far pointers to master.lib's
  `grc_clip_polygon_n()` (`0000:139E`) and `grcg_polygon_cx()` (`0000:18B4`).
  A clip result of 0 means the laser is off-screen (returns true); a negative
  result draws the four unclipped corners.
- ZUN quirk: the hit test steps from the laser's end to its start and tests
  12x12-pixel boxes every 16 pixels, leaving 4-pixel gaps through which the
  player can pass.

## Why this stays assembly

The ray moves BP from its frame to BP-4, then BP-12, and back, while the
private helpers read and write the caller's stack through BP, DI and BX.
The line helper's displacement depends on BP+4, and the hit test saves DI
and SI in reverse order.

A scratch Turbo C++ 4.0 compile (`-S -O -3 -k-`) of the vector helper with
pseudo-registers reproduces every arithmetic instruction, but always wraps
the body in `push di` / `pop di`, whether DI is used through inline `asm`, a
`_DI` pseudo-register or with `-r-`. The original saves only SI. Matching it
needs `__emit__` opcode bytes, as ReC98 does, which is transcription rather
than source; the reversed `push di; push si` in the hit test has the same
problem.
