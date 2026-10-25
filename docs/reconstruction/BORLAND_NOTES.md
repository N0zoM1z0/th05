# Borland reconstruction notes

These observations come from this pinned TH05 target and toolchain. They extend
TH03/TH04's workflow; they do not establish historical source spelling or allow
another target to inherit acceptance. Per-owner notes and retained receipts
contain the full boundaries and bindings.

## Types and calling conventions

The real ABI has two-byte int/near pointers, four-byte far pointers and
segment-only allocation handles. Preserve the class identity in mangled names
and compound return types: `PlayfieldMotion::update_seg3` returns an actual
`PlayfieldPoint` through DX:AX. Declaring a convenient void replacement would
lose the real interface even if the caller happens to inspect registers.

Turbo C++ 4.02 predates built-in bool. Use the actual one-byte game type and
verify enums under the recorded `-b-` setting. Assert complete field layouts,
not merely offsets used by the current function. Slot size does not establish
all overlay sizes: the Cheeto template is a 25-byte view inside a true 26-byte
custom slot. Do not invent a field to force those sizes to agree.

Enum domains also affect intermediate arithmetic. Reducing the sprite enum to
currently used constants below 256 made the decay-pattern ternary operate on
AL/AH. Preserving the real main-sprite domain through `PAT_MAX=320` and its
original word-width bound restored the original AX operations. An enum must
retain its real type even when a function only uses small values.

A truthful far Pascal declaration can produce the original same-segment
NOP/PUSH CS/near CALL through linker relaxation. Stage setup's two rank-selector
calls now reproduce that sequence from C++ alone. Replacing a reference's
instruction macro with a real call should be tested before retaining any ASM.

## Source structure affects emitted code

Place `-zC` and `-zP` owner options before C++ tokens. A function's first
declaration fixes its segment. Redundant `#pragma codeseg` declarations can
create distinct compiler segment definitions even with the same name; inspect
actual OMF and MAP contributions rather than assuming name equality merges them.

Preserve meaningful inline helper layers. In Boss background, converting float
parameters in local min/max temporaries prevented constant folding and added
46 bytes. Restoring the float-to-subpixel wrapper plus signed-range helper
recovered the expected function size without adding an optimization barrier.

Zero comparisons remain a genuine unresolved example. The particle renderer's
natural signed-zero check generates OR AX,AX, while the original has CMP AX,0.
Sixteen bounded zero-spelling and compiler-option probes all emitted OR. This
is a bounded negative observation, not proof that natural C++ is impossible.
The complete original particle function stays unaccepted; no fake zero address
or handwritten compiler-body instructions substitute for a solution.

## Layout and oracle scope

Symbol-only linker context can anchor real external symbols and function
positions. Origin holes outside actual compiler functions receive no credit.
Boss background uses a separate CODE contribution after its inexact particle
function. The one-byte hole does not accept or repair that function. Each
credited function still has its entire raw extent and ordered fixups checked
at its original address.

Semantic C++ switches generate real compiler CODE tables. Compare every table
byte and destination; report table bytes separately from instructions. Explicit
padding is still compared, then excluded from authored credit. Game assets and
target-derived opcode arrays cannot become compiler-table credit.

Raw code equality alone can fail the strict oracle. After the Boss split,
hexagram drawing's 204 bytes match, but a compiler LEDATA boundary changes the
ordering of its MZ fixup sites. That whole function remains unaccepted. Do not
sort relocation lists or normalize instruction encodings to obtain acceptance.

## Incremental evidence

Use actual OMF include dependencies to freeze each unit's consumed source
closure. New unrelated source files do not invalidate old producers. Successful
tool execution probes are reusable only after checking the pinned manifest and
actual installed compiler/header/library surfaces.

Multiple function scopes in one TU share one compilation per fresh round.
A mixed-result receipt retains its aggregate failure. Explicit subset import
rechecks all saved producers and can accept only independently passing complete
functions, including the compiled negative-control owner. It never edits the
receipt or recompiles solely to discard an inexact neighbor.

When an owner defines BSS state, scaffold stack allocation affects real symbol
positions. In OP main menu, `.stack 80h` inserted alignment plus a stack member
before BSS, shifting references by 84h. Omitting that artificial member restored
all original addresses; no game algorithm needed changing. Inspect DGROUP's
actual MAP members before adjusting declarations or adding any padding.

Japanese UI source remains readable UTF8. Opt-in CP932 staging preserves the
actual compiler byte stream with separate digests and independent import checks.
OP main menu verifies this with real Borland producers, including its complete
semantic string/pointer DATA contribution as a separate uncredited observation.

## Empty foreign segments can overflow a group

