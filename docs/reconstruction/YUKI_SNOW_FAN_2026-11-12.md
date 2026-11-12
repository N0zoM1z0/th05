# Yuki late patterns: exact snow fan and phase transitions

The four complete solo-Yuki attacks in `yuki_patterns_later.inl` share two
actual source protocols. The aimed snow fan fires its first B4 ball at the
player angle and then fires four more at explicit wrapped angle changes
`-12`, `-12`, `+36`, `+12`; these remain separate, ordered real calls in
`YUKI_SNOW_FAN_NEXT_BALL(delta)`. The three finite patterns all restart
the Boss phase frame and return to reposition mode through the shared
`YUKI_SOLO_REPOSITION()` statement group.

The snow-cross attack has an important extra state transition: it reverses
`yuki_solo_snow_step` **after** resetting mode and **before** returning
success. That reversal remains in-place; only the two true shared
assignments were factored. The vector-stack direction reversal and its
signed-byte limit also retain their original ordering.

Focused complete-unit replay:
`.analysis/unit-replays/gpt-web-yuki-snow-fan-four-balls-20261112-b/receipt.json`.
Two genuine Borland/TLINK producers matched all **670 original bytes** of
four complete functions, including ordered MZ relocations `[465,272,163]`;
the compiled snow-speed 4→5 mutation was rejected. These bytes already
belong to an accepted natural C++ owner, so this change refines source
clarity without adding duplicate code credit.
