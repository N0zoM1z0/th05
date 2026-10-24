# EX-Alice foreground candidate

The complete original foreground callback occupies `[11CAD,11D50)` in
`main_01`, near frame `0AE1`, with DS `209D`. Native review decodes all 163
bytes as 64 instructions, checks the actual final RET and every direct branch
destination, and finds no table, padding, initialized DATA or BSS. The next
original function is the accepted HUD owner at `11D50`.

The source reuses the unchanged full canonical Boss. It displays the big
explosion when appropriate; otherwise it adds the actual eight-cel sprite-bank
offset on odd bomb-invincibility frames, draws the normal or damage silhouette,
clears damage after that silhouette, and draws the animated backdrop in its
real phase/sprite range. It always calls both genuine foreign explosion
renderers. The byte frame's `% 2` uses ordinary integer promotion and signed
remainder, preserving the original IDIV semantics.

`exalice_bomb_invincibility` at DS `4A8E` and `exalice_backdrop_patnum` at `4A9C`
are the already maintained canonical EX-Alice state identities, not new aliases.
The sprite functions retain their real far Pascal frame-zero ABI. The explosion
consumers retain near frame `0AE1` and their actual compiler symbol spellings.
No assembly, byte arrays, pseudoregisters, register-allocation hints or fake
callee implementations are present.

The original ordered fixups are `[151,106,88,44]`. Calibration independently
decodes to the same complete 163-byte/64-instruction extent and gives one native
operand-masked routing match. The earlier census's generic mask skipped this
body; that did not establish an incomplete function or a call-relaxation
difference. The private bounded review processes far-transfer encodings before
Capstone immediate fields and keeps its diagnostic mask exactly 163 bytes.
Masking remains a routing aid and never substitutes for full raw acceptance.

The symbol-only binder places real sprite, explosion and DS symbols, with all
holes outside the complete function. Actual OMF must confirm its 163-byte
extent before the fixed outside tail is valid. Each individual ORG stays below
64 KiB, and a separate gap after `main_01` retains DS `209D`.

Private `.analysis/exalice-foreground-boundary-review.json` and
`.analysis/exalice-foreground-unit-proposal.json` record hashes, native
boundaries, calls, branches, layout and the meaningful sprite-bank negative
`patnum += 8;` to `7;`. `python3 .analysis/exalice-foreground-review.py` repeats
the bounded native review. The candidate remains uncompiled and unaccepted;
only a focused two-producer replay with full raw bytes, original ordered
fixups, OMF/MAP/dependency gates and rejected own control can establish exactness.

The focused `main-exalice-foreground-a` replay passed two fresh complete
163-byte producers, full raw bytes, the original ordered fixups
`[151,106,88,44]`, and its own sprite-bank 8-to-7 negative control. The root
accepted this whole callback. Its source, complete ABI header and independent
binder are now frozen accepted inputs.
