# Eight-cell HUD bar

This semantic ASM candidate covers only MAIN D474..D4C0, one complete
76-byte near Pascal procedure. The canonical caller takes row, integer value
and attribute, with RET6 cleanup. Reading only the low byte does not narrow
the public value type. Existing accepted C++ declarations remain unchanged.

The native routine captures BX=SP before saving DI, queues the real far
GAIJI_PUTSA arguments, then reuses BL as its byte bar value. It writes through
ES:DI while packing cell count and glyph selection into byte registers.
This interacting stack/register/string protocol supports an inferred original
handwritten ASM owner; modern donor syntax alone does not establish origin.
Historical source, original assembler and exhaustive vendor ancestry remain
unproved. Pinned ReC98's th05/hud_bar.asm is a semantic reference only.

Eight cells each represent 16 units. Values at least 128 select distinct full
glyphs 30h..37h. Smaller values use repeated 2Fh cells, one fractional glyph
20h..2Fh, then empty glyphs 02h. Native zero intentionally wraps the fractional
index and displays one full cell; the reconstruction adds no zero guard.
The procedure reads the low byte even when the public integer is negative
or exceeds 255. It requires clear DF on entry and does not insert CLD.

The foreign buffer is nine bytes at DS:142C: eight generated glyphs followed
by its existing terminator. No glyph bitmap, initialized buffer, terminator
value or foreign renderer body is supplied. DI is restored; ES is set to DS
before the renderer call. The actual call is FAR 0000:1DBE and its only ordered
MZ relocation is at relative 70. The code frame is 0AE1 and DS is 209D.
All 36 native instructions are decoded; there are no instruction NOPs,
tables, padding or owned DATA/BSS. The following score routine is excluded.

The maintained source contains geometry, symbolic glyph IDs, named stack
fields, semantic loops and the real external surfaces. No target bytes,
foreign instructions or compiler-generated body is supplied. A symbol-only
binder places the full contribution in its original group and preserves the
actual far-provider context. Exact replay and explicit adoption are separate
requirements.

Independent native/source/origin review:
`.analysis/hud-bar-independent-origin-source-review.json`, SHA-256
`c418552280dd5148af14ea8d36b3231527f784a89f9ed9fcaa17d677e4a8767a`.
A native-only independent geometry model passes 267 cases, covering all byte
values, 11 additional integer-truncation cases, exact eight-byte writes,
untouched terminator/canaries, actual far argument order and RET6 cleanup.
The far renderer is intercepted rather than executed in that model; its
native boundary review separately verifies RETF10 and preserved DS/SI/DI/BP.
ES is not promised preserved after that real provider.
Model report: `.analysis/hud-bar-native-semantic-check.json`, SHA-256
`2743dd52c719cd62871fc3ca5611816213eff6a9aa0ceedcd94127e43b6ebbb3`.

Receipt `.analysis/asm-replays/main-hud-bar-a/receipt.json`, SHA-256
`2de65d3fcd49edc5130c0d21b9fe81a3d5b6523fdb5d3841076aa6ca41bb5ca6`,
passes two fresh independent complete producers. Both have one ordinary
76-byte CODE SEGDEF/LEDATA, original group/frame/public boundaries, identical
full linked bytes and ordered fixups `[70]`. The own capacity mutation from
128 to 127 retains the whole scope and changes only byte 31; comparison rejects
it. Actual source aliases, assembler/tool identities, arguments, logs, OMF,
MAP and MZ are re-read by the unchanged validator. The installed tool execution
proof and unchanged accepted units are reused after identity checks.
No source/instruction/flag variants or additional first-producer builds occur.
Explicit ownership adoption remains separate from this replay.

Independent actual-producer review:
`.analysis/hud-bar-actual-replay-independent-review.json`, SHA-256
`b714db6f0014ab417443ae6d00f5f7e5dcc0418b53f3837e19911d3355368b6f`.

The separate decision in `config/reviewed_asm_families.json` adopts only this
complete procedure as 76 reviewed ASM instruction bytes. It grants no C/C++,
foreign DATA, glyph-image, renderer-provider or whole-executable credit.
