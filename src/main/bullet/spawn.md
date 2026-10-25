# Original-assembly bullet generation families

These two maintained ASM owners reconstruct the complete TH05 spawning,
group-velocity and shared difficulty-tuning algorithms. They are independently
reviewed assembly reconstruction, separate from the unchanged C/C++ owners.

| Owner | Complete native extent, exclusive end | Instructions credited | Symbolic CODE tables | Checked zero-credit bytes |
| --- | --- | ---: | ---: | ---: |
| `spawn_groups.asm` | MAIN171EA..173DE | 466 | 32 | 2 |
| `spawn_raw.asm` | MAIN1743C..17676 | 528 | 36 | 6 |

Both use the original CS1527 and DS209D contexts and empty ordered MZ relocation
streams. All1070 bytes compare normally. The1062 authored ASM bytes comprise
994 instruction and68 symbolic dispatch-table bytes. The accepted C++ clipping
function173DE..1743C(94 bytes) between them and C++ tuning17676..176B8(66 bytes)
afterward remain outside these scopes, with unchanged source and evidence.

## Native origin, records and contracts

Independent native and maintained-source review establishes a private packed
register protocol: AL speed tuning, BL/BH spread/stack state, CL/CH speed/group
iteration and SI/DI angle/completion state. Raw allocation patches two CS byte
immediates before spawning. Easy and Lunatic share Hard's register dispatcher
and handlers, so the232-byte tuning family is accepted coherently rather than
as artificial independent C++-style function scopes. These observations support
handwritten assembly beyond merely relying on an `.asm` filename or a shape match.

The maintained sources retain descriptive algorithm labels, field accesses,
real calls and symbolic handler tables. The only explicit pushes/pop pairs added
to the source text expand the candidate's Pascal-call and USES macros; their
actual emitted instructions are independently compared. No opaque instruction
array, emitted opcode directive, numeric local CODE label, fake prefix or
compiler-body conversion supplies authored credit.

`spawn_types.inc` represents the complete Point4, Motion12, BulletTemplate14,
Bullet32 and gather-template14 records, including overlapping bullet state
bytes22/23, final origin/distance fields and all shared template fields.
It emits no DATA/BSS. The semantic ABI headers are pinned separately from the
actual assembler include bytes; no accepted C/C++ declaration was edited.
Binders provide original foreign addresses and segment/group placement without
initialized instruction or DATA payload. Existing providers and state objects
receive no transferred credit through these CODE scopes.

The original behavior is preserved, including unsigned byte wrapping, signed
stack-completion comparison, random-ring low-byte pointer advancement, invalid
group fallback and the stale-AH Easy stack decision. That decision reads the
last spread-angle delta rather than the stack count. It has not been corrected.
Regular/special wrappers preserve the actual template angle/speed word;
allocation and velocity paths preserve SI/DI as the native code does. Neither
source invents an ES or CF result convention.

The candidate semantic references are ReC98 at
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th05/main/bullet/add_1.asm`, `th05/bullet.asm` and their complete type/constant
definitions. Their source text and success labels do not establish TH05 target
acceptance. Literal historical source, the original assembler version and
independently proved pristine provenance remain unknown; the supplied copy
retains candidate-local-attested status.

## Complete native boundaries and exclusions

The first owner includes speed tuning, four emission wrappers and the complete
velocity/angle procedure plus its16-entry table. It has no inert-branch or
runtime-placeholder exclusions. Relative to171EA:

- EVEN bytes45 and75 are checked alignment, with zero credit.
- `[468,500)` is the32-byte symbolic handler table.
- Every remaining byte belongs to a semantic instruction; there are no
  literal NOP instructions inside the bodies.

The second owner includes raw allocation, its far regular-emission trampoline
and the whole shared Easy/Hard/Lunatic tuning family. Relative to1743C:

- EVEN bytes393 and555 are checked alignment, with zero credit.
- Inert jump `[178,180)` targets its immediate fall-through and receives zero credit.
- Runtime-patched dummy immediates193 and212 retain their original value123,
  compare normally and receive zero credit.
- Tables `[394,406)`, `[484,494)` and `[556,570)` contain36 symbolic bytes.
- The remaining528 bytes receive instruction credit. No literal NOP inside a
  real body is silently reclassified as authored padding.

All table words resolve to actual native instruction boundaries in their own
complete owner. Public table/end/patch marker labels emit no bytes, create no
additional functions, and are checked against the real MAP in both producers.
There is no instruction masking, table copying, fixup sorting or output editing.

## Exact evidence and incremental replay

`scripts/replay_asm_family.py` validates the opt-in descriptors in
`config/asm_families.toml`. Each receipt owns one complete actual CODE SEGDEF
and MAP contribution with full nonoverlapping ordinary LEDATA coverage. Two
independent fresh producers, normalized object determinism, unchanged raw bytes,
original relocation order and its own assembled negative are mandatory.
The negative changes speed cap128 to127 for groups, and gather ring points8
to9 for raw allocation, preserving each complete contribution's size.

Private accepted receipts are under`.analysis/bullet-spawn-native/groups-a/`
and`raw-a/`. Both whole diagnostics also passed before formal replay. The
native instruction/handler reviews are`groups-boundary-review.json` and
`raw-boundary-review.json` in that same private parent. Import independently
re-reads real source aliases, argv/logs, objects, MAP/MZ, CS/DGROUP frames,
published boundaries, native target proof and tool identities.

Only the selected owner is compiled. Per-entry configuration and actual source
identities leave other accepted owners reusable; imports can replace multiple
affected owners atomically. Historical verifier inputs remain archived, while
current stricter verification can re-read unchanged saved producers without
claiming new compilation. The groups producer was retained when the DATA-frame
readback guard was added; its actual assembler inputs and outputs did not change.
Installed successful tool execution probes were likewise reused after identity
checks. Original decoded views are reused for any decoded artifact context.

`config/accepted_asm_families.json` records exact evidence. A separate explicit
`config/reviewed_asm_families.json` decision pins each adopted complete record
and these source/origin notes. Replay alone grants no global ownership credit.
The generated inventory overlays only previously unknown bytes, keeps semantic
ASM tables separate from compiler tables, and retains every unreviewed neighbor.

```sh
python3 scripts/replay_asm_family.py --plan
bash scripts/run_heavy.sh python3 scripts/replay_asm_family.py \
  --unit main-bullet-spawn-groups \
  --native-review .analysis/bullet-spawn-native/groups-boundary-review.json \
  --output .analysis/bullet-spawn-native/NEW_FRESH_DIRECTORY
python3 scripts/replay_asm_family.py --accept PATH/receipt.json
python3 scripts/replay_asm_family.py --check
```

Bounded exactness does not establish whole-program linkage, game execution,
packing equality, a complete global denominator or the98% goal. C/C++ counters
and all previously accepted ASM evidence remain unchanged by these new owners.
