# TH05 reconstruction handoff — 2026-11-11

## Start here

The working branch is `main`. Read [AGENTS.md](../AGENTS.md) for the current
lightweight workflow and [ORACLES.md](ORACLES.md) for exactness criteria. The
source of truth is the **current acceptance ledger**, not older exploratory
notes or a previous agent's handoff:

- `config/accepted_units.json`, `config/accepted_units.op.json`,
  `config/accepted_units.maine.json` and `config/accepted_units.zun.json`:
  accepted natural C/C++ (and scoped initialized DATA).
- `config/accepted_asm_families.json` and
  `config/reviewed_asm_families.json`: separately reviewed ASM ownership.
- [Generated progress](PROGRESS.md) and
  [gapless ownership map](../resources/ownership.json): coverage and unknown
  ranges. The global authored-byte denominator is **not yet established**;
  do not claim a percentage from the bounded accepted totals.

Use `git status -sb` before editing, including dirty files; no other agent is
working in this repository. Preserve and integrate legitimate dirty work.
Use only targeted complete-function native replay after changing executable
inputs; **never run the full cold-replay set by default**. For documentation
alone, inspect the diff and use lightweight validation. Commit substantive
progress as `gpt-web: <description>`. Local Git checkpoints are not Git pushes.

## Recent accepted code: do not reopen old failure notes as active blockers

The following statuses were checked against the acceptance manifests and
ledgers as of this handoff. Each accepted owner has its own complete-scope
evidence; referenced function sizes are compared extent bytes, not
necessarily all authored bytes where padding is present.

| Area | Current accepted scope | Maintained evidence |
| --- | --- | --- |
| MAIN EMS Boss faceset | Full **154-byte** C++ function at `B9CC..BA66`; original ordered fixups `[71,24,133,114]` | [EMS review](../src/main/ems/ems.md) |
| MAIN stage session | **803-byte** initializer; genuine four-function 1,826-byte compiler context | [Stage context](../src/main/runtime/stage_session_context.md) |
| MAIN shot collisions | **399 + 210** complete C++ functions, individual exact ordered fixups | [Shot collisions](../src/main/player/shot_runtime.md) |
| MAIN Mai/Yuki tracking | **186-byte** C++ function; TCC `-S` → TASM32 restores fixup order `[38,130]` | [Later attacks](../src/main/boss/mai_yuki/later_patterns.md) |
| MAIN performance selectors | **76-byte** complete reviewed ASM family at `CF7A..CFC6`; **74 authored instruction bytes**, two uncredited `EVEN` NOPs | [Performance/selector family](../src/main/runtime/playperf_select.md) |
| MAIN scrolling | **204-byte** tile-ring update + **115-byte** scroll driver, independently exact | [Ring](../src/main/scroll/ring_update.md), [driver](../src/main/scroll/driver.md) |
| MAIN dialog opcode | Full **456-byte** `dialog_op()` at `13B82..13D4A`, including natural one-byte switch alignment, full 30-byte table and literal ten-site fixup order; 455 authored bytes | [Interpreter](../src/main/dialog/opcode.md) |
| MAIN dialog graphics | **88 + 56 + 74** contiguous bytes, three source-owned graphics functions | [Dialog runtime](../src/main/dialog/runtime.md) |
| MAIN bullet/Gather invalidation | Full **168-byte** reviewed original ASM at `E40E..E4B6`, no alignment or relocations | [Bullet/Gather dirty tiles](../src/main/bullet/gather_invalidate.md) |
| MAIN Mima bomb backdrop | Four-entry **226-byte** GRCG family at `1052C..1060E` exact reviewed ASM; **224 authored** bytes, two uncredited NOPs | [Mima backdrop](../src/main/player/mima_backdrop.md) |
| MAIN sparks | **98-byte** random-spawn and **106-byte** radial-spawn ASM families; distinct 22-byte C++ player wrapper | [Random](../src/main/boss/sparks_add_random.md), [circle](../src/main/boss/sparks_add_circle.md) |
| MAIN/OP/MAINE CDG | Per binary, **342-byte** load/read/free family + **14-byte** free-all; reviewed ASM with real local provider addresses | [Loader](../src/main/formats/cdg_load_family_op_maine.md), [free-all](../src/main/formats/cdg_free_all_op_maine.md) |
| MAIN high-score display | **22-byte** `hiscore_load()` at `C9A4..C9BA` exact C++; original `BX`/`CX` digit loop | [High score loader](../src/main/score/hiscore_load.md) |
| MAIN/OP/MAINE sound effects | Per binary, **57-byte** SE play + **76-byte** SE update exact C++; all original update fixups `[43]` | [Sound controller](../src/shared/sound/se.md) |
| MAIN/OP/MAINE input | Per binary, **262-byte** BIOS/joystick scanner reviewed ASM; **16 + 42-byte** held/input-wait functions accepted C++ | [Scanner](../src/shared/hardware/input_sense_op_maine.md), [wait](../src/shared/hardware/input_wait_context.md) |

