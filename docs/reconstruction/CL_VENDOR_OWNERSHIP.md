# Reviewed CL.LIB ownership

31 complete contributions are classified as third-party library CODE by
`config/reviewed_vendor_units.json`, bound to the exact public evidence hash.
This grants no authored source credit. The global denominator remains unreviewed.

31 complete MAIN library CODE contributions / 2901 bytes have a retained native
proof from the actual pinned CL.LIB member records. CODE is an OMF class; this
does not classify every byte as an instruction. The existing observation universe
is unchanged; every remaining unreviewed span stays unknown.

Whole-library SHA-256: `7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7`.
The enclosing library parser checks ordinary record checksums, member identity,
framing and padding. Every reviewed CODE SEGDEF is covered exactly once by
LEDATA, with no unwritten byte or unsupported byte-transform record. Its full
size and segment match one actual detailed calibration MAP contribution.

The native verifier reconstructs every CODE byte from that member, resolving
each supported FIXUPP to real MAP/library PUBDEF symbols and frame/group bases.
It checks complete reconstructed bytes against the pinned calibration EXE and
the original target, unique whole-extent occurrence, and original ordered MZ
fixups. Fifteen members require actual relocation or the observed five-byte
same-segment far-call rewrite (`NOP; PUSH CS; CALL rel16`); this is calculated
from the real callee address rather than treating fixup fields as wildcards.
The other sixteen members, 866 bytes, independently match their unlinked literal
CODE with zero FIXUPP; a second native verifier confirms that subset.

Full per-member record hashes, exact LEDATA spans, resolved FIXUPP actions and
ordered relocation evidence are in [vendor_ownership.json](../../config/vendor_ownership.json).

| Original MAIN load range | Bytes | Actual pinned CL member | FIXUPP actions |
| --- | ---: | --- | ---: |
| `04603..04640` | 61 | `_stpcpy` | 2 |
| `04640..04654` | 20 | `abort` | 2 |
| `04685..0469B` | 22 | `del` | 1 |
| `0469B..046B1` | 22 | `delarray` | 1 |
| `046B1..0481E` | 365 | `dosenv` | 5 |
| `0481E..0484E` | 48 | `dosgdriv` | 0 |
| `04922..0494A` | 40 | `getvect` | 0 |
| `0494A..049F8` | 174 | `h_ldiv` | 0 |
| `049F8..04A19` | 33 | `h_llsh` | 0 |
| `04A19..04A79` | 96 | `h_padd` | 0 |
| `04ACB..04AE0` | 21 | `isatty` | 0 |
| `04DFF..04E16` | 23 | `n_lxmul` | 0 |
| `04E16..04E37` | 33 | `n_pcmp` | 0 |
| `05B3B..05B76` | 59 | `_access` | 2 |
| `05C46..05C67` | 33 | `chmoda` | 1 |
| `05C67..05D38` | 209 | `fflush` | 2 |
| `062B2..0634F` | 157 | `getdcwd` | 5 |
| `063BF..063E7` | 40 | `memcmp` | 0 |
| `063E7..0640B` | 36 | `memcpy` | 0 |
| `0640B..06453` | 72 | `memset` | 0 |
| `06453..064CA` | 119 | `movmem` | 1 |
| `06774..067B3` | 63 | `strcat` | 0 |
| `067B3..067E3` | 48 | `strcmp` | 0 |
| `067E3..0680C` | 41 | `strcpy` | 0 |
| `0680C..0684D` | 65 | `stricmp` | 0 |
| `0684D..0686E` | 33 | `strlen` | 0 |
| `0686E..068BB` | 77 | `strrchr` | 1 |
| `06ABB..06CBC` | 513 | `xalloc` | 24 |
| `0A1C5..0A2FC` | 311 | `doscmd` | 5 |
| `0A6A1..0A6C4` | 35 | `execl` | 2 |
| `0A6C4..0A6E4` | 32 | `setblock` | 1 |

Review commands (no Wine, compiler or game execution):

```sh
python3 scripts/review_vendor.py --check
python3 scripts/review_vendor.py --structural-check
python3 scripts/ownership.py --check --verify-targets
python3 -m unittest discover -s tests -p test_vendor_review.py
```

The first command replays the actual private pinned library/MAP/MZ inputs.
The structural check needs only public files and does not claim to replay
private bytes. Synthetic tests reject malformed records, missing coverage,
changed bindings, unsupported transformations and reversed fixup order. The
public proof pins the verifier, library parser and toolchain manifest. The
separate review decision explicitly selects all 31 proven members; adding an
unreviewed or deferred member fails closed in the inventory.

Two whole candidates, 2048 bytes, remain **deferred**, even though their linked
calibration bytes equal the original:

- `farheap [0527F,056DA)`: LEDATA leaves original `[05285,0528B)` (six bytes)
  unwritten inside its complete CODE SEGDEF. Both images contain zero there.
- `exec [0A2FC,0A6A1)`: its 255-byte LIDATA expands exactly to the calibration
  prefix, but `[0A460,0A462)` remains unwritten (two zero bytes in both images).

No implicit zero-fill exemption or reservation-ownership rule has been adopted.
The exact reserved spans need explicit review of linker/object allocation
semantics before either complete member can be excluded. This review does not cover startup, vendor DATA/BSS, master.lib, nearby gaps or any other
artifact. Names and approximate instruction shape alone are never sufficient.

## Independently reviewed initialized DATA

[CL DATA ownership](CL_DATA_OWNERSHIP.md) separately reviews24 complete DATA
contributions /1857 bytes across MAIN, OP and MAINE. These receive zero authored
credit and do not transfer CODE acceptance or establish the global denominator.
The ordinary relocation-free DATA lane preserves ambiguous, relocated,
incomplete and all other unreviewed extents as unknown.
