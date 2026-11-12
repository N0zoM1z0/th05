# MAIN eyecatch far pointer to the independently owned resource filename

MAIN `[20A6C,20A70)` is a single complete compiler-generated
four-byte far pointer, `eyename`, whose *value* points at the separately
accepted eight-byte mutable `EYECATCH_FN` string `eye.cdg`. The actual
original pointer is DS `209D:009C` and its target is DS `209D:00AA`.
The C source uses `extern char near EYECATCH_FN[8]` and a natural
`char far *near eyename = EYECATCH_FN;` initializer. The compiler and
linker, not the source or binder, produce the actual four-byte pointer
and its real segment relocation. The canonical `eyename` variable is
also consumed by the independent accepted EMS/eyecatch lifecycle code.

The binder supplies only a *foreign public* for the separately accepted
resource-name owner at its original DATA address, and no target string
contents, pointer words, code or candidate DATA. The following
unclassified word `[20A70,20A72)` remains outside the pointer owner.
The scoped replay
`.analysis/unit-replays/gpt-web-main-eyepointer-a/receipt.json`
proves both native Borland C producers, complete 4-byte initialized
DATA OMF/MAP scope, exact raw bytes and the original ordered MZ segment
fixup at relative +2. A compiled mutation that advances the destination
by one character is rejected. Nothing about the whole executable's
linkage is inferred from this bounded proof.
