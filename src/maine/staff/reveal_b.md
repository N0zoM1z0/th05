# Staff image phase B candidate

The pinned original MAINE decoded image contains one complete function at
`DE79..DFF1`,376 bytes, frame`0A54:3939`. All141 instructions decode through
near `RET8`; there are no NOPs, compiler tables, padding or accepted overlap.
The actual entry differs from the reference's `sub_DE74` label. Addresses and
operands here come directly from `load_unit_target()`, not a blanket adjustment
of reference labels or a synthetic MZ header.

The real interface is near Pascal
`int staff_image_update_b(int center_x,int center_y,int slot,int measure)`.
Arguments occupy four word slots and the return is ordinary AX0/1. Original
callers E5C5 and E61A pass `(528,240,1,76)` and `(464,224,4,120)` respectively;
both test AX as a word after the call. This is not a bool or carry-flag facade.

The frozen shared `image_phase.hpp` supplies the complete canonical CDG16 class,
identical fields and methods to the accepted MAIN EMS class, plus the genuine
foreign interfaces. `cdg_slots` is the real64-slot pool at DS29FE with16-byte
stride. The function reads signed width at+2 and height at+4, converts centered
coordinates by signed division by2, and retains inclusive16-pixel cover loops.
Its text X calculation uses signed divisions by8, clips only the original upper
bound80, and converts Y by signed division by16. No added clipping or altered
negative-coordinate behavior is introduced.

| Real state | DS offset | Complete type/role |
| --- | --- | --- |
| staff_text_clear_requested | 1746 | Shared unsigned byte |
| staff_image_phase_b | 174A | Signed word phase |
| staff_image_cover_b | 174F | Mutable default-distance char[3], two spaces plus NUL |
| staff_image_wipe_extent_b | 50C8 | Signed word extent |
| staff_image_wipe_frame_b | 50CA | Signed word frame counter |
| staff_bgm_measure | 50E0 | Shared signed word music measure |

B's state remains distinct from A's1748/50C4/50C6 objects. The existing staff
frame is50E2 and is not aliased as a new elapsed-frame global. This candidate
owns no initialized DATA, BSS, strings, images or font assets.

Phases0/1 render the bitmap and cover rectangle, initializing extent to
`width/16+7`. Phases2/3 decrease that extent every fourth call and use the real
wipe helper's low-edge result1. Phase4 waits for the requested music measure
except sentinel3996, increases extent every fourth call, and observes result2
at the high edge. The final phase performs the original extent128/direction-1
wipe, resets phase, requests text clearing and returns1; other paths return0.

The foreign helper at DBE6 is near Pascal with six word arguments, RET12 and
three genuine AL results0/1/2. Native bounds confirm extent<0 returns1 and an
extent above width/16+7 returns2; neither is inferred from flags. Its hardware
implementation remains foreign. The other calls are actual far Pascal
`CDG_PUT_NOALPHA_8` at E80:0274 and `TEXT_PUTSA` at0000:22AA. Source uses normal
fields, locals, arithmetic and calls, with no inline ASM, physical register
alias, opcode template, optimizer variant or fabricated API.

The original ordered MZ fixups are `[85,160]`, ascending. A normal standalone
single CODE LEDATA can instead emit these in reverse order even if its raw
bytes match. This is an explicit unresolved producer-context risk: every raw
byte and the original order must pass before acceptance. The binder's foreign
A/wipe extents only establish real link addresses; they do not supply compiler
source context. Any later complete staff-family trial must contain its genuine
functional bodies, not numerical filler chosen for record phase. No standalone
exactness or historical original-TU identity is asserted here.

The independent symbol-only binder places the true empty foreign segments in
A54's group, the full foreign A extent before B, SHARED at E80, and DS at1011.
All ORGs lie outside B's complete compiler contribution; it supplies no game
instructions, owned labels, internal padding, target bytes or `.stack`.
The proposed module `th05/stimgb.cpp` is DOS8.3. One meaningful staged negative
changes the initial extent margin from7 to8 text cells. It has a unique source
match and does not mutate A's source/header or any accepted input.

Private complete instructions, caller/branch review, target proof, ABI and
ordered-fixup evidence are in `.analysis/maine-staff-reveal-b-native-review.json`.
The functional freeze is `.analysis/maine-staff-reveal-b-freeze.json`, and the
unadopted entry/control proposal is `.analysis/maine-staff-reveal-b.proposal.toml`.
Preparation performed no compilation or config/ledger change. This remains a
natural source candidate until actual independent producers and negative pass.

## Single-producer diagnostic

One actual cold producer under `.analysis/native-producers/maine-staff-image-b-a`
produced the complete376-byte contribution. It differs at13 prefix bytes because
the source initialized the image pointer before copying the top coordinate.
The original and independently accepted twin A capture top first. The maintained
B source now restores that canonical initializer order; this revision has not
yet been compiled. No physical-register hints, API changes or filler were added.

The actual standalone ordered stream is `[160,85]`, while original B requires
`[85,160]`. No second or negative producer was run for this known failing
standalone context. The diagnostic is not an acceptance receipt and is not
relabelled exact. A genuine complete-family context is prepared privately for
subsequent validation; no numerical prefix or fixup normalization is supplied.
