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

The corrected ZUN view has exactly **3,874 unknown bytes**, in three intervals:

- `0x0D47..0x0D49` (2 bytes): the original writable CRT CS: runtime slot; it is
  intentionally not initialized or credited.
- `0x13BA..0x2034` (3,194 bytes): `-S` COM runtime addresses `0x09D6..0x1650`.
- `0x21E2..0x2488` (678 bytes): the tail of `-S`, COM runtime addresses
  `0x17FE..0x1AA4`, ending immediately before the accepted `-G` child.

These remaining intervals are deliberately still `unknown`; the ownership
correction does not assert that every byte is executable code. In particular,
the 3,194-byte resident interval needs procedure-by-procedure source mapping,
and the 678-byte tail needs its own CODE/DATA/INIT/BSS boundary review.

Focused checks: `python3 scripts/ownership.py --check`,
`python3 scripts/replay_zun_outer.py --check`,
`python3 scripts/replay_zun_dispatcher.py --check`,
`python3 scripts/replay_zun_adpcm.py --check`,
`python3 scripts/replay_zun_interrupt.py --check`,
`python3 scripts/replay_zun_gaiji.py --check`,
`python3 scripts/replay_zun_memory.py --check`,
`python3 scripts/replay_zun_resdata.py --check`,
`python3 scripts/replay_zun_file_native.py --check`, and
`python3 scripts/replay_zun_crt.py --check`. No full cold replay is needed for
this ownership-only correction.
