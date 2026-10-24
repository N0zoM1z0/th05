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
ordered relocation sites (relative323,155). The separately compiled HP
threshold1000→1001 mutation is rejected. Credit is one complete function and
366 instruction/authored-code bytes, with no DATA, table or padding credit.
The stage-five function in the same receipt has its own producer group and
control; its acceptance is separate from this callback.
