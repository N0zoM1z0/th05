# Exact ZUN `-S` buffered file I/O Master providers

Four complete original Master library procedures now have a contiguous
**356-byte** source-built exact match in the resident `-S` COM member:

| Source function | Original COM offsets | Full bytes |
| --- | --- | ---: |
| `FILE_READ` | `0698..074C` | 180 (179 instructions + 1 `EVEN`) |
| `FILE_FLUSH` | `074C..07B8` | 108 (107 instructions + 1 `EVEN`) |
| `FILE_CLOSE` | `07B8..07C6` | 14 |
| `FILE_ROPEN` | `07C6..07FC` | 54 |

The maintained [`file_family_native.asm`](file_family_native.asm) links
original-source algorithm bodies from `master_read.inc`, `master_close.inc`
and `master_ropen.inc`, using the actual near-Pascal tiny-model macros in
`master_file_tiny.inc`. These are the pinned Master assembler sources by
Akihiko Koizuka with comments normalized to English, not target-derived
opcode or lookup byte arrays.

The functions implement DOS buffered reads (including read-buffer exhaustion,
EOF accounting and direct-I/O fallback), buffered flush/seek, close, and
read-open error propagation. All original external near call addresses and
actual file state offsets in DGROUP are preserved. Source-free holes reserve
the `DOS_ROPEN` provider at `09BE`, other CODE through `16BE`, and foreign
file buffer state at `1872/1874/1AAA..1AB8`. No provider instruction or
initialized file state is supplied or credited.

The focused receipt is
`.analysis/zun-file/gpt-web-file-family-b/receipt.json`. Two independent
TASM32/TLINK builds match **all 356 original bytes**, all four MAP public
function positions, their true single 356-byte CODE LEDATA and original
deterministic OMF. A semantic source negative substitutes the in-buffer
read length for the current buffer position when checking exhaustion; it
changes real generated instructions and is rejected. The two original
`EVEN` bytes at function-relative +131 and +287 are compared but earn zero
code credit. Of 356 bytes, **354 are executable instructions**.

The separately accepted adjacent `RESDATA_EXIST` and `RESDATA_CREATE`
[functions](resdata_native.md) end at `0698`. Together they provide an exact,
continuous **546-byte** source reconstruction at `05DA..07FC`, independent
of and without changing the ZUN resident `main()` C++ entry. All of these
are **original Master vendor library ASM**, so they have zero game-authored
source credit. This is not a claim of a complete `-S` COM build.

Focused source-current acceptance:

```sh
python3 scripts/replay_zun_file_native.py --check
```

Explicit affected-scope native replay:

```sh
python3 scripts/replay_zun_file_native.py --output .analysis/zun-file/NEW
python3 scripts/replay_zun_file_native.py --accept .analysis/zun-file/NEW/receipt.json
```
