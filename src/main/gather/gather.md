# TH05 gather-circle natural C++ candidate

The owner adapts pinned nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th04/main/gather.cpp/.hpp`,
specialized for GAME 5, with the maintained full `BulletTemplate` and motion
types. It preserves the real eight-slot update limit, complete gather/template
structures, shrinking radii, rotating rings, three-stack timing, ordinary and
special bullet emission, clipping and scrolled rendering.

The original `[16F70,171CB)` contribution has 603 instruction bytes. Two
27-byte functions are genuine ASM structure-copy helpers; they remain real
external declarations and symbol-only bindings, with no source implementation
or reconstructed-byte credit. The six complete natural C++ functions occupy
**549 bytes**, arranged as two real compiler contributions around those ASM
functions. Private `.analysis/gather-boundary-review.json` records the original
hashes, bounds, return sites, raw call operands and ordered fixups.

| Function | Original decoded span | Bytes | Candidate segment |
| --- | --- | ---: | --- |
| `gather_add_bullets()` | `16F8B..16FF5` | 106 | `GATHER_ADD_TEXT` |
| `gather_add_only()` | `16FF5..1705D` | 104 | `GATHER_ADD_TEXT` |
| `gather_add_only_3stack(int,unsigned int,unsigned int)` | `1705D..17087` | 42 | `GATHER_ADD_TEXT` |
| `gather_update()` | `170A2..17116` | 116 | `GATHER_RUN_TEXT` |
| `gather_point_on_playfield()` | `17116..17140` | 42 | `GATHER_RUN_TEXT` |
| `gather_render()` | `17140..171CB` | 139 | `GATHER_RUN_TEXT` |

Expected compiler-owned sizes are 252 and 297. Wrapper `th05/gather.cpp` uses
`wrapper_options = "-zPmain_03"`, MAIN binary M. Both segments share original
group frame `1527`; starts are frame offsets `1D1B` and `1E32`. A bounded
diagnostic must measure both actual OMF CODE sizes, not assume they fit these
expectations. A complete-contribution replay can register these two spans as
three functions each; alternatively the table lists complete function scopes.
No table or alignment byte lies in either candidate contribution. The only
ordered MZ fixup is the genuine `VECTOR2_AT` far call's segment word in
`gather_render`, function offset 84 (second contribution offset 242).

`probes/units/gather_bindings.asm` supplies the two real external ASM helper
labels at `1527:1D00` and `1527:1E17`, with their entire foreign intervals
outside the compiler-owned contributions. It supplies neither helper body nor
any target bytes. The second contribution's prefix covers the real second ASM
function, not padding inserted inside a natural function. Other helpers retain
their original near operands and the true `VECTOR2_AT` frame `14AB:03B0`.
`GATHER_ADD_SIZE` and `GATHER_RUN_SIZE` can be overridden only from actual OMF
sizes for a diagnostic; source output must never be padded to force a match.

The complete `gather_t` is 38 bytes and the template is 14; every physical
member is represented. All state is genuinely external: drawpoint DS `36FE`,
bullet template `577E`, gather circles `9BFA` and gather template `9EA6`.
This TU owns no initialized DATA or BSS. The binder anchors DS `209D` and has
no `.stack`. Array declarations retain the reference's public count; the
backing allocation's extra slots are not redefined or assigned credit here.

The canonical geometry header remains unchanged. Its original point methods'
screen/scrolled coordinate formulae are expressed as typed macros here; the
actual signed subpixel representation, clipping inequalities and scroll helper
remain intact. `_ES = A800` selects the real VRAM plane and `_AH` supplies the
real GRCG raw-helper color contract. `gather_point_render` retains its genuine
AX/DX fastcall and ES precondition. There is no handwritten ASM, emitted code,
fake symbol or instruction table.

A natural negative can change the unique `case 4:` to `case 6:`, shifting the
last of the three gather circles by two frames. This must be compiled from a
staged copy and rejected against the first contribution. This packet is static
source preparation, not source-current exactness or reconstruction acceptance.

## Accepted focused replay

`main-gather-b` passes both fresh producers for the two real contributions:
252 add bytes and 297 run bytes, six complete functions, no tables or padding.
The single original ordered far fixup also matches. The compiled case-four to
case-six negative delays the third gather circle and is rejected. Both genuine
27-byte ASM copy helpers stay external; their outside-contribution holes and
all runtime state receive no byte credit. The initial scaffold's oversized
single ORG was split into valid foreign segments before the successful replay;
no semantic source or function extent was padded to pass.
