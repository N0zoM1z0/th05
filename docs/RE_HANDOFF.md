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

## Verified current scope (separate authorship classes)

The current accepted source is broader than the original C++ function list:
C/C++ CODE and initialized DATA, reviewed handwritten ASM, CL.LIB/Master
vendor CODE/DATA, and embedded assets are **different ownership classes**.
Never infer instruction or authored percentage from a CODE SEGDEF or from a
synthetic combined COM. Use the ledgers and generated ownership map for
current counts rather than copying old checkpoint totals into reports.

| Area | Current exact result | Evidence and limits |
| --- | --- | --- |
| MAIN large game functions | Mai/Yuki update **1,018 B**, Shinki update **959 B**, Alice update **939 B**, Yumeko update **884 B**, MAINE cutscene VM **1,555 B**; many other Boss/Staff owners in the table below | Already accepted C++; do not reopen older 1-byte/fixup failure notes as missing functions |
| MAIN vendor CL.LIB | `farheap`/`exec` **2,040 object-written CODE bytes** (8 CS: state bytes remain unknown), `setenvp` **88 CODE bytes**, C0L **144 initialized DATA bytes** | [Original OMF reviews](reconstruction/CL_VENDOR_OWNERSHIP.md); **zero game-authored credit** |
| OP/MAINE vendor CL.LIB | Each has **2,040 source-written CODE bytes** across `farheap` and `exec`; four original runtime-state gaps total **16 bytes** across both EXEs. Another **3,917 complete CODE bytes** are source-exact: OP `xxas` (143), `signal` (769), `setenvp` (88); MAINE `setenvp` (88), `new` (754), `xxas` (143), `signal` (769), `_pathops` (208) and `xmsg` (955) | [Context review](reconstruction/VENDOR_CONTEXT_REVIEW.md); all state gaps and CODE members' foreign DATA/BSS remain unknown |
| OP Music Room | Twelve chromatic key-top mask bytes at `DB01..DB0D` exactly reproduced | [Piano top masks](../src/op/piano/pressed_top.md): **semantic CODE data, zero CPU instructions** |
| ZUN.COM inner and outer dispatch | Outer **371 B**, inner dispatcher/catalog/transfer **558 B** independently exact | [Outer](../src/zun/launcher/outer.md) and [inner](../src/zun/launcher/README.md); no child bytes transferred between sources |
| ZUN.COM children | Separate exact `-O` **926 B**, `-I` **1,009 B**, `-G` **8,377 B**, and `-M` **311 B** child proofs | [ADPCM](../src/zun/adpcm/README.md), [interrupt](../src/zun/interrupt/README.md), [gaiji](../src/zun/gaiji/README.md); font resources and BSS are not executable instructions |
| ZUN `-S` resident | Accepted **322 B** `cfg_init()` C++ CODE, **320 B** C++ initialized DATA; **1,056 B** Master vendor assembly, and **723 source-written B** C0T vendor CRT CODE/DATA | [Resident status](../src/zun/resident/initialize.md), [CRT](../src/zun/resident/crt_native.md), [semantic DATA](../src/zun/resident/semantic_data.md); the **269 B C++ `main()` is not accepted** |

The last [source-built ZUN envelope diagnostic](../src/zun/launcher/README.md)
compares **13,250 of 18,116** original bytes in a nonoverlapping synthetic
layout, leaving 4,866 bytes zero-filled. Its `-S` composition includes 1,698
bytes from separate C++/Master producers; C0T has separate provenance but was
**not included in that composite total**. No claim of an exact full launcher
or complete `-S` child follows from this integration.

## Major accepted source — avoid repeating superseded trials

Check the acceptance IDs before acting on old experimental notes. The
[generated progress](PROGRESS.md) and [ownership map](../resources/ownership.json)
are the complete, current inventories; these highlights are only the larger
or historically confusing cases.

