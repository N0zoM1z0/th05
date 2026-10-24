# Louise reflecting movement provider

Original MAIN **1D8BE..1D938**, **122 bytes / one complete function**, is the
movement provider used by the accepted Louise update. Native decoding covers
all122 bytes with39 instructions. Both Pascal RET4 paths are present, all six
local branches land on instruction starts, and the following byte begins the
accepted98-byte charge function. There is no table, zero or gap. Original
ordered relative MZ fixups are **[34]**, the genuine far vector call.

ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47` retains this algorithm as
`sub_18BB8` in `th05_main.asm`. The provider includes the frozen accepted
Louise update header and its full canonical24-byte Boss and geometry types.
Its actual interface is near Pascal: signed speed word atBP+6, signed duration
word atBP+4, RET4 and completion truth inAL. This was already verified from
both real callers and callee; no dummy interface or flags shim is introduced.
Accepted source/header files remain unchanged.

On frame1 the function obtains a real random angle byte and calls the genuine
C Pascal far `vector2` at **14AB:0008** to fill both signed velocity components
using that angle and the passed speed. The actual random producer is near
1527:002C, load1529C; Capstone's linear2529C display wraps within16-bit CS.
The local angle occupies the original one-byte stack object inside a two-byte
reservation. Its byte argument uses the ordinary large-model word stack slot;
the source passes a normal unsigned char and performs no manual stack access.
The foreign vector routine consumes its low byte and real far word references.

Each frame adds the actual velocity to current position, then reverses X speed
when X<=48 or X>=336 pixels and Y speed when Y<=48 or Y>=96. The inclusive
boundary comparisons and signed16-bit coordinates are retained. Multiplication
by-1 expresses the real component reflection in ordinary C++. Completion
returns true when phase_frame reaches the supplied signed duration, false
otherwise. The four accepted callers pass (speed,frames)=(16,96), (14,128),
(48,48) and (8,128) in subpixels, with no ABI adaptation.

Only the external Boss at DS5ABA is used: full24-byte layout, current point
at0/2, velocity at8/10 and signed phase-frame at16. There is no owned DATA/BSS.
The symbol-only context supplies real RNG/vector addresses, merges the actual
empty canonical foreign segments in their genuine frames, and leaves the
entire source contribution to the compiler. A separate paragraph context
begins1D940 after original complete end1D938, outside the function, to anchor
DS209D. No helper bodies, state values, inside-function holes or `.stack` are
present; every ORG is smaller than64KiB.

`.analysis/louise-flystep-boundary-review.json` pins original target/extent
hashes, complete branches/calls/returns and observed argument/layout evidence.
`.analysis/louise-flystep-candidate.json` proposes valid DOS8.3 module
`th05/louisef.cpp`, B4_UPDATE_TEXT/main_03 and a meaningful compiled negative
changing the right bounce boundary336→335. Native closure, classification and
unique-mutation checks pass. Preparation ran no compiler or Wine and uses no
ASM, pseudo-register template, inert barrier or source/flag variants. Actual
two-cold raw/ordered proof and negative rejection remain required for credit.


`main-louise-flystep-a/receipt.json` accepts all122 instruction bytes and the
original ordered relocation at relative34, with two independent fresh
producers and a rejected336→335 right-bound control. The actual Pascal
speed/duration interface and return in AL are retained; no table, padding,
DATA or BSS receive credit, and previously accepted headers remain unchanged.
