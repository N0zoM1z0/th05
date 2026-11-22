# TH05 reconstruction — handoff (2026-11-15)

## Start here

1. Read [AGENTS.md](../AGENTS.md), [the workflow](RE_WORKFLOW.md) and the
   [exactness contract](ORACLES.md).
2. Check `git status -sb` and `git log -5 --oneline` before editing, and keep
   any in-progress changes from another agent.
3. For counts, use [generated progress](PROGRESS.md), the four accepted-unit
   ledgers and [`resources/ownership.json`](../resources/ownership.json). This
   file does not repeat totals.

Work on `main` and commit locally with your workstream's prefix (`gpt-web:` or
`claude-opus-5.5-high:`). Push only with permission. The supplied Japanese copy
is `candidate-local-attested`. ReC98 and sibling-project acceptance does not
transfer here.

## Current state

`resources/ownership.json` measures the authored denominator: 144,267 of
144,269 authored-candidate bytes are exact (99.999%). Exact bytes come from
accepted C/C++, reviewed original ASM and the reviewed ZUN COM modules. Vendor
code and data, assets, BSS, padding and the zero-credit rows in
`config/reviewed_gaps.json` don't count. Each of those rows is checked against
the original bytes.

All six large MAIN Boss controllers have complete accepted coverage. `src/`
comments now describe the code and ZUN's bugs in plain English. Behaviour
and code-generation findings live in each directory's `NOTES.md` (`README.md`
under `src/zun/`). The remaining per-unit notes are ones an ASM family or
ledger lists as an input, plus a few layout references.

## Open items

- **MAIN `[21E78,21E7A)`**: the last 2 unknown bytes, two zeros between the
  enemy lifetime totals and the sparks sprite (`_sSPARKS` is `14AA`). No code
  operand addresses `14A8`, so their identity can't be proved from code.
- **`main-scroll-coordinate`** stays `missing` in `replay_units.py --plan` on
  purpose. It is an exact C++ alternative over the same 40 bytes as the
  accepted reviewed-ASM owner; don't pass it to `progress.py --accept`. See
  [`coordinates.md`](../src/main/scroll/coordinates.md).
- **BB resource loader**: the C++/`__emit__()` hybrid reproduces all 55 bytes,
  but the reviewed ASM stays the only owner. See
  [`formats/NOTES.md`](../src/main/formats/NOTES.md).
- **Near Vector2**: natural C++ is 67 bytes against the 55-byte ASM owner (a
  12-byte register-copy residual). See
  [`vector2_near.md`](../src/shared/math/vector2_near.md).

- **Position independence**: the DOS product passes three shifted relinks
  and a demo run ([DOS_POSITION_INDEPENDENCE.md](reconstruction/DOS_POSITION_INDEPENDENCE.md)).
  `audit_unit_pi.py` covers every accepted unit at object level.
- **Product integration**: `build.py` now links 99 MAIN and 18 MAINE units in
  place of ReC98 dump procedures ([DOS_BUILD.md](DOS_BUILD.md)). Next: cut
  functions from ReC98 C++ translation units (dialog, boss_6, laser, boss_bg,
  score_rm, gather, midboss and the whole-TU sound/exit/input ones), then the
  72 units whose module is a ReC98 TU path, special pipelines and OP.
- **Private verification**: `python3 scripts/audit_ledgers.py` and
  `ownership.py --check --verify-targets` both pass (2026-11-22). Run them after
  changing a reviewer or ledger.

The ZUN `-S` child's vendor bytes and its resolved small gaps are in
[ZUN_CHILD_OWNERSHIP.md](reconstruction/ZUN_CHILD_OWNERSHIP.md).

## Exact-work loop

- Documentation-only changes need no compiler replay, preflight or full CI;
  inspect the diff.
- For source changes, check `python3 scripts/replay_units.py --plan`, then
  replay only the affected owners and consumers (`--artifact op`, `maine` or
  `zun` for the other ledgers). Never cold-replay everything.
- Acceptance needs two deterministic producers, complete raw bytes, original
  ordered fixups and the shared compiled negative. ASM and vendor work uses its
  own focused replay. A build, size match or note alone is not acceptance.