| Area | Complete accepted scope | Evidence |
| --- | --- | --- |
| MAIN Mai/Yuki Boss | **1,018-byte** update controller, **939-byte** remaining patterns, **186-byte** tracking laser | [Controller](../src/main/boss/mai_yuki/update_context.md), [patterns](../src/main/boss/mai_yuki/later_patterns.md) |
| MAIN Shinki Boss | **959-byte** update, **220-byte** ball updater, **386-byte** wing preparation, **159-byte** particle renderer | [Update](../src/main/boss/shinki/update_context.md), [ball/wing](../src/main/boss/shinki/shinki.md), [renderer](../src/main/boss/shinki/particles_render.md) |
| MAIN Alice / Extra Alice Boss | **939-byte** Alice update; **1,060-byte** Extra Alice update; **140-byte** Alice foreground plus **381-byte** puppets | [Alice](../src/main/boss/alice/update_context.md), [Extra](../src/main/boss/exalice/update.md), [foreground](../src/main/boss/alice/foreground.md) |
| MAIN Yumeko Boss | **884-byte** update; **354/428-byte** attacks; **283-byte** sword lifecycle exact *reviewed ASM* | [Update](../src/main/boss/yumeko/update.md), [attacks](../src/main/boss/yumeko/laser_swords.md), [swords](../src/main/boss/yumeko/swords_update.md) |
| MAIN midboss and defeat | **65-byte** midboss defeat, **414-byte** Boss defeat and **43-byte** player collision, all accepted | [Midboss](../src/main/midboss/default.md), [generic Boss](../src/main/boss/generic.md) |
| MAIN dialog/runtime | **456-byte** dialog interpreter, **803-byte** stage initializer, **280-byte** player movement ASM | [Dialog](../src/main/dialog/opcode.md), [stage](../src/main/runtime/stage_session_context.md), [player](../src/main/player/region_register.md) |
| MAIN loaders/score | **184-byte** STD loader, **168-byte** high-score insertion, **159-byte** far-vector pair | [STD](../src/main/formats/std_load.md), [score](../src/main/score/continue_raw.md), [vector](../src/shared/math/vector_far.md) |
| MAINE script and Staff | **1,555-byte** cutscene VM and **991/626/861-byte** Staff controller/update/render | [Cutscene](../src/maine/cutscene/cutscene.md), [Staff](../src/maine/staff/staff.md) |
| OP Music Room | **218-byte** piano setup, **116-byte** renderer, **30-byte** note lookup, plus the separate 12-byte note-top table | [Piano source](../src/op/piano/setup_exact.md), [render](../src/op/piano/render_exact.md), [note](../src/op/piano/note_register.md) |
| Shared sound and input | MAIN/OP/MAINE sound effects **57 + 76 B** per binary and **262-byte** BIOS scanner per binary | [Sound](../src/shared/sound/se.md), [input](../src/shared/hardware/input_sense_op_maine.md) |

The 55-byte BB loader, 55-byte near-vector helper and 40-byte scroll
coordinate helper also have exact *reviewed ASM* owners. Only their ordinary
C++ alternatives remain inexact, not the machine-code ownership.

## Open work for the next agent

**Highest-value genuine code problem:** ZUN `-S` `main()` at COM
`04A9..05B6`, **269 bytes**. Two native direct TCC/TLINK experiments are
raw-exact under authentic `_INIT_`/BSS framing, but only with three explicit
ReC98 optimizer barriers; those are diagnostic constructs, not trustworthy
original source. The [resident investigation](../src/zun/resident/initialize.md)
keeps the exact and negative experimental evidence. Do **not** accept those
barriers as natural C++ or paste generated instructions. Try source-level
control flow that authentically preserves the three independent error exits.

**Other unresolved origin reviews:** OP's `xxas`, `signal` and `setenvp`,
and MAINE's `setenvp`, have now been recovered as exact native CL.LIB
contributions, not new authored Boss code. The remaining foreign DATA/BSS,
runtime state slots and larger unknown ownership intervals near CRT startup
should be classified using native function/SEGDEF boundaries. [Source candidates and
resolved historical failures](reconstruction/UNACCEPTED_COHORTS.md) provide
context; their earlier diagnostics are not current acceptance status.

**Author-language alternative:** Yumeko's 283-byte `swords_update()` has a
complete *reviewed ASM* owner, while its ordinary C++ alternative still
lowers two twirl jumps differently. See
[sword update notes](../src/main/boss/yumeko/swords_update.md). This is a
source-language refinement, **not missing executable ownership**. Major
Mai/Yuki, Shinki, Alice, Yumeko and Staff state machines are already
accepted in the primary ledger.

## Exactness workflow and cache hygiene

Run `git status -sb` and `python3 scripts/preflight.py` before source work.
Compile/replay **only affected complete units** (`scripts/replay_units.py
--artifact main|op|maine --units ID --output NEW_DIR`; use
`scripts/replay_asm_family.py` for supported original-ASM families). Require
two independent native producers, complete bytes and **original ordered**
MZ fixups, actual OMF/MAP and a meaningful compiled negative. For successful
new source, accept the receipt, regenerate progress/ownership, check `git
diff --check`, then commit `gpt-web: xxx`. Documentation changes require no
native replay; do not run a full cold replay for handoff cleanup.

The ignored `.analysis` directory holds the private original targets, decoded
views, attested Borland/Wine toolchain, calibration MAPs, accepted replay
receipts and some valuable failed compiler experiments. **Keep these.** On
2026-11-11, a conservative local cleanup removed **126 unused paths**:
no-receipt unreferenced failed replay directories, redundant generated
adoption/progress logs and JSON snapshots, and Python caches. `.analysis`
shrank from approximately **895 MB to 868 MB** (filesystem `du -sh`). No
accepted receipt, original target, calibration build or toolchain was deleted.
Ignored-cache deletion is local; the Git commit records the updated handoff,
not the removed binary cache itself.

Historical experiment notes may accurately describe *then-failed* candidates;
read their later accepted sections and the **current ledgers** before
repeating a resolved issue.
