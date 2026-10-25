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
