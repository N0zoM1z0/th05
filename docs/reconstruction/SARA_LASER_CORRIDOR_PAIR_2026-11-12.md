# Sara: exact paired fixed-laser spawn inside the full 12-function Boss family

The stage-one Sara Boss's final laser corridor creates two fixed beam
slots at opposite angles. Both sides must write their angle *before*
spawning. Only the right-hand beam additionally initializes the laser
color and nonshrinking width, between its angle assignment and the actual
spawn. The new natural source operation
`SARA_CORRIDOR_FIXED_LASER(slot, direction, initialize)` preserves that
ordering: the boolean is a compile-time literal, so Borland emits no
conditional branch or extra helper call. The right and left calls retain
their distinct physical slots and signed aiming offsets.

The complete **1,824-byte, 12-function Sara owner** was rebuilt through
its original Borland C++/TLINK pipeline. Both independent producers match
every native machine byte and all original ordered MZ relocation sites,
including the five-entry switch table. The meaningful compiled red-stack
negative was rejected. Evidence:
`.analysis/unit-replays/gpt-web-sara-fixed-corridor-laser-pair-20261112-c/receipt.json`.

An earlier trial accidentally used `angle` as a macro parameter name,
which collided with `laser_template.coords.angle` under the Borland
preprocessor. Renaming it to `direction` fixed that compilation issue.
A literal initialization block and the final simpler compile-time branch
both produced exact code; the latter is retained. No new CODE credit is
taken for this previously accepted owner.
