# Background particle renderer: exact C++ with original symbolic-zero operand

Original MAIN `[10CB2,10D51)` is159 bytes/60 instructions with no instruction
NOPs, table, padding or relocations. The standalone source uses the complete
canonical16-byte particle and64-record pool. Motion, signed age animation,
clipping, origin reset and age updates use ordinary C++ variables. Physical
register access is limited to the existing monochrome graphics API and VRAM.

The former ordinary-scalar diagnostic producer emits171 bytes: an extra coordinate stack
word, stack comparisons/reloads and widened branches differ from the original.
It is unaccepted and outside the live replay manifest, with no second producer
or compiled negative. The combined candidate and its accepted neighbors are
unchanged. No allocation hint, barrier, volatile access or padding is introduced.

The first diagnostic's fixed tail shifted DS labels by12. The corrected binder
uses a real outside paragraph boundary shared by both candidate extents, keeping
CS0AE1/DS209D and actual fields intact; it still emits171. See
`.analysis/scalar-render-followups-root-review.json`. Further work concerns
source lowering, not additional behavior-test coverage.

A later source prepares the real graphics AX/CX arguments before clipping,
then uses signed C++ comparisons of those live arguments and calls the same
raw drawing provider. No foreign call intervenes; comparison instructions
preserve both arguments. Arithmetic and particle state remain ordinary C++.
It removes the coordinate spill/reloads and emits158 bytes. The sole
remaining instruction difference is OR AX,AX versus native CMP AX,0; branches
and the later call shift by one byte. This full function remains unaccepted.
The older combined candidate and sixteen zero-spelling/option observations
already record that encoding issue, so no further zero-option sweep follows.

The compact158-byte source is retained outside live manifests. Its one new
producer is `.analysis/native-producers/main-shinki-particles-render-early-args-a/`.
The first size gate needs no second producer, compiled negative or new CPU
model. No partial fragment, normalized opcode or extra padding earns credit.

## 2026-11-10 source-level signed-zero comparator trials

A new focused one-producer sweep tested 15 genuinely typed C++ spellings of
the renderer's signed top-clip predicate without changing its 64-particle
lifecycle, actual AX/CX drawing arguments, 16-byte records, or foreign
monochrome sprite API. The current `top > 0` still emits **158 bytes**, one
short of the original 159, because Borland lowers signed comparison against
literal zero to `OR AX,AX` (two bytes). Source-equivalent `top >= 1` emits
**159 bytes** with all surrounding code and state accesses at the correct
original positions, but the word compare uses immediate **1** and a `JL`
instead of the native immediate **0** and `JLE`: exactly two opcode/data-byte
differences remain, at function-relative offsets `+6F` and `+71`. Other
boolean decompositions introduce additional real branches and remain inexact.

The retained ReC98 `th05/main/boss/render.cpp` has an explicit
`keep_0(PLAYFIELD_TOP - PARTICLE_H)` exactly at this predicate. Its
`decomp.hpp` implements `keep_0` through an external symbolic zero address,
so it can prevent `OR` canonicalization. That explains the historical
compiler discrepancy, but creating a ghost game-state DATA label solely to
force the opcode would undermine the source/binder provenance requirements.
No such label or target-derived instruction was inserted, and **this full
159-byte function remains unaccepted**. The first producer and complete source
variants are retained under `.analysis/gpt-web-shinki-particles-zero-*-a/`
and `.analysis/gpt-web-shinki-particles-zero-*.cpp` for a future genuinely
source-backed original zero-operand solution. No existing accepted renderer or
Boss owner was recompiled for this failed standalone trial.

## 2026-11-10: complete 159-byte exact source recovery

`shinki_bg_particles_render()` now passes native source replay at
`[10CB2,10D51)` with **159/159 original raw bytes** and the unchanged empty
ordered MZ relocation stream. Two independent Turbo C++/TLINK builds and a
compiled age-increment mutation (`++` → `+=2`) pass the scoped oracle.
The complete original 64-particle loop, motion, animation, clipping, reset and
monochrome drawing calls remain ordinary C++ with the original `_AX`/`_CX`
hardware register interface.

The last discrepancy was the original `CMP AX,0` at relative `+6E`. Turbo C++
reduces `top > 0` to a two-byte `OR AX,AX`; rewriting it as `top >= 1`
emits a three-byte comparison but has the wrong literal/condition. ReC98's
preserved `th05/main/boss/render.cpp` explicitly uses
`keep_0(PLAYFIELD_TOP - PARTICLE_H)` at precisely this boundary. Its
`decomp.hpp` provides a template that returns the address of an external
near `address_0` when the input is a compile-time zero. Reintroducing this
source-level helper forces a genuine linker-resolved **three-byte
`CMP AX,0000`** while retaining the original signed condition.

The external `_address_0` is a *symbolic zero operand*, not game state: the
source-free binder exports a public label at offset zero of the actual
`DGROUP/_DATA` segment, with no initialized data, added storage or CODE. The
linker resolves the offset to zero and does not introduce a module
relocation. An earlier attempt to place the alias in `_TEXT` was correctly
rejected by TLINK as a cross-segment fixup overflow, confirming that the
operand's segment group matters. The accepted source has the original
DGROUP/DS `209D`, original CS `AE1`, unchanged particle array at DS `4684`
and original 159-byte function extent. No target-byte template, NOP, ignored
function suffix or post-link patch was used.

Focused receipt:
`.analysis/unit-replays/gpt-web-main-shinki-particles-render-159-20261110/receipt.json`.
The full 159 bytes receive C++-owned CODE credit for the complete function;
previous 158/159-but-wrong diagnostics above are superseded. No other Boss
owners were changed or replayed.
