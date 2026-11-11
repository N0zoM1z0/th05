# Exact ZUN `-S` Master buffered file I/O

Nine complete original Master library routines form a contiguous **728-byte**
native source contribution at ZUN resident COM offsets `0698..0970`:

| Function | Runtime COM range | Compared bytes |
| --- | --- | ---: |
| `FILE_READ` | `0698..074C` | 180 (179 instructions + 1 `EVEN`) |
| `FILE_FLUSH` | `074C..07B8` | 108 (107 instructions + 1 `EVEN`) |
| `FILE_CLOSE` | `07B8..07C6` | 14 |
| `FILE_ROPEN` | `07C6..07FC` | 54 |
| `FILE_WRITE` | `07FC..08A2` | 166 (165 instructions + 1 `EVEN`) |
| `FILE_CREATE` | `08A2..08DE` | 60 (59 instructions + 1 `EVEN`) |
| `FILE_SEEK` | `08DE..0912` | 52 (51 instructions + 1 `EVEN`) |
| `FILE_TELL` | `0912..0920` | 14 |
| `FILE_APPEND` | `0920..0970` | 80 |

The maintained [assembler module](file_family_native.asm) composes the
original Master routines preserved by ReC98 as `master_{read,close,ropen,
write,create,seek,append}.inc`, with a tiny-model near-Pascal macro definition
in `master_file_tiny.inc`. The implementation handles buffered reads and
writes, flushing, direct DOS access, creating, seeking, appending, current
position and EOF status. It preserves the original unchecked DOS behavior.
The historic routines are from Akihiko Koizuka's Master library, **vendor
ASM**, not compiler-generated ZUN-authored C++.

The isolated proof uses original DS offsets `1872/1874/1AAA..1AB8` for file
state and two real source-free near provider addresses: `DOS_AXDX` at `0980`
and `DOS_ROPEN` at `09BE`. ORG holes outside the nine functions supply no
code or initialized data. No original target bytes are copied into this
module, and neither buffer state nor foreign provider code is credited.

The focused native receipt
`.analysis/zun-file/gpt-web-all-file-a/receipt.json` contains two independent
TASM32/TLINK producers. Each matches **728/728** bytes, all nine actual MAP
function entries, one complete 728-byte CODE LEDATA, and deterministic OMF.
A semantic negative in the buffered read loop changes the source of its
exhaustion check, altering generated instructions; the strict oracle rejects
it. Five natural `EVEN` padding NOPs, at scope-relative `131, 287, 473, 581,
633`, are checked with zero instruction credit. **723 bytes are actual
instructions.** The older 356-byte scoped receipt has been replaced, not
counted a second time.

Together with the independently accepted [190-byte resident-memory
providers](resdata_native.md), the complete source-owned Master core covers
**918 consecutive original bytes** at `05DA..0970` (912 vendor instructions,
6 checked alignment bytes). This does not accept or modify the separate
269-byte resident `main()` C++ function or the entire `-S` program.

The accepted scoped ledger is
[`config/zun_file_native_acceptance.json`](../../../config/zun_file_native_acceptance.json).
Source-current verification requires no compiler:

```sh
python3 scripts/replay_zun_file_native.py --check
```

To replay only this affected file family:

```sh
python3 scripts/replay_zun_file_native.py --output .analysis/zun-file/NEW
python3 scripts/replay_zun_file_native.py --accept .analysis/zun-file/NEW/receipt.json
```
