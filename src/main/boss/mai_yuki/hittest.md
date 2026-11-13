# Mai/Yuki shot-hit state wrappers

This bounded reconstruction supplies two previously external, ordinary natural C++ bodies.
The complete original MAIN cohort is `177F0..1785F`, 111 bytes. It is distinct
from the parked shared update callback, tracking-laser attack and collision
kernels. The `main-mai-yuki-hittest-a` replay passes two independent fresh producers,
full OMF/MAP and raw-byte comparisons, original ordered fixups and the shared
compiled collision-category mutation. The ledger credits111 authored
instruction bytes and two complete functions.

| Function | Complete original interval | ABI |
| --- | --- | --- |
| `yuki_hittest_shots_damage()` | `177F0..1782C`, 60 bytes | Near Pascal, three signed words, `RET 6`, full int AX |
| `mai_yuki_hittest_shots()` | `1782C..1785F`, 51 bytes | Near cdecl, no arguments, unsigned-byte AL result |

Both functions use the original `1527` code frame. Native decoding covers every
byte and every return, with no NOPs, padding or CODE tables. Original ordered
MZ fixups are **[46, 32]**, both in the first function. The candidate reference
is `ReC98/th05_main.asm` lines 12361–12424; its semantics and interfaces were
checked against the pinned original, without transferring source acceptance.

The first helper selects the real Boss shot-collision category, writes signed
hitbox radii, copies Yuki's complete current point and invokes the existing
shot collision procedure. It preserves the full signed damage return across
the conditional sound call, then clears the category selection and returns
the damage. The actual collision API returns damage in AX; no CF predicate or
invented bool wrapper is used.

The selector first invokes the real Mai Boss hit test. Its byte result1 means
Mai was defeated. Otherwise it invokes Yuki's helper with 24-pixel radii and
sound4, stores the actual low-byte damage in the complete `boss2` object,
zero-extends that stored byte for HP subtraction, and compares signed HP to
the real phase-end threshold. It returns byte2 for Yuki's defeat or byte0 for
neither. Named state constants preserve the canonical `unsigned char` return
interface already declared by the shared callback owner.

The header imports the complete canonical 24-byte `boss_stuff_t`, 12-byte
motion and four-byte Point types through unchanged `mai_yuki.hpp` and
`movement.hpp`. Yuki remains `boss2` at DS `209D:5AD2`, with HP at +12,
damage byte at +18 and phase-end HP at +22. It references the existing
`shots_hittest_against_boss` byte at `1DC0`, center at `C4C0` and radius at
`C4C4`; it defines no storage, shortened structures or same-address aliases.

Far providers are `shots_hittest()` at `0AE1:8873` (load `13683`, full int AX)
and C-linkage Pascal `SND_SE_PLAY` at `14AB:0232` (load `14CE2`). The near
Boss predicate is the accepted provider at `1527:A860`, load **1FAD0**. The
original call's signed relative operand wraps within the real 16-bit CS frame;
naively disassembling it with a global linear address can print the incorrect
load `FAD0`. Native review resolves the actual 16-bit offset before adding the
frame base. All first declarations retain their true groups.

The independent binder supplies only real provider labels, canonical globals
and holes outside the whole 111-byte source contribution. The own compiled
negative changes the first helper's real collision-category selection from
true to false; the second function shares that compiled oracle control, with
no independent selector mutation claimed. Original boundaries, branches,
correct physical call targets, hashes and the unit/control proposal are private
under `.analysis/main-mai-yuki-hittest/`. The passing receipt is
`.analysis/unit-replays/main-mai-yuki-hittest-a/receipt.json`. Independent
whole-program linkage and historical original source identity remain unproved.

## Shared hit-result ABI with the actual two-Boss controller (2026-11-12)

The separately accepted 111-byte Mai/Yuki hit selector and the
1,018-byte shared Boss controller now import *one physical source of
truth* for result values: `hit_result.hpp` defines `MY_HIT_NONE = 0`,
`MY_HIT_MAI_DEFEATED = 1` and `MY_HIT_YUKI_DEFEATED = 2`.
The original leaf tests Mai's Boss first; only when Mai does not lose
does it apply the actual Yuki hitbox of **24×24 pixels**, invoke real
shot collision, emit sound **4** on hit, subtract the full stored damage
byte and compare Yuki's signed HP gate. Its existing far/near helper
ABIs, `shots_hittest_against_boss` flag lifecycle and AL result are
unchanged. The shared setup's separate 24×24 hitbox still deliberately
uses sound 10, preserving that phase's different semantics.

`hit_result.hpp` only names compiler constants, not independent state.
The actual one-byte `boss2.phase_state` union is reused by the survivor
transition as the *zero-based defeated index*: Mai loss is stored as 0, Yuki
loss as 1. During combat its byte is viewed as `patterns_seen`; after the
result-minus-one store, the paired controller and foreground view the same
byte through `MaiYukiDefeatCharacterState::defeated_character`. The original
wrapper's real unsigned-byte return and the Boss' subtraction of one use the
same constants. This prevents divergence between independently compiled
source owners without changing a single original byte.

The focused two-unit native receipt at
`.analysis/unit-replays/gpt-web-mai-yuki-shared-hit-protocol-a/receipt.json`
passes two independent Borland producers for all **111 hit-leaf bytes**
and the entire **1,018-byte** Boss controller, their original ordered
MZ fixups and actual OMF/MAP bounds. Both compiled semantic negative
controls are rejected. No new code-byte credit is claimed for existing
accepted source.


## 2026-11-13: typed survivor-result view

`hit_result.hpp` now provides the one-byte `MaiYukiDefeatCharacterState`
overlay and `MY_DEFEATED_CHARACTER()` access macro. It names the later
survivor-dialogue lifetime of `boss2.phase_state` without adding a member to
the canonical 24-byte Boss object. The hit selector still returns 0/1/2 in
AL, and the complete shared Boss controller still stores result minus one;
only the source view changes after that write.

The complete 111-byte hit provider, 1,018-byte paired controller, 194-byte
foreground and 75-byte sprite helper all replay exact twice with original
ordered fixups and the existing compiled negative rejected. See the shared
receipt in `.analysis/unit-replays/gpt-web-mai-yuki-defeated-character-overlay-20261113/`.
