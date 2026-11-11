# ZUN.COM `-O`: complete PMD / ADPCM RAM diagnostic

The original TH05 launcher contains a stand-alone `-O` DOS COM member at
physical outer-file `[0355,06F3)` (926 bytes), executing at COM offsets
`0100..049E`. The authentic target SHA-256 is
`4f9a9451f19bdd8d3ea8949a5ea75df6c2f92a9a84dcf39e1d7cf13421acc8a0`;
its MD5 is `7df7fd3a5135b646513ab1046b07c2d9`.

The maintained [register-level source](check.asm) implements ten complete
near functions. The entry detects the alternate `8`-mode switch, discovers
compatible sound-board ports, checks the PC-98 `FD80` board signature,
and negotiates the ADPCM register/transfer ports. The central diagnostic
then configures the ADPCM controller, uploads the original 32-byte printable
test signature, drains/readbacks the same 32 bytes, and compares them with
`REPE CMPSB`. Explicit polling timeouts, interrupt masks and board fallback
paths are retained; no added recovery, device probing, bounded startup check,
or host-side hardware execution is claimed.

The source contains human-readable register and hardware-service constants,
actual 8086 control flow and a semantic test phrase. It does not contain an
embedded original COM image, instruction byte string, filler, opcode emitter,
or precomputed binary bank. This original-register ASM is **inferred** from
the complete observed native behavior, not attributed to an independently
recovered historical source file.

## Physical boundaries and type-safe accounting

| Complete original COM extent | Description | Bytes | Credit |
| --- | --- | ---: | --- |
| `[0000,037C)` (runtime `0100..047C`) | Ten near procedures, original I/O loops and full register ABI | **892** | Compared instructions; historic origin unreviewed |
| `[037C,039E)` (runtime `047C..049E`) | 32-byte `*+=-PMD ADPCM RAM Check Data-=+*` and 2 initial status bytes | **34** | Initialized semantic DATA, not instructions |
| Runtime `049E..04C8` | Four word-sized I/O port handles, two selector bytes and 32 readback bytes | **42** | Original BSS, *not* in COM file |
| **COM payload** | **Original exact complete program** | **926** | No attribution transfer to global numerator |

The original TASM object contains three ordinary SEGDEFs: `_TEXT` size
`047Ch` including its `ORG 100h`, `_DATA` size `22h`, and `_BSS` size `2Ah`.
The two gapless LEDATA contributions contain exactly **892 CODE bytes** at
`0100` and **34 DATA bytes** at offset zero. BSS is deliberately absent from
both disk image and initialized-data accounting. All ten public procedure
addresses are checked against the original COM map, including the RAM
upload/readback loops and register-command helper.

## Focused native replay

The strict local receipt is
`.analysis/zun-adpcm/gpt-web-original-O-c/receipt.json`. It contains two
independent TASM32/TLINK producers, each yielding a **926/926 byte** full
SHA-256 match, real CODE/DATA/BSS segment and MAP/OMF boundaries, and
identical normalized objects. The compiled negative changes the genuine
hardware inter-register delay from 100 to 101 loop iterations. That source
mutation must change original instruction bytes, preserve the initialized
signature and status data, and is **rejected** by the complete binary oracle.

The accepted ledger is [`config/zun_adpcm_acceptance.json`](../../../config/zun_adpcm_acceptance.json).
Its source-current, lightweight check is:

```sh
python3 scripts/replay_zun_adpcm.py --check
```

The only supported reconstruction replay, **limited to this embedded 926-byte
child**, is:

```sh
python3 scripts/replay_zun_adpcm.py --output .analysis/zun-adpcm/NEW
python3 scripts/replay_zun_adpcm.py --accept .analysis/zun-adpcm/NEW/receipt.json
```

The accepted `-I`, `-G` and `-M` embedded children have distinct independent
acceptances and need no recompile. The large `-S` child and outer ZUN.COM
container still require their own original-source investigation. This
focused exact child must not be interpreted as a global authored-code ratio,
proven original source syntax or complete launcher reconstruction.