The first midboss context put its foreign main_01 labels in a synthetic
`MIDBOSS_MAIN01_BINDINGS` segment, while C++ correctly emitted a zero-byte
`MAI_TEXT` in main_01 and owned `MIDBOSS_TEXT` in main_03. TLINK placed the
otherwise unbound empty MAI_TEXT after the long code/DS context gap, extending
main_01 beyond 64 KiB and reporting group overflow. Its failing MAP made the
segments appear merged, but the actual OMF GRPDEFs proved source group capture
was already correct. Naming the foreign scaffold segment MAI_TEXT lets the
empty real compiler contribution merge at the actual main_01 location. Inspect
OMF before attributing this failure to source function declarations or changing
ABI. No function code, gap inside a function or fake implementation is needed.

## Byte rotate APIs are not necessarily compiler intrinsics

The pinned STDLIB.H declares `_crotr`, but a real optimized TC4J `-S` probe
emits a far library call for `_crotr(value,3)`. Plain `(value >> 3) | (value << 5)`
emits shifts and OR instead of byte ROR. The MAINE score codec consequently
remains external until its genuine original implementation/context is recovered;
API presence alone does not prove an exact natural C++ rotate. The retained
probe is `.analysis/compiler-probes/byte-rotate-a`, with no source-byte credit.

## Assembly-output backend is a hypothesis, not transferred acceptance

TH04's `docs/reconstruction/zun/TH04_ZUN_MAIN_V241.md` records a genuine
`-B`/TASM mechanism that preserved its resident error paths. One private TH05
Shinki diagnostic tested that documented mechanism on the unchanged archived
natural monolithic source. TCC ran once with `-B`, emitted ASM, and stopped at
the expected unavailable DOS `tasm.exe` boundary. The generated ASM SHA was
frozen and never edited. TASM needed an external declaration-only wrapper for
four actual empty foreign CODE SEGDEFs already present in the direct object:
LASER_SC_TEXT, BOSS_BG_TEXT, BULLET_A_TEXT and MAIN_0_TEXT. Those declarations
supply no instructions, values, public aliases or alignment filler.

The resulting complete contribution is still4120 versus original4124;
ball update remains216 versus220. Its TASM fixups are ascending and do not
match the original order. This falsifies that backend explanation for the
missing Shinki branches; it grants no new code, no cold acceptance and no
reason to change accepted producers or the core replay pipeline. Evidence is
`.analysis/compiler-probes/shinki-bmode-a/diagnostic-context2.json`, with the
original failed integration steps retained. No additional source or flag
variants were tried.

## Dialog graphics helpers do not establish original ASM provenance

The three original MAIN helpers at 13A3E..13B18 are complete 88/56/74-byte
hardware routines, each with one ordered loader fixup. REP STOSW and the
alternating page-port OUT/ES-word operations establish their graphics semantics.
They do not establish the language of the original author. ReC98 history labels
box and face sources as reverse engineering (381db0a1/d48479ce), followed by C++
decompilation (35d6fe30/a06996af); the copy conversion 36166192 removes an
IDA-style sub_EEF2/loc_EF0A procedure. Its current box source explicitly forces
TEST BX because ordinary pseudo-register C++ would emit TEST BL, and its EGC
copy macro forces LOOP. These are reconstruction choices, so the existing
source cannot by itself justify a new original-handwritten-ASM classification.
No bodies were imported or credited. Private native boundaries, hashes and
provenance commands are recorded in `.analysis/dialog-graphics-origin-review.json`.


### Shinki control-flow diagnostics already exhausted

Private `shinki-natural-cfg-a/observations.json` records two natural C++
control-flow checks on the original frozen monolithic source. A positive
playfield enclosure with nested decay handling still emits216 versus the
original220 bytes; a real value-returning typed enclosure predicate emits240.
Both use unchanged flags and preserve the actual collision macro side effects.
Neither is exact and neither changes maintained source or credit. Together
with the recorded B/TASM backend result, these are completed negative
observations, not pending suggestions. Do not repeat those source forms or
add idle work to retain the two original jump relay blocks.


## Real local definitions recover EX-Alice far calls

The standalone1060-byte EX-Alice callback emitted1064 bytes: four external
far calls became TLINK's length-preserving NOP/PUSH-CS/near-CALL sequences.
Giving the declaration the caller's segment alone did not change that result.
The coherent real33-byte shot gate,78-byte phase helper and1060-byte update
now share one actual C++ TU/CODE contribution. Every function body is verbatim
from the maintained natural sources, with unchanged real far/near ABI and
compiler flags. That context emits the original four-byte far-call sequences.
Two fresh producers match all1171 raw bytes and ordered fixups[309,272]; the
updater's own1060-byte scope retains all52 switch-table bytes and its own
compiled HP-threshold mutation. Prefix111 already has an owner and is not
counted twice. This is evidence for this source-definition context; unrelated
far calls and source cohorts still require their own actual producers.

## Proven same-CS declarations retain real far interfaces

