# Yumeko's two rotating-spread attack families

The counterrotating blue spread and mirrored green spread now share the
original charge sprite, projectile spawn type and group setup in
`YUMEKO_SPREAD_CHARGE_START(group)`, plus the real frame-clock/reposition
completion protocol in `YUMEKO_SPREAD_REPOSITION()`. The blue pattern's
`BSM_EXACT_LINEAR` special-motion write remains before projectile speed,
while the mirrored pattern sets speed immediately after the shared prefix.
Those originally distinct execution orders must not be merged.

The source is shared with both real sword attack compiler contexts, so all
three complete affected units were replayed: the **518-byte** spreads,
**354-byte** aimed-sword context and **428-byte** laser-sword context.
Two original Borland/TLINK builds per unit match all native bytes and
ordered loader relocations. The existing compiled negative was rejected.
Evidence: `.analysis/unit-replays/gpt-web-yumeko-spreads-charge-reposition-20261112-b/receipt.json`.
Already accepted authored CODE has not been counted again.