Other previously reported blockers are **already resolved**: Shinki ball
updater **220** and wing preparation **386**, Yumeko sword updater **283**
(reviewed ASM), generic Boss defeat **414** and player collision **43**,
MAINE registration menu **1,034**, MAINE Staff controller **991** and
updater/renderer **626/861**, and OP score decoder **169**. Check the
individual accepted IDs before treating old candidate headings as current.
The 55-byte BB loader, 55-byte near vector helper and 40-byte scroll
coordinate helper are exact **reviewed ASM**, although alternative ordinary
C++ source candidates for those functions remain inexact.

## Genuine open work

**Dialog opcode resolved.** The 456-byte interpreter now has full source/
compiler evidence (new accepted row above); do not reopen the earlier missing
switch-table zero as a live blocker. Only the complete opcode extent is
accepted from the joined 1,123-byte context. Its following runner has its
own accepted standalone owner because the joined TU's runner fixup order
differs; this does not invalidate the independently accepted opcode.

**Score insertion remains open:** MAIN `C8F0..C998` is a 168-byte original-register score-insertion function. Typed C++ source and a genuine foreign binder were explored; the pinned 16-bit inline assembler rejected its 386 string-copy primitive. The failed compiler sources/logs are retained in `.analysis/` and no live manifest/acceptance claim was added. See [score entry](../src/main/score/continue_enter.md).

**Other unknown intervals.** The [ownership map](../resources/ownership.json)
contains actual unowned code/data ranges. Examples requiring function-boundary
review are MAIN `C9BA..CAD2` (player invalidation/movement and an inline switch table; the `C9A3` NOP remains outside the accepted `C9A4..C9BA` loader) and
`15311..158AA` (not one automatically accepted function). Use original
ReC98/source and native control-flow evidence before claiming ownership or
credit. Further useful natural-C++ recovery opportunities can be found in
[unaccepted candidates](reconstruction/UNACCEPTED_COHORTS.md). Do not
reinvestigate Shinki or Staff functions already accepted simply because an
old intermediate note calls them “unaccepted.”

## Practical workflow and storage

1. Inspect only the intended files and the current Git status. Prefer
   complete Boss/controller functions **and** relevant leaf functions;
   choose work by potential real source coverage, not only function size.
2. Compare the **entire** changed original function and literal relocation
   order using `scripts/replay_units.py --artifact main --units ID --output
   .analysis/unit-replays/UNIQUE_NAME`. Use `--artifact op` or `--artifact
   maine` for other binaries; reviewed original-ASM units use
   `scripts/replay_asm_family.py --unit ID --native-review FILE --output DIR`.
   Keep the meaningful compiled negative, the source inputs and original
   MAP/OMF/MZ evidence. Do not substitute “same length” for byte exactness.
3. On a genuine pass, adopt the focused receipt, update ownership/progress
   with repository scripts, run the relevant checks, commit with the requested
   `gpt-web:` prefix and leave the tree consistent. For pure prose cleanup,
   no compiler or new receipt is necessary.

The ignored `.analysis/` cache includes a private, attested Borland toolchain
and Wine prefix, target bytes/decoded views, Ghidra context and many exact
producer receipts. **Keep** those prerequisites, all accepted evidence,
meaningful unresolved compiler-context diagnostics and the tracked source /
ledgers. At the 2026-11-11 cleanup, **908 unreferenced, non-accepted `gpt-web-*`
trial folders** were removed locally, reducing `.analysis` from about
**1,503 MiB to 655 MiB** (848.6 MiB freed). Those disposable builds can be
regenerated from maintained source; do not interpret their absence as lost
acceptance. The tracked Git commit contains prose/source/ledger changes,
while ignored cache deletion is local and is not itself represented by Git.

Historical per-function notes remain valuable for source semantics and
failed hypotheses, but their older intermediate conclusions should always
be read alongside the latest accepted section and the current ledger.
