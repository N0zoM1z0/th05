# CDG loaders and `cdg_free()` (ASM)

`cdg_load_family.asm` covers MAIN `[15118,1526E)`, following ReC98
`th04/formats/cdg_load.asm`. Entry points, by offset:

| Offset | Function |
| ---: | --- |
| +0 | `cdg_load_single_noalpha()`: sets `cdg_noalpha`, falls through |
| +6 | `cdg_load_single()` |
| +102 | `cdg_read_single()` (near helper) |
| +190 | `cdg_load_all_noalpha()`: sets `cdg_noalpha`, falls through |
| +196 | `cdg_load_all()` |
| +288 | `cdg_free()` |

The loaders read the 16-byte CDG header, seek to the requested image
according to its plane layout (colors, alpha, or both), and allocate and read
the alpha and four color planes into segments. `cdg_load_all()` copies the
first 12 header bytes into each following slot with `REP MOVSD` (three
DWORDs). ZUN landmine: no file or allocation errors are handled.

The original has NOPs at offsets 5, 15, 101, 195 and 341. Four come from
`EVEN`. The one at +15 belongs to the same-segment far call to `cdg_free()`,
which TLINK relaxes to `PUSH CS` / near call; ReC98 writes it out explicitly.
Leaving it out also shifted the following `EVEN` and made the result two
bytes short.

The same source is used for OP and MAINE; see
[cdg_load_family_op_maine.md](cdg_load_family_op_maine.md).
