# Extra-stage midboss update

This natural C++ candidate reconstructs the original TH05 state machine using
canonical Boss, midboss, bullet and gather types. TH04 maintained
`src/main/midboss/mx_update.cpp` supplies state-machine conventions; its actual
algorithm differs and its acceptance does not transfer. Pinned ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47` TH05 disassembly supplies behavior
and calling-contract evidence, independently checked against the local original.
There are no instruction templates, inline assembly, synthetic state or barriers.

The complete original MAIN load-image range is `[0x165B6,0x16724)`,366 bytes
and113 decoded instructions. The final RETF is16723 and the next genuine
function starts16724 with PUSH BP/MOV BP,SP. The switch compiles as a comparison
chain: there is no post-RET table or padding. The ordered MZ relocation sites
are166F9 and16651, both the actual far sound service at14AB:0232. Exact
acceptance requires independent fresh producer evidence, not this native review.

The foreign dash helper at163FE takes a word frame argument, returns bool in AL,
and executes RET2 at164A1. It invokes the currently selected real near pattern
callback at DS147A. The first attack pattern at164B6 is only addressed by this
owner and uses the genuine no-argument near bool interface. DS147C is the full
six-entry pattern-pointer table, including two null slots; DS1488 is the full
eight-byte angle table. Their types and bounds are preserved as external DATA;
this owner supplies no table values, assets or helper bodies and claims no DATA.

Source first declares its update callback in main_03 before foreign stage
interfaces. The canonical generic Boss header supplies the single item enum and
bullet-zap union. Empty main_01 and main_03 foreign segments are bound in their
actual groups. All Pascal EXTDEF names preserve uppercase encoding. The maintained symbol-only binder is `probes/units/midboss_extra_bindings.asm`.
The private entry proposal is `.analysis/midboss-extra-unit-proposal.toml`; the original-boundary packet
is `.analysis/midboss-extra-boundary-review.json`. The meaningful negative changes
the second-half health threshold from1000 to1001, preserving all other source.


`main-midboss5-extra-b/receipt.json` accepts this complete366-byte callback.
Both independent fresh producers reproduce every raw byte and both original
ordered relocation sites (relative323,155). The batch's compiled control belongs
to stage five and covers this replay. Credit is one complete function and
366 instruction/authored-code bytes, with no DATA, table or padding credit.
The stage-five function's acceptance is separate from this callback.


This owner's supplementary HP1000→1001 rejection is historically recorded in
`main-midboss-extra-negative-c/receipt.json`: one fresh negative, with both
parent positive producers revalidated and reused. The retired checker remains
in Git history at `3af324e`. This additional experiment is not an acceptance
requirement.

## Shared Extra midboss attack-state source

The complete Extra update and its five near movement/pattern functions now
share `MidbossExtraScratch`, a size-16 view of the original Boss scratch bytes.
Byte 12 selects the early or late pattern set after HP falls below 1000,
byte 13 holds the rotating accelerating ring's signed step as a wrapping
byte, byte 14 counts completed dashes, and byte 15 tracks the dash animation.
Original near pattern callbacks and their two-row/alternating-column table
remain external; no independent state is allocated. The original two-stage
entrance/attack and final explosion switch retains the same keys and timing.

A native compiler-shape finding matters here: the original Borland expression
`midbossx_patterns_done & 7` performs an integer promotion *before* masking,
so it emits `MOV AL; MOV AH,0; AND AX,7`. Declaring the named mask as an
`unsigned char` changed that to `AND AL,7; MOV AH,0`, shortened the complete
owner to 365 bytes and failed exactness. Giving the mask its correct `int`
type recovers the original 366-byte code and both fixup sites. The working
source is ordinary C++ with a real semantic typed constant, not NOP padding.

The final focused replay verifies `main-midboss-extra-update` (366 bytes)
and `main-midboss-extra-patterns` (440 bytes) together, both deterministic
Borland producers matching all **806 original bytes** and ordered relocations.
The shared compiled negative was rejected. Receipt:
`.analysis/unit-replays/gpt-web-extra-midboss-shared-scratch-fixed-20261111/receipt.json`.
