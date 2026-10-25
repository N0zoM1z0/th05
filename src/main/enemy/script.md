# TH05 enemy script interpreter

`script.asm` reconstructs the complete original-assembly VM family at MAIN
`1538C..15870`, in the actual CS1527 frame. It consumes a canonical64-byte
Enemy and14-byte BulletTemplate through the original hidden SI/CF/ES protocol.
It is separate from all compiler-generated C/C++ acceptance.

| Surface | Exclusive native extent | Compared bytes |
| --- | --- | ---: |
| Position integration and clipping | 1538C..153B9 | 45 |
| Polar velocity setup | 153B9..153CA | 17 |
| Aim-at-player velocity setup | 153CA..153DF | 21 |
| Enemy bullet-template copy | 153DF..153F3 | 20 |
| EVEN padding | 153F3..153F4 | 1 |
| Interpreter | 153F4..157F9 | 1029 |
| 59-word symbolic CODE dispatch table | 157F9..1586F | 118 |
| EVEN padding | 1586F..15870 | 1 |

The whole1252-byte scope is one actual TASM CODE SEGDEF and one complete TLINK
contribution, not five selected instruction prefixes. The table starts at the
original odd address, has57 distinct handlers, and includes shared/interior
entries. The source derives every table word from a named handler label, never
from numeric target values. There is no initialized DATA or BSS contribution.

## Native origin and semantic reconstruction

The position helper consumes DS:SI and returns clipping in CF using CLC/STC;
the interpreter branches directly on that flag. The helpers preserve only their
actual documented registers and use private SI, ES, AX/DX and stack contracts.
Interpreter handlers share AL instruction lengths, AH durations/arguments, CL
ages and DX mode state, with intentional cross-handler continuations. These
observations support handwritten assembly, rather than reclassifying an
ordinary compiler-generated function merely to obtain matching bytes.

The maintained source names opcode operations, fields, complete record types,
control-flow continuations, rank constants and duration semantics. It uses no
emitted opcodes, target-byte arrays, numeric local CODE labels, fake function
bodies, shortened records or compiler-body conversion. `script_types.inc`
retains all fields of Point4, Motion12, BulletTemplate14 and Enemy64, including
the canonical unused enemy tail. Its size assertions and frozen canonical
C/C++ type inputs preserve the shared ABI without editing accepted headers.
Only the binder contains observed foreign addresses; it supplies no initialized
instruction or DATA payload. The Motion method, vector helper, player-angle
function, RNG and sound provider remain foreign and receive no ASM credit.

Native family bounds and source semantics received independent read-only
review. Candidate ReC98 at`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th05_main.asm` and the complete enemy/bullet definitions, supplies semantic
reference material. Its names, opcode values and acceptance do not transfer.
The sibling TH04 opcode numbering differs; TH05's names and order were derived
from its actual59 native handlers. Historical source text and the original
assembler version remain unknown, and the supplied target remains
candidate-local-attested rather than independently proved pristine.

## Contracts and preserved original behavior

- Entry reads `enemy_cur` at DS3F92 and the script segment at DS0F52. Script
  base/IP arithmetic wraps as16-bit offsets. SI/DI are restored on return.
- A timed instruction yields AL0; removal yields AL1. Opcode values above58
  exit with the original unspecified AL value, without an invented default.
- Template copying preserves SI/DI/ES and assumes the original clear-DF
  convention. No CLD or new register preservation is introduced.
- Turn-start saves/restores DX around velocity calculation. Current-turn
  opcodes07/08 do not: `vector2_near` returns velocityY in DX, so the following
  DL test observes its low byte instead of reliably preserving the opcode's
  requested drift mode. The original bug is preserved.
- Wave vertical/horizontal names refer to the signed drift axis. Vertical
  drift uses cosine-X; horizontal drift uses cosine-Y.

The two actual90h sites are EVEN alignment at family offsets103 and1251.
There are no literal NOP instructions inside the five procedure bodies.
The two-byte `JE` at family1100..1102 targets its immediate fall-through; its
purpose is unknown and it receives zero credit. The source retains a symbolic
branch to that continuation, not an emitted byte string. All four uncredited
bytes compare normally, without normalization or masking.

The resulting authored assembly partition is **1130 instruction bytes and118
semantic ASM CODE-table bytes**, plus4 checked uncredited bytes. The only
original MZ relocation is at family909, the sound call at15716 to14AB:0232.
The59 table words have no MZ relocation sites. Actual OMF local/foreign fixups
are retained and linked normally, and the original ordered MZ stream `[909]`
is compared literally.

## Exact replay and adoption

`replay_enemy_vm.py` requires two independent fresh producers, complete ordinary
OMF/LEDATA coverage, original MAP/group/frame and helper/alias/table boundaries,
full raw bytes, deterministic outputs and the original ordered relocation.
Its own negative changes the minimum autofire interval from16 to17 while
retaining the complete1252-byte contribution; raw comparison must reject it.
Import independently re-reads actual assembler/linker aliases, argv/logs,
OMF/MAP/MZ, source/verifier snapshots, native review and pinned tool surfaces.

The retained exact producer directory is
`.analysis/enemy-vm-native/replay-a/`. The complete native instruction and
handler review is`.analysis/enemy-vm-native/boundary-review.json`.
`config/enemy_vm_acceptance.json` records producer exactness;
`config/reviewed_enemy_vm_unit.json` explicitly adopts only this complete scope
as reviewed native assembly reconstruction. Replay alone does not adopt
ownership. C/C++ counters, ZUN's inferred origin, unknown raster/asset ranges,
foreign providers and all other unreviewed spans are unchanged.

Initial diagnostic attempts`-a` and`-b` stopped on binder CS assumptions before
producing linked outputs. `diagnostic-c` matched the complete1252-byte family
and `[909]`; it is a diagnostic, not an accepted cold-producer receipt. The
final source also documents the independently identified DL-clobber bug.

```sh
bash scripts/run_heavy.sh python3 scripts/replay_enemy_vm.py \
  --native-review .analysis/enemy-vm-native/boundary-review.json \
  --output .analysis/enemy-vm-native/NEW_FRESH_DIRECTORY
python3 scripts/replay_enemy_vm.py --accept PATH/receipt.json
python3 scripts/replay_enemy_vm.py --check
```

Unchanged accepted C/C++ units and tool execution probes need no replay. This
bounded result does not establish whole executable linkage, actual game
execution, packed-file equality, a global denominator or the98% objective.
