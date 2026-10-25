# Shot update and packed-return ABI

Accepted `shots_update` covers the complete original MAIN function at
`[0x133DB,0x13573)`:400 instruction bytes followed by its8-byte semantic
switch table at relative `[400,408)`. Coordinates are offsets in the
unrelocated MZ program image of locally attested MAIN, SHA-256
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
Its frame is `0AE1`, group `main_01`. The near RET is at `0x1356A`.
Every direct branch and table target is an original instruction start.
There is no padding; the two original ordered MZ fixups are `202,112`.
No initialized DATA or BSS belongs to this owner.

The complete canonical Point4/Motion12, Shot18, alive-cache6 and hitshot14
records and all actual method declarations remain unchanged. The real
`PlayfieldMotion::update_seg1()` still returns `PlayfieldPoint`, consumes
one near-this stack word and returns through RET2. The actual32-byte
implementation writes previous/current state and returns new X in AX,
new Y in DX. Pinned ReC98's `th04/main/playfld.hpp` explicitly documents
this direct register access. Actual old typed-result producers copy AX/DX
into point fields directly; this is a packed value, not a far pointer.

The sole new mechanism is explicit, limited result consumption through
real DOS compiler intrinsics. Both original Motion calls stay intact,
followed immediately by four readonly signed comparisons of their actual
AX/DX words. The bounds remain x/y<=-128, x>=6272 and y>=6016. No arithmetic
or assignment is performed on those registers, and no fake scalar/void
prototype, helper, class view, flag condition or compiler-body template is
introduced. The origin is therefore recorded honestly as
`compiler-generated-cxx-dos-intrinsics`.

For surviving live shots, both returned coordinates are written to their
actual cache x/y fields before changing the cached Shot pointer, advancing
the cache or incrementing counters/age. These correspond to original stores
at `0x134EE` and `0x134F0`; no intervening call or register-clobbering
operation occurs. If clipped, the result is dead once removal is chosen.
The hitshot return is used only by immediate clipping; ensuing age updates
and modulo/division occur after its last use. No register value is borrowed
across any subsequent call or arithmetic.

The previous full source is preserved at
`.analysis/shot-update-before-abi.cpp`; reversing the precise return-use
substitutions and genuine DOS-header include restores it byte-for-byte.
The first ABI replay restored the full408-byte size and original ordered
fixups, but both raw comparisons still failed at the homing byte updates
and shared AL store. That failed parent remains preserved; it was not raw
exact. The final source keeps the canonical `Shot.angle` declaration as
plain char and uses an unsigned-char near-reference storage view only at
its +=/-= operations, matching the logical modulo256 byte angle. This is
a genuine character-storage view of the existing field, not a replacement
record, new alias field, physical-register hint or optimizer barrier.
Acceleration, iteration, all other homing semantics and decay remain intact.
The older typed-return431-byte producer is retained separately as a failure.

The same genuine return-boundary mechanism passed the independent653-byte
stage-two owner in `main-stage2-update-abi-a`, but that acceptance does not
transfer to this consumer. Native protocol evidence for both methods and
both shot call lifetimes is retained in
`.analysis/motion-return-abi-review.json` and
`.analysis/shot-update-abi-boundary-review.json`.

The proposal is `.analysis/shot-update-abi-unit-proposal.json`, using the
unchanged maintained `probes/units/shot_update_bindings.asm`. That binder
supplies actual foreign entry/state symbols and no implementation, parent
contribution, table values or stack. The original own negative changes
missile vertical acceleration from4 to5, affecting real trajectories.
Accepted focused replay `main-shots-update-abi-b` proves two fresh
deterministic producers, all408 raw bytes including the eight semantic
table bytes, original ordered relocations `[202,112]`, and valid OMF. The
compiled acceleration mutation4-to5 changes output and is rejected. Its
receipt is `.analysis/unit-replays/main-shots-update-abi-b/receipt.json`.
The control covers the complete owner, not every homing branch separately.
The first ABI parent and earlier typed-result failure remain unaccepted.
Source, headers and binder are now frozen.
