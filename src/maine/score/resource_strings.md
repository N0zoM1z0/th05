# MAINE score files, fonts and slow-mode warning strings

The decoded MAINE interval `[11634,116F1)` is now one complete
**189-byte natural C initialized-DATA contribution**. It owns four
separate writable `GENSOU.SCR` filename objects (44 bytes) used by the
score lifecycle's distinct file operations, four small image/font names
`hi01.pi`, `scnum.bft`, `sctm0.bft` and `sctm1.bft` (38 bytes), two
independent copies of the Japanese slow-mode score warning (51 bytes
each), and the original `name` field caption (5 bytes). The score
warning states that slow-mode play does not save the score. All strings
are initialized by their **meaningful source text**, staged as actual
CP932 for Turbo C; no binary font/image resource or target byte array
is embedded.

The four canonical `SCOREDAT_FN`, `SCOREDAT_FN_0`, `SCOREDAT_FN_1` and
`SCOREDAT_FN_2` C publics retain the distinct names and mutable byte
array ABI required by the separately accepted score file functions.
The repeated Japanese messages likewise remain distinct objects; no
`const` string pooling is used to collapse the original allocation.
Each exact field size and the full 189-byte DATA sum are compiler-checked.

The original disassembly declarations in `th05_maine.asm` and the included
`th05/formats/scoredat_load_for[data].asm` corroborate the four filenames,
the score/font resources and both warnings. The outside-only binder
places this whole C contribution at real DGROUP `1011:1524` and supplies
no instructions, relocations, initialized text or adjacent state. The
three bytes before `[11631,11634)` and the one byte afterward
`[116F1,116F2)` remain separate unknowns; the next already accepted
verdict state starts at `116F2`.

The focused native receipt
`.analysis/unit-replays/gpt-web-maine-score-resource-strings-a/receipt.json`
passes two independent Borland C producers, the entire 189-byte OMF
DATA SEGDEF/LEDATA and MAP contribution, raw equality and original
empty ordered MZ fixups. The compiled filename mutation
`GENSOU.SCR` to `GENSOU.SCX` is rejected without changing the array
size. No unrelated score/vendored CODE or the whole accepted ledger was
replayed.
