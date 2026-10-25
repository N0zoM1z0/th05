# Generic bomb lifecycle candidate

The complete original consecutive owner is `[FA50,FB44)`,244 bytes in MAIN's
unrelocated MZ program image, containing four complete functions:

| Function | Original range | Compared bytes | Actual ABI |
| --- | --- | ---: | --- |
| bomb reset | FA50..FA60 | 16 | C++ near cdecl, no args, RET |
| player activation | FA60..FAF7 | 151 | C near Pascal, no args, RET |
| player tile mask | FAF7..FB0A | 19 | C near Pascal, word cel, RET2 |
| Dream decay | FB0A..FB44 | 58 | C++ near cdecl, no args, RET |

Five original `90 / PUSH CS / CALL near` sequences contain checked uncredited
NOPs at owner offsets77/104/124/160/237. Full comparison keeps all244 bytes;
potential authored instruction credit is239 after acceptance. There are no
tables or source-owned DATA/BSS, and the original ordered MZ list is `[143]`.

The natural donor is maintained TH04 `src/main/player/bomb.cpp`. Actual TH05
behavior uses the standalone bomb count, four-character invincibility and
bullet-clear selectors, a performance decrement and the real resident bombs
counter. The deathbomb guard preserves the32-frame threshold and resets the
actual respawn-motion byte only in its original allowed window. The mask
delegator leaves color unchanged in GAME5, as independently corroborated by
pinned ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`
`th04/main/player/bb_playchar_put.asm`. Dream decay retains ordinary integer
remainder by2/4 and the actual Boss HP-fill condition; no parity/flag variant
or register arithmetic replaces it.

Both complete canonical Boss24 and resident128 records are imported unchanged.
The Boss phase is the real byte at offset15 and bombs-used the resident byte
at28. Background callbacks are genuine two-byte near Pascal function pointers.
`bb_tiles8_t` is the canonical unsigned bitmap byte, with real two-byte `__seg`
allocation addresses. These are not DOS handles or far pointers, and no opaque
record/asset byte array is substituted.

The selector retains its real four-word far Pascal signature and word AX
result; actual RETF8 is at CFC3. Performance decrement retains its char argument
in a two-byte Pascal stack slot and void far return, RETF2 at CFA9. HUD bombs
and Dream remain genuine far APIs in the same AE1 code frame. The sound API
is actually in different CS14AB and receives no samecodeseg annotation.
The mask helper at F968..F9EC has the true near Pascal word argument and RET2.
The reset assigns the actual nonzero `nullfunc_near` callback at C73E.

Only real foreign far callees receive samecodeseg declarations. The maintained
bomb donor explicitly uses that context for HUD bombs, accepted `miss.hpp`
uses it for Dream/performance, and the selector's actual same CS and far-return
contract are independently verified. All far prototypes remain far. None of
the four locally defined functions has such an annotation; no local definition
is migrated into a foreign segment. No call/NOP bytes, fake near cast, helper
body, flag option or placement prefix is supplied.

All original native branches, complete returns, five padding sequences,
foreign stack contracts and physical operand bindings were independently
reviewed against locally attested MAIN, SHA-256
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
The packet is uncompiled and unaccepted. Private evidence, outside-only binder,
source hashes and proposal are in `.analysis/bomb-runtime/`.

The whole244-byte contribution and all four actual MAP boundaries must be
verified, followed by two fresh raw/original-ordered comparisons and the
compiled Reimu-invincibility192-to193 control. That control belongs to this
whole owner; no independent helper control is claimed. Initial options retain
only the donor's normal CODE/group selectors. No accepted source/header was
edited, and no compiler run occurred during this preparation.

## Accepted result

`main-bomb-runtime-a` passes both fresh deterministic whole244-byte raw
comparisons, the original ordered `[143]` fixup and OMF checks. Its compiled
Reimu-duration192-to193 control was rejected for this whole four-function
owner. All239 instruction bytes are imported as authored; the five real
call-padding NOPs are compared and excluded from authored credit. There is no
independent Dream-decay negative claim. CPP, header and maintained binder are
now frozen accepted dependencies.

Current canonical bodies and source-sensitive refresh evidence are documented
in [bomb_family.md](bomb_family.md). Earlier individual controls remain
historical; the eight-owner refresh uses one shared Reimu-star control.
