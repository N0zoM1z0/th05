# Gather template copy: ordinary C++ diagnostic

The near Pascal helper MAIN16F70..16F8B is a complete 27-byte procedure,
taking one near gather reference and returning with RET2. It copies the full
14-byte bullet_template at DS577E into the gather's member at offset24.
Its original ordered MZ fixup stream is empty. ReC98 b6ba5b0a gather.cpp
describes the same operation with copy_near_struct_member; the existing
maintained gather/BulletTemplate declarations assert all fields and extents.

The ordinary struct assignment in copy_to_bullet.cpp emits a valid 27-byte
Borland object, but its bytes differ: it pushes far source and destination
pointers and calls F_SCOPY@. The native helper instead saves SI/DI, sets ES=DS
and copies seven WORDs with REP MOVSW. Equal size grants no acceptance.
The normal focused replay stops at the unresolved real F_SCOPY@ dependency;
no placeholder provider, second producer, negative or behavior model was added.
The proposal is outside the live manifest. The neighboring reverse copy is
not recompiled, and neither procedure gains C++ or ASM credit from this trial.

The complete object diagnostic is `.analysis/gather-copy-to-natural-review.json`,
which records the failed link and source dependencies.
The current simple source and symbol-only binder remain available for further
natural source work; they are not accepted build inputs.