`main-stage-runtime-init-a` independently verifies the natural 174-byte TH05
stage reset from the maintained TH04 donor. That donor already annotates
`shot_level_update` and `hud_put` with `#pragma samecodeseg`; both actual
callees share frame AE1 with this caller and retain genuine far returns.
The TH05 producer keeps their far signatures, normal flags and these source
context declarations. Both complete fresh outputs match, including the
original five-byte `NOP; PUSH CS; CALL rel16` sequences at load offsets
`B5DF` and `B5F8`. The only original ordered MZ relocation is `[144]`, for the
real different-CS item initializer; it stays unchanged. The independent
invincibility-time mutation is rejected.

This is evidence for a truthful compiler context declaration, not permission
to retype a far service as near, supply instructions, or annotate a genuinely
different-CS callee. Validate actual frames and return cleanup first, preserve
the complete compared extent and original ordered fixups, and test only the
affected source. The separate session803 candidate still lacks a mandatory
zero and remains unaccepted; correcting far-call context alone cannot accept it.

The two reset NOPs are uncredited padding (relative133/158); replacement
`main-stage-runtime-init-b` preserves the174 complete compared bytes and
credits172 instructions. A native scan of all accepted MAIN/OP/MAINE CODE
instruction regions also found three older relaxation NOPs in two MAIN
owners. Only those two owners and reset174 were recompiled for corrected
classification; no OP/MAINE omissions were found. Original receipts stay
archived. Padding is never removed from raw comparison.

The same proven context declarations recover the old enemy blockers in
`main-enemy-samecodeseg-a`: the real midboss far entry returns RETF0 and the
real Spark entry RETF8, with both callee frames1527 matching their callers.
Only lifecycle.cpp changes; its full typed ABI remains unchanged. Two fresh
producers pass the original89/576 complete bytes and ordered fixups, with
both linker NOPs explicitly uncredited. This replaces the earlier unsupported
call-context assumption, not the genuine callee interfaces.

## Consume the real packed point return at its ABI boundary

The actual near `PlayfieldMotion::update_seg1` and `update_seg3` implementations
are identical 32-byte routines at load offsets `BE1A` and `1527C`. They consume
one real near-this word, return with RET2, and return the new signed X/Y words
in AX/DX. There is no hidden output pointer or carry-flag result. The full
12-byte Motion and four-byte PlayfieldPoint declarations remain mandatory.
Pinned ReC98 `th04/main/playfld.hpp` explicitly documents direct AX/DX consumers;
the accepted bullet updater already uses this genuine Borland return boundary.

The stage-two updater keeps the full method return type, calls it normally,
and immediately reads signed AX/DX for four bounds comparisons. Its remaining
algorithm uses ordinary typed fields and locals. No register math, shortened
record, scalar-return stand-in or instruction body is introduced. This removes
the named-point spill from664 to the original653 bytes. Two fresh producers
in `main-stage2-update-abi-a` match all raw bytes and fixups `[441,426,225]`;
the independent palette-peak mutation rejects. The scrolling service also
uses the canonical existing C/Pascal/near declaration and the same real address.

`main-shots-update-abi-b` applies the same protocol at both actual method calls.
Live returned coordinates are consumed into the real cache before pointer,
count or age changes; the hit-animation return is consumed before subsequent
work. The remaining homing angle uses an unsigned byte-storage view for modulo
256 updates, preserving the canonical full Shot class. Two fresh producers
match all408 bytes, including eight compiler table bytes and ordered fixups
`[202,112]`; a real acceleration mutation rejects.

These are compiler-extension ABI consumers, recorded as C++ DOS-intrinsic
owners. Do not alias ordinary algorithm locals to physical registers, read a
return after another call or clobber, change the real function prototype, or
reuse the mechanism without checking that callee's actual ABI and lifetime.

## Scalar rvalues can preserve the original transition scaling

The stage-two initializer's476-byte form already had the original single
common X store in DX. Its16-byte difference was exactly four in-place
`frame <<= 3` operations, each four bytes shorter than the original ordinary
scalar-result scaling. Replacing only those four real assignments with
`frame = frame * 8` preserves the eight branches, genuine state writes and
values (all normalized transition frames are0..127). No register variable,
extra work, barrier, flag variation or padding is introduced.

The independently factored initializer in `main-stage2-particle-initializer-a`
now matches all492 bytes and ordered fixups `[484,441]` from two fresh
producers, with its own zoom mutation rejected. The already accepted updater
and ABI header were not changed or replayed. Prior claims that branch stores
caused the shrink are superseded by the actual four-sequence native comparison.

Keep register-return borrowing limited to a proved actual lifetime. The one
item-update experiment235 failed before a second or negative build: ordinary
pickup-X arithmetic overwrote AX before subtracting its supposed borrowed X,
producing self-subtraction. Typed safe248 source was restored exactly. No BX
algorithm alias, register forcing or alternate ABI was introduced to repair it.
