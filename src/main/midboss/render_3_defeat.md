# Stage-three and defeat rendering candidates

These are separate complete natural owners with no combined interval claim.
Stage-three rendering occupies `[13106,13185)` (127 bytes, 48 instructions).
Defeat rendering occupies `[132D3,1337D)` (170 bytes, 63 instructions). The
unaccepted bullet renderer between them is outside both contributions and
receives no credit. Both use near `main_01` frame `0AE1` and DS `209D`.

Native review includes each actual complete RET, all direct branch targets and
an explicit instruction NOP enumeration: zero in each function. Neither range
has a table, alignment/relaxation padding, initialized DATA or BSS. Full raw
bytes remain subject to ordinary comparison. Original ordered fixups are
`[104,86]` and `[147,92,65]`, respectively, with no sorting.

The stage-three renderer reuses the frozen full 22-byte midboss and the accepted
stage-five scalar scroll/sprite/defeat interfaces. It clips negative Y, animates
sprite bank 208 using `stage_frame_mod16 / 8`, preserves other sprite bases,
draws and clears the actual damage silhouette, and dispatches the real defeat
renderer at big-explosion phase.

The defeat renderer grows a fixed-point radius from the real phase frame and
clamps it to 48 pixels. Once capped, its real byte phase advances by one. It
then calculates sixteen genuine polar positions from the complete canonical
sine/cosine interfaces, applies signed Y-then-X clipping, converts the actual Y
through scalar scroll, and draws the real sprite. The byte phase advances by
`0x10` per spoke. Its state is the observed byte at DS `1A60`; this owner does
not define or claim its initialized data.

The polar helper retains far Pascal frame `14AB:0394` and scalar AX return.
Scroll retains near Pascal load `DF28`; the master sprite API retains far
Pascal `0000:2FE0`. Complete accepted types and providers remain unchanged.
There is no returned-point temporary, CF convention, assembly, copied target
byte array, physical-register hint, fake helper or compensating source padding.
The sine/cosine tables remain external semantic objects, with no copied values.

Independent symbol-only binders provide actual foreign symbols and only holes
outside each complete contribution. They do not fill the unaccepted function
between these owners. Actual OMF must confirm each complete extent before its
fixed outside tail is valid.

Private `.analysis/midboss-render3-boundary-review.json` and
`.analysis/midboss-defeat-render-boundary-review.json` record native boundaries,
branches, calls, hashes, field identities and NOP checks. Their separate
`*-unit-proposal.json` files propose meaningful own negatives: the stage-three
animated base cel 208 to 209, and the defeat spoke step `0x10` to `0x11`.
`.analysis/midboss-render-3-defeat-unit-proposals.json` is an integration list,
not a contiguous target range. `python3 .analysis/midboss-render-3-defeat-review.py`
repeats the bounded review. Both candidates remain uncompiled and unaccepted
until focused two-producer full raw/original-order checks, OMF/MAP/dependencies
and rejected own controls pass.

The root imported both complete owners after focused strict replays. Stage
three passed `main-midboss3-render-a` with its own 208-to-209 negative. The first
defeat producer differed only in the genuine loop-update order: the original
increments the loop index before advancing the angle. Moving the actual angle
step into the `for` update clause after `i++` preserved the algorithm and
introduced no idle work. `main-midboss-defeat-render-b` then passed two fresh
complete 170-byte producers, raw bytes, original fixups `[147,92,65]`, and its
compiled `0x10`-to-`0x11` spoke-step control. Stage three retains its original
`[104,86]` fixup stream. The final negative anchor is the update expression
`midboss_defeat_angle += 0x10`, without a trailing semicolon. The accepted C++,
header and binders are now frozen.
