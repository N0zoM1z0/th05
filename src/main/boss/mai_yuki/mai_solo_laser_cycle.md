# Mai solo radial laser cycle candidate

This is the actual461-byte provider at original MAIN1935E–1952B, corroborating
reference anonymous sub_1C34B. It is distinct from the separately maintained
270-byte laser-bounce attack at19250. All461 bytes decode as157 instructions;
the final near RET immediately precedes the real Mai update prologue at1952B.
There is no inline table, padding or MZ relocation inside this complete owner.
Native preparation and source presence do not grant exact authored credit.

The natural algorithm spawns rank+5 radial fixed lasers, keeps their origins at
Mai's real position, grows and shrinks them at the original cycle ticks, clamps
a signed angular velocity, rotates a fractional phase accumulator, reverses the
actual byte direction and periodically selects one of three bullet patterns.
It retains the randomized clock skip and delayed random movement. Ordinary
integer arithmetic preserves the original signed divisions and unsigned
byte-angle wrap; there are no pseudoregisters, raw object views or flags variants.

Complete Laser24, Boss24, B4Ball26/template25 and geometry come from the frozen
mai_solo_advanced.hpp dependency chain unchanged. Actual state is count4432,
angular speed4434, fractional accumulator4436 and inner callback443A. The latter
is a genuine near cdecl void callback, independent of the outer solo bool
callback at4438. Its real three-pointer bank at DS1976 resolves to18EA9,
18F07 and18F60: the already maintained rotating fans, rotating rings and snow
rings. No table values, callback bodies or DATA initialization are supplied.

Foreign manual spawn1A74B and grow1A7A5 are genuine near Pascal word-slot APIs.
The array is the complete32-entry Laser24 pool at DS578C; the real template is
5A8C. RNG and random flight retain their accepted frame1527 interfaces. A real
signed local phase word holds the initial angular phase, cycle tick and integer
step at different times; no fake register-matching helper is introduced.

The private packet is `.analysis/mai-solo-laser-cycle-bindings.asm`,
`.analysis/mai-solo-laser-cycle-unit-proposal.toml` and
`.analysis/mai-solo-laser-cycle-boundary-review.json`. The single meaningful
negative increases the rank-based ray count from+5 to+6. The binder contains
only actual external addresses and outside-owner space, with no code or assets.
Pinned ReC98 b6ba5b0a529edbb31efdf8c0e939263804f8ee47 is behavior corroboration;
all complete bounds, actual fields, pointer targets and empty ordered relocation
lists were independently read from the original. No compiler, core manifest or
accepted-source/header change was performed during preparation.

`main-mai-solo-laser-cycle-a` passes two fresh deterministic complete461-byte
raw comparisons and the empty original relocation stream. The actual
rank-dependent ray count+5→+6 control is compiled and rejected. One complete
function and461 instruction bytes are accepted, without tables, padding,
DATA or BSS. Its header uses a short distinct guard before the first producer.
