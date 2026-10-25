# Piano drawing kernels

Three complete OP source contributions cover four native procedures, one symbolic
near-dispatch table and one semantic coordinate table. They are separate reviewed
ASM ownership, not C/C++ acceptance or whole Music Room reconstruction.

| Complete scope | Native load range | Instruction / dispatch / coordinate bytes |
| --- | --- | --- |
| FM state/render wrapper | D9E2..DA12 | 48 / 0 / 0 |
| Blank keys, pressed key and tables | DA30..DB01 | 161 / 24 / 24 |
| Label glyph blit | DB0D..DB21 | 20 / 0 / 0 |

Actual CS is 0D30 and DS is 0EFE. There are no NOPs, padding, runtime
placeholders, inert branches or ordered MZ fixups in the admitted 277 bytes.
The keyboard contribution has complete procedure starts at relative 0 and 59,
its 12-word dispatch at 161..185, and 12 coordinate words at 185..209. Every
near dispatcher target is a real reviewed instruction boundary in that scope.

## Origin, exclusions and external resources

Pinned ReC98 b6ba5b0a's explicit `th05/op/piano_a.asm` supplies the candidate
algorithms. Native hidden register/FS/segment protocols, direct VRAM/string
operations and interdependent dispatch geometry independently support original
ASM review of these scopes. No synthetic C++ register template, opcode emit,
copied instruction listing or target-byte array is used. Historical original
source and assembler identity remain unproved.

The complete original 345-byte contribution is not adopted wholesale. Keep
DA12..DA30 (30-byte current-note helper), DB01..DB0D (12-byte sprite bank) and
DB21..DB3B (26-byte direct-color helper) entirely unknown. The note helper's
conventional fastcall protocol and candidate history do not independently prove
original ASM; it remains a natural-C++/origin-review lead. The direct-color
helper has a 20-byte core matching pinned GC_SETCO.ASM/GRCG_SETCOLOR and an
existing native vendor core, but modified interrupt/ABI behavior. This warrants
investigation, neither blanket original credit nor vendor exclusion. The byte
DB3B..DB3C lies outside the original contribution, is not a NOP and stays unknown.

The bounded vendor search covered all 653 pinned master0.23 archive members.
Its positive color-helper finding is retained rather than overridden by missing
piano identifiers. It is not an exhaustive renamed-body or ancestry search.
Neither presumed compiler origin nor vendor ancestry is silently excluded.

Pixel resources remain external: the 28-byte black-key row at DS:09EE, label
font at DS:0A0A and CODE sprite bank at CS:0801. Their values are not supplied
or published by this source. The repeated white-key word is derived from the
three-filled/one-edge pixel geometry, not copied from a sprite array.

## Contracts and semantic tables

The full eight-byte note object is five FM bytes plus its three original unused
bytes, at DS:382A (current) and 3832 (previous). FM entry receives ES:DI video
position, SI part ID, DS:BX opaque driver part-pointer address and FS original
game DATA segment. It calls the foreign current-note helper, switches DS through
FS for game state and rendering, and restores DS. It neither defines a shortened
QQ record nor reads its fields. Candidate QQ's full 98-byte layout versus the
shortened C++ view is documented in private review; actual external driver
allocation extent is not established by these owners.

Key drawing preserves DI/SI; pressed-key drawing preserves BX/DI. Entry DF clear
is required by keyboard/label string operations; no CLD is invented. The label
kernel takes AL glyph ID and advances SI/DI while copying eight rows. GRCG mode,
video segment and colors are caller/provider contracts. The direct-color helper
unconditionally enables interrupts, so keyboard drawing and redrawn FM
paths return IF enabled; skipped-render paths do not acquire that behavior.
No invalid-note range check or new register restoration is introduced.

The dispatch contains 12 symbolic near words, not numeric local CODE addresses.
Coordinates are CODE-class semantic data derived from seven white-key degrees
and halfway sharps, left=384 and key width=4. The verifier's narrowly registered
`piano-key-horizontal-positions` model accepts exactly 24 bytes, derives all
12 word values and checks their full native bytes. Arbitrary literal banks,
sprites, unsupported roles, odd half-key widths, overflow, overlap and missing
coverage fail. A coordinate byte equal to 90h is data, not an instruction NOP.
Both table kinds compare normally; they receive distinct accounting categories.

Symbol-only binders preserve real CS/DGROUP and exact provider/resource names,
with no initialized payload or artificial stack. Near provider calls retain CPU
CS even where a scaffold label belongs to the byte-aligned foreign tail. Label
entry DB0D is an original odd intra-contribution address: its standalone source
uses BYTE alignment while the binder preserves the first PARA SHARED frame.
Every ORG is below 64 KiB; no body padding or target patch supplies alignment.

## Exact evidence and incremental reuse

Receipts `.analysis/piano-native/{fm-a,keys-a,label-b}/receipt.json` each contain
two fresh deterministic complete TASM producers, actual ordinary CODE SEGDEF/
LEDATA/MAP/public/frame checks, all raw bytes and empty literal ordered fixups.
Each has its own assembled negative: highlight color 5 to 6, black-key height
9 to 10, or label rows 8 to 7. These change real drawing behavior and are
rejected over each full scope. This is not a claim of a separate compiled table
mutation. Synthetic tests separately reject changed coordinate bytes/model,
asset roles, arbitrary word lists, overlap, overflow and false NOP decoding.

Label-a stopped at its first MAP gate because a WORD-aligned standalone
contribution moved DB0D to DB0E. Correcting only the new source contribution's
alignment restored the reviewed native context; no failed producer was adopted.
The semantic-table verifier extension leaves old per-entry inputs/counts intact;
unchanged source objects, old verifier snapshots and installed tool execution
proofs are reused without claiming fresh compilation of old owners.

Independent reports are `.analysis/piano-native-review.json` (SHA-256
`9213d5fef6d3fb15c93a38ea346d11869ab93596c2106a75fa9ee00c34da4d05`)
and `.analysis/piano-maintained-source-model-review.json` (SHA-256
`1342fb8d39345b4f5f2db0926bff94478ca466e6646ce6911ee276ae895b7872`).
Native proofs/descriptors are pinned in `config/asm_families.toml`; exact records
and explicit per-owner/note adoption remain separate. Totals are 277 compared,
229 ASM instructions, 24 symbolic dispatch bytes and 24 semantic CODE-coordinate
bytes. No DATA/assets, unknown helpers, C/C++ counters or global-denominator
exclusions are claimed. The 98% objective remains open.
