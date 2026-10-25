# Mai/Yuki survivor foreground candidate

The complete original foreground occupies `[1093F,109BD)` (126 bytes,
50 instructions), near `main_01` frame `0AE1`, DS `209D`. Native review includes
the actual final RET, every direct branch and an explicit zero-NOP enumeration.
There is no table, padding, DATA or BSS contribution. Original ordered fixups
are `[114,96,44]`.

Its identity comes from the original shared-fight transition at `1839C`, which
writes `5B2F` to DS `C676`, selecting `AE1:5B2F = 1093F`. The maintained caller
already names this real callback `mai_yuki_survivor_render`; its C++ near Pascal
interface is preserved. The current full Boss contains the survivor's position
after the shared transition has handled the actual state copy.

The renderer selects the big explosion or the normal sprite, animates the
actual 208/192 banks using the byte frame clock with signed `/ 2` promotion,
and draws the real damage silhouette. It does not introduce a damage reset
absent from this original helper. Both genuine foreign explosion renderers
always run afterward. The accepted common foreground header supplies the full
24-byte Boss and real far sprite/near explosion interfaces unchanged.

The independent binder retains the exact foreign CODE segment name and group,
actual master/explosion labels, DS fields and outside-only holes. Its fixed
tail is valid only if actual OMF confirms all 126 bytes. No instruction array,
assembly, pseudoregister, allocator hint, fake provider or source padding is
present. The gap between this owner and the Extra renderer is not a claimed
combined target interval.

Private `.analysis/mai-yuki-survivor-render-boundary-review.json` contains native
boundaries, calls, branches, NOPs, callback identity, hashes and ABI evidence.
Its `*-unit-proposal.json` supplies the meaningful animation `/ 2` to `/ 3`
negative. `python3 .analysis/extra-survivor-render-review.py` repeats the bounded
checks. This source remains uncompiled and unaccepted until two fresh complete
raw/original-order producers, OMF/MAP/dependency gates and its own control pass.

The focused `main-mai-yuki-survivor-render-a` replay passed two fresh complete
126-byte producers, all raw bytes, original ordered fixups `[114,96,44]`, and
its own compiled animation-divisor 2-to-3 negative. The root imported the whole
callback. Its C++, shared complete ABI header and independent binder are now
frozen accepted inputs.
