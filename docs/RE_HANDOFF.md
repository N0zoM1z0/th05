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
has not been accepted. Unknown ownership totals **27,908 decoded bytes**:
MAIN 4,922; OP 7,059; MAINE 7,368; ZUN 8,559. Recalculate from the
ledgers before quoting these numbers after further changes.

The original [MAIN standard-stage filename](../src/main/stage/std_filename.md)
now has its own **nine-byte, two-producer, negative-controlled natural C DATA**
owner at `21924..2192D`. The following separator zero remains unknown. The
adjacent [score-file/continue-name DATA](../src/main/score/resource_names.md)
continues to own `2192E..21942` independently, with no byte counted twice.

The [BFNT/EDGES/BYTE_MASK/BGM initializer review](reconstruction/MAIN_MASTER_LITERAL_TABLES.md)
now owns **333 original Master third-party initialized-DATA bytes**:
eleven complete source-defined scopes including Epson notebook IDs, IBM
video/font DOS device names, the full 16-color RGB palette, and the original
VRAM, joystick, machine and palette runtime defaults. The independent
original MAP publics, genuine OMF LEDATA and full source declarations protect
all zero-initialized field boundaries. Its source-derived
`UNDF` note sentinel is 100. The adjacent alignment zeros, `intdiv`, and
writable foreign DATA remain unknown; none of these tables is game-authored
C++ or part of the accepted denominator.

The original [Master ATAN8 lookup review](reconstruction/MAIN_ATAN8_NATIVE.md)
now attributes 256 source-written initialized DATA bytes at MAIN
`20C2E..20D2E` from the complete, byte-identical original author ASM,
real TASM OMF and original/calibration MZ. Its two following data-alignment
zeros are deliberately **unknown**; this earns no game-authored credit.

The [MAIN pause-screen text](../src/main/resources/pause_spaces.md) and
[demo/EMS/face filename bank](../src/main/resources/session_files.md) now
have two separately accepted *natural C initialized-DATA* owners at
`20BDD..20BEC` (15 bytes) and `20BEC..20C2E` (66 bytes). Each exactly matches
its original semantic strings with two native producers and a real compiled
negative. The following source/foreign DATA is a separate unknown boundary;
neither accepted unit provides a hidden copy of the other.

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
| Large game C++ controllers | MAIN Mai/Yuki **1,018 B**, Shinki **959 B**, Alice **939 B**, Extra Alice **1,060 B**, Yumeko **884 B**; MAINE cutscene VM **1,555 B** and major Staff controller/update/render functions. Their existing acceptance receipts remain current; recent Yumeko phase names and the Shinki typed scratch-state overlays were twice recompiled exactly. The Shinki [state review](../src/main/boss/shinki/update_context.md) covers all 12 impacted units (3,467 bounded bytes), including the 959-byte main controller and 802-byte Devil body. [Boss overview](../src/main/boss/yumeko/update.md), [Shinki](../src/main/boss/shinki/update_context.md), [MAINE](../src/maine/cutscene/cutscene.md). |
| MAIN reviewed ASM and Master | The [MPN loader](../src/main/formats/mpn_loader.md) is now one complete **92-byte game-specific reviewed ASM** owner (90 authored instructions, two checked linker NOPs) with two exact native producers and a rejected compiled negative. Separate original-assembly owners also cover swords, graphics, BGM, memory and file functions. The [BFNT entry review](reconstruction/MAIN_BFNT_ENTRY_NATIVE.md) assigns another 322 complete source-written Master CODE bytes, including a 302-byte image/font-entry function. The [circle helper review](reconstruction/MASTER_CIRCLE_HELPERS_NATIVE.md) assigns 223 full source-written Master CODE bytes, leaving the differing alignment byte at `121B` unknown. A [further Master source review](reconstruction/MASTER_GAP_FUNCTIONS_NATIVE.md) resolves 27 complete functions / 1,516 original vendor CODE bytes, including three private SUPER/linework routines and seven further complete file, machine, memory and packed-file decoder procedures; their adjacent two non-procedure bytes remain unknown. The original [Master BGM review](reconstruction/MASTER_BGM_NATIVE.md) also owns the complete private `BGM_BELL` speaker kernel at `3AAE..3B16` (104 B, two real OMF fixups) and `BGM_GETNUMBER` decimal duration reader at `36C0..36E8` (40 B, no fixups). The earlier [PFINT21 review](reconstruction/MASTER_PF_NATIVE.md) adds **805 real source-written CODE bytes**; the 2-byte dispatch word and one-byte alignment stay unknown. [Master geometry](reconstruction/MASTER_GRCG_NATIVE.md), [SUPER](reconstruction/MASTER_SUPER_NATIVE.md), [file/memory](reconstruction/MASTER_FILE_MEMORY_NATIVE.md). |
| OP/MAINE vendor | Original CL.LIB `xxas`/`signal`/`setenvp` and related members are **already recovered as vendor CODE**; not open game-C++ tasks. [Vendor context](reconstruction/VENDOR_CONTEXT_REVIEW.md), [string runtime](reconstruction/CONTEXT_STRING_RUNTIME.md), [Master functions](reconstruction/CONTEXT_MASTER_LARGE.md), [large PI decoder](reconstruction/CONTEXT_PI_PACK.md), [render helpers](reconstruction/CONTEXT_SUPER_HELPERS.md). The [Master archive/display, BFNT, DOS, EGC, and OP trapezoid hooks](reconstruction/CONTEXT_MASTER_HOOKS.md) now account for 9,139 original source-linked CODE bytes across OP/MAINE, including two complete 296-byte PFOPEN routines and 406 source-written bytes inside each 408-byte PFEND. Each 2-byte PFEND runtime slot stays unknown. The same review also covers eight original BFNT entry/header functions, 964 bytes in all. It additionally covers 24 original DOS, buffering and EGC helper bodies (908 bytes), 34 early palette, file and GRCG functions (1,736 bytes), and 18 complete packed-file I/O and random functions (796 bytes), including the GAME=5 archive-key decoding change. The same review now adds four whole OP residency-palette and trapezoid functions (418 bytes). The adjacent `SOUND_JOY` is a distinct reviewed ASM owner, not part of the rasterizer. Another 13 complete display, machine-identification and integer-square-root functions add 574 source-backed vendor bytes; the `__AHINCR` MAP symbol must not truncate the complete 126-byte `GET_MACHINE_98` source procedure. Both machine-detector bodies and both `GRCG_OFF` leaf functions are now source-linked in full. Another 13 source-backed font, graphics, text-clear, palette and memory functions (920 bytes) are now complete, including two 138-byte `SUPER_ENTRY_BFNT` functions. The native OP text-command dispatcher and MAINE `TEXT_PUTSA` add 142 more source CODE bytes, while their two 4-byte non-LEDATA tail holes remain unknown. The [source-derived GRAPH_PACK_PUT_8_NOCLIP review](reconstruction/CONTEXT_GRAPH_PACK_NOCLIP.md) additionally resolves 196 bytes in each artifact, via the original Master routine with three Y-clip instructions removed. The [BGM timer/PSG source review](reconstruction/CONTEXT_BGM_TIMERS.md) resolves another 1,224 original CODE bytes: 7 complete sound functions per OP/MAINE, including 280-byte timer interrupt hooks and genuine `_TEXT`/DGROUP segment relocations. The [RTC/memory/VSYNC source review](reconstruction/CONTEXT_MEMORY_VSYNC.md) resolves 1,598 original CODE bytes: 14 procedures per artifact, including the full RTC interrupt setup/handler, independent private near VSYNC helpers and genuine segment fixups. The 19-byte gap between each RTC setup and handler stays unknown. The [machine-detection review](reconstruction/CONTEXT_MACHINE_DETECT.md) resolves another 868 original vendor bytes in eight complete functions, including two 342-byte AT probes. |
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

