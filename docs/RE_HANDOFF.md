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
| Accepted bounded C/C++ units (MAIN / OP / MAINE / ZUN) | **536** (350 / 75 / 109 / 2) |
| Source-authored exact C/C++ CODE | **108,784 bytes** |
| Source-authored exact semantic initialized DATA | **17,512 bytes** |
| Total source-authored C/C++ bytes | **126,296 bytes** |
| Unknown bytes (MAIN / OP / MAINE / ZUN) | **3,038 / 5,281 / 4,952 / 8,559** |
| Total unknown decoded bytes | **21,830** |
| Global authored completion percentage | **Unmeasured** |

The **98%** objective is not a measured percentage: neither packed file
sizes nor decoded byte totals are a validated authored-byte denominator.
Reviewed original ASM is a separately recorded ownership lane, not
additional accepted C/C++ units. Source-written vendor library routines,
assets, writable DATA/BSS and alignment need distinct provenance.
There is **no accepted full packed EXE/COM reproduction**. The original
Japanese game copy has candidate-local-attested provenance, not an
independently proven pristine source image.

## Latest scoped progress

- Fresh exact Boss-source improvements: [Sara's 1,824-byte twelve-function context](../src/main/boss/sara/sara.md)
  now shares the red-cloud projectile setup while retaining two separate
  random-angle draws; [Shinki's complete 959-byte controller](../src/main/boss/shinki/update_context.md)
  shares genuine wing movement/callback and approach clock transitions;
  [Alice's complete 939-byte controller](../src/main/boss/alice/update_context.md)
  shares bullet-clear minimums and preserves the distinct phase/clock order.
  All three complete units passed two fresh Borland/TLINK producers, every
  original byte and ordered relocation, plus rejected compiled negatives.
  Previously accepted CODE receives **no duplicate byte credit**.
- Source-verified foreign Master 0.23 DATA: [FIL + DOS_ROPEN file defaults](reconstruction/MASTER_FILE_STATE_2026-11-12.md)
  account for **6 bytes in each MAIN, OP, MAINE**, and
  [PF buffer/error/key defaults plus RAND seed](reconstruction/MASTER_PF_RAND_DATA_2026-11-12.md)
  account for **9 bytes per executable**. This closes **45 unknown vendor
  DATA bytes**, with original author source where available, actual TASM
  source/LEDATA, MAP placement and original MZ comparison. The PF extra
  one-byte alignment in each remains **unknown**.
- [MAINE all-cast line counters](../src/maine/allcast/line_counters_initial.md)
  now have **four complete C++ semantic DATA bytes** from two native producers
  and a compiled negative. The model is source-exact but does not assert an
  identical historical C++/BSS translation-unit organization. Together the
  new DATA reviews reduce unknown by **49 bytes**.
- ZUN has seven additional real common-error-exit first-producer trials;
  these compiled to **261–263 bytes**, not the 269-byte native entry.
  [Their failures](reconstruction/ZUN_RESIDENT_REMOVAL_BRANCH_2026-11-12.md)
  and the still-nearest **269-byte/17-difference natural C++** are explicitly
  separate from accepted resident `cfg_init()` credit.

- Latest complete Boss source refinements: [Alice's X/Y puppet pursuit](../src/main/boss/alice/puppet_motion.md)
  **643 B**, [Yumeko's charged rotating spreads](reconstruction/YUMEKO_SPREAD_CHARGE_2026-11-12.md)
  **518 B** with real 354/428-byte sword compiler contexts,
  [EX-Alice's late firewave/gravity/diamond patterns](reconstruction/EXALICE_LATER_MIRROR_FAN_2026-11-12.md)
  **600 B**, and [Louise's full eight-phase controller](../src/main/boss/louise/update.md)
  **582 B**. All affected complete source units passed two original
  TCC/TLINK producers, raw bytes, ordered relocations and compiled negatives;
  already credited code is not counted twice.
- Two source-backed Master initialized-DATA closures now cover
  [TextVram/VSYNC](reconstruction/MASTER_TEXT_VSYNC_DATA_2026-11-12.md)
  **15 bytes** and [MEM allocator defaults](reconstruction/MASTER_MEMORY_INITIAL_2026-11-12.md)
  **8 bytes**, in each MAIN/OP/MAINE. Together these classify **69 vendor
  bytes** from original author ASM and native OMF. The final differing byte
  after each VSYNC initializer stays unknown.
- New authored C++ DATA: [MAINE registration page and name cursor](../src/maine/registration/initial_cursor_state.md)
  **3 B**, plus [MAIN Extra dialog-sequence byte](../src/main/dialog/sequence_initial.md)
  **1 B**. Complete original source types and consumer bindings are verified
  through four total new scalar bytes. These and 69 vendor bytes reduce
  global unknown by **73 bytes**.
- Four further natural C++ Yumeko sword-updater bounds/collision join tests
  all canonicalize to the same inexact **2,135-byte** nine-function output;
  see [the exact compiler blocker](reconstruction/YUMEKO_TWIRL_COMPILER_2026-11-11.md).

## Latest scoped progress

- The latest source work completed [EX-Alice's charged HP/callback ladder](reconstruction/EXALICE_CHARGED_ADVANCE_2026-11-12.md)
  (**1,060 B**), [Yumeko's mirrored sword fan](reconstruction/YUMEKO_MIRRORED_FAN_CONTEXT_2026-11-12.md)
  (**435 B plus 354-/428-byte dependent contexts**),
  [Mai/Yuki's six-function charge cohort](reconstruction/MAI_YUKI_CHARGE_AND_MUZZLES_2026-11-12.md)
  (**543 B**) and [Yuki's opening three attacks](reconstruction/YUKI_SOLO_OPENING_2026-11-12.md)
  (**509 B**). All complete affected compiler owners were reaccepted through
  two positive builds, original ordered relocations and the existing compiled
  negatives, without duplicate CODE credit.
- The original first-game DATA now separately owns the
  [16-bit character-resource loading flag](../src/main/runtime/load_playchar_initial.md)
  at `20A70..20A72`: **2 newly accepted C++ bytes**. The eight-word
  [Master clipping initializer](reconstruction/MASTER_CLIP_INITIAL_2026-11-12.md)
  also closes **16 foreign DATA bytes each** in MAIN, OP and MAINE, from
  the archived author ASM, native TASM LEDATA and complete target byte evidence.
  This removes 50 previously unknown bytes overall, of which only two
  are game-authored C++.

- Three full Boss source updates: [Yuki's three opening callbacks](reconstruction/YUKI_SOLO_OPENING_2026-11-12.md)
  **509 bytes**, [Mai/Yuki's six charge and first attacks](reconstruction/MAI_YUKI_CHARGE_AND_MUZZLES_2026-11-12.md)
  **543 bytes**, and [Yumeko's sword-fan patterns](reconstruction/YUMEKO_MIRRORED_FAN_CONTEXT_2026-11-12.md)
  **435 bytes plus 354/428-byte dependent contexts**. Each entire changed
  source cohort passed two original-compiler producers, complete bytes,
  original ordered fixups and the compiled negative. Already accepted CODE
  receives no duplicate credit.
- Two formerly unknown Master source gaps were recovered independently:
  [16-byte CODE-class LARGE_BYTE lookup](reconstruction/MASTER_LARGE_BYTE_2026-11-12.md)
  in MAIN and [19-byte private rtc_mod](reconstruction/MASTER_RTC_MOD_2026-11-12.md)
  in **each** OP/MAINE. Total **54 newly classified foreign bytes**,
  with real TASM source/OMF and zero C++ authored credit.
- The real first two MAIN `_DATA` bytes are now
  [signed debug frame step plus enable flag](../src/main/runtime/debug_frame_initial.md):
  **two newly accepted C++ initialized bytes** from explicit `db 0`
  writes, existing 445-/803-byte consumer functions and a compiled negative.
  An earlier one-byte [bullet special-group selector](../src/main/bullet/group_special_initial.md)
  was also accepted after the preceding handoff.

## Already solved — do not spend another turn reproducing them

- Main Boss controllers: [Sara](../src/main/boss/sara/sara.md) **1,824 B**
  across its twelve functions; Mai/Yuki shared **1,018 B**;
  [Shinki](../src/main/boss/shinki/update_context.md) **959 B** with a
  separate **802 B** Devil attack; [Alice](../src/main/boss/alice/update_context.md)
  **939 B**; [EX-Alice](../src/main/boss/exalice/update.md) **1,060 B**;
  [Yumeko](../src/main/boss/yumeko/update.md) **884 B**; Louise's
  complete control/attack families. Check the actual unit IDs/ledgers
  before claiming a new CODE extent.
- [Boss background family](../src/main/boss/BACKGROUND_CANDIDATE.md): all **19
  original-order functions / 3,254 bytes**, with **21 correctly ordered MZ
  relocations**, now reproduce from the coherent natural C++ source and two
  adjacent real compiler CODE contributions. Two independent producer binaries
  match the full joined interval. The 17 manifest functions were replayed and
  their accepted evidence refreshed; the 159-byte Shinki particle and 204-byte
  EX-Alice hexagram functions already have separate accepted owners and receive
  **no duplicate credit**. The former synthetic one-byte background origin
  hole is gone; preserve the original `keep_0` symbolic zero and true split
  before the last two EX-Alice functions when editing this context.
- The previously accepted [EX-Alice controller](../src/main/boss/exalice/update.md)
  **1,060 B** and [Mai/Yuki shared controller](../src/main/boss/mai_yuki/update_context.md)
  **1,018 B** have newly clarified source-level regular-wave/HP and
  paired-hit/reposition rules, respectively. Both **whole functions** were
  replayed twice with their original ordered fixups and compiled negatives;
  these are *source-quality improvements*, not a second CODE credit.
- Large Boss source quality also advanced on three complete original-order
  controllers: [Sara](../src/main/boss/sara/sara.md) **1,824 B / 12 functions**
  with shared mobile-wave hit scoring and reposition timers,
  [Alice](../src/main/boss/alice/update_context.md) **939 B** with proper
  beam/ring puppet formation state, and
  [Yumeko](../src/main/boss/yumeko/update.md) **884 B / 2 functions** with
  timed hit windows and phase-clock transitions. Every affected complete
  compiler owner passed two fresh TCC/TLINK builds, raw bytes, original
  ordered fixups and a meaningful compiled negative. These are refreshed
  *already accepted* CODE units, with **no duplicate authored credit**.
- [Shinki Devil](../src/main/boss/shinki/devil.md) **802 B** now uses
  a coherent symmetric-column firing rule in the **actual shared**
  `devil.inl`; one ordering mismatch was corrected and **all 12 dependent
  Shinki units** (including the 959-byte controller) were reaccepted exact.
  [Yuki](../src/main/boss/mai_yuki/yuki_update.md) **826 B** and
  [Mai](../src/main/boss/mai_yuki/mai_update.md) **786 B** share their
  individual solo wave-count/shot-bonus source protocols, while
  [Louise's](../src/main/boss/louise/later.md) **603 B / 4 functions**
  reuse one parameterized mirrored fan. Every changed full owner passed
  dual actual TCC/TLINK producers, ordered native relocations and compiled
  negatives. These refine existing CODE without recrediting its bytes.
- OP/MAINE now own the four genuine segmented
  [BGIMAGE plane pointers](../src/shared/hardware/bgimage_planes_initial.md)
  at `F9C4..F9CC` / `107D2..107DA`: two separate complete 8-byte
  C++ `_DATA` objects. Capture/free/rectangle-render consumers confirm
  all four 16-bit field addresses; both artifact-specific source units
  passed independent native compilation, original byte/fixup comparisons
  and their compiled nonzero-pointer negatives. This adds **16 new
  game-authored DATA bytes**, without touching nearby sound/memory state.
- The full [Mai/Yuki ten late attacks](reconstruction/MAI_YUKI_SHARED_PATTERNS_2026-11-12.md)
  **939 B** and **1,018 B** joint Boss update context now share the seven
  identical Yuki muzzle assignments and two Cheeto firing tails in their
  actual common `.inl`. **Both complete owners were replayed and accepted**,
  with all original bytes/ordered fixups, two positives and a rejected
  compiled negative. This refreshes already accepted CODE without new credit.
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
- Newly accepted native state: [EX-Alice laser slot and sweep X](../src/main/boss/exalice/attack_state_data.md)
  **4 C++ DATA bytes**, [full frame/STD counters](../src/main/runtime/frame_counter_data.md)
  **10 C++ DATA bytes**, and [item progress/attraction state](../src/main/item/state_data.md)
  **13 C++ DATA bytes**. These are complete, individually replayed original
  16-/32-bit initialized objects with actual large Boss, gameplay and
  process-handoff consumers and compiled negatives. The adjacent item
  alignment byte `[22855,22856)` is still unknown, not credited.
  [SE playback state](../src/shared/sound/se_initial_state.md) and
  [initial memory budget](../src/shared/memory/mem_assign_initial.md) add
  **six C++ plus six C initialized DATA bytes** across MAIN, OP and MAINE.
- Three newly recovered MAIN C++ initializers:
  [STD stage-script segment](../src/main/formats/std_segment_initial.md)
  **2 bytes** at `[21922,21924)`,
  [extend/high-score latches](../src/main/hud/score_extend_initial.md)
  **2 bytes** at `[21D42,21D44)`, and
  [playfield shake redraw clock](../src/main/playfield/shake_redraw_initial.md)
  **1 byte** at `[2191A,2191B)`. Each has an explicit matching ReC98
  `dw 0`/`db 0` source, real independently accepted code consumers, and
  exact complete Turbo C++/TLINK positive and compiled negative evidence.
  Adjacent uninitialized/alignment bytes remain unknown.
- OP Music Room's formerly unknown `[F9CE,FA32)` is now a complete
  [100-byte bitmap resource](reconstruction/OP_PIANO_BITMAP_RESOURCES.md):
  **28 black-key sprite bytes** from the original row-mask ASM plus **72
  font bytes** from the 9×8 original candidate BMP, corroborated by real
  TASM LEDATA, MAP publics and actual piano drawing consumers. These
  are resources, not C++ DATA or instruction credit.
- New MAIN game-authored initialized DATA: two
  [enemy lifecycle totals](../src/main/enemy/lifetime_totals_data.md) at
  `[21E74,21E78)` (**4 bytes**); the one-byte
  [shot-to-Boss collision flag](../src/main/player/shot_collision_flag_data.md)
  at `[22790,22791)`; and the one-byte
  [item auto-drop cycle](../src/main/item/drop_cycle_data.md) at
  `[227D2,227D3)`. All three have real independently accepted consumers,
  complete native C++ producer/negative evidence and zero MZ relocations.
  **Do not absorb neighboring unknown zero/alignment bytes.**
- Foreign Master 0.23 [BGM note/duration DATA](reconstruction/BGM_NOTE_LENGTH_OP_MAINE.md)
  has **two new original source-linked 176-byte tables** in OP/MAINE;
  [Master BYTE_MASK](reconstruction/MASTER_BYTE_MASK_OP_MAINE.md) adds two
  **8-byte tables** in those programs. Original archived author ASM,
  retained TASM ordinary LEDATA, original MAP publics, exact bytes and
  relocation provenance were independently rechecked. Existing MAIN copies
  are not claimed again. The [Borland C0L.OBJ startup](reconstruction/BORLAND_C0_STARTUP.md)
  adds **621 bytes of source-linked foreign CODE in each of MAIN/OP/MAINE**
  with the real 57 OMF fixes and link-frame changes. Total additional
  foreign ownership is **2,231 bytes**; it adds zero game-authored C/C++
  credit. The remaining 5-byte CRT CODE tail in each MZ remains unknown.
- Foreign CL.LIB [`exit`, `files`, `xxv` initialized DATA](reconstruction/CL_DATA_OWNERSHIP.md)
  now has full member-linked byte and original ordered relocation proof in
  all three executables: **2,124 bytes** moved out of unknown, **zero
  game-authored C++ credit**. Do not count the entire surrounding library
  gaps as owned.
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

**Unreviewed CDG state:** Native sources explicitly declare the matching
`_cdg_noalpha` byte as **`db ?`**, not initialized data. Its three native
zero locations remain unknown despite many accepted CDG loader consumers.
Do not claim them via a fabricated compiled zero initializer without new
provenance.

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

**ZUN follow-up:** Ninety additional actual Turbo C++ error-return forms
produced **32 source contributions of the right 269-byte length, none
exact**; a separate `TCC -S`/TASM32 producer emitted **272 bytes** and was
also inexact. Current maintained natural source is still the 269-byte,
17-difference success-first variant. Full first-producer results are in
[ZUN removal-branch findings](reconstruction/ZUN_RESIDENT_REMOVAL_BRANCH_2026-11-12.md).

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

**Additional Yumeko compiler-output route:** The `TCC -S`/TASM32/TLINK
single-producer experiments compiled the actual nine-function source to
**2,134 bytes (`-O-`)** and **2,135 bytes (`-O`)**, both against original
**2,139 bytes**. The strict compiler-assembly owner also rejected unreviewed
source segments. No original C++ sword-updater credit was added; see
[the native compiler review](reconstruction/YUMEKO_TWIRL_COMPILER_2026-11-11.md).

**Additional Yumeko diagnostics:** Three narrow `switch`-on-final-Y
compiler experiments, applied inside the real nine-function sword context,
produce **2,150 / 2,151 / 2,164 bytes** rather than the native **2,139**.
Some missing short jumps reappear, but the dispatch overhead breaks the
complete machine-code/fixup shape. These negative results are documented in
[the Yumeko compiler review](reconstruction/YUMEKO_TWIRL_COMPILER_2026-11-11.md)
with private runnable reproducer `.analysis/gpt-web-yumeko-local-switch-20261112.py`.
The accepted 283-byte reviewed ASM owner and inexact natural C++ candidate
remain unchanged; do not re-try these specific local switches unchanged.

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

A conservative local cleanup on **2026-11-12** removed **79 obsolete
unit-replay directories** and **11 orphaned one-off experiment outputs**,
freeing approximately **88.4 MiB of allocated storage**. At that cleanup checkpoint,
all **358 then-current distinct receipt hashes** still resolved to complete
saved directories. Later exact receipts have since been added; use the live
ledgers to identify their dependencies before any further cleanup. No pinned target, toolchain,
Wine prefix, calibration build, Ghidra project, ASM acceptance, or
Yumeko/ZUN diagnostic baseline was deleted. The public checkout remains
unchanged by these ignored-file deletions.

Older failed or duplicate replays not referenced by a current ledger
or useful live note may be removed to save storage; never delete a
receipt simply because the public repo does not list it as a Git file.
The acceptance JSON stores its SHA-256, not necessarily a pathname.
For a handoff to a *different computer*, preserve required ignored
inputs separately; the Git branch alone is not a self-contained build.
See [shared runtime setup](SHARED_TOOLS.md) and
[toolchain/oracle requirements](ORACLES.md).
