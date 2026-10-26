# Cheeto 32x32 worker: bounded native routing, no acceptance

The unique MAIN private worker `@cheeto_put` occupies DE72..DF28: 182 complete
bytes, including four alignment NOPs at relative 41/63/71/93. All 81 decoded
instructions are covered; original ordered MZ fixups are empty. The public
outer routine ends with RET at relative 101. Its internal even-row helper is
102..138 and odd-row helper 138..182, each ending in near RET. The neighboring
DOS loader DE58..DE72 and scroll provider DF28..DF50 are excluded.

AX supplies left pixels, DX the video-ring top, BX the sprite index and ES
the video plane. The outer routine restores SI/DI and preserves BP/DS/ES/IF.
EAX/BX/CX/DX and arithmetic flags are scratch. Clear DF is required for the
LODSD/STOS string operations. Row helpers split CL shift, CH rows remaining,
DL initial mask, DH next carry, BL current carry and BH two-word counter;
DEC CH returns ZF directly to the outer row loop. These live private register
and flag contracts support inferred handwritten ASM, independently of modern
candidate file syntax. They do not establish authored ownership.

The complete foreign BB bank is 16 sprites of 32 rows, four source bytes per
row: 2048 bytes at DS:378A..3F8A. Its runtime storage is BSS beyond the observed
loaded-image extent, so it is unobserved/uncredited, rather than an observed
unknown interval. No pixel data or new storage is supplied. Each source row
writes five destination bytes, including zero masks, with byte/WORD order
selected for even/odd destinations. A bottom crossing continues at video
row zero. No clipping or invalid-coordinate handling is added.

## Semantics without producer acceptance

A native-only model passes 1280 cases using an entirely generated 2048-byte
bank. Its independent MSB-first per-pixel model covers all 16 sprites, all
eight shifts, both byte parities, zero/full/alternating/generated patterns,
and top rows 0/367/368/369/399. It checks all 96 write events per sprite,
including zeros, addresses/widths/values, bank immutability, preserved private
ABI state and plane canaries. It models mask writes, not colored GRCG
framebuffer effects, and covers only clear DF and valid coordinates.

Model report: `.analysis/cheeto-put-native-semantic-check.json`, SHA-256
`3494a75e878d7af1aa168145004ee5d9b6fe1d3471a82b0f9a0d6b8263fa25b7`.
No compiler/assembler/linker invocation, receipt or adoption was attempted.
Semantic agreement gives zero authored credit and no byte-exact source claim.

## Ancestry gate before reconstruction

The modern pinned candidate th05/formats/bb_cheeto.asm explicitly adapts
z_super_roll_put_tiny_32x32. That donor's header attributes its lineage to
Master SUPERRPT and both Koizuka and ZUN. Primary Master SUPERPUT/SUPERPVR
also share rotate/mask/carry packing techniques. Such specific positive
ancestry requires a separate ownership review; acceptance of the older
16x16 worker does not transfer to this distinct 32x32 body.

The strongest literal primary-source matches are the three-operation
rotate/move/mask idioms at DEDE..DEE4 and DF0D..DF13, six native bytes each,
corresponding to SUPERRPT.ASM lines 157..159 and 177..179. No primary assembly
was built here, so this is an operand-level source comparison, not a proved
primary-object byte match. These short idioms alone do not assign vendor
ownership. The longer ring driver DE9C..DED5 and carry helpers DED8..DF28
have changed operands, order and geometry compared with primary sources;
no unchanged complete vendor procedure was identified in the bounded review.

The explicit modern donor chain and these common algorithms leave mixed
ancestry unresolved. Retain the whole worker as unknown before a distinct
ownership decision. Do not grant fragment credit from a source diff or
classify the entire routine as vendor from its shared techniques. Historical
original source, assembler identity and exhaustive ancestry remain unproved.
This result does not revise any older accepted worker.

Independent native/origin review:
`.analysis/cheeto-put-independent-native-origin-review.json`, SHA-256
`826f1da15611bb809e6232f5aea025b96ecad392439ad7d73a771ec3fa91a7b8`.
It corroborates real near caller sites 12F9C/12FDC and the register/flag
protocol. Root boundary/model route review:
`.analysis/cheeto-put-routing-root-review.json`, SHA-256
`1cecfac5711e66c7d5401ae81a7b9bf4725ff80f66104cca83d04aa729e66a4f`.

All 182 native bytes remain unknown in the ownership inventory. Four NOPs
would receive zero authored credit under a future complete acceptance.
The ordinary Cheeto driver, loader, BB asset and external color/scroll
providers receive no acceptance or authored credit from this investigation.
Global authored denominator and percentage remain unreviewed.
