# TH05 memory-check child

`check.asm` is a maintained **original-style assembly candidate**, with origin
still inferred. It represents the `-M` child embedded in the attested ZUN.COM
container, not the outer launcher's entry point.

The strongest origin evidence is the bare COM entry with no C runtime, direct
stack relocation after DOS block resizing, register-only decimal-formatter
arguments, and complete FLAGS/general-register preservation through
PUSHF/PUSHA/POPA/POPF. TH04's memory-check child instead has a C `main` and CRT;
its C++ implementation does not establish the provenance of this TH05 code.
ReC98 `th05_memchk.asm` explicitly identifies itself as an IDA-generated view.
Its matching input digest corroborates the child boundary, not original source.

No literal historical source has been recovered. The candidate uses semantic
labels and DOS service constants, contains no copied opcode arrays or filler,
and spells the original Japanese messages as text. The maintained file is
**UTF-8**, with LF line endings. The replay explicitly encodes its frozen source
as **CP932** before assembling; this preserves the original DOS string bytes.

## Target boundaries and ABI

All container offsets below are half-open, relative to the pinned original
`.analysis/targets/th05/zun.com`, SHA-256
`5044ae03f7c0333f37d88ef34e244502f90d7314287f6f387c07569e4e0b120e`.
For this child, `runtime COM offset = container offset - 0x4541 + 0x100`.

| Surface | Container extent | Child COM extent | Bytes |
| --- | --- | --- | ---: |
| Memory-check entry/control | `0x4541..0x45A0` | `0x100..0x15F` | 95 |
| Decimal formatter | `0x45A0..0x45CF` | `0x15F..0x18E` | 47 |
| Messages and exit status | `0x45CF..0x4678` | `0x18E..0x237` | 169 |
| Complete child | `0x4541..0x4678` | `0x100..0x237` | 311 |

Code totals **142 bytes**; initialized data totals **169 bytes**. There is no
alignment exclusion or decoded-image relocation table for this plain COM child.
The complete child SHA-256 is
`d2725dac923e8f6d50aa503f0d67461890ee913f53d7bebeeedeabe6dc7746b6`;
its MD5 is `5e401a5cd3d8d42dc67130359c42a7cf`.

At entry, DOS COM conventions give CS=DS=ES=SS at the child's PSP and IP=`0x100`.
The image ends at COM `0x237`. The program requests `0x34` paragraphs after
rounding the image and reserving 16 stack paragraphs, then sets SP=`0x340`.
It uses INT 21h services 4Ah, 09h, 48h, 02h and 4Ch. It deliberately retains
the unchecked carry/error behavior of the original code.

The capacity check compares the returned largest contiguous block against
32,500 paragraphs (520,000 bytes). The decimal helper receives its unsigned
value in AX and the highest printed decimal place in CX, preserving FLAGS and
all general registers. Calls use CX=10 and CX=1000 to emit two and four digits;
this routine does not print arbitrarily large values without truncating higher
decimal positions.

Data addresses in the child's shared segment are:

| Symbol | COM offset | Container offset | Bytes |
| --- | --- | --- | ---: |
| `memory_intro` | `0x18E` | `0x45CF` | 32 |
| `memory_bytes_suffix` | `0x1AE` | `0x45EF` | 16 |
| `memory_insufficient` | `0x1BE` | `0x45FF` | 91 |
| `memory_ready` | `0x219` | `0x465A` | 29 |
| `memory_exit_code` | `0x236` | `0x4677` | 1 |

## Replay scope

The proposed standalone producer is `.186`, tiny model, `ORG 100h`, assembled
with the attested TASM32 and linked as COM with TLINK `-t`, without a C startup
object. Named public entries identify the control and formatter bodies. No
external-symbol scaffold is necessary: messages and both functions belong to
the same complete child.

Two fresh assembly/link rounds now reproduce the complete **311-byte payload
exactly**. OMF integrity, TASM identity, public entry offsets and deterministic
objects pass. A third compiled producer changes 32,500 to 32,501 paragraphs;
the full comparison correctly rejects it. Public acceptance is recorded in
`config/zun_memory_acceptance.json`; its source/manifest fingerprints are
checked by CI. The exact replay is `.analysis/zun-memory/first-b`.

```sh
bash scripts/run_heavy.sh python3 scripts/replay_zun_memory.py --output .analysis/zun-memory/NEW
python3 scripts/replay_zun_memory.py --accept .analysis/zun-memory/NEW/receipt.json
python3 scripts/replay_zun_memory.py --check
```

Runtime semantics and the outer ZUN container's composition remain separate.
Any accepted original-style ASM code/data must be reported separately from
compiler-generated C++ instruction credit and the unreviewed global denominator.
