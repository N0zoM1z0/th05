# TH05 current handoff

Goal: at least 98% authored bytes exact. Commit prefix: `gpt-6.1-sol:`.
Repository: https://github.com/N0zoM1z0/th05 .

Current acceptance: **47 bounded C++ units / 130 complete function occurrences**,
23,859 compared bytes and 23,841 authored code bytes: 23,439 instructions plus
402 semantic compiler-table bytes. Eighteen checked padding bytes receive no
credit. MAIN has 89 functions / 16,014 code bytes, decoded OP 40 / 7,798,
decoded MAINE 1 / 29. Global denominator and percentage remain unreviewed.

## Retained evidence

All paths below are under private `.analysis/unit-replays/`.

| Scope | Receipt directory |
| --- | --- |
| Player angle, bullet tuning, Boss movement, resident CFG | `boss-cfg-a` |
| Boss explosion | `boss-explosion-a` |
| HUD overlay | `hud-overlay-a` |
| Four character shot owners | `reimu-shots-a`, `marisa-shots-a`, `yuuka-shots-a`, `mima-shots-b` |
| Bullet generation clipping | `bullet-clip-d` |
| Stage initialization | `stage-setup-a` |
| 17 complete Boss background functions | `boss-background-functions-a` (explicit subset) |
| Cheeto allocation/homing | `cheeto-update-b` |
| Regular/special bullet update | `bullet-update-d` |
| Enemy rendering from maintained TH04 C++ | `enemies-render-b` |
| Sound interrupt in MAIN / OP / MAINE | `main-kaja-a`, `op-kaja-a`, `maine-kaja-a` |
| OP startup and main menu | `op-main-menu-b` |
| OP setup and character selection | `op-setup-menu-a`, `op-character-menu-a` |
| Seven OP high-score viewer functions | `op-hiscore-scopes-a` (retained producer review) |
| OP configuration and music prefix | `op-config-b`, `op-music-prefix-b` |

Each accepted scope has two independent deterministic producers, full raw and
ordered-fixup comparisons, pinned tools, actual OMF dependencies and a compiled
semantic mutation control. Import rechecks saved MZ/MAP/OMF, wrappers and actual
compiler inputs. Symbol-only context is uncredited; whole-game linkage remains
open. Per-owner notes hold complete boundaries, ABI and bindings.

Three independent acceptance ledgers are `config/accepted_units.json`,
`accepted_units.op.json` and `accepted_units.maine.json`. OP/MAINE use pinned
retained decoded views, not fabricated MZ headers. Their proof includes packed
identity, original relocation order and two decoder load observations. Public
summaries need no private game/cache files. No packed-file equality is claimed.

Standalone ZUN `-M` is separately accepted: 311 complete COM bytes (142 code,
169 data), from semantic ASM with inferred original style. Evidence:
`.analysis/zun-memory/first-b` and `config/zun_memory_acceptance.json`. It does
not contribute C++ credit or establish complete outer ZUN equality.

## Incremental work

User steering: accelerate and replay only new or affected units. Use
`replay_units.py --plan` and `--units ID...`; add `--artifact op` or `maine` for
those contexts. No-work exits before tools/targets. Tool execution probes are
reused after manifest and actual installed tool/header/library identity checks.
Do not cold-replay old units, redo calibration or re-decode unchanged targets.

Multiple complete-function scopes in one TU compile once per fresh round.
Their MAP boundaries include unaccepted neighbors. `progress.py --accept
RECEIPT --units ID...` imports an explicitly passing subset without recompiling;
all saved results and the negative-control owner still undergo validation.
The original mixed receipt and aggregate verdict are unchanged.

New Japanese owners opt into `source_encoding = "cp932"`. Canonical maintained
inputs and snapshots stay UTF8; real compiler bytes have separate identities.
Import reconstructs positive/negative encoding and verifies the assembled alias.
Old MAIN owners remain raw. OP menu exercises actual CP932 Borland producers.
MAIN/MAINE shared sound units explicitly retain binary O; genuine MAINE source
uses a mixture of M/O/E contexts, so inspect real reference producer arguments.

## Open scopes and current next work

Boss background has 17 accepted functions / 2,891 bytes. Its particle renderer
remains 158 versus original 159 bytes (OR AX,AX versus CMP AX,0). The following
compiler contribution uses one uncredited origin hole outside all functions.
The entire 159-byte original particle function stays unaccepted. Hexagram
rendering's 204 raw bytes match, but ordered MZ fixups differ across a compiler
LEDATA boundary, so that whole function also stays unaccepted. Never sort or
normalize those differences.

Stage initialization's 189 initialized DATA bytes and OP menu's 1,089 DATA
bytes / 26 ordered fixups separately match both producers. These are retained
observations with no extra progress credit. Source BSS locations are checked,
not treated as initialized file bytes. OP menu's first scaffold stack displaced
BSS by 84h; omitting artificial stack allocation fixed layout without modifying
the game algorithm. See `BORLAND_NOTES.md` and owner notes for type/ABI lessons.

OP setup adds 1,439 code bytes / 12 functions, character selection 1,181 / 4,
and seven high-score viewer functions add 1,099 bytes. The latter reuse two
unchanged independently produced cold artifacts through the retained-scope
reviewer, which validates the entire original parent and mechanical scope
derivation without recompiling. The remaining 312-byte registration menu has
identical raw code but differing ordered fixups and stays unaccepted.
OP configuration adds 379 bytes / 3 functions and music prefix 381 / 4.
Music suffix and MAINE cutscene scopes remain under review. The cutscene's
52-byte EGC helper and 1,555-byte opcode dispatcher remain unaccepted.
The MAINE helper frames come from original bytes: sound's real frame E80
differs from calibration E7F. Maintain full enum domains and real structures;
no opaque opcode arrays, fake symbols, compiler-body ASM or inert barriers.

## Cached targets, routing and tools

`config/targets.toml` pins the supplied copy; provenance remains
candidate-local-attested. MAIN is ordinary MZ, OP/MAINE DIET-packed MZ, ZUN COM.
Decoded payloads/receipts are in `.analysis/decoded`. Reference calibration
builds complete but fail whole-file equality and create zero credit:
`main-calibration-b` (83 steps), `op-calibration-a` (47),
`maine-calibration-a` (36), under `.analysis/builds/`.

Private surveys route 21 OP shapes / 12,288 candidate bytes, 17 MAINE shapes /
5,678 bytes, and 63 maintained TH04 function shapes / 4,439 bytes. They are
routing only, including possible false complete boundaries and overlaps with
already accepted code. Reuse these maps; independently review original extents.

Pinned Borland tools have independent Wine state. Ghidra 12.1.3 / Temurin 21
are installed; `ghidra-project/TH05-main-loader` passes loader database byte /
fixup attestation and bounded disassembly. Full autoanalysis exceeded 768 MiB;
use loader-only and bounded ranges. Failed old projects are not evidence.
Serialize heavy tools with `.analysis/borland.lock` and `run_heavy.sh` (one CPU,
35% quota, 768 MiB, no swap, low priority). TH03 has unrelated dirty work: never
modify it. TH04 is a read-only reference.