- Update `docs/PROGRESS.md` and ownership only when accepted facts change.
  `python3 scripts/ci.py` is the public check: syntax, ledgers, ownership and
  every reviewed vendor/ASM/ZUN decision, listed once in its `STRUCTURAL`
  table. `--full` adds the tooling tests in `tests/` (about 10 s, all green
  without private inputs). New checks go in that table, not in a second
  CI script.

```sh
python3 scripts/replay_units.py --plan
python3 scripts/replay_units.py --units UNIT_ID --output .analysis/unit-replays/RUN
python3 scripts/progress.py --accept .analysis/unit-replays/RUN/receipt.json --write
python3 scripts/ownership.py --write
python3 scripts/ci.py
```

`replay_units.py` needs compiler-assembly and initialized-DATA units replayed
one per call, and a batch can't mix conflicting module contexts.

### Re-accepting after a shared-header edit

A comment edit in a shared header touches more than the C++ ledgers:

1. Replay the ASM families that list the header in `semantic_inputs`
   (`replay_asm_family.py --plan`; the pinned `native-review.json` is found by
   its hash under `.analysis/asm-replays/`) and accept them in one call.
2. Refresh the adoption digests in `config/reviewed_asm_families.json`,
   `config/reviewed_enemy_vm_unit.json` and `config/reviewed_zun_crt.json`.
3. Run `review_zun_brk.py --write`.

Edits under `src/zun/` also change the ZUN CRT receipt inputs; its accepted
config receipt path is set in `config/zun_crt.toml`.

## Lessons worth keeping

- **Judging ASM owners.** A ReC98 `.cpp` alone doesn't prove compiler origin
  (`snd_load` is "a decompilation of ZUN-written ASM", ReC98 01c92da1).
  Separately assembled ReC98 TUs (`player.asm`, `spark_a.asm`, `bullet*.asm`,
  `hud_*.asm`, `cdg_put.asm`, `cdg_load.asm`, `pi_asm_*.asm`, `input_s.asm`,
  `vector2n.asm`, `hfliplut.asm`, ...) are ZUN's ASM. Register arguments,
  BX-relative frameless entries, `LOOP` and BP-as-data are ASM shapes. The
  laser geometry/ray/hittest TU (348 bytes) is TCC output, but nearly every
  instruction would need an opcode emit, so it stays ASM.
- **Reclassified to C++.** Gather template copies, `tiles_invalidate_*`,
  `cdg_put_noalpha_8`, `egc_copy_rect_1_to_0_16`, Yumeko `swords_update` and
  `hitshot_from` were once "handwritten" ASM owners and are now exact C++.
- **Zero runs.** A "fewer than 16 zero bytes ending on a paragraph" alignment
  rule misfiled ZUN `__heaplen`, MAINE's VSYNC CS words and OP `kbhit` DATA.
  Multi-byte alignment is now limited to the CODE→DGROUP paragraph pad; other
  zero runs need source or OMF evidence. Search raw operand bytes for readers,
  not just a linear disassembly (ZUN `[225A,225C)` turned out to be
  master.lib's `file_sharingmode`). A zero DATA word doesn't name its variable
  either: an early Stage Clear source matched zeros at `[222B4,222B6)` that
  belong to `_explosion_big_frame` ([stage notes](../src/main/stage/NOTES.md)).
- **Pinned scripts.** The verifier no longer hashes Markdown notes or
  `scripts/` in the ASM/C++ acceptance paths, but many vendor reviewers still
  self-hash their own scripts. Avoid editing `scripts/lib/unit_oracle.py`,
  `review_master.py` and similar libraries unless you will clear those gates.

## Local inputs

`.analysis/`, `_reference/`, `.tools/` and `ghidra-project/` are ignored local
state that Git does not carry. Keep the pinned targets, Borland/Wine toolchain,
Ghidra project, ledger-referenced receipts and producers, and accepted native
or vendor evidence; another machine needs them copied separately. Before
deleting evidence, check ledger hashes and tracked references rather than age
or name.
