# Extra Alice hexagram drawing

The complete natural C++ helper at original MAIN `114BE..1158A` is accepted:
**204 instruction bytes, one near Pascal function**. It contains 58 native
instructions, no instruction NOPs, no CODE data, no padding and no owned DATA
or BSS. Its RET4 begins at11587 and ends at the complete1158A boundary. The
following hexagram animation starts at1158A and is a separate accepted scope.

The candidate-local-attested Japanese MAIN.EXE is pinned in
`config/targets.toml`, SHA-256
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
The original complete function SHA-256 is
`e047654a8839c0bbbc58e2d8de655b7c92c8d74a248580c1da86cbe7362da52c`.
Native frame is AE1, DS209D. Every direct branch destination was checked
against a real instruction boundary. The original ordered loader sites are
`[182,161,140,89,70,51,27]`, including the true zero-valued far segment words.
No sorting, masking or normalization is allowed.

## Semantic source and ABI

The maintained source derives from the natural ReC98 `b6ba5b0a` C++ algorithm,
`th05/main/boss/render.cpp`, already represented in `background.cpp`. The new
standalone file preserves that maintained function body, both center constants
and its point-construction macro literally. The older split source and its
17 accepted function snapshots are unchanged. The legacy helper definition
remains outside those accepted scopes; it receives no duplicate credit.
Whole-program linking of both alternative compilation contexts is not claimed.

The helper draws a circle centered at pixel224,200, then two equilateral
triangles. Their vertices use the genuine vector provider with the full
canonical four-byte Point types and Q12.4 radius. Integer angles are spaced
by256/3; the second triangle rotates by256/6. Each coordinate is converted
in-place to pixels by signed right shift4 before drawing its three edges.
No vertices, sprites, target bytes, opaque tables or hardware instruction
bodies are embedded in the source.

Near Pascal arguments are two words: angle at BP+4 and radius at BP+6. All
seven static provider calls remain actual C far Pascal calls:

| Provider | Original frame:offset | Parameters / cleanup |
| --- | --- | --- |
| GRCG_CIRCLE | 0000:10AE | center X, center Y, unsigned radius / RETF6 |
| VECTOR2_AT | 14AB:03B0 | real SPPoint near reference plus four signed words / RETF10 |
| GRCG_LINE | 0000:1716 | four signed pixel coordinates / RETF8 |

The unchanged `background.hpp`, `movement.hpp`, `geometry.hpp` and `abi.hpp`
retain full class identities and layouts. Scratch points are foreign: drawpoint
DS36FE, tri_point_1 DS443C and tri_point_2 DS4440. Their bytes are not supplied
or credited. The standalone source adds no new declaration or shortened view
of any provider, record or calling convention.

## Why a standalone producer is needed

The old monolithic diagnostic `compiler-probes/boss-bg-c` produced matching
204-byte raw code and the correct seven relocations, but had only one positive
and no own negative. It was not accepted. The later split background producer
has the same raw helper bytes, but a real LEDATA boundary through the function
changes relocation collection order. That original failure remains unchanged;
a byte match alone cannot satisfy the oracle.

The standalone compilation emits this one complete function in one ordinary
CODE SEGDEF/LEDATA contribution. It retains all seven relocations in the true
original order. This is a new actual producer context, not a normalized result,
clipped object, recycled old build or altered relocation stream.

The independent symbol-only binder establishes AE1:66AE and DS209D, actual
far providers, and outside-contribution extents. Every ORG is below64KiB.
It contains no instructions, scratch values, inside-function hole or artificial
stack. Actual OMF/MAP checks show 204 owned CODE bytes, empty compiler DATA/BSS
and the correct real group frames. The original 17 accepted functions are not
recompiled or changed.

## Acceptance

Only `.analysis/unit-replays/main-exalice-hexagram-standalone-b/receipt.json`
is imported. Receipt SHA-256 is
`c7fb4b746245ee13f3cad798ae7a119dc6b998948a3620334cbc64382bc348aa`.
It contains two fresh isolated compiler/assembler/linker producers, deterministic
normalized OMF and byte-identical complete comparison MZ files, all204 raw bytes
and the exact original ordered relocation stream. Saved producer import
re-reads actual source, wrappers, objects, MZ/MAP and tool identities.

The own compiled negative changes the real triangle rotation256/6 to256/5,
from42 to51 angle units. Its changed geometry is rejected by the full oracle;
its complete size and relocation stream remain checked. The first `-a` launch
stopped in binding assembly on missing CS assumptions before any C++ compiler
invocation; `-b` supplies the correct foreign segment assumptions. No failed
attempt supplies accepted producer credit. All retained artifacts stay private.
The unchanged installed tool execution proof is reused.

Independent native/source/actual-producer review:
`.analysis/exalice-hexagram-standalone-review.json`, SHA-256
`ddab46db76366afd0f480543df7dfbf96c5e74e21816b3a577c75d485bea5d6a`.
This adds only204 C++ instruction bytes and one function. It changes no ASM,
DATA, padding, vendor, resource, whole-program or packed-file claim.

Saved import,317-test public CI, native ownership verification and all four
empty incremental plans pass. Root final review:
`.analysis/exalice-hexagram-root-final-review.json`, SHA-256
`cc2db7566ffb19beacb456b7878e9949f43874c937ef443e7901f684ee7da243`.
