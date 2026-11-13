# Complete EX-Alice update candidate

The complete far Pascal callback covers original MAIN `1A24A..1A66E`,1060
bytes. Its280 instructions occupy1008 bytes through the final RETF. Three
post-return compiler switch tables then occupy8,8 and36 bytes. No alignment
byte is present. All26 table entries point to real instruction starts inside
the complete callback. The original ordered relocation stream is `[198,161]`.

The state machine handles HP fill, entrance, alternating movement/charge
cycles, phase HP thresholds, background palette changes, scripted pattern
selection, timeout transitions, the final fan and defeat. Shared labels express
actual common movement, hit-test and phase-transition paths. Unsigned byte
state/palette arithmetic and signed frame comparisons remain intact. The
existing4-by2 near-callback table is declared semantically without defining
any entries. The full52 bytes of compiler tables remain in the comparison;
no table crop, byte array or alignment repair is supplied.

Accepted phase and pattern headers provide the real Boss24, bullet, Laser24,
GatherTemplate14, custom26 and CheetoTemplate25 interfaces. The full canonical
RGB/Palette ODR definitions are reused from the Shinki header, representing
all48 palette bytes. Direct colors[0].c fields express actual palette storage
without reference-address temporaries. No palette values, assets or initialized
DATA/BSS are defined. Existing accepted sources and headers remain unchanged.

The update's first far declaration is captured in its actual main03 context
before shared setup declarations. BG and custom-render callbacks belong to
main01/AE1, as does the real null callback. Super conversion is far C Pascal
0000:35A2, returning int; sound is far C Pascal14AB:0232. The accepted far
hit gate retains its true far int ABI, including original PUSH CS plus relative
CALL sites. Phase-next uses the actual Pascal explosion-enum/int argument order.
All near game helpers share frame1527. DS is209D.

The independent symbol-only binder anchors even empty foreign compiler
segments in their real groups. Its byte tail follows the entire1060-byte
contribution at1A66E and ends at209D0. It supplies no instructions, initialized
values, stack, inside-function holes or compiler table bytes.

ReC98 `th05_main.asm` lines18695..19093 supplies semantic evidence. The local
original-minus-calibration displacement is `-503F`; all280 complete instruction
shapes agree. Original complete return, direct branches, three indirect table
target sets and ordered relocations were checked directly against pinned MAIN.
Source presence and routing agreement do not establish exactness.

Private metadata `.analysis/exalice-update-boundary-review.json` contains the
complete unit proposal, three table classifications and a unique natural
negative changing initial end-HP23800 to23700. Two fresh focused producers,
full1060-byte comparison, original ordered fixups and compiled rejection remain
required. No compiler was executed during preparation; no module-wide or packed
artifact claim is made.

The saved focused producers `main-exalice-update-a` and `-b` both stop at
the first-positive size gate:1064 versus original1060 bytes. Four external
far calls to the genuine shot gate are emitted as five-byte calls and relaxed
by TLINK to NOP/PUSH-CS/near-CALL, retaining one extra byte each. The original
uses four-byte PUSH-CS/near-CALL sequences. The four extra NOPs explain all
size differences; the semantic instruction shapes and52 table bytes remain
intact. Nothing is removed or normalized for acceptance.

Capturing the true same-CS far declaration before the independent phase
header does not repair the second producer. That source-context hypothesis
is falsified, and no further flag/binding/padding probes are performed. This
complete natural callback remains outside live replay selection, unaccepted
and uncredited. The accepted separate111-byte shot/transition owner is
unchanged. Actual original TU/callee-definition context remains unresolved.

The real adjacent helper-definition context has subsequently been restored
in `full_context.cpp`, using verbatim natural bodies for the33-byte shot gate,
78-byte phase transition and1060-byte updater. This produces the original
short far calls and passes the updater's full raw/ordered oracle as
`main-exalice-update-full-context-a`. The standalone producer above remains
a retained failed alternative; the target callback itself is now accepted
through that coherent source owner. No acceptance transfers from its failed
receipt, and prefix111 is not counted twice.

## 2026-11-12: natural wave transitions in the complete 1,060-byte controller

The accepted `full_context.cpp` now factors all four **regular-wave**
transitions into a single source-level `EXALICE_REGULAR_ADVANCE` rule that
couples the actual explosion/HP ladder step to installation of its next
attack callback. This makes the wave-to-wave data flow explicit without
reordering any phase-case, changing any threshold or inventing another
runtime helper. The two rising-red approach/charge phases of wave 1 also
share the original `EXALICE_WAVE1_RED_APPROACH` palette rule. Its `palette_changed`
latch still updates only on genuine red-channel changes and retains the exact
original fallthrough behavior between phases.

The updated complete controller (not just the four inner branches) passed
focused `main-exalice-update-full-context` strict replay at
`.analysis/unit-replays/gpt-web-exalice-wave-transition-source-a/receipt.json`.
Both genuine compiler/TLINK producers still match **1,060/1,060 original
bytes**, the three real compiler switch tables and the original **ordered**
relocations `[198,161]`; the compiled `EXALICE_HP_SETUP_END` negative is
rejected. The accepted 33-byte shot gate and 78-byte phase-next helper are
still compiled as real preceding context, not substituted by byte templates.
This is a source-coherence refinement to a **previously accepted** major
Boss function and earns no duplicate new authored CODE credit. No other
accepted units were recompiled and no whole cold replay ran.


