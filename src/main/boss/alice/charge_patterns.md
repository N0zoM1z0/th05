# Alice charged-pattern candidate

Three contiguous natural algorithms follow the accepted puppet beam:

| Function | Original complete extent | Bytes |
|---|---|---:|
| `alice_pattern_laser_fan` | `1E764..1E82C` | 200 |
| `alice_pattern_paired_stacks` | `1E82C..1E8C7` | 155 |
| `alice_pattern_rotating_ring` | `1E8C7..1E957` | 144 |

The full499-byte contribution contains150 instructions, no compiler tables
or padding, and no owned initialized DATA/BSS. All complete returns and local
branch destinations were checked against original MAIN. The original ordered
fixup offsets are `[477,403,333,248,105,45]`; no sorting or normalization is
used. ReC98 `th05_main.asm` lines11837..12015 and the cached calibration give
matching complete instruction shapes at19E12..1A005, solely as routing and
semantic evidence. Neither reference acceptance nor calibration equality is
claimed for TH05 source.

All three charge before frame64, animate sprite184, sound at40 and return to
mode0 at96. The laser fan fires three real shootout lasers at the aimed angle,
then plus16 and minus16, together with a random bullet cloud. The other two
emit mirrored aimed stacks or a rotating red ring every fourth signed frame.
Their state-byte angle updates and genuine signed modulo behavior remain.
Packed word assignments represent the actual adjacent spread/count and
angle/speed-delta fields; no asset or instruction array is introduced.

The frozen `beam.hpp` supplies the validated full Boss, Puppet, Player and
bullet interfaces. The existing accepted `laser.hpp` supplies the complete
24-byte Laser and its real movement-age union. Neither header is edited.
The gather call uses actual16-bit Pascal parameters `(frame-40,9,8)`, matching
the original combined color push`00090008`. `iatan2` is the real far Pascal
integer-returning function at`0000:1F3A`, called with signed y/x differences.
Laser creation is the actual near-cdecl entry at1A66E; gather is near Pascal
at1705D, regular bullets near-cdecl at17204, and sound far Pascal14AB:0232.
The existing tuning callback at DS41DE remains foreign.

The symbol-only binder explicitly anchors even empty foreign `_TEXT`,
`MAIN_01_TEXT`, `SHARED`, `B4_UPDATE_TEXT` and `LASER_SC_TEXT` contexts before
the owned `ALICE_CHG_TEXT/main_03`. All near code shares frame1527; DS is209D.
The paragraph tail begins1E960 outside the complete contribution. It supplies
no instructions, initialized values, inside-function holes, stack or assets.

Private integration metadata is
`.analysis/alice-charge-patterns-boundary-review.json`. The proposed wrapper
is`th05/a_chg.cpp`, unit`main-alice-charge-patterns`. Its meaningful negative
changes laser width8 to9 in the staged canonical source. Root must verify
actual CODE/empty-SEGDEF placement, EXTDEF names, two fresh deterministic
producers, full499 raw bytes, original ordered fixups and compiled rejection.
This preparation executes no compiler and establishes no source acceptance.


`main-alice-charge-patterns-a/receipt.json` accepts all499 raw bytes and all six
original ordered fixup sites across three complete functions. Both independent
fresh deterministic producers agree. The separately compiled laser width8→9
mutation is rejected. Credit is499 authored instruction bytes with no table,
padding, DATA or BSS. The accepted beam and Laser headers were not modified.
