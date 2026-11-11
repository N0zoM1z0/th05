# TH05 reconstruction — next-agent handoff (2026-11-11)

## Read first

Work on local `main`. Start with [AGENTS.md](../AGENTS.md),
[exactness rules](ORACLES.md), `git status -sb` and
`python3 scripts/preflight.py`. Local work is ahead of `origin/main`;
**do not push** unless explicitly requested. Preserve and resolve any dirty
changes, including ignored diagnostics. The original Japanese image has
**candidate-local-attested** provenance, not an independently proven pristine
dump.

These files, not historical trial notes, are authoritative:

- [Accepted C/C++ ledgers](../config/accepted_units.json):
  also `accepted_units.op.json`, `accepted_units.maine.json` and
  `accepted_units.zun.json` in `config/`.
- [Reviewed ASM ownership](../config/reviewed_asm_families.json),
  [generated progress](PROGRESS.md) and
  [gapless ownership](../resources/ownership.json).
- `config/targets.toml` and `config/toolchain.toml`: pinned inputs;
  `.analysis/builds/`: real native calibration objects and linker MAPs.

**Current ledger snapshot:** 454 accepted bounded C/C++ units,
**124,781 authored source bytes** (108,784 CODE plus 15,997 initialized
DATA). This is *not* a percentage: the global authored-byte denominator
has not been accepted. Unknown ownership totals **42,947 decoded bytes**:
MAIN 6,578; OP 13,747; MAINE 14,063; ZUN 8,559. Recalculate from the
ledgers before quoting these numbers after further changes.

## Most useful next reconstruction work

**1. ZUN resident `-S`: natural C++ entry.**
The original `main()` is **269 bytes**, child COM `04A9..05B6`.
[Maintained source](../src/zun/resident/initialize.cpp) compiles to
**260 bytes** naturally. The separately accepted `cfg_init()` (322 B),
semantic DATA (320 B), C0T startup, and Master resident providers are
already solved. An experimental three-barrier ReC98-style source links
**269/269 exact bytes**, but its self-assignments and artificial empty
helper have no justified historical semantics; **never accept it as
natural C++**. Other real-control-flow tests (shared error exit,
separate labels) remain inexact. Start with the
[resident source and diagnostic explanation](../src/zun/resident/initialize.md).
Keep the full-link positive/negative private comparison under
`.analysis/gpt-web-zun-main-exact-diagnostic-*`.

**2. Yumeko sword lifecycle: original ASM exact, C++ alternative not.**
The **283-byte** `swords_update()` already has a reviewed ASM owner.
The natural [C++ alternative](../src/main/boss/yumeko/swords_update.cpp)
is not accepted. In the real nine-function `main_03` context,
`#pragma option -O-` yields the **correct 2,139-byte** combined CODE size
but emits short twirl-branch proxies. Switching on Borland jump optimization
(`-O`) produces the **correct two original near JL/JGE opcodes** at
updater offsets `+5E` and `+72`, but removes two unrelated two-byte jumps
in the bounds/collision paths: combined CODE becomes **2,135 bytes**.
The next task is a *natural* source flow that preserves both short jumps
and the near conditionals. See [compiler findings](reconstruction/YUMEKO_TWIRL_COMPILER_2026-11-11.md).
Useful private comparison outputs:
`.analysis/gpt-web-yumeko-newtwirl-baseline-native-a/` and
`.analysis/gpt-web-yumeko-conditional-long-baseline-optim-native/`.
Do not insert NOPs, copied instructions, or optimizer barriers.

**3. Other unknown code/data.**
Use `resources/ownership.json` and real function/SEGDEF boundaries.
Unknown is not synonymous with game-authored code: it also includes
foreign writable DATA/BSS, unreviewed library CRT, alignment, and resources.
Prioritize a *complete* recoverable original function rather than filling
adjacent gaps. Review the
[resolved/unresolved candidate index](reconstruction/UNACCEPTED_COHORTS.md)
before reviving an old experiment.

## Do not repeat already accepted work

