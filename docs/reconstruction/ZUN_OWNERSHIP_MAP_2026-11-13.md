# ZUN.COM ownership overlay correction (2026-11-13)

The ownership view covers the complete original 18,116-byte `ZUN.COM` file.
Its earlier 8,290-byte unknown total included several complete, independently
accepted modules that were not yet imported into `resources/ownership.json`.
This was an inventory integration gap, not newly discovered source bytes.

`scripts/review_zun_ownership.py` now binds each focused acceptance to the
original launcher member and overlays only its source-written interval:

| Scope | Complete bytes | Instructions | Initialized data | Alignment |
| --- | ---: | ---: | ---: | ---: |
| COMCSTM outer header/help/wrapper | 371 | 71 | 300 | 0 |
| Inner dispatcher/catalog/copy helper | 558 | 213 | 345 | 0 |
| `-O` ADPCM child | 926 | 892 | 34 | 0 |
| `-I` interrupt child | 1,009 | 450 | 557 | 2 |
| `-G` gaiji reader/messages (font separate) | 185 | 75 | 109 | 1 |
| `-M` memory child | 311 | 142 | 169 | 0 |
| Master `-S` resdata/graph-clear family | 226 | 224 | 0 | 2 |
| Master `-S` file/DOS family | 830 | 823 | 0 | 7 |
| **Newly overlaid total** | **4,416** | **2,890** | **1,514** | **12** |

The two Master families are classified as `verified-vendor-code` with zero
source-authored credit. The launcher/child reconstructions use separate
`accepted-zun-com-*` categories because they are not part of the MAIN/OP/MAINE
reviewed-ASM denominator. Their source-origin limits remain in their individual
acceptance records. The existing C0T CRT, three resident C++ units, and the
8,192-byte embedded font retain their previous independent owners; none is
counted a second time.

## Borland nearheap object matched (2026-11-13)

The original tiny-model `CT.LIB` `nearheap` member is now independently matched
at `-S` COM runtime `0x0C9C..0x0F13` (631 CODE bytes) and DATA
`0x1A6A..0x1A70` (6 initialized bytes). Its three public function boundaries
are `_free` at 0, `_malloc` at 207 and `_realloc` at 550; the DATA publics
`__first`, `__last` and `__rover` occupy offsets 0, 2 and 4. All 579 non-
relocation CODE bytes match verbatim; the only 52 differing bytes are exactly
the member's 26 two-byte OMF relocation fields. The six DATA bytes match
verbatim.

The FIXUPP stream is now decoded semantically, not treated as an opaque mask:
20 offset relocations use `_DATA` through `DGROUP` and resolve to `DS:1A6A`
plus their original addends; six relative external relocations resolve to
`___brk` at `0x0C1D` and `___sbrk` at `0x0C43`. Both target entries have the
original near-function prologue. Re-applying those exact OMF relocations to the
pinned CT.LIB LEDATA reconstructs the complete 631-byte target CODE exactly.
The 41-file Borland library tree and the individual `CT.LIB` member are both
hash-attested. Two negative controls mutate a nonrelocation instruction and a
resolved relocation word; both are rejected by the same comparison path.

`scripts/review_zun_nearheap.py --check` pins the installed Borland library
tree, exact `nearheap` OMF member/publics/groups/externals/LEDATA/FIXUPP
semantics, original `-S` child identity, all relocation offsets, and both
target slices. The object is vendor code/data and receives zero
source-authored credit. The two referenced `brk` entrypoints are not claimed
by this nearheap record; their own 127-byte CT.LIB module remains a separate
source/relocation review within the preceding unknown interval.

The corrected ZUN view now has exactly **3,237 unknown bytes**, in five
intervals:

- `0x0D47..0x0D49` (2 bytes): the original writable CRT CS: runtime slot; it is
  intentionally not initialized or credited.
- `0x13BA..0x1680` (710 bytes): `-S` COM runtime `0x09D6..0x0C9C`.
- `0x18F7..0x2034` (1,853 bytes): `-S` COM runtime `0x0F13..0x1650`.
- `0x21E2..0x244E` (620 bytes): `-S` COM runtime `0x17FE..0x1A6A`.
- `0x2454..0x2488` (52 bytes): `-S` COM runtime `0x1A70..0x1AA4`, ending
  immediately before the accepted `-G` child.

These intervals remain deliberately `unknown`; the ownership correction does
not assert that every byte is executable code. The resident tail still needs
its own CODE/DATA/INIT/BSS boundary review.

Focused checks: `python3 scripts/ownership.py --check`,
`python3 scripts/replay_zun_outer.py --check`,
`python3 scripts/replay_zun_dispatcher.py --check`,
`python3 scripts/replay_zun_adpcm.py --check`,
`python3 scripts/replay_zun_interrupt.py --check`,
`python3 scripts/replay_zun_gaiji.py --check`,
`python3 scripts/replay_zun_memory.py --check`,
`python3 scripts/replay_zun_resdata.py --check`,
`python3 scripts/replay_zun_file_native.py --check`, and
`python3 scripts/replay_zun_crt.py --check`, and
`python3 scripts/review_zun_nearheap.py --check`. No full cold replay is needed
for these bounded ownership/vendor-object checks.
