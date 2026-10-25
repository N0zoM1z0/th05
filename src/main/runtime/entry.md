# MAIN entry

`entry.cpp` maintains the complete original `[AE38,AEA6)` entry in frame
`AE1`, DS `209D`. All110 bytes compare; the linker-relaxation NOP at relative103
is checked with zero credit. The owner contributes109 authored instructions.
The real compiler main returns far, with no arguments. There is no trailing
table or initialized source DATA/BSS.

The algorithm and complete declarations are factored unchanged from the
maintained adjacent entry/loop candidate. It loads the actual128-byte resident,
sets the paragraph budget, initializes graphics and sound, then loops through
stage sessions until handing off to OP. The real filename objects are foreign
bindings; no strings or assets are supplied by the scaffold.

The original five-byte handoff at AE9F is NOP/PUSH-CS/CALL near to CEC2.
That callee is the independently accepted159-byte `GameExecl`, in the same
physical AE1 frame, ending in RETF4 at CF5E. `#pragma samecodeseg GameExecl`
communicates this proven context while retaining its actual far Pascal
signature. It changes no algorithm, argument width, return convention or
instruction body. This is the same genuine context recovered for stage reset
and enemy lifecycle, without physical-register expressions or flag changes.

`main-entry-c` passed two fresh complete producers, actual OMF/MAP/dependency
validation, raw comparison, original ordered fixups `[79,67,44,23]`, and its
own compiled paragraph-budget increment. The earlier two scaffold attempts
failed before a successful link: one omitted ASSUME CS for outside near
labels, and one left the real empty foreign SEGDEF outside the correct group
context. Both artifacts remain private; neither supplies positive evidence.

The separate gameplay loop remains unaccepted. Its foreign address is bound
to the real AEA6; no loop bytes or algorithm are supplied by this oracle.
The combined `main.cpp` includes both canonical bodies for continued work,
with no duplicate credit. Private `.analysis/main-entry-boundary-review.json`
records native instructions, NOPs, actual ABI proof and input identities.
