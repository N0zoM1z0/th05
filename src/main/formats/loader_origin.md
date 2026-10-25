# Deferred STD and MAP loader origins

A fresh read-only native and source-history review keeps both loaders unknown.
No new compiler or assembly producer was run for either loader.

| Function | Complete MAIN range | Bytes / instructions | Ordered MZ fixups |
| --- | --- | --- | --- |
| STD load | C742..C7FA | 184 / 72 | [43, 173] |
| MAP load | E5C2..E606 | 68 / 29 | [41] |

Both have a near RET, no instruction NOP and no embedded table or padding.
The allocator fixups bind the real FAR HMEM_ALLOCBYTE at 0000:281A. STD's
second fixup is the stage callback selector 1527; its offset 1906 resolves to
the already accepted STD interpreter at load 16B76. These observations do not
change ownership of that interpreter, either free function, globals or assets.

STD changes DS/ES to its allocated segment, shares the DI/CX cursor across
three REPNE SCASB title scans, and uses MOVZX byte reads during script parsing.
This suggests hand-managed assembly, but is insufficient independent historical
language evidence. The external no-argument near API is ordinary. Pinned ReC98
b6ba5b0a's pseudo-register/emit reconstruction and history 325818bf/261d5037 do
not explicitly attribute this body to ZUN-written ASM. They are candidate
evidence, not maintained source or proof of its producer.

MAP's raw DOS read/allocation sequence and DS swap offer weaker language
evidence. Its available TH05 reference is an instruction listing; the TH04 C++
donor changes file APIs and release sequencing. Neither is copied into a counted
body. No original compiler, ASM or vendor classification follows from this gap.

The bounded 653-member vendor review found the real allocator's MEMHEAP.ASM
ancestry. Raw DOS and string-scan idioms are widespread; missing game-format
names do not prove originality of the surrounding loaders. Retain the unknown
252 bytes in the denominator partition. Full formats, native globals, ABI,
DF requirements, DOS error behavior and unchecked parser behavior are in private
`.analysis/std-map-loader-native-origin-review.json`, SHA-256
`45f6604a3bfb648f54d326390770674d825805c8f41d66765b3424303e9423c3`.
Earlier source and free-function outcomes remain in [format notes](README.md).
