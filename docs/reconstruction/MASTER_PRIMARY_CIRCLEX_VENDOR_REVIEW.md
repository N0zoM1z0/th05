# Circle outline from unchanged original Master source

The separate original-source proof covers only GRCG_CIRCLE_X at MAIN
121C..130C, one complete 240-byte vendor CODE contribution. It grants zero
authored credit. Existing literal, private-rename, circle-fill, EGC and EMS
proofs remain unchanged; this result does not adopt other circle procedures.

The author's GC_CIRCX.ASM and FUNC.INC are consumed byte-identically, including
CP932 comments, line endings, private names, .186, .MODEL SMALL, DATA-before-CODE
declarations, JMOV/ORG self-patching fields and EVEN directives. The original
MAKEFILE profile is `/mx /t /q /w2 /jJUMPS /DFARMODEL`. FAR macros supply the
actual three-word Pascal interface and RETF6 despite the physical SMALL model.
No operand edits, identifier transformations, flag variants or opcode copies
are used to turn the candidate into original source.

## Independent foreign DATA context

The only foreign operands are WORD globals ClipYT, ClipYT_seg and
graph_VramZoom. Their DS offsets 0372, 0378 and 03CC derive independently
from complete original initializer declarations. The 16-byte CLIP record
uniquely occurs at DS:036C; the 11-byte GRP record uniquely occurs at DS:03C4.
The source parser preserves declaration widths/order and restricted literal
products. It rejects anonymous data, ORG/ALIGN/EVEN and unrecognized layout
directives rather than silently skipping them. Labels and public aliases
emit no data. DATA? starts a separate uninitialized section.

Uniqueness is checked only in available loaded DATA, load offsets
209D0..23A26. The symbolic linker DATA reserve C4C8 is a virtual extent and
does not imply that all its bytes exist in the native file. The bindings
are not inferred by reversing three instruction operands or subtracting a
global calibration delta. No initializer bytes are supplied by the binder,
and neither anchor record receives DATA ownership or authored credit.

## Complete original producers

Each original OMF is 492 bytes and contains 240 CODE bytes with empty DATA.
Its quiet author profile has 20 CRC-valid records and no translator-version
COMENT. The new guard binds that profile to the actual pinned assembler,
successful argv/logs and full source identities. Generic game-ASM and previous
original-source guards are unchanged.

Six original LEDATAs cover the complete CODE exactly once: offsets/lengths
0/87, 87/5, 92/3, 95/71, 166/3 and 169/71. These are genuine JMOV/ORG record
boundaries; they are neither flattened nor filled. Actual SEGDEF order is
_TEXT index1 and empty _DATA index2, with DATA in DGROUP. The source's textual
DATA-before-CODE declaration order alone does not predict OMF ordering.

The actual FIXUPP contains three external DATA offsets at 14/29/36 and five
CS-local offsets at 18/22/41/45/49. The self-patched WORD operands at 85/93/167
retain their original initial 1234h; shift bytes at 91/165 retain 9. All fields
compare normally. The source reads foreign globals before switching DS to
video memory, saves/restores DS/SI/DI/BP and leaves ES untouched. It has no
string instructions or added clear-DF requirement. Radius zero returns through
the original RETF6 path.

Both independent source producers match all 240 native bytes, SHA-256
`34d1c8991f308c411c6ab23054f464ba09f60f414183f9587614dad14a35b982`,
and the empty ordered MZ relocation stream. Complete native decode includes
107 instructions with three NOPs at 57/65/239. All three come from original
EVEN directives, including ENDFUNC's final EVEN. They receive zero authored
credit, as do all other vendor bytes. The preceding byte at 121B remains
unknown and outside this scope.

The own staged semantic negative changes the unique INC AX to DEC AX. It
retains the full extent and fixups, changes only byte 78 and is rejected.
Original source OMF, MAP and whole linked MZ outputs are byte-identical across
positives. Raw binder-object hashes are retained; only their dependency-time
comments may differ. Existing metadata handling compares those payload-free
binders, without normalizing original CODE, source objects, linked output or
relocation order.

The first new producer is retained after checking its actual source, tool,
arguments, logs and outputs. Only the independent second and own negative are
subsequently assembled. Total source assemblies are three, symbol-only binding
assemblies six and links three. The read-only reviewer is completed afterwards
and re-observes all saved actual producers. Parser hardening changes only
reader checks; it triggers no new assembly. Installed execution evidence and
all unchanged accepted objects are reused after identity checks.

Public structural CI reads only maintained metadata and reviewer sources.
Focused tests use CRC-valid synthetic INT3 containers, never native instruction
bytes. They reject missing/overlapping CODE, wrong relocation association,
uncredited-field masking, altered DATA context, unsafe/skipped initializer
directives, source/result/flag edits, widened adoption and authored credit.
Native replay additionally rereads the original archive, actual staged inputs,
OMF/MAP/MZ and target bytes. No private game or original-source payload is
published.

## Scope and limitations

The explicit decision is separate from the proof. It adopts only this complete
library procedure as vendor CODE with zero authored credit and a null global
denominator. Historical game project, original game assembler, whole executable
and packed-container equality remain unproved. GC_CIRCL's own BSS placement,
other circle bodies and the intervening byte remain unknown.

Independent first-source/native/OMF review:
`.analysis/vendor-review/circlex-primary-first-independent-review.json`, SHA-256
`2b78cce81ae33131298a845a1bc769dfd1de0f92b88c19bde5f014cf3d3d022a`.

Independent final source/gate/actual/test review:
`.analysis/vendor-review/circlex-primary-source-gate-independent-review.json`,
SHA-256 `43259e0b0794fa5e7cb306dbbe447c3d6981e3cb4bb21c3bf66c86dcd6139e33`.
All 12 focused tests pass. Proposal proof:
`config/master_primary_circlex_ownership.json`, SHA-256
`304a57d179f5a271995a0a7d3ebdc7b5a408e440de5fb3f2a7c7eed83419810b`.
`config/reviewed_master_primary_circlex.json` is the separate explicit adoption.

Final independent adoption/count review:
`.analysis/vendor-review/circlex-primary-final-adoption-independent-review.json`,
SHA-256 `5c95c1c700724514e09de4a1f56c5f6a69c88ba109776e5d5bdf80ecc54fcc51`.
Exactly these 240 bytes move from unknown to vendor CODE; all 53 prior config
files and the other three whole artifact views remain unchanged. The 364-test
CI, native target ownership, generated progress and diff checks pass; all five
incremental plans are empty. Root final review:
`.analysis/vendor-review/circlex-primary-root-final-review.json`, SHA-256
`ee79a1a0f451a747039f92453f2c1643c0a9046d5c2d65fbd28b832d3950e9d0`.
