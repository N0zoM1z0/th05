# MAIN actual Stage Clear/All Clear previous Miss/Bomb counters

The physically correct decoded MAIN interval `[22432,22434)` is one
complete two-byte near-C initialized-DATA contribution. Its original
DGROUP offsets are **`209D:1A62` and `209D:1A63`**, matching the true
large native `stage_bonus_full_bindings.asm` and the real code addresses
used by the complete 561-byte `stage_clear_bonus()` and 579-byte
`stage_allclear_bonus()` source owners. These are two independently
addressable mutable `unsigned char` C publics:
`bonus_previous_miss_count` and `bonus_previous_bomb_count`, both
initialized to zero. After reading the live resident Miss/Bomb totals,
each original full function compares those totals against its two
previous-stage snapshots, then writes back the current totals before
rendering the No Miss/No Bomb lines. The original `no_bomb` bonus
requires `no_miss` as well as an unchanged Bomb count.

## Correcting an earlier ambiguous zero-byte ownership claim

An earlier accepted initializer used the right two C symbols and the
correct **two zero bytes**, but placed its bounded isolated DATA at
`[222B4,222B6)` (DGROUP `18E4`). A raw-only test naturally passed:
zero-initialized C globals cannot distinguish two wrong original
addresses with identical bytes. Checking the actual independently
accepted source consumer's native CODE binder shows that
**`209D:18E4` is `_explosion_big_frame`**, a signed 16-bit large Boss
explosion frame. The original Stage Clear consumers instead reference
**`209D:1A62/1A63`**, decoded `[22432,22434)`.

The original accepted stage-bonus initializer entry has therefore been
**moved rather than duplicated**: its unit ID remains
`main-stage-bonus-previous-resource-counters-data`, the manifest's
`target_start` is now `0x22432`, and its symbol-only binder reserves
exactly the true `1A62h` outside DATA prefix. The old interval is
separately owned by the genuine `_explosion_big_frame` C initializer,
with its own actual consumer and negative control. See
`src/main/boss/explosion_frame.md`.

## Source-current native evidence

The moved previous-resource source was recompiled by two independent
pinned Borland C/TLINK producers against the **correct** live MAIN
coordinate. All two real initialized bytes, the OMF/LEDATA/MAP extent,
empty original ordered MZ fixups, and the compiled Bomb seed 0→1
negative pass:
`.analysis/unit-replays/gpt-web-rehome-bonus-original-address-a/receipt.json`.
The earlier receipts with target `0x222B4` are retained as historical
byte matches but are **not** current acceptance proof of these two
counters. The full Stage Clear and All Clear CODE were already separately
native-source accepted; their correct DS addresses were never changed.
No target bytes were falsified, no original resource asset or neighboring
state was claimed, and no whole MAIN cold replay was performed.
