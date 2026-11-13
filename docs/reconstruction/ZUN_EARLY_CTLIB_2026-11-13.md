# ZUN `-S` early Borland CT.LIB code partition (2026-11-13)

The previously unknown `-S` COM runtime interval `0x09D6..0x0C1D` is now
fully identified as nine complete original Borland Turbo C++ 4.0 `CT.LIB`
`_TEXT` segments. Their target COM extents are contiguous, non-overlapping,
and close the entire 583-byte interval:

| Original CT.LIB member | COM start | COM end | CODE bytes | 16-bit OMF fixups |
| --- | ---: | ---: | ---: | ---: |
| `_abort` | `09D6` | `09EB` | 21 | 3 |
| `atexit` | `09EB` | `0A13` | 40 | 4 |
| `errormsg` | `0A13` | `0A32` | 31 | 3 |
| `exit` | `0A32` | `0AD2` | 160 | 11 |
| `ioerror` | `0AD2` | `0B24` | 82 | 5 |
| `isatty` | `0B24` | `0B39` | 21 | 0 |
| `lseek` | `0B39` | `0B66` | 45 | 2 |
| `n_scopy` | `0B66` | `0B82` | 28 | 0 |
| `setupio` | `0B82` | `0C1D` | 155 | 17 |
| **Total** | | | **583** | **45** |

Every member is reconstructed from its original OMF records in the pinned
`CT.LIB`; no target bytes are copied into the source object. The review checks
complete `_TEXT` SEGDEF/LEDATA extents, ordered PUBDEF and EXTDEF tables,
DGROUP membership, original FIXUPP record identity and every relocation
site. All 493 non-relocation bytes compare verbatim. The 45 two-byte fields
are re-applied with their original OMF frame/target semantics and resolve to
18 separately checked public symbols across these CT.LIB members and the
original `C0T.OBJ`.

Notable cross-module edges include `_abort` to `___ErrorMessage`/`__exit`,
`exit` to the CRT termination callbacks and the `atexit` state, `errormsg` to
`__rtl_write`/`__streams`/`_strlen`, `lseek` to `__openfd`/`__IOERROR`, and
`setupio` to `__streams`/`__nfile`/`__openfd`/`_isatty`/`_setvbuf`. These are
resolved against original public boundaries rather than inferred from symbol
names alone.

The verifier also rejects a mutated non-relocation instruction and a mutated
resolved relocation word. It is a vendor-origin ownership proof, not authored
TH05 credit. DATA, INITDATA, BSS and any runtime-writable slots belonging to
these modules are deliberately not claimed by this CODE-only review; they
remain separate until their own physical boundaries and initialization
semantics are established.

Run the focused check with:

```sh
python3 scripts/review_zun_early_ctlib.py --check
```

Acceptance evidence is in `config/zun_early_ctlib_acceptance.json`, generated
from `config/zun_early_ctlib.toml`. The reviewed outer-file interval is
`0x13BA..0x1601`, immediately adjacent to the independently accepted `brk`
member beginning at `0x1601`.
