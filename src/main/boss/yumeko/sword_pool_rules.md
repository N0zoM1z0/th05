# Yumeko flying sword pool: natural allocator and graphics lifetime contract

The complete 121-byte near-Pascal `swords_add()` and independent 66-byte
near-Pascal `swords_render()` now use the *same* `sword_pool_rules.hpp`
compiler-only source protocol. The original custom-entity pool holds
64 records of the unchanged 26-byte `sword_t`: the initial template is
slot zero, and exactly **63 active sword slots** are traversed from
slot **1**. The allocator reserves only the first free sword, keeping
the original copy of the current template origin, true `F_ALIVE`
flag, player-performance-tuned byte speed, shrinking-circle helper,
near vector-to-velocity calculation and unchanged 25-byte template
angle/speed/twirl ABI. It still sets circle color **9** and chooses
the directional tiny sprite from its actual sprite base **193**.

The renderer traverses the identical active range in original order,
retaining the distinction between `F_FREE` and all non-free states.
The real PC-98 blue-plane selector and raw tiny-32 drawing call are
unchanged. The only source-level geometry names represent the
original Q12.4-to-pixel shift by **four bits** and **16-pixel** X
alignment adjustment; the original scroll conversion still supplies
the Y coordinate. No packed sprites, sword data, extra iteration or
new drawing code are inserted.

These sources are also included inside Yumeko's original nine-function
attack compilation context, so the two separately accepted 354-byte
aimed-sword and 428-byte mixed laser/sword callers were independently
replayed along with both leaf functions. Two native Borland producers
match **121 + 66 + 354 + 428 original CODE bytes** and the literal
ordered original relocations; the compiled source control changes the
actual shrinking-circle color from 9 to 10 and is rejected. Focused
receipt: `.analysis/unit-replays/gpt-web-yumeko-sword-pool-a/receipt.json`.

The neighboring **283-byte** `swords_update()` is now supplied to this
context by a raw-exact C++/inline-ASM hybrid, confirmed inside the full
2,139-byte original-order MAIN03 contribution. The same bytes remain owned
only by the independently accepted reviewed-ASM family; this context replay
makes no duplicate C++ CODE claim.
The four previously accepted exact functions receive no duplicate
CODE credit, and there is no whole-game cold replay.
