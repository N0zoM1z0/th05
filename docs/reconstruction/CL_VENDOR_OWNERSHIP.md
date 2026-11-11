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

Two additional large CODE members were **deferred from this gapless-LEDATA
lane** as whole 2,048-byte contributions. Their real Borland OMF records
contain runtime-write state reservations, not original executable bytes:

- `farheap [0527F,056DA)` (1,115 bytes): 1,109 bytes are covered by original
  LEDATA records; `[05285,0528B)` is an unwritten six-byte `CS:` state bank,
  independently read and written by native far-heap operations.
- `exec [0A2FC,0A6A1)` (933 bytes): 931 bytes are covered by original LIDATA
  and LEDATA records, including a real 255-byte zero-initialized CODE buffer;
  `[0A460,0A462)` is an unwritten two-byte `CS:` state slot, updated by
  the native DOS exec code at `0A471` and referenced later.

These two are now separately reviewed with the original complete CL.LIB member
records, complete target/calibration byte identity, all 70 ordered source
FIXUPP resolutions, actual LIDATA expansion, and unique native CODE
boundaries. The **separate** [reserved vendor proof](../../config/vendor_reserved_ownership.json),
[explicit adoption](../../config/reviewed_vendor_reserved.json), and
[verifier](../../scripts/review_vendor_reserved.py) pin precisely the four
source-written intervals totaling **2,040 vendor bytes**. The eight
unwritten bytes **remain `unknown` in the ownership partition**, with zero
source credit: *no implicit linker zero-fill ownership exemption has been
adopted*. This additional adoption does not rewrite or enlarge the original
31-member, 2,901-byte gapless proof.

To check the source-current record without private inputs, or verify the
actual two original vendor members without recompiling the game:

```sh
python3 scripts/review_vendor_reserved.py --structural-check
python3 scripts/review_vendor_reserved.py --check
```

All of this is third-party CODE-segment provenance. A CODE SEGDEF includes
noninstruction buffers (notably the 255-byte LIDATA); it does not establish
game-authored source or a denominator. Startup, vendor DATA/BSS, Master,
nearby gaps and other artifacts remain independent.

## Independently reviewed initialized DATA

[CL DATA ownership](CL_DATA_OWNERSHIP.md) separately reviews24 complete DATA
contributions /1857 bytes across MAIN, OP and MAINE. These receive zero authored
credit and do not transfer CODE acceptance or establish the global denominator.
The ordinary relocation-free DATA lane preserves ambiguous, relocated,
incomplete and all other unreviewed extents as unknown.
