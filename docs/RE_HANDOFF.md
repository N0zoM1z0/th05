# TH05 reconstruction — next-agent handoff (2026-11-12)

## Where to start

Read [AGENTS.md](../AGENTS.md), [exactness rules](ORACLES.md) and the
[short replay workflow](RE_WORKFLOW.md). Work on the live `main` branch.
Check `git status -sb` and `python3 scripts/replay_units.py --plan`
before editing. **All dirty changes belong to this workstream**; carry
them through instead of leaving or discarding them. Commit meaningful
progress locally as `gpt-web: ...`; do not push without a request.

The source of truth is the current manifests and accepted ledgers under
[`config/`](../config/), the generated [progress](PROGRESS.md), and the
[gapless ownership inventory](../resources/ownership.json). Recalculate
counts there after any acceptance; this dated snapshot is for orientation.

| Verified state at this handoff | Value |
| --- | ---: |
| Accepted bounded C/C++ units (MAIN / OP / MAINE / ZUN) | **513** (335 / 72 / 104 / 2) |
| Source-authored exact C/C++ CODE | **108,784 bytes** |
| Source-authored exact semantic initialized DATA | **17,433 bytes** |
| Total source-authored C/C++ bytes | **126,217 bytes** |
| Unknown bytes (MAIN / OP / MAINE / ZUN) | **4,485 / 6,979 / 6,557 / 8,559** |
| Total unknown decoded bytes | **26,580** |
| Global authored completion percentage | **Unmeasured** |

The **98%** objective is not a measured percentage: neither packed file
sizes nor decoded byte totals are a validated authored-byte denominator.
Reviewed original ASM is a separately recorded ownership lane, not
additional accepted C/C++ units. Source-written vendor library routines,
assets, writable DATA/BSS and alignment need distinct provenance.
There is **no accepted full packed EXE/COM reproduction**. The original
Japanese game copy has candidate-local-attested provenance, not an
independently proven pristine source image.

## Already solved — do not spend another turn reproducing them

- Main Boss controllers: [Sara](../src/main/boss/sara/sara.md) **1,824 B**
  across its twelve functions; Mai/Yuki shared **1,018 B**;
  [Shinki](../src/main/boss/shinki/update_context.md) **959 B** with a
  separate **802 B** Devil attack; [Alice](../src/main/boss/alice/update_context.md)
  **939 B**; [EX-Alice](../src/main/boss/exalice/update.md) **1,060 B**;
  [Yumeko](../src/main/boss/yumeko/update.md) **884 B**; Louise's
  complete control/attack families. Check the actual unit IDs/ledgers
  before claiming a new CODE extent.
- Stage and ending controllers: Stage 2 complete **653 B** update plus
  **492 B** particle initializer and **51 B** invalidation leaf;
  complete Stage Clear and All Clear **561 B / 579 B**;
  MAINE [cutscene VM](../src/maine/cutscene/cutscene.md) **1,555 B**,
  [Staff controller](../src/maine/staff/initialized_state.md) **991 B**,
  [Verdict](../src/maine/verdict/bonus_scoring_rules.md) **1,748 B**;
  OP [main menu](../src/op/main/menu.md) **3,291 B** and
  [setup](../src/op/setup/window_choreography.md) **1,439 B**.
- Physical initialized DATA now has separately accepted, compiler-made
  near C/C++ owners. Examples: [Extra/Stage 5 midboss near callback
  arrays](../src/main/midboss/extra_schedule_data.md),
  [Boss movement clamp](../src/main/boss/movement_default_clamp.md),
  [Shinki/EX-Alice backdrop C globals](../src/main/boss/shinki/background_rules.md),
  [Staff state](../src/maine/staff/initialized_state.md), and the
  [Stage 2 three-state C initializer](../src/main/stage/stage2_transition_counters.md).
- The original reviewed ASM owners and foreign CL/Master vendor functions
  are documented under [reconstruction notes](reconstruction/). Don't
  relabel already reviewed vendor CODE as newly recovered game-authored C++.

### Important corrected DATA provenance

An isolated initializer matching **two zero bytes is not proof of its
symbol identity**. An earlier accepted Stage Clear proposal used the
wrong address because two unrelated regions happened to contain zeros.
This has been corrected in the actual manifest and bounded receipts:

| Decoded MAIN interval | Correct original owner | Real DS offset |
| --- | --- | --- |
| `[222B4,222B6)` | [Large Boss explosion frame](../src/main/boss/explosion_frame.md), signed `int` | `18E4` |
| `[22432,22434)` | [Previous Miss/Bomb counters](../src/main/stage/bonus_previous_resources.md), two `unsigned char` | `1A62 / 1A63` |

