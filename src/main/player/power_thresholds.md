# Shot-level power threshold DATA

The complete accepted owner is the nine-word `SHOT_LEVEL_TO_POWER` array at
original MAIN `[2227C,2228E)`, 18 bytes, DS `209D:18AC..18BE`.
The thresholds are 6, 12, 16, 24, 32, 48, 72, 96 and 128. Their meaning is
the power required to cross each successive shot-level boundary, not an
opaque numeric payload or asset.

Original code at `E3E2..E40E` loads the unsigned power byte at DS `36F0`,
sets the loop count to nine, compares AX with a word at `[BX+18AC]`, and uses
an unsigned-below branch. It advances BX by two, divides the byte offset by
two for the shot level, selects the actual shot callback and updates the HUD.
This proves both complete bounds and the unsigned two-byte threshold role.
The source reuses the canonical `uint16_t` ABI definition and asserts all
18 bytes. No helper prototype or accepted caller changes are introduced.

The source is ordinary C++ static initialization. The DATA start is genuinely
word-aligned; no preceding field, padding or extra context is needed. The
symbol-only binder supplies actual MAIN code frames and the DATA prefix
ending at `18AC`, with no source bytes, stack, CODE or internal hole.
Original ordered MZ fixups are empty, and there are zero padding bytes.

The own semantic negative raises the first threshold from six to seven.
`main-shot-power-threshold-data-a` passes two fresh deterministic producers,
complete gapless compiler DATA and MAP contributions, all 18 raw bytes,
original ordered fixups, actual inputs/tools/dependencies and its rejected
compiled mutation. It adds 18 authored initialized DATA bytes and no CODE
or function credit.

Private `.analysis/power-exalice-data-boundary-review.json` records original
instructions, types, complete extent, references and hashes. The adjacent
unit-proposal JSON contains both independently reviewed small DATA owners.
Run `python3 .analysis/power-exalice-data-review.py` for native checks only.
