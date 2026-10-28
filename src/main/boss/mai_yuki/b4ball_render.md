# B4 ball renderer

The complete MAIN function `[108DF,1093F)` is96 bytes/37 instructions with
near CS0AE1 and DS209D. Native review covers its final RET and every direct
branch. There are no instruction NOPs, tables, padding or relocation sites.

Maintained C++ iterates the63 actual balls after the template, animates four
cels, applies the8-cel damage offset and clears the real damage word only for
normal sprites. The canonical complete26-byte ball and64-record custom pool
remain unchanged. Near scalar scroll atDF28 and tiny32 graphics atBF62 retain
their actual Pascal cleanup and AX/DX/ES contract. Register access is confined
to that existing graphics boundary and VRAM selection; ordinary arithmetic,
conditions and traversal are compiler-generated C++.

`b4ball_render.hpp` repeats the existing tiny32 declaration and call macro,
without changing accepted headers. Combining the broad standalone B4 and bullet
headers initially failed on their pre-existing duplicate declarations; no object
from that frontend failure is accepted. The corrected independent producer
matched96 bytes, then a normal replay supplied two fresh deterministic producers
and its compiled damage-offset8-to9 control. The control changes only byte53.

Receipt `.analysis/unit-replays/main-b4ball-render-a/receipt.json`, SHA-256
`fad693879f203da0876abbb69094e62c7817d0b8bd9fde9e8bb38ab3fc0f6df5`.
Both actual OMF objects are valid with one complete96-byte LEDATA. MAP scopes,
source closures, actual argv, symbol-only binder, link response and complete
raw/ordered-fixup comparisons are checked. Normalized object identities, MAPs
and scaffold MZs are deterministic. The binder emits no initialized bytes.
Root review `.analysis/b4ball-render-root-review.json`, SHA-256
`d475d337ac316312d5c147d19cc8e9bdc7c5b590a49b7b09fe4072b5417eb6be`.

Import adds96 C++ instruction bytes and one complete function. The donor ASM
filename establishes neither handwritten origin nor acceptance. Literal
historical source, assets, whole-game linkage and packed-file equality are
outside this bounded acceptance.
