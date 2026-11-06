# Background particle renderer candidate

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
CS0AE1/DS209D and actual fields intact; it still emits171. Evidence:
`.analysis/native-producers/main-shinki-particles-render-b` and
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
