# EX-Alice spiral/gather attack: exact C++

MAIN `19FAE..1A0FC` is one complete 334-byte near bool callback: 107
instructions, two returns, no NOP, padding or table. All 15 direct branch
destinations are instruction starts. CS is `1527` / `main_03`, DS `209D`;
the two original ordered segment fixups are `[86,256]`, both real far
Pascal sound calls at `14AB:0232`.

The C++ body is unchanged from the maintained final-pattern source. It adjusts
the shared origin, gathers alternating circles, mirrors fixed-speed fans,
accelerates/decelerates byte-angle state and captures the player's X position
when the sweep finishes. Signed frame remainders, unsigned angle wrap and all
canonical Boss24, BulletTemplate14, Custom26/Cheeto25 and Gather14 types remain
unchanged. Game state and providers remain external; no DATA or BSS is owned.

The previous direct full-TU producers matched every raw byte but emitted
fixups `[256,86]`. The existing `tcc-s-tasm32` recipe now compiles this complete
callback alone, assembles the unedited compiler text and links the symbol-only
binder. It matches all 334 raw bytes and the original ascending order. This is
compiler-generated C++ acceptance, with no original-ASM ownership claim.
ReC98 `th05_main.asm` lines 18452..18581 supplies candidate semantics only;
historical source/TU boundaries remain unproved.

`spiral_gather.inl` is the single canonical body included by both the original
four-function context and the standalone producer. Substituting it back into
`final_patterns.cpp` reconstructs that file's previous bytes exactly. The three
accepted neighboring functions were replayed because their source input
changed; all retain their original 475 bytes, functions and ordered fixups.
Their replacement receipt adds no credit. All other accepted records remain
identical, and no shared header or build tool changed.

Two fresh independent compiler/assembler/linker chains have identical generated
assembly, normalized OMF, MAP and MZ identities. Actual OMF owns one 334-byte
CODE LEDATA record and empty DATA/BSS. The compiled radius 256-to-257 control
is rejected while retaining the full extent and original fixup order.

New receipt: `.analysis/unit-replays/main-exalice-spiral-compiler-assembly-b/receipt.json`,
SHA-256 `955968f00fa9aa1e17a19214e4d29334d5c6ea98a3606654896f1a2cf5ee9b98`.
Affected neighbors: `.analysis/unit-replays/main-exalice-final-shared-body-c/receipt.json`,
SHA-256 `232876579ad3a084ae66d60c8c0f37b4ed87fa8e06be306041899d6c300f3c27`.
Native/source review: `.analysis/exalice-spiral-compiler-assembly-native-review.json`,
SHA-256 `8b7e1b6986636faacad6b711776cc385a12b6e2e917c12253ae9ade64281a30c`.
The earlier single producer is diagnostic only. Target provenance remains
candidate-local-attested. Net new coverage is one function / 334 C++ instruction
bytes; no complete executable or global percentage is claimed.

## 2026-11-13: typed later-pattern scratch overlay

The spiral's turn controller and acceleration step are now named through the
`ExAliceLaterPatternState` view of the original `boss_statebyte`: `turn_phase`
is byte 13 and `spiral.acceleration_step` is byte 14. The adjacent firewave
pattern reuses byte 13 for its own turn phase and byte 14 as its bullet angle.
Both attacks initialize their own pair at their existing entry frame; this is
sequential reuse, not persistent cross-pattern state. The independent
byte-15 `spiral_angle_offset` remains unchanged. Compile-time assertions pin
the complete 16-byte Boss scratch layout and both absolute offsets.

The complete 334-byte spiral function was recompiled through the existing
TCC-S/TASM32 pipeline: both compiler stages preserve all raw bytes and the
original ordered fixups `[86,256]`; the compiled radius mutation is rejected.
The seven other accepted EX-Alice units that include the shared header were
also replayed as complete owners, including the 600-byte firewave/later
cohort and 1,060-byte update controller. All remain byte/fixup exact. These
are source-semantic refinements to existing accepted owners, with no duplicate
instruction credit.
