# Alice foreground candidate

The complete adjacent original functions are `puppets_render` at
`[141D7,14354)` (381 bytes) and `alice_fg_render` at `[14354,143E0)`
(140 bytes). They use near frame `0AE1`/`main_01`, with DS `209D`. Native review
decodes all 521 bytes as 189 instructions, validates the real returns and every
direct branch destination, and finds no table, padding, DATA or BSS contribution.
At the initial proposal stage this candidate was not yet compiled or
accepted; the later exact 381-byte puppet and 140-byte foreground owners at
the end of this note supersede that status.

The puppet renderer reuses the full accepted 26-byte `AlicePuppet` from
`beam.hpp`, overlaid on the first two complete custom-entity slots. It clips
32-pixel sprites, computes triangular bobbing, selects animation or the damage
silhouette, draws charging circles and the connecting beam, and renders the
final two beam sprites. The real two-entry X-center local and the most recent
center Y remain ordinary local variables. Beam states rely on the game's
visible-puppet invariant; the source does not add dummy initializers to alter
the original paths.

The foreground callback uses the canonical full Boss. It chooses the explosion
sprite or normal animation, renders a damage silhouette when required, calls
the real puppet renderer defined in the same TU, and updates both actual
foreign explosion renderers. All first declarations capture the real
`main_01` context before the canonical stage callback declarations. No accepted
header was modified.

The master.lib sprite, circle and line APIs retain their far Pascal ABI. The
one-plane call has five real word arguments: pattern plane zero and the actual
`0xFF00 | GC_RMW` put-plane control. These are hardware rendering semantics,
not asset values or code bytes. The PC-98 GRCG is disabled through the real
`outportb(0x7C, 0)` interface. The code contains no assembler, emits, register
allocation hints or replacement helper bodies. ReC98 retains the Alice
procedure semantics in assembly; the source reconstructs the rendering
algorithm with its complete types and primary graphics interfaces. TH04-family
sprite interfaces guide ABI reuse, not acceptance.

Original ordered fixups for the complete cohort are
`[506,488,425,375,355,325,313,256,240,220,204,168,148]`. The per-function orders
are preserved independently in the private review. Calibration is only a
routing aid and its relocation order is not substituted for the original.

The symbol-only binder places the original foreign master, explosion and DS
symbols, including all empty foreign compiler segments by their actual names.
Its holes occur outside both complete functions. The actual OMF CODE must
first confirm a 521-byte contribution before that fixed outside tail is valid.
No opcode or padding adjustment may be used to repair a different result.

Private files `.analysis/alice-foreground-boundary-review.json` and
`.analysis/alice-foreground-unit-proposal.json` contain the complete native
boundaries, branch/call sites, target/source hashes, ABI bindings and proposal.
`python3 .analysis/alice-foreground-review.py` repeats the bounded native review.
The meaningful staged-source negative changes the beam color from 9 to 10.
At the original proposal stage, acceptance required independent producers,
original bytes/fixups, OMF/MAP/dependency checks and rejection of the control.
The later accepted receipts meet those requirements.

The first combined producer, `main-alice-foreground-a`, emitted 381 bytes for
the puppet renderer and 150 for the 140-byte foreground callback. The puppet
renderer retained every instruction boundary and all ten original ordered
fixups; its twelve raw differences were the DS offsets displaced by the
combined callback's extra ten bytes. This was a failed full comparison, not an
accepted normalized result. The callback's additional bytes were an ordinary
left/top local allocation difference and a duplicated signed animation divide;
that 150-byte diagnostic remained unaccepted. The accepted 140-byte
natural callback later superseded this particular failed experiment.

The unchanged complete puppet-rendering body was factored into
`puppets_render.cpp`. The coherent `foreground.cpp` includes that canonical body
under a combine guard, keeping the actual C/Pascal interface intact. The private
factor proof confirms literal body equality with the first combined producer;
no source instructions were altered to split it. The independent binder ends
the whole compiler-owned extent at `14354` and anchors DS correctly without the
unaccepted callback. `main-alice-puppets-whole-a` then passed two fresh complete
381-byte producers, raw bytes, original ordered fixups and the own beam-color
9-to-10 negative control. The root accepted only these 381 bytes; the separate
150-byte callback candidate receives no credit.

Two later independent callback trials retain the complete140-byte target scope
without recompiling the accepted puppet owner. A joined byte-frame local with
an attack bypass emits146: ordinary pattern/left register declarations restore
the native allocation, but a six-byte byte-local store/reload remains at the
join. A simple inline quarter-frame helper emits148, retaining the duplicated
divide. Both stop after one diagnostic producer and grant no credit. Their
These one-off producer directories were removed after the complete 140-byte
foreground callback was accepted. The diagnostic outcomes are retained here
because they explain why the joined-frame and inline-quarter helpers were not
adopted; no current source or acceptance depends on those binaries.

An ordinary `register unsigned char` declaration on that joined frame local
also emits146, with the same store/reload.
Experimental files were removed; the maintained baseline is unchanged.

## 2026-11-10: complete 140-byte foreground C++ recovery

**`alice_fg_render()` is now accepted** as a complete 140-byte natural C++
source function at `[14354,143E0)`, with original ordered fixups
`[125,107,44]`. This supersedes the earlier 150/146-byte standalone
candidate failures above. The genuine adjacent `puppets_render()` is still
included from its single maintained 381-byte source; its existing accepted
owner is unchanged, and both functions together now reproduce all
**521/521 original bytes** in the real physical `ALICE_FG_TEXT` segment.

The earlier compiler assigned the X position to the BP local and Y to DI,
which made both drawing calls use a three-byte stack push. Reordering the
natural local declarations as **left, top, patnum** restores the native
X-in-DI and Y-on-stack allocation, without physical register aliases. The
conditional animation expression is written as three ordinary branches
using the existing true frame-modulo variables; the native shared signed
`/4` for the final animation frame is generated without the duplicated
local compiler path. The same natural source preserves original big-explosion
routing, damaged one-plane rendering, puppet rendering and both explosion
updates. No instruction template, arbitrary ABI change, substituted DATA,
artificial alignment byte or foreign helper implementation was used.

The original binder's ten-byte 150-byte candidate end was incorrect once the
function shrank to its real 140 bytes. The separately reviewed
`probes/units/alice_foreground_exact_bindings.asm` restores the original
`143E0` end and therefore the true DATA/DS209D address frame; it contains
only foreign symbols and original outside intervals. The generated object
naturally preserves the complete raw function and the literal original
three-site relocation order, rather than postprocessing fixups.

The focused receipt is
`.analysis/unit-replays/gpt-web-main-alice-foreground-complete-20261110/receipt.json`.
Two independent real Turbo C++/TLINK producers match all 140 bytes and
all ordered fixups, with complete MAP/OMF boundaries. The compiled negative
changes the actual alternate animation speed from `/4` to `/2` and is
rejected. Only the 140-byte foreground callback adds new authored C++ CODE
credit; previously accepted 381 puppet bytes are not counted again.
