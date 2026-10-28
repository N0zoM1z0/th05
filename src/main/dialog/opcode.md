# Complete dialog interpreter: isolated and split-context investigation

The pinned MAIN interpreter at `[13B82,13D4A)` is456 bytes:425 instruction
bytes, one zero at425 and the complete30-byte command table at426. Its124
instructions have no NOPs. All fifteen command-table destinations and direct
branches land on reviewed instruction starts. Original ordered MZ fixups are
`[395,336,312,269,224,217,174,145,136,86]`. The target remains the locally
attested Japanese candidate, not an independently proved pristine executable.

The unchanged semantic command body is factored from runtime.cpp into
opcode.inl. The existing box/run producers, shared declarations, packed5-byte
sprite command and all accepted dependencies are unchanged. opcode.cpp puts
the complete interpreter in its own real main_01 contribution and restores
the CODE selector and ordinary late `-a2` after includes. Its first producer
still emits455 bytes and stops at the complete size gate. This independently
confirms that isolating the interpreter does not restore the missing zero.

opcode_context.cpp additionally contains the literal maintained definitions
of the two genuinely earlier STD callbacks, in native source order. They
occupy a separate73-byte CODE contribution at their actual139F5 address.
The symbol-only binder leaves the intervening three graphics helpers and
box functions foreign, without supplying instructions or values. The new
interpreter contribution is again455 bytes and fails its first size gate.
There is no second positive, compiled negative, receipt or acceptance for
either attempt. Both proposals are retained privately outside the live manifest.

Actual OMF, staged source, compiler arguments, MAP and MZ are reread. Both
interpreters start at13B82. Their425-byte instruction bodies differ only at
relative23,116,180: the table operand is one byte earlier and the short source
contribution shifts the two foreign forward labels one byte earlier. All15
compiler-generated case targets agree with the native table. Ordered fixups
agree. The STD prefix retains its73-byte size and actual relaxed transfer,
including uncredited NOP24, but its forward animation call also shifts by one
byte at27. It is not raw exact or a replacement for the existing accepted
callback owner. These are diagnostic observations, not normalized acceptance.

The split-segment prefix therefore does not resolve the table phase. The
intervening218-byte graphics implementation remains a separate source/language
question; it must not be replaced by an instruction transcription, fabricated
prefix, inside-function reservation or padding. No source body, object, table
word, operand or relocation stream is patched to manufacture equality.

## Native and compiled behavior

Each of the native and two actual compiled interpreters passes780 cases:
all256 command bytes under three state/payload scenarios, plus twelve byte-read
cases wrapping the script offset fromFFFF to0000. The model checks AL's boolean
result, Pascal cleanup, preserved SI/DI/BP/CS/DS/SS, complete dialog pointer,
cursor/side fields and adjacent canaries. It checks actual stack words and call
order for faces, filenames, sprite cleanup, packed sprite payloads, sound,
palette fades, gaiji and text wiping. Cases include nonzero unused parameter
high bytes, noncanonical nonzero sides, extreme coordinates, empty filenames,
unsigned filename bytes and stop/play music commands. The original false-return
quirk for executed commands remains intact.

Foreign graphics, audio, delay and strlen use explicit ABI stubs with scratch
register clobbers. Hardware effects, assets, timing, blocking behavior and the
STD callbacks are not executed by this model. The2,340 total cases establish
bounded interpreter semantics, with zero exact or authored credit.

Native/source/actual producer review:
`.analysis/dialog-opcode-root-review.json`, SHA-256
`cbfac3b961c10cd82eba16ca5b9561722359c57a8c760628fd97333f94b54df8`.
Semantic model `.analysis/dialog-opcode-semantic-model.json`, SHA-256
`d81121f28079d6fd1e4d0de76fb48790ef42bedf186bf282dba387d108c7f593`.
Failed first producers:
`.analysis/unit-replays/main-dialog-opcode-standalone-a/` and
`.analysis/unit-replays/main-dialog-opcode-context-a/`.

After that producer review, one empty final line was removed from opcode.inl
to satisfy the staged diff check. The archived source hashes describe the
original producer snapshots; this whitespace cleanup claims no new compilation.
