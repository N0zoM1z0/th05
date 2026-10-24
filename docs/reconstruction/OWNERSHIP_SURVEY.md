# TH05 ownership survey

This survey records the pinned targets and existing calibration
outputs, recorded on 2026-10-24. **The authored-byte denominator is still
unreviewed.** None of the candidates below changes progress, acceptance or
exclusion ledgers. Exact vendor-byte observations are not authored-source credit.

## Coordinate systems and complete outer bounds

Ranges below are half-open. MAIN addresses are offsets in its unrelocated MZ
load module; add `0xFC0` for original-file offsets, or `0x10000` for physical
addresses at load segment `1000`. ZUN ranges instead use original COM file
offsets; each embedded program has its own PSP-biased runtime coordinates.

| Artifact | Original bytes | Header | Observed payload bytes | Relocations | Payload method |
| --- | ---: | ---: | ---: | ---: | --- |
| MAIN | 149990 | 4032 | 145958 | 998 | Plain MZ |
| OP | 44450 | 32 | 77798 | 952 | Target-owned DIET decoder |
| MAINE | 44321 | 32 | 77396 | 667 | Target-owned DIET decoder |
| ZUN | 18116 | COM | 18116 | 0 | Plain COM containing nested programs |

The decoded observations under `.analysis/decoded/*/receipt.json` bind all four
payload digests; the current `payload.bin` files were rehashed in this survey.
OP/MAINE receipts record two distinct load segments, identical decoded bytes and
ordered relocation streams, and restored entry/stack state. No unpacking or
emulation was rerun for this survey.

The decoded carriers total 319268 initialized bytes. This is an observation
universe, **not an authored-code denominator**. Do not add packed OP/MAINE bytes
to their decoded bytes, or extracted ZUN members to their containing ZUN bytes.
Packing, headers, wrapper metadata, asset data and unknown ownership need their
own classifications. Unknown spans must remain visible and conservatively
included in any provisional coverage bound.

## MAIN: evidence-ready vendor candidates

Existing private calibration inputs:

- `.analysis/builds/main-calibration-b/source/bin/th05/main.exe`:
  `630b909739501bab6a9ef2c2b65e517332277c8ea66895af2ee4ba9d3e04d380`.
- Its `source/obj/th05/main.map`:
  `e2092c37785d852420f84f9830cbcc82dcd5157696b348c329fb1e52a15bbed3`.
- Pinned vendor `CL.LIB`:
  `7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7`.
- `MATHL.LIB`:
  `608a4d9eb16115a35c81ccd4c8751758aee8e08ccb3f25606cc9edcae4dbe8d7`.
- `EMU.LIB`:
  `e702f1f5dc95d61bdb1689af746d69ac5e303e38ebf77175cd6fd600eb3edc74`.

TH03's `scripts/lib/borland_library.py:library_members` validates the library
record framing, ordinary member checksums, A3 member names, padding and directory
bounds without invoking TLIB. It recognizes 893 CL, 77 MATHL and seven EMU
members. Matching these member names against the existing detailed linker MAP
produces the following **33 candidate vendor CODE contributions / 4949 bytes**.
Each complete MAP contribution matches MAIN at the same load offset, with raw
byte equality, identical ordered relative MZ fixups and a unique byte occurrence
in the target. All are CL.LIB members; this does not classify other functions
from their names alone.

| MAIN load range | Bytes | Vendor member |
| --- | ---: | --- |
| `4603–4640` | 61 | `_stpcpy` |
| `4640–4654` | 20 | `abort` |
| `4685–469B` | 22 | `del` |
| `469B–46B1` | 22 | `delarray` |
| `46B1–481E` | 365 | `dosenv` |
| `481E–484E` | 48 | `dosgdriv` |
| `4922–494A` | 40 | `getvect` |
| `494A–49F8` | 174 | `h_ldiv` |
| `49F8–4A19` | 33 | `h_llsh` |
| `4A19–4A79` | 96 | `h_padd` |
| `4ACB–4AE0` | 21 | `isatty` |
| `4DFF–4E16` | 23 | `n_lxmul` |
| `4E16–4E37` | 33 | `n_pcmp` |
| `527F–56DA` | 1115 | `farheap` |
| `5B3B–5B76` | 59 | `_access` |
| `5C46–5C67` | 33 | `chmoda` |
| `5C67–5D38` | 209 | `fflush` |
| `62B2–634F` | 157 | `getdcwd` |
| `63BF–63E7` | 40 | `memcmp` |
| `63E7–640B` | 36 | `memcpy` |
| `640B–6453` | 72 | `memset` |
| `6453–64CA` | 119 | `movmem` |
| `6774–67B3` | 63 | `strcat` |
| `67B3–67E3` | 48 | `strcmp` |
| `67E3–680C` | 41 | `strcpy` |
| `680C–684D` | 65 | `stricmp` |
| `684D–686E` | 33 | `strlen` |
| `686E–68BB` | 77 | `strrchr` |
| `6ABB–6CBC` | 513 | `xalloc` |
| `A1C5–A2FC` | 311 | `doscmd` |
| `A2FC–A6A1` | 933 | `exec` |
| `A6A1–A6C4` | 35 | `execl` |
| `A6C4–A6E4` | 32 | `setblock` |

