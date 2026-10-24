# TH05 laser state and controls

Natural semantic C++ derives from ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th05/main/bullet/laser.cpp` and `laser.hpp`. Its acceptance does not transfer.
Original intervals below are independently checked against the pinned local
MAIN MZ load image, not file offsets or calibration addresses.

The full 24-byte Laser and 10-byte coordinate structures retain the real
flag/color, origin, distance endpoints, angle, signed/unsigned width overlay,
speed, age, active/shrink timing, target width and three unused bytes. The
layout assertions check every consumed scalar boundary. Thirty-two slots start
at DS:578C and the template at DS:5A8C; DS is 209D.

| Complete function | Original interval | Bytes |
| --- | --- | ---: |
| Shoot-out allocation | 1A66E..1A6EF | 129 |
| Timed fixed spawn | 1A6EF..1A74B | 92 |
| Manual fixed spawn | 1A74B..1A7A5 | 90 |
| Manual growth | 1A7A5..1A7CE | 41 |
| Stop by current state | 1A7CE..1A82E | 96 |

`main-laser-control-a` compares the complete 448-byte compiler contribution
from two independent fresh producers and rejects a compiled target-width
mutation from 6 to 7. All bytes and original ordered loader fixups match;
no padding, DATA or BSS receives credit. Genuine speed tuning uses the observed
AL fastcall API, vector placement and sound retain their far Pascal frames.
The symbol-only binder supplies their original addresses and no bodies.

The separate update candidate covers 12BAD..12CE5, including its seven-word
compiler switch table at offset 298. `main-laser-update-b` passes both complete raw/ordered comparisons and
rejects its own compiled speed-decay mutation from division by 2 to 4. It
implements shoot-out movement, fixed
width growth/shrinkage, clear/zap decay and real age transitions. Signed width
comparisons and signed division retain their original semantics. The table is generated from the semantic switch and counted separately from
298 instruction bytes.
The renderer is a separate complete 582-byte function, 12CE5..12F2B.
`main-laser-render-a` passes two independent raw/ordered producers and its own
compiled minimum-radius mutation from 2 to 3. It preserves ray widths across
inner/outer rendering, screen conversions, shoot-out decay edges, and actual
foreign clipping results. The genuine color helper receives AH explicitly;
its body and the custom register/stack ray helper remain external. All 582
bytes are natural C++ with no inline opcode or helper-body transcription.
