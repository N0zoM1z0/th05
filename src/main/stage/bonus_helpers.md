# Stage-bonus multiplier helpers

The complete adjacent owner is `[1C669,1C79A)` (305 bytes), in `main_03` frame
`1527`, DS `209D`. The first helper is 89 instruction bytes; the modifier helper
has 208 instruction bytes followed by its actual eight-byte compiler rank
table. Native review checks 98 instructions, both returns, every direct branch
and all four table destinations. There are zero instruction NOPs and zero
alignment bytes. The complete original ordered MZ stream is `[82]`.

The pure maintained TH04 `src/main/stage/bonus.cpp` supplies the natural
algorithm, independently checked against the original TH05 operands and ABI.
The first helper accepts a real far pointer to an unsigned 32-bit score,
multiplies it by a signed word factor, divides by ten, and prints its description
in red below factor ten or green otherwise. Each adjustment rounds through the
actual unsigned division. Its Pascal arguments are row, description, factor
and the four-byte far pointer, with RET10.

The second helper returns through RET4. Without the actual Boss defeat-bonus
flag, it zeroes the bonus and prints description zero. Starting credits of
six/five/four lives apply factors three/five/seven; one/two/three continues
apply eight/six/four. Difficulty applies five/ten/twelve/fourteen for
Easy/Normal/Hard/Lunatic. The source preserves real display rows and ordering.

The full canonical Boss24 and resident128 remain unchanged. TH05's eleven
description entries are real two-byte near string pointers, independently
verified by index scale two and the implicit DS word at the far text call.
This differs from the TH04 donor's far-pointer declaration. The table and
strings remain foreign; no pointer values, Japanese text, images or opaque
bytes are copied into maintained source. No initialized DATA or BSS is defined.

The four rank table words lie at `1C792..1C79A` and point to actual instruction
starts inside the modifier helper. They are semantic compiler CODE data, not
padding or assets. The next real stage-clear function starts at `1C79A`; the
table cannot be dropped from this owner. All 305 bytes must compare normally.
No extra alignment option, fake prefix, ASM, emit, CF convention, register
hint, point temporary or compensating padding is used.

The symbol-only binder preserves real `TEXT_PUTSA` at `0000:2598`, main03 frame
`1527`, the authentic DS variables and holes only outside the entire compiled
contribution. Actual OMF must confirm the complete extent before the fixed
tail is valid. The source's combine guard permits its real unchanged bodies
to supply genuine context for a later full bonus owner, without modifying an
accepted helper source after this packet freezes.

Private `.analysis/stage-bonus-helpers-boundary-review.json` records hashes,
native bounds, NOPs, calls, field widths, table targets and ABI evidence.
`.analysis/stage-bonus-helpers-unit-proposal.json` proposes the whole pair with
a meaningful divisor ten-to-nine negative.
`python3 .analysis/stage-bonus-helpers-review.py` repeats the bounded native
checks. The focused `main-stage-bonus-helpers-a` replay passed two fresh
305-byte producers, complete raw and original-order comparisons, actual
OMF/MAP/dependency gates and its own compiled divisor ten-to-nine control.
All 297 instruction and eight generated table bytes are accepted.
