# Exact outer COMCSTM packaging header and wrapper

The physical TH05 ZUN.COM outside wrapper consists of a 39-byte COMCSTM
header at original `[0000,0027)`, a 264-byte Shift-JIS/CP932 Japanese help
text at `[0027,012F)`, and a complete 68-byte vendor startup stub at
`[4680,46C4)`. The first three bytes form a real near jump across the
entire inner executable; the other 36 header bytes carry usage/inner pointers,
lengths, the original DOS timestamp `2579AF64h`, and the
`comcstm (c)O.Morikawa 1996` copyright notice.

The maintained source [outer.asm](outer.asm) derives its COMCSTM header from
the actual `Pipeline/comcstm.c` algorithm and the wrapper from
`Pipeline/cstmstub.asm`. It prints usage via DOS INT21/AH40 when asked for
`-?` or `?`, or moves the entire inner COM from the original far offset down
to runtime `0100` using `REP MOVSW`. The original 264-byte usage text is
maintained as readable [UTF-8](usage_ja.txt), with a private CP932 generation
step preserving the original file's final lone carriage return. The original
`-I` usage line ends in a significant ASCII space; the maintained UTF-8
source spells that space with the visible `␠` marker, which the private
serializer converts back to one literal space before CP932 encoding. The source
does not embed hex strings of target executable bytes.

## Exact physical comparison and exclusions

| Original ZUN.COM file interval | Source data | Bytes | Category |
| --- | --- | ---: | --- |
| `[0000,0003)` | Native entry jump | 3 | CODE |
| `[0003,0027)` | COMCSTM usage/inner offsets, timestamp and copyright | 36 | Semantic header DATA |
| `[0027,012F)` | Japanese usage message | 264 | Semantic text DATA |
| `[012F,4680)` | Independently embedded inner executable | **17,745** | **Foreign proof-only zero ORG hole** |
| `[4680,46C4)` | Complete COMCSTM wrapper and memory-copy logic | 68 | Third-party CODE |
| **Compared source-owned total** | **Two discontiguous original scopes** | **371** | **71 CODE + 300 DATA** |

The proof-only COM has the original 18,116-byte size, but the 17,745-byte
inner hole is filled with **zero**, not with any proprietary child or copied
original bytes. It is therefore *not* a reconstructed full ZUN.COM.
The separately accepted [inner dispatcher/catalog](README.md) proves 558
of those inner bytes independently; the `-S` resident executable remains
inexact. No global authored-byte credit is claimed for this third-party
packaging wrapper.

## Independently reproduced native evidence

Focused receipt:
`.analysis/zun-outer/gpt-web-outer-clean-b/receipt.json`.
Two independent TASM32/TLINK producers match every original source-owned
byte: 39/39 header, 264/264 usage and 68/68 wrapper. The real OMF has exactly
one 303-byte LEDATA at `ORG 0100` and one 68-byte LEDATA at `ORG 4780`, two
ordinary CODE/DATA segment descriptors, no other initialized payload and
six genuine MAP public positions. A compiled source negative changes DOS
output handle 1 (stdout) to 2 (stderr); only the wrapper instruction bytes
change, while header, usage, and all foreign gaps remain unchanged.

The accepted standalone evidence is
[`config/zun_outer_acceptance.json`](../../../config/zun_outer_acceptance.json).
The lightweight source-current check needs neither Wine nor the original
ZUN.COM asset:

```sh
python3 scripts/replay_zun_outer.py --check
```

The only native work in the local focused replay is the outer wrapper:

```sh
python3 scripts/replay_zun_outer.py --output .analysis/zun-outer/NEW
python3 scripts/replay_zun_outer.py --accept .analysis/zun-outer/NEW/receipt.json
```

The original COMCSTM construction procedure is visible in pinned ReC98 but
that reference does not by itself prove literal historical source identity;
third-party vendor ownership remains distinct from ZUN's own program code.
