# Natural staff-roll controller candidate

This independent C++ candidate owns the complete original MAINE function
`E422..E801`:991 instruction bytes,312 instructions and48 internal branches.
The actual final RET is atE800 and belongs to the function. There are no NOPs,
switch tables or internal padding. The zero atE801 is outside this owner;
the next actual far procedure begins atE802, relative to paragraph frameE80.
Original target decoding establishes these addresses independently; no global
`+5` rebasing rule is used.

The controller is a no-argument near cdecl void procedure in frame0A54. It
initializes the verdict display, snapshots the stage tally, loads external
staff images and fonts, runs the particle/orb/image/rain timeline, allows the
player to switch between two saved verdict views, fades out and frees resources.
ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47` `th05_maine.asm`
`staffroll_animate` is disassembly evidence for those ordinary scene operations;
it does not establish historical original C++ source or a historical TU.
The maintained TH04 staff controller corroborates the high-level resource and
palette APIs, while its distinct scene sequence is not imported as TH05 behavior.

The source uses ordinary loops, signed stage/measure results, an unsigned16-bit
bitmap offset, an integer slide state and standard Borland `outportb` calls.
The bitmap's upper bound is an unsigned comparison; only the lower subtraction
check interprets its wrapped word as signed, as the original does. The explicit
scene calls preserve image slots, coordinates, measure gates and each frame-pump
ordering. No physical-register algorithm, FLAGS facade, instruction macro,
barrier or compiler-option variant supplies this controller.

Existing unchanged headers provide full Palette8/RGB3, CDG16, Resident128,
Score8 and staff records. The accepted verdict family's real CODESEG is selected
only for its foreign declarations; no verdict function body is included. The
existing `staff_frame` atDS50E2 and `staff_bgm_measure` at50E0 are reused under
their canonical names. No second frame alias or field view is created. Other
direct state consists of the complete input word, palette tone/component and
verdict coordinates/colors. All fourteen resource-name arrays remain genuine
external mutable default-distance objects; no font, image or other asset bytes
are defined by this owner.

The two real external bitmap procedures remain near Pascal with one unsigned
word argument and RET2: snap atE3A4 and put atE3CF. Their43/83-byte device kernels
contain segment changes and REP copies; none of those instructions is converted
into a compiler-body ASM implementation here. The other providers retain their
existing real near or far Pascal/cdecl declarations and original addresses.
The controller owns zero initialized DATA and BSS.

The symbol-only binder supplies real providers beforeE422 and an empty owned
CODESEG. Its SHARED SEGDEF is genuinely word-aligned: a991-byte controller ends
atE801, and that real alignment supplies the outside zero beforeE802. SHARED
labels use their native paragraph-frame offsets minus two; physicalE802 plus
that local offset equals frameE80 plus the native offset. Its endpoint is the
real DS base10110. Actual TLINK SEGDEF framing, MAP positions and ordered MZ
results still require a producer: this arithmetic is not a tested linker claim.
There is no manual zero, instruction, artificial function, inside hole, rebase
or context adjustment to conceal a source-size failure.

The literal29-site original MZ stream has two descending runs, beginning
`705,340,...,39` and `985,971,966,950,938`. A standalone991-byte compiler owner
may emit a different record order even if every raw byte matches. This is an
independent known gate; neither sorting nor a byte-count prefix is proposed.
The intended next action is one isolated diagnostic of the actual natural
producer. Exact acceptance is not promised, and no compiler was invoked here.

The proposed unit is `maine-staff-controller`, module `th05/st_ctl.cpp`,
segment `STAFF_CONTROL_TEXT/group_01`, standard MAINE context. Its meaningful
own control changes `Palettes.colors[0].c.b = 48;` to47, within the true byte
component range. Private `.analysis/staff-controller-boundary-review.json`
and `.analysis/staff-controller-proposal.json` pin the original, ABI and frozen
source packet. No registration, acceptance or authored credit is added.

## Actual diagnostic results

Only one actual producer was run per revision; neither is an acceptance receipt
and no second or negative was compiled. Revision a was1001 bytes rather than
991. Native instruction correspondence isolated five added two-byte initial
jumps: four top-tested loops and the final fade loop. It also found an actual
input-gating mistake: Down/Up handling must remain inside the same idle-slide
gate as Shot/OK. Both original completion waits reuse an ordinary integer
scratch value across reset scene lifetimes.

Revision b restores the original first-iteration/control-state flow using
ordinary do-loops, the correct idle gate and genuine integer lifetime reuse,
without register hints, flags reads or layout changes. Its entire991-byte
compiler contribution matches the original raw bytes. The actual MAP confirms
the real word-aligned SHARED startE802/frameE80 and DATA10110/DS1011; the RET
atE800 is included and the outsideE801 alignment byte is not credited.

Ordered relocations still fail independently: standalone b emits all29 in one
descending run, while the original has two descending runs. The function stays
unaccepted and outside the default replay plan. No sorting, normalization or
artificial prefix is supplied. Any future context must contain genuine source
bodies and retain all original bytes/order and fresh-producer/control gates.
The a/b artifacts and source snapshots remain private under
`.analysis/native-producers/maine-staff-controller-a` and `-b`, with the precise
flow-recovery proof under `.analysis/staff-controller-a-forensic/`.
