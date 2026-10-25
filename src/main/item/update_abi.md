# Parked item update and abandoned long borrow

The original complete MAIN `items_update` occupies `[0x1D0AD,0x1D19E)`,
241 instruction bytes, frame `1527`, group `main_03`. Coordinates are MZ
program-image offsets in locally attested MAIN, SHA-256
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
There are no tables or padding; the original ordered MZ offsets are
`[208,66]`. This function remains unaccepted and receives no credit.

The maintained source has been restored byte-for-byte to the semantic-safe
named-point implementation that produced 248 bytes. Its SHA-256 is
`e863440312e9d2f10934787a56ddfee85404a8ebe103197733ba656aaa35e7de`,
matching `.analysis/item-update-before-abi.cpp` and the old retained source.
The full item20, Motion12, Point4, forty-slot pool, word attraction flag and
all real prototypes/headers remain unchanged.

The one authorized return-borrow trial generated 235 bytes and was stopped
after its first producer in `main-items-update-abi-a`. There was no second
positive or compiled negative. The proposed pull-speed mutation from 10 to
11 was not compiled and is not claimed rejected. Its actual source and
artifacts remain preserved under that failed producer.

The packed method ABI itself was correct: the same 32-byte `update_seg3`
updates the real Motion, returns X in AX and Y in DX, and uses near-this
RET2. The trial correctly consumed those words for immediate clipping and
top clamping. DX also remained the required pre-clamp Y through pickup.
The failure occurred later in ordinary expression evaluation: at
`0x1D154`, the compiler loaded player X into AX, overwriting returned item X.
At `0x1D15A`, it emitted SUB AX,AX, making the X pickup distance zero. The
X bound therefore always passed. The Y expression still consumed original
DX at `0x1D167`, but that does not repair the lost X coordinate.

Both pickup blocks used AX encodings rather than the original BX encodings,
shortening each block by three bytes: `241-6=235`. The code-size mismatch
also shifted the bounded foreign DATA context; those offsets are not new
record-field evidence. This was an actual long-lifetime protocol failure,
not a false pointer return or a Motion-layout problem.

The safe source preserves the pre-clamp returned coordinates in the true
point local. Replacing returned Y with current item Y would still be wrong:
the real record is clamped before pickup, while pickup must retain the old
returned Y. No BX arithmetic kernel, register assignment, inline ASM,
compiler flag, alternative return type, helper, alias, padding or further
borrow variant is proposed. The accepted immediate-return mechanism in
stage653 and shot408 remains valid; a no-call window alone did not extend
that evidence through these ordinary pickup expressions.

Detailed native evidence is `.analysis/item-update-abi-protocol-result.json`.
The original ABI/lifetime review and failed proposal remain in
`.analysis/item-update-motion-abi-review.json` and
`.analysis/item-update-abi-unit-proposal.json`. The existing binder and all
accepted source/header files are untouched. Current safe248 source presence,
failed235 output and exact241 acceptance are separate claims; the last has
not been achieved.
