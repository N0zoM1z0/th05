# Exact OP piano pressed-key top masks

The original Music Room has a twelve-byte table at decoded OP
`DB01..DB0D`, immediately after the accepted pressed-key renderer and before
the accepted glyph painter. The table is **semantic CODE data**: one byte
for each chromatic pitch from C to B, not twelve CPU instructions.

[Maintained assembly](pressed_top.asm) derives the mask of each note from
three original piano geometries (a sharp/outer key, the middle of a white
key, and the right edge of a white key), left-shifted into bit plane 5. The
patterns match the explicit note names and masks retained in pinned ReC98
`th05/op/piano_a.asm`. There are no copied original-byte arrays or
instruction-transcription templates.

Strict focused receipt:
`.analysis/piano-pressed-top/gpt-web-top-a/receipt.json`.
Two independent TASM32/TLINK producers generate the entire 12-byte CODE
LEDATA at original CS `0D30`, offset `0801`, and match all original bytes,
with zero MZ relocations. A compiled negative changes the note-mask plane
shift from 5 to 4; the original comparison rejects it. The symbol-only
[binder](../../../probes/units/piano_pressed_top_bindings.asm) supplies no
initialized data.

Acceptance is recorded in `config/piano_pressed_top_acceptance.json`. The
ownership map classifies all 12 bytes as
`accepted-reviewed-asm-semantic-code-table`, with **zero instruction bytes**.
The neighboring accepted piano FM wrapper, renderer, label copier and C++
current-note lookup keep their existing source inputs and acceptance.
