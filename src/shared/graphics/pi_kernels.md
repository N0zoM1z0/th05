# PI row, palette and release kernels

Two complete maintained ASM contributions independently reconstruct eight native
procedure occurrences across OP and MAINE. They receive separate reviewed ASM
credit, not C/C++ credit, asset ownership or whole-program acceptance.

| Artifact | Masked row kernel | Plain rows / palette / free family | CS / DS |
| --- | --- | --- | --- |
| OP | DD10..DD97, 135 bytes | DE80..DF12, 146 bytes | 0D30 / 0EFE |
| MAINE | EEB8..EF3F, 135 bytes | F028..F0BA, 146 bytes | 0E80 / 1011 |

The masked contribution contains one complete near procedure and no NOPs,
padding or tables. Its ordered MZ fixups are [54,106], two real far calls.
The other contribution contains plain rows at relative 0..58, palette application
at 58..96 and free at 96..146. Its ordered fixups are [17,89,140]. The sole NOP
is at 145 after free's RETF 2, checked alignment with zero credit. The other
source EVEN directives emit no bytes. There are no runtime placeholders, inert
branches, CODE tables, owned initialized DATA or asset payloads.

## Native origin and provenance

Candidate algorithms are pinned ReC98 b6ba5b0a's explicit symbolic
`th05/formats/pi_asm_1.asm` and `pi_asm_2.asm`. Acceptance does not transfer.
Independent native review verifies complete returns, branches, actual caller
contracts and all NOPs against each pinned original load module.

The frameless row kernels deliberately use BP=SP without saving BP, take hidden
ES:SI packed-data pointers and DI height, and return near with eight argument
bytes removed. Masked drawing also takes AX mask ID, switches DS to video RAM
and uses a private EGC mask helper. Palette/free use BX as the argument-frame
base instead of BP. These interacting private protocols support reviewed genuine
original ASM ownership. No specific inspected native portion has positive
compiler-generated provenance. Literal historical source, original assembler
identity and possible historical mixed-source arrangements remain unproved.

Maintained sources use named pointer-normalization macros, typed record/geometry
constants, real stack arguments, symbolic loops and provider names. They contain
no codegen helpers, opcode arrays, target-byte includes or copied instruction
listing. Their exact comparison is separate from origin and ownership review.

A bounded check of all 653 members of the pinned master0.23 archive found no
game wrapper, slot or mask-identifier hits. Positive vendor findings include the
complete PiHeader definition and the actual library providers. Those definitions
corroborate ABI; neither borrowed type declarations nor provider bodies receive
authored credit. This is not an exhaustive renamed-body search and does not
exclude every historical vendor adaptation.

## Full ABI and external state

The full 72-byte PI header retains comment far pointer, comment length, mode,
aspect bytes, plane byte, four machine bytes, machine-extension length and far
pointer, X/Y sizes at 20/22, and 48-byte RGB palette at 24. Each palette has
16 complete RGB triples. Eight headers occupy 576 bytes; eight offset:segment
buffer entries occupy 32 bytes. The type include emits no initialized bytes.

| Foreign object (DS offset) | OP | MAINE |
| --- | --- | --- |
| Four masks, four words each (32 bytes) | 0A64 | 06DE |
| Eight far buffer pointers | 0A84 | 06FE |
| Complete current palette | 2E1E | 1D9A |
| Mask pointer / row / destination words | 384C / 384E / 3850 | 27B4 / 27B6 / 27B8 |
| Eight full headers | 3852 | 27BA |

Actual calibration OMF EXTDEF/PUBDEF records were independently checked, including
literal `Palettes` without a leading underscore, lowercase `_pi_headers` and
`_pi_buffers`, uppercase `_PI_MASKS`, and the exact C++ entry aliases. The private
helper spelling is `@pi_mask_setup_egc_and_advance$qv`. MAP gates check the
demangled signatures together with ordinary entry/end labels; aliases add no
functions or bytes.

Far providers remain external: GRAPH_PACK_PUT_8_NOCLIP, EGC_OFF, PALETTE_SHOW
and GRAPH_PI_FREE. The mask helper remains foreign at DD97/EF3F and receives
no CODE credit. Mask patterns and every packed image/header/palette value are
unowned by these units; only addresses and complete types are maintained.

## Preserved behavior

Row arguments are word stride, width, top and left at incoming SP+2/+4/+6/+8.
Both kernels intentionally clobber BP; RETN 8 matches the real wrappers that
restore their own frames. Packed data advances by stride, then normalizes
ES:SI through `ES += SI >> 4; SI &= 15`, preserving original word wrapping.
DI is a do-while height counter; no new zero-height guard is introduced.

Masked rows first use the unclipped pack provider at scratch row 400, then use
EGC with source offset 32000 to transfer to the real destination. Destination
left conversion uses logical SHR, and vertical wrapping subtracts one plane
after advancing the global offset. DS/ES, SI and DI are saved around this video
phase. The helper advances mask state; no helper body is imitated here.

Plain rows mutate the private top argument, wrapping by one subtraction at 400.
Palette apply captures BX=SP before saving SI/DI, copies all 48 bytes and calls
the real palette provider. Its REP MOVSD occurs before PALETTE_SHOW's CLD, so
DF-clear entry is a real precondition. No CLD is inserted. Normal pack-provider
paths clear DF; unusual early-clipped paths can return before CLD, so these
units do not promise unconditional DF clearing for arbitrary inputs.

Free captures its far argument at SS:[BX+4], checks the complete dword pointer,
pushes real far header/image arguments, clears the buffer before the provider
call and returns with RETF 2. It does not invent header clearing or new failure
handling. Palette/free preserve the original BX stack contract and cleanup.

Symbol-only binders preserve actual CS/DGROUP frames and contain no initialized
payload or artificial stack. The masked unit's byte-aligned foreign tail keeps
its odd 135-byte boundary and genuine near helper address without creating a
SHARED group. Reserves use independently checked foreign DATA bounds, and all
ORG values remain below 64 KiB.

## Exact gates and explicit adoption

Receipts under `.analysis/pi-kernels-native/` are `op-masked-a`, `op-plain-a`,
`maine-masked-a` and `maine-plain-a`, each containing `receipt.json`. All four
have two fresh deterministic TASM producers, complete ordinary CODE SEGDEF and
LEDATA coverage, actual MAP/public/CS/DGROUP checks, every raw byte and literal
ordered relocation agreement. Each has its own assembled semantic negative:
scratch row 400 to 399, or palette copy from 16 to 15 colors while its full type
remains 16 colors. Each mutation is rejected over the same complete scope and
ordered fixup stream. Unchanged tool execution proofs and all previous accepted
owners are reused after dependency-identity checks.

Independent reports are `.analysis/pi-kernels-native-review.json`
(SHA-256 `8351ac227687736eeb1fd28742df06fd8b2f3a71101817524dc186f7f01f0a55`)
and `.analysis/pi-kernels-maintained-source-review.json`
(SHA-256 `b6f8ebc631ab0f9cd243563b5e1640e3c9986b630242433fbd5209734c131b00`).
Native proofs are pinned in `config/asm_families.toml`; exact records and explicit
per-owner/note adoption remain separate in `accepted_asm_families.json` and
`reviewed_asm_families.json`. Totals are 562 compared bytes, 560 reviewed ASM
instruction bytes and two checked uncredited NOPs. C/C++ counters are unchanged;
the global denominator and 98% objective remain open.
