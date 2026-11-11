# Complete original SUPERPTR drawing procedures in OP and MAINE

Five complete original Master source procedures at each of the OP/MAINE
rectangle-rendering entry points are now independently source-linked, for
**1,010 newly reviewed CODE bytes**. The actual original author archive
provides the full `SUPER_PUT_RECT` function and three near `PROC/ENDP`
drawing helpers plus a separate source-language error exit.

| Procedure | OP (full original extent) | MAINE | Bytes each |
| --- | --- | --- | ---: |
| `SUPERPTR_EXIT` | `2730..2736` | `296E..2974` | 6 |
| `SUPER_PUT_RECT` | `2736..2874` | `2974..2AB2` | 318 |
| `superptr_draw_shift` | `2874..28BA` | `2AB2..2AF8` | 70 |
| `superptr_draw_noshift` | `28BA..28EA` | `2AF8..2B28` | 48 |
| `superptr_draw` | `28EA..2929` | `2B28..2B67` | 63 |

The original source is `SUPERPTR.ASM` from the Master 0.23 author archive.
The native TASM translation unit only renames local scratch, branch and
self-modifying patch labels. The [source and OMF review](../../scripts/review_context_super_helpers.py)
compares each complete original `PROC/ENDP` or `FUNC` body to the
actual compiled assembler input, then resolves its real CODE LEDATA and
all ordered FIXUPP records into both original and calibrated executables.
All ten complete functions match every byte and their original empty
ordered MZ relocation streams.

The trailing **one-byte EVEN alignment** at OP `2929` and MAINE `2B67`
is **not included**. Likewise, the separate `SUPERPUT_DISP` functions
and their three alignment bytes have their own complete-source review
in [the OP/MAINE Master functions](CONTEXT_MASTER_LARGE.md), and are not
re-adopted here.

[Native original source proof](../../config/context_super_helpers.json)
and [explicit adoption](../../config/reviewed_context_super_helpers.json):

```sh
python3 scripts/review_context_super_helpers.py --check
python3 scripts/ownership.py --check
```

These are source-backed **third-party native Master ASM** bytes with
zero game-authored C++ credit. No full cold replay was run.
