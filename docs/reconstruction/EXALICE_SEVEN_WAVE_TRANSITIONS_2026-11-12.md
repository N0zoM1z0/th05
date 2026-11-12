# EX-Alice full Boss: seven identical HP/callback handoff protocols

The original 1,060-byte complete EX-Alice controller repeats one genuine
transition operation **seven times**: four regular-wave and the first three
charged-wave handoffs call `exalice_phase_next(explosion, hp_end)` and then
install the specific following `exalice_pattern` callback. Separate source
macros for regular and charged waves previously duplicated this entire
identical operation. The maintained natural C++ now uses one
`EXALICE_WAVE_ADVANCE(explosion, hp_end, next_attack)` protocol, preserving
all seven independent original HP targets, explosion directions and callback
choices. The terminal charge-wave phase still advances without a new attack
callback, retaining its unique behavior.

The full shared-context owner (the original far shot gate, near phase helper,
compiler switch table and all complete Boss update instructions) was
recompiled in two independent Borland/TLINK positive producers. Both match
the complete **1,060 original bytes**, its ordered native relocations and
MAP/OMF boundaries; the existing compiled HP-threshold mutation was
rejected. Evidence:
`.analysis/unit-replays/gpt-web-exalice-unified-seven-handoffs-20261112-a/receipt.json`.
No duplicate CODE credit, C++ state or artificial compiler operations.
