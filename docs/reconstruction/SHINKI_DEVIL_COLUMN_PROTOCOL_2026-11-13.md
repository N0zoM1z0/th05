# Shinki Devil: four physical columns and mirrored volley motion

The Devil's four fixed-laser slots are emitted from right to left. After
the first slot A launches, each subsequent B/C/D slot shifts the true
laser-origin X by one wing-column width before spawning. The three
repeated shifts now use `DEVIL_NEXT_FIXED_LASER(slot)`. Both the primary
red-bullet and secondary decorative-bullet waves likewise advance to
the next column **before** selecting its own mirrored angle and emitting
the bullet. Their six shared operations now use
`DEVIL_NEXT_FIRE_COL(direction)`. The first decorative shot deliberately
retains its different order (angle before X position), and the original
four-slot laser growth, ballistics and tempo remain unchanged.

Because `devil.inl` participates in the real large Shinki compiler
context, the focused dependency plan replayed **12 complete affected
units**, not just the 802-byte Devil callback. All source units passed both
Borland/TLINK producers, full original byte comparison, ordered MZ
relocations and the compiled semantic negative. Among the 12 are the
**802-byte `pattern_devil()` and 959-byte `shinki_update()`**. Evidence:
`.analysis/unit-replays/gpt-web-shinki-devil-real-columns-20261113-a/receipt.json`.
This improves already accepted large Boss C++ source and does not add
duplicate CODE credit.
