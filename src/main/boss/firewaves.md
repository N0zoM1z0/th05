# EX-Alice firewaves

Natural C++ from pinned ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th05/main/boss/bx.cpp`. Two true six-byte firewave records retain byte alive /
direction flags and signed word bottom / amplitude. Addition picks the first
free record; update advances the bottom four pixels and disables it at 608.

The complete original MAIN contribution `[1983D,1989B)` is 94 instruction
bytes, with complete add `[1983D,19871)` (52) and update `[19871,1989B)` (42).
Both are near in original `main_03` frame `1527`; the Pascal add cleans four
argument bytes. All local branches land on observed instruction starts. There
are no CODE tables, padding or MZ fixups. The original DS `209D` pool offset
is `4A90`, independently observed in both function operands.

`main-firewaves-b` passes both independent cold producers and the compiled
four-to-three pixel speed negative. The symbol-only scaffold emits neither
state values nor helper bodies; no BSS or whole-executable credit is claimed.
