# Image kernel assembly ownership

Five complete native CODE contributions are reconstructed from maintained semantic
assembly. Explicit adoption is separate from exact replay, C/C++ acceptance,
assets, packed-file equality and the still-unreviewed global denominator.

| Owner | Complete load-image range | Actual CS | Compared | Instruction credit |
| --- | --- | --- | ---: | ---: |
| MAIN pellet top/bottom | C322..C41E | 0AE1 | 252 | 249 |
| MAIN CDG alpha | 14D68..14DFC | 14AB | 148 | 146 |
| OP CDG alpha | D758..D7EC | 0D30 | 148 | 146 |
| OP background rectangle | DB3C..DBBE | 0D30 | 130 | 123 |
| MAINE background rectangle | ECE4..ED66 | 0E80 | 130 | 123 |

These are the actual linked copies. MAINE has no corresponding CDG contribution,
and MAIN has no rectangle contribution. Candidate calibration addresses do not
transfer: MAIN CDG starts at CS:02B8, and MAINE rectangle at CS:04E4.
All five original ordered MZ relocation streams inside these scopes are empty.
Real relocated far calls establish the shared kernels' segment frames; pellet
near calls and both complete procedure boundaries establish their MAIN context.

## Native origin and source review

Independent native review supports genuine original assembly: the pellet pair
uses direct string/VRAM operations with a hidden ES/GRCG contract and transforms
its complete queue union in place; CDG repurposes BP after argument access and
uses a segment-sentinel plane loop; rectangle writes its own CS operand fields.
These complete owners are distinct from the compiler-generated `bullets_render`
caller, whose existing mismatch remains unaccepted.

Candidate algorithms are pinned ReC98 b6ba5b0a, specifically
`th04/main/bullet/pellet_r.asm`, `th04/formats/cdg_put.asm` and
`th04/hardware/bgimager.asm`, selected in their GAME5 contexts. Their local
history explicitly describes reverse engineering or undecompilable routines;
they are semantic references, not recovered historical sources. Their acceptance
does not transfer. The maintained sources retain symbolic loops, typed layouts,
hardware constants and self-modification, without opcode arrays, target-derived
instruction listings, local numeric CODE addresses or sprite/image payloads.

A bounded vendor check rehashed both pinned master0.23 archives, validated all
653 extracted members and searched every member plus all 240 files under the
reference `libs/master.lib` for renderer identifiers, game globals/types and
distinctive local aliases. No matches were found. This search does not exclude
all historical vendor derivations; shared hardware macros alone prove neither
authorship nor vendor origin. Historical source text and original assembler
identity remain unknown.

## Preserved contracts

The pellet pair consists of complete near procedures at relative 0 and 146.
Both preserve BP/SI/DI and segment registers. Callers supply ES, active GRCG,
the intended colors and clear DF; working registers and flags are clobbered.
The full four-byte queue union overlays signed left/top with word VRAM/sprite
offsets, as in the unchanged canonical `src/main/bullet/update.hpp`. The top
pass transforms it for the bottom pass. The bottom pass deliberately reads its
first word with `MOV AX,[SI]`, without advancing SI; subsequent `LODSW` repeats
the first source row, consuming four rows across five writes. Keep this behavior.
The foreign sprite addresses 209D:0E4A and 209D:0ECA bind external resources;
no asset bytes or DATA ownership are supplied.

CDG is far Pascal `(left, top, slot)`, returning with RETF 6. The complete
16-byte record has five initial words, bytes at 10/11 and segment words at
12/14; its 64-slot pool is not narrowed. Canonical C++ records in the unchanged
MAIN EMS and MAINE staff headers are pinned semantic inputs. Slots reside at
MAIN 209D:306C and OP 0EFE:3A96. BP/SI/DI/DS are preserved, while EAX/BX/CX/DX
and flags are working state. Unconditional CLI/STI returns with interrupts
enabled; CLD clears DF. The sentinel pop leaves ES=0, and GRCG is disabled.
No incoming IF/DF/ES restoration is invented. GAME5 has no CS patch fields.

Rectangle is far Pascal `(left, top, width, height)`, returning with RETF 8.
The full eight-byte foreign cache contains four 16-bit B/R/G/E segment handles,
at OP 0EFE:09E4 and MAINE 1011:06C2, matching unchanged
`src/shared/hardware/bgimage_free.hpp`. It preserves BP/SI/DI/DS, clears DF,
leaves interrupt state untouched and leaves ES at the final E plane. Width
rounding, self-modified VRAM offset/word width and GAME5's JNZ height loop are
preserved; no clipping or zero-dimension guard is added.

## Complete comparison and exclusions

Every instruction NOP is enumerated below. No hardware NOP in these scopes
receives authored instruction credit:

| Owner | Relative checked alignment offsets | Other checked zero-credit ranges |
| --- | --- | --- |
| Pellet pair | 87, 145, 175 | None |
| Each CDG | 113, 147 | None |
| Each rectangle | 129 | Jump [55,57); patched fields [102,104), [107,109) |

The rectangle jump targets its following instruction. A prefetch-flush purpose
after the CS writes remains possible and unproved; preserve it and conservatively
grant zero credit. Its category does not assert that removing it is safe. All
NOPs, jumps and dummy 1234h operand bytes participate in the full raw comparison.
Totals are 808 compared, 787 instruction credit, nine alignment bytes, four
jump bytes and eight runtime-placeholder bytes; no tables or DATA are owned.

`replay_asm_family.py` requires two fresh deterministic TASM producers per owner,
one complete ordinary CODE SEGDEF and complete LEDATA coverage, actual MAP
segment/group/CS/DGROUP frames, public/patch offsets, unmodified raw bytes and
literal ordered fixups. Symbol-only binders contain no initialized payload.
MAIN reserves use real segment divisions with every ORG below 64 KiB; OP's CDG
reserve ends at its complete foreign slot pool, and MAINE's reserve uses the
independently accepted foreign all-cast DATA bound. No artificial stack is added.

Each owner has its own assembled semantic negative: pellet top height 6 to 7,
CDG GRCG mode C0h to C1h, or rectangle plane count 4 to 3. All are rejected with
the same complete scope and ordered relocation stream. The unchanged installed
toolchain execution proof and unrelated accepted producer evidence are reused.

Private native proofs and receipts are retained under
`.analysis/render-kernels-native/`: `main-pellet-render-b`, `main-cdg-alpha-a`,
`op-cdg-alpha-a`, `op-bgimage-rect-a` and `maine-bgimage-rect-a` each contain
`receipt.json`. The first pellet binder attempt (`main-pellet-render-a`) stopped
on a location-counter overflow before assembly of the source; dividing its
foreign reserves at the actual segment frames fixed the setup. It grants no
evidence or credit. Native proofs are pinned per descriptor in
`config/asm_families.toml`; adoption pins each accepted record and these notes in
`config/reviewed_asm_families.json`.

Independent read-only review reports are retained as
`.analysis/image-kernels-origin-review.json` (SHA-256
`e6d2588d0fc28aaae3b3d92861b523f844d94abc4e36ce763799552d9d65d9dc`) and
`.analysis/pellet-render-native-review.json` (SHA-256
`679a0f2993806ba34fd6c5a923c0e36413712ad8d6eaeba2bb94f089a21f15f0`).