| Family | Accepted source status and useful evidence |
| --- | --- |
| Large game C++ controllers | MAIN Mai/Yuki **1,018 B**, Shinki **959 B**, Alice **939 B**, Extra Alice **1,060 B**, Yumeko **884 B**; MAINE cutscene VM **1,555 B** and major Staff controller/update/render functions. Their existing acceptance receipts remain current; recent Yumeko and Shinki phase-name edits were twice recompiled exactly. [Boss overview](../src/main/boss/yumeko/update.md), [Shinki](../src/main/boss/shinki/update_context.md), [MAINE](../src/maine/cutscene/cutscene.md). |
| MAIN reviewed ASM and Master | The [MPN loader](../src/main/formats/mpn_loader.md) is now one complete **92-byte game-specific reviewed ASM** owner (90 authored instructions, two checked linker NOPs) with two exact native producers and a rejected compiled negative. Separate original-assembly owners also cover swords, graphics, BGM, memory and file functions. The [circle helper review](reconstruction/MASTER_CIRCLE_HELPERS_NATIVE.md) assigns 223 full source-written Master CODE bytes, leaving the differing alignment byte at `121B` unknown. A [further Master source review](reconstruction/MASTER_GAP_FUNCTIONS_NATIVE.md) resolves 17 complete functions / 1,079 original vendor CODE bytes. The earlier [PFINT21 review](reconstruction/MASTER_PF_NATIVE.md) adds **805 real source-written CODE bytes**; the 2-byte dispatch word and one-byte alignment stay unknown. [Master geometry](reconstruction/MASTER_GRCG_NATIVE.md), [SUPER](reconstruction/MASTER_SUPER_NATIVE.md), [file/memory](reconstruction/MASTER_FILE_MEMORY_NATIVE.md). |
| OP/MAINE vendor | Original CL.LIB `xxas`/`signal`/`setenvp` and related members are **already recovered as vendor CODE**; not open game-C++ tasks. [Vendor context](reconstruction/VENDOR_CONTEXT_REVIEW.md), [string runtime](reconstruction/CONTEXT_STRING_RUNTIME.md), [Master functions](reconstruction/CONTEXT_MASTER_LARGE.md), [large PI decoder](reconstruction/CONTEXT_PI_PACK.md), [render helpers](reconstruction/CONTEXT_SUPER_HELPERS.md). |
| Embedded data | MAIN **2,752 B** original bitmap/preshift tables and ZUN **8,192 B** font bitmap are resources, not CPU instructions or authored C++. [Sprites](reconstruction/MAIN_SPRITE_BITMAPS.md), [font](reconstruction/ZUN_FONT_RESOURCE.md). |
| ZUN packed children | Independent accepted/reviewed scopes for `-O`, `-I`, `-G` and `-M`, but **no full packed-file exactness** or accepted resident `-S` `main()`. [Launcher](../src/zun/launcher/README.md) and [resident](../src/zun/resident/initialize.md). |

The 55-byte BB loader, 55-byte near-vector helper, and 40-byte scroll
coordinate helper also have exact **reviewed ASM** owners. Their
ordinary C++ variants being inexact does not make the executable bytes
unknown.

## Fast exactness workflow

For changed executable inputs, replay **only affected complete units**
with their original ordered MZ fixups and meaningful compiled negative:

```sh
python3 scripts/replay_units.py --units UNIT_ID --output .analysis/unit-replays/NEW_RUN
# OP/MAINE/ZUN: add --artifact op|maine|zun
python3 scripts/progress.py --accept .analysis/unit-replays/NEW_RUN/receipt.json --units UNIT_ID --write
python3 scripts/ownership.py --write
python3 scripts/ci.py
git diff --check
git commit -m "gpt-web: describe exact change"
```

ASM families use `scripts/replay_asm_family.py` and a separate source
classification. Stop after a complete-size/byte failure rather than
crediting fragments. For documentation-only changes, review the diff:
**no cold replay, receipt refresh, or full tooling suite** is required.
Commit locally; never push without permission.

## Local workspace and storage

`.analysis/` is ignored and is the private working set. **Keep** its
original targets, pinned Borland/Wine toolchain, native calibration
objects/MAPs, Ghidra data, the **336 locally present current accepted
replay receipts**, and the highlighted unresolved ZUN/Yumeko diagnostics.
A conservative 2026-11-11 cleanup removed **198 obsolete local outputs**:
20 no-longer-current and unreferenced unit replays; 108 unreferenced
one-off experimental directories; 44 superseded import/progress JSON
snapshots; and 26 redundant unsuccessful Yumeko native builds.
Allocated `.analysis` space fell from about **911 MiB to 835 MiB**
(approximately **76 MiB saved**). The two key Yumeko compiled
comparisons and all relevant experiment scripts remain. Historical
experiments referenced by source notes are otherwise preserved.
Only ignored local caches were deleted; the accepted ledgers and
Git-tracked source are unchanged by that cleanup.
