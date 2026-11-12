# Mai/Yuki: paired attack callbacks advance in lockstep

In the complete 1,018-byte `mai_yuki_update()` controller, both the first
and final paired attack banks use the same actual `patterns_seen & 1`
selection for Mai and Yuki. The maintained source now names this relationship
as `MY_SELECT_PATTERN_PAIR(mai_bank, yuki_bank)`, while the middle laser
phase retains its separate Mai tracking-laser and Yuki laser bank handling.
The source still performs its two original function-pointer assignments in
the same order, without a new runtime helper or changed pattern count.

The affected whole `main-mai-yuki-update-context` owner passed two
Turbo C++/TLINK builds, all 1,018 original bytes and nine ordered loader
relocations `[942,931,915,898,874,723,312,171,123]`. The compiled HP-gate
negative was rejected. Focused receipt:
`.analysis/unit-replays/gpt-web-maiyuki-pair-bank-selection-20261112-a/receipt.json`.
This is a natural-source improvement to already accepted Boss CODE, without
recrediting the ten preceding shared attack bodies.
