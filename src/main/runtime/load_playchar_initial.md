# Initial character-resource loading decision in MAIN

MAIN `[20A70,20A72)` is the original 16-bit `load_playchar_resources` flag
at DS `209D:00A0`. The pinned `th05_main.asm` declares its two bytes as
consecutive `db 0` literals immediately before the pause-action glyphs.
The actual 803-byte accepted stage-session initializer writes the word to
zero, changes it to one at stage 1 or Extra, and tests it when deciding
whether to reload character-specific sprite, bullet and bomb resources.
The original native instructions use `word ptr [00A0]` consistently; this is
one mutable 16-bit state word, not two unrelated boolean flags.

`load_playchar_initial.cpp` declares the canonical `int` state with one
zero initializer. Two genuine Borland/TLINK producers each emit exactly the
original two DATA bytes at that address with empty ordered MZ relocations.
The compiled negative initializes the loading decision to one and fails.
Receipt:
`.analysis/unit-replays/gpt-web-main-playchar-loading-20261112-a/receipt.json`.

This adds two source-authored C++ initialized DATA bytes. The adjacent
pause-action glyph bank, eyecatch pointers and startup resource strings
retain their independently accepted owners.
