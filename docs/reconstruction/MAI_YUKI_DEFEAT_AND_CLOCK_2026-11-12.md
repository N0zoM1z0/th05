# Mai/Yuki full Boss controller: phase clocks and survivor choice

The complete 1,018-byte paired Boss controller reuses its genuine
**phase-increment-before-frame-reset** operation in the shared entrance,
ready and post-big-explosion phase exits. The original small-explosion
transition is deliberately different: it updates `bullet_zap.active`
between the phase increment and frame-clock reset, so it is *not* rewritten
through this common protocol.

The four real checks for `boss2.phase_state.patterns_seen == MY_DEFEATED_MAI`
now use `MY_MAI_WAS_DEFEATED()`. This is the same stored defeated-character
code for the small and large explosion target selection, sprite advance,
and surviving character's dialog/callback installation. It remains a real
read at each original site; it is neither cached nor a new state field.

The full `main-mai-yuki-update-context` unit passed both actual Borland/TLINK
producers, all **1,018 original machine bytes**, all nine original ordered
MZ relocations and the compiled HP-gate mutation. Focused receipt:
`.analysis/unit-replays/gpt-web-maiyuki-death-choice-phase-clock-20261112-a/receipt.json`.
No duplicate authored CODE credit, new helper machine instructions or
full cold replay.
