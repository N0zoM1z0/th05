# TH05 handoff

Goal: at least 98% authored bytes exact from maintained source. The global
authored denominator and percentage remain unreviewed; the goal is not complete.

## Current accepted source

328 bounded C/C++ CODE/DATA units, 513 complete function occurrences:
**102,687 authored bytes exact** = 87,350 CODE + 15,337 initialized DATA.
CODE consists of 86,558 instruction and 792 compiler-table bytes. Complete
compared extents total 102,774, including 87 uncredited padding bytes.

| Artifact | Functions | CODE | Initialized DATA |
| --- | ---: | ---: | ---: |
| MAIN | 394 | 66,164 | 3,091 |
| OP | 62 | 11,251 | 8,649 |
| MAINE | 56 | 9,613 | 3,597 |
| ZUN | 1 | 322 | 0 |

Separate reviewed ASM: 7,020 instruction, 210 dispatch-table, 24 semantic
CODE-coordinate and 64 DATA bytes; 7,388 complete bytes include 70 uncredited.
Vendor CODE/DATA: 73,804/3,777; font resource: 8,192. These are separate from
C/C++ credit. Unknown ownership: **123,333 bytes**, including MAIN 43,623.
Generated authority: [progress](PROGRESS.md), [ownership](../resources/ownership.json).

## Latest exact recovery

`main-yumeko-swords-render`: MAIN `[143E0,14422)`,66 bytes/28 instructions,
no NOPs, tables, padding or relocations. Two fresh normal producers match all
bytes and ordered fixups; the live/free predicate control is rejected at byte22.
Import adds66 instruction bytes/one function. Older records remain unchanged.
Receipt `.analysis/unit-replays/main-yumeko-swords-render-a/receipt.json`, SHA-256
`b1bd8679efe138790eec8986c303143b5a1194a3f664f1ce7873f409882ea5e0`.
See [source evidence](../src/main/boss/yumeko/swords_render.md).

Previous3af324e added B4 renderer96 and narrowed routine validation to exact
work. The simplified process remains in effect; no new behavior models/tests
were added in this iteration.

## Current work direction

The major boss update callbacks are already accepted. Continue on genuine
unmatched functions and their leaves, using native bytes and current source
rather than treating old failed experiments as restrictions.

- **Next: Yumeko sword updater283**, now recovered as ordinary280-byte C++.
  Missing local removal proxy2, merged loop-tail jump2 and a one-byte longer
  player-Y calculation explain the gap. A targeted-O- profile285 was rejected;
  baseline280 restored. Do not insert padding or a register arithmetic template.
- Yumeko aimed swords354 and laser/swords428 now match every raw byte, but
  standalone relocation order differs. They remain unaccepted. The actual
  aim ABI is two coordinate words plus one angle word, near Pascal RET6; a
  local word-value view removes the old Subpixel temporary without editing
  shared declarations. Full records and ordinary calculations are retained.
- A genuine allocator121/updater280/patterns435 prefix restores the aimed
  relocation stream, but places the function three bytes early. Its requested
  separate-segment scope fails because first declaration fixes B5_UPDATE_TEXT.
  This is an actual failed producer, not acceptance. Correct updater/context
  recovery is needed. [Details](../src/main/boss/yumeko/laser_swords.md).
- B4 updater273 remains278; eager deltas290 and cleanup label278 were rejected.
  Source restored; corrected outside PARA placement now keeps DS209D for273/278.
- Shinki wing386 still has a relocation-order mismatch; scalar ball updater232
  remains inexact against220. Dialog opcode455 remains short of456.
- Staff updater623/renderer858 still differ from626/861. Generic boss collision
  scalar46/full-point59 differ from43; Shinki particle171 differs from159.

Joint current review: `.analysis/yumeko-later-root-review.json`, SHA-256
`1099a5063c7943fba749a258d3e449b1fdf1c75c916d329b5ef33cdbda94001c`.
Only the renderer66 is accepted;782 raw-equal attack bytes stay unknown.
All unchanged accepted owners and installed execution proofs were reused.

## User-directed focus, 2026-10-28

Prioritize exact C/C++ recovery. Do not routinely add CPU behavior models,
allocation-failure/null-pointer checks, exhaustive inputs, fault injection or
per-function supplementary negatives. Such experiments are optional and useful
only for a concrete source/ABI ambiguity. Historical test narratives are not
an ongoing checklist; earlier detailed handoffs remain in Git history.

Replay only new/affected units and reuse unchanged accepted dependencies/tools.
`python3 scripts/ci.py` now performs lightweight public consistency checks;
`--full` explicitly runs the tooling regression suite. Full CI is not required
after each function or commit. The obsolete zero-compare probe, monolithic
boss-background diagnostic and supplemental-negative tools themselves are also
retired, along with their mock suites; their scripts remain in Git at3af324e.
The normal replay's shared control is sufficient. Documentation/test-only
cleanup needs no compiler replay or generated progress refresh.

Keep short evidence notes, update generated progress/ownership for accepted
changes, and commit/push substantive progress. Preserve the
[exact contract](ORACLES.md), [workflow](RE_WORKFLOW.md), original Borland ABI,
complete bytes and original relocation order. Serialize Wine/Borland/Ghidra.
