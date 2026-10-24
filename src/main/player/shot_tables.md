# Character shot-function table

This natural initialized DATA owner defines the real `SHOT_FUNCS[4][10]`
object. It occupies DS:`1D70..1DC0`, or MZ program-image offsets
`[0x22740,0x22790)`, in locally attested MAIN, SHA-256
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
Its DATA frame is `209D`; every callback uses near offsets in frame `0AE1`.
The complete extent is80 initialized bytes, with zero CODE functions,
padding, BSS or original MZ relocations. No neighboring data is included.

Rows are ordered Reimu, Marisa, Mima and Yuuka. Each row selects shot levels0
through9; common level0/1 providers are repeated in every row, followed by
the eight corresponding character providers. There are40 entries and34
unique callbacks. Every original target word was independently resolved
against the actual public entry addresses in the retained accepted common
and four-character provider MAPs. The actual complete provider payload
hashes were also rechecked against the accepted ledger. These checks route
the initializer to genuine functions; provider acceptance does not establish
the new DATA producer's exactness.

The definition directly reuses `SessionShotFunction` and the complete4-by10
array declaration from the canonical `gameplay_session_init.hpp`. The type
is a2-byte near Pascal pointer to `void(void)`, with a20-byte row. Root
corrected that canonical typedef from cdecl to the actual Pascal interface
and owns the affected468-byte initializer replay. This DATA owner adds no
cast, incompatible duplicate typedef, partial view or new helper body.
The two common callbacks have C++ linkage; the32 character callbacks have
C linkage, exactly as their maintained source definitions. Their Pascal
calling convention is the same.

The initializer uses semantic function names only. It contains no target
words, byte arrays, relocation patches or copied callback implementation.
The table contributes no CODE function count and does not re-credit the
already accepted providers. Source has no assets or external downloads.
Pinned ReC98 `b6ba5b0a`'s `th05_main.asm` supplies the named row/level ordering;
actual target data, maintained callback definitions and retained provider
MAPs were independently checked. The reviewed accepted DATA extents have
no intersection with these80 bytes; the private proof pins the exact ledger
snapshot used for that interval check.

Private integration inputs are `.analysis/shot-tables-unit-proposal.json`,
`.analysis/shot-tables-bindings.asm`, and
`.analysis/shot-tables-boundary-review.json`. The binder supplies only real
foreign callback symbols and outside-owner context. The compiler owns the
entire array; the binder supplies no pointer values or DATA implementation,
and creates no artificial stack. The negative exchanges Reimu level2 and
level3 entries, preserving valid pointer types while changing the actual
power-level behavior. Accepted focused replay `main-shot-function-table-data-a` proves two fresh
deterministic producers, all80 raw bytes, original empty ordered MZ
relocations and valid OMF. The compiled Reimu level2/3 order mutation is
rejected. Its receipt is
`.analysis/unit-replays/main-shot-function-table-data-a/receipt.json`.
The canonical Pascal-type consumer replay was handled separately by root;
accepted source, header and binder remain frozen.
