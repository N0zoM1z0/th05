# Complete Music Room frontend context

The maintained source now has one canonical implementation in
`music_body.inl`, included by the thin `music.cpp` translation unit. This
replacement is accepted through `op-music-full-context-a`. Its fifteen
CODE/DATA records pass two fresh deterministic producers and the actual DATA
mutation; `op-music-full-context-code-negative-a` supplies the shared CODE
mutation. The old split receipts remain unchanged historical evidence.
The reviewed proposal is retained privately as
`.analysis/op-music-full-context.proposal.toml`.

The original family is `BE79..C7D5`, 2396 bytes / 15 complete functions, in
frame `0A39`. Native decoding covers every function without NOPs, padding or
CODE tables. Fourteen accepted function scopes total 2366 bytes. The
intervening 30-byte `nopoly_B_put()` has no acceptance entry. The same replay also
refreshes the complete 6217-byte DATA owner. Its 732-byte BSS placement remains
a layout check, without stored-byte credit.

The old split source has a 381-byte / four-function prefix, a symbol-only
foreign helper slot and a 1985-byte suffix. It previously accepted twelve functions but
failed original relocation order for the polygon renderer and menu. The retained
real calibration compiles the complete frontend as one CODE contribution.
Its 1020/1018/358-byte LEDATA payloads place those fixups in the original record
groups. Native comparison verifies both complete functions, raw bytes and
literal ordered relocations. The new maintained producer independently reproduces those record groups
and passes both complete functions; retained calibration alone is not acceptance.

## Actual DS/ES hardware boundary

`nopoly_B_put()` is a near no-argument function. The original saves BP, SI, DI
and DS, selects ES=`A800`, reads the two-byte saved-plane segment handle at
incoming DS:`4EB8`, then selects that handle as DS. It copies 16000 words
from DS:0 to ES:0 and restores the caller's DS and saved general registers.
ES remains `A800`; CX reaches zero. The original contains no CLD and retains
DF; forward restoration requires the caller's normal DF=0 convention. Graphics
page and GRCG state belong to the actual callers, without an added port shim.

Installed Borland `MEM.H` line93 declares the real `__memcpy__` intrinsic.
The new source uses that API for the complete copy. Only DS save/restore is
explicit assembly; ES/DS assignments express the real temporary hardware
address spaces. There are no DI/SI assignments, register arithmetic, supplied
XOR/REP instructions, opcode arrays or call templates.

The original and retained compiler helper are both 30 bytes. Their only byte
differences are at offsets16 and18: the original uses `31 FF / 31 F6`, while
the intrinsic emits `33 FF / 33 F6`. Both encodings have the same semantics and
length. Both fresh maintained producers confirm these same two differences.
The source preserves compiler output; the complete helper remains
unaccepted. Neither a successful copy nor surrounding exact functions can
promote those 30 bytes.

## Canonical source and affected acceptance

The factor preserves every pre-existing implementation byte. Only the old
foreign-helper marker and segment selector are replaced by the genuine helper
body. Header type/ABI tokens are unchanged; all own first declarations now
capture `OP_MUSIC_TEXT/op_01`, including the menu declaration before its
canonical header repeats it. The new symbol-only binder has no foreign helper
label or interior ORG hole. It retains shared frame `0D30`, DS `0EFE`, DATA end
`2817` and BSS extent `4D84..5060`, without `.stack`.

The affected acceptance closure is nine CODE records representing twelve
functions, plus the Music Room DATA record. No other accepted OP, MAIN or
MAINE closure references these inputs. The old 381-byte prefix cannot remain
a complete contribution inside the new producer. The proposal explicitly
reuses its ID for the first 212-byte function and adds the other three scopes
of 106/49/14 bytes. The old eight suffix IDs remain complete functions. New
scopes are the 502-byte polygon renderer and 837-byte menu. Every end is the
actual next function public, including the unaccepted helper; the final menu
ends at the real contribution end.

All fifteen accepted CODE/DATA records share one source/module, encoding,
binding context and compiler recipe. The focused replay compiled the TU
once per positive round. The combined replay uses three compiler invocations:
two positive producers and a DATA negative changing `music.pi` to `music.pj`.
One additional compiler invocation changes the menu threshold from24 to25
and validates the shared fourteen-function CODE cohort. It is one shared
compiled control, not a separate negative for every function or for both new
scopes. It rebuilds no positive producer. The new OMF/MAP/raw/ordered-fixup evidence and CP932 consumed-source
validation pass, and all affected records were imported atomically. The two
new functions add 1339 authored instruction bytes. No unchanged owner outside
the Music Room closure was replayed. The whole 2396-byte contribution
must never be described as raw exact while its helper remains different.

Private baseline and inverse-factor proofs are retained in
`.analysis/op-music-full-context-baseline/`,
`.analysis/op-music-canonical-factor-equivalence.json` and
`.analysis/op-music-full-context-proposal.json`. No historical producer,
receipt or ordered fixup list was changed by this preparation.
