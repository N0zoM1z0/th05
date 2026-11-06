# Exact background-plane release

The natural body follows maintained TH04 `src/shared/hardware/bgimage.cpp`
and pinned ReC98 b6ba5b0a `th04/hardware/bgimage.cpp`. It checks B, releases
B/R/G/E in order through the actual far Pascal `hmem_free` interface, then
clears only B. The other three segment handles retain their original values.
The complete canonical eight-byte plane structure contains four two-byte
segmented pointers; its type and accepted consumers remain unchanged.

| Decoded artifact | Complete function | CS / DS | Allocator | Original ordered fixups |
| --- | --- | --- | --- | --- |
| OP | D726..D758, 50 bytes | D300 / EFE0 | 0000:2426 | 14, 23, 32, 41 |
| MAINE | EC0A..EC3C, 50 bytes | E800 / 10110 | 0000:2664 | 14, 23, 32, 41 |

Each function consists of 12 instructions, ending in RETF, with one conditional
branch to that return. There are no NOPs, tables, padding, initialized DATA or
BSS. SHARED is genuinely ungrouped. The four-plane objects at DS09E4/DS06C2,
allocator providers and all neighboring code remain foreign.

Existing direct-object calibration already matched OP's 50 raw bytes but
emitted descending fixups. A new actual TCC `-S` / TASM32 diagnostic established
all 50 bytes and the original ascending order before extending the maintained
recipe to decoded artifacts. The ordinary C++ body and header are unchanged.
TASM consumes the compiler's complete, unedited output; the semantic wrapper
only includes that file. No instruction, OMF record or fixup is repaired.

Both independent focused replays pass two fresh deterministic producers,
complete ordinary OMF/MAP scope, all raw bytes and the original ordered
relocations. Each compiled E-to-G release-argument negative changes only
byte 36 within its own 50-byte scope and is rejected. Actual compiler binary
options are O for OP and E for MAINE. Frozen decoded payloads and relocation
streams are revalidated against their pinned original target proofs; this
is no packed-file exactness claim.

Acceptance adds two complete C++ function occurrences and 100 instruction
bytes, with no ASM or DATA credit. The 386-byte Shinki wing owner was the only
previously accepted unit affected by the recipe change; its fresh replay passes
and replaces its evidence without adding coverage. Other accepted objects and
installed tool probes are reused after input identity checks. No whole cold
replay or game behavior model runs.

Native boundary/ABI review:
`.analysis/bgimage-free-compiler-assembly-native-review.json`, SHA-256
`fddb90360bf59524f01aa042c9509130f1735a3d34f2e85f5157691371a1f1be`.
The saved decoded-proof audit rejects five changed-artifact cases without compiler invocations at `.analysis/bgimage-free-decoded-proof-audit.json`.

OP receipt: `.analysis/unit-replays/op-bgimage-free-compiler-assembly-a/receipt.json`,
SHA-256 `4d09585180a9c32bcd64230d11d33ae242108a2e3d6887dde501e47412d2585e`.

MAINE receipt: `.analysis/unit-replays/maine-bgimage-free-compiler-assembly-a/receipt.json`,
SHA-256 `5925d7b48be03ff0534727ac41b59cbca54d2aa15909273a16c399f29b23fbd9`.
