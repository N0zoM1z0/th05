# Original MAIN automatic item-drop cycle: exact C++ initialized DATA

The persistent unsigned-byte `item_drop_cycle` lives at actual MAIN
DS:`1E02`, original load-module byte `[227D2,227D3)`. The accepted `items_add`
function (from the real item family) increments that byte for
`IT_ENEMY_DROP_NEXT`, checks its low parity bit and derives its 64-entry
automatic drop-table index from the resulting count. The accepted
`items_init()` resets the same byte from the native random ring at stage
start. These independent real consumer bindings identify its variable type
and role, not merely the occurrence of an all-zero byte.

`drop_cycle_data.cpp` supplies one ordinary mutable, C++-linkage
`unsigned char` initializer with a compile-time type assertion. It produces
exactly one byte in a complete Borland `_DATA` contribution without any
foreign or adjacent initialized bytes. Both independent original-compiler
/TLINK producers match the original `00h` byte, actual MAP address and empty
ordered MZ relocations. The compiled negative changes the initial cycle to 1
and fails the raw oracle. Focused receipt:
`.analysis/unit-replays/gpt-web-main-item-drop-cycle-a/receipt.json`.

The next original byte `[227D3,227D4)` is *not* included: no valid
consumer proves that it belongs to this variable or to the separately
accepted item reward tables at `[227D4,22848)`. This credits **one exact
semantic C++ DATA byte**, zero new instruction bytes, and does not claim
the original historical translation-unit boundary.
