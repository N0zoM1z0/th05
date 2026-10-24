# Natural player region candidates

Semantic donors are maintained TH04 `src/main/player/invalidate.cpp`,
`move.cpp`, and `move.hpp`. Real TH05 bounds, fields, arguments, clipping and
input behavior are independently reviewed from the supplied original MAIN.
ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47` supplies additional layout and
algorithm evidence. Its `th05/player.asm` reconstruction reproduces the target
shapes, but does not by itself prove historical handwritten origin.

| Owner | Original complete range | Instruction bytes | CODE-data |
| --- | --- | ---: | ---: |
| `invalidate.cpp` | `C9BA..CA4B` | 145 | 0 |
| `move.cpp` | `CA4C..CAD2` | 94 | 40 |

The inter-function NOP at CA4B is excluded. Invalidation has one actual loader
fixup at unit offset60, targeting VECTOR2_AT's14AB frame. Movement has no loader
fixups. Its20-word table at CAAA occupies offset94 and every entry points to an
instruction boundary in the same original function. Whether a natural C++
switch emits that exact table is unproved. No credit, layout acceptance or raw
match is claimed by source preparation. Full279 bytes must pass the real oracle.

No shared or accepted player/geometry header is changed. The one canonical
PlayfieldMotion12 and SPPoint4 are reused. Invalidation passes complete drawpoint,
player previous point and option previous point through the already proved
legacy four-byte Pascal ABI view of the existing tiles_invalidate_around entry.
The TH04 donor's drawpoint_x/drawpoint_y field aliases are not introduced.
The real whole drawpoint is DS:36FE; the real option previous point is DS:36EA.

TH05 death radius is unsigned16. It subtracts112 with wrap, then halves
unsigned at the fifth of eight points. Signed TH04 integer division would change
wrapped values, so the real word type matters. Angle remains a byte with wrap.
The original stores angle/count together in AL/AH, but VECTOR2_AT reads its word
angle and clears BH before indexing trig data (original14E67/14E6A). Its upper
byte therefore carries no vector semantics. The natural source passes the real
angle value without manufacturing packed register state. Original clipping is
y[-128,6016) and x[-128,6272), with a48x48 dirty rectangle. Live invalidation uses
32x48, followed by the64x16 option rectangle.

Movement uses two independent signed word globals at DS:36DE and DS:36E2.
The original BSS has a separate unused word after each; neither global is
misdeclared as a padded structure or appended to player_pos. Negative values
retain their control-inversion meaning. A local player_input_t names the same
unsigned16-bit wire type without redefining the existing demo header's input_t.
MOVE_INVALID/VALID/NOINPUT are byte results0/1/2; the original caller at CC9D
checks AL at CCA0. It clears both velocity words before passing movement-masked
input. Cardinal cases deliberately leave the other axis unchanged.

TH05 ignores input bits12..15, while unsupported shot/bomb lower-byte bits still
cause invalid input. Dedicated diagonal keys and combined cardinal diagonals
have the same effects. A bounded native-analysis model compared the actual
normalization/table actions with the natural switch for all65,536 word inputs.
That establishes modeled semantic dispatch equivalence, not execution or compiler
exactness. No target-derived table is embedded in maintained source.

Code-generation uncertainty is material: original invalidation packs its counter
and angle into AX and only saves DI around its death path. Original movement
preloads speed registers and compresses high-byte directions into a20-entry
jump table. A standard natural loop/switch may not lower to these compact
sequences. This packet deliberately contains no pseudoregister mathematics,
packed-state surrogate, ASM body, emitted bytes or inert barrier to force it.
Keep mismatches unaccepted rather than treating the assembly reconstruction as
proof or trying flag variants. Initial `-k-` reflects the observed frame omission;
movement retains the maintained donor's ordinary `-a2` switch-data setting.

Aliases are `th05/p_inval.cpp` and `th05/p_move.cpp`, GAME5/BINARY M,
main_01. Source owns no initialized DATA or BSS. Private address-only binders,
full original boundary evidence and proposed entries are under
`.analysis/player-region-*`. Controls expand the live dirty width or reverse the
left-only movement case. All assembler labels have explicit matching CS context;
there are no helper bodies, field aliases, state values or artificial stack.

The first real cold producer rejects both candidates: invalidation176 versus
original145, movement174 versus134. Each failed complete extent is checked
before starting a second producer; actual sources/argv/OMF/MZ/MAP/logs remain
saved under `main-player-invalidate-a` and `main-player-move-a`, with no second
compile or negative claim. These source candidates receive zero exact credit.
No aliases, register-packing templates or compiler flag variants were added.
