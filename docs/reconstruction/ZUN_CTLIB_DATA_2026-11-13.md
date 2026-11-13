# ZUN `-S` resident CT.LIB DATA/INITDATA tail (2026-11-13)

The final 52 file-backed bytes of the resident `-S` child, COM
`[0x1A70, 0x1AA4)`, are now matched to seven complete original Borland
Turbo C++ 4.0 `CT.LIB` OMF segments. The review classifies **42 source-written
initialized bytes** and **10 zero-filled bytes inside the original `setargv`
DATA SEGDEF**. No bytes in this 52-byte interval remain unknown.

| Member / segment | COM extent | SEGDEF bytes | LEDATA bytes | Classification |
| --- | ---: | ---: | ---: | --- |
| `_pathops:2` `_DATA` | `1A70..1A80` | 16 | 16 | initialized DATA |
| `setvbuf:2` `_DATA` | `1A80..1A84` | 4 | 4 | initialized DATA |
| `sysnerr:2` `_DATA` | `1A84..1A86` | 2 | 2 | initialized DATA |
| `setargv:2` `_DATA` | `1A86..1A94` | 14 | 4 | 4 initialized + 10 uninitialized |
| `setupio:4` `_INIT_` | `1A94..1A9A` | 6 | 6 | initialized INITDATA |
| `_pathops:4` `_INIT_` | `1A9A..1AA0` | 6 | 6 | initialized INITDATA |
| `setargv:3` `_INIT_` | `1AA0..1AA6` | 6 | 4 | 4 initialized; final 2 bytes beyond file |
| **File-backed total** | | | **42** | **42 initialized + 10 uninitialized** |

The three INITDATA segment bases are pinned by original OMF relocation
fields: `setupio:4` resolves to `0x1A94`, `_pathops:4` to `0x1A9A`, and
`setargv:3` to `0x1AA0`. The `_DATA` bases for `_pathops`, `setvbuf`, and
`setargv` are independently anchored by the already accepted CODE relocations;
`sysnerr:2` is anchored by `ioerror`'s accepted reference to `__sys_nerr`.
The `setargv` DATA SEGDEF is 14 bytes but has only a four-byte LEDATA record;
the ten-byte unwritten suffix is zero in the original target and is classified
as uninitialized vendor storage, not initialized DATA or code.

The verifier checks the complete original OMF member identities, segment and
group layouts, ordered LEDATA/PUBDEF/EXTDEF/FIXUPP metadata, exact segment
bases, and every file-backed target byte. Relocated words must resolve to the
independently accepted public/segment addresses. It rejects a mutated ordinary
DATA byte and a mutated relocation word. The 16-bit fixups in INITDATA are
applied exactly; no compiler replay is involved.

The last two bytes of `setargv:3` INITDATA are at COM `0x1AA4..0x1AA6`,
outside the `-S` file-backed child extent, and are not part of this claim.
The separate C0T INIT/BSS table beyond the accepted OMF LEDATA spans is not
claimed. No zero-filled extent is inferred solely from its contents.

Focused reproduction:

```sh
python3 scripts/review_zun_ctlib_data.py --check
python3 scripts/review_zun_ownership.py --check
python3 scripts/ownership.py --check
```

Acceptance evidence is `config/zun_ctlib_data_acceptance.json`, generated
from `config/zun_ctlib_data.toml`. All 52 bytes remain vendor-owned with zero
authored-code credit.
