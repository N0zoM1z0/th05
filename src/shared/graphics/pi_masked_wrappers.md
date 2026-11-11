# TH05 masked .PI drawing: exact OP and MAINE C++

The full-screen `pi_put_masked_8(left, top, slot, mask_id)` and
quarter-screen `pi_put_quarter_masked_8(left, top, slot, quarter, mask_id)`
are now complete source-owned C++ functions in both decoded programs:

| Program | Full screen | Quarter screen | Total |
| --- | --- | --- | ---: |
| OP | `DC94..DCC6` (50) | `DCC6..DD0F` (73) | 123 bytes |
| MAINE | `EE3C..EE6E` (50) | `EE6E..EEB7` (73) | 123 bytes |

The function pair uses the real 72-byte PI headers and far image-buffer
pointers, with the original Pascal stack arguments and 386 register operations.
The first function selects the actual image width and row stride; the quarter
version translates the quarter's two-bit selection into pixel/segment offsets
and draws a 320×200 region. Both call the independently accepted near masked
row kernel at OP `DD10` / MAINE `EEB8`. Source semantics follow pinned ReC98
`th05/formats/pi_cpp_1.cpp` and `th05/formats/pi_impl.hpp`. Image data,
headers, the row kernel, and the standalone NOPs at OP `DD0F` / MAINE `EEB7`
remain outside the two new function owners.

Native code for both functions is reproduced using the authentic TCC `-S` →
TASM32 → TLINK pipeline. The external row kernel belongs to the same original
CS even though an isolated replay binder reserves its foreign near entry in a
separate CODE segment. The proof-only CODE group resolves this near address
without supplying any instruction bytes or changing either source function.

Focused receipts:

- `.analysis/unit-replays/gpt-web-op-pi-masked-wrappers-a/receipt.json`
- `.analysis/unit-replays/gpt-web-maine-pi-masked-wrappers-a/receipt.json`

Each contains two fresh positive producer runs, complete 123-byte exact
comparisons, original empty ordered MZ relocation streams, real MAP/OMF
contribution checks, and a compiled negative changing the 160-pixel quarter
horizontal offset to 159. The negative was rejected in both programs. There
is no overlap with the previously accepted masked row painter or graphics
assets, and no full cold replay was run.
