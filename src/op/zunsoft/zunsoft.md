# ZUN Soft logo: natural C++ source packet

The complete original decoded OP cohort is `B616..BA94`, 1150 bytes:

| Function | Complete extent | Instruction bytes |
| --- | --- | ---: |
| Pyro creation | `B616..B69A` (132) | 132 |
| Pyro update/render | `B69A..B7C5` (299) | 299 |
| Palette update/show | `B7C5..B806` (65) | 65 |
| Logo controller | `B806..BA94` (654) | 606 |

All 380 instructions, terminal returns, direct branches and sparse-switch
destinations are reviewed against the pinned decoded target. The controller's
instruction body ends at BA64. Its twelve word keys occupy BA64..BA7C; twelve
word targets occupy BA7C..BA94. There is no NOP or padding. CS is A39 / op_01,
DS EFE, Master frame 0000 and shared-provider frame D30. Literal original
fixup order for the whole cohort is
`[967,822,796,787,778,769,760,749,711,704,598,587,576,571,564,557,547,540,523,488,413,382,352,311,281,245,91,74,1096,1091,1086,1070,1065]`.

Maintained TH04 `src/op/music/zunsoft*.inl` supplies natural C++ bodies; ReC98
`th04/zunsoft.asm` and `th04/op/zunsoft.cpp` corroborate behavior and the complete
record. TH05 native code determines all actual provider addresses and its input
differences: held reset/sense at each frame's start, no TH04 initial/end-of-frame
reset call, and the real far PI-free call. No donor acceptance transfers.

The full 14-byte pyro contains alive/age, canonical SPPoint origin, previous and
current Subpixel distances, speed, angle and pattern. All 256 slots are retained.
Complete RGB/Palette definitions match the accepted owners; palettes contain all
sixteen colors even though this scene fades only the first fifteen. State and
all six resource-name arrays remain foreign to this CODE source. There is no
owned initialized DATA or BSS, image data, artificial prefix, barrier or assembly
algorithm. Only real page-port I/O uses the Borland hardware primitive.

Creation has four actual Pascal word slots: x at BP+0A, y at BP+08, count at
BP+06 and the sprite byte at BP+04, with RET8. Native callers push high=x/low=y
as a dword before count/pattern. Descriptive scalar coordinates preserve that
binary ABI; the reference's grouping into a screen-point parameter and original
historical source spelling remain unproved. The updater is near/noargs, the
palette helper is near Pascal with RET2, and the controller is near C++/noargs.
SI/DI/BP are preserved. First declarations retain the complete own code context
and genuine external near/far provider frames. The source preserves signed
division/random remainders, latched skip, per-frame ordering and unchecked APIs.

Private proposal: `.analysis/op-zunsoft-unit-proposal.json`. Native/source/ABI
review: `.analysis/op-zunsoft-native-review.json`, SHA-256
`9f5f028a3a56700d90886b98a4a95a6adde2507e9c6936b499e46901e2703d84`.
The ordinary shared control changes spawn-speed bias 64 to 65. The focused `op-zunsoft` replay passes with two independent cold producers:
all 1150 raw bytes and all 33 ordered fixups match, and the compiled speed-bias
negative differs as required. The complete four-function CODE scope is accepted
in `config/accepted_units.op.json`; the receipt is
`.analysis/unit-replays/gpt-web-op-zunsoft-20261110/receipt.json`. Target provenance is
candidate-local-attested; there is no packed-file or whole-program claim.


The first actual diagnostic is
`.analysis/native-producers/op-zunsoft-a/native-diagnostic.json`, SHA-256
`e6b0709a0805b577d40aa3e2b3e19eb11d9aa14a67050a8316dcc93cb2acb163`.
The source ABI review confirms the existing Pascal-far `super_free` declaration.
`pc98_gfx.hpp` uses `MASTER_RET`; `libs/master.lib/func.hpp` selects `MASTER_FAR`
for `__LARGE__` and expands `MASTER_RET` to `far pascal`. The distinct
`MASTER_CRET` macro supplies `far cdecl`. Absence of `MASTER_CALL` therefore did
not imply cdecl. This correction changes documentation only; source and binder
remain frozen. The original diagnostic was only a preliminary result; formal replay has
since independently accepted the same source and binder.

## Separate filename source: accepted initialized DATA

`filenames.cpp` holds six mutable source-name arrays in original order,
covering exactly 54 native bytes at decoded OP `FECA..FF00` / DS `0EEA..0F20`.
Two independent compiler producers match every DATA byte, and the compiled
filename mutation changes the owned DATA as expected. The binder retains
foreign DATA after the six strings through the already accepted Music Room
DATA endpoint DS:2817, which supplies sufficient original context for a valid
DOS MZ image without fabricating a stack. Only the six strings earn DATA
credit. This is an independent `op-zunsoft-filenames` acceptance, receipt
`.analysis/unit-replays/gpt-web-op-zunsoft-filenames-b-20261110/receipt.json`.
Image/font payloads and unrelated initialized DATA remain foreign.