The [OP joystick initialization](../src/op/joystick/js_start.md) now has one
new **42-byte reviewed ASM source owner** (`JS_START`, OP `2BAC..2BD6`):
41 source instructions and one checked alignment NOP, with two original-byte
exact TASM producers and a rejected poll-count negative. The obsolete SAJ-98
search is intentionally absent; external sound functions and DATA/BSS remain
symbol-only, not claimed as reconstructed CODE.
The [MAINE joystick startup](../src/maine/joystick/js_start.md) now similarly
owns **60 complete original ASM bytes** at `2E46..2E82`: 41-byte `JS_START`
and 17-byte near `SOUND_JOY` instruction bodies, plus two checked alignment
NOPs. Both functions, external sound references, MAINE's own DATA/BSS frame
and the original ordered fixups passed independent scoped producers and a
rejected poll-count mutation. The following joystick sense function is now
independently reconstructed, with its own original near helper and boundary.

The [OP PSG reader](../src/op/joystick/sound_joy.md) is now a separate 18-byte
reviewed ASM function at `2CA8..2CBA` (17 instructions, one NOP). The
[OP/MAINE joystick sense implementation](../src/shared/joystick/sense.md)
reconstructs two original 21-byte intervals at `2CBA..2CCF` and
`2E82..2E97`: each contains both the far `JS_SENSE` and a separate near
`SAJOUT`. All three underwent independent exact TASM/TLINK double builds and
compiled semantic negatives. The final zeros at OP `2CCF` and MAINE `2E97`
are still unknown; original Master KOIZOID ownership ends before `SOUND_JOY`.

MAIN's [game-specific joystick initialization](../src/main/joystick/js_start.md)
and [far joystick sensor](../src/main/joystick/js_sense.md) now own the two
complete exact ASM functions at `363E..3668` (42 B, one checked NOP) and
`367A..3686` (12 B). Original `SOUND_JOY` and `SAJOUT` remain separate vendor
owners, and the byte at `3679` remains unknown. These two independent
native-replay receipts add 53 source instruction bytes, not a new C++ owner.