`xalloc` has ordered relative fixup offsets
`[489,362,346,157,136,115,101,93]` in both images. The other 32 candidate
contributions have no MZ fixups. Candidate full-member boundaries still need a
durable ownership review before any exclusion is accepted. These observations
do not certify the complete calibration executable, which differs from MAIN.

Reproduce the table without compiling or running game code, from the TH05 root:

```sh
python3 - <<'PY'
from pathlib import Path
import importlib.util, re, sys
sys.path.insert(0, 'scripts')
from lib.pc98 import parse_mz, digest_file
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from lib.unit_oracle import compare_unit
root = Path.cwd()
reader = root.parents[1] / 'th03-reconstruction/th03/scripts/lib/borland_library.py'
spec = importlib.util.spec_from_file_location('vendor_members', reader)
vendor = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = vendor
spec.loader.exec_module(vendor)
lib = root / '.analysis/toolchain/installed/tc40j/LIB/CL.LIB'
assert digest_file(lib) == '7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7'
names = {m.name.casefold() for m in vendor.library_members(lib.read_bytes())}
artifact = find_artifact(load_target_manifest(root/'config/targets.toml'), 'th05-main')
target = parse_mz(read_verified_artifact(root, artifact))
base = Path('.analysis/builds/main-calibration-b/source')
assert digest_file(base/'bin/th05/main.exe') == '630b909739501bab6a9ef2c2b65e517332277c8ea66895af2ee4ba9d3e04d380'
assert digest_file(base/'obj/th05/main.map') == 'e2092c37785d852420f84f9830cbcc82dcd5157696b348c329fb1e52a15bbed3'
candidate = parse_mz((base / 'bin/th05/main.exe').read_bytes())
pattern = re.compile(r'\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+'
                     r'C=CODE\s+S=\S+\s+G=\S+\s+M=(\S+)', re.I)
count = total = 0
for line in (base / 'obj/th05/main.map').read_text(encoding='cp437').splitlines():
    m = pattern.match(line)
    if not m or m[4].casefold() not in names:
        continue
    start, size = int(m[1], 16)*16 + int(m[2], 16), int(m[3], 16)
    if not size or not compare_unit(target, candidate, start, start, size)['exact']:
        continue
    body = target.program_image[start:start+size]
    assert target.program_image.find(body) == start
    assert target.program_image.find(body, start+1) == -1
    print(f'{start:05X}-{start+size:05X} {size:4d} {m[4]}')
    count, total = count+1, total+size
assert (count, total) == (33, 4949)
PY
```

## MAIN: boundaries that remain candidates

The observed startup DGROUP segment is `209D`, versus `209E` in the calibration
MAP. The entire range `[209D0,23A26)` cannot therefore be called a reviewed data
or BSS exclusion from the candidate MAP alone.

- Calibration `c0.ASM/_TEXT` owns `[00000,00271)`. Target and candidate share
  four relocation sites (`1,5E,A5,13E`), but 15 byte positions differ. This
  range is a compiler-startup candidate, not a raw exact match. Pinned
  `C0L.OBJ` SHA-256 is
  `09fe156e5dceb4afa30235e8d9cf7a17a40a91ee646babe16b3286731eb429a2`.
- Its candidate DATA extent is 144 bytes at `209E0`. Target bytes at `209D0`
  differ at relative byte `82`; the target contains the Borland copyright and
  divide-error strings. These are useful compiler-data anchors, not a complete
  accepted DATA ownership partition.
- `_TEXT` mixes master.lib includes, game-specific MPN code, PF support and
  vendor library contributions. The root ASM's `[0272,45E8)` contribution is
  therefore not a single third-party library exclusion.
- Calibration `_TEXTC` comprises `ctor2`, `ctor3`, and `strings` at
  `[1FD8D,209D5)`. Their target positions and complete linked fixups have not
  been established here.
- The candidate MAP places `_DATA`, `_INIT_`, `_EXIT_`, `_BSS` and stack in
  distinct classes. Actual file-backed tail bytes must be partitioned against
  the original, rather than dropping everything called BSS by a candidate.

The pinned reference ASM is source-routing evidence. Its MAIN IDA header gives
MD5 `6a9ab51c7215e3d9ca580cd9f04f4d12` and loaded length `23A48`, whereas our
MAIN MD5 is `952585e02435c3b3b111975a78b05983` and its load length is `23A26`.
The `22`-byte difference and the original/candidate DGROUP difference prohibit
blind transfer of reference labels and segment boundaries.

Useful next parsers are TH04's
`scripts/boundary_review/build_function_boundary_ledger.py` detailed MAP reader
and `export_tasm_function_boundaries.py:listing_procedures`. A later single
bounded TASM listing can attribute included master.lib procedures to complete
source extents. Neither procedure names nor lengths inferred from the next
symbol suffice for an accepted target boundary.

