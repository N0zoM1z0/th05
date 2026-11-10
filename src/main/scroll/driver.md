# TH05 scrolling driver: exact 115-byte source

This natural C++ owner covers original MAIN `C506..C579`, one complete
115-byte near-void function ending at its actual RET. Every original branch
lands on an instruction boundary in that function. There are no instruction
NOPs, padding, switch tables or owned DATA/BSS. The sole original ordered MZ
site is relative57, the segment word of `GRAPH_SCROLLUP` at `0000:1EE2`.
That genuine C far-Pascal API takes one unsigned word and returns with RETF2.
The final tile-ring update is a separate near-void provider at `C43A`.

The maintained TH04 `src/main/scroll/driver.cpp` supplies semantic provenance;
ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05_main.asm`
`sub_10214`, corroborates the independently decoded TH05 behavior. TH05 adds
its stage_id5 gate: clear the active byte and skip the hardware-origin call,
while preserving the ordinary accumulator and tile-ring calls. The remembered
page origins remain a genuine two-element signed-word array.

The existing complete `SubpixelLength8` and `Subpixel` classes are reused
unchanged. A byte addition first wraps the fractional accumulator modulo256;
when it reaches16, an ordinary int quotient gives a pixel advance0..15.
Subtract that advance from the signed0..399 scroll origin, wrap a negative
origin by400, publish the byte advance, retain the four-bit fraction and store
the signed-word subpixel distance. The tile-ring provider still runs on frames
with no pixel advance. Source expressions preserve these real widths and state
transitions; no storage alias or abbreviated record is introduced.

The donor's physical-register/FLAGS implementation is not copied. This owner
uses an ordinary local quotient and tests the actual stored signed subtraction
result. It contains no DOS pseudo-register arithmetic, flags reads, instruction
assembly, compiler barriers or option variants. Whether this natural dataflow
produces all115 original bytes is unproved until the focused producer runs; a
size or lowering mismatch does not justify a prologue or register rewrite.

The independent binder anchors the real main_01 frame `0AE1`, shared frame
`14AB` and DS `209D`, with all ORG extents outside the complete owned function.
Its state labels match canonical per-stage initialization and actual native
operands. It supplies no state bytes, helper instructions, internal gaps or
stack. Existing accepted headers and owners are unchanged. In particular the
already parked334-byte bullet renderer is a distinct function and is untouched.

The proposed unit is `main-scroll-driver`, module `th05/scr_drv.cpp`, segment
`SCROLL_DRIVER_TEXT/main_01`, standard MAIN large-model optimized context.
The owner negative changes the real wrap height from400 to399. Private
`.analysis/scroll-driver-boundary-review.json` and
`.analysis/scroll-driver-proposal.json` record the initial native scope and
proposal. That packet was source-only; the later failed producer is below.

## First producer: unaccepted123 bytes

`main-scroll-driver-a` stopped at its first size gate: the actual complete
compiler contribution is123 bytes, versus the original115. No second positive
or compiled negative ran. The failed producer tree, original natural source,
header and binder remain intact. No scope is accepted and authored credit is
zero. No further source, register, FLAGS or compiler-option variant is proposed.

The first65 bytes match the original exactly. The byte-accumulator expression
then uses a different same-width instruction sequence while preserving its
ordinary modulo256 update. The extra eight bytes come from reloading the
fraction before the quotient (three), copying that local quotient into another
compiler register (two), the one-byte-longer encoding used to publish its low
byte (one), and copying the quotient back for the final shift (two). Neither
the real frame prologue nor an argument/return ABI is the cause.

The compiler also selects arithmetic rather than logical right shift for the
promoted int quotient, and a normal signed comparison rather than the original
sign-only test after subtraction. These change encodings, not instruction
widths. The zero-extended byte input is0..255, so both shifts give the same
quotient0..15. In the valid scroll-origin0..399 domain, subtracting that quotient
cannot overflow a signed word, and both sign decisions agree. This bounded
semantic observation is not a claim about arbitrary corrupted out-of-range
state or exact reproduction of the original physical-register/FLAGS kernel.

Both actual callees and their argument protocols remain correct. The original
and candidate each have literal relocation order `[57]`, but that passing
subcheck does not overcome the size/raw failure. The additional CODE bytes also
move the following real paragraph-aligned shared frame from14AB to14AC and DS
from209D to209E; this is a layout consequence of the failed size gate. No
binding address or outside extent is adjusted to hide it.

Private `.analysis/scroll-driver-123-native-review.json` pins the actual MZ,
MAP, OMF and source snapshots, native instruction correspondence and the exact
eight-byte accounting. The maintained implementation stays ordinary typed C++.

## Accepted complete scroll driver — 2026-11-10

`scroll_driver()` now matches all **115/115 bytes** at `[C506,C579)`, with
the original far `GRAPH_SCROLLUP` relocation at `+57`. Two independent
Borland C++/TLINK builds also reject a compiled change to the genuine 400-line
wrap rule. Receipt:
`.analysis/unit-replays/gpt-web-main-scroll-driver-115-20261110/receipt.json`.

The 123-byte ordinary C++ candidate was eight bytes longer because the
fraction accumulator was reloaded and the signed scroll result was tested
through an additional memory read. The original TH05 CPU dataflow keeps the
byte fraction in AL, clears AH to obtain the 0–15-pixel advance in AX, and
subtracts AX from the real `scroll_line` word in place. One original-register
inline `SUB`/`JNS` pair uses the actual subtraction sign flag to apply the
400-line wrap only when needed. The subsequent low-byte advance, fractional
mask and shifted subpixel delta are built directly from AX. Those hardware
instructions preserve the source behavior without artificial CODE bytes or
post-link changes. The stage-5 scroll-disable, page origins, hardware scroll
and tile-ring callback remain unchanged.

This is natural C++ with a small inline register/flag primitive, not a pure
C++ codegen claim. The previous failed first-producer diagnostics above remain
historical; the complete 115-byte function is now independently accepted.

## 2026-11-11: accepted upstream 204-byte tile-row producer

The previously source-free `scroll_tile_ring_update()` callee at `C43A` is
now independently accepted as a full **204-byte C++/register** state machine.
The existing 115-byte scroll driver is unchanged and remains independently
accepted. Both adjacent functions now form the exact original 319-byte
`C43A..C579` code block. See [tile-ring source](ring_update.md) for the
full STD/map dataflow, real physical frames and focused two-producer receipt.