Both initializers have independent native C positive/negative proofs.
The complete **452-byte** Boss explosion and **561-/579-byte** scoring
consumers have been recompiled with correct public symbols. Future
DATA candidates must be checked against native consumer bindings,
original public names, actual byte/word types and alignment, **not just
raw equality**. Don't absorb adjacent zeros into a speculative struct.

## Real unresolved work

**1. ZUN `-S` resident `main()` — natural source not yet exact.** The
original complete embedded function is **269 bytes** at COM
`04A9..05B6`; the maintained natural C++ version currently compiles
as **260 bytes**. The independent **322-byte `cfg_init()`** and
**320-byte semantic DATA** are accepted. Fourteen real first-producer
option-flow experiments have been recorded in
[the native trials](reconstruction/ZUN_RESIDENT_NATIVE_OPTION_TRIALS_2026-11-12.md).
One natural variant compiled to 269 bytes but differed at **252 byte
positions**; identical size was correctly rejected. A separate old
self-assignment/empty-helper version has the right bytes but uses
artificial compiler barriers and must **not** be accepted as natural
source. Preserve the toolchain, original CRT bindings, and concise
reproducible trial scripts rather than retrying variants unchanged.

**2. Yumeko `swords_update()` — source-language alternative only.** The
complete **283-byte original function is already exact as reviewed
ASM**. Its [natural C++ alternative](../src/main/boss/yumeko/swords_update.cpp)
still differs. In the original nine-function context, `-O-` gives the
expected **2,139-byte** combined length with wrong short branch proxies;
`-O` produces the two genuine near-conditional jumps but drops two
original short jumps and yields **2,135 bytes**. Four further genuine
`next_sword` flow rewrites canonicalized to that same inexact output.
See [Yumeko compiler findings](reconstruction/YUMEKO_TWIRL_COMPILER_2026-11-11.md).
Do not add padding, fake side effects, borrowed machine code, or credit
this C++ function a second time.

**3. Remaining original ownership.** Use the *current* unknown
intervals in `resources/ownership.json` and the
[unaccepted candidate index](reconstruction/UNACCEPTED_COHORTS.md).
Prioritize complete recoverable functions and their natural calls, and
verify game-specific semantic DATA against actual users. Several small
unowned intervals are genuine alignment, hardware/vendor state, BSS,
or pixel assets. Zero-heavy intervals are especially ambiguous.

## Fast, bounded verification

Run only what changed; ordinary Markdown cleanup needs neither
compiler replay nor regenerated acceptance receipts.

```sh
# Inspect the working tree and affected accepted source scopes.
git status -sb
python3 scripts/replay_units.py --plan
python3 scripts/replay_units.py --artifact maine --plan
python3 scripts/replay_asm_family.py --plan

# For source changes: only the affected complete units.
python3 scripts/replay_units.py --units UNIT_ID --output .analysis/unit-replays/NEW_UNIQUE_RUN
python3 scripts/progress.py --accept .analysis/unit-replays/NEW_UNIQUE_RUN/receipt.json --write
python3 scripts/ownership.py --write
python3 scripts/ci.py
git diff --check
git commit -m "gpt-web: explain exact progress"
```

The three other binary manifests use `--artifact op|maine|zun` for
both replay and progress acceptance. A shared `.inl` or header may
invalidate *several* accepted units and source-reviewed ASM inputs;
check `--plan` and replay the complete affected closure. Keep true
linker group frames and ordered original relocations. Use `-S`/
TASM32 only where it is the demonstrably native compiler path.

## Private storage: retain useful proofs, discard stale experiments

`.analysis/`, `.tools/`, `_reference/` and `ghidra-project/` are ignored
local working inputs, **not portable Git artifacts**. Preserve the
pinned target binaries/decoded payloads, Wine toolchain and prefix,
calibration objects and MAPs, Ghidra project, original review evidence,
all **current ledger-referenced receipt directories and their complete
native producer/negative snapshots**, plus the specific unresolved
ZUN/Yumeko trial scripts and discriminating diagnostics.

Older failed or duplicate replays not referenced by a current ledger
or useful live note may be removed to save storage; never delete a
receipt simply because the public repo does not list it as a Git file.
The acceptance JSON stores its SHA-256, not necessarily a pathname.
For a handoff to a *different computer*, preserve required ignored
inputs separately; the Git branch alone is not a self-contained build.
See [shared runtime setup](SHARED_TOOLS.md) and
[toolchain/oracle requirements](ORACLES.md).