## ZUN: complete physical partition, origin still unreviewed

`python3 scripts/inspect_launcher.py` replays the dependency-free container
parser against pinned ZUN and writes
`.analysis/launcher/th05-zun/receipt.json`. It does not execute instructions or
export proprietary members into the public tree. It validates outer offsets
and jump, inner directory names and 33 entry slots, monotonic complete member
partition, the transfer call, the eight-byte copy helper and full-file SHA-256.
Per-span checksums in the receipt are observer-computed SHA-256 values; no
original member-checksum field has been established.

| Original COM file range | Bytes | Physical role |
| --- | ---: | --- |
| `0000–0027` | 39 | COMCSTM header, pointers, timestamp, copyright |
| `0027–012F` | 264 | Usage text |
| `012F–020E` | 223 | Inner COM dispatcher stub |
| `020E–0355` | 327 | Count, 32 names, 33 offsets, transfer call |
| `0355–06F3` | 926 | `-O` embedded COM |
| `06F3–0AE4` | 1009 | `-I` embedded COM |
| `0AE4–2488` | 6564 | `-S` embedded COM |
| `2488–4541` | 8377 | `-G` embedded COM |
| `4541–4678` | 311 | `-M` embedded COM |
| `4678–4680` | 8 | Inner copy/transfer helper |
| `4680–46C4` | 68 | Outer COMCSTM wrapper code |

The inner table stores its own runtime starts, not outer-file offsets. Add
`12F` to each inner file offset to recover the table above. The outer header
records inner size `4551`, usage length `108`, and timestamp `2579AF64`; its
initial jump reaches outer offset `4680` exactly.

Three complete embedded payload MD5s agree with the reference ASM's original
input identity, strengthening those source-routing links:

| Member | MD5 | Reference |
| --- | --- | --- |
| `-I` | `e22366913b7288f2ec82e280b386c86d` | `th05_zuninit.asm` |
| `-G` | `7c8f4cab7f06b9a218e838d50bb4e314` | `th05_gjinit.asm` |
| `-M` | `5e401a5cd3d8d42dc67130359c42a7cf` | `th05_memchk.asm` |

The ZUNINIT reference header says `th04/ZUN.COM`, but its exact MD5 identifies
our TH05 `-I` payload. The `-G` source includes font bitmap data, and `-I/-M`
include messages. Whole member size is consequently not an instruction-byte
count. COMCSTM's third-party copyright and `Pipeline/{comcstm.c,cstmstub.asm}`
route packaging ownership investigation; source origin of the inner dispatcher
and helper remains separately reviewable. `-O` and `-S` ownership and internal
code/data boundaries remain open.

## Next ownership work

1. Create a gapless artifact-local interval ledger whose initial state is
   unknown; keep origin, boundary confidence, source presence and acceptance
   separate. Split physical bytes only with retained complete-boundary evidence.
2. Review the 33 vendor candidates against their actual pinned library members
   and complete MAP contributions before accepting exclusions. Bind startup
   externals rather than normalizing away its mismatches.
3. Use bounded source/listing and target comparisons for the master.lib prefix,
   compiler tails and DGROUP. Keep interleaved game helpers and library data
   separate. Reuse the already accepted player/tuning boundaries without
   extrapolating to surrounding functions.
4. Establish independent OP/MAINE decoded ownership partitions. Their packed
   streams and decoder stubs are separate packaging surfaces with different
   coordinates; metadata and unknown decoded bytes must not disappear.
5. Subdivide ZUN members into code, initialized data and genuine handwritten
   assembly candidates. Preserve embedded asset data and unknown ownership.
6. Publish the final scope explicitly: instruction bytes, compared extents and
   initialized game-owned data are different quantities. Until the entire
   intended scope is reviewed, retain an unmeasured denominator or a clearly
   labelled conservative bound; never calculate 98% from accepted units alone.

## Gapless observation inventory

[`resources/ownership.json`](../../resources/ownership.json) now covers every
byte of MAIN's load module, the retained OP/MAINE decoded load modules, and
the entire outer ZUN COM: 319,268 bytes without gaps or overlaps. It is an
observation universe, not a final authored denominator. Original MZ headers
and the packed OP/MAINE streams have separate container coordinates and are
not added to decoded payloads. Embedded ZUN children are not counted twice.

The inventory projects only source-current accepted C++ intervals and their
explicit switch-table/padding classifications. All remaining intervals stay
`unknown`, including vendor candidates, assets, runtime data and ASM whose
global ownership is still unreviewed. In particular, the separately accepted
ZUN memory child retains its unreviewed global ownership status here. No
vendor candidate is excluded merely because a reference name or shape matches.
Both the authored denominator and percentage remain null.

`python3 scripts/ownership.py --write` regenerates the inventory after progress
changes. Public CI checks its coverage, exact agreement with the acceptance
ledgers and source freshness without private targets. Add `--verify-targets`
to rehash all cached comparison views against their pins; this performs no
decoding, emulation or compilation. Unknown intervals remain available for
later explicit library/ASM/initialized-data ownership reviews.
