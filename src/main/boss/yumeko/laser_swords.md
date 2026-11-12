# Aimed-sword and laser/sword recovery: exact in real context

Two complete MAIN bodies now reproduce all original instruction bytes:
aimed swords `[1F088,1F1EA)`354 and laser/swords `[1F3F0,1F59C)`428.
Their109/132 native instructions, branches and final near returns are reviewed;
there are no instruction NOPs, tables or padding. **Both are now accepted in the complete adjacent source context**, not in
the earlier standalone objects: the original relocation order differs from
each isolated compiler result. Historical failures below remain useful.

| Scope | Original relocation offsets | Standalone compiler |
| --- | --- | --- |
| Aimed swords354 | 71,329,309,203 | 329,309,203,71 |
| Laser/swords428 | 232,72,402,382 | 402,382,232,72 |

The aimed body is canonical in `aimed_swords.inl`, included by its independent
wrapper. The superseded combined wrapper is retained in Git. The word-value aim
adapter removes the old three-byte Subpixel temporary. Native171CC reads X/Y
as words at BP+8/+6, angle as a byte at BP+4, and returns RET6. Both canonical
Subpixels are two bytes; their original declaration and full types are unchanged.
The function-pointer view forwards the same values to the same real symbol.
It introduces no helper implementation or physical-register arithmetic.

The new laser/sword body retains the full Laser24, Sword26, Boss24 and template
records. Its setup, paired aimed volleys, random laser origins, two random
swords and HP-triggered rank transition are semantic C++. The final rank vector
is40/48/52/48. An initial argument-order mistake and a declaration-order trial
remain failed diagnostics; only the corrected body has428-byte raw equality.
An initial link failure from an empty main_01 segment beyond64K was corrected
by placing that real empty segment at its actual group context.

Standalone raw matches: `.analysis/native-producers/main-yumeko-aimed-swords-a`
and `main-yumeko-laser-swords-d`. Each is one diagnostic producer, not an exact
receipt; no unnecessary second producer/control was run for known order failures.

A genuine original-order prefix of allocator121, updater280 and three-pattern
family435 emits LEDATA `[0,1021)`/`[1021,1190)` and restores the aimed function's
original relocation stream. However, the updater is three bytes short of283,
so aimed entry is1F085 instead of1F088 and relative calls differ. The first
prototype also keeps its definition in B5_UPDATE_TEXT; a later selector does
not move it to the requested segment. This context attempt failed its requested
scope gate and is preserved privately, with no imported scope or filler bytes.

The `-y` line-information trial also reproduces354 raw bytes but leaves the
standalone relocation order unchanged. The separate-segment trial likewise
does not restore the original stream.

The earlier gap is resolved for both attack callbacks by the full original-order
compiler context. The sword updater itself remains raw-inexact and unaccepted. Joint
review `.analysis/yumeko-later-root-review.json`, SHA-256
`1099a5063c7943fba749a258d3e449b1fdf1c75c916d329b5ef33cdbda94001c`.

## Accepted complete 354- and 428-byte Boss attack callbacks

Both callbacks now pass independently against the pinned MAIN executable:
`main-yumeko-aimed-swords-context` at `[1F088,1F1EA)` and
`main-yumeko-laser-swords-context` at `[1F3F0,1F59C)`. Each has two fresh,
raw-exact compiler/linker producers, its full original ordered MZ relocation
stream, the complete actual compiler OMF/MAP function-public boundary and a
rejected compiled HP-threshold negative. This adds **782 authored C++ CODE
bytes** and two complete functions, with no filler or target-byte copying.

The missing record phase came from the genuine adjacent code before the attacks.
`attacks_context.cpp` compiles the real 66-byte sword renderer in `main_01`
followed by `main_03`'s allocator121, scalar sword updater283,
three-pattern family435, aimed attack354, two spreads518 and laser attack428.
The full original source layout is 66+2139=2205 compiler bytes. The
supplier in `main_01` changes the compiler's natural OMF LEDATA/FIXUPP record
breaks in the later `main_03` contribution. This reproduces the **literal**
original 25-entry ordered fixup stream of that full main-03 group; no records
are sorted or edited. Both new whole functions match their original offsets,
including all near calls and DS operands.

The isolated candidate sword updater was 280 bytes; the genuine DX:AX
coordinate-return consumer with local `-O-` now emits the original **283-byte
size**, allowing correct downstream addresses and record grouping. Its own
raw bytes still differ, so its entire function remains unaccepted. The renderer,
allocator, three original patterns and two spreads were already accepted:
all six prior function bodies remain the same and receive **zero new credit**.
The only needed source changes to their standalone wrappers are conditional
guards around translation-unit-only `-zC/-zP` pragmas. The compiler still sees
one canonical function body per existing `.cpp` when included in the combined
context; no alternate implementation is copied to a new helper TU.

The meaningful C++ negatives are `600 -> 601` in `aimed_swords.inl` and
`500 -> 501` in `laser_swords.cpp`. Focused receipts:

- `.analysis/unit-replays/gpt-web-main-yumeko-aimed-context-20261110/receipt.json`
- `.analysis/unit-replays/gpt-web-main-yumeko-laser-context-20261110/receipt.json`

