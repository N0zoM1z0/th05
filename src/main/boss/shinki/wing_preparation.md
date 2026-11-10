# Shinki wing preparation and ball-update evidence

The complete wing transition MAIN1ADDE..1AF60 is accepted from maintained
C++ through the explicit `tcc-s-tasm32` compiler recipe. All386 instruction
bytes and the original ordered MZ fixups `[76,305]` match. There is no table,
padding, initialized DATA or BSS. Canonical Boss, Laser, templates, palettes,
geometry, return type and foreign interfaces remain unchanged. The C++
algorithm and headers did not need instruction, type or behavior changes.

## Compiler recipe and acceptance

The former direct TCC object matches every raw byte but emits `[305,76]`.
The new recipe compiles the same C++ with `-S`, then assembles the unmodified
compiler output with the pinned TASM32 and links the normal symbol-only
binder. Its natural object fixup stream yields `[76,305]`; no instruction,
object record, relocation list or linker output is edited or sorted. This is
C++ recovery, with no new handwritten-ASM ownership claim. The historical
producer and literal historical source remain unknown.

TCC emits GROUP members for foreign first-declaration contexts without
emitting all corresponding empty SEGDEFs in its assembly text. The consumer
wrapper supplies only those absent CODE declarations, checked against the
real binder's classes and groups, then includes the compiler file verbatim.
It supplies no executable instruction, initialized data or artificial stack.
Actual MAP readback retains CS15270, DS209D0 and main_03. Complete ordinary
OMF/LEDATA ownership excludes every other nonempty source segment.

Both fresh producers preserve the compiler-generated assembly hash before
and after TASM and reproduce the same assembly text, normalized OMF, MAP and
whole comparison MZ. Input mtimes are fixed build metadata; compared bytes
and ordered fixups are never normalized. TCC's actual E9 dependency records,
C++ wrapper, consumed source/header bytes, binder, recipe code, toolchain
execution proof and actual compiler/assembler/linker commands are frozen.
Saved-receipt import independently reads those artifacts and rejects changed
compiler text, context, command, object, linked code or aliased producer paths.
The default direct-object recipe and existing acceptance remain unchanged.

The normal shared source negative changes shake duration8 to9. It changes
only byte311, keeps the complete386-byte extent and ordered fixups, and is
rejected. No additional game behavior model or per-function test is added.
Only the new pipeline's focused tooling checks and existing incremental
replay tests run; no full CI or accepted-set cold replay is required.

## Affected replay after adding decoded artifact contexts

The recipe now supports explicit OP/MAINE binary and decoded-target proofs.
Its source identity therefore changed for this accepted wing owner. Only this
accepted owner was replayed: two fresh unchanged C++ chains still match all386
bytes and `[76,305]`, with the same shake-duration negative rejected.
The replacement adopted receipt is
`.analysis/unit-replays/main-shinki-wing-artifact-context-c/receipt.json`,
SHA-256 `cf074f3e7ad481533070945dc10777f56576091105fd4fc5f6d32000d1ae7655`.
Coverage stays386 bytes;
this receipt replacement adds no function or authored byte.

## Ball updater remains unaccepted

The original ball update1AACF..1ABAB is220 instruction bytes, no NOPs, table
or MZ fixups. An older register-backed candidate emits216, merging two jumps;
its bounded jump-optimization-off diagnostic emits224. Neither is an owner.
The ordinary scalar candidate in balls_update.cpp limits register reads to
the genuine DX:AX Point return, borrows it for clipping and unpacks at the
collision consumer. Immediate and later unpacking both emit232, using a
stack delta and longer conditional branches. No failed compiler body is
promoted to ASM. These observations do not require repeated builds.

The existing full-pool semantic evidence remains reference, not an additional
acceptance gate: `.analysis/shinki-balls-semantic-model.json`, SHA-256
`ea2bd3684eda5abb2a63ac9e9e8796c3317a7a02915e9e1dc843a9ebc8a54b53`.
Earlier native/source/actual review: `.analysis/shinki-wing-balls-root-review.json`,
SHA-256 `273fdda668ee1168da244a77f903094842d335cf183f3007af8a1ff90e28c39d`.
Only the separate wing function gains386 C++ bytes and one complete function.
