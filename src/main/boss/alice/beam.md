# Alice puppet-beam exact natural C++ reconstruction

This single complete algorithm occupies original MAIN
`[1E602,1E764)`:354 instruction bytes,102 instructions and four near-cdecl
returns. It has no compiler table, padding, initialized DATA or BSS.
The actual ordered loader-fixup offsets are `[350,235,219,133]`.
All local direct branches land at reviewed instruction starts.

The function waits until both puppets stop moving, charges their beam,
contracts the gather circles, changes the beam animation state, performs
shot/player collisions and emits periodic aimed bullet stacks. The unsigned
beam timer/window and signed Boss frame modulo operations remain distinct.
Shot collision uses a56-by8-pixel radius around the beam center; player
collision retains the different half-open horizontal/vertical bounds and
16-bit unsigned wraparound. No gameplay correction or cap is added to the
original growing burst window.

The complete26-byte puppet overlay retains both flags, full motion, phase
frame, radius union, pattern, HP, word damage and the original signed 16-bit
`padding` word at offset24. This is not a guessed field: the pinned original
`th05/main/boss/b3puppet.hpp` declares `int16_t padding` after
`damage_this_frame`, and the maintained layout now mirrors that exact source.
Puppets occupy slots0 and1 of the existing canonical26-byte custom pool. Boss24, BulletTemplate14, Player motion and four-byte points are reused
without changing an accepted definition. Whole coordinate objects have no
padding, so their32-bit storage comparison expresses both coordinate equality
tests directly. The stack assignment combines the two actual adjacent count
and speed fields; it supplies no opaque data or instruction array.

ReC98 `th05_main.asm`, lines11708..11830, supplies candidate semantic evidence
under the old `sub_19CB0` name. The cached calibration routes the same complete
102-instruction shape at19CB0..19E12, relative to the independently anchored
Alice callback. Calibration addresses and donor acceptance do not transfer.
The private packet contains the actual original hashes, branch/return checks,
helpers, globals and source identities.

One important observed interface is the shot-hitbox consumer. It is a real
far entry at`0AE1:8A02`, taking no stack arguments and returning damage in AX;
the original caller stores that result in a word local and tests it. The old
reference also declares it FAR. It remains foreign, with no supplied helper
body. Sound is the real far Pascal entry at`14AB:0232`; regular bullets are
near-cdecl at17204. The two-byte tuning callback is the actual near Pascal
pointer at DS41DE. Near code uses frame1527 and globals use DS209D.

The independent binder contains symbol addresses and outside-function context
only. Its empty foreign CODE segments retain their actual group frames;
DATA/BSS remain word-aligned, no ORG exceeds64KiB, and no stack, instruction,
initialized value or inside-function hole is supplied. Source and options
follow the existing MAIN large-model compiler contract.

Accepted unit: `main-alice-puppet-beam`, wrapper `th05/a_beam.cpp`,
`B4_UPDATE_TEXT/main_03`. Two independent fresh deterministic producers
reproduce all354 raw bytes and all four original ordered fixups. The compiled
beam-width56-to-55 mutation is rejected. Credit is one complete function and
354 authored instruction bytes; there is no owned table, executable padding,
initialized DATA or BSS. The later padding-field source-name correction below
was separately replayed across every dependent accepted Alice unit.

## Puppet tail-word provenance (2026-11-13)

The final two bytes of `AlicePuppet` are named `padding`, not `unused_24`.
The original ReC98 `th05/main/boss/b3puppet.hpp` declares the exact tail
field as `int16_t padding` immediately after `damage_this_frame`. Borland's
16-bit `int` is the same two-byte storage word, so the maintained overlay uses
`int padding` plus the existing offset-24 assertion. This is a source-name
recovery only: the field remains unaccessed by the Alice puppet algorithms,
its offset and size are unchanged, and the focused 14-unit replay reproduces
every original CODE/DATA byte, relocation and negative-control rejection.

## Shared beam-state semantics (2026-11-11)

The original animation protocol is now named without changing its storage:
`boss_statebyte[9]` selects inactive (0), charging circles (1),
contracting circles / connecting line (2), and paired beam sprites (3).
The adjacent `boss_statebyte[8]` supplies the beam's sprite-pattern offset.
Alice's beam controller writes these states at its 16-, 32- and
64-frame milestones; actual beam attacks start at frame 80. The puppet
motion owner suppresses shot damage during sprite phase 3, and the
puppet foreground renders each corresponding circle, line or sprite.
Both the standalone sources and the coherent Alice foreground/update
translation-unit contexts use the same named values. The declarations
are compiler constants and add no BSS or fabricated DATA.

Focused, two-producer original-byte and ordered-relocation replays matched
all five affected accepted extents: beam (354 bytes), puppet render (381),
puppet entrance/movement (643), the complete Alice Boss update including
its alignment/switch table (939), and combined foreground (140). Each
replay also rejected its compiled semantic negative. The verification
receipts are in `.analysis/unit-replays/` under
`gpt-web-alice-beam-semantics-pair2-20261111` and
`gpt-web-alice-beam-semantics-consumers2-20261111`. All five extents
were accepted before this semantic-naming change; no duplicate credit is added.
