# TH05 handoff

Goal: at least 98% authored bytes exact from maintained source. The global
authored denominator and percentage remain unreviewed; the goal is not complete.

## Current accepted source

327 bounded C/C++ CODE/DATA units, 512 complete function occurrences:
**102,621 authored bytes exact** = 87,284 CODE + 15,337 initialized DATA.
CODE consists of 86,492 instruction and 792 compiler-table bytes. Complete
compared extents total 102,708, including 87 uncredited padding bytes.

| Artifact | Functions | CODE | Initialized DATA |
| --- | ---: | ---: | ---: |
| MAIN | 393 | 66,098 | 3,091 |
| OP | 62 | 11,251 | 8,649 |
| MAINE | 56 | 9,613 | 3,597 |
| ZUN | 1 | 322 | 0 |

Separate reviewed ASM: 7,020 instruction, 210 dispatch-table, 24 semantic
CODE-coordinate and 64 DATA bytes; 7,388 complete bytes include 70 uncredited.
Vendor CODE/DATA: 73,804/3,777; font resource: 8,192. These are separate from
C/C++ credit. Unknown ownership: **123,399 bytes**, including MAIN 43,689.
Generated authority: [progress](PROGRESS.md), [ownership](../resources/ownership.json).

## Latest exact recovery

`main-b4ball-render`: MAIN `[108DF,1093F)`, 96 bytes/37 instructions, no NOPs,
tables, padding or relocations. Maintained C++ uses the canonical full26-byte
ball records and actual AX/DX/ES graphics boundary. Two normal fresh producers
match every byte; their own damage-offset8-to9 control is rejected. Import
adds96 instruction bytes/one function; older accepted records are unchanged.

Receipt: `.analysis/unit-replays/main-b4ball-render-a/receipt.json`, SHA-256
`fad693879f203da0876abbb69094e62c7817d0b8bd9fde9e8bb38ab3fc0f6df5`.
See [source evidence](../src/main/boss/mai_yuki/b4ball_render.md).

Previous accepted additions at3915fba: Sara159 and Mai/Yuki194 foregrounds.
Ordinary local declaration order resolved both register allocations. Their
canonical inls, accepted receipts and full per-owner notes remain unchanged.

## Current work direction

The major boss update callbacks are already accepted. Continue on genuine
unmatched functions and their leaves, using native bytes and current source
rather than treating old failed experiments as restrictions.

- Shinki wing preparation386 matches raw bytes but its relocation order differs.
  A genuine compiler context is still needed; never sort the relocation stream.
- Shinki ball updater220: ordinary scalar candidate232 remains inexact.
- Dialog opcode456: standalone and real-prefix candidates455 remain inexact.
- Staff updater626 and renderer861: candidates623/858 each omit one redundant
  trail-pointer reload. The new ordinary declaration/initialization-order trial
  still emits4223 for the full4229 family; both canonical inls were restored.
- Generic boss collision43: scalar declaration-order candidate46 and full-point
  candidate59 remain inexact. Shinki particle renderer159: ordinary coordinates
  produce171. These single-producer diagnostics add no credit.

The latter diagnostics and concise root findings remain under
`.analysis/scalar-render-followups-root-review.json`; the maintained standalone
candidates are not registered for default replay. No failed result is accepted.

## User-directed focus, 2026-10-28

Prioritize exact C/C++ recovery. Do not routinely add CPU behavior models,
allocation-failure/null-pointer checks, exhaustive inputs, fault injection or
per-function supplementary negatives. Such experiments are optional and useful
only for a concrete source/ABI ambiguity. Historical test narratives are not
an ongoing checklist; earlier detailed handoffs remain in Git history.

Replay only new/affected units and reuse unchanged accepted dependencies/tools.
`python3 scripts/ci.py` now performs lightweight public consistency checks;
`--full` explicitly runs the tooling regression suite. Full CI is not required
after each function or commit. The obsolete zero-compare probe, one-off boss
background diagnostic and supplemental-control mock suites were removed.

Keep short evidence notes, update generated progress/ownership for accepted
changes, and commit/push substantive progress. Preserve the
[exact contract](ORACLES.md), [workflow](RE_WORKFLOW.md), original Borland ABI,
complete bytes and original relocation order. Serialize Wine/Borland/Ghidra.

This change passes the lightweight consistency check and all362 tooling tests
in one explicit full run for the CI-tool change. The MAIN incremental plan is
empty and diff checks pass. This result does not add a recurring test obligation.
