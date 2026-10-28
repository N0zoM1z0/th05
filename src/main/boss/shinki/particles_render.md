# Background particle renderer candidate

Original MAIN `[10CB2,10D51)` is159 bytes/60 instructions with no instruction
NOPs, table, padding or relocations. The standalone source uses the complete
canonical16-byte particle and64-record pool. Motion, signed age animation,
clipping, origin reset and age updates use ordinary C++ variables. Physical
register access is limited to the existing monochrome graphics API and VRAM.

The final single diagnostic producer emits171 bytes: an extra coordinate stack
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
