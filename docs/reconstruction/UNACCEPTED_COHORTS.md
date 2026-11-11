# Current open reconstruction candidates — 2026-11-11

The acceptance manifests and ledgers, not historical first-producer notes,
determine which complete original extents are owned. See
[the handoff](../RE_HANDOFF.md), [progress](../PROGRESS.md) and the
[gapless ownership map](../../resources/ownership.json). The global authored
denominator is still unmeasured; unreviewed intervals are not accepted by
proximity to an accepted neighbor.

## Resolved compiler-context problem

MAIN `dialog_op()` at `13B82..13D4A` is now accepted as a **complete
456-byte C++ function**, with its original one-byte switch-table alignment,
30-byte table and all ten ordered relocations. The real preceding 73-byte
STD callbacks, followed by already accepted graphics and box functions,
restore the exact compiler context. The previous 455-byte diagnostics are
superseded. See [interpreter acceptance](../../src/main/dialog/opcode.md).

## Different-language alternatives, not missing executable ownership

These complete machine-code functions **already have accepted reviewed ASM
owners**. Only their ordinary C++ alternatives remain inexact and should not
be described as uncovered code:

| Alternative C++ source | Status of that alternative | Accepted owner |
| --- | --- | --- |
| BB resource loader | Ordinary C++ 56 versus original 55 bytes | Full 55-byte reviewed ASM, [review](../../src/main/formats/bb_load.md) |
| Near vector helper | Ordinary C++ 92/106 versus original 55, with following EVEN byte excluded | Full 55-byte reviewed ASM, [review](../../src/shared/math/vector2_near.md) |
| Scroll coordinate helper | Ordinary C++ 47/51 versus original 40 bytes | Full 40-byte reviewed ASM, [review](../../src/main/scroll/coordinates.md) |

## Large unknown regions and superseded investigations

The original MAIN `C9BA..CAD2` player region is now complete reviewed native
ASM with a symbolic 20-case dispatch table; its original natural C++
alternatives remain unaccepted. The 184-byte STD loader, 168-byte score insertion and 159-byte far vector
pair are now accepted natural C++ using real TCC `-S`/TASM32 producers, not
hand-credited ASM. The 68-byte MAP loader is also previously accepted C++; remaining
questions include unreviewed code/data origin boundaries. Review the original function boundaries,
semantic source and foreign symbols before adding an acceptance candidate;
use the generated ownership map to discover other live gaps.

**Resolved, not open:** MAIN EMS Boss face loader **154** and its ordered
fixups; shot collision functions **399 + 210**; stage initializer **803**;
scroll ring/driver **204 + 115**; Mai/Yuki tracking laser **186**; Shinki
ball/wing **220 + 386**; Yumeko swords **283** as original-register ASM;
generic Boss defeat/collision **414 + 43**; OP score decoder **169**; MAINE
registration menu **1,034** and Staff controller/update/render
**991/626/861**. These each have an independently accepted owner. Earlier
statements of inexactness in per-owner notebooks describe failed variants,
not the current result. Unrelated unsettled source or whole-translation-unit
claims do not invalidate a separately accepted full function.

For recovery, keep meaningful semantic and ABI findings in the owner notes.
Do not revive old trial binaries merely to repeat a failed compiler option,
normalize fixup order, treat a partial fragment as a complete function, or
add copied machine-code/padding to fabricate equality.
