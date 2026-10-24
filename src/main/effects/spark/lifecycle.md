# Spark initialization and invalidation

The complete adjacent MAIN functions at load offsets `[E10E,E134)` and
`[E134,E152)` pass the strict oracle: 68 instruction bytes, two complete
functions, no padding or compiler tables, and original ordered fixup `[49]`.
Two fresh positive producers agree in raw bytes and relocation order. The
compiled negative changes the invalidation width from 8 to 9 and is rejected.
The retained receipt is `.analysis/unit-replays/main-spark-lifecycle-a/receipt.json`.

The semantic donors are the maintained TH04 reconstruction's natural C++
`spark/init.cpp` and `spark/invalidate.cpp`; acceptance is independently proved
against TH05. The full 16-byte spark retains flag, age, twelve-byte motion, and
word angle. The original traversal bug visits 96 records despite the active
pool's 64 records. Initialization writes only the low byte of the angle and
ring-offset word, preserving the actual original behavior.

IRand keeps its real far Pascal integer return before conversion to a byte.
Invalidation uses the reviewed legacy Borland point-by-value view of the real
four-byte point/RET4 tile entry, shared with enemy invalidation. Register pointer
and counter locals express the traversal; there are no physical register hints,
compiler-body assembly, or target-byte arrays. The symbol-only binder supplies
foreign addresses and receives no authored credit. Whole-program placement and
packing remain open.
