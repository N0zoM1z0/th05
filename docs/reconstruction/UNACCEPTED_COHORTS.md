# Retained natural candidates

These sources preserve useful reconstruction work and verified failure findings.
Source presence supplies no exact credit. Known failures are absent from the
default replay manifest; unchanged accepted owners need no cold replay.
Per-owner notes identify current diagnostics and source/ABI decisions.

| Candidate | Retained observation | Evidence |
| --- | --- | --- |
| General BB loader | Native 55; natural named-parameter C++ emits 56 with a BP frame and first allocator fixup 10 versus 7. Full far filename and segment return ABI preserved; no second/negative or credit. | [Loader](../../src/main/formats/bb_load.md) |
| Gather template copy | Original 27; ordinary assignment also emits 27 but calls F_SCOPY@ with far pointers. Link stops at the real unresolved provider; no accepted bytes. | [Copy](../../src/main/gather/copy.md) |
| OP score decoder | Original169; ordinary byte key181, register byte key182. The local-key spills across the byte-rotate primitive remain unresolved; ordinary181 source restored; TC4 rejects the proposed assembly-containing inline primitive. | [Decoder](../../src/shared/score/decode.md) |
| Near vector helper | Native 55 plus a separate unknown EVEN byte; wide-local C++ 106, word-domain candidate 92. No ASM promotion. | [Vector](../../src/shared/math/vector2_near.md) |
| Scroll coordinate helper | Native 40; ordinary integer candidate 47, inline-helper form 51. Source 47 restored; corrected empty SEGDEF binding verified by relinking its existing object. | [Coordinate](../../src/main/scroll/coordinates.md) |
| Shot collision pair | Original399+210; current compiled419+233. Repeated quotient evaluation still adds instructions; the selector context is now verified NOP/PUSH CS/CALL to the true far Pascal provider. Whole pair still fails. | [Current source/ABI notes](../../src/main/player/shot_runtime.md) |
| Standalone laser collision | Immutable quotient baseline218 versus210. Readonly inline clamp233, assigned inline parameter221 and register quotient221 all fail; baseline restored. | [Current notes](../../src/main/player/shot_runtime.md) |
| Item motion updater | Original241; safe typed-return producer248 remains. One long return-borrow experiment235 overwrote returned X during ordinary pickup arithmetic, making X subtraction self-subtraction. Safe source restored; no second/negative or register-forcing variants. | [Item ABI](../../src/main/item/update_abi.md) |
| Shot rendering | Original164, safe word-local producer173; the one byte-local experiment175 was stopped at the first boundary check and abandoned. The safe original source is restored. | [Shot rendering](../../src/main/player/shot_render.md) |
| Stage-session initialization | Original803 includes mandatory zero772, thirty table bytes and three uncredited relaxation NOPs213/403/595. New common SEGDEF restores transfer/fixup routing; late `-a2` still emits802 and is rejected. Correct potential credit799, not802. | [Stage session](../../src/main/runtime/stage_session_context.md) |
| Dialog opcode | Direct compiler455 against456; generated-ASM route matches456 raw bytes but reverses fixup order. | [Current notes](../../src/main/dialog/opcode.md) |

Notes distinguish semantic corrections from actual compilations.
Per-owner notes contain full layouts, actual interfaces and boundary reviews.
No successful interior fragment, normalized relocation order, physical-register
algorithm, copied instruction body, or inserted padding replaces a complete
natural owner. New investigations should use these observations rather than
repeat identical failed builds.

Superseded blockers are accepted: MAIN gameplay frame loop 445 with its true AX/DX word-mask dataflow, Mai/Yuki complete 273-byte B4 ball updater with native AX/DX hit-testing, generic Boss 43-byte AX/DX player collision after exact 414-byte defeat and 352-byte helpers, Yumeko complete 283-byte sword update as exact reviewed native ASM, Shinki ball update220 in true native C++ branch context, Alice foreground callback 140 in its true 521-byte two-function context, Staff bitmap 43+83, 991-byte controller and complete 626/861 updater/renderer, MAINE full registration menu 1034 and source-neighbor score codecs 86+100 (all original ordered fixups restored in authentic 4369-byte natural compiler context), Yumeko aimed354 and laser428 attack callbacks in their full natural compiler context (782 new authored bytes), OP ZUNsoft four-function CODE 1150 and independent filename DATA 54 (both with two producers and compiled negatives), Sara foreground159, Mai/Yuki foreground194,
Mima bomb control161 through the genuine [bomb family](../../src/main/player/bomb_family.md),
frameless MAP release23, and complete bullet/pellet rendering334 through the
documented speed option and ordinary register declarations. Their earlier
failures are superseded and do not need another replay.

The old shot-update blocker is superseded by the accepted complete408-byte
`main-shots-update-abi-b` owner, including its eight generated table bytes.
It keeps the full actual Motion return type and uses only its proven packed
return boundary; no source fields or method ABI were shortened.

Both complete stage-two background functions are now accepted independently:
initializer492 (`main-stage2-particle-initializer-a`) and updater653
(`main-stage2-update-abi-a`). Earlier498/476/664 observations are superseded
as open blockers. No whole-combined-TU equality is implied.

The item collection blocker is also superseded: the genuine [six-function
family](../../src/main/item/family.md) matches its whole 1,183-byte contribution
and original record order. New collector 620 and initializer 29 add 648 authored
bytes; the separate 241-byte motion updater remains unaccepted.
