# Shared OP exit callbacks

This natural C++ source restores two complete decoded OP callbacks:

| Function | Original load extent | Size | Checked NOPs |
| --- | --- | ---: | ---: |
| `game_exit_to_dos()` | `D41C..D435` | 25 | 1 |
| `game_exit()` | `D7EC..D834` | 72 | 0 |

At initial review, neither range overlapped existing OP acceptance. Both functions genuinely return
far with no arguments. The DOS wrapper's offset3 NOP is original same-CS far
call relaxation padding; it is compared normally and receives no credit.
The original ordered relocation streams are `[21, 16, 11]` and
`[68, 63, 58, 53, 48, 43, 28, 17, 6]`. There are no compiler tables or owned
DATA/BSS. The complete accepted match credits96 authored instruction bytes
from97 compared bytes.

Maintained TH04 `src/shared/core/game_exit.cpp` and ReC98's TH02 DOS wrapper
are ordinary natural donors. The complete observed TH05 cleanup order releases
the packfile, clears both real graphics pages, restores page selection, ends
memory/vsync/text/joystick state, restores EGC and finishes BGM. The wrapper
then restores keyboard beep, system line and text cursor. All MASTER return
types and Pascal far signatures are retained. The wrapper uses the genuine
far C++ cleanup signature and explicit actual same-CS context, without a
near retype or supplied call instructions.

The graphics page operations use ordinary `outportb` calls already present
in accepted OP initialization. This is a real hardware protocol, with no
physical-register allocation hints, dummy operations, branch templates or
compiler flag experiments. All library implementations remain foreign.

The first coherent-TU producer `op-game-exit-a` is honestly rejected: the
same-code-segment annotation also associates a defined callee with the caller's
contribution. The actual compiler therefore put both 25/72-byte bodies in
`EXIT_DOS_TEXT` and emitted an empty `EXIT_CORE_TEXT`. Its 97-byte contribution
failed the declared whole25 boundary; no second producer or negative ran.
This is a genuine TU-context mismatch, not an algorithm or type correction.

The revised packet follows the two actual donors: `game_exit_to_dos.cpp` owns
only the wrapper and `game_exit.cpp` owns only cleanup. Both bodies are verbatim
unchanged. The shared header has no same-code-segment annotation; only the
wrapper annotates its actual foreign far callee. Each TU has its own module,
four-file closure, outside-only binder and compiled negative. Normal replay
must compile the two distinct TUs honestly. No empty prefix or foreign body
is compiled as context. Actual CS is `0D30` and DS `0EFE`. Reserving the real
foreign music DATA end at DS:`2817` keeps the harness's minimum allocation
valid without artificial stack bytes.

Private `.analysis/op-game-exit-boundary-review.json` records full original
instructions, NOP classification, ordered fixups, actual library addresses,
hashes and closure. `.analysis/op-game-exit-candidate.json` proposes both
complete contributions with separate negatives: the wrapper's beep restoration
is replaced by cursor restoration, while the core's first graphics-access page
changes from 1 to 0. Two fresh complete raw/ordered producers and each
independent compiled negative remain required. The unchanged-body factor is
pinned in `.analysis/op-game-exit-split-proof.json`; the failed parent remains
intact. No acceptance or packed
container claim is made by this source preparation.

The independent producers subsequently pass as `op-game-exit-to-dos-b` and
`op-game-exit-core-b`: each has two fresh complete raw-byte and original
ordered-fixup checks plus its own compiled negative. The DOS wrapper's
beep-to-cursor substitution and the core's access-page 1-to-0 mutation are
both rejected. The root imported both complete functions, 97 compared bytes
and 96 authored instruction bytes after excluding the one checked NOP. Both
CPP files, their shared header and separate binders are frozen accepted inputs.
The earlier combined producer stays unchanged and failed; no positive or
negative compilation is attributed to that rejected placement.

The piano334 functions remain parked: their reference relies on artificial
fastcall arguments, preservation hints and an explicitly forced XOR encoding.
The separate background-free50 candidate has a strict ordered-fixup blocker;
the new exit source does not import either implementation. Native details and
current acceptance-overlap checks are in
`.analysis/op-remaining-native-review.json`.
