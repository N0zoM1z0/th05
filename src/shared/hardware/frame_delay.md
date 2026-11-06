# Shared VSync frame delay

`frame_delay.cpp` recovers the complete 21-byte function independently in MAIN,
decoded OP and decoded MAINE. Each has six instructions, no instruction NOP,
table, padding or MZ relocation. The old MAIN prefix survey's 22nd byte is a
foreign zero after the actual `RETF 2`; it is outside every accepted scope.

| Artifact | Complete load scope | CS | DS | VSync word offset | Receipt under `.analysis/unit-replays/` |
| --- | --- | --- | --- | --- | --- |
| MAIN | `[15102,15117)` | 14AB | 209D | 267A | `main-frame-delay-exact/receipt.json` |
| OP | `[E15E,E173)` | 0D30 | 0EFE | 2E4E | `op-frame-delay-exact/receipt.json` |
| MAINE | `[F288,F29D)` | 0E80 | 1011 | 1DCA | `maine-frame-delay-exact/receipt.json` |

The function has a real FAR Pascal boundary, one signed word argument and
callee cleanup. Borland's `peek` reads that argument from SS:SP+4 into BX;
this is argument transport, not a register-based replacement of an algorithm.
It then clears the IRQ-owned volatile unsigned word and polls it against the
unchanged bound. The unsigned comparison preserves zero waits and negative
arguments' unsigned word interpretation. No new defensive handling is added.

The maintained TH04 `src/shared/hardware/frame_delay.cpp` supplies the same
counter/reset/comparison semantics in ordinary C++. Pinned ReC98 b6ba5b0a's
`th05/frmdelay.cpp` supplies the TH05 stack-boundary evidence. Its handwritten
argument-load instruction is replaced by the genuine DOS intrinsic, as in the
already accepted TH05 scroll conversion; its appended zero is not copied.
Neither reference supplies acceptance for these three target occurrences.

The binders contain only the original segment context, foreign extents and
external VSync labels. Source owns no initialized DATA or BSS. Each focused
replay passes two deterministic producers, valid compiler OMF, all 21 raw bytes
and the empty original ordered relocation stream. Its staged reset-to-one
mutation is compiled and rejected. Unchanged accepted units are reused.

Receipt SHA-256, in table order:

* `3f993167b8c9bca9a5cffa8a31c5c30b5d2983bfe46d73534f6185dca402543d`
* `45f50dd52bc907b12f10399dabc59afe4b075f43621b4e7bb7ac1286b857dca7`
* `00663754b99018bd181b2ca401a91f0e45eba4df5df1ce63e494d7f290f61e54`
