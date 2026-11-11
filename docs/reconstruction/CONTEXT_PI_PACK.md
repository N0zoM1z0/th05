# Original Master GRAPH_PI_LOAD_PACK in OP and MAINE

The complete Master 0.23 **1,512-byte PI/RLE image decoder** is now
source-exact in both TH05 OP and MAINE, for **3,024 previously unknown
native CODE bytes**. The source is the original author's `GRPPILOD.ASM`
and the actual preserved ReC98 adaptation built by TASM32 into the
original monolithic OP/MAINE assembler objects.

| Artifact | Original full CODE extent | Native CODE | Actual OMF FIXUPP | MZ segment relocations |
| --- | --- | ---: | ---: | --- |
| OP | `1354..193C` | 1,512 B | 5 | `+220, +309, +1192` |
| MAINE | `1446..1A2E` | 1,512 B | 5 | `+220, +309, +1192` |

The original upstream procedure and the maintained source have **all
438 effective source operations in the same order**, after reviewing
exactly one FAR parameter `_push` expansion, seven logically equivalent
long-branch trampolines, explicit DS segment qualifiers, one renamed EOF
constant, and historical `NOPCALL` spelling. The original and native
complete procedure SHA-256 digests and original Master archive are bound
in the [native proof](../../config/context_pi_pack.json).

Both real TASM OMF objects supply complete gapless CODE LEDATA and exactly
five original ordered FIXUPP records: two offsets targeting the module's
actual `_DATA` contribution (relative to DGROUP), and three segment words
targeting actual DGROUP. The pinned native TLINK MAPs establish **different
data contribution offsets**: OP `04D2h` and MAINE `00BCh`.

The original OP code matches the retained calibration throughout. MAINE
differs at three genuine segment words because its **original DGROUP
paragraph is 1011h**, whereas the calibration's is **1010h**. Applying
these group bases to the unchanged original TASM OMF yields both original
1,512-byte functions byte for byte. The three original MZ fixups preserve
their native order. No placeholder bytes, target-byte copies, or modified
machine instructions are used.

The [explicit review decision](../../config/reviewed_context_pi_pack.json)
adopts only these two complete CODE ranges. The other Master functions
and intervening unowned bytes remain unclassified. They are source-backed
third-party Master assembly, **zero game-authored C++ credit**.

```sh
python3 scripts/review_context_pi_pack.py --check
python3 scripts/review_context_pi_pack.py --structural-check
python3 scripts/ownership.py --check
```
