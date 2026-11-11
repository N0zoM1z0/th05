# Exact Master resident-memory providers inside ZUN `-S`

The `-S` executable's two contiguous original Master library helpers now
have complete, source-built **190-byte** exact proofs:

| Complete original near-Pascal function | Runtime COM range | Raw bytes |
| --- | --- | ---: |
| `RESDATA_EXIST` | `05DA..0622` | 72 |
| `RESDATA_CREATE` | `0622..0697` | 117 |
| Compiler/library `EVEN` after `RESDATA_CREATE` | `0697..0698` | 1 |

`RESDATA_EXIST` walks the DOS MCB chain from INT21/AH52, tests the owner and
paragraph count, and compares the user-supplied resident signature byte by
byte. `RESDATA_CREATE` calls it, saves the DOS allocation strategy, attempts
low-memory allocation before retrying high-memory, marks the new block's MCB
owner, copies the source identifier and restores the original DOS strategy.
Both routines preserve BP, SI and DI and return through real `RET 6` near
Pascal cleanups. The source is the canonical 8086 Master resident-data
implementation from pinned ReC98 `libs/master.lib/resdata.asm` by Akihiko
Koizuka, faithfully expressed with named MCB offsets and DOS services in
[maintained assembly](resdata_native.asm). This is **vendor code**, not
additional game-authored C++.

## Focused proof

The source contribution occupies exactly the original `05DA..0698` COM
runtime range inside ZUN's separate `-S` member (`0AE4..2488` in the outer
container). The proof-only tiny COM uses an empty `0100..05DA` ORG reservation
and fills no neighboring resident function or data. The two native
TASM32/TLINK producer runs match **190/190 original bytes**, one ordinary
190-byte CODE LEDATA, the actual three public label positions, and an empty
MZ relocation stream. The compiled negative changes the MCB paragraph-count
offset from 3 to 4; its instructions differ while the original trailing
alignment NOP stays identical.

Focused receipt:
`.analysis/zun-resdata/gpt-web-resdata-b/receipt.json`.
Accepted ledger:
[`config/zun_resdata_acceptance.json`](../../../config/zun_resdata_acceptance.json).

The source-current check needs no native compiler or full replay:

```sh
python3 scripts/replay_zun_resdata.py --check
```

A newly requested local producer replays *only these two functions*:

```sh
python3 scripts/replay_zun_resdata.py --output .analysis/zun-resdata/NEW
python3 scripts/replay_zun_resdata.py --accept .analysis/zun-resdata/NEW/receipt.json
```

The 189 instruction bytes are separate, reviewed Master library code and
receive **zero global game-authored credit**. The standalone original 269-byte
ZUN `main()` entry and the rest of `-S` remain unaccepted; neither is patched,
filled from the original COM, nor pulled into this unit's acceptance.
