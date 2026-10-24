# Boss explosion producer candidate

This owner localizes the candidate `th05/boss_exp.cpp` contribution from
nmlgc/ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`. It uses maintained
natural C++, a complete 16-byte explosion state and genuine Borland DOS
pseudoregisters/port-I/O intrinsics. No target instruction arrays, replacement
returns, alignment injections or missing-field padding are supplied.

The routing survey's masked comparison is only a discovery aid. Inspecting
the pinned original MAIN confirms two complete raw instruction streams at
load-module offsets `0x1060E..0x106D8` (202 bytes) and
`0x106D8..0x107D2` (250 bytes). Both end with real returns; their combined
452-byte extent contains no NOP exclusions. Target SHA-256 is
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
These are load-module offsets, not MZ-file offsets. The MZ header is 4032 bytes.

Use wrapper `th05/boss_exp.cpp` including `src/main/boss/explosion.cpp` with
the existing MAIN C++ flags (`-O -b- -3 -Z -d -DGAME=5 -ml -DBINARY='M'`).
The source selects `BOSS_EXP_TEXT`; the original context puts it in `main_01`.
No old accepted source or shared header was changed for this candidate.

Numeric references below are observed in the original target; the descriptive
symbol roles and declarations are corroborated by the candidate source.
DS retains the previously observed DGROUP-relative segment `209D`.

| Symbol / dependency | Original reference |
| --- | --- |
| `_explosions_small` | DS:`43FC`, two 16-byte entries |
| `_explosions_big` | DS:`441C`, one 16-byte entry |
| `_explosion_big_frame` | DS:`18E4`, signed word |
| `_SinTable8` | DS:`041C`, external signed-word table |
| `_CosTable8` | DS:`049C`, external signed-word table |
| `_PaletteTone` | DS:`03DA`, unsigned word |
| `_palette_changed` | DS:`576D`, byte |
| `@grcg_setmode_rmw$qv` | Near destination, load-module `0xC1F8` |
| `Z_SUPER_ROLL_PUT_TINY_16X16_RAW` | Near destination `0xC07C`; AX=left, DX=top, Pascal stack patnum |
| `@POLAR$QIII` | Far destination `14AB:0394`, load-module `0x14E44`; three Pascal word arguments |
| `SUPER_PUT` | Far destination `0000:33F0`; three Pascal word arguments |

The two trigonometric tables overlap in their reference layout. Their declared
array views are external ABI declarations, not new data owners. The exact far
segment:offset operands matter independently of their equivalent linear address.

The smaller renderer uses unsigned AX/DX expressions for clipping and a 16x16
sprite pattern 164. The larger renderer uses signed locals and pattern 3. It
deliberately retains the original 64x64 clipping assumption for a 48x48 sprite.
Converting those expressions into differently typed helper arguments can alter
both the comparisons and generated code.

No compilation or exact acceptance is asserted by this packet. A focused cold
build must verify OMF, complete 452 raw bytes and all five far-segment fixup
sites, followed by its required independent round and negative control. Any
symbol-binding scaffold proves only bounded code bytes, never full layout or
ownership of the external data/helpers.
