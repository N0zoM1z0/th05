# Final EX-Alice patterns candidate

Four complete patterns cover original MAIN `19EB2..1A1DB`,809 instruction
bytes and265 instructions. No table, padding, initialized DATA or BSS occurs.
The next far hit gate and phase-transition helper are separate owners.

| Function | Original extent | Bytes | Original ordered fixups |
|---|---|---:|---|
| `exalice_pattern_cross_cheetos` | `19EB2..19F41` | 143 | `[124]` |
| `exalice_pattern_turning_cheetos` | `19F41..19FAE` | 109 | `[77]` |
| `exalice_pattern_spiral_gather` | `19FAE..1A0FC` | 334 | `[86,256]` |
| `exalice_pattern_final_fan` | `1A0FC..1A1DB` | 223 | `[176,151,36]` |

The first two combine cross bullets and aimed Cheetos, or alternate aimed
Cheetos while moving. The spiral pattern gathers circles, mirrors fixed-speed
fans, advances unsigned angle state and captures a new player-aligned origin
after deceleration. The final pattern increases fan speed and horizontal
movement radius with HP loss. It preserves signed16-bit HP subtraction,
explicit unsigned32-bit scaling/division, and16 subpixels per pixel.

The full original relocation stream is
`[338,220,124,762,737,622,508]`. In particular, the spiral's two relocation
sites have ascending original order. These identities are not sorted or
normalized, and a whole-contribution verdict is distinct from function scopes.

The frozen pattern, Cheeto, gather and math headers supply complete Boss24,
BulletTemplate14, custom26, CheetoTemplate25 and GatherTemplate14 types. Real
unused fields and overlay storage remain present. Palette11 is a word; stored
angles and gather angle delta are bytes. Negative angle values are explicit
integral byte conversions, without negative floating conversion. The final
gather call uses the proven actual color order `(frame-64,6,7)`.

Near helpers share frame1527. Sound and polar are far Pascal at14AB:0232 and
14AB:0394. DS is209D, with the persistent sweep coordinate at199A. The binder
supplies only actual foreign labels and holes outside compiled functions.
Its byte-aligned tail follows1A1DB, anchors the real Cheeto producer at1A82E,
and ends at209D0. No instructions, initialized values, stack or internal
padding are supplied.

ReC98 `th05_main.asm` lines18326..18660 supplies semantic evidence. Reference
`1EEF1` maps to original19EB2; the preceding reference1EE2F already belongs
to the laser-pattern owner. All four complete instruction shapes, original
returns, local branches and ordered fixups were checked natively. Source
acceptance remains a separate compiler-oracle decision.

Private `.analysis/exalice-final-patterns-boundary-review.json` provides the
whole809-byte entry and optional complete-function scopes. The meaningful
staged negative increases the first Cheeto speed3 to4. Two fresh focused builds,
full raw/fixup comparison and compiled rejection remain required. No compiler
was executed during preparation; existing accepted files remain unchanged.

The first focused producer emitted787 rather than809 bytes: conditional aim
arguments factored argument construction out of both calls (-8 bytes each),
and two conditional angle assignments shared their stores (-3 bytes each).
Actual original control/data flow supports branch-local complete aim calls
and branch-local assignments. Expressing those natural branches preserves
the true Subpixel/byte ABI and arithmetic, with no flags, register hints or
barriers, and restores all809 raw bytes.

`main-exalice-final-scopes-b` accepts three complete functions: cross cheetos
143, turning cheetos109 and final fan223 (475 instruction bytes total). Both
fresh producers pass every selected function's full raw bytes, actual public
return boundary and original ordered fixups. One real cheeto speed3→4 control
is compiled in the first function; no separate negative per sibling is claimed.

The spiral/gather function remains unaccepted. A separate read of both saved
positive MZ files confirms all334 raw bytes, but the original ordered fixups
are[86,256] and both producers emit[256,86]. No sorting or normalization is
applied, and no credit is granted for those334 bytes or a whole809-byte owner.
All compiler instructions remain in the real TU so accepted neighbors retain
their correct physical context. No DATA, BSS, tables or padding receive credit.
