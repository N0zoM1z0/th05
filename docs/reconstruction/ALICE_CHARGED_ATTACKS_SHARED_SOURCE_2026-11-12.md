# Alice: one natural charge-attack implementation for two exact contexts

The three charged Alice patterns (aimed laser fan, paired rotating stacks,
and rotating ring) were previously duplicated in the standalone
`charge_patterns.cpp` and full Boss `update_context.cpp`. Their implementations
were identical except for two names for the same zero-valued reposition mode.
Both compiler contexts now include `charge_patterns_body.inl` as their actual
function source. This removes the duplicate function bodies and makes the
same six-color gather/sprite setup, charge-start sound and timed reposition
transition explicit across the three distinct attacks. Each pattern still
has its own angle initialization, shot count, aiming calls and sound events;
no new runtime helper or storage is emitted.

Both affected **complete accepted owners** were recompiled with the original
Borland 16-bit toolchain, not just the surrounding update controller:

- `main-alice-charge-patterns`: **499/499** original bytes, with all six
  original ordered relocations exact in both positive builds
- `main-alice-update-context`: **939/939** original bytes, with its original
  relocation and switch dispatch exact in both positive builds

The existing compiled negative for the laser-fan width now mutates the real
shared `.inl` source instead of the removed duplicate `.cpp` text. Both
positive producers and the negative pass; the full scoped receipt is
`.analysis/unit-replays/gpt-web-alice-shared-499-and-939-native-b/receipt.json`.
No original CODE byte is counted twice, and only these two affected units
were replayed.