All four affected prior accepted wrappers—sword render66, sword add121,
patterns435, spreads518—have independent focused refreshed receipts under
`.analysis/unit-replays/gpt-web-main-yumeko-{swords-render,swords-add,patterns,spreads}-context-refresh-20261110/`.
No full accepted-set replay was performed.

## Accepted two large callbacks with real Yumeko compiler context — 2026-11-10

Reconstructed the actual adjacent source/record context, not a relocation
rewrite. The maintained `attacks_context.cpp` contains the real MAIN01
66-byte sword renderer and the MAIN03 121-byte sword allocator, 283-byte sword
updater, three movement/pattern routines (435 bytes), aimed sword attack (354
bytes), two spread attacks (518 bytes), and laser/sword attack (428 bytes) in
their original order. Each `*.cpp` remains the single canonical definition:
its standalone `-zC/-zP` pragma is suppressed only under
`TH05_YUMEKO_COMBINED_CONTEXT`. In the context, the ordinary compiler switch
is restored before the later patterns. This is a real contiguous multi-function
compiler object with 2139 MAIN03 bytes plus 66 MAIN01 bytes, rather than a
binder-supplied CODE prefix. All foreign compiler segments, near/far interfaces,
CS frames and ordered relocations come from the actual TCC/TLINK output.

The sword updater is a maintained ordinary C++ **283-byte context provider**
using its native DX:AX point-return words and the jump-optimization-off
profile. Its size and relocation agree with the original, but twirl-path
branches remain different; **none of those 283 bytes are accepted**. The other
five previously accepted neighboring functions (121, 66, 435 and 518-byte
units; seven functions total) were recompiled through their own standalone
sources and retained exactness. These are not new bytes.

In the full context the aim and laser-sword functions now match the original
**354/354** and **428/428** instruction bytes *and* literal relative MZ
relocation order. The standalone wrong streams were `[329,309,203,71]` and
`[402,382,232,72]`; original order `[71,329,309,203]` and
`[232,72,402,382]` is recovered naturally through OMF record boundaries.
Each callback underwent an **independent focused normal replay** with two
fresh deterministic producers, full MAP function boundary and complete
OMF/LEDATA checks, and its own compiled HP gate mutation (600→601 for aimed,
500→501 for laser/swords). Both semantic negatives were rejected. Results:

- `.analysis/unit-replays/gpt-web-main-yumeko-aimed-context-20261110/receipt.json`
- `.analysis/unit-replays/gpt-web-main-yumeko-laser-context-20261110/receipt.json`

The four affected accepted neighboring units also have independent focused
refresh receipts:
`gpt-web-main-yumeko-{swords-render,swords-add,patterns,spreads}-context-refresh-20261110`.
Total **new** authored C++ CODE credit is 782 bytes across two complete major
Boss attack functions; no prefix, false updater bytes, asset data, or global
executable completeness is counted. The full source context provides a useful
basis for finally restoring the sword updater's twirl branch lowering.

## Mixed laser/sword waveform and explicit per-rank speedup (2026-11-12)

The maintained **428-byte** original laser/sword attack now has a real,
source-visible `laser_swords_timing.hpp` protocol. The original 32-frame
charge starts its sound at frame 16 with 7/6 gather colors; the bullet
and laser shootout speeds remain 96 and 100 subpixels, with a 24-frame
laser age, 28-frame grow delay, 6-pixel laser width, and charging sword
rotation time 32. The 64-frame periodic pair fires every second frame:
two blue shots originate 64 pixels apart, initially offset 32 pixels
left and 16 pixels up. The same original pattern periodically adds a
random laser from the top row and two swords with bounded random X/Y
origins and a ±15 angular offset. No new projectile is created.

After the remaining HP before the next phase gate drops **strictly
below 500** and the original acceleration latch is still zero, the
source keeps the genuine explosion and 20-frame minimum bullet clear.
Laser frequency uses original easy/normal/hard/lunatic intervals
**34/28/20/20** and the paired-volley window uses **40/48/52/48**.
The distinct short preprocessor names avoid Borland's 31-character
significance collision found in the Shinki Devil pattern. The source
still uses the real existing scratch bytes at offsets 1, 12, 13, 14,
15; it adds neither fields nor game-asset bytes.

The two accepted callbacks share the *real nine-function* compiler
context. Changing `laser_swords.cpp` thus affects both the 428-byte
laser/sword owner and the preceding 354-byte aimed-swords owner, which
was separately recompiled rather than skipped. Their complete source
bytes, MAP/public boundaries, literal **original ordered relocations**
and separate compiled semantic negatives all pass in two independent
Borland/TLINK producers:

- `.analysis/unit-replays/gpt-web-yumeko-laser-swords-rules-a/receipt.json`
- `.analysis/unit-replays/gpt-web-yumeko-aimed-context-after-lasers-a/receipt.json`

The unaccepted *natural C++* source candidate for the intervening
283-byte `swords_update()` remains raw-inexact and earns no CODE credit.
The already accepted real ASM counterpart stays untouched; the new
source names do not introduce optimizer barriers or guessed opcode
sequences. No all-game cold replay was performed.
