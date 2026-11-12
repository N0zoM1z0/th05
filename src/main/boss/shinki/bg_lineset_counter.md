# Shinki type-A background lineset zoom-cycle counter

The decoded original MAIN `[22358,22359)` is a complete one-byte mutable
near-C DATA object, `shinki_bg_linesets_zoomed_out`. The original
`th05_main.asm` exports the exact public immediately before a *separate*
alignment byte and the independently accepted two-byte particle-count
sentinel `[2235A,2235C)`. The actual Shinki background's line-update code
increments this byte each time either rotating lineset reaches the
224-pixel zoom limit, and uses `(counter % 4) < 2` to select the paired
spin directions. A single writable unsigned byte initialized to zero
expresses that source-level role without inventing a larger zero-filled
background struct or borrowing any neighboring bytes.

The source-free native binder only supplies the authentic MAIN code frames
and the external DGROUP prefix at `209D:1988`. The initializer is one real
Borland C byte, with no authored padding, switch table or relocation.
Two independent pinned compiler producers match all of the original byte,
OMF/MAP DATA extent and empty ordered MZ fixup list. A compiled change of
the seed from zero to one is rejected:
`.analysis/unit-replays/gpt-web-shinki-lineset-counter-a/receipt.json`.

The original `[22359,2235A)` alignment zero is **not** accepted; the
previously accepted particle-count word is also not recredited.
The independent consumer source will be selectively revalidated after
its C-linkage declaration is joined to this physical owner.

## Consumer ABI completion (2026-11-12)

The original zero-initialized byte is now exposed through
`background_rules.h` to the entire 17-function Shinki/EX-Alice
background owner using its true C symbol and unsigned-byte width.
Its standalone source includes that exact declaration, with original
code, source-initialized byte, and compiled negative all verified
under `gpt-web-bg-abi-counter-b`. Full consumer evidence is in
`background_rules.md`.
