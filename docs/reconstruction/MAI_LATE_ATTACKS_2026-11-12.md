# Mai solo: three complete late attack functions

The full 615-byte `main-mai-solo-advanced` compiler contribution was
refactored into two genuine repeated source protocols without changing any
native machine bytes. All three patterns complete by resetting the actual
Boss phase clock and movement mode before returning success; the common
`MAI_LATE_ATTACK_COMPLETE()` names that transition. During the four-slot
laser startup, slot 0 fires at the original initial angle, while slots
1–3 each advance by the same signed random delta before firing. These
three operations now share `MAI_LASER_NEXT_SLOT(slot)`, preserving the
slot order, delta arithmetic and distinct callbacks.

The complete affected **615 bytes across 3 functions**, and all ordered
MZ relocations `[567,295,120]`, passed two actual Turbo C++/TLINK
producers. The existing compiled fan-speed mutation (3→4) was rejected.
Receipt:
`.analysis/unit-replays/gpt-web-mai-late-attack-completion-20261112-a/receipt.json`.
No newly accepted authored CODE bytes are claimed; this improves an
already source-exact Boss attack family.
