# Exact unmasked .PI drawing in OP and MAINE

The two natural C++ wrappers `pi_put_8()` and `pi_put_quarter_8()` now
have complete original function matches in both decoded game executables:

| Program | Full-size drawing (47 bytes) | Quarter drawing (70 bytes) |
| --- | --- | --- |
| OP | `DE0A..DE39` | `DE3A..DE80` |
| MAINE | `EFB2..EFE1` | `EFE2..F028` |

The one-byte `EVEN` alignment NOP at `DE39` / `EFE1` is outside both
functions and remains uncredited. The original far-Pascal calling conventions,
external PI header and far image-buffer arrays, and near `pi_put_8_rowloop`
provider are preserved. `pi_put_8()` gets the actual 72-byte PI header's
X/Y sizes and packed row stride. The quarter function uses the original
320-pixel and 200-row geometry, including the 160-byte horizontal offset
and 4,000-paragraph segment shift used to select the specified quadrant.
The functions follow pinned ReC98 `th05/formats/pi_cpp_2.cpp` and
`th05/formats/pi_impl.hpp`, with semantic register/near-call assembly only.

Both objects are built via the unchanged TCC `-S` → TASM32 → TLINK pipeline.
The isolated near row helper is an address-only foreign provider; a proof-local
CS group connects the foreign CODE segment to the source contribution without
injecting its instructions or changing native bytes. The 135-byte masked and
58-byte unmasked row kernels already accepted in the repository are not
included or counted here.

Focused receipts, each with two original-toolchain positive producers, a
complete byte/fixup match and a compiled negative:

- `.analysis/unit-replays/gpt-web-op-pi-plain-full-a/receipt.json`
- `.analysis/unit-replays/gpt-web-op-pi-plain-quarter-a/receipt.json`
- `.analysis/unit-replays/gpt-web-maine-pi-plain-full-a/receipt.json`
- `.analysis/unit-replays/gpt-web-maine-pi-plain-quarter-a/receipt.json`

The full-source negative changes the PI buffer-pointer index shift; the
quarter negative changes the horizontal offset by one. All four negatives
are rejected. No full cold replay was used.
