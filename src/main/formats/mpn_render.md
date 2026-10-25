# Complete MPN tile renderer

The complete MAIN family at 4226..4282 contains a 75-byte far tile wrapper,
one alignment NOP and a 16-byte private near plane worker. Its actual CS is
0000 and DATA frame is 209D. The following Master PFINT21 CODE-resident data
starts at 4282 and is outside this owner. All 92 bytes are compared; only the
91 non-NOP instruction bytes are candidates for separately reviewed ASM credit.
There are no tables or MZ relocations in this scope, and no owned DATA/BSS.

The semantic source uses the MPN geometry of four consecutive 16x16 planes,
two bytes per row and 128 bytes per image. A shared source cursor feeds four
calls to one row-copy worker, in B/R/G/E order. The worker advances SI by one
32-byte plane and restores the same VRAM origin in DI. The source has no
opcode arrays, literal target instruction listing, sprite/palette payloads,
loader body, foreign provider or artificial stack.

## Real interfaces and state

The far wrapper is Pascal `(left, top, image)`, with three stack words and
RETF6. The native MPN_LOAD caller at E599 pushes left/top/image and calls
0000:4226, independently confirming these offsets. The wrapper captures BX
before saving SI; it saves DI/DS only on the valid-image path. The private
worker is genuinely near and consumes AX=plane segment, DS:SI=source cursor
and DI=destination origin. That complete hidden register protocol supports a
handwritten-assembly inference; it is not an ordinary C++ helper declaration.

The image allocation segment is the word at DS3068. The inclusive image limit
is the full word at DS306A, loaded from the file header's count and unused
bytes. It must not be narrowed to an eight-bit count or replaced by a false
four-byte pointer. The unsigned image guard accepts indices through that limit.
Multiplying the index by 128 retains the original 16-bit offset wrap.

The valid path preserves DS/SI/DI/BP/SS and the far return/cleanup contract;
it leaves ES at E000. An out-of-range image returns without video writes and
preserves incoming ES/DI/DS. AX/BX/CX/DX and arithmetic flags are working state.
IF/DF are unchanged; clear DF and normal direct plane-write graphics state
are caller preconditions. Signed left/8 uses SAR. There is no coordinate
clipping, row-ring wrapping, graphics-mode setup or allocation check.

## Language and source provenance

The maintained TH04 MPN renderer supplies a semantic architecture reference,
but its different slot record, pointer layout, FS/GS/ES plane schedule and
acceptance do not transfer. Independent TH05 native boundaries, caller/worker
contracts and raw byte gates are required. No specific compiler-generated
portion was identified in this family. Historical source text and original
assembler identity remain unproved.

A bounded primary Master 0.23 investigation found no MPN identifiers in its
653 source members and inspected 14 relevant graphics/pattern bodies. OVERPUT8
is a real architectural similarity: four plane calls and y*80 arithmetic.
Its variable-size pattern format, mask handling, unsigned X shift, register
protocol and private REP workers differ. No extensive directly matching
derivative body or explicit vendor attribution like tiny16 was identified.
This supports a game-specific ASM inference while leaving historical ancestry
open; absence of a name alone proves no originality. The tiny16 renderer,
MPN loader/free/upload code and every neighboring unknown span remain outside
this decision.

The instruction NOP at relative 75 aligns the private worker. It is generated
by EVEN, compared normally and assigned zero authored credit. No instruction
bytes or data are supplied to fill any other part of the family.

Private independent origin/native review:
`.analysis/mpn-render-independent-origin-native-routing-review.json`, SHA-256
`c25fe28ee32914c1955639d52104914aac80840aa79d31ef7493921d9f5547c7`.

A separate native-only check passes 60 generated-data cases against an
independent row-address model, covering all four planes, copied zero bytes,
inclusive and high-word image limits, unsigned rejection, 16-bit index wrap,
the original caller's edge coordinates and preserved far/private ABI state.
It does not claim safety for arbitrary coordinates. Report:
`.analysis/mpn-render-native-semantic-check.json`, SHA-256
`22a5a591902ece568504989db50e65045ea36fb788227825e01cbc8d9d5bff6d`.

Exact-source acceptance and explicit ownership adoption remain separate.
C/C++ progress, images, palettes, whole-executable equality and the unreviewed
global authored denominator are not established by this family.

## Exact replay

Two fresh independent TASM producers each supply one complete 92-byte _TEXT
contribution, with full ordinary OMF/LEDATA coverage, the actual 0000:4226
entry and 209D DATA frame. All native bytes and the original empty ordered
MZ-fixup stream agree. Both source objects, binding objects, MAP and linked
MZ outputs are deterministic under the existing timestamp-aware identity
checks. The binder supplies no initialized bytes, entry or stack.

The own assembled negative changes only the worker row count from 16 to 15.
It retains the 128-byte image format, full 92-byte extent, publics, frames and
empty ordered fixup stream. Its three changed bytes at relative 79/89/90 are
rejected by the same raw oracle. All older accepted units and the successful
installed tool execution probe are reused after identity checks.

Receipt: `.analysis/asm-replays/main-mpn-render-a/receipt.json`, SHA-256
`1967ff58c3bb2510e1104373918dfb60e4f5eb0a01ba956216ea5b4bcc15eb8d`.
Prepared-source review and the explicit true-NEAR call clarification:
`.analysis/mpn-render-final-source-addendum.json`, SHA-256
`1e2b27853228a23fae41123cead99dcf5f1b06351374a3170f5273b007f560f7`.
Independent actual saved-producer review:
`.analysis/mpn-render-actual-replay-independent-review.json`, SHA-256
`50c3994de4fc69e5e025b6a8fab7f8817368c62a51c653b4520609d2f271fdd6`.
The explicit decision in `config/reviewed_asm_families.json` adopts this
complete family as 91 reviewed ASM instruction bytes and one uncredited
alignment byte. All C/C++ counts and neighboring ownership remain separate.
