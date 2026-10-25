# TH05 normal and Extra ending dispatch

Original MAIN contains two contiguous complete no-argument far C++ routines:
`end_game()` atD71E..D756 (56 bytes) and `end_extra()` atD756..D77C (38 bytes).
Both return with RETF. The complete94-byte contribution has35 instructions,
no tables and ordered MZ fixups `[81,74,43,36]`. No accepted extent overlaps it.

Natural semantic provenance is maintained TH04 `src/main/end/ending.cpp`.
TH05 combines normal good/bad selection: a nonzero existing `continues_used`
byte at DS3702 selectsBAD FE, otherwiseGOOD FF. Extra selectsFD. The complete
five-value ending-sequence enum is retained, together with the actual full
128-byte `resident_t` and its end_sequence byte at+1A. TH04's separate
end_type_ascii assignment is absent from the original TH05 and is not added.

Both functions fade the real sound driver with word0204, fade the palette at
speed16 and call the existing far Pascal `GameExecl(const char far*)` returning
int. This exactly matches the accepted handoff provider's C++ linkage and
full parameter/return types. The original callee atCEC2 is earlier in the same
AE1 code frame; the genuine `samecodeseg` annotation retains its far signature.
Sound and palette providers retain true far Pascal ABIs at14AB:04AC and0:0644.
Two distinct foreign DGROUP filename objects at143E/1444 each contain the real
six-byte `maine` filename, rather than being collapsed to another occurrence.

The original native calls to GameExecl include90/0E/E8 relaxation sequences.
Their NOPs are whole-contribution offsets49 and87 (second-function offset31).
All94 bytes must compare exactly; these two padding bytes receive zero credit,
so the passing producer credits92 instruction bytes. The source
and binder emit no NOP or other helper instruction. The outside-only binder
anchors original code/data frames and real foreign symbols, and owns no DATA,
BSS, stack or filename values.

The focused `main-ending-dispatch-a` replay passed two independent fresh
producers, all94 compared bytes, complete OMF/MAP checks and the original
literal ordered fixups. The meaningful compiled negative changes the normal
continues-used condition from!=0 to==0 and fails comparison. This is one
shared CODE control for the actual two-function TU, rather than a separate
own control for Extra. The ledger credits92 instruction bytes and two complete
functions; both checked linker NOPs retain zero authored credit.

Private `.analysis/ending-dispatch-boundary-review.json` retains the original
native proof, and `.analysis/unit-replays/main-ending-dispatch-a/receipt.json`
records the acceptance. Historical original-TU identity and independent
whole-program placement remain unproved.
