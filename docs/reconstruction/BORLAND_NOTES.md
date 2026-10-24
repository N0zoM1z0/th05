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
