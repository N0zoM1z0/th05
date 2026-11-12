# MAIN normal/Extra end child-executable filenames

At the original MAIN near-DATA interval `[21E0E,21E1A)` there are two
separate mutable six-byte `maine` strings. These are the actual filename
arguments to two different `GameExecl()` calls in the original program:
`end_game()` writes ES_GOOD/ES_BAD depending on continues, then fades and
launches MAINE, while `end_extra()` selects ES_EXTRA before the same
handoff. The original `th05_main.asm` labels them separately as
`aMaine` and `aMaine_0`; there is no valid reason to pool the storage just
because the printable names are identical.

The natural C source models both as distinct writable `char[6]` objects,
with size assertions. It does not include the actual child binary, DOS
command line, DOS loader or source instructions. The binder preserves
MAIN01/MAIN03, the shared CODE frame and DGROUP at `209D:143E`, with
no preassembled candidate payload or addresses. The neighboring unknown
state and UI glyph selectors remain outside this contribution.

A focused two-producer native Borland C replay proves exact 12-byte
initialized DATA, complete original MAP and OMF SEGDEF/LEDATA boundaries,
raw-byte equality and the original empty ordered MZ relocation stream.
Changing only the Extra-path name from `maine` to `mainf` compiles to a
nonmatching 12-byte contribution and is rejected. Receipt:
`.analysis/unit-replays/gpt-web-main-end-binary-names-a/receipt.json`.
No whole MAIN cold replay was executed.
