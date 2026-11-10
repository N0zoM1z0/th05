# Active-spark update candidate

The complete original MAIN update `[E086,E0D2)` is76 instruction bytes,
near cdecl, with no NOP, table or MZ relocation. It visits the64 real active
records at DS5AEA, using the unchanged canonical16-byte spark and12-byte
Motion declarations. This is separate from the96-record initialization bug.

`update.cpp` expresses free/removed state handling, actual motion update,
unsigned clipping, gravity and byte-age expiration in ordinary C++. The only
register reads consume the genuine DX:AX `PlayfieldPoint` return immediately,
before another call; no arithmetic is assigned to a physical register. X is
tested before the later Y expression may reuse AX. The real motion provider
is near Pascal at AE1:100A, returns the full point and removes its this word.
No layout, return type, helper implementation or failure handling is invented.

Semantic evidence is pinned ReC98 b6ba5b0a's `th04/main/sparks.asm`, its full
spark declarations, the original TH05 procedure and the independently accepted
TH05 [lifecycle](lifecycle.md). The ASM filename alone supplies no original
language classification. The accepted graphics worker and raster bank are
outside this candidate's ownership.

The first producer emits72 bytes, not76. It merges the two remove stores into
one common tail and copies returned Y to AX for its test. Those differences
are not padding. An ordinary Y local plus an early-continue loop emits84:
Y lives in CX, and the comma loop condition materializes a Boolean. Both
first diagnostic producers have wrong complete extents; neither is an
acceptance receipt or has a second producer or negative.
The initial72-byte source is restored exactly. Its diagnostic remains at
`.analysis/native-producers/main-sparks-update-a/`.

The initial nominal76-byte tail placed the72-byte diagnostic's foreign pool
at209C:5AEA. The maintained outside-only binder now uses the actual72-byte
end's paragraph E0D0 so DS returns to209D. This scaffold correction is not
recompiled or accepted; neither old linked result establishes whole-program
behavior. All source state remains foreign, with zero owned DATA or BSS.

The proposal is private, outside live exact manifests, and adds zero credit.
A future passing replay can mutate the genuine age threshold40-to41; that
control has not been compiled and is not claimed rejected. No behavior model
or unrelated tests were added. Accepted lifecycle/renderer inputs are unchanged.
