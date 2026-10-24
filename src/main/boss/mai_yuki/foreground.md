# Mai/Yuki foreground candidate

This natural owner defines the real sprite helper at `[107D2,1081D)` (75 bytes)
and the complete shared foreground callback at `[1081D,108DF)` (194 bytes).
Both use near frame `0AE1`, `main_01`; DS is `209D`. Native review verifies
108 instructions across all 269 bytes, both real returns and every internal
direct branch. The helper is near Pascal with four signed word arguments and
RET8. Neither function has a table, padding, initialized DATA or BSS.

The helper animates the Mai/Yuki sprite banks 184 and 200 and selects the normal
sprite or damage silhouette through the real far Pascal master.lib APIs. The
callback computes both screen coordinates using the unchanged canonical full
Boss records. `boss` is at DS `5ABA`, and `boss2` is the real Yuki record at
`5AD2`. Its `phase_state` byte at `5AE7` selects which boss is being defeated.
The callback renders the appropriate explosion and surviving sprites, calls the
two actual foreign explosion renderers, and clears both real damage flags.

The 16-cel Yuki bank offset and the `0xFF00 | GC_RMW` plane control are real
sprite/hardware interfaces. No asset contents, copied target bytes, assembly,
register-allocation hints or stand-in implementations are present. The adjacent
helper and callback are defined in the same genuine TU and segment. Canonical
accepted headers remain unchanged.

Original ordered fixups are `[165,146,67,49]` for the complete cohort,
`[67,49]` for the helper and `[90,71]` for the callback. Calibration contributes
only unique complete-body routing; its collection order does not replace the
original stream. The independent binder provides real foreign master/explosion
labels and outside-only gaps. It keeps each individual ORG below 64 KiB and
separates the gap after `main_01` from the group before reaching DS `209D`.
Its fixed tail is valid only if actual OMF confirms the complete 269-byte extent.

Private `.analysis/mai-yuki-foreground-boundary-review.json` contains target and
source hashes, native boundaries, returns, branches, calls, layout and ABI
evidence. `.analysis/mai-yuki-foreground-unit-proposal.json` registers the whole
pair and a meaningful own animation-speed mutation, `/ 2` to `/ 3`.
`python3 .analysis/mai-yuki-foreground-review.py` repeats the bounded review.
The candidate is uncompiled and unaccepted; two fresh producers, full raw and
ordered-fixup agreement, OMF/MAP/dependency verification and a rejected negative
control remain necessary.

The first producer, `main-mai-yuki-foreground-a`, emitted the exact 75-byte
helper boundary followed by a 198-byte callback, rather than the original 194.
The helper's instruction boundaries and original ordered fixups `[67,49]`
were unchanged. Its sole raw mismatch was the stage-frame byte's DS offset,
displaced by the callback's extra four bytes moving the fixed outside tail.
That comparison failed and earns no normalized credit. Native inspection
isolated the callback difference to ordinary coordinate allocation: Mai's
coordinates were stored on the stack and Yuki's occupied SI/DI, while the
original did the reverse. No register hints or speculative variants are used
to change the complete callback.

The helper's literal statement body is now maintained once in `sprite_put.cpp`;
the coherent `foreground.cpp` includes it under a combine guard. The actual
four-word near Pascal interface is unchanged. Its separate symbol-only binder
ends the whole 75-byte contribution at `1081D`, so the unaccepted callback
cannot displace the real DS context. The private
`.analysis/mai-yuki-sprite-put-factor-proof.json` records equality to the saved
producer and the independent complete-contribution proposal. Only this helper
is proposed for a focused replay, using its own animation `/ 2` to `/ 3`
negative. The full 198-byte callback remains a complete unaccepted candidate.

The focused standalone replay `main-mai-yuki-sprite-put-a` subsequently passed
two fresh complete 75-byte producers, full raw bytes, the original ordered
fixups `[67,49]`, and the own animation-speed negative control. The root
accepted those 75 bytes only. `sprite_put.cpp`, its complete ABI header and its
independent binder are now frozen accepted inputs. The coherent callback still
emits 198 bytes and receives no exact credit.
