# Shinki background A/B/C/D controllers and the original C seed interface

The genuine MAIN stage-six background system is a contiguous family of
source-defined near and Pascal functions, not an independent renderer.
Its physical particle counter is now a separate, initialized, **two-byte
C public** `shinki_bg_type_a_particles_alive`, shared by the C++
background source through the C-linkage declaration in
`background_rules.h`. The actual original DGROUP seed is word 255 at
`209D:198A`, and the C++ type-A initialization compares against the
same `(-1 & 0xFF)` semantic sentinel. The code does not replace or
allocate the original `boss_particles`, `linesets` or other phase-state
objects. It does not claim any of the neighboring zero-initialized
background flags as authored DATA.

The real *A-type* background creates two opposite-facing line sets,
initializes the true particle pool with the offscreen `-999`-pixel
sentinel, then starts at most one new particle **every four Boss frames**
at the playfield center. The original speed range is 2–6 pixels per
frame, and the initial line angle is 0x40 with opposite 0x80 turn.
Once the linesets zoom out to radius 224, the existing byte-count
latch advances. Its two near helpers continue to grow lines and render
particles, rather than being merged into the large controller.

The *B-type* background sets initial line radius 256, horizontal
initial centers at 1/6 and 5/6 of the playfield, and drives the
original falling particles and vertical line velocities toward -14.
The *C-type* reverses the vertical motion and changes the particle
velocity bound to -10, with its distinct upward-line 14-pixel speed
limit. The *D-type* reuses the original particle buffer as rising
smoke, initialized at -1 pixel velocity and indexed into existing
64-pixel vertical bands. The separate `shinki_bg_render()` preserves
its true Boss-phase classification at 4, 8 and 12 and its original
GRCG/direct-color page operations. These phase values are source
constants only; no new Boss state machine or image data was copied.

The source edit touched the shared `background.cpp` that also compiles
Sara, Louise, Alice, Mai/Yuki, Yumeko and EX-Alice backdrop functions.
Every one of the **17 complete accepted background CODE scopes**, plus
the independently accepted two-byte C seed contributor, was therefore
replayed in one focused native batch. The two independent pinned
Borland producers match all original raw bytes, OMF/MAP boundaries,
ordered relocations and their compiled negative controls, including
the original 306-byte A-type initialization, 224-byte B-type part1,
281-byte B-type update, 332-byte C-type update, and 173-byte final
Shinki background router. Receipt:
`.analysis/unit-replays/gpt-web-bg-particles-seed-shinki-a/receipt.json`.
The source paths are semantic improvements to already accepted CODE,
not new CODE byte credit. No other source owner or full-game cold replay
was run.

## All original Shinki/Extra Alice C publics joined to real C++ consumers (2026-11-12)

The complete Shinki and EX-Alice background native code now imports the
original independent C DATA publics through the **single**
`background_rules.h` interface. The physical source definitions remain
separate initialized-DATA contributions: zoom count at `22358` (one byte),
particle sentinel at `2235A` (two bytes), type-B gate at `2235C` (one),
B/C spin clock at `2235E` (two), type-C and type-D gates at `22360..22361`
(two) and EX-Alice hexagram direction at `22362` (one). The alignment
zeros at `22359`, `2235D` and `22363` and all unidentified downstream
zeros remain outside the source-owned intervals.

The header's actual `extern "C"` declarations use one-byte character,
16-bit integer, or—specifically for the EX-Alice three-state flag—the
original one-byte C++ `hexagrams_flag_t` **enum**. The enum's values
0/1/2 and `FLAG_COUNT` are now named at file scope; the earlier
function-local `extern` is no longer needed. The C producer still owns
one unsigned byte at the original public `_hexagrams_flag`; no copy or
additional enum object exists. The original one-byte type assertion
stays in the actual animator function, so Borland's byte-level
integer promotion, rotation direction reversal and jump structure
are still directly tested against the target.

Seventeen complete original `background.cpp` CODE scopes were recompiled
twice with all their actual OMF/MAP contexts, full raw equality and
literal ordered MZ fixups. Each of the **five** independently affected
C source-defined DATA contributions was separately recompiled twice,
with its own compiled initializer mutation rejected. Unmodified complete
959-byte Shinki and 1,060-byte EX-Alice Boss state machines were also
selectively tested by the same native acceptance lane, with their own
negative controls. Receipts:

- `.analysis/unit-replays/gpt-web-shinki-all-background-c-publics-a/receipt.json`
- `.analysis/unit-replays/gpt-web-bg-abi-counter-b/receipt.json`
- `.analysis/unit-replays/gpt-web-bg-abi-seed-b/receipt.json`
- `.analysis/unit-replays/gpt-web-bg-abi-bflag-b/receipt.json`
- `.analysis/unit-replays/gpt-web-bg-abi-spinline-b/receipt.json`
- `.analysis/unit-replays/gpt-web-bg-abi-late-b/receipt.json`
- `.analysis/unit-replays/gpt-web-bg-abi-large-boss-callers-b/receipt.json`

All these objects and CODE were **already accepted** in their separate
physical ranges. This change recovers the true cross-source C ABI and
the original enum type, not a second claim over original bytes or a
claim about full-program relocation success. No full cold replay ran.
