# MAIN eyecatch CDG filename

The original MAIN near-DATA interval `[20A7A,20A82)` is now a whole,
8-byte natural C filename initializer, `EYECATCH_FN[] = "eye.cdg"`.
The source-level name is independently attested by
`_reference/ReC98/th05_main.asm`'s `_EYECATCH_FN` declaration and the
`th05/shiftjis/fns.hpp` interface. It is a mutable resource filename, not
the CDG artwork itself or an address assembled out of target bytes.

The symbol-only native binder preserves the MAIN01/main03 code frames
and DGROUP `209D:00AA`. It contributes no initialized candidate bytes,
foreign source code or adjacent pointers. The preceding initialized
pointer context remains unowned; the following source-defined filename
bank has its own previously accepted DATA contribution.

Two independent Borland C compiles in the focused
`.analysis/unit-replays/gpt-web-main-eyecatch-fn-a/receipt.json` match the
full 8-byte original raw/OMF/MAP DATA extent and the empty ordered MZ
fixup stream. Replacing the final filename letter by `f` is a compiled,
rejected DATA mutation. Nothing else was replayed.
