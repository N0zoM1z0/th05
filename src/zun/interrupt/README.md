# ZUN.COM `-I` resident STOP/COPY interrupt guard

The original TH05 launcher embeds a complete independent `-I` DOS COM member
at outer file `[06F3,0AE4)` (1,009 bytes), with runtime COM offset
`0100..04F1`. This module installs and removes PC-98 INT 06h/05h guards,
including their original vectors, displays STOP/COPY warnings directly through
the BIOS text/kanji planes, converts Shift-JIS pairs to the PC-98 character
encoding, waits for key release/press/release, and frees both the resident
block and the DOS environment block when uninstalled.

The semantic TASM source is [install.asm](install.asm). It uses named register
contracts, real interrupt service numbers, meaningful symbolic branches,
actual CP932 Japanese messages and no copied target-image bytes or meaningless
padding. The pinned ReC98 `th05_zuninit.asm` supplies an **IDA-generated
reference**, not the original historical source. The independent original
member MD5 `e22366913b7288f2ec82e280b386c86d` and SHA-256
`6091d53910b5a4bbcd132d663dc9531d8ea65cff95baf4307a3cd5e768e1e8b1`
confirm this is the TH05 `-I` payload, despite the older reference's `th04`
filename label.

## Independently reviewed physical boundaries

| Runtime COM span | Outer file span | Content | Bytes |
| --- | --- | --- | ---: |
| `0100..01EA` | `06F3..07DD` | Interrupt wrappers, warning renderer, character conversion | 234 |
| `01EA..02EC` | `07DD..08DF` | ZUNP magic, saved vectors, seven warning lines and state | 258 |
| `02EC..03C6` | `08DF..09B9` | Detection, command dispatch, install/uninstall | 218 |
| `03C6..04F1` | `09B9..0AE4` | Launcher messages and status strings | 299 |
| **Total** | **`06F3..0AE4`** | **Mixed CODE / initialized data** | **1,009** |

The two original `EVEN` NOPs are inside CODE at COM `0103` and `019B`.
Thus 452 compared CODE bytes contain **450 actual instructions** and 2
uncredited alignment bytes; the other **557 bytes** are initialized signature,
state and messages. The original uses one mixed `_TEXT` OMF segment; it is
incorrect to claim two separate physical DATA segments or copy the embedded
text into gameplay source.

## Exact focused native acceptance

The receipt
`.analysis/zun-interrupt/gpt-web-i-first-a/receipt.json` contains two
independent native TASM32/TLINK COM producers. Both reproduce all 1,009 bytes
with the exact original SHA-256, all eight real MAP public boundaries, a
single gapless CODE LEDATA at `ORG 0100` and deterministic normalized OMF.
The source negative changes the STOP-specific guard selection value, which
changes instruction bytes while retaining unchanged initialized messages and
is rejected by the complete original member comparison.

The stand-alone acceptance is in
[`config/zun_interrupt_acceptance.json`](../../../config/zun_interrupt_acceptance.json).
The focused verification command is:

```sh
python3 scripts/replay_zun_interrupt.py --check
```

The explicitly bounded replay is:

```sh
python3 scripts/replay_zun_interrupt.py --output .analysis/zun-interrupt/NEW
python3 scripts/replay_zun_interrupt.py --accept .analysis/zun-interrupt/NEW/receipt.json
```

**Source-origin limit:** original register-level assembly is strongly supported,
but the literal shipped source file is not known. Like the separately accepted
`-M` child, this complete COM acceptance is tracked separately from the
unfinished global authored-code denominator and the main EXE ownership map.
Do not count all 1,009 bytes as authored instructions or transfer credit to
ZUN.COM's remaining `-O`, `-S`, `-G` or outer launcher sections.
