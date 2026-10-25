# Complete bullet and pellet renderer candidate

The original renderer occupies `[13185,132D3)` in near `main_01`, frame `0AE1`,
with DS `209D`. Native review decodes all 334 bytes as 122 instructions,
validates the final RET and every direct branch, and explicitly enumerates
zero instruction NOPs. There is no switch table, alignment/relaxation padding,
initialized DATA or BSS. All raw bytes still require normal comparison. The
ordered MZ fixup stream is empty because every foreign consumer is a real near
call in this frame.

The full canonical 32-byte `bullet_t`, 400-entry pool, 180-entry near-pointer
cloud queue, flags and sprite-domain enums come from the unchanged accepted
`update.hpp`. The renderer starts at pool entry 399, draws 220 large bullets
backward, and leaves its genuine iterator at pellet entry 179. Active large
bullets use the actual tiny-16 API; cloud phases retain their signed clipping,
color-domain selection, four-frame cadence and tiny-32 sprite API.

Without zap or clearing, the real cloud queue uses a postdecrement condition;
its final zero test leaves the count at -1. Queued clouds precede the actual
top/bottom pellet renderers, with white and the real bottom color supplied to
the GRCG. During zap/clear, the remaining 180 actual pellets render backward
through the normal sprite path. No pool reset, synthetic data or substituted
consumer changes these paths.

The public provider keeps the maintained runtime's actual C near Pascal
`BULLETS_RENDER` identity. Scalar scroll conversion returns AX. The existing
tiny-16 wrapper and the authentic tiny-32 wrapper supply DX=top and AX=left;
the GRCG color API consumes AH. ES=`A800` is the actual VRAM entry requirement.
These genuine foreign interfaces do not force ordinary C++ register allocation.
The source contains no assembler, emits, target byte arrays, fake helpers or
partial structure stand-ins. Accepted providers and headers remain unchanged.

The original prologue uses PUSH BP, MOV BP/SP and a two-byte stack allocation.
This observed compiler-context fact is retained in the review. No flag,
prologue, padding or assembly workaround is proposed if the natural producer
differs. The independent binder places only real foreign symbols and holes
outside the complete function, including scalar scroll at `DF28` before this
owner. Its fixed tail is valid only after actual OMF confirms 334 bytes.

Private `.analysis/bullet-render-boundary-review.json` records the native
boundaries, NOP enumeration, calls, field widths, full pool identities, hashes
and ABI/layout evidence. `.analysis/bullet-render-unit-proposal.json` proposes
the complete owner and a meaningful cloud-blue base-cel negative, subtracting
two instead of one. `python3 .analysis/bullet-render-review.py` repeats the
bounded review. The source remains uncompiled and unaccepted pending two fresh
raw/ordered-fixup producers, OMF/MAP/dependency gates and a rejected own control.

The first focused producer, `main-bullets-render-a`, emitted 330 bytes instead
of the complete original 334, so the boundary gate stopped without a second
producer or negative. Native comparison found no semantic, type or control-flow
correction: the original six-byte manual BP/stack prologue became a four-byte
ENTER, and the compiler assigned the ordinary loop counter to DI and the
pattern number to the stack instead of the original opposite allocation. The
latter changes the instruction encodings by a further net two bytes. Original
and candidate both have zero NOPs and empty MZ fixup streams. The fixed outside
tail consequently displaced DS; that diagnostic offset adjustment was never
accepted as raw exactness. The full 334-byte function remains unaccepted and
is not cut into partial ranges. No flags, assembly prologue, source padding,
idle branches or physical-allocation variants are proposed.
