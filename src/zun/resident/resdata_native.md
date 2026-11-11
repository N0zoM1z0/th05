# Exact Master PC-98 graphics and resident memory functions in ZUN `-S`

Three complete Master library functions are now source-exact at ZUN's
resident COM offsets `05B6..0698` (**226 bytes**):

| Original near procedure | COM range | Full bytes |
| --- | --- | ---: |
| `GRAPH_CLEAR` | `05B6..05DA` | 36 (35 instructions + 1 `EVEN`) |
| `RESDATA_EXIST` | `05DA..0622` | 72 |
| `RESDATA_CREATE` | `0622..0698` | 118 (117 instructions + 1 `EVEN`) |

`GRAPH_CLEAR` sets PC-98 GRCG black-tile mode through ports `7C/7E`, clears
one caller-selected page using the real foreign DS video segment and word
count at `185C/185E`, and restores the GRCG control mode. This source is
preserved from the original Akihiko Koizuka Master `graph_clear.asm` in
[graph_clear_native.inc](graph_clear_native.inc), with named hardware globals
and no inferred video allocations.

`RESDATA_EXIST` scans DOS memory control blocks from INT21/AH52, comparing
resident ownership, size and the supplied identifier. `RESDATA_CREATE` saves
the DOS allocator strategy, attempts lower/higher memory placement, assigns
MCB ownership, copies the identifier and restores the strategy. The original
8086 near-Pascal register logic and full `RET 6` cleanup are kept in
[resdata_native.asm](resdata_native.asm), based on pinned ReC98
`libs/master.lib/resdata.asm`.

## Focused native acceptance

Receipt `.analysis/zun-resdata/gpt-web-graph-resdata-c/receipt.json` contains
two independent TASM32/TLINK producers. Each emits **226/226 exact bytes**,
with two contiguous original CODE LEDATA records (36 and 190 bytes), all
four original MAP publics and a deterministic OMF. A semantic negative
changes the MCB size-field offset, which changes instructions but preserves
both natural `EVEN` bytes. The **224 instruction bytes** and **two uncredited
padding bytes** are reviewed separately, without crediting data or source-free
nearby CODE.

The first `0100..05B6` bytes in the isolated tiny COM are a foreign zero ORG
reservation. The original global DS video words are referenced by address,
not supplied with values or patched. This is the historical **Master vendor
library**, with zero game-authored credit.

Accepted scope: [`config/zun_resdata_acceptance.json`](../../../config/zun_resdata_acceptance.json).
Source-current validation and affected-only native replay:

```sh
python3 scripts/replay_zun_resdata.py --check
python3 scripts/replay_zun_resdata.py --output .analysis/zun-resdata/NEW
python3 scripts/replay_zun_resdata.py --accept .analysis/zun-resdata/NEW/receipt.json
```

The adjacent [Master file/DOS family](file_family_native.md) is separately
accepted at `0698..09D6`. Together these provide **1,056 consecutive exact
bytes** (**1,047 instructions and nine NOP alignments**) in `-S`, without
claiming the still-unaccepted 269-byte ZUN C++ entry or a whole program build.
