# Staff scene renderer candidate

The complete original MAINE procedure atDFF1..E34E is861 bytes/335 instructions
with no NOPs, compiler tables or padding. It clears the window, draws48 stars,
eight orb trails, the main orb and64 particles, then draws an eight-pixel frame.
The source references the unchanged complete20-byte particle/65-object pool,
real4-byte points and canonical window state. Its wide centers retain32-bit
signed arithmetic; trail centers retain signed16-bit storage and their actual
sentinel. Master graphics use genuine C far Pascal APIs, and standard
`outportb(0x7C,0)` calls disable the real hardware controller. No assets, DATA,
BSS, assembly body, register aliases or false helper prototypes are introduced.

Original ordered fixups are
`[781,708,645,577,555,407,382,365,258,245,165,91,28,849]`. The nonmonotonic final
entry requires an evidenced real compiler context. The coherent staff family
is a future candidate context, not proof of the historical original TU.

To avoid unnecessary builds for the known standalone order failure, only one
actual producer was run using the existing `cold_round` staging and pinned
toolchain under `.analysis/native-producers/maine-staff-render-a`. It is a native
shape diagnostic, never an acceptance receipt; no second or negative was run.
It produced858 bytes/334 instructions. The sole missing instruction is an
original redundant near-pointer reload immediately after the trail sentinel
comparison. Both type layouts, pointers, signed arithmetic and genuine APIs
are consistent; there is no demonstrated type/ABI correction to apply.
A same-size loop-color/index initialization order also differs.

The source remains ordinary C++ and unaccepted. No reload, volatile field,
barrier, fake prefix or register template is added to force the missing bytes.
The native full-boundary review is `.analysis/staff-render-native/root-review.json`;
independent forensic detail is `workflow-review.json` in that private directory.
The private source/control proposal is `unit-proposal.json`; the meaningful
uncompiled negative would change the first trail color from6 to5.
