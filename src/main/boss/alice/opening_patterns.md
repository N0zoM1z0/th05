# Alice recovery and opening patterns

Six complete functions fill original MAIN `1E435..1E602`, immediately before
the accepted beam. The461-byte contribution contains149 instructions, no
padding, compiler tables, initialized DATA or BSS.

| Function | Original extent | Bytes | Ordered fixups |
|---|---|---:|---|
| `alice_puppet_recover` | `1E435..1E44D` | 24 | none |
| `alice_puppet_hold` | `1E44D..1E456` | 9 | none |
| `alice_pattern_opening` | `1E456..1E4F0` | 154 | `[149]` |
| `alice_pattern_opening_cycle` | `1E4F0..1E50A` | 26 | none |
| `alice_pattern_ring_stack` | `1E50A..1E586` | 124 | `[100]` |
| `alice_pattern_spread_stack` | `1E586..1E602` | 124 | `[100]` |

Recovery completes after96 unsigned puppet frames; hold intentionally returns
false and does not use its genuine argument. These are real near Pascal
callbacks taking a near Puppet reference and returning AL with RET2. The
other four functions are near cdecl boss-pattern algorithms. Their complete
returns and every local branch destination were checked natively.

The opening charges until64, then emits32 random bullets of alternating
sprites within a48-pixel spawn area. Its cycle wrapper resets mode/frame at96.
The other patterns charge similarly and fire an aimed28-way ring stack or
seven-way spread stack at64. Packed assignments represent the real adjacent
spread count, angle delta, stack count and speed-delta fields. No asset,
instruction or callback-pointer array is introduced.

The frozen beam header supplies the canonical full Puppet26, Boss24, Player,
motion and BulletTemplate14 types. Gather has the actual near Pascal argument
order `(frame-40,9,8)`; random helpers and bullet emission share frame1527.
Sound is far Pascal14AB:0232 and DS is209D. The symbol-only binder preserves
the foreign segment names and anchors a paragraph tail after1E610, ending at
209D0. It supplies no instructions, initialized values, stack or internal hole.

The original full-contribution relocation stream is `[437,313,182]`, retained
without sorting. ReC98 `th05_main.asm` lines11473..11701 supplies semantic
evidence; cached calibration matches all six complete instruction shapes,
providing routing evidence only. Preparation does not establish source exactness.

Private metadata `.analysis/alice-opening-patterns-boundary-review.json`
provides the whole461-byte proposal and optional six complete-function scopes.
`.analysis/alice-opening-pattern-scopes.json` contains the scope entries.
`main-alice-opening-patterns-a` passes two fresh deterministic complete
461-byte raw comparisons and the original ordered fixups `[437,313,182]`.
The compiled ring spread count28→27 control is rejected for this whole owner.
All six functions are accepted. No DATA, BSS, compiler tables or padding
receive credit, and the optional individual scopes are not imported.
