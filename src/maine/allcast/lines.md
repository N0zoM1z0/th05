This is an accepted bounded C++ reconstruction for TH05 MAINE
`screen_line_next_animate`, the complete original `[0xB1B5, 0xB273)` function.
The original has 190 instruction bytes, 67 instructions, four local branches,
and no NOPs, compiler tables, or padding. Its literal ordered MZ relocation
sites are `[145, 128, 95, 78]`. No accepted unit overlaps this range.

The original selects a full far string pointer, centers its line within the
current screen, draws four decreasing dissolve masks on both pages, and then
draws bold text on both pages. It advances the total and screen-local line
indices and returns a byte Boolean in AL. The four source calls to
`graph_putsa_fx` use the actual far Pascal five-word interface. The four calls
to the accepted near `wait_flip_and_check_measure_target` ignore its byte
result. The four-byte local is a genuine far pointer, and the FX state retains
the complete canonical word enum from `verdict/main.hpp`.

Pinned ReC98 revision `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th05/end/allcast.cpp`, provides the surrounding state and caller semantics
but only forward-declares this helper. The original target and
`th05_maine.asm` provide native algorithm/ABI evidence. This source is an
ordinary semantic reconstruction, without an instruction transcription or
physical-register algorithm. The historical original source expression and
translation-unit boundary remain unknown.

The 47 far string-pointer slots at DS:0820 and their text are foreign. The
seven genuine screen counts start at DS:08DC and contain `1, 2, 6, 10, 9, 12,
7`. The old assembly label `LINES_PER_SCREEN` at DS:08DA overlaps the final
far pointer's segment word. It does not establish a separate dummy-count
object. This candidate declares the seven actual counts and indexes them by
`loaded_screen_id - 1`; the accepted caller supplies screen IDs 1 through 7.
The first actual producer successfully folds the natural zero-based index
into the original address expression. No overlapping C array, invented data,
or compensating context is supplied.

The binder supplies only real outside addresses. The wait helper's raw name
`@wait_flip_and_check_measure_targ$qv` is verified from its accepted OMF
PUBDEF. The proposed negative changes the real line position from 64 to 65.
The accepted `allcast.cpp` and `allcast.hpp` are unchanged.

The first focused producer, `maine-allcast-line-a`, emitted193 bytes and
stopped at the size gate before a second producer or compiled negative.
The full word enum, genuine seven-count index, far-pointer local, graphics
protocol, near wait calls, and AL Boolean return were correct. An enum-cast
assignment loaded, decremented and stored the FX selector, taking seven bytes
instead of the original four-byte word-memory decrement. Its three extra
bytes also changed subsequent foreign layout; those addresses were not rebound.
The actual193-byte evidence remains in
`.analysis/allcast-line-193-native-review.json`.

The single source correction uses the direct high-level expression
`graph_putsa_fx_func--`, retaining the full canonical enum and all ABI and
compiler settings. Pinned Turbo C++4.02 supports this historical expression
and issues its normal integer-to-enum warning; the warning is retained, not
suppressed. The actual transitions7 through3 are all named enum values.
No modern ISO portability or historical original expression is claimed.

The corrected `maine-allcast-line-b` focused replay passed both independent
fresh producers: all190 bytes, full OMF/MAP checks and the literal ordered
fixups match. The own compiled negative moves the line position64 to65 and
fails comparison. Its receipt at
`.analysis/unit-replays/maine-allcast-line-b/receipt.json` credits190 authored
instruction bytes and one complete function. No overlapping count array,
register hint, flags trick, output patch or ABI adaptation is used.
