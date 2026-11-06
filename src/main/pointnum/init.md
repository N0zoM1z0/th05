# Point-popup cursor initialization

The complete native procedure body is MAIN `[E16E,E179)`: two five-byte cursor
stores and the near RET at E178. The NOP at E179 is outside this procedure.
Pinned ReC98 b6ba5b0a's `th04/main/pointnum/inv_upd.asm` independently places
`ENDP` before its separate `EVEN`, before invalidation begins at E17A.
The earlier168-byte family proposal combined the three bodies and both EVEN
bytes; its12-byte public spacing was not an11-byte function plus a missing
instruction.

`init.cpp` compiles the complete canonical body from `init.inl` as its own
11-byte contribution. It resets only the two byte cursors at DS3FA4/3FA5,
with real AE1 near Pascal linkage and no argument cleanup. The retained family
includes the same body. Init/update declarations now agree with the canonical
published Pascal interface; record types, member layouts and storage widths
are unchanged. No accepted unit consumed the old lifecycle header.

Focused replay `.analysis/unit-replays/main-pointnums-init-exact/receipt.json`
passes two deterministic builds, valid OMF/MAP ownership, all11 raw bytes and
the empty original ordered fixup stream. Its compiled white-cursor reset0-to1
mutation is rejected. The source owns no DATA/BSS or padding and defines no
pool, list or callback substitute. Existing accepted objects and tool probes
are reused after dependency identity checks.

The following original NOP remains outside both the actual compiler contribution
and the compared scope, unknown and uncredited. It is not masked, normalized,
replaced or claimed reproduced. No inside-function byte is excluded. This is
complete procedure/whole compiler-contribution acceptance, not acceptance of
the original168-byte family or a larger source module.

Receipt SHA-256:
`b5c7cc3790595636914cd2ac84b054ecfc4e4877c504764ffb4cd9298b1bf550`.
Extent SHA-256:
`cca7bf250e3e69a296fccc57ed800a415c77a7878161ff2ad8dd0bc75df84bbc`.
Native/ENDP/EVEN evidence is retained at
`.analysis/pointnums-init-native-boundary-review.json`.

This adds one complete function and11 C++ instruction bytes. Invalidation,
update and both original alignment bytes remain unaccepted. Literal historical
source, full linkage and whole-executable equality remain unproved.