## 2026-11-14: bomb immunity and HP-vs-time phase-drop handshake

The Extra boss's bomb protection is a countdown plus a phase-specific damage
gate, not a blanket `boss_hittest_shots()` wrapper. `exalice_update()`
decrements `exalice_bomb_invincibility` at the very top of every update, before
phase dispatch. The setup frame initializes it to zero. Damage-gated phases
call `exalice_hittest_shots()`: while `bombing` is true that helper reloads the
latch to **39** and returns the suppressed-shot result; otherwise it calls the
real boss hit test only when the countdown has reached zero. Setup and Ready
instead use `boss_hittest_shots_invincible()` directly, so their existing
invincibility is independent of the bomb latch.

Because the reload occurs after that frame's decrement, the last bomb update
leaves 39. The next 38 non-bomb updates decrement to 1 and still suppress shot
damage; the 39th decrements to zero and reopens the real hit test. Repeated
bombing in a damage-gated phase reloads the full window each update. The timer
is not cleared by `exalice_phase_next()`, so a phase boundary cannot bypass the
remaining immunity.

The phase transition's item-drop condition is a second, independent handshake.
`boss_score_bonus()` first performs the regular boss score update and then sets
`boss_phase_timed_out = false`. `exalice_phase_next()` drops point items and
activates the bullet zap only when the explosion type is not `ET_NONE` **and**
that latch is false; it sets the latch true again after the check. Thus an HP
threshold exit that passed `exalice_hittest_shots()` and scored its 20-unit
bonus drops items, while a regular-wave count limit or strict charge timeout
that jumps around the hit/bonus path does not. A bomb-suppressed shot cannot
clear the latch. This is why the same phase helper has different visible
transition effects for HP exits and timeouts without a separate timeout flag
being passed as an argument.

The same helper then increments the phase, resets frame/mode/pattern count to
`0/REPOSITION/0`, copies the previous `phase_end_hp` into current HP, and
installs the next end-HP threshold. The bomb timer is intentionally absent
from this reset, preserving the cross-phase immunity window.

`tests/test_exalice_boss_protocol.py` covers the exact 39-frame countdown,
the two separate hit gates, the `boss_score_bonus` latch write, HP-vs-time
item-drop behavior, and the full phase transition state reset. The accepted
111-byte phase helper and 1,060-byte full-context updater are locally replayed
after the comment-only source clarification; no instruction bytes are added.


## 2026-11-14: exact 32-callback regular waves and ninth final-charge exit

Each of the four regular waves starts with the callback already installed by
the preceding Ready/charge handoff. A completed charge callback resets the
phase clock to zero and returns the Boss to reposition mode. Each completed
random flystep increments `patterns_seen`, switches to charge mode, and selects
`exalice_patterns_by_phase[wave_index][patterns_seen & 1]`. The table lookup
happens **before** the `patterns_seen >= 32` test. At count 32 the selected
row-zero callback is never invoked: the direct jump to `regular_complete`
bypasses both the callback mode and the normal hit/score-bonus path. Each
uninterrupted regular wave therefore executes exactly 32 attack callbacks: the
preinstalled first callback plus 31 table-selected callbacks.

The actual preinstalled callbacks differ by wave. Wave 1 starts with
`random_fan`; wave 2 with `gravity_stacks`; wave 3 with `fixed_laser_fan` (not a
member of that wave's two-entry bank); wave 4 with `cross_cheetos`. The table
banks remain the original four distinct near-function pairs:

| Wave | Preinstalled callback | Alternating bank | Executed callbacks |
|---|---|---|---:|
| 1 | random fan | random fan / turning rings | 16 / 16 |
| 2 | gravity stacks | gravity stacks / diamond rings | 16 / 16 |
| 3 | fixed laser fan | bouncing rings / speedup fans | 1 fixed + 15 / 16 |
| 4 | cross cheetos | cross cheetos / turning cheetos | 16 / 16 |

The uncalled count-32 selection is always bank index zero. This distinction
matters in wave 3: its preinstalled fixed-laser callback is an extra one-off,
while only counts 2..30 invoke the bank's bouncing-ring callback.

The fourth charge wave has a different counter. Every completed callback
increments `patterns_seen`; the strict `> 8` check completes on callback **9**.
That jump also skips `charge_hittest` and its 20-unit score bonus. The ordinary
charge timeout is separately strict `phase_frame > 4000`, so frame 4000 still
runs the hit test and frame 4001 jumps directly to charge completion. These
count/time exits leave `boss_phase_timed_out` true, preserving the phase helper's
no-item-drop behavior; only a successful HP hit followed by `boss_score_bonus`
clears that latch.

`tests/test_exalice_wave_dispatch.py` models all four callback sequences,
the skipped count-32 selection, the nine-callback final charge, the strict
4000/4001 boundary, and the sequential 26,500-to-zero HP handoff. The accepted
1,060-byte full-context updater is replayed locally after the comment-only
clarification; its 52-byte compiler switch tables and original ordered fixups
remain exact.
