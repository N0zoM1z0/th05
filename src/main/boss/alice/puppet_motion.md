# Alice puppet entrance and motion

Two consecutive complete functions cover original MAIN `1DF86..1E209`:
the 159-byte entrance and 484-byte movement/dispatcher. They contain52 and167
instructions, respectively, with no compiler tables, padding or owned DATA.
The accepted whole owner retains both complete functions in one real TU.
The original per-function ordered fixups are `[123,95,54,26]` and
`[365,334,318]`. The original full-region stream is
`[524,493,477,123,95,54,26]`; neither stream is sorted or normalized.

Entrance computes the two puppets' polar spiral positions, advances their
opposite angles, shrinks both radii and preserves previous positions. Motion
eases each signed coordinate toward its destination with large and small
divisors before snapping the remainder. Stationary puppets call real near
Pascal reference-taking bool callbacks, choose new destinations and select
from the existing four-entry semantic callback table. Player collision,
shot damage, score, death animation and revival retain their actual state
semantics. The full26-byte Puppet and canonical Boss/Player storage come
from the frozen beam header, which is not edited.

Polar and sound are real far Pascal functions in frame14AB. Shot testing is
far cdecl at AE1:8873. Random helpers and recovery callbacks are near code
in frame1527. The recovery callback is foreign and remains unimplemented
here. The existing trig and callback tables are declared, with no entries
or opaque data restored. Score is the real unsigned32-bit accumulator.

The symbol-only binder anchors all foreign compiler segments, two scope
starts and DS209D. Its paragraph tail starts at1E210 after both complete
functions; no instructions, initialized values, stack or internal hole are
provided. The accepted source expresses both easing calculations
directly on the actual near-owned puppet fields, preserving signed division
and rounding without constructing reference-address temporaries.

ReC98 `th05_main.asm` lines10918..11207 supplies the semantic reference.
All original branch destinations, complete returns and ordered fixups were
reviewed natively. Cached calibration matches both complete instruction
shapes, providing routing evidence only. Private metadata and suggested
scope/control entries are `.analysis/alice-puppet-motion-boundary-review.json`
and `.analysis/alice-puppet-motion-scopes.json`.

The first saved producer emitted 710 bytes: entrance 159 was raw/fixup exact,
but the inlined easing helper retained FAR references under the large memory
model. Reference construction and ES accesses inflated the dispatcher to 551
bytes. Explicit near references reduced the next result to 690 total bytes
but retained address temporaries. Directly expressing the same easing on the
fields produced 634 total bytes in `main-alice-puppet-motion-c`.

That dispatcher had 475 bytes and 167 instructions, against the original
484 bytes and the same 167 instructions. The loop index occupied DI rather
than BP-2, saving 12 bytes, while the callback result occupied BP-2 rather
than DI, adding 3 bytes. All arithmetic and branch widths agreed. Reusing one
ordinary integer local across the mutually exclusive movement-delta and
callback-result paths recovered the original allocation. This preserves the
actual signed arithmetic and callback promotion without register hints,
barriers, compiler-body ASM or extra work.

`main-alice-puppet-motion-d` passes two fresh deterministic producers for
all 643 instruction bytes and the complete original ordered relocation stream
`[524,493,477,123,95,54,26]`. The actual entrance angle decrement 2→3 mutation
is compiled and rejected for this whole owner. Both functions are accepted;
no compiler tables, padding, DATA or BSS receive credit. The separate recovery
callback and referenced tables remain foreign and uncredited.
