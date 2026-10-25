# Complete BGM measure wait

The natural GAME5 wait loop follows pinned ReC98 `th05/snd/delaymea.cpp`.
It queries the current music measure, uses the real VSync fallback when music
is disabled, and otherwise polls until the signed target measure is reached.
Its genuine API is far Pascal with signed-word measure and unsigned-word
fallback-frame arguments, ending in RETF4. The fallback provider remains far
Pascal with one word argument and RETF2.

| Decoded artifact | Complete wait scope | Compared | Authored instructions | NOP | Ordered fixups |
| --- | --- | ---: | ---: | ---: | --- |
| OP | E0F1..E113 | 34 | 33 | relative17 | `[]` |
| MAINE | F265..F287 | 34 | 33 | relative17 | `[]` |

Both complete native scopes have only the one linker-relaxation NOP; it is
compared normally with zero authored credit. No tables or owned DATA/BSS are
present. The following explicit original zero is outside each scope and gets
no credit. Decoded equality does not claim packed or whole-executable equality.

The literal wait body and genuine declarations remain unchanged from the old
candidate. The new `wait_common.cpp` drops only its unsupported harness CODE
group. Pinned source specifies SHARED without a CODE group, and actual checksum-
valid OP/MAINE calibration `snd_dlym.obj` and `frmdelay.obj` have only DGROUP for
DATA/BSS. This independently supports the new ordinary context. Historical
original-project/TU identities are still unproved.

The69-byte compiler contribution includes unchanged maintained `measure.cpp`:
that real local provider is needed for the native four-byte local far call.
Both full69-byte outputs and original empty relocation lists match in both
artifacts. Previously accepted35-byte query rows, their source/object identities
and authored credit are unchanged. Only the later34-byte function is imported.

Actual common public SHARED before/CPP/after layout supplies the true forward
far frame_delay public at OP E15E / MAINE F288, preserving CS D30/E80 and DS
EFE/1011. The old binder had the same group/frame but a different public SEGDEF
for that callee, leaving9A and an extra relocation20. A zero-C++ diagnostic
relinked the retained OP object unchanged in a genuine common SEGDEF and
matched all69 bytes. That diagnostic retained the old harness group and supplies
no acceptance. Its result did not justify a fake near API or emitted call.

Only these new receipts supply acceptance:

- `.analysis/unit-replays/op-sound-wait-common-a/receipt.json`, SHA-256
  `406366a994eca039020eaefb508d58a52917bfa75b0a3d4ad785343367104b3f`.
- `.analysis/unit-replays/maine-sound-wait-common-a/receipt.json`, SHA-256
  `6409683a3364728a43384436c62a301cd31139e67ac2e5648fea755af776b30d`.

Each supplies two fresh deterministic actual OMF/MAP/MZ producers, correct
no-CODE-group context, complete raw/order checks and an own compiled `<0` to
`<=0` negative. The negative wrongly treats valid music measure0 as disabled,
changes selected byte12, keeps the complete34-byte scope, ordered relocations
and binding models, and is rejected. Both use the actual binaryO compiler
context, including MAINE's reference exception. Installed execution proofs and
unrelated accepted objects are reused.

The old standalone35-byte attempt and grouped `op-sound-wait-d` raw/fixup
failure remain unchanged and unaccepted. New symbolic binders provide no code,
values, stack, entry, inside-function gap, fixup sorting or byte normalization.
No source body, provider declaration, callback ABI or optimizer sweep is used
to manufacture relaxation.
