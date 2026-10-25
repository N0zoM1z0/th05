# Laser geometry, rendering and collision assembly

Four complete native procedures form one 348-byte contribution in MAIN,
CS 0AE1 / DS 209D. They are explicitly reviewed as original-assembly
reconstruction, independently of the C/C++ ledger and global denominator.

| Procedure | Complete native load range | Bytes | Private/public contract |
| --- | --- | ---: | --- |
| Vector at center | D5C2..D5FA | 56 | SS:BP center, BX length, CX angle, SS:DI output |
| Line to pixels | D5FA..D626 | 44 | SS:DI point, SS:BX endpoint, displacement at SS:BP+4 |
| Render ray | D626..D6C6 | 160 | Near Pascal const coords reference; word result AX |
| Hit test | D6C6..D71E | 88 | Near Pascal full Laser reference; RET 2 |

The complete contribution has 127 instructions and no NOPs, padding, tables,
runtime placeholders, inert branches, initialized DATA or assets. Its original
ordered MZ relocation sites are exactly [228,245], both genuine far calls inside
the ray procedure. Every direct branch remains within its complete native
procedure. Existing accepted laser update/render callers independently establish
the actual near frame, entry addresses and argument types.

## Origin and maintained source

Pinned ReC98 b6ba5b0a's `th05/main/bullet/laser_rh.cpp` supplies the geometric
algorithms and documents the unusual private register protocol. Its register
templates, codegen helpers and opcode emits are not authored C++ recovery and
are not used as such. This maintained source instead expresses signed polar
components, point conversion, stack overlays, clipped rendering and spaced hit
boxes through named semantic ASM macros, labels and complete typed layouts.
It contains no target-byte arrays, numeric local CODE addresses, padding,
compiler-body conversion or copied instruction listing.

Native evidence supports deliberate assembly-level design: ray BP moves from
its ordinary frame F to F-4, then F-12, then back to F; private helpers read and
write the caller's SS stack through BP/DI/BX. The line helper's displacement
depends on BP+4. Hit testing deliberately reverses the usual SI/DI save order.
These interacting protocols, rather than an inability to match natural C++,
support the explicit original-ASM classification. No particular native subspan
has positive compiler-generated provenance in the inspected evidence. Standard
ENTER/LEAVE alone establish neither origin. Original assembly-heavy mixed C/ASM
source remains possible; literal historical source and original assembler
identity are unproved. No compiler-generated owner is promoted by this review.

A bounded search of all 653 members of the pinned master0.23 source archive
found no function/type/private-alias matches. A broader English BP/geometry
search had two hits in AJSTART.ASM, independently reviewed as conventional
joystick-calibration stack arguments. This is not an exhaustive renamed-body
or dataflow search and does not exclude every historical vendor derivation.

## Preserved arithmetic and ABI

The unchanged canonical `laser.hpp`, `geometry.hpp` and `abi.hpp` are semantic
inputs. The maintained ASM include retains full point4, motion12, coords10,
Laser24, the complete flag domain, width/active-age unions and real trailing
unused fields. Ray's 32-byte scratch union retains all eight construction
points, the four corner overlay and the eight-point clipping buffer; hit's
scratch is eight bytes. No entity or stack object is shortened for matching.

The vector helper sign-extends signed BX and each signed word table sample,
multiplies in 32 bits and arithmetic-shifts by eight. Adding the center and
storing the coordinate wrap at 16 bits; AX returns Y. BP/BX/CX/DI are preserved,
SI is saved/restored, and EAX/EDX/flags are clobbered. The line helper preserves
BP/BX/CX/SI/DI and segments; it uses word wrapping and arithmetic subpixel
conversion, changing AX/DX/flags while their upper halves remain untouched.

Ray uses paired ENTER 32 / LEAVE frames and passes two genuine SS:DI far
pointers to clipping: six stack words for four logical parameters, followed
by three words for the two polygon parameters. The native providers at
0000:139E and 0000:18B4 use Pascal cleanup of 12 and 6 bytes. They preserve
DI/SI/SS and may change ES; no DS=SS assumption replaces the explicit pointer
segments. Negative clipping results preserve the original four-corner fallback.
Both outer procedures preserve BP/SI/DI and remove their word reference argument.

Hit testing retains signed end-to-start stepping, strict unsigned overlap tests,
12-by-12 pixel boxes at 16-pixel intervals and the resulting four-pixel gaps.
It writes the foreign player-hit byte; it does not close those gameplay gaps.
Neither local geometry helper changes DF or segment registers. Foreign sine/
cosine tables and player state are addresses only: DS:041C,049C,36D2,36F3.

The source exports the actual compiler EXTDEF aliases
`@LASER_RENDER_RAY$QRX14LASER_COORDS_T` and `@LASER_HITTEST$QR5LASER`, verified
in actual assembler PUBDEF records at relative 100 and 260. TLINK demangles
them; the MAP gate checks both exact demangled signatures and ordinary entry
labels. These aliases add no functions or bytes. Symbol-only binders preserve
the actual segment divisions and contain no initialized payload or artificial
stack; every ORG is below 64 KiB.

## Exact gates and retained evidence

`.analysis/laser-rh-native/replay-e/receipt.json` passes two fresh deterministic
whole TASM producers, complete ordinary CODE SEGDEF/LEDATA integrity, actual
MAP/public/CS/DGROUP readback, all raw bytes and literal ordered relocations.
Its own assembled hit-step mutation from 16 to 15 changes collision sampling
and is rejected across the same complete scope and original fixup stream.
Unchanged installed tool execution proofs and all prior accepted source owners
are reused after identity checks. No C/C++ dependency changed or needed replay.

Setup attempts remain private and unaccepted. Replay-a stopped before source
assembly on missing binder CS context; replay-b stopped on a full-union width
operand selection. Replay-c stopped after its first producer's size check:
manual frame teardown was four bytes longer than the independently reviewed
paired LEAVE operations. Replay-d had correct complete size but stopped on
MAP names: TLINK prints the actual exported aliases as demangled signatures.
These supported context/source/gate corrections neither patch output bytes nor
mask comparisons; no failed producer was relabelled accepted.

Independent private reports are `.analysis/laser-rh-native-review.json`
(SHA-256 `7621a031d0fb4a04a9416573bdc54fcba6533c73708906c0cca5b5c067dc8b70`)
and `.analysis/laser-rh-maintained-source-review.json`
(SHA-256 `71b671796a6a0c3d4bfb0b5e6f36464d2ac3f221427dbddfda8cad0a118a10a9`).
The native byte/boundary proof is pinned in `config/asm_families.toml`.
The explicit ownership decision pins this note and the accepted record in
`config/reviewed_asm_families.json`. Whole-program linkage/packing and the
98% objective remain open.
