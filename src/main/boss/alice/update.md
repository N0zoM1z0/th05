# Alice update candidate

The complete candidate covers original MAIN `1E957..1ED41`: the genuine
63-byte final spread followed by Alice's full939-byte far callback. The
callback contains908 instruction bytes, one zero alignment byte and a
30-byte compiler switch table after its final RETF. Together the two
functions contain971 instruction bytes and253 instructions. The original
ordered relocation offsets are `[196,59]`.

The spread configures a periodic13-way red fan. The callback handles entrance,
HP thresholds, random movement, puppet initialization, pattern selection,
beam windows and defeat. Shared state and callback tables remain foreign
semantic objects. No asset payload, pointer-table entries, target instruction
arrays or artificial helper bodies are supplied.

The frozen beam header supplies the full26-byte Puppet and canonical Boss,
motion, bullet and player types. The frozen gather header supplies its real
14-byte template. The actual puppet dispatcher pushes a near puppet reference
and consumes AL; all four callbacks load that argument and return RET2.
Their declarations therefore use real near Pascal reference-taking bool
functions. The separate main-pattern callbacks are near cdecl void functions.
The existing4-by3 pattern table stores24 bytes of near function pointers.

All near MAIN03 calls use frame1527; sound is far Pascal14AB:0232 and the
background callback belongs to main01/AE1. Its first declaration preserves
that context before the common stage header. DS is209D. The binder places
only foreign symbols and outside-contribution layout holes. It defines no
instructions, initialized data, stack, or hole within the1002-byte candidate.
The genuine odd-sized prefix and the real `-a2` option after canonical types
preserve the callback's table alignment without changing accepted layouts.

ReC98 `th05_main.asm` lines12019..12355 supplies the semantic reference.
Cached calibration has identical complete instruction shapes at1A005 and
1A044; it provides routing evidence only. Original complete return boundaries,
direct branch destinations, all15 table destinations and ordered fixups were
checked natively. Source acceptance still requires the focused exact oracle.

Private integration metadata is
`.analysis/alice-update-boundary-review.json`, including the proposed whole
unit and a unique staged mutation of the real initial HP threshold7400 to7300.
No compiler, emulator or Ghidra was run during this preparation.
