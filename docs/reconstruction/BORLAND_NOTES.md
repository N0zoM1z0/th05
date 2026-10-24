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
